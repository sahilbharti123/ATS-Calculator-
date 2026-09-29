#!/usr/bin/env python3
"""storybank.py: collects every 📖 Story box from book/*.md into Appendix D (run before build.py)."""
import re, glob, os
BOOK="book"; out=[]
out.append("# Appendix D: The Story Bank: Every Memory Tale in One Place\n")
out.append("The reader who commissioned this book said: lists fade, stories stay. Here are all the stories from the chapters, in order, each with its one-line rule, so you can revise the whole grammar of astrology in an evening by reading the tales alone. The cast never changes: the **King** (Sun), the **Queen Mother** (Moon), the **Commander** (Mars), the young **Prince** and secretary (Mercury), the **Royal Priest** (Jupiter), the **Minister of Pleasure** (Venus), the old **Judge of Labour** (Saturn), and the two strangers at the gate: smoke-headed **Rahu** and the headless sadhu **Ketu**. The twelve houses are the rooms of the palace, the signs are the districts of the kingdom, the nakshatras are its streets, and the dashas are the railway timetable.\n")
count=0
for f in sorted(glob.glob(f"{BOOK}/[0-2]*.md")):
    s=open(f,encoding="utf-8").read()
    title=re.match(r"# (.*)",s).group(1)
    stories=re.findall(r"(> \*\*📖 Story:[^\n]*(?:\n>[^\n]*)*)", s)
    if not stories: continue
    out.append(f"\n## From {title}\n")
    for st in stories:
        out.append(st+"\n"); count+=1
out.append(f"\n---\n*{count} stories in all. If you can retell them, you can read a chart.*\n")
open(f"{BOOK}/93-appendix-d-story-bank.md","w",encoding="utf-8").write("\n".join(out))
print("stories collected:",count)
