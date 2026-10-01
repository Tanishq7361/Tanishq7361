"""
medieval.py - tiny SVG toolkit for the profile README.

Every piece of lettering is converted to vector outlines with fontTools, so the
SVGs look identical everywhere (GitHub blocks external fonts inside images).
Fonts live in scripts/fonts and are licensed under the SIL Open Font License.
"""
import json
import math
import os
import random

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))

FONT_FILES = {
    "deco": "cinzel-decorative-latin-900-normal.woff",   # titles
    "decob": "cinzel-decorative-latin-700-normal.woff",
    "cin": "cinzel-latin-600-normal.woff",               # labels, small caps
    "cinb": "cinzel-latin-700-normal.woff",
    "body": "cormorant-garamond-latin-600-normal.woff",  # prose
    "ital": "cormorant-garamond-latin-600-italic.woff",
}
_FONTS = {}


def _font(key):
    if key not in _FONTS:
        f = TTFont(os.path.join(HERE, "fonts", FONT_FILES[key]))
        _FONTS[key] = (f.getGlyphSet(), f.getBestCmap(), f["head"].unitsPerEm)
    return _FONTS[key]


def _n(v):
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


def _glyph(cm, ch):
    return cm.get(ord(ch)) or cm.get(32)


def width(fk, text, size, ls=0.0):
    gs, cm, upm = _font(fk)
    s = size / upm
    if not text:
        return 0.0
    return sum(gs[_glyph(cm, c)].width * s + ls for c in text) - ls


_REG = {}   # glyph outlines shared by every flat-coloured <use> in the current SVG


def _flat(fill):
    return not fill.startswith("url(")


def txt(fk, text, size, x, y, fill, anchor="start", ls=0.0, extra=""):
    """Lettering as vectors. y is the baseline.

    Flat colours re-use one outline per glyph through <use> (small files);
    gradient fills are emitted as a single <path> so the gradient stays in page space.
    """
    gs, cm, upm = _font(fk)
    s = size / upm
    w = width(fk, text, size, ls)
    cx = x - (w if anchor == "end" else w / 2 if anchor == "middle" else 0)
    if _flat(fill):
        uses = []
        for ch in text:
            g = _glyph(cm, ch)
            gid = f"{fk}-{ord(ch):x}"
            if gid not in _REG:
                p = SVGPathPen(gs, ntos=lambda v: str(int(round(v))))
                gs[g].draw(p)
                _REG[gid] = p.getCommands()
            if _REG[gid]:
                uses.append(f'<use href="#{gid}" transform="translate({_n(cx)} {_n(y)}) scale({s:.4f} {-s:.4f})"/>')
            cx += gs[g].width * s + ls
        return f'<g fill="{fill}" {extra}>{"".join(uses)}</g>' if uses else ""
    pen = SVGPathPen(gs, ntos=_n)
    for ch in text:
        g = _glyph(cm, ch)
        gs[g].draw(TransformPen(pen, (s, 0, 0, -s, cx, y)))
        cx += gs[g].width * s + ls
    d = pen.getCommands()
    return f'<path d="{d}" fill="{fill}" {extra}/>' if d else ""


def wrap(fk, text, size, maxw, ls=0.0):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if cur and width(fk, trial, size, ls) > maxw:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def para(fk, text, size, x, y, maxw, lh, fill, anchor="start", ls=0.0):
    out, lines = [], wrap(fk, text, size, maxw, ls)
    for i, ln in enumerate(lines):
        out.append(txt(fk, ln, size, x, y + i * lh, fill, anchor, ls))
    return "".join(out), len(lines)


def fit(fk, text, size, maxw, ls=0.0):
    w = width(fk, text, size, ls)
    return size if w <= maxw else size * maxw / w


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;")


ICONS = json.load(open(os.path.join(HERE, "icons.json")))

# ------------------------------------------------------------------ palette
GOLD = "#d9b13b"
GOLD_HI = "#f7dc7a"
GOLD_LO = "#8a6d1f"
SILVER = "#b9c6de"
PARCH = "#e6d3a3"
INK = "#2b1d0e"

COMMON = """
<linearGradient id="gold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff1b8"/><stop offset=".45" stop-color="#e2b93b"/><stop offset="1" stop-color="#8a6d1f"/></linearGradient>
<linearGradient id="goldH" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8a6d1f"/><stop offset=".5" stop-color="#f7dc7a"/><stop offset="1" stop-color="#8a6d1f"/></linearGradient>
<linearGradient id="fadeL" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#d9b13b" stop-opacity="0"/><stop offset="1" stop-color="#f0cb5a"/></linearGradient>
<linearGradient id="fadeR" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#f0cb5a"/><stop offset="1" stop-color="#d9b13b" stop-opacity="0"/></linearGradient>
<linearGradient id="silver" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4f7ff"/><stop offset=".5" stop-color="#aebbd6"/><stop offset="1" stop-color="#6b7896"/></linearGradient>
<linearGradient id="stone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#151d33"/><stop offset="1" stop-color="#0a0f1d"/></linearGradient>
<radialGradient id="glowGold"><stop offset="0" stop-color="#ffd97a" stop-opacity=".65"/><stop offset="1" stop-color="#ffd97a" stop-opacity="0"/></radialGradient>
<radialGradient id="glowFire"><stop offset="0" stop-color="#ff9a2e" stop-opacity=".55"/><stop offset="1" stop-color="#ff9a2e" stop-opacity="0"/></radialGradient>
<filter id="b3" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="3"/></filter>
<filter id="b8" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="8"/></filter>
<filter id="b16" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="16"/></filter>
"""


def svg(w, h, body, defs="", title=""):
    glyphs = "".join(f'<path id="{i}" d="{d}"/>' for i, d in _REG.items())
    _REG.clear()
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="{esc(title)}"><title>{esc(title)}</title>'
        f"<defs>{COMMON}{defs}{glyphs}</defs>{body}</svg>"
    )


def shimmer(gid, x0, x1, dur=5.0, span=260):
    """Gold gradient whose bright band sweeps from x0 to x1 forever."""
    return (
        f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x0 - span}" y1="0" x2="{x0}" y2="0">'
        '<stop offset="0" stop-color="#b8892a"/><stop offset=".38" stop-color="#f0c94f"/>'
        '<stop offset=".5" stop-color="#fffbe6"/><stop offset=".62" stop-color="#f0c94f"/>'
        '<stop offset="1" stop-color="#b8892a"/>'
        f'<animate attributeName="x1" values="{x0 - span};{x1}" dur="{dur}s" repeatCount="indefinite"/>'
        f'<animate attributeName="x2" values="{x0};{x1 + span}" dur="{dur}s" repeatCount="indefinite"/>'
        "</linearGradient>"
    )


def shine(gid, x0, x1, dur=5.0, span=220, peak=.85):
    """A soft white band that sweeps across gold lettering (overlay layer)."""
    return (
        f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x0 - span}" y1="0" x2="{x0}" y2="0">'
        f'<stop offset="0" stop-color="#fffbe6" stop-opacity="0"/><stop offset=".5" stop-color="#fffbe6" stop-opacity="{peak}"/>'
        '<stop offset="1" stop-color="#fffbe6" stop-opacity="0"/>'
        f'<animate attributeName="x1" values="{x0 - span};{x1}" dur="{dur}s" repeatCount="indefinite"/>'
        f'<animate attributeName="x2" values="{x0};{x1 + span}" dur="{dur}s" repeatCount="indefinite"/>'
        "</linearGradient>"
    )


def gold_text(fk, text, size, x, y, gid, anchor="start", ls=0.0, shadow=True, extra=""):
    """Embossed gold lettering: drop shadow, vertical gold, travelling shine."""
    out = []
    if shadow:
        out.append(txt(fk, text, size, x, y + 2.2, "#000", anchor, ls, 'opacity=".55"'))
    out.append(txt(fk, text, size, x, y, "url(#gold)", anchor, ls, extra))
    out.append(txt(fk, text, size, x, y, f"url(#{gid})", anchor, ls))
    return "".join(out)


# --------------------------------------------------------------- primitives
def diamond(cx, cy, r, fill, extra=""):
    d = f"M{_n(cx)} {_n(cy - r)}L{_n(cx + r)} {_n(cy)}L{_n(cx)} {_n(cy + r)}L{_n(cx - r)} {_n(cy)}Z"
    if extra.startswith("<"):  # animation children
        return f'<path d="{d}" fill="{fill}">{extra}</path>'
    return f'<path d="{d}" fill="{fill}" {extra}/>'


def pulse(attr="opacity", lo=0.5, hi=1.0, dur=3.0, begin=0.0):
    return (
        f'<animate attributeName="{attr}" values="{lo};{hi};{lo}" dur="{dur}s" '
        f'begin="-{begin:.1f}s" repeatCount="indefinite"/>'
    )


def orn(cx, y, half, col=GOLD):
    """Horizontal ornament: fading rules, a jewel and two studs."""
    return (
        f'<rect x="{cx - half}" y="{y - .6}" width="{half - 26}" height="1.2" fill="url(#fadeL)"/>'
        f'<rect x="{cx + 26}" y="{y - .6}" width="{half - 26}" height="1.2" fill="url(#fadeR)"/>'
        + diamond(cx, y, 7, "url(#gold)")
        + diamond(cx - 17, y, 3, col)
        + diamond(cx + 17, y, 3, col)
        + f'<circle cx="{cx - 27}" cy="{y}" r="1.5" fill="{col}"/><circle cx="{cx + 27}" cy="{y}" r="1.5" fill="{col}"/>'
    )


def sword(x, y, rot=0, scale=1.0, blade="url(#silver)"):
    return (
        f'<g transform="translate({x} {y}) rotate({rot}) scale({scale})">'
        f'<path d="M0 -34L3.4 -27V3H-3.4V-27Z" fill="{blade}"/>'
        '<path d="M0 -34V3" stroke="#57627e" stroke-width=".6"/>'
        '<rect x="-11" y="3" width="22" height="3.6" rx="1.6" fill="url(#gold)"/>'
        '<rect x="-1.7" y="6.6" width="3.4" height="11" fill="#6a4a1c"/>'
        '<circle cx="0" cy="20" r="3" fill="url(#gold)"/></g>'
    )


def shield_path(w=90, h=104):
    return (
        f"M{w / 2} 0L{w - 2} {h * .115}V{h * .5}C{w - 2} {h * .75} {w * .76} {h * .92} {w / 2} {h}"
        f"C{w * .24} {h * .92} 2 {h * .75} 2 {h * .5}V{h * .115}Z"
    )


def corner(x, y, sx, sy, col=GOLD):
    return (
        f'<g transform="translate({x} {y}) scale({sx} {sy})" fill="none" stroke="{col}" stroke-width="1.4" stroke-linecap="round">'
        '<path d="M0 22V6Q0 0 6 0H22"/><path d="M7 22V11Q7 7 11 7H22" opacity=".55"/>'
        f'<circle cx="3.2" cy="3.2" r="1.7" fill="{col}" stroke="none"/></g>'
    )


def panel(w, h, r=10, inset=7):
    """Dark stone plaque with a double gold rule and corner brackets."""
    return (
        f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="{r}" fill="url(#stone)" stroke="url(#goldH)" stroke-width="1.6"/>'
        f'<rect x="{1 + inset}" y="{1 + inset}" width="{w - 2 - 2 * inset}" height="{h - 2 - 2 * inset}" rx="{r - 3}" fill="none" stroke="{GOLD}" stroke-opacity=".28"/>'
        + corner(10, 10, 1, 1) + corner(w - 10, 10, -1, 1)
        + corner(10, h - 10, 1, -1) + corner(w - 10, h - 10, -1, -1)
    )


def icon(name, cx, cy, size, fill="url(#gold)"):
    d = ICONS.get(name)
    if not d:
        return ""
    s = size / 24
    return f'<path transform="translate({_n(cx - size / 2)} {_n(cy - size / 2)}) scale({s:.3f})" d="{d}" fill="{fill}"/>'


# -------------------------------------------------------------- scene parts
def stars(rng, n, w, h, y0=0):
    out = []
    for _ in range(n):
        x, y = rng.uniform(0, w), rng.uniform(y0, h)
        r = rng.choice([.5, .6, .8, 1.0, 1.3, 1.7])
        o = rng.uniform(.35, .95)
        dur, b = rng.uniform(2.5, 7), rng.uniform(0, 6)
        out.append(
            f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fff8e1" opacity="{o:.2f}">'
            f'<animate attributeName="opacity" values="{o:.2f};{o * .2:.2f};{o:.2f}" dur="{dur:.1f}s" begin="-{b:.1f}s" repeatCount="indefinite"/></circle>'
        )
    for _ in range(max(3, n // 14)):  # four-point sparkles
        x, y = rng.uniform(0, w), rng.uniform(y0, h * .8)
        s, b = rng.uniform(4, 8), rng.uniform(0, 5)
        out.append(
            f'<path transform="translate({x:.0f} {y:.0f})" d="M0 -{s:.1f}Q0 0 {s:.1f} 0Q0 0 0 {s:.1f}Q0 0 -{s:.1f} 0Q0 0 0 -{s:.1f}Z" fill="#fff4cf">'
            f'<animate attributeName="opacity" values="1;.15;1" dur="{rng.uniform(3, 6):.1f}s" begin="-{b:.1f}s" repeatCount="indefinite"/></path>'
        )
    return "".join(out)


def ridge(rng, w, h, valley, amp, rough=.56, n=256):
    pts = [0.0] * (n + 1)
    pts[0], pts[n] = rng.uniform(-1, 1), rng.uniform(-1, 1)
    disp, seg = 1.0, n
    while seg > 1:
        half = seg // 2
        for i in range(half, n, seg):
            pts[i] = (pts[i - half] + pts[i + half]) / 2 + rng.uniform(-disp, disp)
        disp *= rough
        seg = half
    lo, hi = min(pts), max(pts)
    ys = [valley - amp * (p - lo) / (hi - lo) for p in pts]
    top = "".join(f"{'M' if i == 0 else 'L'}{_n(i * w / n)} {_n(y)}" for i, y in enumerate(ys))
    return top + f"L{w} {h}L0 {h}Z", top


def pines(rng, w, base, n, hmin, hmax, fill, lit=None):
    d = []
    for _ in range(n):
        x, h = rng.uniform(-10, w + 10), rng.uniform(hmin, hmax)
        top = base - h
        w1, w2, w3 = .17 * h, .27 * h, .36 * h
        y1, y2 = top + .34 * h, top + .64 * h
        d.append(
            f"M{_n(x)} {_n(top)}L{_n(x + w1)} {_n(y1)}L{_n(x + w1 * .45)} {_n(y1)}L{_n(x + w2)} {_n(y2)}"
            f"L{_n(x + w2 * .45)} {_n(y2)}L{_n(x + w3)} {_n(base)}L{_n(x - w3)} {_n(base)}"
            f"L{_n(x - w2 * .45)} {_n(y2)}L{_n(x - w2)} {_n(y2)}L{_n(x - w1 * .45)} {_n(y1)}L{_n(x - w1)} {_n(y1)}Z"
        )
    return f'<path d="{"".join(d)}" fill="{fill}"/>'


def citadel(x, y, s=1.0, fill="#060a14", rim="#1b2745", windows=True, beacon=True, seed=1):
    """A little fortress silhouette standing on (x, y)."""
    rng = random.Random(seed)
    shapes = [
        # curtain wall
        "M-124 0V-36H124V0Z",
        # keep + roof
        "M-19 0V-104H19V0Z", "M-24 -104L0 -156L24 -104Z",
        # left / right towers
        "M-74 0V-74H-46V0Z", "M-78 -74L-60 -112L-42 -74Z",
        "M46 0V-88H76V0Z", "M42 -88L61 -130L80 -88Z",
        # outer turrets
        "M-124 0V-58H-104V0Z", "M-128 -58L-114 -84L-100 -58Z",
        "M104 0V-52H124V0Z", "M100 -52L114 -78L128 -52Z",
    ]
    cren = "".join(f"M{i} -36V-43H{i + 6}V-36Z" for i in range(-118, 118, 12))
    d = "".join(shapes) + cren
    out = [f'<g transform="translate({x} {y}) scale({s})">',
           f'<path d="{d}" fill="{fill}" stroke="{rim}" stroke-width=".8"/>',
           f'<path d="M0 -156V-176" stroke="{fill}" stroke-width="1.6"/><path d="M0 -176L16 -171L0 -166Z" fill="#7a1f2b"/>']
    if windows:
        spots = [(-62, -50), (-62, -30), (61, -64), (61, -40), (-8, -84), (4, -84), (-6, -60), (6, -60),
                 (-114, -40), (114, -34), (-30, -22), (30, -22)]
        for wx, wy in spots:
            b, dur = rng.uniform(0, 4), rng.uniform(2, 5)
            out.append(
                f'<rect x="{wx - 2}" y="{wy - 4}" width="4" height="8" rx="1.5" fill="#ffcf5a">'
                f'<animate attributeName="opacity" values="1;.35;.9;.5;1" dur="{dur:.1f}s" begin="-{b:.1f}s" repeatCount="indefinite"/></rect>'
            )
        out.append('<path d="M-9 0V-14A9 9 0 0 1 9 -14V0Z" fill="#ffcf5a" opacity=".9">'
                   '<animate attributeName="opacity" values=".9;.55;.9" dur="2.6s" repeatCount="indefinite"/></path>')
    if beacon:
        out.append('<circle cx="0" cy="-160" r="34" fill="url(#glowGold)">'
                   '<animate attributeName="r" values="26;42;26" dur="4s" repeatCount="indefinite"/></circle>'
                   '<circle cx="0" cy="-160" r="3" fill="#fff2b8"/>')
    out.append("</g>")
    return "".join(out)


FLAME = "M0 0C-20 0-22-22-10-36C-6-28-2-26-2-34C0-46 6-52 4-66C16-52 24-34 20-16C18-6 10 0 0 0Z"


def brazier(x, y, s=1.0, seed=3, embers=14):
    rng = random.Random(seed)
    out = [f'<g transform="translate({x} {y}) scale({s})">',
           '<circle cx="0" cy="-70" r="86" fill="url(#glowFire)"><animate attributeName="opacity" values=".75;1;.6;.95;.75" dur="1.7s" repeatCount="indefinite"/></circle>',
           # pedestal + bowl
           '<path d="M-9 0L-6 -34H6L9 0Z" fill="#0b0f1b" stroke="#2a3556" stroke-width=".8"/>',
           '<path d="M-24 0H24L18 -6H-18Z" fill="#0b0f1b" stroke="#2a3556" stroke-width=".8"/>',
           '<path d="M-26 -38H26Q22 -18 0 -16Q-22 -18 -26 -38Z" fill="#0d1220" stroke="url(#goldH)" stroke-width="1.4"/>',
           '<g transform="translate(0 -38)">',
           f'<g><animateTransform attributeName="transform" type="scale" values="1 1;1.07 .92;.95 1.1;1.03 .96;1 1" dur="1.15s" repeatCount="indefinite"/>'
           f'<path d="{FLAME}" fill="#ff7a1a"/>'
           f'<g transform="scale(.72)"><path d="{FLAME}" fill="#ffb92e"/></g>'
           f'<g transform="scale(.42)"><path d="{FLAME}" fill="#fff0a8"/></g></g></g>']
    for _ in range(embers):
        ex, dur, b = rng.uniform(-14, 14), rng.uniform(2.2, 4.6), rng.uniform(0, 4)
        rise = rng.uniform(90, 200)
        out.append(
            f'<circle cx="{ex:.1f}" cy="-46" r="{rng.uniform(.8, 1.8):.1f}" fill="#ffb347">'
            f'<animate attributeName="cy" values="-46;{-46 - rise:.0f}" dur="{dur:.1f}s" begin="-{b:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="cx" values="{ex:.1f};{ex + rng.uniform(-26, 26):.1f}" dur="{dur:.1f}s" begin="-{b:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;1;0" dur="{dur:.1f}s" begin="-{b:.1f}s" repeatCount="indefinite"/></circle>'
        )
    out.append("</g>")
    return "".join(out)


def fireflies(rng, n, x0, x1, y0, y1):
    out = []
    for _ in range(n):
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        dx, dy = rng.uniform(50, 130), rng.uniform(14, 40)
        dur, b = rng.uniform(12, 26), rng.uniform(0, 20)
        path = f"M0 0C{dx * .3:.0f} {-dy:.0f} {dx * .7:.0f} {-dy:.0f} {dx:.0f} 0C{dx * .7:.0f} {dy:.0f} {dx * .3:.0f} {dy:.0f} 0 0Z"
        out.append(
            f'<g transform="translate({x:.0f} {y:.0f})"><circle r="9" fill="url(#glowGold)"/><circle r="1.5" fill="#fff0a6"/>'
            f'<animateMotion path="{path}" dur="{dur:.1f}s" begin="-{b:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="1;.15;1" dur="{rng.uniform(2, 4):.1f}s" begin="-{b:.1f}s" repeatCount="indefinite"/></g>'
        )
    return "".join(out)


def moon(cx, cy, r=34):
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{r * 3.2:.0f}" fill="url(#glowGold)" opacity=".28"><animate attributeName="opacity" values=".2;.36;.2" dur="7s" repeatCount="indefinite"/></circle>'
        f'<mask id="cres"><rect x="{cx - r * 2}" y="{cy - r * 2}" width="{r * 4}" height="{r * 4}" fill="#fff"/>'
        f'<circle cx="{cx + r * .42:.0f}" cy="{cy - r * .2:.0f}" r="{r * .88:.0f}" fill="#000"/></mask>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#f6efd6" mask="url(#cres)"/>'
    )
