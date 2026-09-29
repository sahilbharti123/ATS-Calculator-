#!/usr/bin/env python3
"""
kundali_svg.py: draws Vedic astrology diagrams as clean SVG files.

Usage examples
--------------
# North Indian chart: Lagna in Leo (sign 5); planets given as house:planets
python3 kundali_svg.py north --lagna 5 --planets "1:Su,Me;4:Ju;7:Sa(R);9:Mo" \
    --title "Example: Leo Lagna" --out ../images/example.svg

# Same chart, South Indian style
python3 kundali_svg.py south --lagna 5 --planets "1:Su,Me;4:Ju;7:Sa;9:Mo" --out ../images/example-south.svg

# Highlight houses (e.g. aspects) : --highlight "1,4,7,10"
# Lal Kitab chart (houses fixed, no signs): kundali_svg.py lalkitab --planets "1:Su;2:Ju" --out x.svg

Planet codes: Su Mo Ma Me Ju Ve Sa Ra Ke  (add (R) for retrograde, e.g. Sa(R))
Sign numbers: 1 Aries, 2 Taurus, 3 Gemini, 4 Cancer, 5 Leo, 6 Virgo,
              7 Libra, 8 Scorpio, 9 Sagittarius, 10 Capricorn, 11 Aquarius, 12 Pisces
"""
import argparse, math, sys, os

SIGNS = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio",
         "Sagittarius","Capricorn","Aquarius","Pisces"]
SIGN_ABBR = ["Ar","Ta","Ge","Cn","Le","Vi","Li","Sc","Sg","Cp","Aq","Pi"]
SIGN_LORD = ["Ma","Ve","Me","Mo","Su","Me","Ve","Ma","Ju","Sa","Sa","Ju"]
PLANET_NAME = {"Su":"Sun","Mo":"Moon","Ma":"Mars","Me":"Mercury","Ju":"Jupiter",
               "Ve":"Venus","Sa":"Saturn","Ra":"Rahu","Ke":"Ketu","As":"Lagna"}
PLANET_COLOR = {"Su":"#c2410c","Mo":"#4b5563","Ma":"#b91c1c","Me":"#15803d","Ju":"#b45309",
                "Ve":"#be185d","Sa":"#1e3a8a","Ra":"#4c1d95","Ke":"#6b21a8","As":"#000000"}

INK = "#3b2314"        # dark brown line colour
PAPER = "#fffaf0"      # cream background
GOLD = "#b8860b"
HILITE = "#fde68a"     # soft yellow highlight
HILITE2 = "#bbf7d0"    # soft green highlight
MAROON = "#7f1d1d"

def esc(s):
    return (s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"))

def parse_planets(spec):
    """'1:Su,Me;4:Ju' -> {1:['Su','Me'],4:['Ju']}"""
    out = {}
    if not spec:
        return out
    for part in spec.split(";"):
        part = part.strip()
        if not part:
            continue
        k, v = part.split(":")
        out[int(k)] = [p.strip() for p in v.split(",") if p.strip()]
    return out

def planet_label(code):
    """'Sa(R)' -> ('Sa', True)"""
    retro = code.endswith("(R)")
    base = code.replace("(R)","")
    return base, retro

def svg_header(w, h, title=None):
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Georgia, \'Times New Roman\', serif">']
    s.append(f'<rect x="0" y="0" width="{w}" height="{h}" rx="12" fill="{PAPER}" stroke="{GOLD}" stroke-width="2"/>')
    if title:
        s.append(f'<text x="{w/2}" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="{MAROON}">{esc(title)}</text>')
    return s

def planets_text(x, y, plist, size=15, line=18, anchor="middle"):
    """Stack planets vertically centred at (x,y)."""
    out = []
    n = len(plist)
    if n == 0:
        return out
    start = y - (n-1)*line/2
    for i, code in enumerate(plist):
        base, retro = planet_label(code)
        col = PLANET_COLOR.get(base, INK)
        label = base + ("ᴿ" if retro else "")
        out.append(f'<text x="{x}" y="{start+i*line+size*0.35}" text-anchor="{anchor}" font-size="{size}" font-weight="bold" fill="{col}">{esc(label)}</text>')
    return out

# ---------------------------------------------------------------- NORTH INDIAN
def north_chart(lagna, planets, title=None, highlight=None, size=440, house_labels=True,
                caption=None, show_sign_names=False):
    S = size
    pad_top = 45 if title else 10
    pad_bottom = 40 if caption else 10
    W = S + 20
    H = S + pad_top + pad_bottom
    ox, oy = 10, pad_top
    svg = svg_header(W, H, title)
    hl = set(highlight or [])

    def P(x, y):
        return f"{ox+x},{oy+y}"

    # house polygons (vertices) and label centres
    T=(S/2,0); R=(S,S/2); B=(S/2,S); L=(0,S/2); C=(S/2,S/2)
    a=(S/4,S/4); b=(3*S/4,S/4); c=(3*S/4,3*S/4); d=(S/4,3*S/4)
    TL=(0,0); TR=(S,0); BR=(S,S); BL=(0,S)
    houses = {
        1: ([T,b,C,a], (S/2, S/4)),
        2: ([TL,T,a], (S/4, S/9)),
        3: ([TL,a,L], (S/9, S/4)),
        4: ([L,a,C,d], (S/4, S/2)),
        5: ([BL,L,d], (S/9, 3*S/4)),
        6: ([BL,d,B], (S/4, 8*S/9)),
        7: ([B,d,C,c], (S/2, 3*S/4)),
        8: ([BR,B,c], (3*S/4, 8*S/9)),
        9: ([BR,c,R], (8*S/9, 3*S/4)),
        10:([R,c,C,b], (3*S/4, S/2)),
        11:([TR,R,b], (8*S/9, S/4)),
        12:([TR,b,T], (3*S/4, S/9)),
    }
    # sign-number label positions (near the inner corner of each house)
    sign_pos = {
        1:(S/2, S/2-30), 2:(S/4, S/4-14), 3:(S/4-16, S/4+5), 4:(S/2-30, S/2+5),
        5:(S/4-16, 3*S/4+5), 6:(S/4, 3*S/4+20), 7:(S/2, S/2+40), 8:(3*S/4, 3*S/4+20),
        9:(3*S/4+16, 3*S/4+5), 10:(S/2+30, S/2+5), 11:(3*S/4+16, S/4+5), 12:(3*S/4, S/4-14)
    }
    for h, (poly, centre) in houses.items():
        pts = " ".join(P(*v) for v in poly)
        fill = HILITE if h in hl else "none"
        svg.append(f'<polygon points="{pts}" fill="{fill}" stroke="none"/>')
    # lines
    svg.append(f'<rect x="{ox}" y="{oy}" width="{S}" height="{S}" fill="none" stroke="{INK}" stroke-width="2.5"/>')
    svg.append(f'<line x1="{ox}" y1="{oy}" x2="{ox+S}" y2="{oy+S}" stroke="{INK}" stroke-width="2"/>')
    svg.append(f'<line x1="{ox+S}" y1="{oy}" x2="{ox}" y2="{oy+S}" stroke="{INK}" stroke-width="2"/>')
    svg.append(f'<polygon points="{P(*T)} {P(*R)} {P(*B)} {P(*L)}" fill="none" stroke="{INK}" stroke-width="2"/>')

    for h, (poly, centre) in houses.items():
        sign = ((lagna - 1 + h - 1) % 12) + 1
        sx, sy = sign_pos[h]
        label = SIGN_ABBR[sign-1] if show_sign_names else str(sign)
        svg.append(f'<text x="{ox+sx}" y="{oy+sy}" text-anchor="middle" font-size="12" fill="{GOLD}" font-weight="bold">{label}</text>')
        cx, cy = centre
        plist = planets.get(h, [])
        if h == 1:
            plist = ["As"] + [p for p in plist if p != "As"] if "As" not in plist else plist
        # smaller font for triangular houses
        fs = 15 if h in (1,4,7,10) else 13
        ln = 17 if h in (1,4,7,10) else 14
        if len(plist) > 3 and h not in (1,4,7,10):
            # two columns for crowded corner houses
            col1, col2 = plist[0::2], plist[1::2]
            svg += planets_text(ox+cx-14, oy+cy, col1, size=fs, line=ln)
            svg += planets_text(ox+cx+14, oy+cy, col2, size=fs, line=ln)
        else:
            svg += planets_text(ox+cx, oy+cy, plist, size=fs, line=ln)
        if house_labels:
            # tiny house number at the outer edge for beginners
            pass
    if caption:
        svg.append(f'<text x="{W/2}" y="{H-14}" text-anchor="middle" font-size="13" fill="{INK}" font-style="italic">{esc(caption)}</text>')
    svg.append("</svg>")
    return "\n".join(svg)

# ---------------------------------------------------------------- SOUTH INDIAN
def south_chart(lagna, planets, title=None, highlight=None, size=440, caption=None):
    """planets is keyed by HOUSE (same as north) and converted to signs here."""
    S = size; cell = S/4
    pad_top = 45 if title else 10
    pad_bottom = 40 if caption else 10
    W = S + 20; H = S + pad_top + pad_bottom
    ox, oy = 10, pad_top
    svg = svg_header(W, H, title)
    hl = set(highlight or [])
    # grid position (col,row) of each sign 1..12
    grid = {12:(0,0),1:(1,0),2:(2,0),3:(3,0),4:(3,1),5:(3,2),6:(3,3),7:(2,3),8:(1,3),9:(0,3),10:(0,2),11:(0,1)}
    # house -> sign
    by_sign = {}
    for h, plist in planets.items():
        sign = ((lagna-1+h-1)%12)+1
        by_sign.setdefault(sign, []).extend(plist)
    for sign, (col,row) in grid.items():
        x = ox+col*cell; y = oy+row*cell
        house = ((sign - lagna) % 12) + 1
        fill = HILITE if house in hl else "none"
        svg.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" fill="{fill}" stroke="{INK}" stroke-width="2"/>')
        svg.append(f'<text x="{x+6}" y="{y+16}" font-size="11" fill="{GOLD}" font-weight="bold">{SIGN_ABBR[sign-1]}</text>')
        svg.append(f'<text x="{x+cell-6}" y="{y+16}" font-size="11" text-anchor="end" fill="#9ca3af">H{house}</text>')
        if sign == lagna:
            svg.append(f'<line x1="{x}" y1="{y+26}" x2="{x+26}" y2="{y}" stroke="{MAROON}" stroke-width="2.5"/>')
        plist = by_sign.get(sign, [])
        svg += planets_text(x+cell/2, y+cell/2+6, plist, size=14, line=16)
    # centre text
    svg.append(f'<text x="{ox+S/2}" y="{oy+S/2-8}" text-anchor="middle" font-size="14" fill="{MAROON}" font-weight="bold">Rasi Chart</text>')
    svg.append(f'<text x="{ox+S/2}" y="{oy+S/2+12}" text-anchor="middle" font-size="12" fill="{INK}">Lagna: {SIGNS[lagna-1]}</text>')
    svg.append(f'<text x="{ox+S/2}" y="{oy+S/2+30}" text-anchor="middle" font-size="11" fill="#6b7280">(signs fixed; slash marks Lagna)</text>')
    if caption:
        svg.append(f'<text x="{W/2}" y="{H-14}" text-anchor="middle" font-size="13" fill="{INK}" font-style="italic">{esc(caption)}</text>')
    svg.append("</svg>")
    return "\n".join(svg)

# ---------------------------------------------------------------- LAL KITAB
def lalkitab_chart(planets, title=None, caption=None, size=440):
    """Lal Kitab uses the North Indian diamond but houses are FIXED (house 1 = Aries always),
    so only house numbers are printed."""
    svg = north_chart(1, planets, title=title, size=size, caption=caption)
    return svg

# ---------------------------------------------------------------- ZODIAC WHEEL
def zodiac_wheel(title="The Zodiac Belt (Rashi Chakra)", caption=None, size=520, mode="lords"):
    W = H = size + (50 if title else 10) + (35 if caption else 0)
    cx = size/2 + 10; cy = size/2 + (45 if title else 10)
    R = size/2 - 10; r_in = R*0.58
    svg = svg_header(W, H, title)
    ELEMENT = ["Fire","Earth","Air","Water"]
    ELEM_COL = {"Fire":"#fecaca","Earth":"#d9f99d","Air":"#bae6fd","Water":"#ddd6fe"}
    for i in range(12):
        # Aries starts at 9 o'clock, going counter-clockwise (as in the sky)
        a0 = math.radians(180 - i*30); a1 = math.radians(180 - (i+1)*30)
        x0,y0 = cx+R*math.cos(a0), cy-R*math.sin(a0)
        x1,y1 = cx+R*math.cos(a1), cy-R*math.sin(a1)
        xi0,yi0 = cx+r_in*math.cos(a0), cy-r_in*math.sin(a0)
        xi1,yi1 = cx+r_in*math.cos(a1), cy-r_in*math.sin(a1)
        elem = ELEMENT[i%4]
        path = f'M{x0},{y0} A{R},{R} 0 0 0 {x1},{y1} L{xi1},{yi1} A{r_in},{r_in} 0 0 1 {xi0},{yi0} Z'
        svg.append(f'<path d="{path}" fill="{ELEM_COL[elem]}" stroke="{INK}" stroke-width="1.5"/>')
        am = math.radians(180 - (i+0.5)*30); rm = (R+r_in)/2
        tx,ty = cx+rm*math.cos(am), cy-rm*math.sin(am)
        svg.append(f'<text x="{tx}" y="{ty-6}" text-anchor="middle" font-size="13" font-weight="bold" fill="{INK}">{i+1}. {SIGNS[i]}</text>')
        sub = f'Lord: {PLANET_NAME[SIGN_LORD[i]]}' if mode=="lords" else elem
        svg.append(f'<text x="{tx}" y="{ty+11}" text-anchor="middle" font-size="11" fill="{MAROON}">{sub}</text>')
    svg.append(f'<circle cx="{cx}" cy="{cy}" r="{r_in}" fill="{PAPER}" stroke="{INK}" stroke-width="1.5"/>')
    svg.append(f'<text x="{cx}" y="{cy-30}" text-anchor="middle" font-size="14" font-weight="bold" fill="{MAROON}">12 signs × 30° = 360°</text>')
    svg.append(f'<text x="{cx}" y="{cy-8}" text-anchor="middle" font-size="12" fill="{INK}">Order runs anti-clockwise,</text>')
    svg.append(f'<text x="{cx}" y="{cy+10}" text-anchor="middle" font-size="12" fill="{INK}">Aries → Pisces, as the Moon moves.</text>')
    # legend
    lx = cx - 95; ly = cy + 35
    for j, e in enumerate(ELEMENT):
        svg.append(f'<rect x="{lx + j*50}" y="{ly}" width="12" height="12" fill="{ELEM_COL[e]}" stroke="{INK}"/>')
        svg.append(f'<text x="{lx + j*50 + 16}" y="{ly+11}" font-size="11" fill="{INK}">{e}</text>')
    if caption:
        svg.append(f'<text x="{W/2}" y="{H-12}" text-anchor="middle" font-size="13" fill="{INK}" font-style="italic">{esc(caption)}</text>')
    svg.append("</svg>")
    return "\n".join(svg)

# ---------------------------------------------------------------- NAKSHATRA WHEEL
NAKS = [("Ashwini","Ke"),("Bharani","Ve"),("Krittika","Su"),("Rohini","Mo"),("Mrigashira","Ma"),
        ("Ardra","Ra"),("Punarvasu","Ju"),("Pushya","Sa"),("Ashlesha","Me"),("Magha","Ke"),
        ("P.Phalguni","Ve"),("U.Phalguni","Su"),("Hasta","Mo"),("Chitra","Ma"),("Swati","Ra"),
        ("Vishakha","Ju"),("Anuradha","Sa"),("Jyeshtha","Me"),("Mula","Ke"),("P.Ashadha","Ve"),
        ("U.Ashadha","Su"),("Shravana","Mo"),("Dhanishta","Ma"),("Shatabhisha","Ra"),
        ("P.Bhadrapada","Ju"),("U.Bhadrapada","Sa"),("Revati","Me")]
LORD_COL = {"Ke":"#e9d5ff","Ve":"#fbcfe8","Su":"#fed7aa","Mo":"#e5e7eb","Ma":"#fecaca","Ra":"#c7d2fe",
            "Ju":"#fde68a","Sa":"#bfdbfe","Me":"#bbf7d0"}

def nakshatra_wheel(title="The 27 Nakshatras and their Vimshottari lords", caption=None, size=640):
    W = H = size + (50 if title else 10) + (35 if caption else 0)
    cx = size/2 + 10; cy = size/2 + (45 if title else 10)
    R = size/2 - 10; r_mid = R*0.74; r_in = R*0.56
    svg = svg_header(W, H, title)
    # outer ring: nakshatras
    for i, (name, lord) in enumerate(NAKS):
        a0 = math.radians(180 - i*(360/27)); a1 = math.radians(180 - (i+1)*(360/27))
        x0,y0 = cx+R*math.cos(a0), cy-R*math.sin(a0); x1,y1 = cx+R*math.cos(a1), cy-R*math.sin(a1)
        xi0,yi0 = cx+r_mid*math.cos(a0), cy-r_mid*math.sin(a0); xi1,yi1 = cx+r_mid*math.cos(a1), cy-r_mid*math.sin(a1)
        path = f'M{x0},{y0} A{R},{R} 0 0 0 {x1},{y1} L{xi1},{yi1} A{r_mid},{r_mid} 0 0 1 {xi0},{yi0} Z'
        svg.append(f'<path d="{path}" fill="{LORD_COL[lord]}" stroke="{INK}" stroke-width="1"/>')
        am = math.radians(180 - (i+0.5)*(360/27)); rm = (R+r_mid)/2
        tx,ty = cx+rm*math.cos(am), cy-rm*math.sin(am)
        deg = (180 - (i+0.5)*(360/27))
        rot = -deg if -90 <= deg <= 90 else (-deg+180)
        svg.append(f'<text x="{tx}" y="{ty}" text-anchor="middle" dominant-baseline="middle" font-size="10" font-weight="bold" fill="{INK}" transform="rotate({rot},{tx},{ty})">{i+1}. {name} ({lord})</text>')
    # inner ring: signs
    for i in range(12):
        a0 = math.radians(180 - i*30); a1 = math.radians(180 - (i+1)*30)
        x0,y0 = cx+r_mid*math.cos(a0), cy-r_mid*math.sin(a0); x1,y1 = cx+r_mid*math.cos(a1), cy-r_mid*math.sin(a1)
        xi0,yi0 = cx+r_in*math.cos(a0), cy-r_in*math.sin(a0); xi1,yi1 = cx+r_in*math.cos(a1), cy-r_in*math.sin(a1)
        path = f'M{x0},{y0} A{r_mid},{r_mid} 0 0 0 {x1},{y1} L{xi1},{yi1} A{r_in},{r_in} 0 0 1 {xi0},{yi0} Z'
        svg.append(f'<path d="{path}" fill="{PAPER}" stroke="{INK}" stroke-width="1.5"/>')
        am = math.radians(180 - (i+0.5)*30); rm = (r_mid+r_in)/2
        tx,ty = cx+rm*math.cos(am), cy-rm*math.sin(am)
        svg.append(f'<text x="{tx}" y="{ty+4}" text-anchor="middle" font-size="12" font-weight="bold" fill="{MAROON}">{SIGNS[i]}</text>')
    svg.append(f'<circle cx="{cx}" cy="{cy}" r="{r_in}" fill="{PAPER}" stroke="{INK}" stroke-width="1.5"/>')
    lines = ["27 nakshatras × 13°20′ = 360°", "Each sign holds 2¼ nakshatras", "(9 padas of 3°20′ each).",
             "Lord sequence repeats 3 times:", "Ke Ve Su Mo Ma Ra Ju Sa Me"]
    for k, t in enumerate(lines):
        svg.append(f'<text x="{cx}" y="{cy-30+k*18}" text-anchor="middle" font-size="{13 if k==0 else 12}" font-weight="{"bold" if k==0 else "normal"}" fill="{INK}">{t}</text>')
    # legend
    lx = cx - 120; ly = cy + 70
    for j, (lord, col) in enumerate(LORD_COL.items()):
        col_x = lx + (j%5)*50; row_y = ly + (j//5)*18
        svg.append(f'<rect x="{col_x}" y="{row_y}" width="11" height="11" fill="{col}" stroke="{INK}"/>')
        svg.append(f'<text x="{col_x+14}" y="{row_y+10}" font-size="10" fill="{INK}">{lord}</text>')
    if caption:
        svg.append(f'<text x="{W/2}" y="{H-12}" text-anchor="middle" font-size="13" fill="{INK}" font-style="italic">{esc(caption)}</text>')
    svg.append("</svg>")
    return "\n".join(svg)

# ---------------------------------------------------------------- DASHA BAR
DASHA_ORDER = [("Ketu",7),("Venus",20),("Sun",6),("Moon",10),("Mars",7),("Rahu",18),("Jupiter",16),("Saturn",19),("Mercury",17)]
DASHA_COL = {"Ketu":"#e9d5ff","Venus":"#fbcfe8","Sun":"#fed7aa","Moon":"#e5e7eb","Mars":"#fecaca","Rahu":"#c7d2fe",
             "Jupiter":"#fde68a","Saturn":"#bfdbfe","Mercury":"#bbf7d0"}

def dasha_bar(title="Vimshottari Dasha: the 120-year cycle", caption=None, start_lord="Ketu", start_offset_years=0.0, birth_year=None, width=760):
    H = 200 if not caption else 230
    W = width
    svg = svg_header(W, H, title)
    x0 = 30; bar_w = W-60; y0 = 70; bar_h = 46
    # rotate order to start_lord
    idx = [d[0] for d in DASHA_ORDER].index(start_lord)
    order = DASHA_ORDER[idx:] + DASHA_ORDER[:idx]
    total = 120.0
    x = x0
    elapsed = -start_offset_years
    for name, yrs in order:
        w = bar_w*yrs/total
        svg.append(f'<rect x="{x}" y="{y0}" width="{w}" height="{bar_h}" fill="{DASHA_COL[name]}" stroke="{INK}" stroke-width="1.2"/>')
        svg.append(f'<text x="{x+w/2}" y="{y0+20}" text-anchor="middle" font-size="{12 if w>45 else 10}" font-weight="bold" fill="{INK}">{name if w>60 else name[:2]}</text>')
        svg.append(f'<text x="{x+w/2}" y="{y0+37}" text-anchor="middle" font-size="11" fill="{MAROON}">{yrs} y</text>')
        # age tick
        age = max(0, elapsed + (yrs if name==start_lord else 0)) if name==start_lord else elapsed
        x += w
        elapsed += yrs
        label = f"{elapsed:g}" if start_offset_years==0 else f"{elapsed:g}"
        svg.append(f'<line x1="{x}" y1="{y0+bar_h}" x2="{x}" y2="{y0+bar_h+8}" stroke="{INK}"/>')
        svg.append(f'<text x="{x}" y="{y0+bar_h+22}" text-anchor="middle" font-size="10" fill="{INK}">age {label}</text>')
    svg.append(f'<text x="{x0}" y="{y0-10}" font-size="12" fill="{INK}">Birth (balance of {start_lord} dasha runs first)</text>')
    svg.append(f'<text x="{x0}" y="{y0+bar_h+45}" font-size="12" fill="{INK}">Order never changes: Ketu → Venus → Sun → Moon → Mars → Rahu → Jupiter → Saturn → Mercury → (Ketu again)</text>')
    if caption:
        svg.append(f'<text x="{W/2}" y="{H-12}" text-anchor="middle" font-size="13" fill="{INK}" font-style="italic">{esc(caption)}</text>')
    svg.append("</svg>")
    return "\n".join(svg)

# ---------------------------------------------------------------- HOUSE GROUPS
def house_groups(title="House groups every astrologer memorises", size=440):
    """Four small north charts side by side: Kendra, Trikona, Dusthana, Upachaya."""
    groups = [("Kendra (1,4,7,10): pillars", [1,4,7,10]),
              ("Trikona (1,5,9): Lakshmi's houses", [1,5,9]),
              ("Dusthana (6,8,12): the difficult trio", [6,8,12]),
              ("Upachaya (3,6,10,11): growth with time", [3,6,10,11])]
    small = 300
    W = 2*(small+20) + 20; H = 2*(small+60) + 50
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Georgia, serif">',
           f'<rect x="0" y="0" width="{W}" height="{H}" rx="12" fill="{PAPER}" stroke="{GOLD}" stroke-width="2"/>',
           f'<text x="{W/2}" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="{MAROON}">{esc(title)}</text>']
    for i, (label, hs) in enumerate(groups):
        col = i%2; row = i//2
        gx = 10 + col*(small+20); gy = 50 + row*(small+60)
        inner = north_chart(1, {}, title=None, highlight=hs, size=small)
        # strip outer svg wrapper & background rect
        body = inner.split("\n",2)[2].rsplit("</svg>",1)[0]
        svg.append(f'<g transform="translate({gx},{gy})">{body}</g>')
        svg.append(f'<text x="{gx+small/2+10}" y="{gy+small+38}" text-anchor="middle" font-size="14" font-weight="bold" fill="{INK}">{esc(label)}</text>')
    svg.append("</svg>")
    return "\n".join(svg)

# ---------------------------------------------------------------- ASPECTS
def aspect_diagram(planet, house, title=None, caption=None, size=400):
    """Highlight the houses a planet aspects from a given house (Parashari drishti)."""
    special = {"Ma":[4,8],"Ju":[5,9],"Sa":[3,10]}
    offs = [7] + special.get(planet, [])
    targets = [((house-1+o-1)%12)+1 for o in offs]
    return north_chart(1, {house:[planet]}, title=title, highlight=targets, size=size, caption=caption)

# ---------------------------------------------------------------- SADE SATI
def sade_sati(title="Sade Sati: Saturn's 7½-year walk over the natal Moon", caption=None, size=420):
    # Moon in house 4 (say), Saturn transits 3, 4, 5
    planets = {4:["Mo"], 3:["Sa→"], 5:["→Sa"]}
    return north_chart(1, {4:["Mo"]}, title=title, highlight=[3,4,5], size=size, caption=caption)

# ---------------------------------------------------------------- CLI
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kind", choices=["north","south","lalkitab","zodiac","nakshatra","dasha","housegroups","aspect","sadesati"])
    ap.add_argument("--lagna", type=int, default=1)
    ap.add_argument("--planets", default="")
    ap.add_argument("--title", default=None)
    ap.add_argument("--caption", default=None)
    ap.add_argument("--highlight", default="")
    ap.add_argument("--planet", default="Ma")
    ap.add_argument("--house", type=int, default=1)
    ap.add_argument("--start-lord", default="Ketu")
    ap.add_argument("--size", type=int, default=440)
    ap.add_argument("--sign-names", action="store_true")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    planets = parse_planets(a.planets)
    hl = [int(x) for x in a.highlight.split(",") if x.strip()]
    if a.kind == "north":
        s = north_chart(a.lagna, planets, a.title, hl, a.size, caption=a.caption, show_sign_names=a.sign_names)
    elif a.kind == "south":
        s = south_chart(a.lagna, planets, a.title, hl, a.size, caption=a.caption)
    elif a.kind == "lalkitab":
        s = lalkitab_chart(planets, a.title, a.caption, a.size)
    elif a.kind == "zodiac":
        s = zodiac_wheel(a.title or "The Zodiac Belt (Rashi Chakra)", a.caption)
    elif a.kind == "nakshatra":
        s = nakshatra_wheel(a.title or "The 27 Nakshatras and their Vimshottari lords", a.caption)
    elif a.kind == "dasha":
        s = dasha_bar(a.title or "Vimshottari Dasha: the 120-year cycle", a.caption, a.start_lord)
    elif a.kind == "housegroups":
        s = house_groups(a.title or "House groups every astrologer memorises")
    elif a.kind == "aspect":
        s = aspect_diagram(a.planet, a.house, a.title, a.caption, a.size)
    elif a.kind == "sadesati":
        s = sade_sati(a.title or "Sade Sati: Saturn's 7½-year walk over the natal Moon", a.caption, a.size)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(s)
    print("wrote", a.out)

if __name__ == "__main__":
    main()
