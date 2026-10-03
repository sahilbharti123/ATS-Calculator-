#!/usr/bin/env python3
"""svg2png.py — renders every images/*.svg to images_png/*.png (2x) with headless Chromium, for the EPUB."""
import os, re, glob, subprocess, sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC=os.path.join(ROOT,"images"); DST=os.path.join(ROOT,"images_png"); os.makedirs(DST,exist_ok=True)
CHROME="/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
CHROME_BAR=88  # headless Chromium counts a toolbar in --window-size; without this the bottom of every figure is cut off
TMP=os.path.join(ROOT,"dist","_svgpage.html")
os.makedirs(os.path.dirname(TMP),exist_ok=True)
files=sorted(glob.glob(os.path.join(SRC,"*.svg")))
only=[a for a in sys.argv[1:]]
for f in files:
    name=os.path.basename(f)[:-4]
    out=os.path.join(DST,name+".png")
    if only and name not in only: continue
    if os.path.exists(out) and os.path.getmtime(out)>os.path.getmtime(f): continue
    s=open(f,encoding="utf-8").read()
    w=int(float(re.search(r'width=["\']([\d.]+)["\']',s).group(1))); h=int(float(re.search(r'height=["\']([\d.]+)["\']',s).group(1)))
    open(TMP,"w").write(f'<html><body style="margin:0;background:#fff"><img src="file://{f}" width="{w}" height="{h}"></body></html>')
    subprocess.run([CHROME,"--headless","--no-sandbox","--disable-gpu","--hide-scrollbars","--force-device-scale-factor=2",
                    f"--window-size={w},{h+CHROME_BAR}",f"--screenshot={out}",f"file://{TMP}"],capture_output=True,timeout=60)
    if os.path.exists(out):
        from PIL import Image
        im=Image.open(out); im.crop((0,0,2*w,2*h)).save(out)
    print("ok" if os.path.exists(out) else "FAIL", name)
if os.path.exists(TMP): os.remove(TMP)
