"""Renderers for dynamic SVGs (stats, languages, heatmap) in Cyberpunk HUD theme."""
import math
import random

from cyber import (
    CYAN, CYAN_DIM, CYAN_GLOW, MAGENTA, PURPLE, NEON_GREEN, AMBER,
    DARK_BG, PANEL_BG, PANEL_BORDER, TEXT_MAIN, TEXT_MUTED,
    cyber_svg, cyber_panel, scanline, reticle
)
from medieval import txt, width, fit, wrap, para, esc, _n

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DASH = "—"


def fmt(v):
    return DASH if v is None else f"{v:,}"


def _glyph_commit(cx, cy):
    return (
        f'<g transform="translate({cx} {cy})" stroke="{CYAN}" stroke-width="2" fill="none">'
        f'<circle cx="0" cy="0" r="6"/>'
        f'<line x1="-14" y1="0" x2="-6" y2="0"/>'
        f'<line x1="6" y1="0" x2="14" y2="0"/>'
        f'</g>'
    )


def _glyph_pr(cx, cy):
    return (
        f'<g transform="translate({cx} {cy})" fill="none" stroke="{MAGENTA}" stroke-width="2" stroke-linecap="round">'
        f'<circle cx="-7" cy="-8" r="3.2"/><circle cx="-7" cy="9" r="3.2"/><circle cx="8" cy="9" r="3.2"/>'
        f'<path d="M-7 -4.8V5.8M-7 -1Q-7 4 8 5.6"/></g>'
    )


def _glyph_star(cx, cy):
    pts = []
    for k in range(10):
        r = 11 if k % 2 == 0 else 4.8
        a = -math.pi / 2 + k * math.pi / 5
        pts.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{AMBER}"/>'


def _glyph_repo(cx, cy):
    return (
        f'<g transform="translate({cx} {cy})" fill="none" stroke="{NEON_GREEN}" stroke-width="2" stroke-linejoin="round">'
        f'<path d="M-9 -11H7Q10 -11 10 -8V10H-6Q-9 10 -9 7Z"/><path d="M-9 7Q-9 4 -6 4H10"/><path d="M-3 -5H4" stroke-linecap="round"/></g>'
    )


def stats(d):
    W, H = 900, 468
    b = [
        cyber_panel(W, H, ch=16, stroke=CYAN, fill="url(#cyberCardBg)", stroke_w=1.4),
        scanline(W, H, dur=6.0),
    ]

    def big(cx, cy, value, label, sub, col=CYAN):
        s = fit("deco", value, 50, 220, 1)
        return (
            txt("deco", value, s, cx, cy, col, "middle", 1)
            + f'<text x="{cx}" y="{cy + 34}" fill="{TEXT_MUTED}" font-family="monospace" font-size="11" font-weight="bold" text-anchor="middle" letter-spacing="2">{label}</text>'
            + f'<text x="{cx}" y="{cy + 58}" fill="{TEXT_MUTED}" font-family="monospace" font-size="10" text-anchor="middle">{sub}</text>'
        )

    b.append(big(160, 150, fmt(d.get("total")), "TOTAL TELEMETRY", d.get("since_label", "since first commit"), CYAN))
    b.append(big(740, 150, fmt(d.get("longest")), "LONGEST OVERCLOCK", d.get("longest_range", ""), MAGENTA))

    # Centre Reticle Medallion: Current Streak
    cx, cy = 450, 140
    v = fmt(d.get("cur"))
    b.append(
        f'<circle cx="{cx}" cy="{cy}" r="78" fill="#060c18" stroke="{PANEL_BORDER}" stroke-width="2"/>'
        f'<circle cx="{cx}" cy="{cy}" r="70" fill="none" stroke="{CYAN}" stroke-width="2" stroke-dasharray="12 8">'
        f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="10s" repeatCount="indefinite"/>'
        f'</circle>'
        f'<circle cx="{cx}" cy="{cy}" r="58" fill="none" stroke="{MAGENTA}" stroke-width="1.5" stroke-dasharray="18 12">'
        f'<animateTransform attributeName="transform" type="rotate" from="360 {cx} {cy}" to="0 {cx} {cy}" dur="8s" repeatCount="indefinite"/>'
        f'</circle>'
    )
    b.append(txt("deco", v, fit("deco", v, 48, 90, 0), cx, cy + 16, "#ffffff", "middle", 0))
    b.append(f'<text x="{cx}" y="{cy + 104}" fill="{CYAN}" font-family="monospace" font-size="12" font-weight="bold" text-anchor="middle" letter-spacing="2">ACTIVE STREAK DAYS</text>')
    b.append(f'<text x="{cx}" y="{cy + 124}" fill="{TEXT_MUTED}" font-family="monospace" font-size="10.5" text-anchor="middle">{d.get("cur_range", "")}</text>')

    # Divider line
    b.append(f'<line x1="60" y1="284" x2="840" y2="284" stroke="{PANEL_BORDER}" stroke-width="1.2"/>')

    cols = [
        (_glyph_commit, fmt(d.get("commits")), "COMMITS // 12 MO", CYAN),
        (_glyph_pr, fmt(d.get("prs")), "PULL REQUESTS", MAGENTA),
        (_glyph_star, fmt(d.get("stars")), "STARS EARNED", AMBER),
        (_glyph_repo, fmt(d.get("repos")), "PUBLIC REPOS", NEON_GREEN)
    ]
    for i, (g, val, lab, col) in enumerate(cols):
        x = 112 + i * 225
        b.append(
            f'<circle cx="{x}" cy="326" r="22" fill="#071020" stroke="{col}" stroke-width="1.2"/>'
            f'<circle cx="{x}" cy="326" r="26" fill="{col}" opacity=".15"><animate attributeName="r" values="22;30;22" dur="3s" repeatCount="indefinite"/></circle>'
            + g(x, 326)
            + txt("deco", val, fit("deco", val, 30, 160, 1), x, 390, col, "middle", 1)
            + f'<text x="{x}" y="{416}" fill="{TEXT_MUTED}" font-family="monospace" font-size="10" font-weight="bold" text-anchor="middle" letter-spacing="1">{lab}</text>'
        )
        if i:
            b.append(f'<line x1="{x - 112.5}" y1="306" x2="{x - 112.5}" y2="430" stroke="{PANEL_BORDER}" stroke-width="1"/>')

    b.append(f'<text x="450" y="452" fill="{TEXT_MUTED}" font-family="monospace" font-size="10" text-anchor="middle" letter-spacing="1">{d.get("updated_label", "// NEURAL LEDGER SYNCED VIA GITHUB GRAPHQL API //")}</text>')
    return cyber_svg(W, H, "".join(b), "", "GitHub Cyber Stats Matrix")


PALETTE = [
    ("#00f0ff", "#0088cc"),
    ("#ff007f", "#aa0055"),
    ("#00ff9d", "#00995e"),
    ("#fcee0a", "#cc9900"),
    ("#9d00ff", "#5500aa"),
    ("#38b6ff", "#0055aa")
]


def langs(d):
    rows = (d.get("langs") or [])[:6]
    placeholder = not rows
    n = 0 if placeholder else len(rows)
    W, H = 900, (190 if placeholder else 96 + n * 48 + 12)
    defs = "".join(f'<linearGradient id="cyberLg{i}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{c}"/></linearGradient>'
                   for i, (a, c) in enumerate(PALETTE))
    
    b = [
        cyber_panel(W, H, ch=14, stroke=CYAN, fill="url(#cyberCardBg)", stroke_w=1.2),
        f'<text x="48" y="48" fill="{CYAN}" font-family="monospace" font-size="14" font-weight="bold" letter-spacing="2">TELEMETRY // CODE METRICS BY WEIGHT</text>',
        f'<text x="{W - 48}" y="48" fill="{TEXT_MUTED}" font-family="monospace" font-size="11" text-anchor="end">BYTES PER LANGUAGE IN REPOS</text>',
        f'<line x1="48" y1="62" x2="{W - 48}" y2="62" stroke="{PANEL_BORDER}" stroke-width="1.2"/>'
    ]

    bx, bw = 240, 520
    for i in range(n):
        y = 86 + i * 48
        name, pct = rows[i]
        col_idx = i % len(PALETTE)
        col_pair = PALETTE[col_idx]
        fw = max(14, bw * pct / 100) if not placeholder else 0
        b.append(f'<circle cx="58" cy="{y + 11}" r="5" fill="{col_pair[0]}"/>')
        b.append(f'<text x="76" y="{y + 16}" fill="{TEXT_MAIN}" font-family="monospace" font-size="12" font-weight="bold">{name.upper()}</text>')
        b.append(f'<rect x="{bx}" y="{y}" width="{bw}" height="18" fill="#070d1a" stroke="{PANEL_BORDER}" stroke-width="1"/>')
        if not placeholder:
            b.append(f'<rect x="{bx}" y="{y}" width="{fw:.0f}" height="18" fill="url(#cyberLg{col_idx})"/>')
            b.append(f'<text x="{W - 48}" y="{y + 15}" fill="{col_pair[0]}" font-family="monospace" font-size="12" font-weight="bold" text-anchor="end">{pct:.1f}%</text>')

    if placeholder:
        b.append(f'<text x="450" y="130" fill="{CYAN}" font-family="monospace" font-size="14" text-anchor="middle">[ COMPILING CODE TELEMETRY SCANS... ]</text>')

    return cyber_svg(W, H, "".join(b), defs, "Cyber Language Distribution")


LEVELS = ["#070d1c", "#004759", "#008399", "#00c8db", "#00f0ff"]


def heatmap(d):
    weeks = d.get("weeks")
    W, H = 900, 240
    c, g, x0, y0 = 12, 3, 84, 94
    placeholder = not weeks
    if placeholder:
        weeks = [[(None, 0)] * 7 for _ in range(53)]
    mx = max((cnt for wk in weeks for _, cnt in wk), default=0)
    total = d.get("year_total")

    b = [
        cyber_panel(W, H, ch=14, stroke=CYAN, fill="url(#cyberCardBg)", stroke_w=1.2),
        f'<text x="48" y="48" fill="{CYAN}" font-family="monospace" font-size="14" font-weight="bold" letter-spacing="2">CHRONICLE // NEURAL FIRINGS MATRIX</text>',
        f'<text x="{W - 48}" y="48" fill="{NEON_GREEN}" font-family="monospace" font-size="11" text-anchor="end">{total:,} CONTRIBUTIONS IN PAST YEAR' if total is not None else f'<text x="{W - 48}" y="48" fill="{NEON_GREEN}" font-family="monospace" font-size="11" text-anchor="end">ANNUAL SENSOR MATRIX',
        f'<line x1="48" y1="62" x2="{W - 48}" y2="62" stroke="{PANEL_BORDER}" stroke-width="1.2"/>'
    ]

    rng = random.Random(42)
    prev, last_x = None, -99
    cells = []
    for ci, wk in enumerate(weeks):
        x = x0 + ci * (c + g)
        first = wk[0][0]
        if first:
            m = int(first[5:7]) - 1
            if m != prev:
                if ci < len(weeks) - 2 and x - last_x >= 40:
                    b.append(f'<text x="{x}" y="82" fill="{TEXT_MUTED}" font-family="monospace" font-size="9.5">{MONTHS[m].upper()}</text>')
                    last_x = x
                prev = m
        for ri, (dt, cnt) in enumerate(wk):
            lvl = 0 if cnt <= 0 or mx == 0 else max(1, min(4, math.ceil(4 * cnt / mx)))
            y = y0 + ri * (c + g)
            extra = ""
            if lvl == 4 and rng.random() < .4:
                extra = f'><animate attributeName="fill" values="{LEVELS[4]};#ffffff;{LEVELS[4]}" dur="{rng.uniform(2, 4):.1f}s" repeatCount="indefinite"/></rect'
            cells.append(f'<rect x="{x}" y="{y}" width="{c}" height="{c}" fill="{LEVELS[lvl]}" stroke="#040814" stroke-width=".6"{extra}/>'.replace("/></rect/>", "/></rect>"))

    b.append("".join(cells))
    for ri, lab in ((1, "MON"), (3, "WED"), (5, "FRI")):
        b.append(f'<text x="{x0 - 8}" y="{y0 + ri * (c + g) + 9}" fill="{TEXT_MUTED}" font-family="monospace" font-size="8.5" text-anchor="end">{lab}</text>')

    # Legend
    ly = H - 28
    lx = W - 48 - 5 * (c + 4) - 64
    b.append(f'<text x="{lx}" y="{ly + 9}" fill="{TEXT_MUTED}" font-family="monospace" font-size="9" text-anchor="end">IDLE</text>')
    for i in range(5):
        b.append(f'<rect x="{lx + 8 + i * (c + 4)}" y="{ly}" width="{c}" height="{c}" fill="{LEVELS[i]}"/>')
    b.append(f'<text x="{lx + 14 + 5 * (c + 4)}" y="{ly + 9}" fill="{TEXT_MUTED}" font-family="monospace" font-size="9">PEAK</text>')

    if placeholder:
        b.append(f'<text x="450" y="140" fill="{CYAN}" font-family="monospace" font-size="14" text-anchor="middle">[ SENSORS COMPILING TELEMETRY CHRONICLE... ]</text>')

    return cyber_svg(W, H, "".join(b), "", "Cyber Contribution Heatmap")
