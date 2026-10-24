"""Original SVG rendering system for the Zibgame profile."""

from __future__ import annotations

import base64
from html import escape
from pathlib import Path
import re

from . import config


WIDTH = 780
ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "generated"
PORTRAIT = ROOT / "source" / "zibrian-cyber-portrait.png"
ICONS = ROOT / "source" / "icons"

COLORS = {
    "bg": "#050811",
    "surface": "#090E1B",
    "surface2": "#0C1424",
    "line": "#1D3354",
    "line2": "#285A8D",
    "text": "#DCE9F7",
    "muted": "#7D91A9",
    "dim": "#4B6079",
    "blue": "#377DFF",
    "cyan": "#58E6FF",
    "cyan2": "#1AB6D2",
    "green": "#58E6A9",
    "amber": "#FFCA6A",
    "orange": "#FF9F43",
    "purple": "#A879FF",
    "pink": "#FF4FD8",
    "red": "#FF6B7A",
}

LANGUAGE_COLORS = ["#377DFF", "#58E6FF", "#58E6A9", "#A98BFF", "#FFCA6A", "#FF7FA8", "#7D91A9"]
CALENDAR_COLORS = ["#0D1727", "#123153", "#185181", "#237AB1", "#58E6FF"]


def _defs() -> str:
    return f"""
    <defs>
      <linearGradient id="panel" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stop-color="#0C1424"/><stop offset="1" stop-color="#070B14"/>
      </linearGradient>
      <linearGradient id="bluefade" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stop-color="{COLORS['blue']}" stop-opacity=".30"/>
        <stop offset="1" stop-color="{COLORS['cyan']}" stop-opacity="0"/>
      </linearGradient>
      <radialGradient id="halo" cx="78%" cy="28%" r="58%">
        <stop offset="0" stop-color="{COLORS['blue']}" stop-opacity=".20"/>
        <stop offset="1" stop-color="{COLORS['bg']}" stop-opacity="0"/>
      </radialGradient>
      <pattern id="grid" width="26" height="26" patternUnits="userSpaceOnUse">
        <path d="M26 0H0V26" fill="none" stroke="#183052" stroke-width=".7" opacity=".42"/>
      </pattern>
      <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
        <rect width="4" height="2" fill="#000" opacity=".22"/>
      </pattern>
      <filter id="glow" x="-80%" y="-80%" width="260%" height="260%">
        <feGaussianBlur stdDeviation="2.2" result="blur"/>
        <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
      </filter>
      <clipPath id="heroPortrait"><path d="M548 47H746V283L718 311H520V75Z"/></clipPath>
    </defs>"""


BASE_STYLE = f"""
text,tspan{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace}}
.sans{{font-family:Inter,'Segoe UI',Arial,sans-serif}}
.micro{{font-size:9px;letter-spacing:1.55px}}
.muted{{fill:{COLORS['muted']}}}
.label{{fill:{COLORS['cyan']};font-size:10px;letter-spacing:1.7px}}
.pulse{{animation:pulse 2.4s ease-in-out infinite}}
.blink{{animation:blink 1.2s steps(1,end) infinite}}
.scan{{animation:scan 7s linear infinite}}
.dash{{animation:dash 5s linear infinite}}
@keyframes pulse{{0%,100%{{opacity:.42}}50%{{opacity:1}}}}
@keyframes blink{{0%,56%{{opacity:1}}57%,100%{{opacity:.18}}}}
@keyframes scan{{from{{transform:translateY(-30px)}}to{{transform:translateY(380px)}}}}
@keyframes dash{{to{{stroke-dashoffset:-80}}}}
"""


def document(width: int, height: int, body: str, style: str = "", *, defs: str = "") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img">{_defs()}{defs}'
        f'<style>{BASE_STYLE}{style}</style>{body}</svg>'
    )


def background(height: int, *, grid: bool = False) -> str:
    parts = [f'<rect width="{WIDTH}" height="{height}" fill="{COLORS["bg"]}"/>']
    if grid:
        parts.append(f'<rect width="{WIDTH}" height="{height}" fill="url(#grid)" opacity=".55"/>')
    parts.append(f'<rect width="{WIDTH}" height="{height}" fill="url(#halo)"/>')
    return "".join(parts)


def frame(height: int, code: str, title: str) -> str:
    return f"""
    <rect x="1" y="1" width="778" height="{height - 2}" rx="4" fill="url(#panel)" stroke="{COLORS['line']}"/>
    <rect x="1" y="1" width="5" height="{height - 2}" rx="2" fill="{COLORS['blue']}"/>
    <path d="M18 31H762" stroke="{COLORS['line']}"/>
    <circle class="pulse" cx="20" cy="16" r="3.5" fill="{COLORS['green']}"/>
    <text x="31" y="20" class="label">{escape(title)}</text>
    <text x="760" y="20" text-anchor="end" class="micro muted">{escape(code)}</text>
    """


def _portrait_data() -> str:
    return base64.b64encode(PORTRAIT.read_bytes()).decode("ascii")


def data_uri(path: Path) -> str:
    mime = {
        ".svg": "image/svg+xml",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
    }[path.suffix.lower()]
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{payload}"


def svg_with_replacements_uri(path: Path, replacements: dict[str, str]) -> str:
    source = path.read_text(encoding="utf-8")
    for old, new in replacements.items():
        source = source.replace(old, new)
    payload = base64.b64encode(source.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{payload}"


def _stat(x: int, value, label: str) -> str:
    return f"""
      <text x="{x}" y="280" class="sans" font-size="23" font-weight="700" fill="{COLORS['text']}">{value}</text>
      <text x="{x}" y="298" class="micro muted">{escape(label)}</text>
    """


def hero(stats: dict) -> str:
    portrait = _portrait_data()
    body = background(330, grid=True) + f"""
    <path d="M1 1H779V329H1Z" fill="none" stroke="{COLORS['line2']}"/>
    <path d="M20 27H390" stroke="{COLORS['line']}"/>
    <circle class="blink" cx="20" cy="18" r="3.5" fill="{COLORS['green']}"/>
    <text x="31" y="22" class="micro" fill="{COLORS['muted']}">PUBLIC PROFILE // VERIFIED SOURCE</text>
    <text x="512" y="22" class="micro" fill="{COLORS['muted']}">FRANCE</text>
    <text x="760" y="22" text-anchor="end" class="micro" fill="{COLORS['green']}">STATUS: BUILDING</text>

    <text x="28" y="78" class="sans" font-size="13" font-weight="700" letter-spacing="2.2" fill="{COLORS['cyan']}">CYBERSECURITY ENGINEERING CONSOLE</text>
    <text x="26" y="128" class="sans" font-size="42" font-weight="800" letter-spacing="-1" fill="{COLORS['text']}">ZIBRIAN</text>
    <text x="26" y="171" class="sans" font-size="42" font-weight="800" letter-spacing="-1" fill="{COLORS['text']}">CADINOT<tspan fill="{COLORS['blue']}">.</tspan></text>
    <text x="28" y="201" font-size="13" font-weight="700" fill="{COLORS['cyan']}">{escape(config.ROLE.upper())}</text>
    <text x="28" y="228" class="sans" font-size="12" fill="{COLORS['muted']}">42 student · ethical hacking · personal projects</text>

    <path d="M28 252H485" stroke="{COLORS['line']}"/>
    {_stat(28, stats['repos'], 'PUBLIC REPOS')}
    {_stat(145, stats['stars'], 'STARS')}
    {_stat(230, stats['followers'], 'FOLLOWERS')}
    {_stat(355, stats['following'], 'FOLLOWING')}

    <path d="M548 47H746V283L718 311H520V75Z" fill="#07101E" stroke="{COLORS['cyan']}" stroke-width="1.5"/>
    <g clip-path="url(#heroPortrait)">
      <image x="514" y="41" width="238" height="276" preserveAspectRatio="xMidYMid slice" href="data:image/png;base64,{portrait}"/>
      <rect x="514" y="41" width="238" height="276" fill="url(#scan)" opacity=".42"/>
      <rect class="scan" x="514" y="34" width="238" height="20" fill="{COLORS['cyan']}" opacity=".08"/>
    </g>
    <path class="dash" d="M531 63H735V292H531Z" fill="none" stroke="{COLORS['cyan']}" stroke-dasharray="18 8" opacity=".45"/>
    <rect x="529" y="55" width="100" height="18" fill="#050811" opacity=".82"/>
    <text x="536" y="68" class="micro" fill="{COLORS['cyan']}">ID // ZIBGAME</text>
    <circle class="blink" cx="731" cy="297" r="4" fill="{COLORS['green']}" filter="url(#glow)"/>
    """
    return document(WIDTH, 330, body)


def about() -> str:
    body = frame(154, "PROFILE://IDENTITY", "01 // ABOUT") + f"""
    <rect x="22" y="45" width="736" height="84" rx="4" fill="#050A13" stroke="{COLORS['line']}"/>
    <rect x="22" y="45" width="3" height="84" rx="1.5" fill="{COLORS['cyan']}"/>
    <text x="40" y="66" class="micro" fill="{COLORS['cyan']}">OFFENSIVE SECURITY // LOW-LEVEL SYSTEMS</text>
    <text x="40" y="91" class="sans" font-size="15" font-weight="750" fill="{COLORS['text']}">I build to understand what happens below the abstraction layer.</text>
    <text x="40" y="112" class="sans" font-size="10.8" fill="{COLORS['muted']}">Packers, hypervisors and native Windows security tooling built from first principles.</text>
    <text x="735" y="66" text-anchor="end" class="micro" fill="{COLORS['blue']}">42 LE HAVRE</text>
    <circle class="pulse" cx="742" cy="109" r="3" fill="{COLORS['green']}"/>
    <text x="22" y="145" class="micro muted">REVERSE ENGINEERING // WINDOWS INTERNALS // BUG BOUNTY // AUTHORIZED RESEARCH</text>
    """
    return document(WIDTH, 154, body.rstrip())


def capabilities() -> str:
    body = frame(142, "BIN://TOOLCHAIN", "02 // LANGUAGES & TOOLS")
    icon_files = [
        "c.svg", "cplusplus.svg", "assembly-blue.svg", "python.svg", "windows-original.png",
        "linux.svg", "docker-original.png", "vim.svg", "bash.svg", "powershell.svg",
    ]
    x_positions = [22 + index * 73.6 for index in range(10)]
    for index, (tool, icon_file, x) in enumerate(
        zip(config.TOOLS, icon_files, x_positions)
    ):
        icon = (
            svg_with_replacements_uri(ICONS / icon_file, {"#293138": "#EAF0F7"})
            if icon_file == "bash.svg"
            else data_uri(ICONS / icon_file)
        )
        body += f'<rect x="{x:.1f}" y="48" width="60" height="78" rx="5" fill="#070D18" stroke="{COLORS["line2"]}"/>'
        body += f'<image x="{x + 12:.1f}" y="57" width="36" height="36" preserveAspectRatio="xMidYMid meet" href="{icon}"/>'
        body += f'<circle class="pulse" style="animation-delay:{index * 0.17:.2f}s" cx="{x + 52:.1f}" cy="56" r="2.5" fill="{COLORS["blue"]}"/>'
        body += f'<text x="{x + 30:.1f}" y="113" text-anchor="middle" class="sans" font-size="8.5" font-weight="650" fill="{COLORS["text"]}">{escape(tool)}</text>'
    return document(WIDTH, 142, body)


def project_header(
    title: str,
    number: str,
    code: str,
) -> str:
    body = background(64) + f"""
    <rect x="1" y="1" width="778" height="62" rx="4" fill="url(#panel)" stroke="{COLORS['line']}"/>
    <rect x="1" y="1" width="5" height="62" rx="2" fill="{COLORS['blue']}"/>
    <text x="24" y="38" class="sans" font-size="16" font-weight="750" fill="{COLORS['text']}">{escape(title)} <tspan fill="{COLORS['blue']}">// {escape(number)}</tspan></text>
    <text x="756" y="36" text-anchor="end" class="micro" fill="{COLORS['cyan']}">{escape(code)}</text>
    <circle class="pulse" cx="756" cy="17" r="3" fill="{COLORS['blue']}"/>
    """
    return document(WIDTH, 64, body.rstrip())


def telemetry(stats: dict, languages: list[tuple[str, float]], calendar: list[int]) -> str:
    body = frame(326, "LIVE://GITHUB", "06 // 📊 GITHUB STATS")
    stat_items = [("REPOSITORIES", stats["repos"]), ("TOTAL STARS", stats["stars"]), ("FOLLOWERS", stats["followers"]), ("FOLLOWING", stats["following"])]
    for index, (label, value) in enumerate(stat_items):
        x = 22 + index * 185
        body += f'<rect x="{x}" y="47" width="169" height="54" rx="4" fill="#07101D" stroke="{COLORS["line"]}"/>'
        body += f'<text x="{x+13}" y="74" class="sans" font-size="21" font-weight="700" fill="{COLORS["text"]}">{value}</text>'
        body += f'<text x="{x+13}" y="91" class="micro muted">{escape(label)}</text>'

    body += f'<text x="22" y="128" class="micro muted">LANGUAGE DISTRIBUTION // BYTES ACROSS OWNED PUBLIC REPOSITORIES</text>'
    total = sum(value for _, value in languages) or 1
    x, bar_y, bar_width = 22.0, 143, 736.0
    for index, (name, value) in enumerate(languages):
        width = bar_width * value / total
        color = LANGUAGE_COLORS[index % len(LANGUAGE_COLORS)]
        body += f'<rect x="{x:.1f}" y="{bar_y}" width="{width:.1f}" height="11" fill="{color}"/>'
        x += width
    lx = 22
    for index, (name, value) in enumerate(languages):
        color = LANGUAGE_COLORS[index % len(LANGUAGE_COLORS)]
        item_width = 78 + len(name) * 5.7
        body += f'<circle cx="{lx+4}" cy="173" r="4" fill="{color}"/><text x="{lx+14}" y="177" font-size="10" fill="{COLORS["text"]}">{escape(name)} <tspan fill="{COLORS["muted"]}">{value:.1f}%</tspan></text>'
        lx += item_width

    body += f'<text x="22" y="207" class="micro muted">CONTRIBUTION SIGNAL // LAST 53 WEEKS</text>'
    cell, gap = 8, 3
    values = calendar[-371:] if calendar else [0] * 371
    for index, level in enumerate(values):
        column, row = divmod(index, 7)
        x = 22 + column * (cell + gap)
        y = 221 + row * (cell + gap)
        color = CALENDAR_COLORS[max(0, min(4, int(level)))]
        body += f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="1.5" fill="{color}"/>'
    body += f'<path d="M22 304H758" stroke="{COLORS["line"]}"/>'
    body += f'<text x="758" y="319" text-anchor="end" class="micro" fill="{COLORS["green"]}">SELF-HOSTED DATA // NO THIRD-PARTY CARD SERVICE</text>'
    return document(WIDTH, 326, body)


def currently() -> str:
    body = frame(152, "NOW://FOCUS", "05 // ⚡ CURRENTLY") + f"""
    <rect x="22" y="48" width="736" height="67" rx="4" fill="#050A13" stroke="{COLORS['purple']}"/>
    <text x="38" y="72" font-size="11" fill="{COLORS['purple']}">zibgame@security:~$</text>
    <text x="191" y="72" font-size="11" fill="{COLORS['text']}">cat current-focus.txt</text>
    <text x="38" y="99" class="sans" font-size="14" font-weight="700" fill="{COLORS['green']}">Working on Cisco cybersecurity certification and ethical hacking.</text>
    <rect class="blink" x="602" y="86" width="8" height="15" fill="{COLORS['cyan']}"/>
    <text x="22" y="139" class="micro muted">— ZIBRIAN CADINOT —</text>
    <text x="758" y="139" text-anchor="end" class="micro" fill="{COLORS['pink']}">KEEP LEARNING // KEEP BUILDING</text>
    """
    return document(WIDTH, 152, body)


def colored_svg_uri(path: Path, color: str) -> str:
    source = path.read_text(encoding="utf-8")
    source = source.replace("<svg ", f'<svg fill="{color}" ', 1)
    payload = base64.b64encode(source.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{payload}"


def contact_segment(title: str, subtitle: str, index: int) -> str:
    width, height = 195, 116
    accents = [COLORS["cyan"], COLORS["blue"], COLORS["cyan2"], COLORS["blue"]]
    accent = accents[index]
    if index == 0:
        logo = f"""
        <g transform="translate(20 49)" fill="none" stroke="{accent}" stroke-width="1.6">
          <circle cx="20" cy="20" r="17"/><path d="M3 20h34M20 3c7 7 7 27 0 34M20 3c-7 7-7 27 0 34"/>
        </g>"""
    else:
        icon_paths = [None, ICONS / "linkedin.svg", ICONS / "hackthebox.svg", ICONS / "intigriti.svg"]
        uri = colored_svg_uri(icon_paths[index], accent)
        logo = f'<image x="22" y="50" width="36" height="36" preserveAspectRatio="xMidYMid meet" href="{uri}"/>'
    top_label = "07 // CONTACT ME" if index == 0 else f"CHANNEL 0{index + 1}"
    body = f"""
    <rect x=".5" y=".5" width="194" height="115" fill="{COLORS['surface2']}" stroke="{COLORS['line']}"/>
    <rect x=".5" y=".5" width="194" height="31" fill="#080D17" stroke="{COLORS['line']}"/>
    <rect x=".5" y=".5" width="4" height="115" fill="{accent}"/>
    <text x="13" y="20" class="micro" fill="{accent}">{escape(top_label)}</text>
    <circle class="pulse" cx="181" cy="16" r="3" fill="{accent}"/>
    {logo}
    <text x="70" y="63" class="micro" fill="{accent}">{escape(title)}</text>
    <text x="70" y="82" class="sans" font-size="8.8" fill="{COLORS['muted']}">{escape(subtitle)}</text>
    <path d="M165 93h14m-5-5 5 5-5 5" fill="none" stroke="{accent}" stroke-width="1.4"/>
    """
    return document(width, height, body)


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  wrote {path.relative_to(ROOT.parent)}")


def render_all(stats: dict, languages: list[tuple[str, float]], calendar: list[int]) -> None:
    write(GENERATED / "hero.svg", hero(stats))
    write(GENERATED / "about-v2.svg", about())
    write(GENERATED / "toolchain-v4.svg", capabilities())
    write(GENERATED / "projects-42-header.svg", project_header(
        "42 PROJECTS", "03", "CURRICULUM://CORE",
    ))
    write(GENERATED / "personal-projects-header.svg", project_header(
        "PERSONAL PROJECTS", "04", "WORK://SELECTED",
    ))
    write(GENERATED / "currently.svg", currently())
    write(GENERATED / "telemetry.svg", telemetry(stats, languages, calendar))

    for index, (title, subtitle, _, _) in enumerate(config.LINKS):
        write(GENERATED / f"contact-{index + 1}-{slug(title)}.svg", contact_segment(title, subtitle, index))
