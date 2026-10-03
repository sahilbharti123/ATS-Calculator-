#!/usr/bin/env python3
"""
make_cover.py: builds the Book 2 front cover (1600x2560, KDP ebook size) from cover/cover-art.png
plus typography in the style of the Book 1 cover. Output: cover/cover-front.jpg and cover/cover-front.png.
Replace cover/cover-art.png with the full-resolution Canva export (page 11 of the character-sheet design)
and re-run; the art is resampled to fit, so any resolution works.
"""
import os, base64, subprocess, io
from PIL import Image, ImageFilter
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COV=os.path.join(ROOT,"cover")
W,H=1600,2560
CHROME_BAR=88   # headless Chromium counts a toolbar in --window-size; the screenshot viewport is this much shorter
ART_W,ART_H=1040,1560     # 2:3 panel
ART_X,ART_Y=(W-ART_W)//2,690

art_path=os.path.join(COV,"cover-art.png")
if not os.path.exists(art_path):
    art_path=os.path.join(COV,"cover-art-preview.png")
im=Image.open(art_path).convert("RGB")
# fit-and-crop to 2:3
r=max(ART_W/im.width, ART_H/im.height)
im=im.resize((round(im.width*r),round(im.height*r)),Image.LANCZOS)
l=(im.width-ART_W)//2; t=(im.height-ART_H)//2
im=im.crop((l,t,l+ART_W,t+ART_H))
if r>1.5: im=im.filter(ImageFilter.UnsharpMask(radius=2,percent=60,threshold=3))
buf=io.BytesIO(); im.save(buf,"PNG"); art_b64=base64.b64encode(buf.getvalue()).decode()

leaf='''<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
<path d="M60 8 C 63 40, 80 57, 112 60 C 80 63, 63 80, 60 112 C 57 80, 40 63, 8 60 C 40 57, 57 40, 60 8 Z" fill="#e0b94a"/>
<path d="M22 14 C 23 22, 28 27, 36 28 C 28 29, 23 34, 22 42 C 21 34, 16 29, 8 28 C 16 27, 21 22, 22 14 Z" fill="#8d9bd1"/>
<path d="M98 84 C 99 92, 104 97, 112 98 C 104 99, 99 104, 98 112 C 97 104, 92 99, 84 98 C 92 97, 97 92, 98 84 Z" fill="#8d9bd1"/></svg>'''
leaf_uri="data:image/svg+xml;base64,"+base64.b64encode(leaf.encode()).decode()

html=f'''<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="fonts/fonts.css">
<style>
html,body{{margin:0;padding:0}}
body{{width:{W}px;height:{H}px;overflow:hidden;position:relative;
 background:linear-gradient(180deg,#fdf3cf 0%,#f7eed6 18%,#e7eefb 45%,#dcd3f0 78%,#efe3ef 100%);
 font-family:'Nunito',sans-serif;color:#1e2a5a}}
.frame{{position:absolute;left:44px;top:44px;right:44px;bottom:44px;border:3px solid rgba(91,106,166,.55);border-radius:6px}}
.leaf{{position:absolute;width:110px;height:110px;background:url("{leaf_uri}") no-repeat center/contain;opacity:.9}}
.tl{{left:70px;top:70px}} .tr{{right:70px;top:70px}}
.bl{{left:70px;bottom:70px}} .br{{right:70px;bottom:70px}}
.star{{position:absolute;color:#e0b94a;font-size:40px}}
h1{{position:absolute;left:0;right:0;top:118px;margin:0;text-align:center;font-family:'Fraunces',serif;font-weight:700;
 font-size:170px;line-height:.95;letter-spacing:-2px;color:#1e2a5a;text-shadow:0 3px 0 rgba(255,255,255,.6)}}
h1 small{{display:block;font-size:112px;font-weight:600;letter-spacing:0}}
.sub{{position:absolute;left:160px;right:160px;top:520px;text-align:center;font-size:42px;font-weight:600;line-height:1.3;color:#2b3a78}}
.art{{position:absolute;left:{ART_X}px;top:{ART_Y}px;width:{ART_W}px;height:{ART_H}px;border-radius:28px;overflow:hidden;
 box-shadow:0 30px 70px rgba(60,60,120,.25), 0 0 0 10px rgba(255,255,255,.55)}}
.art img{{width:100%;height:100%;display:block}}
.art:after{{content:"";position:absolute;inset:0;border-radius:28px;box-shadow:inset 0 0 60px rgba(255,245,220,.35)}}
.tag{{position:absolute;left:120px;right:120px;top:2290px;text-align:center;font-size:36px;font-weight:600;line-height:1.35;color:#2b3a78}}
.author{{position:absolute;left:0;right:0;top:2400px;text-align:center;font-family:'Fraunces',serif;font-style:italic;font-weight:500;font-size:40px;color:#1e2a5a;letter-spacing:1px}}
.series{{position:absolute;left:0;right:0;top:60px;text-align:center;font-size:26px;font-weight:700;letter-spacing:5px;text-transform:uppercase;color:#7c86b3}}
</style></head><body>
<div class="frame"></div>
<div class="leaf tl"></div><div class="leaf tr"></div><div class="leaf bl"></div><div class="leaf br"></div>
<div class="series">Astrology, Gently &nbsp;·&nbsp; Book Two</div>
<h1>Your Life<small>in Seasons</small></h1>
<div class="sub">A kind guide to the dasha system<br>and what each season of your life is asking of you</div>
<div class="art"><img src="data:image/png;base64,{art_b64}"></div>
<div class="tag">Plain words. A reason for every rule.<br>And no fear.</div>
<div class="author">Anushka Bharti</div>
</body></html>'''
page=os.path.join(COV,"cover-front.html"); open(page,"w",encoding="utf-8").write(html)
CHROME="/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
png=os.path.join(COV,"cover-front.png")
subprocess.run([CHROME,"--headless","--no-sandbox","--disable-gpu","--hide-scrollbars","--allow-file-access-from-files",
    f"--window-size={W},{H+CHROME_BAR}",f"--screenshot={png}",f"file://{page}"],capture_output=True,timeout=120)
raw=Image.open(png); print("screenshot",raw.size); out=raw.convert("RGB").crop((0,0,W,H)); out.save(png)
out.save(os.path.join(COV,"cover-front.jpg"),"JPEG",quality=92)
os.remove(page)
print("cover/cover-front.jpg", out.size, "art source:", os.path.basename(art_path), im.size)
