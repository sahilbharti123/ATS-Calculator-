#!/usr/bin/env python3
"""Ensure numbered lists inside Practice boxes render as lists (insert a bare '>' line after the label)."""
import glob, re
n=0
for f in sorted(glob.glob("book/*.md")):
    s=open(f,encoding="utf-8").read()
    new=re.sub(r"(> \*\*✍️ Practice:\*\*[^\n]*)\n(> \d+\.)", r"\1\n>\n\2", s)
    if new!=s: open(f,"w",encoding="utf-8").write(new); n+=1
print("fixed files:",n)
