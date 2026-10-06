#!/usr/bin/env python3
"""
comic_pages.py: composes finished comic pages from the YAML script and the panel images.

  python3 tools/comic_pages.py pages [p061 p062 ...]   -> comic/pages/pNNN.png (1800x2700, 6x9 in at 300 dpi)
  python3 tools/comic_pages.py book                    -> dist/Your-Life-in-Seasons-comic-print-6x9.pdf from all pages
  python3 tools/comic_pages.py missing                 -> lists panels that have no image yet

Script: comic/script/*.yaml (see comic/COMIC-BIBLE.md). Panel images: comic/panels/<page id>-<n>.png
(n = 1-based panel index). A missing panel is drawn as a grey placeholder so layout can be checked early.

Layouts and the aspect each panel is generated at (see PANEL_ASPECT):
  single: one panel (3:4)          two: two stacked (3:2)       three: three stacked (2:1)
  four: 2x2 (1:1)                  grid6: 3 rows x 2 (4:3)      fact: one panel (4:3) + fact box
Bubbles are placed in dialogue order across the top of the panel; each tail points at its speaker,
whose horizontal position is the speaker's index in the panel's `chars` list (left to right).
"""
import os, sys, glob, math, re
import yaml
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT_DIR = os.path.join(ROOT, "comic", "script")
PANEL_DIR = os.path.join(ROOT, "comic", "panels")
PAGE_DIR = os.path.join(ROOT, "comic", "pages")
FONT_DIR = os.path.join(ROOT, "comic", "fonts")
os.makedirs(PAGE_DIR, exist_ok=True)

W, H = 1800, 2700
M = 96                       # side margin
TOP = 100                    # top margin
BOTTOM = 110                 # bottom margin (page number lives here)
GUT = 34                     # gutter between panels
BORDER = 7                   # panel border

NAVY = (30, 42, 90); INK = (20, 20, 24); CREAM = (255, 247, 223); PAPER = (253, 251, 245)
GOLD = (200, 150, 60); GREY = (120, 120, 128); RED = (196, 60, 50); GREEN = (70, 150, 90); AMBER = (225, 170, 50)

PANEL_ASPECT = {  # width / height of generated panels per layout
    "single": 3/4, "two": 3/2, "three": 2/1, "four": 1/1, "grid6": 4/3, "fact": 4/3,
}
PANEL_COUNT = {"single": 1, "two": 2, "three": 3, "four": 4, "grid6": 6, "fact": 1}
CANVA_RATIO = {"single": "PORTRAIT_3_4", "two": "LANDSCAPE_3_2", "three": "LANDSCAPE_2_1",
               "four": "SQUARE_1_1", "grid6": "LANDSCAPE_4_3", "fact": "LANDSCAPE_4_3"}

def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

F_TITLE = lambda s: font("Bangers.ttf", s)
F_BUBBLE = lambda s: font("ComicNeue-Bold.ttf", s)
F_CAPTION = lambda s: font("PatrickHand.ttf", s)
F_SMALL = lambda s: font("Nunito-Regular.ttf", s)
F_FACT = lambda s: font("Nunito-ExtraBold.ttf", s)

# ---------------------------------------------------------------- script
def load_script():
    pages = []
    for f in sorted(glob.glob(os.path.join(SCRIPT_DIR, "*.yaml"))):
        data = yaml.safe_load(open(f, encoding="utf-8")) or []
        for p in data:
            p["_file"] = os.path.basename(f)
            pages.append(p)
    pages.sort(key=lambda p: p["id"])
    return pages

# ---------------------------------------------------------------- text helpers
def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def text_block(draw, lines, fnt, x, y, fill, align="left", max_w=None, spacing=1.18):
    lh = int(fnt.size * spacing)
    for i, ln in enumerate(lines):
        tw = draw.textlength(ln, font=fnt)
        if align == "center" and max_w: xx = x + (max_w - tw) / 2
        elif align == "right" and max_w: xx = x + max_w - tw
        else: xx = x
        draw.text((xx, y + i * lh), ln, font=fnt, fill=fill)
    return y + len(lines) * lh

# ---------------------------------------------------------------- panels
def fit_cover(im, w, h):
    r = max(w / im.width, h / im.height)
    im = im.resize((max(1, round(im.width * r)), max(1, round(im.height * r))), Image.LANCZOS)
    l = (im.width - w) // 2; t = (im.height - h) // 2
    return im.crop((l, t, l + w, t + h))

def panel_image(pid, n, w, h):
    path = os.path.join(PANEL_DIR, f"{pid}-{n}.png")
    if os.path.exists(path):
        return fit_cover(Image.open(path).convert("RGB"), w, h), True
    ph = Image.new("RGB", (w, h), (225, 222, 214))
    d = ImageDraw.Draw(ph)
    d.text((w / 2, h / 2), f"{pid} panel {n}", font=F_SMALL(min(48, w // 12)), fill=GREY, anchor="mm")
    return ph, False

def draw_bubble(draw, text, cx, top, max_w, fnt, tail_to=None, thought=False, panel_x=(0, 10**6), tail_y=None):
    """Speech bubble centred near cx (kept inside panel_x) with its top edge at `top`.
    The tail tip points at (tail_to, below the bubble); its base stays within the bubble. With tail_y the tail
    stretches down to that height (the speaker's head), at most six text heights long."""
    pad_x, pad_y = int(fnt.size * 0.8), int(fnt.size * 0.55)
    lines = wrap(draw, text, fnt, max_w - 2 * pad_x)
    lh = int(fnt.size * 1.12)
    tw = max(draw.textlength(l, font=fnt) for l in lines)
    bw = int(tw + 2 * pad_x); bh = int(len(lines) * lh + 2 * pad_y)
    cx = min(max(cx, panel_x[0] + bw / 2 + 10), panel_x[1] - bw / 2 - 10)
    x0 = int(cx - bw / 2); y0 = int(top); x1 = x0 + bw; y1 = y0 + bh
    r = min(bh // 2, int(fnt.size * 1.4))
    stroke = max(3, fnt.size // 9)
    if tail_to is not None and not thought:
        tx = int(min(max(tail_to, x0 + r), x1 - r))
        base = int(fnt.size * 0.5)
        tail_len = int(fnt.size * 1.3)
        tip = (int(min(max(tail_to, tx - base * 2), tx + base * 2)), y1 + tail_len)
        if tail_y is not None and tail_y > y1 + tail_len:
            ty = min(tail_y, y1 + fnt.size * 6)
            reach = (ty - y1) * 0.55                      # slant at most ~30 degrees
            tip = (int(min(max(tail_to, tx - reach), tx + reach)), int(ty))
            base = int(max(base, (ty - y1) * 0.13))       # long tails get a wider base
            tx = int(min(max(tx, x0 + r + base), x1 - r - base)) if x1 - x0 > 2 * (r + base) else tx
        draw.polygon([(tx - base, y1 - 2), (tx + base, y1 - 2), tip], fill="white", outline=INK)
        draw.line([(tx - base, y1 - 2), tip, (tx + base, y1 - 2)], fill=INK, width=stroke)
    draw.rounded_rectangle([x0, y0, x1, y1], radius=r, fill="white", outline=INK, width=stroke)
    if tail_to is not None and not thought:
        draw.line([(tx - base + 1, y1 - stroke // 2 - 1), (tx + base - 1, y1 - stroke // 2 - 1)], fill="white", width=stroke + 2)
    if thought and tail_to is not None:
        for k, rr in enumerate((int(fnt.size * 0.4), int(fnt.size * 0.27), int(fnt.size * 0.16))):
            cy = y1 + int(fnt.size * (0.55 + k * 0.75))
            cxx = int(cx + (tail_to - cx) * (0.2 + 0.3 * k))
            draw.ellipse([cxx - rr, cy - rr, cxx + rr, cy + rr], fill="white", outline=INK, width=max(2, stroke - 1))
    y = y0 + pad_y
    for ln in lines:
        draw.text((x0 + (bw - draw.textlength(ln, font=fnt)) / 2, y), ln, font=fnt, fill=INK)
        y += lh
    return (x0, y0, x1, y1), y1

def content_top(im, x_frac=None, band=0.25):
    """Row (fraction of height) where the drawing starts below the calm top band, scanning a column strip
    around x_frac (or the whole width). Compares each row to the mean colour of the top 3% rows."""
    small = im.convert("RGB").resize((160, 160))
    px = small.load()
    x0, x1 = (0, 160) if x_frac is None else (max(0, int(x_frac * 160) - 16), min(160, int(x_frac * 160) + 16))
    ref = [0, 0, 0]; cnt = 0
    for y in range(0, 5):
        for x in range(x0, x1):
            r, g, b = px[x, y]; ref[0] += r; ref[1] += g; ref[2] += b; cnt += 1
    ref = [c / max(1, cnt) for c in ref]
    for y in range(3, 160):
        diff = 0; m = 0
        for x in range(x0, x1):
            r, g, b = px[x, y]
            d = abs(r - ref[0]) + abs(g - ref[1]) + abs(b - ref[2])
            if d > 90: m += 1
        if m > (x1 - x0) * 0.35: return y / 160
    return band

def speaker_positions(pid, n, panel):
    """Horizontal position (0..1) of each character. From comic/panels/<pid>-<n>.json if the generator
    recorded it ({"positions": {"Mars": 0.2, ...}}), else evenly spaced in `chars` order."""
    chars = panel.get("chars") or []
    pos = {c: (i + 0.5) / max(1, len(chars)) for i, c in enumerate(chars)}
    side = os.path.join(PANEL_DIR, f"{pid}-{n}.json")
    if os.path.exists(side):
        try:
            import json
            data = json.load(open(side))
            for k, v in (data.get("positions") or {}).items():
                pos[k] = float(v)
        except Exception:
            pass
    return pos

def overlaps(a, b, gap=10):
    return not (a[2] + gap < b[0] or b[2] + gap < a[0] or a[3] + gap < b[1] or b[3] + gap < a[1])

def place_bubbles(page_img, pid, n, panel, box, fsize, beam=14, branch=7):
    """Bubbles in dialogue order, laid out by a small beam search over positions (and two narrower wraps).
    A layout scores well when no bubbles overlap, reading order holds (each bubble sits below the previous
    one, or in the same row to its right), every character's face stays clear, bubbles sit high in the panel,
    and each one is close to its speaker so the tail is short."""
    x0, y0, x1, y1 = box
    pw, ph = x1 - x0, y1 - y0
    bubbles = panel.get("bubbles") or []
    if not bubbles: return
    pos = speaker_positions(pid, n, panel)
    draw = ImageDraw.Draw(page_img)
    fnt = F_BUBBLE(fsize)
    max_w = int(min(pw * 0.46, 620 * fsize / 36))
    top0 = y0 + int(fsize * 0.6)
    panel_img = page_img.crop((x0 + BORDER, y0 + BORDER, x1 - BORDER, y1 - BORDER))   # inside the border
    pad_x, pad_y = int(fnt.size * 0.8), int(fnt.size * 0.55)
    gap = int(fsize * 0.6)
    # face zones of every character (head top from the art; tall enough to cover a crown or plume and the face)
    hw, face_h = pw * 0.065, min(ph * 0.34, pw * 0.2)
    heads = {who: y0 + int(content_top(panel_img, f) * ph) for who, f in pos.items()}
    zones = [(x0 + pw * f - hw, heads[who], x0 + pw * f + hw, heads[who] + face_h) for who, f in pos.items()]

    def candidates(b):
        who = b.get("who")
        px = x0 + pw * pos.get(who, 0.5)
        head_y = heads.get(who, y0 + int(content_top(panel_img, 0.5) * ph))
        out = []
        for mw, wpen in ((max_w, 0), (int(max_w * 0.72), 0.15), (int(max_w * 0.52), 0.35)):
            lines = wrap(draw, b["text"], fnt, mw - 2 * pad_x)
            bw = int(max(draw.textlength(l, font=fnt) for l in lines) + 2 * pad_x)
            bh = int(len(lines) * int(fnt.size * 1.12) + 2 * pad_y)
            if bw > pw - 20: continue
            for top in range(top0, int(y1 - bh - fsize * 1.6), max(6, int(fsize * 0.7))):
                for k in range(25):
                    cx = x0 + bw / 2 + 10 + (pw - bw - 20) * k / 24
                    r = (int(cx - bw / 2), top, int(cx + bw / 2), top + bh)
                    s = wpen + 0.8 * (top - top0) / ph
                    for z in zones:
                        ix = min(r[2], z[2]) - max(r[0], z[0]); iy = min(r[3], z[3]) - max(r[1], z[1])
                        if ix > 0 and iy > 0: s += 40 * ix * iy / ((z[2] - z[0]) * (z[3] - z[1]))
                    dx = max(0, r[0] + fsize - px, px - (r[2] - fsize)) / pw
                    s += 6 * dx + 0.6 * abs(cx - px) / pw
                    above = head_y - int(fsize * 1.2) - r[3]
                    if above >= 0: s += 0.3 * max(0, above - fsize * 6) / ph + 0.1 * above / ph
                    else: s += 0.4 + 3 * (-above) / ph
                    out.append((s, r, px, head_y))
        return out

    def tail_box(r, px, hy):
        # the area a stretched tail sweeps, from the bubble's bottom edge down towards the speaker's head
        tx = min(max(px, r[0] + fsize), r[2] - fsize)
        ty = max(r[3] + int(fsize * 1.3), min(hy - int(fsize * 0.3), r[3] + fsize * 6))
        reach = (ty - r[3]) * 0.55
        tip = min(max(px, tx - reach), tx + reach)
        return (int(min(tx, tip) - fsize * 0.5), r[3] + 2, int(max(tx, tip) + fsize * 0.5), int(ty))

    states = [(0.0, [], [], [])]
    for b in bubbles:
        cands = candidates(b)
        nxt = []
        for S, placed, laid, tails in states:
            scored = []
            for s, r, px, hy in cands:
                if any(overlaps(r, q, gap) for q in placed): s += 1000
                t = tail_box(r, px, hy)
                s += 30 * sum(overlaps(t, q, 0) for q in placed) + 30 * sum(overlaps(r, q, 0) for q in tails)
                if placed:
                    prev = placed[-1]
                    if r[0] >= prev[2] - gap:
                        if r[1] < prev[1]: s += 200
                    elif r[1] < prev[3] + gap // 2: s += 200
                scored.append((s, r, px, hy))
            scored.sort(key=lambda c: c[0])
            picked = []
            for s, r, px, hy in scored:
                if any(abs(r[0] - q[1][0]) < pw * 0.15 and abs(r[1] - q[1][1]) < fsize * 2 for q in picked): continue
                picked.append((s, r, px, hy))
                if len(picked) >= branch: break
            for s, r, px, hy in picked:
                nxt.append((S + s, placed + [r], laid + [(b, r, px, hy)], tails + [tail_box(r, px, hy)]))
        nxt.sort(key=lambda st: st[0])
        states = nxt[:beam]
    for b, r, px, hy in states[0][2]:
        draw_bubble(draw, b["text"], (r[0] + r[2]) / 2, r[1], r[2] - r[0] + 2, fnt, tail_to=int(px),
                    thought=bool(b.get("thought")), panel_x=(x0, x1), tail_y=hy - int(fsize * 0.3))

def panel_boxes(layout, area):
    ax0, ay0, ax1, ay1 = area
    aw, ah = ax1 - ax0, ay1 - ay0
    boxes = []
    if layout in ("single", "fact"):
        asp = PANEL_ASPECT[layout]
        w = aw; h = int(w / asp)
        if h > ah: h = ah; w = int(h * asp)
        x = ax0 + (aw - w) // 2
        boxes = [(x, ay0, x + w, ay0 + h)]
    elif layout in ("two", "three"):
        n = PANEL_COUNT[layout]
        h = (ah - GUT * (n - 1)) // n
        w = aw
        asp = PANEL_ASPECT[layout]
        if w / h > asp: w = int(h * asp)
        else: h = int(w / asp);
        x = ax0 + (aw - w) // 2
        total = n * h + GUT * (n - 1)
        y = ay0 + (ah - total) // 2
        for i in range(n):
            boxes.append((x, y + i * (h + GUT), x + w, y + i * (h + GUT) + h))
    elif layout == "four":
        w = (aw - GUT) // 2; h = w
        total_h = 2 * h + GUT
        y = ay0 + max(0, (ah - total_h) // 2)
        for r in range(2):
            for c in range(2):
                boxes.append((ax0 + c * (w + GUT), y + r * (h + GUT), ax0 + c * (w + GUT) + w, y + r * (h + GUT) + h))
    elif layout == "grid6":
        w = (aw - GUT) // 2; h = int(w / PANEL_ASPECT["grid6"])
        total_h = 3 * h + 2 * GUT
        if total_h > ah:
            h = (ah - 2 * GUT) // 3; w = int(h * PANEL_ASPECT["grid6"]); total_h = 3 * h + 2 * GUT
        x = ax0 + (aw - (2 * w + GUT)) // 2
        y = ay0 + max(0, (ah - total_h) // 2)
        for r in range(3):
            for c in range(2):
                boxes.append((x + c * (w + GUT), y + r * (h + GUT), x + c * (w + GUT) + w, y + r * (h + GUT) + h))
    return boxes

def chapter_label(p):
    ch = p.get("chapter", "")
    years = {"ketu": 7, "venus": 20, "sun": 6, "moon": 10, "mars": 7, "rahu": 18, "jupiter": 16, "saturn": 19, "mercury": 17}
    if ch in years: return f"THE {ch.upper()} SEASON · {years[ch]} YEARS"
    return {1: "PART ONE · THE TEAM", 3: "PART THREE · LIVING WITH THE TEAM"}.get(p.get("part"), "")

def render_page(p, number):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    layout = p["layout"]
    # ---- title band
    y = TOP
    label = chapter_label(p)
    if label:
        d.text((M, y), label, font=F_SMALL(26), fill=GOLD)
        y += 38
    tf = F_TITLE(78)
    tlines = wrap(d, p.get("title", ""), tf, W - 2 * M)
    y = text_block(d, tlines, tf, M, y, NAVY, spacing=1.0)
    y += 14
    d.line([(M, y), (W - M, y)], fill=NAVY, width=4)
    y += 30
    # ---- bottom: footnote + caption measured first
    cap_font = F_CAPTION(40)
    cap_lines = wrap(d, p.get("caption", ""), cap_font, W - 2 * M - 60)
    cap_h = len(cap_lines) * int(40 * 1.2) + 44
    fn_lines = []
    if p.get("footnote"):
        fn_lines = wrap(d, p["footnote"], F_SMALL(26), W - 2 * M - 40)
    fn_h = (len(fn_lines) * 32 + 28) if fn_lines else 0
    fact_lines = []
    fact_h = 0
    if layout == "fact":
        for ln in p.get("fact") or []:
            fact_lines.append(wrap(d, str(ln), F_FACT(34), W - 2 * M - 120))
        fact_h = sum(len(l) * 42 + 14 for l in fact_lines) + 60
    bottom_y = H - BOTTOM
    area = (M, y, W - M, bottom_y - cap_h - fn_h - fact_h - 30)
    # ---- panels
    boxes = panel_boxes(layout, area)
    fsize = {"single": 40, "two": 36, "three": 34, "four": 30, "grid6": 24, "fact": 36}[layout]
    panels = p.get("panels") or []
    missing = []
    for i, box in enumerate(boxes):
        x0, y0, x1, y1 = box
        im, ok = panel_image(p["id"], i + 1, x1 - x0, y1 - y0)
        if not ok: missing.append(f"{p['id']}-{i+1}")
        img.paste(im, (x0, y0))
        d.rectangle([x0 - BORDER // 2, y0 - BORDER // 2, x1 + BORDER // 2, y1 + BORDER // 2], outline=INK, width=BORDER)
        if i < len(panels):
            place_bubbles(img, p['id'], i + 1, panels[i], box, fsize)
    d = ImageDraw.Draw(img)
    # ---- fact box
    yb = max(b[3] for b in boxes) + 36 if boxes else area[1]
    if layout == "fact" and fact_lines:
        bx0, bx1 = M, W - M
        bh = fact_h
        d.rounded_rectangle([bx0, yb, bx1, yb + bh], radius=18, fill=CREAM, outline=GOLD, width=4)
        yy = yb + 30
        for lines in fact_lines:
            first = lines[0].lower()
            col = GREEN if first.startswith(("on your side", "friend")) else RED if first.startswith(("tests you", "test")) else AMBER if first.startswith("mixed") else NAVY
            d.ellipse([bx0 + 36, yy + 10, bx0 + 60, yy + 34], fill=col)
            yy = text_block(d, lines, F_FACT(34), bx0 + 84, yy, INK, spacing=1.24) + 14
        yb = yb + bh + 24
    # ---- caption
    cy0 = bottom_y - fn_h - cap_h
    d.rounded_rectangle([M, cy0, W - M, cy0 + cap_h], radius=10, fill=CREAM, outline=INK, width=3)
    text_block(d, cap_lines, cap_font, M + 30, cy0 + 20, INK, spacing=1.2)
    # ---- footnote
    if fn_lines:
        fy = cy0 + cap_h + 10
        text_block(d, fn_lines, F_SMALL(26), M + 20, fy, GREY, spacing=1.23)
    # ---- page number
    d.text((W / 2, H - 56), str(number), font=F_SMALL(28), fill=GREY, anchor="mm")
    return img, missing

def cmd_pages(only):
    pages = load_script()
    all_missing = []
    for idx, p in enumerate(pages, start=1):
        if only and p["id"] not in only: continue
        img, missing = render_page(p, idx)
        img.save(os.path.join(PAGE_DIR, f"{p['id']}.png"))
        all_missing += missing
        print("page", p["id"], p["layout"], "missing panels:", len(missing))
    if all_missing: print("missing panel images:", len(all_missing))

def cmd_book():
    pages = load_script()
    files = [os.path.join(PAGE_DIR, f"{p['id']}.png") for p in pages]
    files = [f for f in files if os.path.exists(f)]
    if not files: print("no pages rendered"); return
    ims = [Image.open(f).convert("RGB") for f in files]
    out = os.path.join(ROOT, "dist", "Your-Life-in-Seasons-comic-print-6x9.pdf")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    ims[0].save(out, "PDF", resolution=300, save_all=True, append_images=ims[1:])
    print("wrote", out, len(ims), "pages")

def cmd_missing():
    pages = load_script()
    n = 0
    for p in pages:
        for i in range(PANEL_COUNT[p["layout"]]):
            if not os.path.exists(os.path.join(PANEL_DIR, f"{p['id']}-{i+1}.png")):
                print(f"{p['id']}-{i+1}"); n += 1
    print("missing:", n, "of", sum(PANEL_COUNT[p["layout"]] for p in pages))

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "pages"
    if cmd == "pages": cmd_pages(set(sys.argv[2:]))
    elif cmd == "book": cmd_book()
    elif cmd == "missing": cmd_missing()
    else: print(__doc__)
