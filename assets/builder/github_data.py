"""Fetch GitHub data at build time, with stable offline fallbacks."""

from __future__ import annotations

from collections import Counter
import json
import os
import re
import urllib.request

from . import config


def _json(url: str):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "zibgame-profile-builder",
    }
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def fetch_profile():
    """Return profile stats, repositories and aggregate language percentages."""
    try:
        user = _json(f"https://api.github.com/users/{config.USERNAME}")
        repositories = []
        page = 1
        while True:
            batch = _json(
                f"https://api.github.com/users/{config.USERNAME}/repos"
                f"?per_page=100&page={page}&type=owner"
            )
            repositories.extend(batch)
            if len(batch) < 100:
                break
            page += 1

        stats = {
            "repos": user.get("public_repos", len(repositories)),
            "stars": sum(repo.get("stargazers_count", 0) for repo in repositories),
            "followers": user.get("followers", 0),
            "following": user.get("following", 0),
        }

        totals = Counter()
        language_attempts = 0
        language_failures = 0
        for repo in repositories:
            if repo.get("fork") or repo.get("name") in {config.USERNAME, "zibgame.github.io"}:
                continue
            language_attempts += 1
            try:
                totals.update(_json(repo["languages_url"]))
            except Exception as exc:  # one repository must not break the profile
                language_failures += 1
                print(f"  language fetch skipped for {repo.get('name')}: {exc}")

        if language_attempts and language_failures > language_attempts // 4:
            print("  language coverage incomplete; using the last stable snapshot")
            return stats, list(config.FALLBACK_LANGUAGES)

        language_total = sum(totals.values()) or 1
        languages = [
            (name, round(value * 100 / language_total, 1))
            for name, value in totals.most_common(6)
        ]
        return stats, languages or list(config.FALLBACK_LANGUAGES)
    except Exception as exc:
        print(f"  GitHub API unavailable: {exc}; using fallback data")
        return dict(config.FALLBACK_STATS), list(config.FALLBACK_LANGUAGES)


def fetch_contributions():
    """Read the public contribution heatmap levels rendered by GitHub."""
    try:
        request = urllib.request.Request(
            f"https://github.com/users/{config.USERNAME}/contributions",
            headers={"User-Agent": "Mozilla/5.0"},
        )
        with urllib.request.urlopen(request, timeout=20) as response:
            html = response.read().decode("utf-8", errors="replace")
        levels = [int(value) for value in re.findall(r'data-level="([0-4])"', html)]
        if levels:
            return levels[-371:]
    except Exception as exc:
        print(f"  contribution calendar unavailable: {exc}")
    return [0] * 371
