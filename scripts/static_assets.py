"""Renderers for the Cyberpunk / Sci-Fi HUD static SVG assets."""
import math
import random

from cyber import (
    CYAN, CYAN_DIM, CYAN_GLOW, MAGENTA, PURPLE, NEON_GREEN, AMBER,
    DARK_BG, PANEL_BG, PANEL_BORDER, TEXT_MAIN, TEXT_MUTED,
    cyber_svg, cyber_panel, scanline, equalizer, reticle, badge
)
from medieval import txt, width, fit, wrap, para, esc, icon, ICONS


# ------------------------------------------------------------------ header
def header():
    W, H = 1200, 480
    b = [
        # Dark Cyber Void background
        f'<rect width="{W}" height="{H}" fill="url(#cyberSky)"/>',
        
        # Cyber grid in background
        f'<rect width="{W}" height="{H}" fill="url(#cyberGrid)" opacity=".8"/>',
        
        # Horizon neon glow
        f'<ellipse cx="600" cy="{H * 0.72:.0f}" rx="560" ry="160" fill="url(#scanBeam)" opacity=".25"/>',
        
        # Perspective wireframe lines (vanishing to center)
        f'<g stroke="{CYAN}" stroke-width=".8" stroke-opacity=".15">'
        f'<line x1="600" y1="260" x2="0" y2="480"/>'
        f'<line x1="600" y1="260" x2="200" y2="480"/>'
        f'<line x1="600" y1="260" x2="400" y2="480"/>'
        f'<line x1="600" y1="260" x2="800" y2="480"/>'
        f'<line x1="600" y1="260" x2="1000" y2="480"/>'
        f'<line x1="600" y1="260" x2="1200" y2="480"/>'
        f'</g>',
        
        # Horizontal perspective grid rungs
        f'<g stroke="{CYAN}" stroke-width=".8" stroke-opacity=".2">'
        f'<line x1="300" y1="310" x2="900" y2="310"/>'
        f'<line x1="220" y1="350" x2="980" y2="350"/>'
        f'<line x1="120" y1="400" x2="1080" y2="400"/>'
        f'<line x1="0" y1="460" x2="1200" y2="460"/>'
        f'</g>',

        # Corner HUD brackets
        f'<path d="M 30,70 L 30,30 L 70,30" fill="none" stroke="{CYAN}" stroke-width="2.5"/>',
        f'<path d="M 1170,70 L 1170,30 L 1130,30" fill="none" stroke="{CYAN}" stroke-width="2.5"/>',
        f'<path d="M 30,410 L 30,450 L 70,450" fill="none" stroke="{MAGENTA}" stroke-width="2.5"/>',
        f'<path d="M 1170,410 L 1170,450 L 1130,450" fill="none" stroke="{MAGENTA}" stroke-width="2.5"/>',

        # HUD Reticles
        reticle(105, 120, 36, CYAN),
        reticle(1095, 120, 36, MAGENTA),

        # Audio Equalizers
        equalizer(75, 410, bars=10, bw=4, maxh=28, col=CYAN),
        equalizer(1075, 410, bars=10, bw=4, maxh=28, col=MAGENTA),

        # Top System Bar
        f'<rect x="250" y="32" width="700" height="26" fill="#060c1c" stroke="{PANEL_BORDER}" stroke-width="1"/>',
        f'<text x="270" y="49" fill="{CYAN}" font-family="monospace" font-size="11" font-weight="bold" letter-spacing="2">[ SYSTEM: OPERATIONAL ]</text>',
        f'<text x="600" y="49" fill="{AMBER}" font-family="monospace" font-size="11" font-weight="bold" text-anchor="middle" letter-spacing="2">[ CYBER_PROTOCOL: v2026.4 ]</text>',
        f'<text x="930" y="49" fill="{NEON_GREEN}" font-family="monospace" font-size="11" font-weight="bold" text-anchor="end" letter-spacing="2">[ LATENCY: 0.4ms ]</text>',

        # Animated Laser Scanline
        scanline(1200, 480, dur=6.0),

        # Central HUD Panel for Name
        f'<rect x="180" y="100" width="840" height="250" fill="#060b18" fill-opacity=".82" stroke="{CYAN}" stroke-width="1.2" stroke-opacity=".4"/>',
        f'<rect x="184" y="104" width="832" height="242" fill="none" stroke="{MAGENTA}" stroke-width=".8" stroke-opacity=".25" stroke-dasharray="8 6"/>',
        
        # Sub-heading banner
        f'<text x="600" y="146" fill="{CYAN}" font-family="monospace" font-size="13" font-weight="bold" text-anchor="middle" letter-spacing="5">// TACTICAL OPERATIVE DOSSIER //</text>',
    ]

    # Name: TANISHQ SHAH
    name = "TANISHQ SHAH"
    size = fit("deco", name, 76, 760, 6)
    b.append(
        f'<g filter="url(#laserBlur)" opacity=".7">'
        + txt("deco", name, size, 600, 230, CYAN, "middle", 6)
        + '</g>'
    )
    b.append(
        f'<g>'
        f'<animate attributeName="opacity" values="1;.85;1" dur="4s" repeatCount="indefinite"/>'
        + txt("deco", name, size, 600, 230, "#ffffff", "middle", 6)
        + '</g>'
    )

    # Subtitle and Callings
    sub = "SYSTEMS ARCHITECT  ·  C++20 LOW-LEVEL  ·  FULL-STACK OPERATOR"
    sub_size = fit("cin", sub, 17, 780, 3)
    b.append(
        f'<text x="600" y="278" fill="{CYAN_GLOW}" font-family="monospace" font-size="13.5" font-weight="bold" text-anchor="middle" letter-spacing="2">'
        f'{sub}'
        f'</text>'
    )

    # University / Cadre
    b.append(
        f'<text x="600" y="316" fill="{TEXT_MUTED}" font-family="monospace" font-size="12" text-anchor="middle" letter-spacing="2">'
        f'DA-IICT (DHIRUBHAI AMBANI UNIVERSITY)  ·  B.TECH ICT'
        f'</text>'
    )

    # Lower laser border
    b.append(f'<rect y="{H - 3}" width="{W}" height="3" fill="url(#cyberLaser)"/>')
    return cyber_svg(W, H, "".join(b), "", "Tanishq Shah — Cyberpunk Sci-Fi HUD Terminal")


# ----------------------------------------------------- rotating titles ticker
def titles():
    W, H = 900, 72
    items = [
        "// [01] LOW-LEVEL C++20 SYSTEMS ARCHITECT",
        "// [02] FULL-STACK FINTECH & SENSORY OPERATOR",
        "// [03] HIGH-CONCURRENCY DATABASE ENGINE FORGER",
        "// [04] ALGORITHM & COMPETITIVE SPECIALIST"
    ]
    b = [
        cyber_panel(W, H, ch=12, stroke=CYAN, fill="#070c1a", stroke_w=1.2),
        reticle(44, 36, 18, CYAN),
        reticle(856, 36, 18, MAGENTA),
        f'<line x1="80" y1="36" x2="160" y2="36" stroke="{CYAN}" stroke-width="1.2" stroke-opacity=".5"/>',
        f'<line x1="740" y1="36" x2="820" y2="36" stroke="{MAGENTA}" stroke-width="1.2" stroke-opacity=".5"/>',
    ]

    for i, t in enumerate(items):
        b.append(
            f'<g opacity="{1 if i == 0 else 0}">'
            f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;.06;.22;.28;1" '
            f'dur="12s" begin="{3 * i}s" repeatCount="indefinite"/>'
            f'<animateTransform attributeName="transform" type="translate" values="0 8;0 0;0 0;0 -8;0 -8" '
            f'keyTimes="0;.06;.22;.28;1" dur="12s" begin="{3 * i}s" repeatCount="indefinite"/>'
            f'<text x="450" y="43" fill="{CYAN}" font-family="monospace" font-size="16" font-weight="bold" text-anchor="middle" letter-spacing="2.5">{t}</text>'
            f'</g>'
        )

    return cyber_svg(W, H, "".join(b), "", "Active Cyber Directives")


# --------------------------------------------------- section header
def section_header(title, sub):
    W, H = 900, 96
    size = fit("deco", title, 32, 540, 3)
    b = [
        cyber_panel(W, H, ch=14, stroke=CYAN, fill="#070d1e", stroke_w=1.2),
        reticle(46, 48, 22, CYAN),
        reticle(854, 48, 22, MAGENTA),
        f'<line x1="84" y1="48" x2="220" y2="48" stroke="url(#neonCyan)" stroke-width="1.5" stroke-opacity=".7"/>',
        f'<line x1="680" y1="48" x2="816" y2="48" stroke="url(#neonMagenta)" stroke-width="1.5" stroke-opacity=".7"/>',
        txt("deco", title, size, 450, 52, CYAN, "middle", 3),
        f'<text x="450" y="78" fill="{TEXT_MUTED}" font-family="monospace" font-size="11.5" text-anchor="middle" letter-spacing="3">// {sub.upper()} //</text>',
    ]
    return cyber_svg(W, H, "".join(b), "", title)


def divider():
    W, H = 900, 48
    b = [
        f'<rect x="60" y="23" width="780" height="2" fill="url(#cyberLaser)"/>',
        f'<circle cx="450" cy="24" r="16" fill="{CYAN}" opacity=".15"><animate attributeName="r" values="10;22;10" dur="2.5s" repeatCount="indefinite"/></circle>',
        reticle(450, 24, 14, CYAN),
        f'<polygon points="446,20 454,20 450,28" fill="{MAGENTA}"/>',
        f'<rect x="200" y="21" width="6" height="6" fill="{CYAN}"/>',
        f'<rect x="700" y="21" width="6" height="6" fill="{MAGENTA}"/>',
    ]
    return cyber_svg(W, H, "".join(b), "", "Cyber Laser Divider")


# ------------------------------------------------------------ operative dossier (about)
def about():
    W, H = 900, 410
    b = [
        cyber_panel(W, H, ch=18, stroke=CYAN, fill="url(#cyberCardBg)", stroke_w=1.4),
        scanline(W, H, dur=5.5),
        
        # Header banner inside panel
        f'<rect x="30" y="24" width="840" height="34" fill="#0a1428" stroke="{PANEL_BORDER}" stroke-width="1"/>',
        f'<text x="48" y="46" fill="{CYAN}" font-family="monospace" font-size="12" font-weight="bold" letter-spacing="2">OPERATIVE PROTOCOL // TANISHQ SHAH [TS-7361]</text>',
        f'<text x="852" y="46" fill="{NEON_GREEN}" font-family="monospace" font-size="11" font-weight="bold" text-anchor="end" letter-spacing="1">STATUS: DEPLOYMENT READY</text>',

        # Left Column: Radar Scanner & Tactical HUD Display
        f'<rect x="30" y="72" width="220" height="308" fill="#070f20" stroke="{PANEL_BORDER}" stroke-width="1"/>',
        reticle(140, 180, 68, CYAN),
        
        # Radar rotating sweep line
        f'<g transform="translate(140 180)">'
        f'<line x1="0" y1="0" x2="68" y2="0" stroke="{CYAN}" stroke-width="2">'
        f'<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="4s" repeatCount="indefinite"/>'
        f'</line>'
        # Target blips
        f'<circle cx="28" cy="-32" r="3.5" fill="{NEON_GREEN}"><animate attributeName="opacity" values=".1;1;.1" dur="2s" repeatCount="indefinite"/></circle>'
        f'<circle cx="-42" cy="18" r="3" fill="{MAGENTA}"><animate attributeName="opacity" values="1;.2;1" dur="3s" repeatCount="indefinite"/></circle>'
        f'<circle cx="16" cy="46" r="3" fill="{AMBER}"><animate attributeName="opacity" values=".2;1;.2" dur="1.5s" repeatCount="indefinite"/></circle>'
        f'</g>',

        f'<text x="140" y="280" fill="{CYAN}" font-family="monospace" font-size="11" font-weight="bold" text-anchor="middle" letter-spacing="1.5">RADAR: ACTIVE SCAN</text>',
        f'<text x="140" y="302" fill="{TEXT_MUTED}" font-family="monospace" font-size="10" text-anchor="middle">RANGE: UNLIMITED</text>',
        equalizer(95, 350, bars=9, bw=7, maxh=24, gap=3, col=CYAN),

        # Right Column: Operative Specs Table
        f'<rect x="264" y="72" width="606" height="308" fill="#070e1d" stroke="{PANEL_BORDER}" stroke-width="1"/>',
    ]

    rows = [
        ("CODENAME", "Tanishq Shah"),
        ("AFFILIATION", "B.Tech ICT · DA-IICT (Dhirubhai Ambani University)"),
        ("PRIMARY WEAPON", "C++20 (Low-Level Systems, Multithreading, DSA)"),
        ("SYSTEMS STACK", "Spring Boot · React · PostgreSQL · Python · FastAPI"),
        ("CORE MISSIONS", "EquiSplit, Vaayu & CacheCore In-Memory DB"),
        ("CURRENT DIRECTIVE", "Seeking Software Engineering Internships & Placements"),
    ]

    y = 104
    for lab, val in rows:
        b.append(
            f'<text x="286" y="{y}" fill="{CYAN}" font-family="monospace" font-size="11" font-weight="bold" letter-spacing="1.5">{lab}</text>'
            f'<text x="430" y="{y}" fill="{TEXT_MAIN}" font-family="monospace" font-size="12">{val}</text>'
            f'<line x1="286" y1="{y + 10}" x2="846" y2="{y + 10}" stroke="{PANEL_BORDER}" stroke-width="1"/>'
        )
        y += 33

    # Telemetry skill bars at the bottom
    b.append(f'<text x="286" y="{y + 10}" fill="{TEXT_MUTED}" font-family="monospace" font-size="10.5" letter-spacing="1.5">COMBAT PROFICIENCY TELEMETRY:</text>')
    
    # Bar 1: Algorithms & C++20
    b.append(
        f'<text x="286" y="{y + 32}" fill="{CYAN}" font-family="monospace" font-size="10">ALGORITHMS &amp; C++20</text>'
        f'<rect x="430" y="{y + 22}" width="360" height="12" fill="#0a152e" stroke="{PANEL_BORDER}"/>'
        f'<rect x="430" y="{y + 22}" width="342" height="12" fill="url(#neonCyan)"/>'
        f'<text x="800" y="{y + 32}" fill="{CYAN}" font-family="monospace" font-size="10" font-weight="bold">95%</text>'
    )
    # Bar 2: Full-Stack Architecture
    b.append(
        f'<text x="286" y="{y + 54}" fill="{MAGENTA}" font-family="monospace" font-size="10">FULL-STACK SYSTEMS</text>'
        f'<rect x="430" y="{y + 44}" width="360" height="12" fill="#0a152e" stroke="{PANEL_BORDER}"/>'
        f'<rect x="430" y="{y + 44}" width="324" height="12" fill="url(#neonMagenta)"/>'
        f'<text x="800" y="{y + 54}" fill="{MAGENTA}" font-family="monospace" font-size="10" font-weight="bold">90%</text>'
    )
    # Bar 3: Database & Concurrency
    b.append(
        f'<text x="286" y="{y + 76}" fill="{NEON_GREEN}" font-family="monospace" font-size="10">CONCURRENCY &amp; DB</text>'
        f'<rect x="430" y="{y + 66}" width="360" height="12" fill="#0a152e" stroke="{PANEL_BORDER}"/>'
        f'<rect x="430" y="{y + 66}" width="316" height="12" fill="{NEON_GREEN}"/>'
        f'<text x="800" y="{y + 76}" fill="{NEON_GREEN}" font-family="monospace" font-size="10" font-weight="bold">88%</text>'
    )

    return cyber_svg(W, H, "".join(b), "", "Operative Dossier: Tanishq Shah")


# ------------------------------------------------------------------ armory
def arsenal():
    W, H = 900, 420
    b = [
        cyber_panel(W, H, ch=16, stroke=CYAN, fill="url(#cyberCardBg)", stroke_w=1.2),
        scanline(W, H, dur=6.0),
    ]

    modules = [
        ("01 // CORE ENGINES & LANGUAGES", CYAN, [
            ("C++20", "cplusplus", "Specialist · Concurrency & Low-Latency"),
            ("Java", "java", "Enterprise · Spring Boot Backend"),
            ("Python", "python", "Scientific, Fast-Prototyping & AI"),
            ("SQL", "mysql", "Relational Schemas, BCNF & Query Tuning"),
            ("TypeScript", "typescript", "Strongly-Typed Interactive Frontends")
        ]),
        ("02 // FRAMEWORKS & SYSTEM ARCHITECTURE", MAGENTA, [
            ("Spring Boot", "spring", "Robust REST Microservices & Security"),
            ("React.js", "react", "Component-Driven Reactive Web Interfaces"),
            ("PostgreSQL", "postgresql", "ACID Compliance, Indexing & Relations"),
            ("FastAPI", "fastapi", "Asynchronous High-Throughput Python APIs"),
            ("Node.js", "nodedotjs", "Async Event Loops & Runtime Tooling")
        ]),
        ("03 // CYBER FORGES & PROTOCOLS", NEON_GREEN, [
            ("Git / GitHub", "git", "Version Control, Branching & CI/CD Actions"),
            ("Linux / POSIX", "linux", "Shell Scripting, Process & Memory Mgmt"),
            ("Concurrency", "cplusplus", "Reader-Writer Locks, Atomic Ops & Threads"),
            ("REST APIs", "fastapi", "Contract Design, JWT Auth & Scalability")
        ]),
    ]

    y = 26
    for title, col, items in modules:
        b.append(
            f'<rect x="24" y="{y}" width="852" height="28" fill="#091326" stroke="{col}" stroke-width="1" stroke-opacity=".7"/>'
            f'<text x="40" y="{y + 19}" fill="{col}" font-family="monospace" font-size="12" font-weight="bold" letter-spacing="2">{title}</text>'
        )
        y += 36

        # Badges row
        bx = 24
        bw = (852 - (len(items) - 1) * 10) // len(items)
        for name, ic, desc in items:
            b.append(
                f'<g transform="translate({bx} {y})">'
                f'<rect width="{bw}" height="68" fill="#060c18" stroke="{PANEL_BORDER}" stroke-width="1"/>'
                f'<line x1="0" y1="0" x2="{bw}" y2="0" stroke="{col}" stroke-width="2" stroke-opacity=".8"/>'
                f'<text x="{bw/2}" y="24" fill="{TEXT_MAIN}" font-family="monospace" font-size="12" font-weight="bold" text-anchor="middle">{name}</text>'
                f'<text x="{bw/2}" y="44" fill="{TEXT_MUTED}" font-family="monospace" font-size="9.5" text-anchor="middle">{desc.split("·")[0]}</text>'
                f'<text x="{bw/2}" y="57" fill="{col}" font-family="monospace" font-size="8.5" text-anchor="middle" letter-spacing="1">[ READY ]</text>'
                f'</g>'
            )
            bx += bw + 10
        y += 84

    return cyber_svg(W, H, "".join(b), "", "Cyber Arsenal & Tech Weapons")


# ------------------------------------------------------------ project cards
def quest_equisplit():
    W, H = 900, 250
    b = [
        cyber_panel(W, H, ch=16, stroke=CYAN, fill="url(#cyberCardBg)", stroke_w=1.4),
        scanline(W, H, dur=4.5),
        reticle(76, 76, 36, CYAN),
        # Title chip
        f'<rect x="136" y="24" width="736" height="32" fill="#091428" stroke="{CYAN}" stroke-width="1" stroke-opacity=".8"/>',
        f'<text x="152" y="45" fill="{CYAN}" font-family="monospace" font-size="14" font-weight="bold" letter-spacing="2">PROJECT // EQUISPLIT [FINTECH LEDGER ENGINE]</text>',
        f'<text x="856" y="45" fill="{NEON_GREEN}" font-family="monospace" font-size="11" font-weight="bold" text-anchor="end">[ STATUS: DEPLOYED ]</text>',
        
        # Subtitle
        f'<text x="136" y="80" fill="{AMBER}" font-family="monospace" font-size="12" font-weight="bold" letter-spacing="1">FULL-STACK EXPENSE SHARING &amp; DEBT SIMPLIFICATION PLATFORM</text>',
        
        # Description
        f'<text x="136" y="108" fill="{TEXT_MAIN}" font-family="monospace" font-size="11.5">Intelligent expense settlement platform built with Spring Boot, React, and PostgreSQL.</text>',
        f'<text x="136" y="128" fill="{TEXT_MUTED}" font-family="monospace" font-size="11">Automates multi-user split debt simplification, real-time transaction tracking, and analytics.</text>',
        f'<text x="136" y="148" fill="{TEXT_MUTED}" font-family="monospace" font-size="11">Secured via JWT authentication, stateful sessions, and robust relational normalization.</text>',

        # Tech stack pills
        badge(136, 174, "SPRING BOOT", CYAN),
        badge(260, 174, "REACT.JS", CYAN),
        badge(364, 174, "POSTGRESQL", MAGENTA),
        badge(488, 174, "JWT SECURITY", AMBER),
        badge(618, 174, "ANALYTICS", NEON_GREEN),

        # Telemetry footer
        f'<line x1="136" y1="216" x2="872" y2="216" stroke="{PANEL_BORDER}" stroke-width="1"/>',
        f'<text x="136" y="233" fill="{TEXT_MUTED}" font-family="monospace" font-size="10" letter-spacing="1">REPO: github.com/Tanishq7361/EquiSplit // ACCESS PROTOCOL READY</text>',
    ]
    return cyber_svg(W, H, "".join(b), "", "EquiSplit Cyber Deck")


def quest_vaayu():
    W, H = 900, 250
    b = [
        cyber_panel(W, H, ch=16, stroke=NEON_GREEN, fill="url(#cyberCardBg)", stroke_w=1.4),
        scanline(W, H, dur=4.8),
        reticle(76, 76, 36, NEON_GREEN),
        # Title chip
        f'<rect x="136" y="24" width="736" height="32" fill="#081820" stroke="{NEON_GREEN}" stroke-width="1" stroke-opacity=".8"/>',
        f'<text x="152" y="45" fill="{NEON_GREEN}" font-family="monospace" font-size="14" font-weight="bold" letter-spacing="2">PROJECT // VAAYU [ATMOSPHERIC SENSORY NETWORK]</text>',
        f'<text x="856" y="45" fill="{CYAN}" font-family="monospace" font-size="11" font-weight="bold" text-anchor="end">[ PROTOCOL: SENSING ]</text>',
        
        # Subtitle
        f'<text x="136" y="80" fill="{AMBER}" font-family="monospace" font-size="12" font-weight="bold" letter-spacing="1">ENVIRONMENTAL INTELLIGENCE &amp; REAL-TIME AIR TELEMETRY</text>',
        
        # Description
        f'<text x="136" y="108" fill="{TEXT_MAIN}" font-family="monospace" font-size="11.5">Atmospheric monitoring network designed for live sensory ingestion and telemetry tracking.</text>',
        f'<text x="136" y="128" fill="{TEXT_MUTED}" font-family="monospace" font-size="11">Processes air quality indices (AQI), microparticulate trends (PM2.5/PM10), and dispersion models.</text>',
        f'<text x="136" y="148" fill="{TEXT_MUTED}" font-family="monospace" font-size="11">Visualizes real-time sensor streams through interactive geospatial dashboards &amp; alerts.</text>',

        # Tech stack pills
        badge(136, 174, "PYTHON", NEON_GREEN),
        badge(222, 174, "FASTAPI", NEON_GREEN),
        badge(312, 174, "IOT STREAMS", CYAN),
        badge(434, 174, "REACT TELEMETRY", MAGENTA),
        badge(588, 174, "PREDICTIVE MODELING", AMBER),

        # Telemetry footer
        f'<line x1="136" y1="216" x2="872" y2="216" stroke="{PANEL_BORDER}" stroke-width="1"/>',
        f'<text x="136" y="233" fill="{TEXT_MUTED}" font-family="monospace" font-size="10" letter-spacing="1">REPO: github.com/Tanishq7361/Vaayu // SENSORY CHANNELS OPEN</text>',
    ]
    return cyber_svg(W, H, "".join(b), "", "Vaayu Cyber Deck")


def quest_cachecore():
    W, H = 900, 250
    b = [
        cyber_panel(W, H, ch=16, stroke=MAGENTA, fill="url(#cyberCardBg)", stroke_w=1.4),
        scanline(W, H, dur=4.2),
        reticle(76, 76, 36, MAGENTA),
        # Title chip
        f'<rect x="136" y="24" width="736" height="32" fill="#18081a" stroke="{MAGENTA}" stroke-width="1" stroke-opacity=".8"/>',
        f'<text x="152" y="45" fill="{MAGENTA}" font-family="monospace" font-size="14" font-weight="bold" letter-spacing="2">PROJECT // CACHECORE [IN-MEMORY KEY-VALUE DB]</text>',
        f'<text x="856" y="45" fill="{AMBER}" font-family="monospace" font-size="11" font-weight="bold" text-anchor="end">[ LOW-LATENCY C++20 ]</text>',
        
        # Subtitle
        f'<text x="136" y="80" fill="{CYAN}" font-family="monospace" font-size="12" font-weight="bold" letter-spacing="1">HIGH-CONCURRENCY IN-MEMORY STORAGE WITH DISK PERSISTENCE</text>',
        
        # Description
        f'<text x="136" y="108" fill="{TEXT_MAIN}" font-family="monospace" font-size="11.5">Engineered from ground up in modern C++20 with multithreaded reader-writer concurrency locks.</text>',
        f'<text x="136" y="128" fill="{TEXT_MUTED}" font-family="monospace" font-size="11">Implements LRU/LFU cache eviction policies, Write-Ahead Logging (WAL) for durability,</text>',
        f'<text x="136" y="148" fill="{TEXT_MUTED}" font-family="monospace" font-size="11">and periodic disk snapshotting to deliver sub-millisecond retrieval benchmarks.</text>',

        # Tech stack pills
        badge(136, 174, "C++20", MAGENTA),
        badge(210, 174, "CONCURRENCY LOCKS", MAGENTA),
        badge(384, 174, "WAL PERSISTENCE", CYAN),
        badge(538, 174, "EVICTION POLICIES", AMBER),
        badge(706, 174, "SYSTEMS", NEON_GREEN),

        # Telemetry footer
        f'<line x1="136" y1="216" x2="872" y2="216" stroke="{PANEL_BORDER}" stroke-width="1"/>',
        f'<text x="136" y="233" fill="{TEXT_MUTED}" font-family="monospace" font-size="10" letter-spacing="1">REPO: github.com/Tanishq7361/CacheCore // LOW-LEVEL ENGINE ONLINE</text>',
    ]
    return cyber_svg(W, H, "".join(b), "", "CacheCore Cyber Deck")


# ------------------------------------------------------------ feats of valor
def feats():
    W, H = 900, 270
    b = [
        cyber_panel(W, H, ch=16, stroke=CYAN, fill="url(#cyberCardBg)", stroke_w=1.2),
        scanline(W, H, dur=6.0),
    ]

    items = [
        ("GOLDMAN SACHS INDIA HACKATHON 2026", "QUALIFIER // INTERVIEW STAGE", "Advanced to competitive technical interview round among thousands of engineering contenders across India.", AMBER),
        ("GOOGLE AGENTIC AI DAY HACKATHON 2025", "ON-SITE FINALIST // BIEC BENGALURU", "Selected and invited on-site at BIEC Bengaluru to engineer autonomous agentic workflows & systems.", CYAN),
        ("TIC TECH TOE HACKATHONS", "CAMPUS LAURELS // DA-IICT", "Competed across multiple editions on-campus at Dhirubhai Ambani University, solving algorithmic & systems challenges.", NEON_GREEN),
        ("COMPETITIVE PROGRAMMING CADRE", "ACTIVE OPERATIVE // CODEFORCES & LEETCODE", "Regular solver on Codeforces (King-T), LeetCode (King-T_7361), CodeChef (tanishq7361), and Codolio.", MAGENTA),
    ]

    y = 20
    for title, badge_lbl, desc, col in items:
        b.append(
            f'<g transform="translate(24 {y})">'
            f'<rect width="852" height="52" fill="#070e1c" stroke="{PANEL_BORDER}" stroke-width="1"/>'
            f'<line x1="0" y1="0" x2="4" y2="52" stroke="{col}" stroke-width="4"/>'
            f'<text x="18" y="22" fill="{col}" font-family="monospace" font-size="12" font-weight="bold" letter-spacing="1">{title}</text>'
            f'<text x="836" y="22" fill="{TEXT_MUTED}" font-family="monospace" font-size="10" font-weight="bold" text-anchor="end" letter-spacing="1">[{badge_lbl}]</text>'
            f'<text x="18" y="40" fill="{TEXT_MAIN}" font-family="monospace" font-size="11">{desc}</text>'
            f'</g>'
        )
        y += 60

    return cyber_svg(W, H, "".join(b), "", "Combat Telemetry & Citations")


# ------------------------------------------------------------ action buttons
def button(label, icon_name, width_px=250):
    W, H = width_px, 48
    ch = 10
    poly = f"{ch},0 {W-ch},0 {W},{ch} {W},{H-ch} {W-ch},{H} {ch},{H} 0,{H-ch} 0,{ch}"
    
    b = [
        f'<polygon points="{poly}" fill="#081024" stroke="{CYAN}" stroke-width="1.4"/>',
        f'<polygon points="{ch+2},2 {W-ch-2},2 {W-2},{ch+2} {W-2},{H-ch-2} {W-ch-2},{H-2} {ch+2},{H-2} 2,{H-ch-2} 2,{ch+2}" fill="none" stroke="{MAGENTA}" stroke-width=".8" stroke-opacity=".4"/>',
        # Corner neon accents
        f'<path d="M 0,16 L 0,{ch} L {ch},0 L 16,0" fill="none" stroke="{CYAN_GLOW}" stroke-width="2.5"/>',
        f'<path d="M {W-16},{H} L {W-ch},{H} L {W},{H-ch} L {W},{H-16}" fill="none" stroke="{MAGENTA}" stroke-width="2.5"/>',
        
        # Label & Glyphs
        f'<text x="{W/2}" y="29" fill="{CYAN}" font-family="monospace" font-size="11.5" font-weight="bold" text-anchor="middle" letter-spacing="1.8">'
        f'&gt;&gt; {label} &lt;&lt;'
        f'</text>',
    ]
    return cyber_svg(W, H, "".join(b), "", label)


# ------------------------------------------------------------------ footer
def footer():
    W, H = 1200, 360
    b = [
        # Cyber Void Sky
        f'<rect width="{W}" height="{H}" fill="url(#cyberSky)"/>',
        f'<rect width="{W}" height="{H}" fill="url(#cyberGrid)" opacity=".5"/>',

        # Perspective Wireframe Grid (Runway)
        f'<g stroke="{CYAN}" stroke-width="1" stroke-opacity=".25">'
        f'<line x1="600" y1="120" x2="0" y2="360"/>'
        f'<line x1="600" y1="120" x2="200" y2="360"/>'
        f'<line x1="600" y1="120" x2="400" y2="360"/>'
        f'<line x1="600" y1="120" x2="520" y2="360"/>'
        f'<line x1="600" y1="120" x2="680" y2="360"/>'
        f'<line x1="600" y1="120" x2="800" y2="360"/>'
        f'<line x1="600" y1="120" x2="1000" y2="360"/>'
        f'<line x1="600" y1="120" x2="1200" y2="360"/>'
        f'</g>',

        # Grid rungs
        f'<g stroke="{MAGENTA}" stroke-width="1" stroke-opacity=".3">'
        f'<line x1="450" y1="160" x2="750" y2="160"/>'
        f'<line x1="360" y1="200" x2="840" y2="200"/>'
        f'<line x1="240" y1="250" x2="960" y2="250"/>'
        f'<line x1="80" y1="310" x2="1120" y2="310"/>'
        f'</g>',

        # Vanishing Sun / Wireframe Sphere
        f'<circle cx="600" cy="120" r="70" fill="none" stroke="{MAGENTA}" stroke-width="1.8" stroke-dasharray="8 6"/>',
        f'<circle cx="600" cy="120" r="40" fill="none" stroke="{CYAN}" stroke-width="1.4"/>',
        f'<circle cx="600" cy="120" r="6" fill="#fff"/>',

        # Center HUD Text Box
        f'<rect x="250" y="210" width="700" height="96" fill="#060c1c" fill-opacity=".92" stroke="{CYAN}" stroke-width="1.2"/>',
        f'<path d="M 250,230 L 250,210 L 270,210" fill="none" stroke="{CYAN}" stroke-width="3"/>',
        f'<path d="M 950,286 L 950,306 L 930,306" fill="none" stroke="{MAGENTA}" stroke-width="3"/>',

        # Farewell quote
        f'<text x="600" y="246" fill="{CYAN}" font-family="monospace" font-size="13" font-weight="bold" text-anchor="middle" letter-spacing="3">'
        f'// ALL RUNTIMES NOMINAL · ZERO UNCAUGHT EXCEPTIONS //'
        f'</text>',

        # Hallmark
        f'<text x="600" y="278" fill="{TEXT_MUTED}" font-family="monospace" font-size="11" text-anchor="middle" letter-spacing="2">'
        f'SYSTEM ARCHITECTED &amp; FORGED BY TANISHQ SHAH  ·  ANNO MMXXVI'
        f'</text>',

        f'<rect y="0" width="{W}" height="2" fill="url(#cyberLaser)"/>',
    ]
    return cyber_svg(W, H, "".join(b), "", "Farewell, Cyber Operative")
