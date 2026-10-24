"""Generate the standalone, machine-readable profile document."""

from __future__ import annotations

from pathlib import Path

from . import config


ROOT = Path(__file__).resolve().parents[2]
PROFILE = ROOT / "PROFILE.md"


def _project_table(projects: list[tuple[str, str, str, str]], *, personal: bool = False) -> str:
    lines = ["| Project | Description |", "|---|---|"]
    theme_names = {key: title.title() for key, title, _, _ in config.PERSONAL_THEMES}
    for name, url, category, description in projects:
        if personal:
            theme = theme_names[config.PERSONAL_PROJECT_THEME[name]]
            description = f"**{theme}** · {category} — {description}"
        else:
            description = f"**{category}** — {description}"
        lines.append(f"| [{name}]({url}) | {description} |")
    return "\n".join(lines)


def semantic_markdown(stats: dict) -> str:
    tools = " · ".join(config.TOOLS)
    projects_42 = _project_table(config.PROJECTS_42)
    personal_projects = _project_table(config.OTHER_PROJECTS, personal=True)
    return f"""# 🧑‍💻 42 Student — Zibrian Cadinot

I am an **offensive cybersecurity developer, ethical hacker and low-level security researcher** studying at **42 Le Havre**. I build practical security tooling and personal software projects in C, C++, Python and x86-64 Assembly.

My primary direction is **offensive cybersecurity**: Windows x64 internals, reverse engineering, debugger and anomaly detection, process injection research, persistence and privilege-elevation research, command-and-control concepts, authorized network testing, web/API security and bug bounty. I also build hypervisors, debuggers, AI automation and developer tools.

All security work is designed for **authorized environments, educational laboratories, defensive understanding and responsible disclosure**.

## 🛡️ Offensive Cybersecurity Profile

- **Primary identity:** Offensive Cybersecurity Developer / Ethical Hacker
- **Technical specialization:** Windows internals, low-level C/C++, x86-64 Assembly and reverse engineering
- **Security research:** Injection, persistence, privilege elevation, anti-debugging, C2 concepts and network testing
- **Web security:** Bug bounty, IDOR, API security and business-logic testing
- **Systems engineering:** Hypervisors, debuggers, networking, virtualization, UNIX and Docker
- **Additional work:** AI automation, developer tooling, terminal applications and game development
- **Ethical scope:** Authorized research and testing only

## 🛠️ Languages & Tools

{tools}

## 📁 Projects 42

{projects_42}

## 🎯 Personal Projects

The following list preserves my deliberate priority order. These projects represent my offensive cybersecurity, low-level, AI and developer-tooling work.

{personal_projects}

## 📊 GitHub Snapshot

- Public repositories: {stats['repos']}
- Total stars across owned public repositories: {stats['stars']}
- Followers: {stats['followers']}
- Following: {stats['following']}

## ⚡ Currently

Working on **Cisco cybersecurity certification and ethical hacking**.

## Contact & Security Profiles

- Portfolio: https://zibgame.github.io
- GitHub: https://github.com/Zibgame
- LinkedIn: https://www.linkedin.com/in/zibrian-cadinot
- Hack The Box: https://profile.hackthebox.com/profile/019d539a-c442-70f1-b6c9-1231e7ac1b94
- Intigriti: https://app.intigriti.com/researcher/profile/zibgame
"""


def write_semantic_profiles(stats: dict) -> None:
    content = semantic_markdown(stats).strip() + "\n"
    PROFILE.write_text(content, encoding="utf-8")
    print("  wrote PROFILE.md")
