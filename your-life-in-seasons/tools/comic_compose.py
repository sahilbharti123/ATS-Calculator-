#!/usr/bin/env python3
"""
comic_compose.py: builds comic strips from illustrated character cut-outs + the scripts in comic_scripts.py.

Pipeline
  1. cover/characters/<Name>.png : a full-resolution character sheet (three poses on white) from the illustrator.
  2. python3 tools/comic_compose.py split      → cover/characters/cut/<Name>-<i>.png (transparent cut-outs, i = 0,1,2)
  3. python3 tools/comic_compose.py strips     → images/<key>.png for every strip in comic_scripts.STRIPS

Pose mapping: each sheet has three poses left→right. Scripts refer to poses by name; POSE_INDEX maps a name
to the sheet column for that character (edit after looking at the sheets).
"""
import os, sys, math, textwrap, importlib.util
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHEETS = os.path.join(ROOT, "cover", "characters")
CUT = os.path.join(SHEETS, "cut")
OUT = os.path.join(ROOT, "images")
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_ITAL = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
INK = (43, 51, 80); PAPER = (255, 253, 247); BORDER = (184, 149, 106); CAPTION_BG = (238, 241, 248)

# which sheet column (0,1,2) plays which script pose, per character
POSE_INDEX = {
    "default": {"stand": 0, "point": 2, "wave": 2, "arms_up": 2, "think": 1, "sit": 1},
    "You":     {"stand": 0, "point": 0, "wave": 1, "arms_up": 1, "think": 2, "sit": 2},
    "Mars":    {"stand": 0, "point": 1, "wave": 1, "arms_up": 1, "think": 2, "sit": 2},
    "Ketu":    {"stand": 1, "point": 2, "wave": 2, "arms_up": 2, "think": 0, "sit": 0},
    "Rahu":    {"stand": 1, "point": 0, "wave": 0, "arms_up": 2, "think": 1, "sit": 1},
    "Moon":    {"stand": 0, "point": 0, "wave": 0, "arms_up": 2, "think": 1, "sit": 1},
    "Venus":   {"stand": 0, "point": 0, "wave": 2, "arms_up": 2, "think": 1, "sit": 1},
    "Jupiter": {"stand": 0, "point": 0, "wave": 2, "arms_up": 2, "think": 1, "sit": 1},
    "Saturn":  {"stand": 0, "point": 2, "wave": 2, "arms_up": 2, "think": 1, "sit": 1},
    "Sun":     {"stand": 0, "point": 2, "wave": 2, "arms_up": 2, "think": 1, "sit": 1},
    "Mercury": {"stand": 0, "point": 2, "wave": 2, "arms_up": 1, "think": 1, "sit": 1},
}

# ------------------------------------------------------------------ 1. split sheets into transparent cut-outs
def knock_out_white(im, thresh=235):
    """Make near-white background transparent by flood-filling from the image border."""
    im = im.convert("RGBA")
    w, h = im.size
    px = im.load()
    from collections import deque
    seen = bytearray(w*h)
    q = deque()
    def white(p): return p[0] > thresh and p[1] > thresh and p[2] > thresh
    for x in range(w):
        for y in (0, h-1):
            if white(px[x, y]) and not seen[y*w+x]: q.append((x, y)); seen[y*w+x] = 1
    for y in range(h):
        for x in (0, w-1):
            if white(px[x, y]) and not seen[y*w+x]: q.append((x, y)); seen[y*w+x] = 1
    while q:
        x, y = q.popleft()
        r, g, b, a = px[x, y]
        px[x, y] = (r, g, b, 0)
        for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
            if 0 <= nx < w and 0 <= ny < h and not seen[ny*w+nx] and white(px[nx, ny]):
                seen[ny*w+nx] = 1; q.append((nx, ny))
    # soften the edge slightly
    alpha = im.split()[3].filter(ImageFilter.GaussianBlur(0.6))
    im.putalpha(alpha)
    return im

def keep_largest_island(im, min_frac=0.02):
    """Remove alpha islands smaller than min_frac of the largest one (stray bits of neighbouring figures)."""
    a = im.split()[3]; w, h = im.size
    scale = max(1, int(max(w, h) / 400))
    small = a.resize((max(1, w//scale), max(1, h//scale)), Image.NEAREST)
    sw, sh = small.size; px = small.load()
    label = [[0]*sw for _ in range(sh)]; sizes = {}; cur = 0
    from collections import deque
    for y in range(sh):
        for x in range(sw):
            if px[x, y] > 30 and label[y][x] == 0:
                cur += 1; q = deque([(x, y)]); label[y][x] = cur; n = 0
                while q:
                    cx, cy = q.popleft(); n += 1
                    for nx, ny in ((cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)):
                        if 0 <= nx < sw and 0 <= ny < sh and label[ny][nx] == 0 and px[nx, ny] > 30:
                            label[ny][nx] = cur; q.append((nx, ny))
                sizes[cur] = n
    if not sizes: return im
    biggest = max(sizes.values())
    keep = {k for k, v in sizes.items() if v >= biggest*min_frac}
    mask = Image.new("L", (sw, sh), 0); mp = mask.load()
    for y in range(sh):
        for x in range(sw):
            if label[y][x] in keep: mp[x, y] = 255
    mask = mask.resize((w, h), Image.NEAREST).filter(ImageFilter.MaxFilter(5))
    new_a = Image.composite(a, Image.new("L", (w, h), 0), mask)
    im = im.copy(); im.putalpha(new_a); return im

def split_sheet(path, name):
    im = knock_out_white(Image.open(path))
    w, h = im.size
    alpha = im.split()[3]
    cols = [sum(1 for y in range(0, h, 2) if alpha.getpixel((x, y)) > 40) for x in range(w)]
    def cut_at(lo, hi):
        zone = range(int(w*lo), int(w*hi))
        return min(zone, key=lambda x: sum(cols[max(0, x-3):x+4]))
    c1 = cut_at(0.26, 0.42); c2 = cut_at(0.58, 0.76)
    spans = [(0, c1), (c1, c2), (c2, w)]
    os.makedirs(CUT, exist_ok=True)
    outs = []
    for i, (x0, x1) in enumerate(spans):
        crop = im.crop((max(0, x0-6), 0, min(w, x1+6), h))
        crop = keep_largest_island(crop)
        bbox = crop.split()[3].getbbox()
        if bbox: crop = crop.crop(bbox)
        p = os.path.join(CUT, f"{name}-{i}.png"); crop.save(p); outs.append(p)
    return outs

# ------------------------------------------------------------------ 2. compose strips
def font(size, kind="reg"):
    return ImageFont.truetype({"reg": FONT_REG, "bold": FONT_BOLD, "ital": FONT_ITAL}[kind], size)

def wrap_text(draw, text, fnt, max_w):
    words = text.split(); lines = []; cur = ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=fnt) <= max_w: cur = t
        else: lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

def rounded(draw, box, r, fill, outline, width):
    draw.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)

def draw_bubble(draw, x, y, w, text, tail_to=None, size=26, thought=False):
    fnt = font(size)
    lines = wrap_text(draw, text, fnt, w - 36)
    lh = size + 8; h = len(lines)*lh + 28
    if thought:
        draw.ellipse([x, y, x+w, y+h], fill="white", outline=INK, width=4)
        if tail_to:
            tx, ty = tail_to
            for k, rr in ((0.35, 12), (0.65, 7)):
                cx = x + w/2 + (tx - (x+w/2))*k; cy = y + h + (ty - (y+h))*k
                draw.ellipse([cx-rr, cy-rr, cx+rr, cy+rr], fill="white", outline=INK, width=3)
    else:
        rounded(draw, [x, y, x+w, y+h], 22, "white", INK, 4)
        if tail_to:
            tx, ty = tail_to
            bx = min(max(tx, x+40), x+w-40)
            draw.polygon([(bx-16, y+h-2), (bx+16, y+h-2), (tx, ty)], fill="white", outline=INK)
            draw.line([(bx-15, y+h-2), (bx+15, y+h-2)], fill="white", width=6)
            draw.line([(bx-16, y+h-2), (tx, ty)], fill=INK, width=4); draw.line([(bx+16, y+h-2), (tx, ty)], fill=INK, width=4)
    for i, ln in enumerate(lines):
        tw = draw.textlength(ln, font=fnt)
        draw.text((x + (w-tw)/2, y + 14 + i*lh), ln, font=fnt, fill=INK)
    return h

def place_character(canvas, name, pose, cx, ground_y, target_h):
    idx = POSE_INDEX.get(name, POSE_INDEX["default"]).get(pose, 0)
    p = os.path.join(CUT, f"{name}-{idx}.png")
    if not os.path.exists(p):
        p = os.path.join(CUT, f"{name}-0.png")
    im = Image.open(p).convert("RGBA")
    scale = target_h / im.height
    im = im.resize((max(1, int(im.width*scale)), int(target_h)), Image.LANCZOS)
    x = int(cx - im.width/2); y = int(ground_y - im.height)
    canvas.alpha_composite(im, (max(0, x), max(0, y)))
    return (cx, y)  # top centre, for bubble tails

def render_strip(key, strip, panel_w=820, panel_h=760, gutter=28):
    panels = strip["panels"]; n = len(panels); cols = min(n, 3); rows = math.ceil(n/cols)
    title_h = 80 if strip.get("title") else 0
    W = cols*panel_w + (cols+1)*gutter; H = rows*panel_h + (rows+1)*gutter + title_h
    canvas = Image.new("RGBA", (W, H), PAPER + (255,))
    draw = ImageDraw.Draw(canvas)
    if strip.get("title"):
        f = font(36, "bold"); tw = draw.textlength(strip["title"], font=f)
        draw.text(((W-tw)/2, 24), strip["title"], font=f, fill=INK)
    for i, p in enumerate(panels):
        c = i % cols; r = i // cols
        px = gutter + c*(panel_w+gutter); py = title_h + gutter + r*(panel_h+gutter)
        rounded(draw, [px, py, px+panel_w, py+panel_h], 18, "white", INK, 5)
        top = py + 18
        if p.get("caption"):
            f = font(24, "ital"); lines = wrap_text(draw, p["caption"], f, panel_w - 60)
            ch = len(lines)*32 + 20
            rounded(draw, [px+18, py+18, px+panel_w-18, py+18+ch], 10, CAPTION_BG, BORDER, 2)
            for k, ln in enumerate(lines): draw.text((px+32, py+28+k*32), ln, font=f, fill=INK)
            top = py + 18 + ch + 12
        chars = p.get("chars", [])
        ground = py + panel_h - 36
        slots = {1: [0.5], 2: [0.28, 0.72], 3: [0.18, 0.5, 0.82]}[max(1, min(3, len(chars)))]
        pos = {}
        # characters are drawn after bubbles are measured so bubbles can sit above them; measure first
        base_h = {1: 0.52, 2: 0.5, 3: 0.44}[max(1, min(3, len(chars)))] * panel_h
        heads = {}
        layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        for k, ch_ in enumerate(chars):
            cx = px + panel_w*ch_.get("x", slots[k]); th = base_h * ch_.get("r", 40)/40
            heads[ch_["name"]] = place_character(layer, ch_["name"], ch_.get("pose", "stand"), cx, ground, th)
        placed = []  # (x0,y0,x1,y1)
        bubbles = p.get("bubbles", [])
        fnt = font(26)
        specs = []
        for b in bubbles:
            who = b.get("who"); bw = int(min(b.get("w", panel_w*0.58), panel_w - 60))
            lines = wrap_text(draw, b["text"], fnt, bw - 36); bh = len(lines)*34 + 28
            if who in heads:
                hx, hy = heads[who]; bx = int(max(px + 14, min(px + panel_w - 14 - bw, hx - bw/2))); by = int(hy - bh - 26)
                tail = (int(hx), int(hy) + 8)
            else:
                bx = px + 30; by = top; tail = None
            specs.append([bx, by, bw, bh, b, tail])
        # later bubbles stay low near their speaker; earlier ones move up if they overlap
        for i in range(len(specs)-1, -1, -1):
            bx, by, bw, bh, b, tail = specs[i]
            by = min(by, py + panel_h - 60 - bh)
            def hits(y):
                return any(not (bx+bw < x0 or bx > x1 or y+bh < y0 or y > y1) for (x0, y0, x1, y1) in placed)
            while hits(by) and by > top: by -= 6
            by = max(by, top)
            specs[i][1] = by; placed.append((bx, by, bx+bw, by+bh))
        canvas.alpha_composite(layer)
        for bx, by, bw, bh, b, tail in specs:
            draw_bubble(draw, bx, by, bw, b["text"], tail, thought=b.get("thought", False))
    return canvas.convert("RGB")

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "strips"
    if cmd == "split":
        for f in sorted(os.listdir(SHEETS)):
            if f.lower().endswith((".png", ".jpg", ".jpeg")):
                name = os.path.splitext(f)[0]
                outs = split_sheet(os.path.join(SHEETS, f), name)
                print(name, len(outs), "cut-outs")
    else:
        spec = importlib.util.spec_from_file_location("comic_scripts", os.path.join(ROOT, "tools", "comic_scripts.py"))
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        only = sys.argv[2:]
        os.makedirs(OUT, exist_ok=True)
        for key, strip in mod.STRIPS.items():
            if only and key not in only: continue
            im = render_strip(key, strip)
            im.save(os.path.join(OUT, f"{key}.png"), optimize=True)
            print("ok", key, im.size)

if __name__ == "__main__":
    main()
