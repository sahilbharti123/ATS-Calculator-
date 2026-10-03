import re, glob, json
DROP = {
 "Real Christmas trees on rent",
 "Rent a real Christmas tree, delivered and collected",
 "A monthly printed family newspaper for grandparents",
 "Stylish earplugs for weddings, concerts and noisy nights",
 "Speeches written for you: weddings, farewells and anniversaries",
 "Sun-protection clothing for Indian summers",
 "Gentle skincare kits for teenagers",
 "Hard-water rinse for hair and skin",
 "Swimming lessons for babies in warm hotel pools",
 "Someone shows your flat to tenants for you",
}
groups=[]
dropped=[]
for f in sorted(glob.glob("batch_*.md")):
    txt=open(f,encoding="utf-8").read()
    title=re.search(r"(?m)^# (.+)$",txt).group(1).strip()
    parts=re.split(r"(?m)^(?=### )",txt)
    ideas=[]
    for p in parts:
        if not p.startswith("### "): continue
        name=p.split("\n")[0][4:].strip()
        if name in DROP: dropped.append(name); continue
        body=p.split("\n",1)[1].strip()
        # strip trailing horizontal rules / notes
        body=re.sub(r"\n---+\s*$","",body).strip()
        ideas.append((name,body))
    groups.append((title,ideas))
print("dropped",len(dropped),sorted(set(DROP)-set(dropped)))
n=0
out=[]
for title,ideas in groups:
    out.append(f"## {title}\n")
    for name,body in ideas:
        n+=1
        out.append(f"### {n}. {name}\n{body}\n")
print("total",n)
open("compiled_100.md","w",encoding="utf-8").write("\n".join(out))
