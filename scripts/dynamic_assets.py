"""Renderers for the SVGs that change with your GitHub activity."""
import math
import random

from medieval import *  # noqa: F401,F403
from medieval import _n

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DASH = "—"


def fmt(v):
    return DASH if v is None else f"{v:,}"


def _glyph_commit(cx, cy):
    return sword(cx, cy + 4, 45, .55)


def _glyph_pr(cx, cy):
    return (f'<g transform="translate({cx} {cy})" fill="none" stroke="url(#gold)" stroke-width="2" stroke-linecap="round">'
            '<circle cx="-7" cy="-8" r="3.2"/><circle cx="-7" cy="9" r="3.2"/><circle cx="8" cy="9" r="3.2"/>'
            '<path d="M-7 -4.8V5.8M-7 -1Q-7 4 8 5.6"/></g>')


def _glyph_star(cx, cy):
    pts = []
    for k in range(10):
        r = 12 if k % 2 == 0 else 5.2
        a = -math.pi / 2 + k * math.pi / 5
        pts.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="url(#gold)"/>'


def _glyph_repo(cx, cy):
    return (f'<g transform="translate({cx} {cy})" fill="none" stroke="url(#gold)" stroke-width="2" stroke-linejoin="round">'
            '<path d="M-9 -11H7Q10 -11 10 -8V10H-6Q-9 10 -9 7Z"/><path d="M-9 7Q-9 4 -6 4H10"/><path d="M-3 -5H4" stroke-linecap="round"/></g>')


def stats(d):
    W, H = 900, 468
    defs = shine("sn", 100, 800, 6, 240) + (
        '<linearGradient id="ringg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff1b8"/><stop offset=".5" stop-color="#d9a92e"/><stop offset="1" stop-color="#8a6d1f"/></linearGradient>')
    b = [panel(W, H, 14, 7)]

    def big(cx, cy, value, label, sub):
        s = fit("deco", value, 52, 220, 1)
        return (gold_text("deco", value, s, cx, cy, "sn", "middle", 1)
                + txt("cin", label, 13, cx, cy + 34, SILVER, "middle", 4)
                + txt("ital", sub, 18, cx, cy + 58, "#8fa0c6", "middle"))

    b.append(big(160, 150, fmt(d.get("total")), "TOTAL DEEDS", d.get("since_label", "since the first commit")))
    b.append(big(740, 150, fmt(d.get("longest")), "LONGEST STREAK", d.get("longest_range", "")))
    # centre medallion: current streak
    cx, cy = 450, 138
    v = fmt(d.get("cur"))
    b.append(f'<circle cx="{cx}" cy="{cy}" r="88" fill="url(#glowGold)" opacity=".35"><animate attributeName="opacity" values=".2;.45;.2" dur="4s" repeatCount="indefinite"/></circle>'
             f'<circle cx="{cx}" cy="{cy}" r="68" fill="#0a0f1d" stroke="url(#ringg)" stroke-width="5"/>'
             f'<circle cx="{cx}" cy="{cy}" r="59" fill="none" stroke="{GOLD}" stroke-opacity=".3" stroke-dasharray="2 5"/>'
             f'<circle cx="{cx}" cy="{cy}" r="68" fill="none" stroke="#fff6cf" stroke-width="5" stroke-linecap="round" stroke-dasharray="46 383">'
             f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="7s" repeatCount="indefinite"/></circle>'
             f'<g transform="translate({cx} {cy - 66}) scale(.5)"><g>'
             '<animateTransform attributeName="transform" type="scale" values="1 1;1.08 .92;.94 1.1;1 1" dur="1.2s" repeatCount="indefinite"/>'
             f'<path d="{FLAME}" fill="#ff7a1a"/><g transform="scale(.72)"><path d="{FLAME}" fill="#ffb92e"/></g>'
             f'<g transform="scale(.42)"><path d="{FLAME}" fill="#fff0a8"/></g></g></g>')
    b.append(gold_text("deco", v, fit("deco", v, 54, 92, 0), cx, cy + 18, "sn", "middle", 0, False))
    b.append(txt("cin", "CURRENT STREAK", 13, cx, cy + 102, GOLD_HI, "middle", 4))
    b.append(txt("ital", d.get("cur_range", ""), 18, cx, cy + 126, "#8fa0c6", "middle"))
    b.append(orn(450, 292, 380))

    cols = [(_glyph_commit, fmt(d.get("commits")), "COMMITS · 12 MO"),
            (_glyph_pr, fmt(d.get("prs")), "PULL REQUESTS"),
            (_glyph_star, fmt(d.get("stars")), "STARS EARNED"),
            (_glyph_repo, fmt(d.get("repos")), "PUBLIC REPOS")]
    for i, (g, val, lab) in enumerate(cols):
        x = 112 + i * 225
        b.append(f'<circle cx="{x}" cy="330" r="22" fill="#0b1020" stroke="{GOLD}" stroke-opacity=".55"/>'
                 f'<circle cx="{x}" cy="330" r="27" fill="url(#glowGold)" opacity=".0"><animate attributeName="opacity" values="0;.5;0" dur="{3 + i * .5}s" begin="-{i}s" repeatCount="indefinite"/></circle>'
                 + g(x, 330)
                 + gold_text("deco", val, fit("deco", val, 32, 170, 1), x, 393, "sn", "middle", 1, False)
                 + txt("cin", lab, 11.5, x, 418, SILVER, "middle", 3))
        if i:
            b.append(f'<rect x="{x - 112.5}" y="312" width="1" height="100" fill="{GOLD}" opacity=".18"/>')
    b.append(txt("ital", d.get("updated_label", "Awaiting the first muster of the scribes"), 15, 450, 452, "#5f6f96", "middle"))
    return svg(W, H, "".join(b), defs, "Ledger of the realm: contributions, streaks, commits, pull requests, stars and public repositories")


PALETTE = [("#f7dc7a", "#a97f1c"), ("#e8eefc", "#7d8bab"), ("#6fe0b0", "#1b7a5a"),
           ("#ef6b7d", "#8e2436"), ("#7fb0ff", "#2a4fa0"), ("#ffb45a", "#b0561a")]


def langs(d):
    rows = (d.get("langs") or [])[:6]
    placeholder = not rows
    n = 0 if placeholder else len(rows)
    W, H = 900, (190 if placeholder else 96 + n * 46 + 8)
    defs = "".join(f'<linearGradient id="lg{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{c}"/></linearGradient>'
                   for i, (a, c) in enumerate(PALETTE))
    defs += '<linearGradient id="sw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
    b = [panel(W, H, 14, 7),
         txt("cinb", "TONGUES BY WEIGHT", 15, 48, 50, "url(#gold)", "start", 5),
         txt("ital", "measured in bytes across my public repositories", 18, W - 48, 50, "#8fa0c6", "end"),
         f'<rect x="48" y="62" width="{W - 96}" height="1" fill="url(#goldH)" opacity=".4"/>']
    bx, bw = 250, 500
    for i in range(n):
        y = 88 + i * 46
        name, pct = rows[i]
        col = i % len(PALETTE)
        fw = max(16, bw * pct / 100) if not placeholder else 0
        b.append(f'<circle cx="60" cy="{y + 9}" r="5" fill="url(#lg{col})"/>')
        b.append(txt("cinb", name.upper(), fit("cinb", name.upper(), 14, 165, 2), 78, y + 14, PARCH, "start", 2))
        b.append(f'<rect x="{bx}" y="{y}" width="{bw}" height="18" rx="9" fill="#080c18" stroke="{GOLD}" stroke-opacity=".28"/>')
        if not placeholder:
            b.append(f'<rect x="{bx}" y="{y}" width="{fw:.0f}" height="18" rx="9" fill="url(#lg{col})"/>'
                     f'<clipPath id="c{i}"><rect x="{bx}" y="{y}" width="{fw:.0f}" height="18" rx="9"/></clipPath>'
                     f'<g clip-path="url(#c{i})"><rect y="{y}" width="60" height="18" fill="url(#sw)">'
                     f'<animate attributeName="x" values="{bx - 60};{bx + fw:.0f}" dur="{3.4 + i * .5:.1f}s" begin="-{i * .8:.1f}s" repeatCount="indefinite"/></rect></g>')
            b.append(txt("cinb", f"{pct:.1f}%", 14, W - 48, y + 14, "#f4e2a4", "end", 1.5))
    if placeholder:
        b.append(txt("ital", "The scribes are counting the tongues…", 26, 450, 132, "#f4e2a4", "middle"))
    return svg(W, H, "".join(b), defs, "Languages by share of code: " + (", ".join(f"{a} {p:.0f}%" for a, p in rows) or "not yet counted"))


LEVELS = ["#151c2f", "#5a4713", "#9a7a1c", "#dcae2e", "#ffe38a"]


def heatmap(d):
    weeks = d.get("weeks")
    W, H = 900, 240
    c, g, x0, y0 = 12, 3, 84, 94
    defs = ('<linearGradient id="beam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff2c0" stop-opacity="0"/>'
            '<stop offset=".5" stop-color="#fff2c0" stop-opacity=".16"/><stop offset="1" stop-color="#fff2c0" stop-opacity="0"/></linearGradient>')
    placeholder = not weeks
    if placeholder:
        weeks = [[(None, 0)] * 7 for _ in range(53)]
    mx = max((cnt for wk in weeks for _, cnt in wk), default=0)
    total = d.get("year_total")
    b = [panel(W, H, 14, 7),
         txt("cinb", "CHRONICLE OF DEEDS", 15, 48, 50, "url(#gold)", "start", 5),
         txt("ital", (f"{total:,} deeds in the past year" if total is not None else "the past year, day by day"), 18, W - 48, 50, "#8fa0c6", "end"),
         f'<rect x="48" y="62" width="{W - 96}" height="1" fill="url(#goldH)" opacity=".4"/>']
    rng = random.Random(5)
    prev, last_x = None, -99
    cells = []
    for ci, wk in enumerate(weeks):
        x = x0 + ci * (c + g)
        first = wk[0][0]
        if first:
            m = int(first[5:7]) - 1
            if m != prev:
                if ci < len(weeks) - 2 and x - last_x >= 40:
                    b.append(txt("cin", MONTHS[m].upper(), 10, x, 84, "#8fa0c6", "start", 1.5))
                    last_x = x
                prev = m
        for ri, (dt, cnt) in enumerate(wk):
            lvl = 0 if cnt <= 0 or mx == 0 else max(1, min(4, math.ceil(4 * cnt / mx)))
            y = y0 + ri * (c + g)
            extra = ""
            if lvl == 4 and rng.random() < .45:
                extra = f'><animate attributeName="fill" values="{LEVELS[4]};#fffbe6;{LEVELS[4]}" dur="{rng.uniform(2, 5):.1f}s" begin="-{rng.uniform(0, 4):.1f}s" repeatCount="indefinite"/></rect'
            cells.append(f'<rect x="{x}" y="{y}" width="{c}" height="{c}" rx="3" fill="{LEVELS[lvl]}"{extra}/>'.replace("/></rect/>", "/></rect>"))
    b.append("".join(cells))
    for ri, lab in ((1, "MON"), (3, "WED"), (5, "FRI")):
        b.append(txt("cin", lab, 8.5, x0 - 8, y0 + ri * (c + g) + 10, "#6f7fa6", "end", 1))
    gw = 53 * (c + g)
    b.append(f'<clipPath id="gridclip"><rect x="{x0}" y="{y0}" width="{gw}" height="{7 * (c + g)}"/></clipPath>'
             f'<g clip-path="url(#gridclip)"><rect y="{y0}" width="110" height="{7 * (c + g)}" fill="url(#beam)">'
             f'<animate attributeName="x" values="{x0 - 110};{x0 + gw}" dur="7s" repeatCount="indefinite"/></rect></g>')
    # legend
    ly = H - 34
    lx = W - 48 - 5 * (c + 4) - 56
    b.append(txt("cin", "FEWER", 9.5, lx, ly + 10, "#6f7fa6", "end", 2))
    for i in range(5):
        b.append(f'<rect x="{lx + 10 + i * (c + 4)}" y="{ly}" width="{c}" height="{c}" rx="3" fill="{LEVELS[i]}"/>')
    b.append(txt("cin", "MORE", 9.5, lx + 16 + 5 * (c + 4), ly + 10, "#6f7fa6", "start", 2))
    if placeholder:
        b.append('<rect x="240" y="118" width="420" height="56" rx="28" fill="#0a0f1d" fill-opacity=".92" stroke="#d9b13b" stroke-opacity=".5"/>'
                 + txt("ital", "The scribes are compiling the chronicle…", 24, 450, 154, "#f4e2a4", "middle"))
    return svg(W, H, "".join(b), defs, "Contribution heatmap for the past year")
