#!/usr/bin/env python3
"""
comic.py: renders friendly multi-panel comic strips (SVG) with the nine planet characters and "You".

A strip is a list of panels; a panel has an optional caption, 1-3 characters with expressions/poses,
and speech or thought bubbles. See STRIPS in comic_scripts.py and `python3 tools/comic.py --all`.

Characters: Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu, You
Expressions: happy, calm, worried, angry, sly, sleepy, surprised, proud, sad
Poses: stand, point, wave, sit, arms_up, think
"""
import math, textwrap, os, sys, json

INK = "#2b3350"; PAPER = "#fffdf7"; BORDER = "#b8956a"; CAPTION_BG = "#eef1f8"
PAL = {
    "Sun":     dict(body="#f6b26b", dark="#c2410c", light="#fde68a"),
    "Moon":    dict(body="#e5e7eb", dark="#6b7280", light="#f8fafc"),
    "Mars":    dict(body="#f4a6a6", dark="#b91c1c", light="#fecaca"),
    "Mercury": dict(body="#b7d7a8", dark="#15803d", light="#dcfce7"),
    "Jupiter": dict(body="#f9d976", dark="#b45309", light="#fef3c7"),
    "Venus":   dict(body="#f4b6c2", dark="#be185d", light="#fce7f3"),
    "Saturn":  dict(body="#a9c4e2", dark="#1e3a8a", light="#dbeafe"),
    "Rahu":    dict(body="#cbb7e6", dark="#4c1d95", light="#ede9fe"),
    "Ketu":    dict(body="#d8c7ea", dark="#6b21a8", light="#f3e8ff"),
    "You":     dict(body="#fcd9b6", dark="#7c4a24", light="#fff1e6"),
}

def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

# ----------------------------------------------------------------------------- faces
def face(cx, cy, r, expr, dark):
    """Eyes, brows and mouth for a round face of radius r centred at (cx, cy)."""
    e = []
    ex = r*0.38; ey = cy - r*0.12; er = max(2.2, r*0.075)
    if expr == "sleepy":
        e.append(f'<path d="M{cx-ex-er*1.6},{ey} q{er*1.6},{er*1.6} {er*3.2},0" stroke="{dark}" stroke-width="2.2" fill="none" stroke-linecap="round"/>')
        e.append(f'<path d="M{cx+ex-er*1.6},{ey} q{er*1.6},{er*1.6} {er*3.2},0" stroke="{dark}" stroke-width="2.2" fill="none" stroke-linecap="round"/>')
    elif expr == "happy":
        e.append(f'<path d="M{cx-ex-er*1.6},{ey+er} q{er*1.6},-{er*2} {er*3.2},0" stroke="{dark}" stroke-width="2.4" fill="none" stroke-linecap="round"/>')
        e.append(f'<path d="M{cx+ex-er*1.6},{ey+er} q{er*1.6},-{er*2} {er*3.2},0" stroke="{dark}" stroke-width="2.4" fill="none" stroke-linecap="round"/>')
    else:
        rr = er*1.5 if expr == "surprised" else er
        e.append(f'<circle cx="{cx-ex}" cy="{ey}" r="{rr}" fill="{dark}"/><circle cx="{cx+ex}" cy="{ey}" r="{rr}" fill="{dark}"/>')
        e.append(f'<circle cx="{cx-ex+rr*0.4}" cy="{ey-rr*0.4}" r="{rr*0.35}" fill="#fff"/><circle cx="{cx+ex+rr*0.4}" cy="{ey-rr*0.4}" r="{rr*0.35}" fill="#fff"/>')
    # brows
    by = ey - r*0.22
    if expr in ("angry",):
        e.append(f'<line x1="{cx-ex-er*1.8}" y1="{by-3}" x2="{cx-ex+er*1.8}" y2="{by+4}" stroke="{dark}" stroke-width="2.6" stroke-linecap="round"/>')
        e.append(f'<line x1="{cx+ex-er*1.8}" y1="{by+4}" x2="{cx+ex+er*1.8}" y2="{by-3}" stroke="{dark}" stroke-width="2.6" stroke-linecap="round"/>')
    elif expr in ("worried", "sad"):
        e.append(f'<line x1="{cx-ex-er*1.8}" y1="{by+3}" x2="{cx-ex+er*1.8}" y2="{by-3}" stroke="{dark}" stroke-width="2.4" stroke-linecap="round"/>')
        e.append(f'<line x1="{cx+ex-er*1.8}" y1="{by-3}" x2="{cx+ex+er*1.8}" y2="{by+3}" stroke="{dark}" stroke-width="2.4" stroke-linecap="round"/>')
    elif expr == "sly":
        e.append(f'<line x1="{cx-ex-er*1.8}" y1="{by}" x2="{cx-ex+er*1.8}" y2="{by+3}" stroke="{dark}" stroke-width="2.4" stroke-linecap="round"/>')
        e.append(f'<line x1="{cx+ex-er*1.8}" y1="{by-4}" x2="{cx+ex+er*1.8}" y2="{by}" stroke="{dark}" stroke-width="2.4" stroke-linecap="round"/>')
    elif expr == "surprised":
        e.append(f'<path d="M{cx-ex-er*1.8},{by} q{er*1.8},-{er*1.4} {er*3.6},0" stroke="{dark}" stroke-width="2.2" fill="none"/>')
        e.append(f'<path d="M{cx+ex-er*1.8},{by} q{er*1.8},-{er*1.4} {er*3.6},0" stroke="{dark}" stroke-width="2.2" fill="none"/>')
    # mouth
    my = cy + r*0.33; mw = r*0.42
    if expr in ("happy", "proud", "sly"):
        k = 0.9 if expr == "happy" else 0.5
        e.append(f'<path d="M{cx-mw/2},{my} q{mw/2},{mw*k} {mw},0" stroke="{dark}" stroke-width="2.6" fill="none" stroke-linecap="round"/>')
    elif expr in ("worried", "sad"):
        e.append(f'<path d="M{cx-mw/2},{my+4} q{mw/2},-{mw*0.6} {mw},0" stroke="{dark}" stroke-width="2.6" fill="none" stroke-linecap="round"/>')
    elif expr == "angry":
        e.append(f'<line x1="{cx-mw/2}" y1="{my}" x2="{cx+mw/2}" y2="{my}" stroke="{dark}" stroke-width="2.8" stroke-linecap="round"/>')
    elif expr == "surprised":
        e.append(f'<ellipse cx="{cx}" cy="{my}" rx="{mw*0.28}" ry="{mw*0.4}" fill="{dark}"/>')
    elif expr == "sleepy":
        e.append(f'<path d="M{cx-mw/3},{my} q{mw/3},{mw*0.3} {mw*0.66},0" stroke="{dark}" stroke-width="2.2" fill="none" stroke-linecap="round"/>')
    else:  # calm
        e.append(f'<path d="M{cx-mw/2},{my} q{mw/2},{mw*0.35} {mw},0" stroke="{dark}" stroke-width="2.4" fill="none" stroke-linecap="round"/>')
    if expr in ("happy", "proud", "shy"):
        e.append(f'<circle cx="{cx-r*0.55}" cy="{cy+r*0.18}" r="{r*0.09}" fill="#f9a8d4" opacity="0.7"/><circle cx="{cx+r*0.55}" cy="{cy+r*0.18}" r="{r*0.09}" fill="#f9a8d4" opacity="0.7"/>')
    return "".join(e)

def arms(cx, cy, r, pose, dark, flip=False):
    """Two arms as rounded lines; pose decides their direction."""
    s = -1 if flip else 1
    L = r*0.95
    a = []
    def arm(x0, y0, x1, y1):
        a.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" stroke="{dark}" stroke-width="{max(4, r*0.11)}" stroke-linecap="round"/>')
        a.append(f'<circle cx="{x1}" cy="{y1}" r="{max(4, r*0.11)}" fill="{dark}"/>')
    sy = cy + r*0.15
    if pose == "point":
        arm(cx - s*r*0.9, sy, cx - s*r*0.9 - s*L*0.5, sy + L*0.5)
        arm(cx + s*r*0.9, sy, cx + s*r*0.9 + s*L*0.95, sy - L*0.25)
    elif pose == "wave":
        arm(cx - s*r*0.9, sy, cx - s*r*0.9 - s*L*0.5, sy + L*0.5)
        arm(cx + s*r*0.9, sy, cx + s*r*0.9 + s*L*0.55, sy - L*0.9)
    elif pose == "arms_up":
        arm(cx - r*0.9, sy, cx - r*0.9 - L*0.55, sy - L*0.9)
        arm(cx + r*0.9, sy, cx + r*0.9 + L*0.55, sy - L*0.9)
    elif pose == "think":
        arm(cx - s*r*0.9, sy, cx - s*r*0.9 - s*L*0.5, sy + L*0.5)
        arm(cx + s*r*0.9, sy, cx + s*r*0.35, cy + r*0.45)
    elif pose == "sit":
        arm(cx - r*0.9, sy, cx - r*0.6, sy + L*0.75)
        arm(cx + r*0.9, sy, cx + r*0.6, sy + L*0.75)
    else:  # stand
        arm(cx - r*0.9, sy, cx - r*0.9 - L*0.45, sy + L*0.55)
        arm(cx + r*0.9, sy, cx + r*0.9 + L*0.45, sy + L*0.55)
    return "".join(a)

def legs(cx, cy, r, pose, dark):
    if pose == "sit":
        return (f'<path d="M{cx-r*0.9},{cy+r*0.95} q{r*0.4},{r*0.5} {r*0.9},{r*0.35}" stroke="{dark}" stroke-width="{max(4, r*0.11)}" fill="none" stroke-linecap="round"/>'
                f'<path d="M{cx+r*0.9},{cy+r*0.95} q-{r*0.4},{r*0.5} -{r*0.9},{r*0.35}" stroke="{dark}" stroke-width="{max(4, r*0.11)}" fill="none" stroke-linecap="round"/>')
    return (f'<line x1="{cx-r*0.35}" y1="{cy+r*0.95}" x2="{cx-r*0.45}" y2="{cy+r*1.55}" stroke="{dark}" stroke-width="{max(4, r*0.11)}" stroke-linecap="round"/>'
            f'<line x1="{cx+r*0.35}" y1="{cy+r*0.95}" x2="{cx+r*0.45}" y2="{cy+r*1.55}" stroke="{dark}" stroke-width="{max(4, r*0.11)}" stroke-linecap="round"/>'
            f'<ellipse cx="{cx-r*0.5}" cy="{cy+r*1.6}" rx="{r*0.22}" ry="{r*0.1}" fill="{dark}"/><ellipse cx="{cx+r*0.5}" cy="{cy+r*1.6}" rx="{r*0.22}" ry="{r*0.1}" fill="{dark}"/>')

def character(name, cx, cy, r=42, expr="calm", pose="stand", flip=False, label=True):
    """Draws a character whose round body/face is centred at (cx, cy) with radius r."""
    p = PAL[name]; d = p["dark"]; b = p["body"]
    out = []
    out.append(legs(cx, cy, r, pose, d))
    out.append(arms(cx, cy, r, pose, d, flip))
    if name == "Sun":
        for k in range(12):
            a = k*30; x1 = cx + math.cos(math.radians(a))*r*1.15; y1 = cy + math.sin(math.radians(a))*r*1.15
            x2 = cx + math.cos(math.radians(a))*r*1.45; y2 = cy + math.sin(math.radians(a))*r*1.45
            out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{p["light"]}" stroke-width="6" stroke-linecap="round"/>')
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{b}" stroke="{d}" stroke-width="3"/>')
        # crown
        out.append(f'<path d="M{cx-r*0.55},{cy-r*0.85} l{r*0.18},-{r*0.45} l{r*0.2},{r*0.3} l{r*0.17},-{r*0.5} l{r*0.17},{r*0.5} l{r*0.2},-{r*0.3} l{r*0.18},{r*0.45} z" fill="#fde68a" stroke="{d}" stroke-width="2.5"/>')
    elif name == "Moon":
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{b}" stroke="{d}" stroke-width="3"/>')
        out.append(f'<circle cx="{cx+r*0.42}" cy="{cy-r*0.3}" r="{r*0.78}" fill="{PAPER}" opacity="0.0"/>')
        # soft shawl
        out.append(f'<path d="M{cx-r*0.95},{cy-r*0.3} q{r*0.95},-{r*1.1} {r*1.9},0 q-{r*0.95},{r*0.25} -{r*1.9},0 z" fill="#c7d2fe" stroke="{d}" stroke-width="2.5"/>')
        out.append(f'<circle cx="{cx-r*0.3}" cy="{cy+r*0.55}" r="{r*0.07}" fill="{d}" opacity="0.4"/><circle cx="{cx+r*0.45}" cy="{cy+r*0.4}" r="{r*0.05}" fill="{d}" opacity="0.4"/>')
    elif name == "Mars":
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{b}" stroke="{d}" stroke-width="3"/>')
        # helmet with crest
        out.append(f'<path d="M{cx-r*0.85},{cy-r*0.52} a{r*0.85},{r*0.85} 0 0 1 {r*1.7},0 z" fill="#ef4444" stroke="{d}" stroke-width="2.5"/>')
        out.append(f'<path d="M{cx},{cy-r*1.2} q{r*0.5},-{r*0.5} {r*0.9},-{r*0.1}" stroke="{d}" stroke-width="6" fill="none" stroke-linecap="round"/>')
    elif name == "Mercury":
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{b}" stroke="{d}" stroke-width="3"/>')
        # glasses
        out.append(f'<circle cx="{cx-r*0.38}" cy="{cy-r*0.12}" r="{r*0.26}" fill="none" stroke="{d}" stroke-width="2.4"/><circle cx="{cx+r*0.38}" cy="{cy-r*0.12}" r="{r*0.26}" fill="none" stroke="{d}" stroke-width="2.4"/><line x1="{cx-r*0.12}" y1="{cy-r*0.12}" x2="{cx+r*0.12}" y2="{cy-r*0.12}" stroke="{d}" stroke-width="2.4"/>')
        # a little hair tuft
        out.append(f'<path d="M{cx-r*0.2},{cy-r*0.98} q{r*0.2},-{r*0.45} {r*0.5},-{r*0.1}" stroke="{d}" stroke-width="3" fill="none" stroke-linecap="round"/>')
    elif name == "Jupiter":
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r*1.08}" fill="{b}" stroke="{d}" stroke-width="3"/>')
        # scholar's cap and beard
        out.append(f'<rect x="{cx-r*0.7}" y="{cy-r*1.35}" width="{r*1.4}" height="{r*0.45}" rx="6" fill="#b45309" stroke="{d}" stroke-width="2"/>')
        out.append(f'<path d="M{cx-r*0.5},{cy+r*0.55} q{r*0.5},{r*0.7} {r*1.0},0" fill="#fff7ed" stroke="{d}" stroke-width="2"/>')
    elif name == "Venus":
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{b}" stroke="{d}" stroke-width="3"/>')
        # flower in hair
        fx, fy = cx+r*0.62, cy-r*0.72
        for k in range(5):
            a = math.radians(k*72); out.append(f'<circle cx="{fx+math.cos(a)*r*0.16}" cy="{fy+math.sin(a)*r*0.16}" r="{r*0.12}" fill="#fff" stroke="{d}" stroke-width="1.5"/>')
        out.append(f'<circle cx="{fx}" cy="{fy}" r="{r*0.09}" fill="#fde68a"/>')
    elif name == "Saturn":
        out.append(f'<ellipse cx="{cx}" cy="{cy+r*0.1}" rx="{r*1.55}" ry="{r*0.35}" fill="none" stroke="{d}" stroke-width="5" opacity="0.6"/>')
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{b}" stroke="{d}" stroke-width="3"/>')
        out.append(f'<path d="M{cx-r*1.55},{cy+r*0.1} a{r*1.55},{r*0.35} 0 0 0 {r*3.1},0" fill="none" stroke="{d}" stroke-width="5" opacity="0.9"/>')
        # spectacles on a string and a small moustache
        out.append(f'<circle cx="{cx-r*0.38}" cy="{cy-r*0.12}" r="{r*0.22}" fill="none" stroke="{d}" stroke-width="2"/><circle cx="{cx+r*0.38}" cy="{cy-r*0.12}" r="{r*0.22}" fill="none" stroke="{d}" stroke-width="2"/>')
        out.append(f'<path d="M{cx-r*0.28},{cy+r*0.22} q{r*0.28},-{r*0.15} {r*0.56},0" stroke="{d}" stroke-width="3" fill="none" stroke-linecap="round"/>')
    elif name == "Rahu":
        # a smoky head: a cloud of overlapping circles
        out.append(f'<circle cx="{cx-r*0.55}" cy="{cy+r*0.2}" r="{r*0.62}" fill="{b}" stroke="{d}" stroke-width="3"/>')
        out.append(f'<circle cx="{cx+r*0.55}" cy="{cy+r*0.2}" r="{r*0.62}" fill="{b}" stroke="{d}" stroke-width="3"/>')
        out.append(f'<circle cx="{cx}" cy="{cy-r*0.25}" r="{r*0.8}" fill="{b}" stroke="{d}" stroke-width="3"/>')
        out.append(f'<circle cx="{cx-r*0.55}" cy="{cy+r*0.2}" r="{r*0.6}" fill="{b}"/><circle cx="{cx+r*0.55}" cy="{cy+r*0.2}" r="{r*0.6}" fill="{b}"/><circle cx="{cx}" cy="{cy-r*0.25}" r="{r*0.78}" fill="{b}"/>')
        out.append(f'<rect x="{cx-r*0.9}" y="{cy+r*0.4}" width="{r*1.8}" height="{r*0.42}" fill="{b}"/><line x1="{cx-r*1.1}" y1="{cy+r*0.8}" x2="{cx+r*1.1}" y2="{cy+r*0.8}" stroke="{d}" stroke-width="3" stroke-linecap="round"/>')
        out.append(f'<path d="M{cx-r*0.1},{cy-r*1.0} q{r*0.35},-{r*0.45} {r*0.1},-{r*0.85} q{r*0.45},{r*0.35} {r*0.55},{r*0.6}" fill="none" stroke="{d}" stroke-width="2.5" opacity="0.6"/>')
    elif name == "Ketu":
        # headless: a halo where the head would be, body is the circle
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{b}" stroke="{d}" stroke-width="3"/>')
        out.append(f'<ellipse cx="{cx}" cy="{cy-r*1.25}" rx="{r*0.55}" ry="{r*0.16}" fill="none" stroke="#fde68a" stroke-width="5"/>')
        out.append(f'<text x="{cx}" y="{cy+r*0.12}" text-anchor="middle" font-size="{r*0.5}" fill="{d}" font-family="Georgia, serif">ॐ</text>')
    elif name == "You":
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{b}" stroke="{d}" stroke-width="3"/>')
        # hair
        out.append(f'<path d="M{cx-r*0.98},{cy-r*0.2} a{r*0.98},{r*0.98} 0 0 1 {r*1.96},0 q-{r*0.3},-{r*0.3} -{r*0.65},-{r*0.15} q-{r*0.33},-{r*0.25} -{r*0.66},0 q-{r*0.35},-{r*0.15} -{r*0.65},{r*0.15} z" fill="#3b2314"/>')
    if name != "Ketu":
        out.append(face(cx, cy, r, expr, d))
    if label:
        out.append(f'<text x="{cx}" y="{cy+r*1.95}" text-anchor="middle" font-size="12" fill="{INK}" font-family="Georgia, serif" font-weight="bold">{esc(name)}</text>')
    return "".join(out)

# ----------------------------------------------------------------------------- bubbles
def wrap(text, width):
    return textwrap.wrap(text, width) or [""]

def bubble(x, y, w, text, tail_to=None, thought=False, size=13):
    """Speech bubble with top-left at (x, y), width w; height from the wrapped text."""
    cpl = max(10, int(w / (size*0.52)))
    lines = wrap(text, cpl)
    h = len(lines)*(size+4) + 16
    out = []
    if thought:
        out.append(f'<ellipse cx="{x+w/2}" cy="{y+h/2}" rx="{w/2+6}" ry="{h/2+6}" fill="#fff" stroke="{INK}" stroke-width="2"/>')
        if tail_to:
            tx, ty = tail_to
            out.append(f'<circle cx="{(x+w/2+tx)/2}" cy="{(y+h+ty)/2}" r="5" fill="#fff" stroke="{INK}" stroke-width="2"/><circle cx="{(x+w/2+2*tx)/3}" cy="{(y+h+2*ty)/3}" r="3" fill="#fff" stroke="{INK}" stroke-width="2"/>')
    else:
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#fff" stroke="{INK}" stroke-width="2"/>')
        if tail_to:
            tx, ty = tail_to
            bx = min(max(tx, x+20), x+w-20)
            out.append(f'<polygon points="{bx-9},{y+h-1} {bx+9},{y+h-1} {tx},{ty}" fill="#fff" stroke="{INK}" stroke-width="2"/>')
            out.append(f'<line x1="{bx-8}" y1="{y+h-1}" x2="{bx+8}" y2="{y+h-1}" stroke="#fff" stroke-width="3"/>')
    for i, ln in enumerate(lines):
        out.append(f'<text x="{x+w/2}" y="{y+14+i*(size+4)+size*0.3}" text-anchor="middle" font-size="{size}" fill="{INK}" font-family="Georgia, serif">{esc(ln)}</text>')
    return "".join(out), h

# ----------------------------------------------------------------------------- panels
def render_strip(strip, panel_w=360, panel_h=330, gutter=14):
    """strip = {"title": str, "panels": [ {caption, chars:[{name,expr,pose,x}], bubbles:[{who, text, thought}] } ]}"""
    panels = strip["panels"]
    n = len(panels)
    cols = min(n, 3); rows = math.ceil(n/cols)
    W = cols*panel_w + (cols+1)*gutter
    title_h = 36 if strip.get("title") else 0
    H = rows*panel_h + (rows+1)*gutter + title_h
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Georgia, serif">',
           f'<rect width="{W}" height="{H}" rx="10" fill="{PAPER}"/>']
    if strip.get("title"):
        out.append(f'<text x="{W/2}" y="26" text-anchor="middle" font-size="16" font-weight="bold" fill="{INK}">{esc(strip["title"])}</text>')
    for i, p in enumerate(panels):
        c = i % cols; r = i // cols
        px = gutter + c*(panel_w+gutter); py = title_h + gutter + r*(panel_h+gutter)
        out.append(f'<rect x="{px}" y="{py}" width="{panel_w}" height="{panel_h}" rx="8" fill="#fff" stroke="{INK}" stroke-width="2.5"/>')
        top = py + 8
        if p.get("caption"):
            lines = wrap(p["caption"], 52)
            ch = len(lines)*16 + 10
            out.append(f'<rect x="{px+8}" y="{py+8}" width="{panel_w-16}" height="{ch}" rx="6" fill="{CAPTION_BG}" stroke="{BORDER}" stroke-width="1"/>')
            for k, ln in enumerate(lines):
                out.append(f'<text x="{px+16}" y="{py+8+14+k*16}" font-size="12" font-style="italic" fill="{INK}">{esc(ln)}</text>')
            top = py + 8 + ch + 6
        chars = p.get("chars", [])
        # positions: spread characters along the bottom third
        ground = py + panel_h - 60
        slots = {1: [0.5], 2: [0.3, 0.72], 3: [0.2, 0.5, 0.8]}[max(1, min(3, len(chars)))]
        pos = {}
        for k, ch_ in enumerate(chars):
            cx = px + panel_w*ch_.get("x", slots[k]); r_ = ch_.get("r", 40)
            cy = ground - r_*0.8
            pos[ch_["name"]] = (cx, cy - r_*1.1, r_)
            out.append(character(ch_["name"], cx, cy, r_, ch_.get("expr", "calm"), ch_.get("pose", "stand"), ch_.get("flip", False), ch_.get("label", True)))
        # bubbles stacked from the top
        by = top + 4
        for bdef in p.get("bubbles", []):
            who = bdef.get("who")
            tail = None
            if who in pos:
                tx, ty, rr = pos[who]; tail = (tx, ty + 6)
            bw = bdef.get("w", panel_w - 40)
            bx = px + 20 if bdef.get("side", "auto") != "right" else px + panel_w - 20 - bw
            if who in pos and bdef.get("side", "auto") == "auto":
                tx = pos[who][0]
                bx = max(px + 10, min(px + panel_w - 10 - bw, tx - bw/2))
            svg_b, h = bubble(bx, by, bw, bdef["text"], tail, bdef.get("thought", False))
            out.append(svg_b); by += h + 10
    out.append("</svg>")
    return "\n".join(out)

def main():
    import importlib.util
    here = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location("comic_scripts", os.path.join(here, "comic_scripts.py"))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    outdir = os.path.join(os.path.dirname(here), "images")
    only = sys.argv[1:] if len(sys.argv) > 1 and sys.argv[1] != "--all" else None
    for key, strip in mod.STRIPS.items():
        if only and key not in only: continue
        svg = render_strip(strip)
        path = os.path.join(outdir, f"{key}.svg")
        open(path, "w", encoding="utf-8").write(svg)
        import xml.dom.minidom; xml.dom.minidom.parseString(svg)
        print("ok", path)

if __name__ == "__main__":
    main()
