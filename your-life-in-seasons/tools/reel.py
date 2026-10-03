#!/usr/bin/env python3
"""
reel.py: builds a vertical Instagram reel (1080x1920, 30 fps, silent) from still scenes + a shot list.

  python3 tools/reel.py comic/instagram/reel1/shots.yaml

shots.yaml:
  out: reel1.mp4                      # written next to the yaml, plus stills/ (one PNG per shot, for a carousel)
  fps: 30
  shots:
    - card: {title: "GRAHA GOSSIP", sub: "presents", small: "Kitne saal the?"}   # full-frame title card
      dur: 2.2
    - image: scene1.png
      dur: 3.5
      zoom: in | out | pan-left | pan-right  (default in)
      focus: [0.5, 0.4]               # point (fractions) the zoom moves toward
      bubbles:                        # speech bubbles, comic lettering
        - {text: "Kitne saal the?", at: [0.5, 0.18], tail: [0.5, 0.33], size: 64}
      caption: "Saturn, opening the ledger."     # bottom caption box (optional)
      label: "SATURN · 19 YEARS"                  # small top label (optional)
    - card: {title: "...", lines: ["...", "..."]}
Transitions between shots are 0.5 s crossfades.
"""
import os, sys, subprocess, shutil, math
import yaml
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio_ffmpeg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = os.path.join(ROOT, "comic", "fonts")
FF = imageio_ffmpeg.get_ffmpeg_exe()
W, H = 1080, 1920
NAVY = (30, 42, 90); INK = (20, 20, 24); CREAM = (255, 247, 223); GOLD = (224, 185, 74); PAPER = (253, 251, 245)

def font(name, size): return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w or not cur: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def bubble(draw, text, at, tail, size, max_w=None):
    fnt = font("ComicNeue-Bold.ttf", size)
    max_w = max_w or int(W * 0.78)
    pad_x, pad_y = int(size * 0.8), int(size * 0.55)
    lines = wrap(draw, text, fnt, max_w - 2 * pad_x)
    lh = int(size * 1.12)
    tw = max(draw.textlength(l, font=fnt) for l in lines)
    bw, bh = int(tw + 2 * pad_x), int(len(lines) * lh + 2 * pad_y)
    cx, cy = at[0] * W, at[1] * H
    cx = min(max(cx, bw / 2 + 24), W - bw / 2 - 24)
    x0, y0 = int(cx - bw / 2), int(cy - bh / 2); x1, y1 = x0 + bw, y0 + bh
    stroke = max(4, size // 9)
    if tail:
        tx, ty = tail[0] * W, tail[1] * H
        bx = int(min(max(tx, x0 + size), x1 - size))
        base = int(size * 0.5)
        if ty > y1:   # tail downwards
            pts = [(bx - base, y1 - 2), (bx + base, y1 - 2), (int(tx), int(ty))]
        else:          # tail upwards
            pts = [(bx - base, y0 + 2), (bx + base, y0 + 2), (int(tx), int(ty))]
        draw.polygon(pts, fill="white", outline=INK)
        draw.line([pts[0], pts[2], pts[1]], fill=INK, width=stroke)
    draw.rounded_rectangle([x0, y0, x1, y1], radius=min(bh // 2, int(size * 1.4)), fill="white", outline=INK, width=stroke)
    if tail:
        yy = (y1 - stroke // 2 - 1) if ty > y1 else (y0 + stroke // 2 + 1)
        draw.line([(bx - base + 1, yy), (bx + base - 1, yy)], fill="white", width=stroke + 2)
    y = y0 + pad_y
    for ln in lines:
        draw.text((x0 + (bw - draw.textlength(ln, font=fnt)) / 2, y), ln, font=fnt, fill=INK); y += lh

def caption_box(draw, text, size=46, y_frac=0.86):
    fnt = font("PatrickHand.ttf", size)
    lines = wrap(draw, text, fnt, W - 160)
    lh = int(size * 1.2); bh = len(lines) * lh + 40
    y0 = int(H * y_frac - bh / 2)
    draw.rounded_rectangle([60, y0, W - 60, y0 + bh], radius=14, fill=CREAM, outline=INK, width=4)
    y = y0 + 20
    for ln in lines:
        draw.text(((W - draw.textlength(ln, font=fnt)) / 2, y), ln, font=fnt, fill=INK); y += lh

def label(draw, text):
    fnt = font("Nunito-ExtraBold.ttf", 34)
    tw = draw.textlength(text, font=fnt)
    draw.rounded_rectangle([W / 2 - tw / 2 - 26, 70, W / 2 + tw / 2 + 26, 134], radius=32, fill=NAVY)
    draw.text((W / 2 - tw / 2, 82), text, font=fnt, fill=GOLD)

def overlay_png(shot, path):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if shot.get("label"): label(d, shot["label"])
    for b in shot.get("bubbles") or []:
        bubble(d, b["text"], b.get("at", [0.5, 0.2]), b.get("tail"), b.get("size", 60), b.get("max_w"))
    if shot.get("caption"): caption_box(d, shot["caption"], shot.get("caption_size", 46), shot.get("caption_y", 0.86))
    im.save(path)

def card_png(card, path):
    im = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(im)
    # soft gradient
    for y in range(H):
        t = y / H
        col = tuple(int(a * (1 - t) + b * t) for a, b in zip((253, 243, 207), (220, 211, 240)))
        d.line([(0, y), (W, y)], fill=col)
    d.rectangle([40, 40, W - 40, H - 40], outline=(91, 106, 166), width=4)
    y = int(H * 0.30)
    if card.get("sub_top"):
        f = font("Nunito-ExtraBold.ttf", 40); t = card["sub_top"]
        d.text(((W - d.textlength(t, font=f)) / 2, y - 90), t, font=f, fill=(124, 134, 179))
    f = font("Bangers.ttf", card.get("title_size", 150))
    for ln in wrap(d, card.get("title", ""), f, W - 160):
        d.text(((W - d.textlength(ln, font=f)) / 2, y), ln, font=f, fill=NAVY); y += int(f.size * 1.0)
    if card.get("sub"):
        f = font("PatrickHand.ttf", 64); y += 30
        for ln in wrap(d, card["sub"], f, W - 200):
            d.text(((W - d.textlength(ln, font=f)) / 2, y), ln, font=f, fill=(43, 58, 120)); y += 76
    if card.get("lines"):
        f = font("ComicNeue-Bold.ttf", 52); y += 50
        for ln0 in card["lines"]:
            for ln in wrap(d, ln0, f, W - 220):
                d.text(((W - d.textlength(ln, font=f)) / 2, y), ln, font=f, fill=INK); y += 66
            y += 18
    if card.get("small"):
        f = font("Nunito-ExtraBold.ttf", 38); t = card["small"]
        d.text(((W - d.textlength(t, font=f)) / 2, H - 200), t, font=f, fill=(124, 134, 179))
    im.save(path)

def fit_image(src, path):
    im = Image.open(src).convert("RGB")
    r = max(W * 1.0 / im.width, H * 1.0 / im.height) * 1.08   # 8% larger so the zoom/pan never shows edges
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    im.save(path)
    return im.size

def build(yaml_path):
    cfg = yaml.safe_load(open(yaml_path, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(yaml_path))
    fps = cfg.get("fps", 30)
    tmp = os.path.join(base, "_build"); shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    stills = os.path.join(base, "stills"); os.makedirs(stills, exist_ok=True)
    clips = []
    for i, shot in enumerate(cfg["shots"]):
        dur = float(shot.get("dur", 3)); frames = int(dur * fps)
        clip = os.path.join(tmp, f"clip{i:02d}.mp4")
        if "card" in shot:
            png = os.path.join(tmp, f"card{i:02d}.png"); card_png(shot["card"], png)
            shutil.copy(png, os.path.join(stills, f"{i+1:02d}.png"))
            subprocess.run([FF, "-y", "-loglevel", "error", "-loop", "1", "-i", png, "-t", str(dur), "-r", str(fps),
                            "-vf", f"scale={W}:{H},format=yuv420p", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", clip], check=True)
        else:
            src = os.path.join(base, shot["image"])
            big = os.path.join(tmp, f"bg{i:02d}.png"); bw, bh = fit_image(src, big)
            ov = os.path.join(tmp, f"ov{i:02d}.png"); overlay_png(shot, ov)
            # still for carousel
            still = Image.open(big).convert("RGBA")
            l, t = (bw - W) // 2, (bh - H) // 2
            still = still.crop((l, t, l + W, t + H)); still.alpha_composite(Image.open(ov)); still.convert("RGB").save(os.path.join(stills, f"{i+1:02d}.png"))
            zoom = shot.get("zoom", "in"); fx, fy = shot.get("focus", [0.5, 0.45])
            zmax = 1.12
            if zoom == "in":
                z = f"min(1+{zmax-1}*on/{frames},{zmax})"
            elif zoom == "out":
                z = f"max({zmax}-{zmax-1}*on/{frames},1)"
            else:
                z = "1.06"
            # keep the focus point fixed on screen while zooming
            x = f"(iw*{fx})-(iw/zoom*{fx})"; y = f"(ih*{fy})-(ih/zoom*{fy})"
            if zoom == "pan-left": x = f"(iw-iw/zoom)*(1-on/{frames})"
            if zoom == "pan-right": x = f"(iw-iw/zoom)*(on/{frames})"
            vf = (f"[0:v]scale={bw}:{bh},zoompan=z='{z}':x='{x}':y='{y}':d={frames}:s={W}x{H}:fps={fps}[bg];"
                  f"[bg][1:v]overlay=0:0:format=auto,format=yuv420p[v]")
            subprocess.run([FF, "-y", "-loglevel", "error", "-loop", "1", "-i", big, "-i", ov, "-filter_complex", vf, "-map", "[v]",
                            "-t", str(dur), "-r", str(fps), "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", clip], check=True)
        clips.append((clip, dur))
    # crossfade concat
    xf = float(cfg.get("xfade", 0.5))
    inputs = [];
    for c, _ in clips: inputs += ["-i", c]
    if len(clips) == 1:
        shutil.copy(clips[0][0], os.path.join(base, cfg.get("out", "reel.mp4"))); return
    fc = []; prev = "[0:v]"; offset = 0.0
    for i in range(1, len(clips)):
        offset += clips[i - 1][1] - xf
        out = f"[x{i}]" if i < len(clips) - 1 else "[v]"
        fc.append(f"{prev}[{i}:v]xfade=transition=fade:duration={xf}:offset={offset:.3f}{out}")
        prev = out
    outp = os.path.join(base, cfg.get("out", "reel.mp4"))
    subprocess.run([FF, "-y", "-loglevel", "error"] + inputs + ["-filter_complex", ";".join(fc), "-map", "[v]",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", outp], check=True)
    total = sum(d for _, d in clips) - xf * (len(clips) - 1)
    print("wrote", outp, f"{total:.1f}s", "stills in", stills)
    shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    build(sys.argv[1])
