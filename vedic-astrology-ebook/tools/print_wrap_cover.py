#!/usr/bin/env python3
"""
print_wrap_cover.py — builds the KDP paperback full-wrap cover (back + spine + front) for a 6x9 in book.
Usage: python3 tools/print_wrap_cover.py <page_count>   → cover/cover-paperback-wrap.pdf and .png
KDP white paper: spine = pages × 0.002252 in; bleed 0.125 in on all outer edges.
"""
import sys, os, subprocess, base64
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pages=int(sys.argv[1]); spine=pages*0.002252
W=6.0; H=9.0; B=0.125
total_w=2*W+spine+2*B; total_h=H+2*B
DPI=300
px=lambda inch: round(inch*DPI)
front_b64=base64.b64encode(open(os.path.join(ROOT,"cover","cover-front.jpg"),"rb").read()).decode()
back_text=[
 "You bought the books everyone recommends. You opened them",
 "with real hope. And within ten pages you felt stupid.",
 "",
 "You are not stupid. Those books were written for students who",
 "already knew the sky. This one is written for everyone else.",
 "",
 "Astrology, Gently teaches Vedic astrology as a language with",
 "a small grammar: nine planets, twelve signs, twelve houses,",
 "twenty-seven stars. Every rule comes with its reason. Every hard",
 "idea comes with a story from a royal court you will never forget.",
 "Every table is colour-coded. Lal Kitab is clearly labelled",
 "wherever it appears, so you always know which system you are in.",
 "",
 "By the last page you will read a full chart, time the seasons of",
 "a life, answer the questions people actually ask about work,",
 "money, love, health and children, and sit across from someone",
 "with kindness and confidence. And if you never read for anyone",
 "but yourself and the people you love, you will still understand",
 "your own life a great deal better. That is the real reason this",
 "book was written.",
]
lines="".join(f'<text x="{px(B+0.6)}" y="{px(B+1.6)+i*px(0.26)}" font-size="{px(0.17)}" fill="#2b3350">{t}</text>' for i,t in enumerate(back_text))
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{px(total_w)}" height="{px(total_h)}" viewBox="0 0 {px(total_w)} {px(total_h)}" font-family="'Liberation Serif', Georgia, serif">
<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fdf3c9"/><stop offset="0.5" stop-color="#e8eef8"/><stop offset="1" stop-color="#d9c9ec"/></linearGradient></defs>
<rect width="100%" height="100%" fill="url(#g)"/>
<!-- back cover -->
<rect x="{px(B+0.35)}" y="{px(B+0.35)}" width="{px(W-0.7)}" height="{px(H-0.7)}" fill="none" stroke="#7c86b3" stroke-width="2"/>
<text x="{px(B+W/2)}" y="{px(B+1.05)}" text-anchor="middle" font-size="{px(0.28)}" font-weight="bold" fill="#1e2a5a">A gentle place to begin</text>
{lines}
<text x="{px(B+W/2)}" y="{px(B+H-1.35)}" text-anchor="middle" font-size="{px(0.16)}" font-style="italic" fill="#2b3350">Anushka Bharti is a practising astrologer who taught herself Jyotish</text>
<text x="{px(B+W/2)}" y="{px(B+H-1.10)}" text-anchor="middle" font-size="{px(0.16)}" font-style="italic" fill="#2b3350">after the classics failed her. This is her first book.</text>
<rect x="{px(B+W-2.1)}" y="{px(B+H-0.95)}" width="{px(1.6)}" height="{px(0.55)}" fill="#ffffff" stroke="#b8956a" stroke-width="1"/>
<text x="{px(B+W-1.3)}" y="{px(B+H-0.62)}" text-anchor="middle" font-size="{px(0.1)}" fill="#999">ISBN barcode area</text>
<!-- spine -->
<rect x="{px(B+W)}" y="0" width="{px(spine)}" height="{px(total_h)}" fill="#1e2a5a"/>
<text transform="translate({px(B+W+spine/2)},{px(total_h/2)}) rotate(90)" text-anchor="middle" font-size="{px(min(0.22, spine*0.42))}" fill="#fdf3c9" letter-spacing="2">Astrology, Gently &#160;&#160;·&#160;&#160; Anushka Bharti</text>
<!-- front cover -->
<image x="{px(B+W+spine)}" y="{px(B)}" width="{px(W)}" height="{px(H)}" preserveAspectRatio="none" xlink:href="data:image/jpeg;base64,{front_b64}"/>
</svg>'''
out_svg=os.path.join(ROOT,"cover","cover-paperback-wrap.svg"); open(out_svg,"w",encoding="utf-8").write(svg)
html=os.path.join(ROOT,"cover","_wrap.html"); open(html,"w").write(f'<html><body style="margin:0"><img style="display:block" src="file://{out_svg}" width="{px(total_w)}" height="{px(total_h)}"></body></html>')
CHROME="/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
png=os.path.join(ROOT,"cover","cover-paperback-wrap.png")
subprocess.run([CHROME,"--headless","--no-sandbox","--disable-gpu","--hide-scrollbars",f"--window-size={px(total_w)},{px(total_h)+88}",f"--screenshot={png}",f"file://{html}"],capture_output=True,timeout=120)
from PIL import Image
im=Image.open(png).convert("RGB").crop((0,0,px(total_w),px(total_h))); im.save(png); im.save(os.path.join(ROOT,"cover","cover-paperback-wrap.pdf"),"PDF",resolution=DPI)
os.remove(html)
print(f"pages={pages} spine={spine:.3f}in wrap={total_w:.3f}x{total_h:.3f}in → cover/cover-paperback-wrap.pdf/.png ({im.size})")
