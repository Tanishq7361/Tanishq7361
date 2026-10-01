"""
cyber.py - Cyberpunk & Sci-Fi HUD visual primitives and SVG generator.
Combines vector font outlines with high-action sci-fi HUD styling,
neon glows, animated laser scanlines, radar sweeps, and cyber grids.
"""
import math
import os
import random
from medieval import txt, width, fit, wrap, para, esc, _font, _n, _glyph, _REG, ICONS

# ------------------------------------------------------------------ palette
CYAN = "#00f0ff"
CYAN_DIM = "#0088aa"
CYAN_GLOW = "#38f8ff"
MAGENTA = "#ff007f"
PURPLE = "#9d00ff"
NEON_GREEN = "#00ff9d"
AMBER = "#fcee0a"
DARK_BG = "#040711"
PANEL_BG = "#080e1c"
PANEL_BORDER = "#142442"
TEXT_MAIN = "#e6f6ff"
TEXT_MUTED = "#7898ba"

CYBER_DEFS = """
<linearGradient id="cyberSky" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#02040a"/>
  <stop offset=".4" stop-color="#060b18"/>
  <stop offset=".8" stop-color="#0a152e"/>
  <stop offset="1" stop-color="#121026"/>
</linearGradient>

<linearGradient id="neonCyan" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#00c8ff"/>
  <stop offset=".5" stop-color="#00f0ff"/>
  <stop offset="1" stop-color="#70f8ff"/>
</linearGradient>

<linearGradient id="neonMagenta" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#ff0055"/>
  <stop offset=".5" stop-color="#ff00a0"/>
  <stop offset="1" stop-color="#bf00ff"/>
</linearGradient>

<linearGradient id="cyberLaser" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#00f0ff" stop-opacity="0"/>
  <stop offset=".15" stop-color="#00f0ff" stop-opacity=".8"/>
  <stop offset=".5" stop-color="#ffffff" stop-opacity="1"/>
  <stop offset=".85" stop-color="#ff007f" stop-opacity=".8"/>
  <stop offset="1" stop-color="#ff007f" stop-opacity="0"/>
</linearGradient>

<linearGradient id="scanBeam" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#00f0ff" stop-opacity="0"/>
  <stop offset=".8" stop-color="#00f0ff" stop-opacity=".15"/>
  <stop offset="1" stop-color="#00f0ff" stop-opacity=".85"/>
</linearGradient>

<linearGradient id="cyberCardBg" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#091224" stop-opacity=".96"/>
  <stop offset="1" stop-color="#050a16" stop-opacity=".98"/>
</linearGradient>

<pattern id="cyberGrid" width="30" height="30" patternUnits="userSpaceOnUse">
  <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#00f0ff" stroke-width=".7" stroke-opacity=".08"/>
</pattern>

<pattern id="hexGrid" width="28" height="48.5" patternUnits="userSpaceOnUse">
  <path d="M14 0L28 8.08V24.25L14 32.33L0 24.25V8.08Z M0 48.5L14 40.42L28 48.5" fill="none" stroke="#00f0ff" stroke-width=".6" stroke-opacity=".06"/>
</pattern>

<filter id="glowCyan" x="-40%" y="-40%" width="180%" height="180%">
  <feGaussianBlur stdDeviation="3.5" result="blur"/>
  <feMerge>
    <feMergeNode in="blur"/>
    <feMergeNode in="SourceGraphic"/>
  </feMerge>
</filter>

<filter id="glowMagenta" x="-40%" y="-40%" width="180%" height="180%">
  <feGaussianBlur stdDeviation="3.5" result="blur"/>
  <feMerge>
    <feMergeNode in="blur"/>
    <feMergeNode in="SourceGraphic"/>
  </feMerge>
</filter>

<filter id="laserBlur" x="-20%" y="-20%" width="140%" height="140%">
  <feGaussianBlur stdDeviation="5"/>
</filter>
"""


def cyber_svg(w, h, body, defs="", title=""):
    """Assemble final SVG with cyber defs and vector font glyphs."""
    glyphs = "".join(f'<path id="{i}" d="{d}"/>' for i, d in _REG.items())
    _REG.clear()
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="{esc(title)}"><title>{esc(title)}</title>'
        f"<defs>{CYBER_DEFS}{defs}{glyphs}</defs>{body}</svg>"
    )


def cyber_panel(w, h, ch=16, stroke=CYAN, fill="url(#cyberCardBg)", stroke_w=1.2, grid=True):
    """Futuristic chamfered cyber container with tech brackets and grid."""
    p = [
        f'<polygon points="{ch},0 {w-ch},0 {w},{ch} {w},{h-ch} {w-ch},{h} {ch},{h} 0,{h-ch} 0,{ch}" '
        f'fill="{fill}" stroke="{PANEL_BORDER}" stroke-width="{stroke_w}"/>'
    ]
    if grid:
        p.append(
            f'<polygon points="{ch+2},2 {w-ch-2},2 {w-2},{ch+2} {w-2},{h-ch-2} {w-ch-2},{h-2} {ch+2},{h-2} 2,{h-ch-2} 2,{ch+2}" '
            f'fill="url(#cyberGrid)" opacity=".7"/>'
        )
    # Corner brackets (HUD accents)
    bw = min(28, w // 8)
    bh = min(24, h // 8)
    # Top-Left
    p.append(f'<path d="M 0,{bh} L 0,{ch} L {ch},0 L {bw},0" fill="none" stroke="{stroke}" stroke-width="2.2"/>')
    # Top-Right
    p.append(f'<path d="M {w-bw},0 L {w-ch},0 L {w},{ch} L {w},{bh}" fill="none" stroke="{stroke}" stroke-width="2.2"/>')
    # Bottom-Right
    p.append(f'<path d="M {w},{h-bh} L {w},{h-ch} L {w-ch},{h} L {w-bw},{h}" fill="none" stroke="{MAGENTA}" stroke-width="2.2"/>')
    # Bottom-Left
    p.append(f'<path d="M {bw},{h} L {ch},{h} L 0,{h-ch} L 0,{h-bh}" fill="none" stroke="{MAGENTA}" stroke-width="2.2"/>')
    
    # Subtle circuit tick marks
    p.append(f'<line x1="{w//2 - 40}" y1="1" x2="{w//2 + 40}" y2="1" stroke="{stroke}" stroke-width="2" stroke-opacity=".7"/>')
    p.append(f'<circle cx="{w//2 - 44}" cy="1" r="1.5" fill="{stroke}"/>')
    p.append(f'<circle cx="{w//2 + 44}" cy="1" r="1.5" fill="{stroke}"/>')
    return "".join(p)


def scanline(w, h, dur=5.0):
    """Vertical laser scanline passing through the container."""
    return (
        f'<g opacity=".75">'
        f'<line x1="2" y1="0" x2="{w-2}" y2="0" stroke="url(#neonCyan)" stroke-width="1.8" filter="url(#laserBlur)">'
        f'<animate attributeName="y1" values="2;{h-4};2" dur="{dur}s" repeatCount="indefinite"/>'
        f'<animate attributeName="y2" values="2;{h-4};2" dur="{dur}s" repeatCount="indefinite"/>'
        f'</line>'
        f'<line x1="2" y1="0" x2="{w-2}" y2="0" stroke="#fff" stroke-width="1">'
        f'<animate attributeName="y1" values="2;{h-4};2" dur="{dur}s" repeatCount="indefinite"/>'
        f'<animate attributeName="y2" values="2;{h-4};2" dur="{dur}s" repeatCount="indefinite"/>'
        f'</line>'
        f'</g>'
    )


def equalizer(x, y, bars=8, bw=4, maxh=24, gap=3, col=CYAN):
    """Action equalizer audio/frequency bars animating."""
    out = [f'<g transform="translate({x} {y})">']
    random.seed(42)
    for i in range(bars):
        h1 = random.randint(4, maxh // 2)
        h2 = random.randint(maxh // 2, maxh)
        h3 = random.randint(3, maxh)
        dur = round(random.uniform(0.8, 1.4), 2)
        bx = i * (bw + gap)
        out.append(
            f'<rect x="{bx}" y="-{h1}" width="{bw}" height="{h1}" fill="{col}" opacity=".85">'
            f'<animate attributeName="height" values="{h1};{h2};{h3};{h1}" dur="{dur}s" repeatCount="indefinite"/>'
            f'<animate attributeName="y" values="-{h1};-{h2};-{h3};-{h1}" dur="{dur}s" repeatCount="indefinite"/>'
            f'</rect>'
        )
    out.append('</g>')
    return "".join(out)


def reticle(cx, cy, r=32, col=CYAN):
    """Targeting crosshairs & rotating HUD reticle."""
    return (
        f'<g transform="translate({cx} {cy})">'
        f'<circle cx="0" cy="0" r="{r}" fill="none" stroke="{col}" stroke-width="1.2" stroke-opacity=".5" stroke-dasharray="6 8">'
        f'<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="12s" repeatCount="indefinite"/>'
        f'</circle>'
        f'<circle cx="0" cy="0" r="{r * 0.65:.1f}" fill="none" stroke="{MAGENTA}" stroke-width="1.2" stroke-opacity=".6" stroke-dasharray="14 10">'
        f'<animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="8s" repeatCount="indefinite"/>'
        f'</circle>'
        f'<circle cx="0" cy="0" r="3" fill="{col}">'
        f'<animate attributeName="opacity" values=".4;1;.4" dur="1.8s" repeatCount="indefinite"/>'
        f'</circle>'
        f'<line x1="-{r+8}" y1="0" x2="-{r-4}" y2="0" stroke="{col}" stroke-width="1.5"/>'
        f'<line x1="{r-4}" y1="0" x2="{r+8}" y2="0" stroke="{col}" stroke-width="1.5"/>'
        f'<line x1="0" y1="-{r+8}" x2="0" y2="-{r-4}" stroke="{col}" stroke-width="1.5"/>'
        f'<line x1="0" y1="{r-4}" x2="0" y2="{r+8}" stroke="{col}" stroke-width="1.5"/>'
        f'</g>'
    )


def badge(x, y, text, col=CYAN, bg="#0b172a"):
    """Futuristic chamfered badge pill."""
    w = len(text) * 7.5 + 16
    h = 20
    d = f"M 4 0 L {w-4} 0 L {w} 4 L {w} {h-4} L {w-4} {h} L 4 {h} L 0 {h-4} L 0 4 Z"
    return (
        f'<g transform="translate({x} {y})">'
        f'<path d="{d}" fill="{bg}" stroke="{col}" stroke-width="1" stroke-opacity=".8"/>'
        f'<text x="{w/2}" y="14" fill="{col}" font-family="monospace" font-size="10.5" font-weight="bold" text-anchor="middle" letter-spacing="1">{text}</text>'
        f'</g>'
    )
