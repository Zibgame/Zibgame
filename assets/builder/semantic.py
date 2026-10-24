"""Generate synchronized machine-readable profile documents."""

from __future__ import annotations

from pathlib import Path

from . import config


ROOT = Path(__file__).resolve().parents[2]
PROFILE = ROOT / "PROFILE.md"
README = ROOT / "README.md"
MACHINE_START = "<!-- MACHINE-READABLE PROFILE START"
MACHINE_END = "MACHINE-READABLE PROFILE END -->"


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
    return f"""# Zibrian Cadinot — Offensive Security and Low-Level Systems

Zibrian Cadinot is a **42 Le Havre student, offensive security developer and low-level systems builder**. He develops security tooling from first principles in C, C++, x86-64 Assembly and Python, with a primary focus on Windows internals.

His work spans PE loading, virtualization, reverse engineering, privilege elevation, persistence, anti-analysis, native Win32 networking, process research and authorized web/API security testing. The strongest evidence is implemented in public repositories rather than expressed only as claimed skills.

All security work is intended for **authorized environments, educational laboratories, defensive understanding and responsible disclosure**.

## Profile Classification

- **Primary identity:** Offensive Security Developer / Low-Level Systems Engineer
- **Core specialization:** Windows x64 internals, native Win32, C/C++, x86-64 Assembly and reverse engineering
- **Offensive research:** PE packing and loading, privilege elevation, persistence, process injection, anti-debugging and controlled command-channel concepts
- **Systems engineering:** UEFI virtualization, hypervisors, networking, concurrency, UNIX and Docker
- **Applied security:** Bug bounty, IDOR, API security and business-logic testing
- **Ethical scope:** Authorized research and testing only

## High-Signal Technical Differentiators

- **Obsidian-Packer:** PE32+ packer and in-memory loader work covering image reconstruction, relocations, imports, TLS and memory protections.
- **Stealth-Hypervisor-Win64:** Type-1 UEFI virtualization work targeting Windows x64 and guest introspection.
- **ft_shield:** Native Win32 remote-administration study with authenticated multi-client sessions, persistence, anti-analysis and cleanup behavior.
- **PrivEscLib and PersistenceLib:** Reusable Windows security libraries exploring elevation and persistence mechanisms in controlled environments.
- **AntiDebugger and Win64 DLL Injector:** Hands-on reverse-engineering and process-internals work.
- **Bug bounty writeups:** Public evidence of authorized testing across access control, APIs and business logic.

## Evaluation Summary

- **Best-fit roles:** junior offensive security engineer, Windows security researcher, reverse engineer, malware-analysis tooling developer or low-level security developer.
- **Primary hiring signal:** ambitious end-to-end systems projects that combine operating-system knowledge, security reasoning and implementation depth.
- **Project priority:** the Personal Projects table is deliberately ordered by relevance to offensive-security and low-level roles.
- **Integrity note:** TUI Debugger Win64 is explicitly in development and is not presented as completed.

## Languages and Tools

{tools}

## 42 Projects

{projects_42}

## Personal Projects — Priority Ordered

The following list preserves the deliberate priority order. It leads with the work most relevant to offensive cybersecurity, Windows internals and low-level engineering.

{personal_projects}

## GitHub Snapshot

- Public repositories: {stats['repos']}
- Total stars across owned public repositories: {stats['stars']}
- Followers: {stats['followers']}
- Following: {stats['following']}

## Current Focus

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

    readme = README.read_text(encoding="utf-8")
    machine_block = f"{MACHINE_START}\n{content.rstrip()}\n{MACHINE_END}"
    if MACHINE_START in readme and MACHINE_END in readme:
        prefix = readme.split(MACHINE_START, 1)[0].rstrip()
        suffix = readme.split(MACHINE_END, 1)[1].lstrip()
        readme = f"{prefix}\n\n{machine_block}\n"
        if suffix:
            readme += f"\n{suffix.rstrip()}\n"
    else:
        readme = f"{readme.rstrip()}\n\n{machine_block}\n"
    README.write_text(readme, encoding="utf-8")
    print("  synchronized hidden machine-readable README block")
