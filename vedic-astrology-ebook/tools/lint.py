#!/usr/bin/env python3
"""lint.py — structural checks for book/*.md (run from the ebook folder)."""
import re, os, glob, sys
BOOK="book"; IMG="images"
problems=0
for f in sorted(glob.glob(f"{BOOK}/*.md")):
    s=open(f,encoding="utf-8").read(); name=os.path.basename(f); errs=[]
    first=s.splitlines()[0]
    if not re.match(r"# (Chapter \d+|Appendix [A-Z]): |# A Love Letter|# About the Author", first): errs.append(f"bad first line: {first[:60]}")
    for m in re.finditer(r"!\[([^\]]*)\]\(([^)]+)\)", s):
        p=os.path.normpath(os.path.join(BOOK,m.group(2)))
        if not os.path.exists(p): errs.append(f"missing image {m.group(2)}")
        if not m.group(1).strip(): errs.append(f"empty alt for {m.group(2)}")
    if name[0] in "12" or (name[0]=="0" and not name.startswith("00")):
        for need in ["## In one breath","## Practice","<details>","</details>"]:
            if need not in s: errs.append(f"missing {need}")
    # heading level skips
    prev=1
    for m in re.finditer(r"^(#{1,4}) ", s, flags=re.M):
        lvl=len(m.group(1))
        if lvl>prev+1: errs.append(f"heading level skip near: {s[m.start():m.start()+50]!r}")
        prev=lvl
    # Lal Kitab boxes must carry a source line
    for m in re.finditer(r"> \*\*📕 From Lal Kitab:\*\*(.*?)(?:\n\n|\Z)", s, flags=re.S):
        if "Source: Lal Kitab" not in m.group(0): errs.append("Lal Kitab box without source line")
    # Lal Kitab mentioned outside boxes (allowed in ch22, ch01 and appendices)
    if not (name.startswith(("22","01","00","9"))):
        for line in s.splitlines():
            if "Lal Kitab" in line and not line.startswith(">") and "Chapter 22" not in line and "Ch 22" not in line and "Ch. 22" not in line:
                errs.append(f"Lal Kitab outside a box: {line[:80]!r}"); break
    if name[0] in "012" and not name.startswith(("00","01")):
        n=s.count("**📖 Story:")
        if n<2: errs.append(f"only {n} Story boxes (need 2+)")
    for m in re.finditer(r"> \*\*📖 Story:[^\n]*(?:\n>[^\n]*)*", s):
        if "**Rule:**" not in m.group(0): errs.append(f"Story without a Rule line: {m.group(0)[:60]!r}")
    n_em=s.count("—")
    if n_em: errs.append(f"{n_em} em dash(es) — not allowed")
    for m in re.finditer(r"[A-Za-z] – [A-Za-z]", s):
        ctx=s[max(0,m.start()-10):m.end()+10]
        if not re.search(r"[0-9°′]", ctx):
            errs.append(f"en dash used as punctuation: {ctx!r}"); break
    words=len(s.split())
    print(f"{name:55s} {words:6d} words  {'OK' if not errs else ''}")
    for e in errs: print("    -", e); problems+=1
print("problems:",problems); sys.exit(1 if problems else 0)
