#!/usr/bin/env python3
"""insert_comics.py: puts each chapter's comic strip (images/chNN-comic.png) before the chapter's first section heading. Idempotent."""
import re, glob, os, sys
ONLY=set(sys.argv[1:])  # optional chapter numbers, e.g. 04 05
CAPTIONS = {
 "01": "Same person, three seasons. The planets as the court that runs your household, one season at a time.",
 "02": "How your first season is chosen: the Moon's street on the night you were born decides who goes first.",
 "03": "Seasons inside seasons: the season lord runs the house, the sub-season lord runs the kitchen.",
 "04": "The Ketu season in three panels.", "05": "The Venus season in three panels.", "06": "The Sun season in three panels.",
 "07": "The Moon season in three panels.", "08": "The Mars season in three panels.", "09": "The Rahu season in three panels.",
 "10": "The Jupiter season in three panels.", "11": "The Saturn season in three panels.", "12": "The Mercury season in three panels.",
 "13": "Same planet, different room: the three questions before you judge a season.",
 "14": "Weather inside the season: a transit is a visitor passing the window, not a new manager.",
 "15": "The changeover: the awkward year when one courtier packs and the next arrives early.",
 "16": "Three lives in October 2026.", "17": "Living well in a hard season.", "18": "Your season map: it was never random.",
}
n=0
for f in sorted(glob.glob("book/[0-1][0-9]-*.md")):
    num=os.path.basename(f)[:2]
    img=f"images/ch{num}-comic.png"
    if num=="00" or not os.path.exists(img): continue
    if ONLY and num not in ONLY: continue
    s=open(f,encoding="utf-8").read()
    if f"ch{num}-comic.png" in s: continue
    # place the strip at the end of the chapter's opening, just before the first section heading
    i=s.index("\n## ")
    block=f"\n![Comic strip: {CAPTIONS[num]}](../images/ch{num}-comic.png)\n*{CAPTIONS[num]}*\n"
    s=s[:i]+"\n"+block.rstrip("\n")+"\n"+s[i:]
    s=re.sub(r"\n{3,}","\n\n",s)
    open(f,"w",encoding="utf-8").write(s); n+=1
print("inserted strips into", n, "chapters")
