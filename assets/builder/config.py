"""Content and identity configuration for the GitHub profile."""

USERNAME = "Zibgame"
DISPLAY_NAME = "Zibrian Cadinot"
LOCATION = "France"
ROLE = "Cybersecurity // Low-Level Systems"
TAGLINE = "42 student building personal projects across cybersecurity, systems and automation."
CURRENT_FOCUS = "Cisco cybersecurity certification and ethical hacking"

FALLBACK_STATS = {
    "repos": 56,
    "stars": 61,
    "followers": 39,
    "following": 35,
}

FALLBACK_LANGUAGES = [
    ("C", 56.8),
    ("C++", 31.7),
    ("Python", 2.4),
    ("GLSL", 1.7),
    ("TypeScript", 1.4),
    ("Makefile", 1.2),
]

TOOLS = [
    "C", "C++", "x86_64 ASM", "Python", "Windows", "Linux",
    "Docker", "Vim", "Bash", "PowerShell",
]

TOOL_GROUPS = [
    ("LANGUAGES", "C · C++ · Python · x86-64 Assembly"),
    ("PLATFORMS", "Windows · Linux · Docker"),
    ("WORKFLOW", "Vim · Bash · PowerShell"),
    ("FOCUS", "Win64 internals · networking · virtualization"),
]

CAPABILITIES = [
    ("LOW-LEVEL", "Memory, processes, assembly, Win64 internals"),
    ("SECURITY", "Bug bounty, web/API testing, research labs"),
    ("SYSTEMS", "Networking, virtualization, Docker, UNIX"),
    ("ENGINEERING", "Developer tools, automation, AI workflows"),
]

LINKS = [
    ("PORTFOLIO", "zibgame.github.io", "https://zibgame.github.io", "WEB"),
    ("LINKEDIN", "Zibrian Cadinot", "https://www.linkedin.com/in/zibrian-cadinot", "IN"),
    ("HACK THE BOX", "Cybersecurity profile", "https://profile.hackthebox.com/profile/019d539a-c442-70f1-b6c9-1231e7ac1b94", "HTB"),
    ("INTIGRITI", "Bug bounty profile", "https://app.intigriti.com/researcher/profile/zibgame", "INT"),
]

PROJECTS_42 = [
    ("42 Piscine", "https://github.com/Zibgame/42_Piscine", "C / SHELL", "C fundamentals, shell, logic and algorithms."),
    ("Libft", "https://github.com/Zibgame/libft", "C / LIBRARY", "Custom C library reimplementing standard functions."),
    ("get_next_line", "https://github.com/Zibgame/get_next_line", "C / I/O", "Efficient line-by-line file reader with buffered state."),
    ("ft_printf", "https://github.com/Zibgame/ft_printf", "C / PARSING", "A printf reimplementation with custom format parsing."),
    ("Born2beRoot", "https://github.com/Zibgame/Born2beRoot", "LINUX / HARDENING", "Debian server setup, security and virtualization."),
    ("Minitalk", "https://github.com/Zibgame/minitalk", "C / IPC", "Inter-process communication using UNIX signals."),
    ("So Long", "https://github.com/Zibgame/so_long", "C / GRAPHICS", "Small 2D game built with MiniLibX."),
    ("Push Swap", "https://github.com/Zibgame/push_swap", "C / ALGORITHMS", "Constrained-stack sorting and operation optimization."),
    ("Philosophers", "https://github.com/Zibgame/Philosophers", "C / THREADS", "Concurrency simulation with mutexes and deadlock control."),
    ("Minishell", "https://github.com/Zibgame/Minishell", "C / UNIX", "POSIX shell with parsing, pipes, builtins and execve."),
    ("CUBE-3D", "https://github.com/Pixyde/cub3d", "C / RAYCASTING", "Wolfenstein-style raycaster and graphics engine."),
    ("42-C++", "https://github.com/Zibgame/42_cpp", "C++ / OOP", "Core C++ concepts, object design and idioms."),
    ("NetPractice", "https://github.com/Zibgame/NetPractice", "NETWORKING", "TCP/IP addressing, routing and subnetting fundamentals."),
    ("ft_irc", "https://github.com/tren-chvl/ft_irc", "C++ / NETWORKING", "IRC server with sockets and client handling."),
    ("Inception", "https://github.com/Zibgame/Inception", "DOCKER / DEVOPS", "Containerized services, networks and persistent storage."),
    ("Transcendence", "https://github.com/Zibgame/ft_transcendence", "FULL STACK", "Full-stack multiplayer web application."),
]

PERSONAL_THEMES = [
    ("CYBER", "OFFENSIVE / CYBER", "Security labs, research and bug bounty", "#FF6B7A"),
    ("LOW", "LOW-LEVEL / SYSTEMS", "Win64 internals, assembly and debugging", "#58E6FF"),
    ("AI", "AI / AUTOMATION", "Applied AI, audio and developer automation", "#A879FF"),
    ("TOOLS", "DEVELOPER TOOLS / APPS", "Editors, desktop apps and personal workflows", "#58E6A9"),
]

PERSONAL_PROJECT_THEME = {
    "Obsidian-Packer": "CYBER",
    "ft_shield": "CYBER",
    "UDP-Flood-Win64": "CYBER",
    "Win64-Dll-Injector": "CYBER",
    "C2-Windows-x64": "CYBER",
    "PersistenceLib-Win64": "CYBER",
    "PrivEscLib-Win64": "CYBER",
    "AntiDebugger-Win64": "CYBER",
    "Bug Bounty": "CYBER",
    "Stealth-Hypervisor-Win64": "LOW",
    "TUI Debugger Win64": "LOW",
    "ASM Lib": "LOW",
    "ft_randint": "LOW",
    "Mockify": "AI",
    "AI Guitar MIDI Amp Controller": "AI",
    "Norm AI Fixer": "AI",
    "Zim": "TOOLS",
    "Lite Calculator App": "TOOLS",
    "Vim Config": "TOOLS",
    "Zsh Config": "TOOLS",
}

# Editorial priority order: keep the strongest and most representative work first.
OTHER_PROJECTS = [
    ("Obsidian-Packer", "https://github.com/Zibgame/Obsidian-Packer", "PE32+ / C++", "x86-64 PE packer and in-memory loader with image reconstruction, relocations, imports, TLS and memory protections."),
    ("Stealth-Hypervisor-Win64", "https://github.com/Zibgame/Stealth-Hypervisor", "UEFI / VIRTUALIZATION", "Type-1 Win64 research hypervisor with VM introspection."),
    ("ft_shield", "https://github.com/Zibgame/ft_shield", "C / NATIVE WIN32", "Native Win32 remote-administration study with an authenticated multi-client shell, persistence and anti-analysis checks."),
    ("PrivEscLib-Win64", "https://github.com/Zibgame/PrivEscLib-Win64", "WINDOWS SECURITY", "Privilege-elevation mechanisms studied in controlled environments."),
    ("AntiDebugger-Win64", "https://github.com/Zibgame/AntiDebugger-Win64", "REVERSE ENGINEERING", "Debugger and anomaly detection for low-level security research."),
    ("Bug Bounty", "https://github.com/Zibgame/intigriti-writeups", "WEB / API SECURITY", "Authorized findings and writeups: IDOR, APIs and business logic."),
    ("PersistenceLib-Win64", "https://github.com/Zibgame/PersistenceLib-Win64", "WINDOWS SECURITY", "Modular persistence setup, detection and removal research."),
    ("Win64-Dll-Injector", "https://github.com/Zibgame/win32-dll-injector", "WINDOWS INTERNALS", "Process memory and DLL loading research on Win64."),
    ("C2-Windows-x64", "https://github.com/Zibgame/C2-Windows-x64", "CONTROLLED LAB", "Winsock command-channel lab for security education."),
    ("ASM Lib", "https://github.com/Zibgame/asm-lib", "ASM / C", "x86_64 assembly library and low-level exercises."),
    ("TUI Debugger Win64", "https://github.com/Zibgame/TUI-Debugger-Win64", "DEBUGGING / WIN64", "In-development terminal debugger for registers, assembly, breakpoints and process state."),
    ("UDP-Flood-Win64", "https://github.com/Zibgame/UDP-Flood-Win64", "NETWORK LAB", "Educational UDP traffic-stress implementation for authorized labs."),
    ("Mockify", "https://github.com/Zibgame/Mockify", "PYTHON / AI", "AI-driven mockup pipeline with automated visual quality control."),
    ("Norm AI Fixer", "https://github.com/Zibgame/norm-ai-fixer", "PYTHON / LOCAL AI", "Offline AI code normalizer with configurable rules."),
    ("AI Guitar MIDI Amp Controller", "https://github.com/Zibgame/ai-guitar-midi-amp-controller", "PYTHON / AUDIO", "AI-assisted guitar amplifier and MIDI controller."),
    ("Zim", "https://github.com/Zibgame/zim", "C++ / EDITOR", "Minimal Vim-inspired terminal editor with modal navigation."),
    ("Lite Calculator App", "https://github.com/Zibgame/calculator-app", "C# / WPF", "Lightweight desktop calculator with a clean WPF interface."),
    ("ft_randint", "https://github.com/Zibgame/ft_randint", "C / ALGORITHMS", "Custom pseudo-random integer generator implemented in C."),
    ("Vim Config", "https://github.com/Zibgame/Vim-config", "VIM", "Personal Vim configuration inspired by the 42 environment."),
    ("Zsh Config", "https://github.com/Zibgame/zsh-config", "SHELL", "Personalized Zsh configuration and workflow."),
]

FEATURED_NAMES = {
    "Obsidian-Packer",
    "ft_shield",
    "Stealth-Hypervisor-Win64",
    "PrivEscLib-Win64",
    "PersistenceLib-Win64",
    "Bug Bounty",
    "AntiDebugger-Win64",
}
