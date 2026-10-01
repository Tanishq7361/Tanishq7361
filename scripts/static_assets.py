"""Renderers for the hand-authored, never-changing SVG assets."""
import math
import random

from medieval import *  # noqa: F401,F403
from medieval import _n

SPLINE = 'calcMode="spline" keyTimes="0;.5;1" keySplines=".45 0 .55 1;.45 0 .55 1"'


# ------------------------------------------------------------------ header
def header():
    W, H = 1200, 460
    rng = random.Random(7)
    size = fit("deco", "TANISHQ SHAH", 88, 860, 6)
    sub = "WANDERER OF CODE  ·  FORGER OF FULL-STACK REALMS"
    ssize = fit("cin", sub, 21, 860, 5)

    defs = shine("tg", 150, 1050, 6.5, 320) + """
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#03050b"/><stop offset=".5" stop-color="#0b1430"/><stop offset=".82" stop-color="#1b2448"/><stop offset="1" stop-color="#2f2f52"/></linearGradient>
<radialGradient id="horizon"><stop offset="0" stop-color="#e8b34a" stop-opacity=".38"/><stop offset="1" stop-color="#e8b34a" stop-opacity="0"/></radialGradient>
<linearGradient id="m1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#26355f"/><stop offset="1" stop-color="#131c3a"/></linearGradient>
<linearGradient id="m2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#172344"/><stop offset="1" stop-color="#0b1228"/></linearGradient>
<radialGradient id="scrim"><stop offset="0" stop-color="#03050b" stop-opacity=".7"/><stop offset="1" stop-color="#03050b" stop-opacity="0"/></radialGradient>
<linearGradient id="shoot" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="shade" x1="0" y1="0" x2="0" y2="1"><stop offset=".35" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#3a2400" stop-opacity=".6"/></linearGradient>
"""
    r1, r1top = ridge(rng, W, H, 372, 125, .58)
    r2, r2top = ridge(rng, W, H, 412, 100, .55)
    r3, _ = ridge(rng, W, H, 444, 62, .5)

    b = [f'<rect width="{W}" height="{H}" fill="url(#sky)"/>',
         f'<ellipse cx="600" cy="{H * .78:.0f}" rx="680" ry="210" fill="url(#horizon)"><animate attributeName="opacity" values=".7;1;.7" dur="9s" repeatCount="indefinite"/></ellipse>',
         stars(rng, 120, W, 280), moon(985, 104, 34),
         # shooting star
         '<g opacity="0"><animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;.58;.6;.68;1" dur="11s" repeatCount="indefinite"/>'
         '<animateTransform attributeName="transform" type="translate" values="260 30;260 30;620 170;620 170" keyTimes="0;.58;.68;1" dur="11s" repeatCount="indefinite"/>'
         '<rect x="-90" y="-.8" width="90" height="1.6" fill="url(#shoot)" transform="rotate(23)"/></g>',
         # distant ridge
         f'<path d="{r1}" fill="url(#m1)"/><path d="{r1top}" fill="none" stroke="#3a4d82" stroke-opacity=".55" stroke-width="1"/>',
         citadel(1000, 374, .42, fill="#0d1631", rim="#22315a", windows=True, beacon=False, seed=5),
         f'<path d="{r2}" fill="url(#m2)"/><path d="{r2top}" fill="none" stroke="#2a3a66" stroke-opacity=".5" stroke-width="1"/>',
         '<path d="M20 470Q215 380 410 470Z" fill="#0a1128"/>',
         citadel(215, 414, 1.0, seed=2)]
    # drifting mist
    for i, (cx, cy, rx, ry, dur) in enumerate([(300, 380, 340, 26, 26), (820, 400, 380, 24, 34), (560, 350, 300, 18, 30)]):
        b.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#9db4e0" opacity=".11" filter="url(#b16)">'
                 f'<animateTransform attributeName="transform" type="translate" values="-70 0;70 0;-70 0" dur="{dur}s" begin="-{i * 7}s" repeatCount="indefinite"/></ellipse>')
    b += [f'<path d="{r3}" fill="#080d1b"/>',
          f'<g transform="translate(0 0)">{pines(rng, W, H + 4, 46, 46, 96, "#070c19")}</g>',
          f'<g>{pines(rng, 330, H + 4, 16, 70, 125, "#03060c")}</g>',
          f'<g transform="translate(870 0)">{pines(rng, 330, H + 4, 16, 70, 125, "#03060c")}</g>',
          f'<g transform="translate(330 0)">{pines(rng, 540, H + 4, 14, 40, 70, "#03060c")}</g>',
          fireflies(rng, 15, 60, 1140, 300, 430),
          brazier(66, H - 6, 1.0, 11), brazier(1134, H - 6, 1.0, 12)]

    # title block
    b += ['<ellipse cx="600" cy="208" rx="520" ry="120" fill="url(#scrim)"/>',
          txt("cin", "— HEARKEN, TRAVELER —", 14, 600, 92, SILVER, "middle", 7, 'opacity=".85"'),
          orn(600, 112, 250),
          txt("deco", "TANISHQ SHAH", size, 600, 220, "#000", "middle", 6, 'opacity=".6" transform="translate(0 4)" filter="url(#b3)"'),
          f'<g><animate attributeName="opacity" values="1;.86;1" dur="6s" repeatCount="indefinite"/>'
          + txt("deco", "TANISHQ SHAH", size, 600, 218, "#ffd56a", "middle", 6, 'opacity=".28" filter="url(#b8)"') + "</g>",
          gold_text("deco", "TANISHQ SHAH", size, 600, 218, "tg", "middle", 6, False, 'stroke="#5a3f0c" stroke-width=".8" paint-order="stroke"'),
          txt("cin", sub, ssize, 600, 262, "#dbe4f7", "middle", 5),
          orn(600, 284, 150),
          txt("cin", "B.TECH ICT  ·  DHIRUBHAI AMBANI UNIVERSITY", 13, 600, 312, "#93a4c9", "middle", 4)]
    b.append(f'<rect y="{H - 2}" width="{W}" height="2" fill="url(#goldH)"/>')
    return svg(W, H, "".join(b), defs, "Tanishq Shah, wanderer of code and forger of full-stack realms")


# ----------------------------------------------------- rotating epithets
def titles():
    W, H = 900, 66
    items = ["FULL STACK ARTISAN", "ARCHITECT OF SYSTEMS", "APPRENTICE OF MACHINE LEARNING", "SLAYER OF ALGORITHMS IN C++"]
    defs = shine("tt", 250, 650, 3.2, 200)
    b = [panel(W, H, 12, 6),
         sword(76, 33, 90, .95), sword(824, 33, -90, .95),
         '<rect x="112" y="32.4" width="60" height="1.2" fill="url(#fadeL)"/><rect x="728" y="32.4" width="60" height="1.2" fill="url(#fadeR)"/>']
    for i, t in enumerate(items):
        s = fit("cinb", t, 22, 560, 5)
        b.append(
            f'<g opacity="{1 if i == 0 else 0}"><animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;.05;.22;.27;1" '
            f'dur="12s" begin="{3 * i}s" repeatCount="indefinite"/>'
            f'<animateTransform attributeName="transform" type="translate" values="0 6;0 0;0 0;0 -6;0 -6" keyTimes="0;.05;.22;.27;1" dur="12s" begin="{3 * i}s" repeatCount="indefinite"/>'
            + gold_text("cinb", t, s, 450, 41, "tt", "middle", 5, False) + "</g>")
    for x in (190, 710):
        b.append(diamond(x, 33, 3.5, GOLD, pulse(dur=2.4)))
    return svg(W, H, "".join(b), defs, "Full Stack Artisan, Architect of Systems, Apprentice of Machine Learning, Slayer of Algorithms")


# --------------------------------------------------- section header/divider
def section_header(title, sub):
    W, H = 900, 98
    size = fit("deco", title, 36, 540, 2)
    tw = width("deco", title, size, 2)
    le, rs = 450 - tw / 2 - 24, 450 + tw / 2 + 24
    defs = shine("sg", 200, 700, 5.5, 240)
    b = [panel(W, H, 12, 6),
         sword(66, 47, 90, 1.15), sword(834, 47, -90, 1.15),
         f'<rect x="118" y="46.4" width="{le - 118:.0f}" height="1.2" fill="url(#fadeL)"/>',
         f'<rect x="{rs:.0f}" y="46.4" width="{782 - rs:.0f}" height="1.2" fill="url(#fadeR)"/>',
         diamond(le, 47, 4.5, GOLD, pulse(dur=2.8)), diamond(rs, 47, 4.5, GOLD, pulse(dur=2.8, begin=1.4)),
         gold_text("deco", title, size, 450, 58, "sg", "middle", 2),
         txt("cin", sub.upper(), 12, 450, 82, "#93a4c9", "middle", 5)]
    return svg(W, H, "".join(b), defs, title)


def divider():
    W, H = 900, 52
    b = [f'<rect x="90" y="25.4" width="300" height="1.2" fill="url(#fadeL)"/><rect x="510" y="25.4" width="300" height="1.2" fill="url(#fadeR)"/>',
         '<circle cx="450" cy="26" r="30" fill="url(#glowGold)"><animate attributeName="opacity" values=".4;.9;.4" dur="3.6s" repeatCount="indefinite"/></circle>',
         sword(450, 33, 42, .8), sword(450, 33, -42, .8),
         diamond(450, 26, 4.5, "url(#gold)")]
    for i, dx in enumerate((66, 112, 170, 240)):
        r = 3.2 - i * .5
        b.append(diamond(450 - dx, 26, r, GOLD, pulse(dur=2.5 + i * .4, begin=i * .6)) + diamond(450 + dx, 26, r, GOLD, pulse(dur=2.5 + i * .4, begin=i * .6 + .3)))
    return svg(W, H, "".join(b), "", "divider")


# ------------------------------------------------------------ about scroll
def about():
    W, H = 900, 376
    rng = random.Random(4)
    defs = """
<linearGradient id="pa" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#c39c5c"/><stop offset=".1" stop-color="#e6d0a0"/><stop offset=".5" stop-color="#f1e2bb"/><stop offset=".9" stop-color="#e6d0a0"/><stop offset="1" stop-color="#c39c5c"/></linearGradient>
<radialGradient id="vig" cx=".5" cy=".5" r=".72"><stop offset=".5" stop-color="#5a3a10" stop-opacity="0"/><stop offset="1" stop-color="#5a3a10" stop-opacity=".45"/></radialGradient>
<linearGradient id="wood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b98146"/><stop offset=".35" stop-color="#d9a466"/><stop offset=".7" stop-color="#7a4d22"/><stop offset="1" stop-color="#4a2c12"/></linearGradient>
<linearGradient id="curlT" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a2208" stop-opacity=".38"/><stop offset="1" stop-color="#3a2208" stop-opacity="0"/></linearGradient>
<linearGradient id="curlB" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#3a2208" stop-opacity=".38"/><stop offset="1" stop-color="#3a2208" stop-opacity="0"/></linearGradient>
<linearGradient id="crest" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9c2a3d"/><stop offset="1" stop-color="#4a0f1b"/></linearGradient>
<radialGradient id="wax" cx=".38" cy=".32" r=".8"><stop offset="0" stop-color="#e0503f"/><stop offset=".55" stop-color="#a5271f"/><stop offset="1" stop-color="#5f1210"/></radialGradient>
<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="3"/><feColorMatrix type="matrix" values="0 0 0 0 .3  0 0 0 0 .2  0 0 0 0 .08  0 0 0 .9 -.34"/></filter>
"""
    px, py, pw, ph = 50, 50, 800, 276
    b = [f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" fill="url(#pa)"/>',
         f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" filter="url(#grain)"/>',
         f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" fill="url(#vig)"/>',
         f'<rect x="{px}" y="{py}" width="{pw}" height="22" fill="url(#curlT)"/><rect x="{px}" y="{py + ph - 22}" width="{pw}" height="22" fill="url(#curlB)"/>',
         f'<rect x="{px + 10}" y="{py + 10}" width="{pw - 20}" height="{ph - 20}" fill="none" stroke="#8a6532" stroke-opacity=".5" stroke-dasharray="1 5"/>']
    # rods
    for y in (24, 324):
        b.append(f'<rect x="28" y="{y}" width="844" height="28" rx="14" fill="url(#wood)" stroke="#3a2208" stroke-width="1"/>')
        for x in (28, 872):
            b.append(f'<circle cx="{x}" cy="{y + 14}" r="17" fill="url(#gold)" stroke="#6b4c10"/><circle cx="{x}" cy="{y + 14}" r="7" fill="#6b4a1c"/>')

    # crest
    b.append('<g transform="translate(74 100) scale(1.62)"><path d="' + shield_path() + '" fill="url(#crest)" stroke="url(#goldH)" stroke-width="2.4"/>'
             '<g transform="translate(6.3 7.2) scale(.86)"><path d="' + shield_path() + '" fill="none" stroke="#e9c85a" stroke-opacity=".55"/></g>'
             '<path d="M8 52L45 26L82 52" fill="none" stroke="#e9c85a" stroke-width="1.6" opacity=".7"/></g>')
    b.append(txt("deco", "TS", 48, 150, 212, "url(#gold)", "middle", 1, 'stroke="#2a0810" stroke-width=".8" paint-order="stroke"'))
    for dx, dy in ((-24, 0), (0, -8), (24, 0)):
        b.append(diamond(150 + dx, 128 + dy, 3.4, "#f4d466", pulse(dur=3, begin=abs(dx) / 10)))
    b.append(txt("cin", "MMXXVI", 13, 150, 244, "#ecd894", "middle", 4))

    b.append(txt("cinb", "THE WANDERER'S ROLL", 21, 560, 96, INK, "middle", 6))
    b.append('<rect x="380" y="106" width="360" height="1.2" fill="#7a5620" opacity=".55"/>' + diamond(560, 106.6, 4, "#7a5620"))
    rows = [("NAME", "Tanishq Shah"),
            ("ORDER", "B.Tech ICT · DA-IICT, Gandhinagar"),
            ("CALLINGS", "Full Stack · System Design · Machine Learning"),
            ("BLADE", "C++, for competitive programming"),
            ("CRAFT", "TypeScript & Python, for projects"),
            ("QUEST", "Argus, an AI-Powered Codebase Companion"),
            ("SEEKING", "Software engineering internships & placements")]
    y = 138
    for lab, val in rows:
        vs = fit("body", val, 22, 796 - 440)
        b.append(txt("cin", lab, 12.5, 292, y, "#6b4a1e", "start", 3.2))
        b.append(txt("body", val, vs, 440, y + 1, INK))
        b.append(f'<line x1="292" y1="{y + 9}" x2="796" y2="{y + 9}" stroke="#8a6532" stroke-opacity=".5" stroke-dasharray="1 4"/>')
        y += 27

    # wax seal
    pts = []
    for k in range(72):
        a = k / 72 * math.tau
        r = 27 + 2.2 * math.sin(a * 9) + 1.2 * math.sin(a * 5 + 1)
        pts.append(f"{'M' if k == 0 else 'L'}{_n(812 + r * math.cos(a))} {_n(96 + r * math.sin(a))}")
    b.append('<circle cx="812" cy="98" r="40" fill="#e0503f" opacity=".0" filter="url(#b8)"><animate attributeName="opacity" values="0;.35;0" dur="4s" repeatCount="indefinite"/></circle>'
             f'<path d="{"".join(pts)}Z" fill="url(#wax)"/><circle cx="812" cy="96" r="18" fill="none" stroke="#3d0a08" stroke-opacity=".45" stroke-width="1.6"/>'
             + txt("deco", "T", 26, 812, 106, "#4d0d0a", "middle", 0, 'opacity=".85"'))
    # drifting dust motes
    for _ in range(14):
        x, y0 = rng.uniform(70, 830), rng.uniform(160, 320)
        dur, bg = rng.uniform(8, 16), rng.uniform(0, 10)
        b.append(f'<circle cx="{x:.0f}" cy="{y0:.0f}" r="{rng.uniform(.8, 1.7):.1f}" fill="#b98a1e">'
                 f'<animate attributeName="cy" values="{y0:.0f};{y0 - 90:.0f}" dur="{dur:.1f}s" begin="-{bg:.1f}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="0;.7;0" dur="{dur:.1f}s" begin="-{bg:.1f}s" repeatCount="indefinite"/></circle>')
    return svg(W, H, "".join(b), defs, "Character sheet: Tanishq Shah, B.Tech ICT student at DA-IICT Gandhinagar. Callings: full stack, system design, machine learning. Current quest: Argus. Seeking software engineering internships.")


# ------------------------------------------------------------------ armory
TIERS = [
    ("TONGUES", "languages I wield", [("C++", "cplusplus"), ("Python", "python"), ("TypeScript", "typescript"), ("JavaScript", "javascript"), ("SQL", "mysql")]),
    ("TOOLS OF THE TRADE", "frameworks & libraries", [("React", "react"), ("FastAPI", "fastapi"), ("Node.js", "nodedotjs"), ("Tailwind", "tailwindcss"), ("Vite", "vite")]),
    ("REALMS & FORGES", "cloud, devops & systems", [("Git", "git"), ("Vercel", "vercel"), ("Render", "render"), ("Linux", "linux")]),
]


def arsenal():
    RH = 166
    W, H = 900, 24 + RH * 3 + 8
    defs = '<linearGradient id="sh" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1c2746"/><stop offset="1" stop-color="#090e1c"/></linearGradient>'
    b = [panel(W, H, 12, 6)]
    for r, (name, sub, items) in enumerate(TIERS):
        top = 26 + r * RH
        cy = top + 66
        lines = wrap("cinb", name, 17, 200, 3)
        y = cy - (len(lines) - 1) * 11 - 8
        for ln in lines:
            b.append(txt("cinb", ln, 17, 150, y, "url(#gold)", "middle", 3))
            y += 23
        b.append(txt("ital", sub, 18, 150, y + 4, "#93a4c9", "middle"))
        b.append(f'<rect x="272" y="{top + 8}" width="1.2" height="{RH - 40}" fill="{GOLD}" opacity=".35"/>')
        n = len(items)
        for i, (label, ic) in enumerate(items):
            cx = 584 + (i - (n - 1) / 2) * 118
            idx = r * 5 + i
            b.append(
                f'<g transform="translate({cx - 45:.0f} {top + 8})"><g>'
                f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -5;0 0" dur="{4 + idx % 3}s" begin="-{idx * .7:.1f}s" repeatCount="indefinite" {SPLINE}/>'
                f'<circle cx="45" cy="52" r="34" fill="url(#glowGold)">{pulse(lo=.25, hi=.7, dur=3.5, begin=idx * .5)}</circle>'
                f'<path d="{shield_path()}" fill="url(#sh)" stroke="url(#goldH)" stroke-width="2.4"/>'
                f'<g transform="translate(5.4 6.2) scale(.88)"><path d="{shield_path()}" fill="none" stroke="{GOLD}" stroke-opacity=".28"/></g>'
                + icon(ic, 45, 50, 40)
                + txt("cinb", label.upper(), fit("cinb", label.upper(), 12.5, 100, 1.6), 45, 134, PARCH, "middle", 1.6)
                + "</g></g>")
        if r < 2:
            b.append(orn(450, top + RH - 8, 380))
    return svg(W, H, "".join(b), defs, "Armory: C++, Python, TypeScript, JavaScript, SQL; React, FastAPI, Node.js, Tailwind CSS, Vite; Git, Vercel, Render, Linux")


# ------------------------------------------------------------------ quests
def _ring(extra=""):
    return ('<circle r="62" fill="none" stroke="url(#gold)" stroke-width="2" stroke-dasharray="2 9" opacity=".75">'
            '<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="70s" repeatCount="indefinite"/></circle>'
            '<circle r="53" fill="#0a0f1d" stroke="url(#goldH)" stroke-width="1.8"/>'
            '<circle r="47" fill="none" stroke="#d9b13b" stroke-opacity=".25"/>' + extra)


def _eye():
    return _ring(
        '<g><animateTransform attributeName="transform" type="scale" values="1 1;1 1;1 .06;1 1" keyTimes="0;.9;.95;1" dur="5.5s" repeatCount="indefinite"/>'
        '<path d="M-40 0Q0 -32 40 0Q0 32 -40 0Z" fill="#e9ddb8" stroke="url(#gold)" stroke-width="1.6"/>'
        '<g><animateTransform attributeName="transform" type="translate" values="0 0;7 0;-6 1;0 0" keyTimes="0;.35;.7;1" dur="9s" repeatCount="indefinite"/>'
        '<circle r="15.5" fill="url(#iris)"/><circle r="6.6" fill="#04070d"/><circle cx="-5" cy="-5" r="2.3" fill="#fff" opacity=".9"/></g></g>')


def _abacus():
    parts = ['<rect x="-38" y="-32" width="76" height="64" rx="5" fill="#181206" stroke="url(#gold)" stroke-width="1.8"/>']
    for j, y in enumerate((-19, -6.5, 6.5, 19)):
        parts.append(f'<line x1="-33" y1="{y}" x2="33" y2="{y}" stroke="#8a6d1f" stroke-width="1.2"/>')
        parts.append(f'<g><animateTransform attributeName="transform" type="translate" values="0 0;22 0;0 0" dur="{4.5 + j * 1.3}s" begin="-{j * 1.1}s" repeatCount="indefinite" {SPLINE}/>'
                     + "".join(f'<circle cx="{x}" cy="{y}" r="5" fill="url(#gold)" stroke="#5e470c" stroke-width=".6"/>' for x in (-26, -15.5)) + "</g>")
        parts.append("".join(f'<circle cx="{x}" cy="{y}" r="5" fill="url(#gold)" stroke="#5e470c" stroke-width=".6"/>' for x in (12, 22.5, 33 - 5)))
    return _ring("".join(parts))


def quest_card(title, subtitle, status, scol, desc, bullets, tags, emblem, uid):
    W, x0 = 900, 232
    maxw = W - x0 - 48
    defs = shine("tq", 250, 700, 5, 200) + (
        '<radialGradient id="iris"><stop offset="0" stop-color="#7cf0c4"/><stop offset=".55" stop-color="#1f8c6c"/><stop offset="1" stop-color="#0b3a34"/></radialGradient>')
    body = []
    tsize = fit("deco", title, 34, 360, 1.5)
    body.append(gold_text("deco", title, tsize, x0, 72, "tq", "start", 1.5))
    body.append(txt("cin", subtitle.upper(), 13, x0, 98, SILVER, "start", 3.4))
    body.append(f'<rect x="{x0}" y="112" width="{maxw}" height="1.2" fill="url(#goldH)" opacity=".55"/>')
    # status pill
    sw = width("cin", status, 11, 2.2)
    px = W - 48 - sw - 44
    body.append(f'<rect x="{px:.0f}" y="40" width="{sw + 44:.0f}" height="28" rx="14" fill="{scol}" fill-opacity=".1" stroke="{scol}" stroke-opacity=".7"/>'
                f'<circle cx="{px + 17:.0f}" cy="54" r="4" fill="{scol}">{pulse("opacity", .3, 1, 1.8)}</circle>'
                f'<circle cx="{px + 17:.0f}" cy="54" r="9" fill="{scol}" opacity=".0"><animate attributeName="opacity" values=".35;0;.35" dur="1.8s" repeatCount="indefinite"/></circle>'
                + txt("cin", status, 11, px + 32, 58, scol, "start", 2.2))
    d, n = para("body", desc, 21.5, x0, 144, maxw, 26, "#e4d7b0")
    body.append(d)
    y = 144 + n * 26 + 6
    for bl in bullets:
        d, k = para("body", bl, 19.5, x0 + 22, y, maxw - 22, 24, "#cfc19a")
        body.append(diamond(x0 + 6, y - 6, 3.6, "url(#gold)") + d)
        y += k * 24 + 5
    y += 12
    cx = x0
    for t in tags:
        cw = width("cin", t.upper(), 10.5, 1.8) + 30
        body.append(f'<rect x="{cx:.0f}" y="{y:.0f}" width="{cw:.0f}" height="26" rx="13" fill="{GOLD}" fill-opacity=".08" stroke="{GOLD}" stroke-opacity=".55"/>'
                    + txt("cin", t.upper(), 10.5, cx + cw / 2, y + 17.5, "#efd58a", "middle", 1.8))
        cx += cw + 10
    H = int(y + 26 + 34)
    ex, ey = 116, max(H // 2, 128)
    watermark = f'<g transform="translate({W - 150} {H / 2:.0f}) scale(2.4)" opacity=".05">{emblem}</g>'
    return svg(W, H, panel(W, H, 14, 7) + watermark + f'<g transform="translate({ex} {ey})">{emblem}</g>' + "".join(body), defs, f"{title}: {subtitle}. {desc}")


def quest_argus():
    return quest_card("Argus", "AI-Powered Codebase Companion", "IN ACTIVE DEVELOPMENT", "#f0b04a",
                      "An AI companion that helps developers understand and navigate codebases. My flagship build, currently taking shape.",
                      [], ["AI Companion", "Developer Tooling", "In Development"], _eye(), "argus")


def quest_aicalc():
    return quest_card("AICalc", "AI-Powered Visual Calculator", "QUEST COMPLETE · LIVE", "#5fd6a0",
                      "Draw math, physics and chemistry problems on a canvas and receive AI-solved answers rendered in LaTeX. Powered by Gemini 2.5 Flash.",
                      ["Freehand drawing, movable text boxes and step-by-step explanations",
                       "Rotates across N API keys on rate limits, retrying on network errors",
                       "Skips blank-canvas requests and compresses images to 768px to cut API costs",
                       "Token usage tracked locally in the browser"],
                      ["React", "TypeScript", "FastAPI", "Gemini 2.5 Flash", "LaTeX"], _abacus(), "aicalc")


# ------------------------------------------------------------------- feats
def feats():
    W, H = 900, 360
    data = [("2026", "Goldman Sachs India Hackathon", "Advanced to the Interview Round", "crimson", ("#a12a40", "#4b0e1a")),
            ("2025", "Google Agentic AI Day Hackathon", "Invited On-site · BIEC Bengaluru", "sapphire", ("#2f5aa8", "#0e2148")),
            ("2025·26", "Tic Tech Toe Hackathon", "On Campus · DAU", "emerald", ("#23886a", "#0b3a2c"))]
    defs = '<linearGradient id="wood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d9a466"/><stop offset=".5" stop-color="#8b5a2b"/><stop offset="1" stop-color="#4a2c12"/></linearGradient>'
    for _, _, _, nm, (c1, c2) in data:
        defs += f'<linearGradient id="{nm}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>'
    b = ['<rect x="26" y="20" width="848" height="14" rx="7" fill="url(#wood)" stroke="#2a1808"/>']
    for x in (26, 874):
        b.append(f'<circle cx="{x}" cy="27" r="13" fill="url(#gold)" stroke="#6b4c10"/>')
    for i, (year, ev, res, nm, _) in enumerate(data):
        cx = 160 + i * 290
        x0, x1 = cx - 118, cx + 118
        pen = f"M{x0} 34H{x1}V258Q{x1} 300 {cx} 326Q{x0} 300 {x0} 258Z"
        g = [f'<path d="{pen}" fill="url(#{nm})" stroke="url(#goldH)" stroke-width="2.4"/>',
             f'<g transform="translate({cx} 180) scale(.93) translate({-cx} -180)"><path d="{pen}" fill="none" stroke="{GOLD}" stroke-opacity=".45"/></g>',
             f'<circle cx="{cx}" cy="92" r="35" fill="url(#glowGold)">{pulse(lo=.3, hi=.75, dur=3.6, begin=i)}</circle>',
             f'<circle cx="{cx}" cy="92" r="31" fill="#0b1020" stroke="url(#gold)" stroke-width="2.2"/><circle cx="{cx}" cy="92" r="26" fill="none" stroke="{GOLD}" stroke-opacity=".4" stroke-dasharray="2 3"/>',
             txt("deco", year, fit("deco", year, 19, 46, 0), cx, 99, "url(#gold)", "middle")]
        y = 158
        for ln in wrap("cinb", ev.upper(), 13.5, 196, 1.2):
            g.append(txt("cinb", ln, 13.5, cx, y, PARCH, "middle", 1.2))
            y += 20
        g.append(orn(cx, y - 3, 70))
        y += 22
        d, _n2 = para("ital", res, 20.5, cx, y, 190, 22, "#ffe79a", "middle")
        g.append(d)
        for px in (x0 + 26, x1 - 26):
            g.append(f'<circle cx="{px}" cy="34" r="4" fill="url(#gold)" stroke="#6b4c10" stroke-width=".6"/>')
        b.append(f'<g><animateTransform attributeName="transform" type="rotate" values="-1.4 {cx} 30;1.4 {cx} 30;-1.4 {cx} 30" dur="{5.5 + i * 1.1:.1f}s" begin="-{i * 1.7:.1f}s" repeatCount="indefinite" {SPLINE}/>{"".join(g)}</g>')
    return svg(W, H, "".join(b), defs, "Feats: Goldman Sachs India Hackathon 2026 (interview round), Google Agentic AI Day Hackathon 2025 (invited on-site, BIEC Bengaluru), Tic Tech Toe Hackathon 2025 and 2026 (on campus, DAU)")


# ----------------------------------------------------------------- buttons
def _btn_icon(kind, cx, cy):
    if kind == "github":
        return icon("github", cx, cy, 20, "url(#gold)")
    if kind == "mail":
        return (f'<g transform="translate({cx} {cy})" fill="none" stroke="url(#gold)" stroke-width="1.8" stroke-linejoin="round">'
                '<rect x="-10" y="-7" width="20" height="14" rx="2.5"/><path d="M-10 -6L0 2L10 -6"/></g>')
    if kind == "in":
        return txt("deco", "in", 17, cx, cy + 6, "url(#gold)", "middle")
    return (f'<g transform="translate({cx} {cy})"><circle r="10.5" fill="none" stroke="url(#gold)" stroke-width="1.6" stroke-dasharray="2.4 2.6"/>'
            '<path d="M0 -8Q0 0 8 0Q0 0 0 8Q0 0 -8 0Q0 0 0 -8Z" fill="url(#gold)"/></g>')


def button(label, kind, w=250):
    H = 58
    defs = shine("bs", 20, w - 20, 3.6, 120, 1)
    b = [f'<rect x="1.5" y="1.5" width="{w - 3}" height="{H - 3}" rx="12" fill="url(#stone)"/>',
         f'<rect x="1.5" y="1.5" width="{w - 3}" height="{H - 3}" rx="12" fill="none" stroke="url(#goldH)" stroke-width="2"/>',
         f'<rect x="1.5" y="1.5" width="{w - 3}" height="{H - 3}" rx="12" fill="none" stroke="url(#bs)" stroke-width="2.4"/>',
         f'<rect x="6.5" y="6.5" width="{w - 13}" height="{H - 13}" rx="8" fill="none" stroke="{GOLD}" stroke-opacity=".2"/>',
         f'<circle cx="36" cy="{H / 2}" r="17" fill="#0b1020" stroke="{GOLD}" stroke-opacity=".6"/>',
         _btn_icon(kind, 36, H / 2),
         diamond(w - 24, H / 2, 3.4, GOLD, pulse(dur=2.2)),
         txt("cinb", label, fit("cinb", label, 14.5, w - 122, 2), (62 + w - 40) / 2, H / 2 + 5, "#f4e2a4", "middle", 2)]
    return svg(w, H, "".join(b), defs, label)


# ------------------------------------------------------------------ footer
def footer():
    W, H = 1200, 388
    rng = random.Random(21)
    defs = ("""
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#03050b"/><stop offset=".55" stop-color="#0d1738"/><stop offset="1" stop-color="#2a2c50"/></linearGradient>
<radialGradient id="horizon"><stop offset="0" stop-color="#e8b34a" stop-opacity=".36"/><stop offset="1" stop-color="#e8b34a" stop-opacity="0"/></radialGradient>
<linearGradient id="m1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#26355f"/><stop offset="1" stop-color="#131c3a"/></linearGradient>
<linearGradient id="m2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#172344"/><stop offset="1" stop-color="#0b1228"/></linearGradient>
<radialGradient id="scrim"><stop offset="0" stop-color="#03050b" stop-opacity=".75"/><stop offset="1" stop-color="#03050b" stop-opacity="0"/></radialGradient>
""" + shine("fg", 250, 950, 6.5, 300))
    r1, r1t = ridge(rng, W, H, 262, 120, .58)
    r2, r2t = ridge(rng, W, H, 308, 90, .55)
    r3, _ = ridge(rng, W, H, 350, 46, .5)
    b = [f'<rect width="{W}" height="{H}" fill="url(#sky)"/>',
         f'<ellipse cx="600" cy="250" rx="700" ry="180" fill="url(#horizon)"><animate attributeName="opacity" values=".7;1;.7" dur="9s" repeatCount="indefinite"/></ellipse>',
         stars(rng, 80, W, 190), moon(170, 70, 24),
         f'<path d="{r1}" fill="url(#m1)"/><path d="{r1t}" fill="none" stroke="#3a4d82" stroke-opacity=".5"/>',
         f'<path d="{r2}" fill="url(#m2)"/>',
         '<path d="M300 400Q600 190 900 400Z" fill="#0a1128"/>',
         citadel(600, 268, .9, seed=9)]
    for i, (cx, cy, rx, ry, dur) in enumerate([(300, 290, 340, 22, 28), (900, 300, 360, 20, 34)]):
        b.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#9db4e0" opacity=".1" filter="url(#b16)"><animateTransform attributeName="transform" type="translate" values="-70 0;70 0;-70 0" dur="{dur}s" begin="-{i * 9}s" repeatCount="indefinite"/></ellipse>')
    b += [f'<path d="{r3}" fill="#080d1b"/>',
          pines(rng, W, H + 4, 44, 40, 90, "#070c19"),
          f'<g>{pines(rng, 300, H + 4, 14, 80, 150, "#03060c")}</g>',
          f'<g transform="translate(900 0)">{pines(rng, 300, H + 4, 14, 80, 150, "#03060c")}</g>',
          fireflies(rng, 12, 60, 1140, 200, 340),
          brazier(80, H - 6, 1.0, 31), brazier(1120, H - 6, 1.0, 32),
          '<ellipse cx="600" cy="332" rx="480" ry="70" fill="url(#scrim)"/>',
          gold_text("deco", "FAREWELL, TRAVELER", 30, 600, 318, "fg", "middle", 5),
          txt("ital", "May your builds be green and your merges swift.", 25, 600, 350, "#dbe4f7", "middle"),
          txt("cin", "FORGED BY TANISHQ SHAH  ·  ANNO MMXXVI", 11.5, 600, 375, "#8092b8", "middle", 4),
          f'<rect y="0" width="{W}" height="2" fill="url(#goldH)"/>']
    return svg(W, H, "".join(b), defs, "Farewell, traveler. May your builds be green and your merges swift.")
