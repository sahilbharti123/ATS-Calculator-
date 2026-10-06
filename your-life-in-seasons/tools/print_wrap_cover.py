#!/usr/bin/env python3
"""
print_wrap_cover.py — builds the KDP paperback full-wrap cover for Your Life in Seasons (back + spine + front) for a 6x9 in book.
Usage: python3 tools/print_wrap_cover.py <page_count>           → cover/cover-paperback-wrap.pdf and .png
       python3 tools/print_wrap_cover.py <page_count> --comic   → cover/cover-comic-paperback-wrap.pdf and .png
KDP white paper: spine = pages × 0.002252 in; premium colour paper (the comic): pages × 0.002347 in.
Bleed 0.125 in on all outer edges.
"""
import sys, os, subprocess, base64
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pages=int(sys.argv[1]); COMIC="--comic" in sys.argv
spine=pages*(0.002347 if COMIC else 0.002252)
NAME="cover-comic-paperback-wrap" if COMIC else "cover-paperback-wrap"
W=6.0; H=9.0; B=0.125
total_w=2*W+spine+2*B; total_h=H+2*B
DPI=300
px=lambda inch: round(inch*DPI)
# front art, with its outer edges stretched into the bleed (top, right, bottom) so trim drift never shows a seam
import io
from PIL import Image as _I
_f=_I.open(os.path.join(ROOT,"cover","cover-comic-front.jpg" if COMIC else "cover-front.jpg")).convert("RGB").resize((px(W),px(H)),_I.LANCZOS)
_e=_I.new("RGB",(px(W)+px(B),px(H)+2*px(B))); _e.paste(_f,(0,px(B)))
_e.paste(_f.crop((0,0,px(W),1)).resize((px(W),px(B))),(0,0)); _e.paste(_f.crop((0,px(H)-1,px(W),px(H))).resize((px(W),px(B))),(0,px(B)+px(H)))
_e.paste(_e.crop((px(W)-1,0,px(W),_e.height)).resize((px(B),_e.height)),(px(W),0))
_buf=io.BytesIO(); _e.save(_buf,"JPEG",quality=92); front_b64=base64.b64encode(_buf.getvalue()).decode()
back_text=[
 "The most common question an astrologer is asked is not",
 "\"what am I like?\" It is \"how long will this last?\"",
 "",
 "Vedic astrology has a beautiful answer. A life is not one long",
 "road. It moves in seasons, each run by one of the nine planets",
 "for a fixed number of years, in a fixed order, and the season",
 "you are born into depends on where the Moon stood the night",
 "you arrived. Astrologers call it the dasha system. This book",
 "calls it what it is: the seasons of your life.",
 "",
 "Written entirely in plain English, with every Sanskrit word",
 "explained once and then set aside, Your Life in Seasons walks",
 "you through all nine seasons and the sub-seasons inside them,",
 "shows you how to find where you are, and tells you, kindly and",
 "specifically, what each season tends to ask of you and what to",
 "do about it. Three worked lives show the whole method, and a",
 "cast of comic-strip planets keeps you company along the way.",
 "",
 "A hard season is a season with a task, not a verdict. By the",
 "last page you will have drawn your own season map and will",
 "know, roughly, how long the weather will hold.",
]
HEAD="How long will this last?"
SERIES="Your Life in Seasons is the second book in the series."
if COMIC:
    HEAD="Who is running your life right now?"
    SERIES="This is the comic edition of Your Life in Seasons."
    back_text=[
 "Vedic astrology says a life moves in seasons. Each one is run",
 "by one of the nine planets for a fixed number of years, with a",
 "deputy inside it and an intern inside that. So if you are in a",
 "Mars season with a Venus deputy and a Sun intern, what does",
 "that actually feel like on a Tuesday?",
 "",
 "This comic shows you. The nine planets move into your flat one",
 "after another: Saturn the Judge with his ledger, Venus with her",
 "brunch plans, Mars with a five a.m. drill, Rahu with a drone and",
 "a shopping bag, Jupiter with laddoos and advice. You live with",
 "each of them, argue with them, and learn what each season is",
 "asking of you.",
 "",
 "Every chapter ends with plain homework for that season, and the",
 "last pages help you draw your own season map. A hard season is",
 "a season with a task, not a verdict.",
]
lines="".join(f'<text x="{px(B+0.6)}" y="{px(B+1.6)+i*px(0.26)}" font-size="{px(0.17)}" fill="#2b3350">{t}</text>' for i,t in enumerate(back_text))
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{px(total_w)}" height="{px(total_h)}" viewBox="0 0 {px(total_w)} {px(total_h)}" font-family="'Liberation Serif', Georgia, serif">
<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fdf3c9"/><stop offset="0.5" stop-color="#e8eef8"/><stop offset="1" stop-color="#d9c9ec"/></linearGradient></defs>
<rect width="100%" height="100%" fill="url(#g)"/>
<!-- back cover -->
<rect x="{px(B+0.35)}" y="{px(B+0.35)}" width="{px(W-0.7)}" height="{px(H-0.7)}" fill="none" stroke="#7c86b3" stroke-width="2"/>
<text x="{px(B+W/2)}" y="{px(B+1.05)}" text-anchor="middle" font-size="{px(0.28)}" font-weight="bold" fill="#1e2a5a">{HEAD}</text>
{lines}
<text x="{px(B+W/2)}" y="{px(B+H-1.35)}" text-anchor="middle" font-size="{px(0.16)}" font-style="italic" fill="#2b3350">Anushka Bharti is a practising astrologer and the author of Astrology, Gently.</text>
<text x="{px(B+W/2)}" y="{px(B+H-1.10)}" text-anchor="middle" font-size="{px(0.16)}" font-style="italic" fill="#2b3350">{SERIES}</text>
<rect x="{px(B+W-2.1)}" y="{px(B+H-0.95)}" width="{px(1.6)}" height="{px(0.55)}" fill="#ffffff" stroke="#b8956a" stroke-width="1"/>
<text x="{px(B+W-1.3)}" y="{px(B+H-0.62)}" text-anchor="middle" font-size="{px(0.1)}" fill="#999">ISBN barcode area</text>
<!-- spine -->
<rect x="{px(B+W)}" y="0" width="{px(spine)}" height="{px(total_h)}" fill="#1e2a5a"/>
<text transform="translate({px(B+W+spine/2)},{px(total_h/2)}) rotate(90)" text-anchor="middle" font-size="{px(min(0.22, spine*0.42))}" fill="#fdf3c9" letter-spacing="2">Your Life in Seasons{": The Comic" if COMIC else ""} &#160;&#160;·&#160;&#160; Anushka Bharti</text>
<!-- front cover -->
<image x="{px(B+W+spine)}" y="0" width="{px(W)+px(B)}" height="{px(H)+2*px(B)}" preserveAspectRatio="none" xlink:href="data:image/jpeg;base64,{front_b64}"/>
</svg>'''
out_svg=os.path.join(ROOT,"cover",NAME+".svg"); open(out_svg,"w",encoding="utf-8").write(svg)
html=os.path.join(ROOT,"cover","_wrap.html"); open(html,"w").write(f'<html><body style="margin:0"><img style="display:block" src="file://{out_svg}" width="{-(-px(total_w)//3)}" height="{-(-px(total_h)//3)}"></body></html>')
CHROME="/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
png=os.path.join(ROOT,"cover",NAME+".png")
# one-third size at 3x device scale; the extra 88 px of window height is headless Chromium's toolbar allowance, cropped below
subprocess.run([CHROME,"--headless","--no-sandbox","--disable-gpu","--hide-scrollbars","--force-device-scale-factor=3",f"--window-size={-(-px(total_w)//3)},{-(-px(total_h)//3)+88}",f"--screenshot={png}",f"file://{html}"],capture_output=True,timeout=120)
from PIL import Image
im=Image.open(png).convert("RGB").crop((0,0,px(total_w),px(total_h))); im.save(png); im.save(os.path.join(ROOT,"cover",NAME+".pdf"),"PDF",resolution=DPI)
os.remove(html)
print(f"pages={pages} spine={spine:.3f}in wrap={total_w:.3f}x{total_h:.3f}in → cover/{NAME}.pdf/.png ({im.size})")
