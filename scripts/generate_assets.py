#!/usr/bin/env python3
"""Generate dark and light theme TUI SVG assets for the dev-Aatif GitHub profile README."""

from __future__ import annotations

import html
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"

FONT_MONO = (
    "ui-monospace, 'SFMono-Regular', 'JetBrains Mono', 'Fira Code', "
    "Menlo, Monaco, Consolas, 'Liberation Mono', monospace"
)
FONT_SANS = (
    "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
)

THEMES = {
    "dark": {
        "bg": "#0b0f14",
        "surface": "#111720",
        "surface_alt": "#151d28",
        "titlebar": "#141b24",
        "border": "#232d3b",
        "border_strong": "#303d4f",
        "text": "#e6edf3",
        "muted": "#8b949e",
        "dim": "#546070",
        "grid": "#1d2633",
        "cyan": "#38bdf8",
        "cyan_bg": "#0f2738",
        "green": "#34d399",
        "green_bg": "#0e2923",
        "amber": "#fbbf24",
        "amber_bg": "#2b210e",
        "purple": "#a78bfa",
        "purple_bg": "#211938",
        "chip_bg": "#18212e",
        "chip_border": "#2a3748",
    },
    "light": {
        "bg": "#fbfcfe",
        "surface": "#f3f6fa",
        "surface_alt": "#ebf0f6",
        "titlebar": "#eef2f7",
        "border": "#d0d7de",
        "border_strong": "#afb8c1",
        "text": "#1f2328",
        "muted": "#57606a",
        "dim": "#8c959f",
        "grid": "#e2e8f0",
        "cyan": "#0284c7",
        "cyan_bg": "#e0f2fe",
        "green": "#059669",
        "green_bg": "#d1fae5",
        "amber": "#d97706",
        "amber_bg": "#fef3c7",
        "purple": "#7c3aed",
        "purple_bg": "#ede9fe",
        "chip_bg": "#ffffff",
        "chip_border": "#d0d7de",
    },
}


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def render_hero(theme_name: str, t: dict[str, str]) -> str:
    w, h = 860, 316
    ascii_art = [
        "    ___         __  _ ____",
        "   /   | ____ _/ /_(_) __/",
        "  / /| |/ __ `/ __/ / /_  ",
        " / ___ |/ /_/ / /_/ / __/ ",
        "/_/  |_|\\__,_/\\__/_/_/    ",
    ]
    ascii_lines = "\n".join(
        f'<text x="34" y="{94 + i * 18}" fill="{t["cyan"]}" font-family="{FONT_MONO}" '
        f'font-size="11.5" font-weight="700" xml:space="preserve">{esc(line)}</text>'
        for i, line in enumerate(ascii_art)
    )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Aatif Terminal Profile Header">
  <defs>
    <pattern id="dots-{theme_name}" width="20" height="20" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1" fill="{t["grid"]}"/>
    </pattern>
    <linearGradient id="accent-bar-{theme_name}" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{t["cyan"]}"/>
      <stop offset="50%" stop-color="{t["green"]}"/>
      <stop offset="100%" stop-color="{t["purple"]}"/>
    </linearGradient>
  </defs>

  <!-- Outer Window -->
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="12" fill="{t["bg"]}" stroke="{t["border"]}" stroke-width="1.5"/>
  <rect x="2" y="39" width="{w - 4}" height="{h - 68}" fill="url(#dots-{theme_name})" opacity="0.65"/>

  <!-- Titlebar -->
  <path d="M 13 1 H {w - 13} A 12 12 0 0 1 {w - 1} 13 V 38 H 1 V 13 A 12 12 0 0 1 13 1 Z" fill="{t["titlebar"]}"/>
  <line x1="1" y1="38" x2="{w - 1}" y2="38" stroke="{t["border"]}" stroke-width="1"/>
  <rect x="1" y="38" width="{w - 2}" height="1.5" fill="url(#accent-bar-{theme_name})" opacity="0.55"/>

  <!-- Window Controls -->
  <circle cx="22" cy="19.5" r="5.5" fill="#ff5f56"/>
  <circle cx="40" cy="19.5" r="5.5" fill="#ffbd2e"/>
  <circle cx="58" cy="19.5" r="5.5" fill="#27c93f"/>

  <!-- Window Title -->
  <text x="{w // 2}" y="23.5" text-anchor="middle" fill="{t["muted"]}" font-family="{FONT_MONO}" font-size="12">aatif@dev-Aatif — zsh — ~/profile</text>

  <!-- Live Status Pill -->
  <rect x="734" y="9.5" width="108" height="20" rx="10" fill="{t["green_bg"]}" stroke="{t["green"]}" stroke-opacity="0.45" stroke-width="1"/>
  <circle cx="748" cy="19.5" r="3.5" fill="{t["green"]}">
    <animate attributeName="opacity" values="1;0.25;1" dur="2.2s" repeatCount="indefinite"/>
  </circle>
  <text x="758" y="23" fill="{t["green"]}" font-family="{FONT_MONO}" font-size="10.5" font-weight="600">ONLINE · 2.6</text>

  <!-- Left ASCII Emblem Card -->
  <rect x="24" y="58" width="234" height="196" rx="8" fill="{t["surface"]}" stroke="{t["border"]}" stroke-width="1"/>
  <text x="36" y="77" fill="{t["dim"]}" font-family="{FONT_MONO}" font-size="10.5">SYS // IDENTITY</text>
  {ascii_lines}
  <line x1="36" y1="192" x2="246" y2="192" stroke="{t["border"]}" stroke-width="1"/>
  <text x="36" y="213" fill="{t["muted"]}" font-family="{FONT_MONO}" font-size="11.5">host: <tspan fill="{t["text"]}">github.com/dev-Aatif</tspan></text>
  <text x="36" y="233" fill="{t["muted"]}" font-family="{FONT_MONO}" font-size="11.5">role: <tspan fill="{t["green"]}">full-stack &amp; mobile</tspan></text>

  <!-- Right Terminal Session -->
  <text x="282" y="76" font-family="{FONT_MONO}" font-size="12.5">
    <tspan fill="{t["green"]}" font-weight="600">$ </tspan><tspan fill="{t["text"]}">whoami --quote</tspan>
  </text>

  <text x="282" y="109" fill="{t["text"]}" font-family="{FONT_SANS}" font-size="24" font-weight="700" letter-spacing="-0.4">Aatif</text>
  <text x="352" y="107" font-family="{FONT_MONO}" font-size="12.5">
    <tspan fill="{t["dim"]}">//  </tspan><tspan fill="{t["cyan"]}" font-weight="600">Mobile · Web &amp; Desktop · Backend &amp; Data</tspan>
  </text>

  <!-- Tagline Quote -->
  <rect x="282" y="124" width="3" height="22" rx="1.5" fill="{t["amber"]}"/>
  <text x="295" y="140" fill="{t["amber"]}" font-family="{FONT_MONO}" font-size="13" font-style="italic">"Built to feel light in the hand, and hold up under load."</text>

  <line x1="282" y1="160" x2="836" y2="160" stroke="{t["border"]}" stroke-width="1" stroke-dasharray="3 3"/>

  <!-- Boot Telemetry -->
  <text x="282" y="183" fill="{t["green"]}" font-family="{FONT_MONO}" font-size="12">[OK]</text>
  <text x="320" y="183" fill="{t["muted"]}" font-family="{FONT_MONO}" font-size="12">mobile</text>
  <text x="388" y="183" fill="{t["dim"]}" font-family="{FONT_MONO}" font-size="12">-&gt;</text>
  <text x="412" y="183" fill="{t["text"]}" font-family="{FONT_MONO}" font-size="12">Flutter · Riverpod · Kotlin · Jetpack Compose</text>

  <text x="282" y="205" fill="{t["cyan"]}" font-family="{FONT_MONO}" font-size="12">[OK]</text>
  <text x="320" y="205" fill="{t["muted"]}" font-family="{FONT_MONO}" font-size="12">web/ui</text>
  <text x="388" y="205" fill="{t["dim"]}" font-family="{FONT_MONO}" font-size="12">-&gt;</text>
  <text x="412" y="205" fill="{t["text"]}" font-family="{FONT_MONO}" font-size="12">TypeScript · React · Next.js · Tailwind · Electron</text>

  <text x="282" y="227" fill="{t["purple"]}" font-family="{FONT_MONO}" font-size="12">[OK]</text>
  <text x="320" y="227" fill="{t["muted"]}" font-family="{FONT_MONO}" font-size="12">data</text>
  <text x="388" y="227" fill="{t["dim"]}" font-family="{FONT_MONO}" font-size="12">-&gt;</text>
  <text x="412" y="227" fill="{t["text"]}" font-family="{FONT_MONO}" font-size="12">Python · Node.js · Express · PostgreSQL · SQLite</text>

  <!-- Active Prompt + Cursor -->
  <text x="282" y="254" font-family="{FONT_MONO}" font-size="12.5">
    <tspan fill="{t["green"]}" font-weight="600">aatif@dev-Aatif</tspan><tspan fill="{t["dim"]}">:</tspan><tspan fill="{t["cyan"]}">~</tspan><tspan fill="{t["text"]}">$ ls ./pinned</tspan>
  </text>
  <rect x="506" y="242" width="8" height="14" rx="1" fill="{t["cyan"]}">
    <animate attributeName="opacity" values="1;1;0;0;1" dur="1.1s" repeatCount="indefinite"/>
  </rect>

  <!-- Bottom TUI Status Bar -->
  <path d="M 1 286 H {w - 1} V 303 A 12 12 0 0 1 {w - 13} 315 H 13 A 12 12 0 0 1 1 303 Z" fill="{t["titlebar"]}"/>
  <line x1="1" y1="286" x2="{w - 1}" y2="286" stroke="{t["border"]}" stroke-width="1"/>
  <rect x="14" y="291" width="62" height="18" rx="4" fill="{t["cyan_bg"]}"/>
  <text x="45" y="304" text-anchor="middle" fill="{t["cyan"]}" font-family="{FONT_MONO}" font-size="10.5" font-weight="700">NORMAL</text>
  <text x="88" y="304" fill="{t["muted"]}" font-family="{FONT_MONO}" font-size="11">branch: <tspan fill="{t["text"]}">main</tspan></text>
  <text x="842" y="304" text-anchor="end" fill="{t["dim"]}" font-family="{FONT_MONO}" font-size="11">git · utf-8 · local-first</text>
</svg>
'''


def render_stack(theme_name: str, t: dict[str, str]) -> str:
    w, h = 860, 260
    panes = [
        {
            "x": 20,
            "y": 46,
            "code": "01",
            "title": "MOBILE",
            "accent": t["green"],
            "accent_bg": t["green_bg"],
            "rows": [
                ("Flutter", "Dart · Riverpod"),
                ("Android", "Kotlin · Jetpack Compose · Material 3"),
            ],
        },
        {
            "x": 438,
            "y": 46,
            "code": "02",
            "title": "WEB & DESKTOP",
            "accent": t["cyan"],
            "accent_bg": t["cyan_bg"],
            "rows": [
                ("Frontend", "TypeScript · JavaScript · React"),
                ("Shells", "Next.js · Tailwind CSS · Electron"),
            ],
        },
        {
            "x": 20,
            "y": 150,
            "code": "03",
            "title": "BACKEND & DATA",
            "accent": t["amber"],
            "accent_bg": t["amber_bg"],
            "rows": [
                ("Runtime", "Python · Node.js · Express"),
                ("Storage", "PostgreSQL · SQLite"),
            ],
        },
        {
            "x": 438,
            "y": 150,
            "code": "04",
            "title": "VERSION CONTROL & FOCUS",
            "accent": t["purple"],
            "accent_bg": t["purple_bg"],
            "rows": [
                ("Workflow", "Git · Clean Diffs · Modular Design"),
                ("Bias", "Offline-First · Cross-Platform"),
            ],
        },
    ]

    pane_svg = []
    for p in panes:
        px, py = p["x"], p["y"]
        pw, ph = 402, 92
        rows_svg = ""
        for idx, (label, val) in enumerate(p["rows"]):
            ry = py + 52 + idx * 23
            rows_svg += (
                f'<text x="{px + 16}" y="{ry}" fill="{t["muted"]}" font-family="{FONT_MONO}" '
                f'font-size="11.5">{esc(label.ljust(9))}</text>'
                f'<text x="{px + 94}" y="{ry}" fill="{t["text"]}" font-family="{FONT_MONO}" '
                f'font-size="12">{esc(val)}</text>\n'
            )

        pane_svg.append(
            f'''  <g>
    <rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="8" fill="{t["surface"]}" stroke="{t["border"]}" stroke-width="1"/>
    <rect x="{px}" y="{py + 12}" width="3" height="20" rx="1.5" fill="{p["accent"]}"/>
    <rect x="{px + 16}" y="{py + 12}" width="26" height="18" rx="4" fill="{p["accent_bg"]}"/>
    <text x="{px + 29}" y="{py + 25}" text-anchor="middle" fill="{p["accent"]}" font-family="{FONT_MONO}" font-size="10.5" font-weight="700">{esc(p["code"])}</text>
    <text x="{px + 50}" y="{py + 25}" fill="{p["accent"]}" font-family="{FONT_MONO}" font-size="11.5" font-weight="700">{esc(p["title"])}</text>
    <circle cx="{px + pw - 18}" cy="{py + 21}" r="3" fill="{p["accent"]}" opacity="0.8"/>
    {rows_svg.strip()}
  </g>'''
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Aatif Tech Stack Matrix">
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="12" fill="{t["bg"]}" stroke="{t["border"]}" stroke-width="1.5"/>
  <text x="22" y="27" fill="{t["dim"]}" font-family="{FONT_MONO}" font-size="11.5" font-weight="700">$ btop --panel=capabilities</text>
  <text x="838" y="27" text-anchor="end" fill="{t["muted"]}" font-family="{FONT_MONO}" font-size="11">4 subsystems active</text>
  <line x1="20" y1="36" x2="{w - 20}" y2="36" stroke="{t["border"]}" stroke-width="1"/>
{chr(10).join(pane_svg)}
</svg>
'''


def render_project_card(
    theme_name: str,
    t: dict[str, str],
    slug: str,
    tag: str,
    accent_key: str,
    summary: str,
    chips: list[str],
) -> str:
    w, h = 860, 114
    accent = t[accent_key]
    accent_bg = t[f"{accent_key}_bg"]

    chips_svg = []
    cx = 24
    for chip in chips:
        cw = len(chip) * 7.2 + 20
        chips_svg.append(
            f'<rect x="{cx}" y="76" width="{cw:.1f}" height="22" rx="5" fill="{t["chip_bg"]}" stroke="{t["chip_border"]}" stroke-width="1"/>'
            f'<text x="{cx + cw / 2:.1f}" y="91" text-anchor="middle" fill="{t["text"]}" font-family="{FONT_MONO}" font-size="11">{esc(chip)}</text>'
        )
        cx += cw + 8

    tag_w = len(tag) * 6.8 + 20
    tag_x = w - 24 - tag_w - 28

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(slug)} project card">
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="10" fill="{t["surface"]}" stroke="{t["border"]}" stroke-width="1.5"/>
  <rect x="1" y="16" width="4" height="{h - 32}" rx="2" fill="{accent}"/>

  <!-- Command Title -->
  <text x="24" y="31" font-family="{FONT_MONO}" font-size="13">
    <tspan fill="{accent}" font-weight="700">$ </tspan><tspan fill="{t["muted"]}">open ~/pinned/</tspan><tspan fill="{t["text"]}" font-size="14" font-weight="700">{esc(slug)}</tspan>
  </text>

  <!-- Right Badge + Arrow -->
  <rect x="{tag_x:.1f}" y="15" width="{tag_w:.1f}" height="20" rx="5" fill="{accent_bg}"/>
  <text x="{tag_x + tag_w / 2:.1f}" y="28.5" text-anchor="middle" fill="{accent}" font-family="{FONT_MONO}" font-size="10.5" font-weight="700">{esc(tag)}</text>
  <text x="836" y="30" text-anchor="end" fill="{accent}" font-family="{FONT_MONO}" font-size="14" font-weight="700">-&gt;</text>

  <!-- Description -->
  <text x="24" y="57" fill="{t["muted"]}" font-family="{FONT_SANS}" font-size="13.5">{esc(summary)}</text>

  <!-- Stack Chips -->
  {"".join(chips_svg)}
</svg>
'''


def render_footer(theme_name: str, t: dict[str, str]) -> str:
    w, h = 860, 54
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Terminal Footer">
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="10" fill="{t["titlebar"]}" stroke="{t["border"]}" stroke-width="1.5"/>
  <text x="22" y="31" font-family="{FONT_MONO}" font-size="12.5">
    <tspan fill="{t["green"]}" font-weight="700">$ </tspan><tspan fill="{t["muted"]}">echo </tspan><tspan fill="{t["text"]}">"Always open to meaningful engineering &amp; sharp products."</tspan>
  </text>
  <text x="838" y="31" text-anchor="end" fill="{t["dim"]}" font-family="{FONT_MONO}" font-size="11.5">EOF · github.com/dev-Aatif</text>
</svg>
'''


def main() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    projects = [
        {
            "file": "project-sarmaya",
            "slug": "sarmaya",
            "tag": "ANDROID · OFFLINE-FIRST",
            "accent": "green",
            "summary": "Offline-first Android portfolio tracker for the Pakistan Stock Exchange (PSX) with event-sourced state.",
            "chips": ["Kotlin", "Jetpack Compose", "Android", "Offline-First"],
        },
        {
            "file": "project-nebula",
            "slug": "nebula-downloader",
            "tag": "DESKTOP · CROSS-PLATFORM",
            "accent": "cyan",
            "summary": "Cross-platform desktop video downloader featuring a dark-mode UI powered by the yt-dlp engine.",
            "chips": ["Electron", "yt-dlp", "Desktop UI", "Cross-Platform"],
        },
        {
            "file": "project-jot",
            "slug": "jot",
            "tag": "CLI · LOCAL-FIRST",
            "accent": "amber",
            "summary": "Local-first, zero-dependency command-line note-taking and management tool written in pure Rust.",
            "chips": ["Rust", "CLI", "Zero-Dependency", "Local-First"],
        },
    ]

    for theme_name, theme in THEMES.items():
        (ASSETS_DIR / f"hero-{theme_name}.svg").write_text(
            render_hero(theme_name, theme), encoding="utf-8"
        )
        (ASSETS_DIR / f"stack-{theme_name}.svg").write_text(
            render_stack(theme_name, theme), encoding="utf-8"
        )
        (ASSETS_DIR / f"footer-{theme_name}.svg").write_text(
            render_footer(theme_name, theme), encoding="utf-8"
        )
        for p in projects:
            (ASSETS_DIR / f"{p['file']}-{theme_name}.svg").write_text(
                render_project_card(
                    theme_name,
                    theme,
                    p["slug"],
                    p["tag"],
                    p["accent"],
                    p["summary"],
                    p["chips"],
                ),
                encoding="utf-8",
            )


if __name__ == "__main__":
    main()
