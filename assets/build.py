#!/usr/bin/env python3
"""Generate every self-hosted SVG used by the Zibgame profile README."""

from builder.github_data import fetch_contributions, fetch_profile
from builder.render import render_all
from builder.semantic import write_semantic_profiles


def main() -> None:
    print("Building Zibgame security profile...")
    stats, languages = fetch_profile()
    contributions = fetch_contributions()
    print(f"  stats={stats} languages={len(languages)} calendar={len(contributions)}")
    render_all(stats, languages, contributions)
    write_semantic_profiles(stats)
    print("Profile assets ready.")


if __name__ == "__main__":
    main()
