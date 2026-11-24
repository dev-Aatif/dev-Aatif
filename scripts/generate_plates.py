#!/usr/bin/env python3
"""
Dual-Theme Kinetic Engineering Monograph — SVG Plate Synthesizer
Generates all Darkroom (dark) and Archival Vellum (light) animated SVG plates
for the dev-Aatif GitHub Profile README.

Zero third-party dependencies — pure Python 3 standard library.
Run: python3 scripts/generate_plates.py
"""

from __future__ import annotations

import math
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
CARDS_DIR = ASSETS / "cards"

FONT_SANS = "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
FONT_MONO = "'SF Mono', 'JetBrains Mono', ui-monospace, 'Cascadia Code', Menlo, Consolas, monospace"

THEMES = {
    "dark": {
        "edition": "DARKROOM // ANODIZED",
        "bg": "#0A0D0C",
        "surface": "#0F1412",
        "surface_alt": "#131916",
        "viewport": "#080B0A",
        "border": "#1F2924",
        "border_strong": "#2C3A33",
        "bevel": "rgba(255,255,255,0.06)",
        "grid": "#161E1A",
        "grid_subtle": "#111714",
        "ink": "#F1F5F3",
        "ink_soft": "#B7C4BD",
        "muted": "#7C8C84",
        "faint": "#47554E",
        "accent": "#34D399",
        "accent_soft": "rgba(52,211,153,0.12)",
        "accent_glow": "rgba(52,211,153,0.32)",
        "amber": "#F59E0B",
        "amber_soft": "rgba(245,158,11,0.16)",
        "ruby": "#FB7185",
        "cyan": "#38BDF8",
        "pill_bg": "#141B18",
        "pill_border": "#24312B",
        "wordmark_fill": "#F3F7F5",
        "wordmark_guide": "#1F2B25",
        "shimmer": "#34D399",
    },
    "light": {
        "edition": "ARCHIVAL // VELLUM",
        "bg": "#FAF9F5",
        "surface": "#F3F1EA",
        "surface_alt": "#ECE9DF",
        "viewport": "#F8F7F2",
        "border": "#D8D4C7",
        "border_strong": "#BFB9A8",
        "bevel": "rgba(255,255,255,0.85)",
        "grid": "#E7E3D7",
        "grid_subtle": "#EFECE3",
        "ink": "#141A17",
        "ink_soft": "#2F3A34",
        "muted": "#5C6861",
        "faint": "#929C96",
        "accent": "#059669",
        "accent_soft": "rgba(5,150,105,0.10)",
        "accent_glow": "rgba(5,150,105,0.22)",
        "amber": "#B45309",
        "amber_soft": "rgba(180,83,9,0.14)",
        "ruby": "#E11D48",
        "cyan": "#0284C7",
        "pill_bg": "#FAF9F5",
        "pill_border": "#CFCBBF",
        "wordmark_fill": "#141A17",
        "wordmark_guide": "#DDD8CB",
        "shimmer": "#059669",
    },
}


def corner_marks(x: int, y: int, w: int, h: int, color: str, size: int = 6) -> str:
    """Precision drafting crosshairs at the four inner corners of a plate."""
    pts = [
        (x, y),
        (x + w, y),
        (x, y + h),
        (x + w, y + h),
    ]
    lines = []
    for px, py in pts:
        lines.append(
            f'<line x1="{px - size}" y1="{py}" x2="{px + size}" y2="{py}" stroke="{color}" stroke-width="1"/>'
        )
        lines.append(
            f'<line x1="{px}" y1="{py - size}" x2="{px}" y2="{py + size}" stroke="{color}" stroke-width="1"/>'
        )
    return "\n    ".join(lines)


def screw_dots(x: int, y: int, w: int, h: int, color: str, pad: int = 10) -> str:
    """Four subtle machined hardware fastener dots."""
    pts = [
        (x + pad, y + pad),
        (x + w - pad, y + pad),
        (x + pad, y + h - pad),
        (x + w - pad, y + h - pad),
    ]
    return "\n    ".join(
        f'<circle cx="{px}" cy="{py}" r="1.5" fill="{color}"/>' for px, py in pts
    )


def aatif_wordmark_paths(ox: float, oy: float) -> str:
    """
    Hand-crafted geometric architectural vector letterforms for 'AATIF'.
    Designed on a 76px cap-height grid with crisp chamfered geometry so it renders
    identically on every OS without external font loading.
    Total width ≈ 328px, height = 76px.
    """
    # Stroke-constructed + filled geometric forms for ultra-sharp precision
    # Letter heights: 0..76 (cap=0, mid=42, base=76)
    # A (x=0..64): wide architectural apex with crisp crossbar
    a1 = (
        "M 0,76 L 26,0 L 38,0 L 64,76 L 50,76 L 44,57 L 20,57 L 14,76 Z "
        "M 23.5,45.5 L 40.5,45.5 L 32,19 Z"
    )
    # Second A shifted +74
    # T (x=148..206): broad balanced bar with crisp stem
    t_path = "M 148,0 L 206,0 L 206,12 L 183.5,12 L 183.5,76 L 170.5,76 L 170.5,12 L 148,12 Z"
    # I (x=222..246): architectural monolith bar with subtle top/bottom micro-serif ticks
    i_path = "M 222,0 L 248,0 L 248,11 L 241.5,11 L 241.5,65 L 248,65 L 248,76 L 222,76 L 222,65 L 228.5,65 L 228.5,11 L 222,11 Z"
    # F (x=266..322): crisp Swiss asymmetric crossbar
    f_path = "M 266,0 L 322,0 L 322,12 L 279,12 L 279,34 L 314,34 L 314,45.5 L 279,45.5 L 279,76 L 266,76 Z"

    return f"""
    <g transform="translate({ox},{oy})">
      <path d="{a1}" fill-rule="evenodd"/>
      <path d="{a1}" transform="translate(74,0)" fill-rule="evenodd"/>
      <path d="{t_path}"/>
      <path d="{i_path}"/>
      <path d="{f_path}"/>
    </g>"""


def build_hero(theme_name: str) -> str:
    t = THEMES[theme_name]
    w, h = 900, 356

    # Build 72 precision bezel ticks around the kinetic astrolabe (cx=726, cy=182, r=114)
    cx, cy = 726, 182
    bezel_ticks = []
    for i in range(72):
        deg = i * 5
        rad = math.radians(deg - 90)
        is_major = (deg % 30 == 0)
        is_mid = (deg % 15 == 0) and not is_major
        r_outer = 116
        r_inner = 104 if is_major else (109 if is_mid else 112)
        x1 = cx + r_inner * math.cos(rad)
        y1 = cy + r_inner * math.sin(rad)
        x2 = cx + r_outer * math.cos(rad)
        y2 = cy + r_outer * math.sin(rad)
        col = t["muted"] if is_major else t["border_strong"]
        sw = "1.4" if is_major else "0.9"
        bezel_ticks.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{sw}"/>'
        )
    bezel_svg = "\n      ".join(bezel_ticks)

    # Cardinal degree readouts
    cardinals = [
        (cx, cy - 124, "000°", "middle"),
        (cx + 126, cy + 3, "090°", "start"),
        (cx, cy + 132, "180°", "middle"),
        (cx - 126, cy + 3, "270°", "end"),
    ]
    cardinal_svg = "\n      ".join(
        f'<text x="{px}" y="{py}" text-anchor="{anc}" font-family="{FONT_MONO}" font-size="8.5" letter-spacing="1" fill="{t["faint"]}">{lbl}</text>'
        for px, py, lbl, anc in cardinals
    )

    wordmark = aatif_wordmark_paths(48, 108)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Aatif — Built with restraint. Engineered to endure.">
  <defs>
    <pattern id="hero-grid-{theme_name}" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M 24 0 L 0 0 0 24" fill="none" stroke="{t["grid"]}" stroke-width="0.75"/>
    </pattern>

    <radialGradient id="dial-glow-{theme_name}" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{t["accent"]}" stop-opacity="0.16"/>
      <stop offset="55%" stop-color="{t["accent"]}" stop-opacity="0.04"/>
      <stop offset="100%" stop-color="{t["accent"]}" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="shimmer-grad-{theme_name}" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{t["shimmer"]}" stop-opacity="0"/>
      <stop offset="45%" stop-color="{t["shimmer"]}" stop-opacity="0.55"/>
      <stop offset="55%" stop-color="{t["ink"]}" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="{t["shimmer"]}" stop-opacity="0"/>
    </linearGradient>

    <clipPath id="wordmark-clip-{theme_name}">
      {wordmark}
    </clipPath>

    <clipPath id="chassis-clip-{theme_name}">
      <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14"/>
    </clipPath>
  </defs>

  <style>
    @keyframes orbit-cw {{
      from {{ transform: rotate(0deg); }}
      to {{ transform: rotate(360deg); }}
    }}
    @keyframes orbit-ccw {{
      from {{ transform: rotate(360deg); }}
      to {{ transform: rotate(0deg); }}
    }}
    @keyframes radar-pulse {{
      0% {{ r: 8px; opacity: 0.75; }}
      100% {{ r: 78px; opacity: 0; }}
    }}
    @keyframes led-breathe {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0.35; }}
    }}
    @keyframes shimmer-sweep {{
      0% {{ transform: translateX(-160px); }}
      35%, 100% {{ transform: translateX(460px); }}
    }}
    .ring-cw {{
      transform-origin: {cx}px {cy}px;
      animation: orbit-cw 54s linear infinite;
    }}
    .ring-ccw {{
      transform-origin: {cx}px {cy}px;
      animation: orbit-ccw 34s linear infinite;
    }}
    .ring-fast {{
      transform-origin: {cx}px {cy}px;
      animation: orbit-cw 18s linear infinite;
    }}
    .pulse-ring {{
      animation: radar-pulse 4.2s cubic-bezier(0.22, 1, 0.36, 1) infinite;
    }}
    .led {{
      animation: led-breathe 2.8s ease-in-out infinite;
    }}
    .shimmer {{
      animation: shimmer-sweep 7.5s ease-in-out infinite;
    }}
    @media (prefers-reduced-motion: reduce) {{
      .ring-cw, .ring-ccw, .ring-fast, .pulse-ring, .led, .shimmer {{
        animation: none !important;
      }}
    }}
  </style>

  <!-- Base Anodized / Vellum Chassis -->
  <g clip-path="url(#chassis-clip-{theme_name})">
    <rect x="0" y="0" width="{w}" height="{h}" fill="{t["bg"]}"/>
    <rect x="0" y="0" width="{w}" height="{h}" fill="url(#hero-grid-{theme_name})" opacity="0.85"/>
    <!-- Subtle vignette glow behind instrument dial -->
    <circle cx="{cx}" cy="{cy}" r="165" fill="url(#dial-glow-{theme_name})"/>
    <!-- Top specular bevel -->
    <line x1="14" y1="1.5" x2="{w - 14}" y2="1.5" stroke="{t["bevel"]}" stroke-width="1"/>
  </g>

  <!-- Outer & Inner Hairline Borders -->
  <rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" rx="14" fill="none" stroke="{t["border"]}" stroke-width="1.25"/>
  <rect x="14" y="14" width="{w - 28}" height="{h - 28}" rx="8" fill="none" stroke="{t["border"]}" stroke-width="0.75" opacity="0.65"/>

  <!-- Corner Registration Marks -->
  <g opacity="0.85">
    {corner_marks(22, 22, w - 44, h - 44, t["faint"], 4)}
  </g>

  <!-- Top Telemetry Header Strip -->
  <g font-family="{FONT_MONO}" font-size="9.5" letter-spacing="1.4">
    <circle cx="48" cy="37" r="3.5" fill="{t["accent"]}" class="led"/>
    <circle cx="48" cy="37" r="6.5" fill="{t["accent"]}" opacity="0.18"/>
    <text x="62" y="40.5" fill="{t["ink_soft"]}" font-weight="600">PLATE 00</text>
    <text x="132" y="40.5" fill="{t["faint"]}">//</text>
    <text x="150" y="40.5" fill="{t["muted"]}">ENGINEERING MONOGRAPH</text>
    <text x="{w - 48}" y="40.5" text-anchor="end" fill="{t["muted"]}">{t["edition"]}</text>
  </g>
  <line x1="36" y1="54" x2="{w - 36}" y2="54" stroke="{t["border"]}" stroke-width="0.9"/>

  <!-- Left Column: Architectural Typography & Philosophy -->
  <g>
    <!-- Eyebrow Spec -->
    <text x="48" y="84" font-family="{FONT_MONO}" font-size="9.5" letter-spacing="2.2" fill="{t["accent"]}" font-weight="600">LOCAL-FIRST SYSTEMS · MOBILE · WEB · DESKTOP</text>

    <!-- Typographic Blueprint Construction Lines around AATIF -->
    <g stroke="{t["wordmark_guide"]}" stroke-width="0.75" stroke-dasharray="3 3">
      <line x1="40" y1="108" x2="420" y2="108"/>
      <line x1="40" y1="150" x2="420" y2="150"/>
      <line x1="40" y1="184" x2="420" y2="184"/>
    </g>
    <text x="426" y="111" font-family="{FONT_MONO}" font-size="7.5" fill="{t["faint"]}">CAP 76</text>
    <text x="426" y="186" font-family="{FONT_MONO}" font-size="7.5" fill="{t["faint"]}">BASE 00</text>

    <!-- Bespoke Geometric Vector Wordmark: AATIF -->
    <g fill="{t["wordmark_fill"]}">
      {wordmark}
    </g>

    <!-- Animated Optical Light Sheen clipped cleanly to AATIF letterforms -->
    <g clip-path="url(#wordmark-clip-{theme_name})">
      <g class="shimmer">
        <rect x="0" y="96" width="110" height="100" fill="url(#shimmer-grad-{theme_name})" transform="skewX(-22)" opacity="0.65"/>
      </g>
    </g>

    <!-- Weighty Quote Tagline -->
    <rect x="48" y="210" width="3" height="44" rx="1.5" fill="{t["accent"]}"/>
    <text x="64" y="229" font-family="{FONT_SANS}" font-size="18.5" font-weight="600" letter-spacing="-0.3" fill="{t["ink"]}">Built with restraint. Engineered to endure.</text>
    <text x="64" y="250" font-family="{FONT_MONO}" font-size="11" fill="{t["muted"]}">Calm software that respects the machine — online or off the grid.</text>
  </g>

  <!-- Bottom Left Calibrated Readout Strip -->
  <line x1="48" y1="278" x2="532" y2="278" stroke="{t["border"]}" stroke-width="0.9"/>
  <g font-family="{FONT_MONO}">
    <text x="48" y="297" font-size="8.5" letter-spacing="1.2" fill="{t["faint"]}">HANDLE</text>
    <text x="48" y="314" font-size="11" font-weight="600" fill="{t["ink_soft"]}">@dev-Aatif</text>

    <line x1="166" y1="286" x2="166" y2="318" stroke="{t["border"]}" stroke-width="0.9"/>
    <text x="182" y="297" font-size="8.5" letter-spacing="1.2" fill="{t["faint"]}">SURFACES</text>
    <text x="182" y="314" font-size="11" font-weight="600" fill="{t["ink_soft"]}">04 ACTIVE</text>

    <line x1="292" y1="286" x2="292" y2="318" stroke="{t["border"]}" stroke-width="0.9"/>
    <text x="308" y="297" font-size="8.5" letter-spacing="1.2" fill="{t["faint"]}">PINNED</text>
    <text x="308" y="314" font-size="11" font-weight="600" fill="{t["ink_soft"]}">06 BUILDS</text>

    <line x1="414" y1="286" x2="414" y2="318" stroke="{t["border"]}" stroke-width="0.9"/>
    <text x="430" y="297" font-size="8.5" letter-spacing="1.2" fill="{t["faint"]}">POSTURE</text>
    <text x="430" y="314" font-size="11" font-weight="600" fill="{t["accent"]}">LOCAL-FIRST</text>
  </g>

  <!-- Vertical Separator before Kinetic Instrument -->
  <line x1="564" y1="68" x2="564" y2="322" stroke="{t["border"]}" stroke-width="0.9" stroke-dasharray="3 4"/>

  <!-- Right Column: Kinetic Optical Astrolabe / Horological Dial -->
  <g>
    <!-- Outer Fixed Bezel -->
    <circle cx="{cx}" cy="{cy}" r="116" fill="{t["viewport"]}" fill-opacity="0.55" stroke="{t["border_strong"]}" stroke-width="1"/>
    <circle cx="{cx}" cy="{cy}" r="96" fill="none" stroke="{t["border"]}" stroke-width="0.75"/>
    <circle cx="{cx}" cy="{cy}" r="64" fill="none" stroke="{t["border"]}" stroke-width="0.75" stroke-dasharray="2 4"/>
    <circle cx="{cx}" cy="{cy}" r="34" fill="none" stroke="{t["border_strong"]}" stroke-width="0.8"/>

    <!-- Crosshairs -->
    <line x1="{cx - 98}" y1="{cy}" x2="{cx + 98}" y2="{cy}" stroke="{t["border"]}" stroke-width="0.75"/>
    <line x1="{cx}" y1="{cy - 98}" x2="{cx}" y2="{cy + 98}" stroke="{t["border"]}" stroke-width="0.75"/>
    <line x1="{cx - 64}" y1="{cy - 64}" x2="{cx + 64}" y2="{cy + 64}" stroke="{t["border"]}" stroke-width="0.6" opacity="0.55"/>
    <line x1="{cx + 64}" y1="{cy - 64}" x2="{cx - 64}" y2="{cy + 64}" stroke="{t["border"]}" stroke-width="0.6" opacity="0.55"/>

    <!-- Precision 72-Tick Vernier Bezel -->
    <g>
      {bezel_svg}
    </g>

    <!-- Cardinal Degree Labels -->
    <g>
      {cardinal_svg}
    </g>

    <!-- Sonar / Optical Calibration Pulse -->
    <circle cx="{cx}" cy="{cy}" r="10" fill="none" stroke="{t["accent"]}" stroke-width="1.2" class="pulse-ring"/>

    <!-- Ring 1: Slow Clockwise Solar Azimuth Track (Hayya nod) -->
    <g class="ring-cw">
      <circle cx="{cx}" cy="{cy}" r="84" fill="none" stroke="{t["accent"]}" stroke-width="1.1" stroke-dasharray="36 18 8 18 96 40" opacity="0.75"/>
      <!-- Amber Solar Zenith Node -->
      <circle cx="{cx}" cy="{cy - 84}" r="4.2" fill="{t["amber"]}"/>
      <circle cx="{cx}" cy="{cy - 84}" r="8.5" fill="{t["amber_soft"]}"/>
      <!-- Opposite Calibration Pip -->
      <rect x="{cx - 2.5}" y="{cy + 81.5}" width="5" height="5" fill="{t["accent"]}" transform="rotate(45 {cx} {cy + 84})"/>
    </g>

    <!-- Ring 2: Counter-Clockwise Darkroom Optical Aperture (Pixel-Forge nod) -->
    <g class="ring-ccw">
      <circle cx="{cx}" cy="{cy}" r="52" fill="none" stroke="{t["ink_soft"]}" stroke-width="1.4" stroke-dasharray="48 60 22 60" opacity="0.55"/>
      <circle cx="{cx + 52}" cy="{cy}" r="3" fill="{t["ruby"]}"/>
      <line x1="{cx - 57}" y1="{cy}" x2="{cx - 46}" y2="{cy}" stroke="{t["accent"]}" stroke-width="1.8"/>
    </g>

    <!-- Ring 3: Fast Inner Sweeping Hand -->
    <g class="ring-fast">
      <line x1="{cx}" y1="{cy + 14}" x2="{cx}" y2="{cy - 44}" stroke="{t["accent"]}" stroke-width="1.35" stroke-linecap="round"/>
      <circle cx="{cx}" cy="{cy - 44}" r="2.2" fill="{t["accent"]}"/>
    </g>

    <!-- Central Aperture Reticle -->
    <polygon points="{cx},{cy - 11} {cx + 11},{cy} {cx},{cy + 11} {cx - 11},{cy}" fill="{t["surface"]}" stroke="{t["accent"]}" stroke-width="1.2"/>
    <circle cx="{cx}" cy="{cy}" r="3.2" fill="{t["accent"]}"/>

    <!-- Micro Label under Instrument -->
    <text x="{cx}" y="330" text-anchor="middle" font-family="{FONT_MONO}" font-size="8.5" letter-spacing="1.6" fill="{t["faint"]}">CALIBRATED · PURE VECTOR</text>
  </g>
</svg>
'''


def build_divider(theme_name: str, index: str, title: str, right_meta: str) -> str:
    t = THEMES[theme_name]
    w, h = 900, 42
    ticks = "\n    ".join(
        f'<line x1="{x}" y1="36" x2="{x}" y2="{40 if x % 40 == 0 else 38.5}" stroke="{t["border_strong"] if x % 40 == 0 else t["border"]}" stroke-width="0.9"/>'
        for x in range(16, w - 12, 10)
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{index} {title}">
  <rect x="0" y="0" width="{w}" height="{h}" fill="none"/>
  <rect x="4" y="8" width="32" height="19" rx="4" fill="{t["accent_soft"]}" stroke="{t["accent"]}" stroke-width="0.9"/>
  <text x="20" y="21" text-anchor="middle" font-family="{FONT_MONO}" font-size="10" font-weight="700" fill="{t["accent"]}">{escape(index)}</text>
  <text x="48" y="21.5" font-family="{FONT_MONO}" font-size="11.5" font-weight="700" letter-spacing="2.2" fill="{t["ink"]}">{escape(title)}</text>
  <text x="{w - 6}" y="21" text-anchor="end" font-family="{FONT_MONO}" font-size="9.5" letter-spacing="1.2" fill="{t["muted"]}">{escape(right_meta)}</text>
  <line x1="4" y1="34" x2="{w - 4}" y2="34" stroke="{t["border"]}" stroke-width="1"/>
  <g opacity="0.8">
    {ticks}
  </g>
</svg>
'''


def render_pills(items: list[str], x0: int, y0: int, max_w: int, t: dict, highlight_first: bool = False) -> str:
    """Layout crisp monospace hardware specification pills with automatic line wrap."""
    cx = x0
    cy = y0
    pill_h = 24
    gap_x = 7
    gap_y = 8
    out = []
    for idx, label in enumerate(items):
        # Monospace character width ~6.9px at 10.5px font-size + 20px padding
        pw = max(44, int(len(label) * 7.1 + 22))
        if cx + pw > x0 + max_w and cx > x0:
            cx = x0
            cy += pill_h + gap_y
        is_hl = highlight_first and idx == 0
        bg = t["accent_soft"] if is_hl else t["pill_bg"]
        bd = t["accent"] if is_hl else t["pill_border"]
        fg = t["accent"] if is_hl else t["ink_soft"]
        out.append(
            f'<rect x="{cx}" y="{cy}" width="{pw}" height="{pill_h}" rx="5" fill="{bg}" stroke="{bd}" stroke-width="0.95"/>'
        )
        out.append(
            f'<text x="{cx + pw / 2:.1f}" y="{cy + 15.5}" text-anchor="middle" font-family="{FONT_MONO}" font-size="10.5" font-weight="{"600" if is_hl else "500"}" fill="{fg}">{escape(label)}</text>'
        )
        cx += pw + gap_x
    return "\n    ".join(out)


def build_patchbay(theme_name: str) -> str:
    t = THEMES[theme_name]
    w, h = 900, 332

    # Exact stack provided by the user
    ch1 = ["Dart", "Flutter", "Riverpod", "Kotlin", "Jetpack Compose", "Material 3"]
    ch2 = ["TypeScript", "JavaScript", "React", "Next.js", "Tailwind CSS", "Electron"]
    ch3 = ["Python", "Node.js", "Express", "PostgreSQL", "SQLite"]
    ch4 = ["Git"]

    # Module positions (2x2 balanced hardware rack)
    # Row 1: y=44..170 (h=126), Row 2: y=184..304 (h=120)
    m_w = 420
    left_x = 22
    right_x = 458

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Capability Patchbay — Mobile, Web and Desktop, Backend and Data, Version Control">
  <defs>
    <pattern id="rack-grid-{theme_name}" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="{t["grid_subtle"]}" stroke-width="0.7"/>
    </pattern>
  </defs>

  <style>
    @keyframes bus-flow {{
      from {{ stroke-dashoffset: 120; }}
      to {{ stroke-dashoffset: 0; }}
    }}
    @keyframes bar-eq-1 {{
      0%, 100% {{ height: 6px; y: 69px; }}
      50% {{ height: 14px; y: 61px; }}
    }}
    @keyframes bar-eq-2 {{
      0%, 100% {{ height: 13px; y: 62px; }}
      50% {{ height: 5px; y: 70px; }}
    }}
    @keyframes bar-eq-3 {{
      0%, 100% {{ height: 9px; y: 66px; }}
      50% {{ height: 15px; y: 60px; }}
    }}
    @keyframes packet-slide {{
      0% {{ transform: translateX(0px); opacity: 0; }}
      20% {{ opacity: 1; }}
      80% {{ opacity: 1; }}
      100% {{ transform: translateX(52px); opacity: 0; }}
    }}
    @keyframes node-pulse {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0.35; }}
    }}
    .bus-trace {{
      stroke-dasharray: 12 28;
      animation: bus-flow 3.6s linear infinite;
    }}
    .eq1 {{ animation: bar-eq-1 1.9s ease-in-out infinite; }}
    .eq2 {{ animation: bar-eq-2 2.3s ease-in-out infinite; }}
    .eq3 {{ animation: bar-eq-3 1.6s ease-in-out infinite; }}
    .pkt1 {{ animation: packet-slide 2.4s linear infinite; }}
    .pkt2 {{ animation: packet-slide 2.4s linear 1.2s infinite; }}
    .led-soft {{ animation: node-pulse 3s ease-in-out infinite; }}
    @media (prefers-reduced-motion: reduce) {{
      .bus-trace, .eq1, .eq2, .eq3, .pkt1, .pkt2, .led-soft {{ animation: none !important; }}
    }}
  </style>

  <!-- Rack Chassis -->
  <rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" rx="12" fill="{t["bg"]}" stroke="{t["border"]}" stroke-width="1.2"/>
  <rect x="2" y="2" width="{w - 4}" height="{h - 4}" rx="11" fill="url(#rack-grid-{theme_name})" opacity="0.75"/>

  <!-- Top Signal Bus Header -->
  <g font-family="{FONT_MONO}" font-size="9" letter-spacing="1.4">
    <circle cx="28" cy="22" r="3" fill="{t["accent"]}" class="led-soft"/>
    <text x="40" y="25" fill="{t["muted"]}">SIGNAL BUS // 04 ACTIVE CHANNELS</text>
    <!-- Live animated copper/emerald bus line -->
    <line x1="278" y1="22" x2="735" y2="22" stroke="{t["border_strong"]}" stroke-width="1"/>
    <line x1="278" y1="22" x2="735" y2="22" stroke="{t["accent"]}" stroke-width="1.5" class="bus-trace"/>
    <text x="{w - 24}" y="25" text-anchor="end" fill="{t["faint"]}">SYNC: NOMINAL</text>
  </g>

  <!-- CH.01 // MOBILE -->
  <g>
    <rect x="{left_x}" y="42" width="{m_w}" height="128" rx="9" fill="{t["surface"]}" stroke="{t["border"]}" stroke-width="1"/>
    {screw_dots(left_x, 42, m_w, 128, t["border_strong"], 9)}
    <circle cx="{left_x + 24}" cy="64" r="3" fill="{t["accent"]}"/>
    <text x="{left_x + 35}" y="67.5" font-family="{FONT_MONO}" font-size="10" font-weight="700" letter-spacing="1.5" fill="{t["accent"]}">CH.01</text>
    <text x="{left_x + 82}" y="67.5" font-family="{FONT_SANS}" font-size="13" font-weight="600" fill="{t["ink"]}">Mobile</text>
    <!-- Micro-meter (3 smooth animated signal bars) -->
    <rect x="{left_x + m_w - 48}" y="57" width="28" height="20" rx="3" fill="{t["viewport"]}" stroke="{t["border"]}" stroke-width="0.8"/>
    <rect x="{left_x + m_w - 43}" y="67" width="3.5" height="8" rx="1" fill="{t["accent"]}" class="eq1"/>
    <rect x="{left_x + m_w - 36}" y="62" width="3.5" height="13" rx="1" fill="{t["accent"]}" class="eq2"/>
    <rect x="{left_x + m_w - 29}" y="65" width="3.5" height="10" rx="1" fill="{t["amber"]}" class="eq3"/>
    <line x1="{left_x + 18}" y1="84" x2="{left_x + m_w - 18}" y2="84" stroke="{t["border"]}" stroke-width="0.8"/>
    {render_pills(ch1, left_x + 18, 96, m_w - 36, t)}
  </g>

  <!-- CH.02 // WEB AND DESKTOP -->
  <g>
    <rect x="{right_x}" y="42" width="{m_w}" height="128" rx="9" fill="{t["surface"]}" stroke="{t["border"]}" stroke-width="1"/>
    {screw_dots(right_x, 42, m_w, 128, t["border_strong"], 9)}
    <circle cx="{right_x + 24}" cy="64" r="3" fill="{t["accent"]}"/>
    <text x="{right_x + 35}" y="67.5" font-family="{FONT_MONO}" font-size="10" font-weight="700" letter-spacing="1.5" fill="{t["accent"]}">CH.02</text>
    <text x="{right_x + 82}" y="67.5" font-family="{FONT_SANS}" font-size="13" font-weight="600" fill="{t["ink"]}">Web and desktop</text>
    <!-- Micro-viewport pulse oscilloscope -->
    <rect x="{right_x + m_w - 66}" y="57" width="46" height="20" rx="3" fill="{t["viewport"]}" stroke="{t["border"]}" stroke-width="0.8"/>
    <path d="M {right_x + m_w - 62} 67 L {right_x + m_w - 53} 67 L {right_x + m_w - 49} 61 L {right_x + m_w - 44} 73 L {right_x + m_w - 39} 65 L {right_x + m_w - 35} 67 L {right_x + m_w - 24} 67" fill="none" stroke="{t["accent"]}" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="{right_x + m_w - 26}" cy="67" r="2" fill="{t["accent"]}" class="led-soft"/>
    <line x1="{right_x + 18}" y1="84" x2="{right_x + m_w - 18}" y2="84" stroke="{t["border"]}" stroke-width="0.8"/>
    {render_pills(ch2, right_x + 18, 96, m_w - 36, t)}
  </g>

  <!-- CH.03 // BACKEND AND DATA -->
  <g>
    <rect x="{left_x}" y="184" width="{m_w}" height="128" rx="9" fill="{t["surface"]}" stroke="{t["border"]}" stroke-width="1"/>
    {screw_dots(left_x, 184, m_w, 128, t["border_strong"], 9)}
    <circle cx="{left_x + 24}" cy="206" r="3" fill="{t["accent"]}"/>
    <text x="{left_x + 35}" y="209.5" font-family="{FONT_MONO}" font-size="10" font-weight="700" letter-spacing="1.5" fill="{t["accent"]}">CH.03</text>
    <text x="{left_x + 82}" y="209.5" font-family="{FONT_SANS}" font-size="13" font-weight="600" fill="{t["ink"]}">Backend and data</text>
    <!-- Animated data-bus packet trace -->
    <rect x="{left_x + m_w - 78}" y="199" width="58" height="20" rx="3" fill="{t["viewport"]}" stroke="{t["border"]}" stroke-width="0.8"/>
    <line x1="{left_x + m_w - 72}" y1="209" x2="{left_x + m_w - 26}" y2="209" stroke="{t["border_strong"]}" stroke-width="1"/>
    <circle cx="{left_x + m_w - 72}" cy="209" r="2.2" fill="{t["accent"]}" class="pkt1"/>
    <circle cx="{left_x + m_w - 72}" cy="209" r="2.2" fill="{t["amber"]}" class="pkt2"/>
    <line x1="{left_x + 18}" y1="226" x2="{left_x + m_w - 18}" y2="226" stroke="{t["border"]}" stroke-width="0.8"/>
    {render_pills(ch3, left_x + 18, 238, m_w - 36, t)}
  </g>

  <!-- CH.04 // VERSION CONTROL -->
  <g>
    <rect x="{right_x}" y="184" width="{m_w}" height="128" rx="9" fill="{t["surface"]}" stroke="{t["border"]}" stroke-width="1"/>
    {screw_dots(right_x, 184, m_w, 128, t["border_strong"], 9)}
    <circle cx="{right_x + 24}" cy="206" r="3" fill="{t["accent"]}"/>
    <text x="{right_x + 35}" y="209.5" font-family="{FONT_MONO}" font-size="10" font-weight="700" letter-spacing="1.5" fill="{t["accent"]}">CH.04</text>
    <text x="{right_x + 82}" y="209.5" font-family="{FONT_SANS}" font-size="13" font-weight="600" fill="{t["ink"]}">Version control</text>
    <line x1="{right_x + 18}" y1="226" x2="{right_x + m_w - 18}" y2="226" stroke="{t["border"]}" stroke-width="0.8"/>
    <!-- Highlighted Git pill -->
    {render_pills(ch4, right_x + 18, 240, 100, t, highlight_first=True)}
    <!-- Crisp branching/merging commit-graph schematic inside CH.04 -->
    <g transform="translate({right_x + 96}, 238)">
      <rect x="0" y="0" width="302" height="50" rx="6" fill="{t["viewport"]}" stroke="{t["border"]}" stroke-width="0.85"/>
      <!-- Main branch line -->
      <line x1="20" y1="18" x2="280" y2="18" stroke="{t["border_strong"]}" stroke-width="1.4"/>
      <line x1="20" y1="18" x2="280" y2="18" stroke="{t["accent"]}" stroke-width="1.4" class="bus-trace"/>
      <!-- Feature branch curve -->
      <path d="M 74 18 C 90 18, 94 35, 112 35 L 188 35 C 206 35, 210 18, 226 18" fill="none" stroke="{t["amber"]}" stroke-width="1.25" opacity="0.85"/>
      <!-- Commit nodes -->
      <circle cx="34" cy="18" r="3.2" fill="{t["surface"]}" stroke="{t["accent"]}" stroke-width="1.4"/>
      <circle cx="74" cy="18" r="3.2" fill="{t["surface"]}" stroke="{t["accent"]}" stroke-width="1.4"/>
      <circle cx="128" cy="35" r="3" fill="{t["surface"]}" stroke="{t["amber"]}" stroke-width="1.4"/>
      <circle cx="174" cy="35" r="3" fill="{t["surface"]}" stroke="{t["amber"]}" stroke-width="1.4"/>
      <circle cx="226" cy="18" r="3.2" fill="{t["surface"]}" stroke="{t["accent"]}" stroke-width="1.4"/>
      <circle cx="268" cy="18" r="4" fill="{t["accent"]}" class="led-soft"/>
      <text x="268" y="39" text-anchor="middle" font-family="{FONT_MONO}" font-size="8" fill="{t["muted"]}">HEAD</text>
      <text x="20" y="39" font-family="{FONT_MONO}" font-size="8" fill="{t["faint"]}">MAIN · CLEAN DIFFS</text>
    </g>
  </g>
</svg>
'''


def card_shell(
    theme_name: str,
    spec_code: str,
    surface_tag: str,
    title: str,
    subtitle: str,
    desc_line1: str,
    desc_line2: str,
    stack_line: str,
    extra_css: str,
    viewport_svg: str,
    card_id: str,
) -> str:
    """Consistent 436x242 museum-grade kinetic specimen card shell."""
    t = THEMES[theme_name]
    w, h = 436, 242
    sub_svg = ""
    if subtitle:
        # Right-aligned pill badge so it never collides with title on any OS font
        badge_w = max(56, int(len(subtitle) * 6.5 + 16))
        bx = w - 18 - badge_w
        sub_svg = (
            f'<rect x="{bx}" y="144" width="{badge_w}" height="19" rx="4" fill="{t["accent_soft"]}" stroke="{t["accent"]}" stroke-width="0.75"/>'
            f'<text x="{bx + badge_w / 2:.1f}" y="156.5" text-anchor="middle" font-family="{FONT_MONO}" font-size="8.5" font-weight="600" letter-spacing="0.8" fill="{t["accent"]}">{escape(subtitle)}</text>'
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{escape(title)} — {escape(desc_line1)}">
  <defs>
    <pattern id="vp-grid-{card_id}-{theme_name}" width="16" height="16" patternUnits="userSpaceOnUse">
      <path d="M 16 0 L 0 0 0 16" fill="none" stroke="{t["grid"]}" stroke-width="0.65"/>
    </pattern>
    <clipPath id="vp-clip-{card_id}-{theme_name}">
      <rect x="18" y="38" width="400" height="90" rx="7"/>
    </clipPath>
  </defs>

  <style>
    @keyframes card-led {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0.35; }}
    }}
    .cled {{ animation: card-led 3.2s ease-in-out infinite; }}
    {extra_css}
    @media (prefers-reduced-motion: reduce) {{
      * {{ animation: none !important; }}
    }}
  </style>

  <!-- Card Chassis -->
  <rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" rx="11" fill="{t["surface"]}" stroke="{t["border"]}" stroke-width="1.15"/>
  <line x1="12" y1="1.5" x2="{w - 12}" y2="1.5" stroke="{t["bevel"]}" stroke-width="1"/>

  <!-- Header Strip -->
  <circle cx="24" cy="21" r="2.8" fill="{t["accent"]}" class="cled"/>
  <text x="34" y="24" font-family="{FONT_MONO}" font-size="9" font-weight="700" letter-spacing="1.2" fill="{t["muted"]}">{escape(spec_code)}</text>
  <text x="100" y="24" font-family="{FONT_MONO}" font-size="9" letter-spacing="1" fill="{t["faint"]}">// {escape(surface_tag)}</text>
  <text x="{w - 20}" y="24" text-anchor="end" font-family="{FONT_MONO}" font-size="11" fill="{t["accent"]}">↗</text>

  <!-- Panoramic Kinetic Instrument Viewport (18, 38, 400 x 90) -->
  <rect x="18" y="38" width="400" height="90" rx="7" fill="{t["viewport"]}" stroke="{t["border_strong"]}" stroke-width="0.9"/>
  <g clip-path="url(#vp-clip-{card_id}-{theme_name})">
    <rect x="18" y="38" width="400" height="90" fill="url(#vp-grid-{card_id}-{theme_name})" opacity="0.75"/>
    {viewport_svg}
  </g>

  <!-- Title & Concise Engineering Description -->
  <text x="20" y="159" font-family="{FONT_SANS}" font-size="16.5" font-weight="700" letter-spacing="-0.25" fill="{t["ink"]}">{escape(title)}</text>
  {sub_svg}
  <text x="20" y="179" font-family="{FONT_SANS}" font-size="11.5" fill="{t["muted"]}">{escape(desc_line1)}</text>
  <text x="20" y="195" font-family="{FONT_SANS}" font-size="11.5" fill="{t["muted"]}">{escape(desc_line2)}</text>

  <!-- Bottom Stack Calibration Footer -->
  <line x1="18" y1="210" x2="{w - 18}" y2="210" stroke="{t["border"]}" stroke-width="0.85"/>
  <text x="20" y="227" font-family="{FONT_MONO}" font-size="9" letter-spacing="0.9" fill="{t["faint"]}">{escape(stack_line)}</text>
</svg>
'''


def build_card_pixel_forge(theme_name: str) -> str:
    """SPEC.01: Pixel-Forge — Animated Darkroom 4x Split-Loupe Upscaler."""
    t = THEMES[theme_name]
    # Coarse 1x pixel blocks (left of loupe) vs ultra-crisp 4x geometric contour (right of loupe)
    # Viewport bounds: x=18..418 (400w), y=38..128 (90h)
    blocks = []
    block_coords = [
        (42, 54, 0.20), (58, 54, 0.35), (74, 54, 0.55), (90, 54, 0.30), (106, 54, 0.18),
        (42, 70, 0.32), (58, 70, 0.65), (74, 70, 0.85), (90, 70, 0.52), (106, 70, 0.26),
        (42, 86, 0.22), (58, 86, 0.45), (74, 86, 0.62), (90, 86, 0.38), (106, 86, 0.16),
    ]
    for bx, by, op in block_coords:
        blocks.append(f'<rect x="{bx}" y="{by}" width="14" height="14" rx="1" fill="{t["muted"]}" opacity="{op}"/>')
    blocks_svg = "\n      ".join(blocks)

    css = """
    @keyframes loupe-glide {
      0%, 100% { transform: translateX(0px); }
      50% { transform: translateX(138px); }
    }
    .loupe { animation: loupe-glide 5.6s ease-in-out infinite; }
    """
    vp = f"""
    <!-- Left Zone: 1x Low-Res Pixel Input -->
    <g>
      {blocks_svg}
      <text x="34" y="118" font-family="{FONT_MONO}" font-size="8" letter-spacing="1" fill="{t["faint"]}">1× RAW INPUT</text>
    </g>

    <!-- Right Zone: 4x On-Device Upscaled Vector Reconstruction -->
    <g transform="translate(172, 0)">
      <circle cx="88" cy="80" r="28" fill="none" stroke="{t["accent"]}" stroke-width="1.35"/>
      <circle cx="88" cy="80" r="19" fill="{t["accent_soft"]}" stroke="{t["accent"]}" stroke-width="1"/>
      <circle cx="88" cy="80" r="9" fill="none" stroke="{t["ink_soft"]}" stroke-width="1.1"/>
      <path d="M 48 94 Q 72 52 88 74 T 134 62" fill="none" stroke="{t["accent"]}" stroke-width="1.6" stroke-linecap="round"/>
      <circle cx="88" cy="80" r="2.6" fill="{t["amber"]}"/>
      <text x="48" y="118" font-family="{FONT_MONO}" font-size="8" letter-spacing="1" fill="{t["accent"]}">4× NCNN VULKAN / ONNX</text>
    </g>

    <!-- Animated Darkroom Split-Loupe Bar -->
    <g class="loupe">
      <line x1="138" y1="38" x2="138" y2="128" stroke="{t["accent"]}" stroke-width="1.6"/>
      <circle cx="138" cy="82" r="13" fill="{t["viewport"]}" fill-opacity="0.7" stroke="{t["accent"]}" stroke-width="1.5"/>
      <line x1="131" y1="82" x2="145" y2="82" stroke="{t["ruby"]}" stroke-width="1"/>
      <line x1="138" y1="75" x2="138" y2="89" stroke="{t["ruby"]}" stroke-width="1"/>
      <rect x="122" y="43" width="32" height="13" rx="3" fill="{t["accent"]}"/>
      <text x="138" y="52.5" text-anchor="middle" font-family="{FONT_MONO}" font-size="7.5" font-weight="700" fill="{t["bg"]}">LOUPE</text>
    </g>

    <!-- Right Spec Callout -->
    <text x="404" y="54" text-anchor="end" font-family="{FONT_MONO}" font-size="8" fill="{t["muted"]}">ZERO CLOUD</text>
    <text x="404" y="66" text-anchor="end" font-family="{FONT_MONO}" font-size="8" fill="{t["faint"]}">ARM64-V8A</text>
    """
    return card_shell(
        theme_name=theme_name,
        spec_code="SPEC.01",
        surface_tag="ANDROID · ON-DEVICE AI",
        title="Pixel-Forge",
        subtitle="DARKROOM 4×",
        desc_line1="Offline on-device AI super-resolution & face restoration",
        desc_line2="with a pinch-to-zoom darkroom loupe and zero uploads.",
        stack_line="KOTLIN · JETPACK COMPOSE · NCNN VULKAN · ONNX RUNTIME",
        extra_css=css,
        viewport_svg=vp,
        card_id="pixelforge",
    )


def build_card_sarmaya(theme_name: str) -> str:
    """SPEC.02: Sarmaya — Animated Event-Sourced PSX Portfolio Ledger."""
    t = THEMES[theme_name]
    css = """
    @keyframes curve-draw {
      0% { stroke-dashoffset: 380; }
      65%, 100% { stroke-dashoffset: 0; }
    }
    @keyframes scan-ledger {
      0%, 100% { transform: translateX(0px); }
      50% { transform: translateX(270px); }
    }
    .equity-line {
      stroke-dasharray: 380;
      animation: curve-draw 5s ease-out infinite;
    }
    .ledger-cursor {
      animation: scan-ledger 6.4s ease-in-out infinite;
    }
    """
    vp = f"""
    <!-- Area under PSX Equity Curve -->
    <path d="M 38 106 L 78 98 L 118 102 L 164 84 L 208 88 L 254 66 L 304 72 L 352 54 L 386 58 L 386 112 L 38 112 Z" fill="{t["accent_soft"]}"/>
    <!-- Animated Equity Curve -->
    <path d="M 38 106 L 78 98 L 118 102 L 164 84 L 208 88 L 254 66 L 304 72 L 352 54 L 386 58" fill="none" stroke="{t["accent"]}" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" class="equity-line"/>

    <!-- Event-Sourced Transaction Replay Markers -->
    <g font-family="{FONT_MONO}" font-size="7.5" text-anchor="middle">
      <circle cx="78" cy="98" r="3" fill="{t["accent"]}"/>
      <text x="78" y="122" fill="{t["muted"]}">BUY</text>

      <circle cx="164" cy="84" r="3" fill="{t["amber"]}"/>
      <text x="164" y="122" fill="{t["amber"]}">DIV</text>

      <circle cx="254" cy="66" r="3" fill="{t["accent"]}"/>
      <text x="254" y="122" fill="{t["muted"]}">BONUS</text>

      <circle cx="352" cy="54" r="3.4" fill="{t["accent"]}"/>
      <text x="352" y="122" fill="{t["accent"]}">P/L</text>
    </g>

    <!-- Sweeping Deterministic Replay Hairline -->
    <g class="ledger-cursor">
      <line x1="68" y1="42" x2="68" y2="112" stroke="{t["ink_soft"]}" stroke-width="0.9" stroke-dasharray="2 2" opacity="0.65"/>
      <circle cx="68" cy="46" r="2.2" fill="{t["amber"]}"/>
    </g>

    <!-- Corner Readout -->
    <text x="32" y="54" font-family="{FONT_MONO}" font-size="8" letter-spacing="1" fill="{t["accent"]}">PSX · EVENT-SOURCED</text>
    <text x="32" y="66" font-family="{FONT_MONO}" font-size="7.5" fill="{t["faint"]}">APPEND-ONLY SQLITE LEDGER</text>
    """
    return card_shell(
        theme_name=theme_name,
        spec_code="SPEC.02",
        surface_tag="ANDROID · FINTECH",
        title="Sarmaya",
        subtitle="PSX LEDGER",
        desc_line1="Offline-first Pakistan Stock Exchange portfolio tracker",
        desc_line2="with an event-sourced engine for exact holdings & P/L.",
        stack_line="KOTLIN · JETPACK COMPOSE · MATERIAL 3 · ROOM SQLITE",
        extra_css=css,
        viewport_svg=vp,
        card_id="sarmaya",
    )


def build_card_hayya(theme_name: str) -> str:
    """SPEC.03: Hayya — Animated Solar Azimuth Arc & Qibla Compass."""
    t = THEMES[theme_name]
    css = """
    @keyframes compass-sway {
      0%, 100% { transform: rotate(-18deg); }
      50% { transform: rotate(22deg); }
    }
    @keyframes sun-pulse {
      0%, 100% { r: 4.5px; opacity: 1; }
      50% { r: 6.2px; opacity: 0.75; }
    }
    .qibla-needle {
      transform-origin: 348px 84px;
      animation: compass-sway 5.2s ease-in-out infinite;
    }
    .solar-orb { animation: sun-pulse 3s ease-in-out infinite; }
    """
    vp = f"""
    <!-- Horizon Line -->
    <line x1="34" y1="106" x2="278" y2="106" stroke="{t["border_strong"]}" stroke-width="1"/>
    <!-- Parabolic Solar Arc (Jean Meeus Solver) -->
    <path d="M 46 106 Q 156 24 266 106" fill="none" stroke="{t["accent"]}" stroke-width="1.4" stroke-dasharray="4 3"/>
    <!-- Prayer Time Nodes along Solar Arc -->
    <circle cx="58" cy="96" r="2.2" fill="{t["muted"]}"/>
    <circle cx="104" cy="70" r="2.2" fill="{t["muted"]}"/>
    <circle cx="156" cy="59" r="2.5" fill="{t["amber"]}"/>
    <circle cx="208" cy="70" r="2.2" fill="{t["muted"]}"/>
    <circle cx="254" cy="96" r="2.2" fill="{t["muted"]}"/>

    <!-- Glowing Sun Animated along the Solar Path via SMIL -->
    <circle r="10" fill="{t["amber_soft"]}">
      <animateMotion dur="8s" repeatCount="indefinite" path="M 46,106 Q 156,24 266,106"/>
    </circle>
    <circle r="4.5" fill="{t["amber"]}" class="solar-orb">
      <animateMotion dur="8s" repeatCount="indefinite" path="M 46,106 Q 156,24 266,106"/>
    </circle>

    <text x="34" y="53" font-family="{FONT_MONO}" font-size="8" letter-spacing="1" fill="{t["accent"]}">DUAL SOLAR SOLVER</text>
    <text x="34" y="120" font-family="{FONT_MONO}" font-size="7.5" fill="{t["faint"]}">FAJR · DHUHR · ASR · MAGHRIB · ISHA</text>

    <!-- Mini Qibla Compass Rose on Right (cx=348, cy=84) -->
    <circle cx="348" cy="84" r="28" fill="{t["surface"]}" stroke="{t["border_strong"]}" stroke-width="1"/>
    <circle cx="348" cy="84" r="21" fill="none" stroke="{t["border"]}" stroke-width="0.7" stroke-dasharray="2 3"/>
    <text x="348" y="64" text-anchor="middle" font-family="{FONT_MONO}" font-size="7" fill="{t["faint"]}">N</text>
    <g class="qibla-needle">
      <polygon points="348,66 352,84 348,80 344,84" fill="{t["accent"]}"/>
      <polygon points="348,102 351,84 348,88 345,84" fill="{t["faint"]}"/>
      <circle cx="348" cy="84" r="2.2" fill="{t["ink"]}"/>
    </g>
    <text x="348" y="122" text-anchor="middle" font-family="{FONT_MONO}" font-size="7.5" fill="{t["muted"]}">QIBLA</text>
    """
    return card_shell(
        theme_name=theme_name,
        spec_code="SPEC.03",
        surface_tag="ANDROID · ZERO-TELEMETRY",
        title="Hayya",
        subtitle="100% OFFLINE",
        desc_line1="Zero-permission Islamic prayer reminder & companion",
        desc_line2="with Doze-resilient alarms, Glance widgets & Qibla.",
        stack_line="KOTLIN · JETPACK COMPOSE · GLANCE · JEAN MEEUS",
        extra_css=css,
        viewport_svg=vp,
        card_id="hayya",
    )


def build_card_nebula(theme_name: str) -> str:
    """SPEC.04: nebula-downloader — Animated Multi-Stream Extraction Conduit."""
    t = THEMES[theme_name]
    css = """
    @keyframes stream-dash {
      from { stroke-dashoffset: 64; }
      to { stroke-dashoffset: 0; }
    }
    @keyframes bar-fill-a {
      0% { width: 42px; }
      70% { width: 142px; }
      100% { width: 142px; }
    }
    @keyframes bar-fill-b {
      0% { width: 24px; }
      80% { width: 118px; }
      100% { width: 118px; }
    }
    .stream-flow {
      stroke-dasharray: 8 8;
      animation: stream-dash 1.8s linear infinite;
    }
    .qbar-a { animation: bar-fill-a 4.8s ease-in-out infinite; }
    .qbar-b { animation: bar-fill-b 5.6s ease-in-out infinite; }
    """
    vp = f"""
    <!-- Source Conduit -->
    <rect x="30" y="54" width="66" height="56" rx="6" fill="{t["surface"]}" stroke="{t["border_strong"]}" stroke-width="1"/>
    <text x="63" y="79" text-anchor="middle" font-family="{FONT_MONO}" font-size="9.5" font-weight="700" fill="{t["accent"]}">YT-DLP</text>
    <text x="63" y="93" text-anchor="middle" font-family="{FONT_MONO}" font-size="7.5" fill="{t["faint"]}">1000+ SITES</text>

    <!-- Animated Multi-Lane Pipeline Traces -->
    <path d="M 96 68 L 154 68" stroke="{t["accent"]}" stroke-width="1.4" class="stream-flow"/>
    <path d="M 96 82 L 154 82" stroke="{t["cyan"]}" stroke-width="1.4" class="stream-flow"/>
    <path d="M 96 96 L 154 96" stroke="{t["amber"]}" stroke-width="1.2" class="stream-flow"/>

    <!-- Concurrent Queue Monitor -->
    <rect x="158" y="48" width="244" height="70" rx="6" fill="{t["surface"]}" stroke="{t["border"]}" stroke-width="0.9"/>
    <text x="170" y="64" font-family="{FONT_MONO}" font-size="7.8" fill="{t["ink_soft"]}">8K VIDEO · MKV</text>
    <rect x="252" y="57" width="136" height="8" rx="3" fill="{t["viewport"]}" stroke="{t["border"]}" stroke-width="0.6"/>
    <rect x="252" y="57" width="112" height="8" rx="3" fill="{t["accent"]}" class="qbar-a"/>

    <text x="170" y="84" font-family="{FONT_MONO}" font-size="7.8" fill="{t["ink_soft"]}">AUDIO · WAV/M4A</text>
    <rect x="252" y="77" width="136" height="8" rx="3" fill="{t["viewport"]}" stroke="{t["border"]}" stroke-width="0.6"/>
    <rect x="252" y="77" width="88" height="8" rx="3" fill="{t["cyan"]}" class="qbar-b"/>

    <text x="170" y="104" font-family="{FONT_MONO}" font-size="7.8" fill="{t["muted"]}">SQLITE INDEX · RESUME READY</text>
    <circle cx="384" cy="101" r="3" fill="{t["accent"]}" class="cled"/>
    """
    return card_shell(
        theme_name=theme_name,
        spec_code="SPEC.04",
        surface_tag="DESKTOP · ELECTRON",
        title="nebula-downloader",
        subtitle="UP TO 8K",
        desc_line1="Cross-platform desktop video & audio downloader",
        desc_line2="with concurrent queues, clipboard watch & SQLite index.",
        stack_line="ELECTRON · REACT 19 · TYPESCRIPT · TAILWIND · YT-DLP",
        extra_css=css,
        viewport_svg=vp,
        card_id="nebula",
    )


def build_card_ergo(theme_name: str) -> str:
    """SPEC.05: Ergo — Animated Flutter Quiz Mastery Heatmap & Accuracy Gauge."""
    t = THEMES[theme_name]
    # 13 cols x 4 rows clean mastery heatmap
    levels = [
        [1, 2, 3, 2, 0, 1, 3, 4, 3, 2, 1, 3, 4],
        [0, 1, 2, 4, 3, 2, 1, 3, 4, 4, 2, 2, 3],
        [2, 3, 1, 2, 4, 3, 2, 1, 2, 3, 4, 3, 4],
        [1, 0, 2, 3, 2, 4, 3, 2, 1, 4, 3, 4, 4],
    ]
    op_map = {0: 0.10, 1: 0.25, 2: 0.48, 3: 0.72, 4: 0.96}
    cells = []
    for r_idx, row in enumerate(levels):
        for c_idx, lv in enumerate(row):
            x = 34 + c_idx * 17
            y = 54 + r_idx * 15
            cls = "hm-hi" if lv == 4 else ("hm-mid" if lv == 3 else "")
            cells.append(
                f'<rect x="{x}" y="{y}" width="12" height="11" rx="2.5" fill="{t["accent"]}" opacity="{op_map[lv]}" class="{cls}"/>'
            )
    cells_svg = "\n      ".join(cells)

    css = """
    @keyframes cell-breathe {
      0%, 100% { opacity: 0.95; }
      50% { opacity: 0.45; }
    }
    @keyframes gauge-sweep {
      0% { stroke-dashoffset: 138; }
      60%, 100% { stroke-dashoffset: 18; }
    }
    .hm-hi { animation: cell-breathe 3.4s ease-in-out infinite; }
    .hm-mid { animation: cell-breathe 4.4s ease-in-out 1.1s infinite; }
    .ergo-arc {
      stroke-dasharray: 138;
      animation: gauge-sweep 5.2s ease-out infinite;
    }
    """
    vp = f"""
    <!-- Left: Activity & Streak Heatmap Matrix -->
    <text x="34" y="49" font-family="{FONT_MONO}" font-size="7.5" letter-spacing="1" fill="{t["muted"]}">STREAK HEATMAP · OFFLINE PACKS</text>
    <g>
      {cells_svg}
    </g>

    <!-- Right: Circular Mastery Gauge (cx=344, cy=84, r=24) -->
    <circle cx="344" cy="84" r="24" fill="none" stroke="{t["border_strong"]}" stroke-width="4"/>
    <circle cx="344" cy="84" r="24" fill="none" stroke="{t["accent"]}" stroke-width="4" stroke-linecap="round" transform="rotate(-90 344 84)" class="ergo-arc"/>
    <text x="344" y="87" text-anchor="middle" font-family="{FONT_MONO}" font-size="11" font-weight="700" fill="{t["ink"]}">M3</text>
    <text x="344" y="120" text-anchor="middle" font-family="{FONT_MONO}" font-size="7.5" fill="{t["faint"]}">ANALYTICS</text>
    """
    return card_shell(
        theme_name=theme_name,
        spec_code="SPEC.05",
        surface_tag="MOBILE · FLUTTER",
        title="Ergo",
        subtitle="DLC ENGINE",
        desc_line1="Fully offline Flutter quiz engine powered by modular",
        desc_line2="external question packs, streaks & heatmap analytics.",
        stack_line="DART · FLUTTER · RIVERPOD · SQLITE · MATERIAL 3",
        extra_css=css,
        viewport_svg=vp,
        card_id="ergo",
    )


def build_card_jot(theme_name: str) -> str:
    """SPEC.06: jot (JOTUN) — Animated Rust FTS5 Terminal Search Beam."""
    t = THEMES[theme_name]
    css = """
    @keyframes cursor-blink {
      0%, 49% { opacity: 1; }
      50%, 100% { opacity: 0; }
    }
    @keyframes beam-scan {
      0%, 100% { transform: translateY(0px); }
      50% { transform: translateY(28px); }
    }
    .t-cursor { animation: cursor-blink 1.1s step-end infinite; }
    .fts-beam { animation: beam-scan 4.2s ease-in-out infinite; }
    """
    vp = f"""
    <!-- Miniature 3-Pane TUI Frame -->
    <rect x="30" y="47" width="376" height="72" rx="5" fill="{t["surface"]}" stroke="{t["border_strong"]}" stroke-width="0.9"/>
    <!-- Vertical Pane Dividers -->
    <line x1="128" y1="47" x2="128" y2="119" stroke="{t["border"]}" stroke-width="0.85"/>
    <line x1="274" y1="47" x2="274" y2="119" stroke="{t["border"]}" stroke-width="0.85"/>

    <!-- Pane 1: Nested Tags -->
    <text x="40" y="61" font-family="{FONT_MONO}" font-size="7.5" font-weight="700" fill="{t["accent"]}"># TAGS</text>
    <text x="40" y="75" font-family="{FONT_MONO}" font-size="7.5" fill="{t["ink_soft"]}">▸ sys/rust</text>
    <text x="40" y="89" font-family="{FONT_MONO}" font-size="7.5" fill="{t["muted"]}">  arch/local</text>
    <text x="40" y="103" font-family="{FONT_MONO}" font-size="7.5" fill="{t["muted"]}">  db/fts5</text>

    <!-- Pane 2: Animated FTS5 Index Scan -->
    <text x="138" y="61" font-family="{FONT_MONO}" font-size="7.5" font-weight="700" fill="{t["amber"]}">/ FTS5 INDEX</text>
    <rect x="134" y="67" width="134" height="14" rx="2.5" fill="{t["accent_soft"]}" stroke="{t["accent"]}" stroke-width="0.7" class="fts-beam"/>
    <text x="140" y="77" font-family="{FONT_MONO}" font-size="7.5" fill="{t["ink"]}">01 · event-store.md</text>
    <text x="140" y="92" font-family="{FONT_MONO}" font-size="7.5" fill="{t["muted"]}">02 · solar-math.md</text>
    <text x="140" y="107" font-family="{FONT_MONO}" font-size="7.5" fill="{t["muted"]}">03 · zero-deps.md</text>

    <!-- Pane 3: Command Prompt + Telemetry -->
    <text x="284" y="61" font-family="{FONT_MONO}" font-size="7.5" font-weight="700" fill="{t["muted"]}">$ JOTUN</text>
    <text x="284" y="77" font-family="{FONT_MONO}" font-size="8" fill="{t["accent"]}">&gt; jot new</text>
    <rect x="334" y="70" width="5.5" height="9" fill="{t["accent"]}" class="t-cursor"/>
    <text x="284" y="96" font-family="{FONT_MONO}" font-size="7.5" fill="{t["faint"]}">RAM  &lt; 10 MB</text>
    <text x="284" y="109" font-family="{FONT_MONO}" font-size="7.5" fill="{t["faint"]}">DEPS   ZERO</text>
    """
    return card_shell(
        theme_name=theme_name,
        spec_code="SPEC.06",
        surface_tag="SHELL · PURE RUST",
        title="jot",
        subtitle="JOTUN TUI",
        desc_line1="Zero-dependency, local-first shell knowledge base",
        desc_line2="in pure Rust with SQLite FTS5 & 3-pane TUI under 10 MB.",
        stack_line="RUST · SQLITE FTS5 · ZERO DEPS · CRATES.IO",
        extra_css=css,
        viewport_svg=vp,
        card_id="jot",
    )


def build_channel_keycap(
    theme_name: str,
    ch_code: str,
    label: str,
    value: str,
    icon_svg: str,
) -> str:
    """Clickable tactile hardware channel switch (286x82)."""
    t = THEMES[theme_name]
    w, h = 286, 82
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{escape(label)}: {escape(value)}">
  <style>
    @keyframes ch-led {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0.35; }}
    }}
    .chled {{ animation: ch-led 3s ease-in-out infinite; }}
    @media (prefers-reduced-motion: reduce) {{ .chled {{ animation: none !important; }} }}
  </style>
  <rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" rx="10" fill="{t["surface"]}" stroke="{t["border"]}" stroke-width="1.15"/>
  <line x1="12" y1="1.5" x2="{w - 12}" y2="1.5" stroke="{t["bevel"]}" stroke-width="1"/>
  <!-- Left Icon Housing -->
  <rect x="14" y="16" width="48" height="50" rx="8" fill="{t["viewport"]}" stroke="{t["border_strong"]}" stroke-width="0.9"/>
  <g stroke="{t["accent"]}" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
    {icon_svg}
  </g>
  <!-- Metadata -->
  <circle cx="76" cy="28" r="2.5" fill="{t["accent"]}" class="chled"/>
  <text x="85" y="31" font-family="{FONT_MONO}" font-size="8.5" font-weight="700" letter-spacing="1.4" fill="{t["muted"]}">{escape(ch_code)} // {escape(label.upper())}</text>
  <text x="74" y="54" font-family="{FONT_MONO}" font-size="11.5" font-weight="600" fill="{t["ink"]}">{escape(value)}</text>
  <text x="{w - 16}" y="31" text-anchor="end" font-family="{FONT_MONO}" font-size="11" fill="{t["accent"]}">↗</text>
</svg>
'''


def build_colophon(theme_name: str) -> str:
    """Closing kinetic vernier calibration ruler footer (900x58)."""
    t = THEMES[theme_name]
    w, h = 900, 58
    ticks = []
    for x in range(20, w - 16, 8):
        is_major = (x - 20) % 40 == 0
        y1 = 8 if is_major else 12
        col = t["border_strong"] if is_major else t["border"]
        ticks.append(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="18" stroke="{col}" stroke-width="0.9"/>')
    ticks_svg = "\n    ".join(ticks)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Aatif — Built with restraint. Engineered to endure.">
  <style>
    @keyframes vernier-sweep {{
      0%, 100% {{ transform: translateX(0px); }}
      50% {{ transform: translateX(836px); }}
    }}
    .v-cursor {{ animation: vernier-sweep 11s ease-in-out infinite; }}
    @media (prefers-reduced-motion: reduce) {{ .v-cursor {{ animation: none !important; }} }}
  </style>
  <rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" rx="10" fill="{t["surface"]}" stroke="{t["border"]}" stroke-width="1"/>
  <line x1="20" y1="18" x2="{w - 20}" y2="18" stroke="{t["border"]}" stroke-width="0.9"/>
  <g>
    {ticks_svg}
  </g>
  <!-- Gliding Optical Calibration Cursor -->
  <g class="v-cursor">
    <line x1="32" y1="5" x2="32" y2="23" stroke="{t["accent"]}" stroke-width="1.8"/>
    <polygon points="32,23 28.5,27 35.5,27" fill="{t["accent"]}"/>
  </g>
  <text x="{w / 2:.0f}" y="42" text-anchor="middle" font-family="{FONT_MONO}" font-size="9.5" letter-spacing="2" fill="{t["muted"]}">AATIF  ·  DEV-AATIF  ·  BUILT WITH RESTRAINT. ENGINEERED TO ENDURE.</text>
</svg>
'''


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    CARDS_DIR.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []

    def save(path: Path, content: str) -> None:
        path.write_text(content, encoding="utf-8")
        written.append(path)

    for theme in ("dark", "light"):
        save(ASSETS / f"hero-{theme}.svg", build_hero(theme))
        save(
            ASSETS / f"divider-01-{theme}.svg",
            build_divider(theme, "01", "CAPABILITY PATCHBAY", "04 CHANNELS · 18 INSTRUMENTS"),
        )
        save(ASSETS / f"patchbay-{theme}.svg", build_patchbay(theme))
        save(
            ASSETS / f"divider-02-{theme}.svg",
            build_divider(theme, "02", "PINNED EXHIBITION", "06 BUILDS · CLICK ANY SPECIMEN"),
        )
        save(CARDS_DIR / f"pixel-forge-{theme}.svg", build_card_pixel_forge(theme))
        save(CARDS_DIR / f"sarmaya-{theme}.svg", build_card_sarmaya(theme))
        save(CARDS_DIR / f"hayya-{theme}.svg", build_card_hayya(theme))
        save(CARDS_DIR / f"nebula-{theme}.svg", build_card_nebula(theme))
        save(CARDS_DIR / f"ergo-{theme}.svg", build_card_ergo(theme))
        save(CARDS_DIR / f"jot-{theme}.svg", build_card_jot(theme))
        save(
            ASSETS / f"divider-03-{theme}.svg",
            build_divider(theme, "03", "SIGNAL DISPATCH", "DIRECT CHANNELS"),
        )
        # Clickable Channel Keycaps
        email_icon = '<rect x="27" y="32" width="22" height="16" rx="2"/><path d="M 28 34 L 38 41 L 48 34"/>'
        linkedin_icon = f'<rect x="28" y="30" width="20" height="20" rx="3"/><line x1="33" y1="38" x2="33" y2="45"/><circle cx="33" cy="34.5" r="0.9" fill="{THEMES[theme]["accent"]}" stroke="none"/><path d="M 38 45 L 38 38 M 38 40 C 38 38, 43 38, 43 41 L 43 45"/>'
        portfolio_icon = '<circle cx="38" cy="41" r="10"/><ellipse cx="38" cy="41" rx="4.5" ry="10"/><line x1="28" y1="41" x2="48" y2="41"/>'

        save(
            ASSETS / f"channel-email-{theme}.svg",
            build_channel_keycap(theme, "CH.A", "Email", "Aatif.biz@protonmail.com", email_icon),
        )
        save(
            ASSETS / f"channel-linkedin-{theme}.svg",
            build_channel_keycap(theme, "CH.B", "LinkedIn", "linkedin.com/in/dev-aatif", linkedin_icon),
        )
        save(
            ASSETS / f"channel-portfolio-{theme}.svg",
            build_channel_keycap(theme, "CH.C", "Portfolio", "dev-aatif.vercel.app", portfolio_icon),
        )
        save(ASSETS / f"colophon-{theme}.svg", build_colophon(theme))

    print(f"Synthesized {len(written)} SVG plates cleanly into {ASSETS}")


if __name__ == "__main__":
    main()
