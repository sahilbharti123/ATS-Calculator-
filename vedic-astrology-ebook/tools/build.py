#!/usr/bin/env python3
"""
build.py: assembles book/*.md into a single self-contained HTML ebook (SVGs inlined)
and, if Chromium is available, prints it to PDF.

  python3 tools/build.py            # writes dist/Kundali-Made-Simple.html and .pdf
  python3 tools/build.py --no-pdf
"""
import re, os, sys, glob, html, subprocess, datetime
import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, "book")
IMAGES = os.path.join(ROOT, "images")
DIST = os.path.join(ROOT, "dist")
TITLE = "Kundali Made Simple"
AUTHOR = "Anushka Bharti"
YEAR = "2026"
COVER = os.path.join(ROOT, "cover", "cover-front.jpg")
SUBTITLE = "Vedic Astrology from Your First Chart to Your First Consultation"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

CSS = r"""
:root { --ink:#2b1a10; --paper:#fffdf7; --maroon:#7f1d1d; --gold:#b8860b; --muted:#6b5b4e; }
* { box-sizing: border-box; }
html { font-size: 17px; }
body { font-family: Georgia, "Noto Serif", "Times New Roman", serif; color: var(--ink); background: var(--paper);
       margin: 0; line-height: 1.6; }
.page { max-width: 820px; margin: 0 auto; padding: 32px 28px 80px; }
h1 { font-size: 2.1rem; color: var(--maroon); border-bottom: 3px solid var(--gold); padding-bottom: .3rem; margin-top: 2.2rem; line-height: 1.2; }
h2 { font-size: 1.45rem; color: var(--maroon); margin-top: 2rem; }
h3 { font-size: 1.15rem; color: #5b2a1a; margin-top: 1.4rem; }
p { margin: .7rem 0; text-align: left; }
img, svg { max-width: 100%; height: auto; display: block; margin: 1.2rem auto .3rem; }
p.caption { display:block; text-align:center; color: var(--muted); font-size: .92rem; margin-top: .1rem; }
table { border-collapse: collapse; width: 100%; margin: 1rem 0; font-size: .9rem; }
th, td { border: 1px solid #d9c9a8; padding: .4rem .55rem; vertical-align: top; }
th { background: #f3e6c8; color: var(--maroon); text-align: left; }
tr:nth-child(even) td { background: #fbf5e8; }
blockquote { margin: 1.1rem 0; padding: .8rem 1rem .8rem 1.1rem; border-left: 5px solid var(--gold); background: #fff7df; border-radius: 6px; }
blockquote p { margin: .35rem 0; }
strong.lbl { font-variant: small-caps; letter-spacing:.04em; color: var(--maroon); }
blockquote.tip { border-left-color:#0e7490; background:#e6f7fb; }
blockquote.fact { border-left-color:#7c3aed; background:#f3ecff; }
blockquote.warn { border-left-color:#b91c1c; background:#fdecec; }
blockquote.consult { border-left-color:#b45309; background:#fff3e0; }
blockquote.lalkitab { border-left-color:#dc2626; background:#fff1f1; border:1px dashed #dc2626; border-left-width:5px; }
blockquote.practice { border-left-color:#15803d; background:#edfaf0; }
blockquote.story { border-left-color:#0f766e; background:#f0fdfa; font-style: italic; }
blockquote.why { border-left-color:#4338ca; background:#eef2ff; }
blockquote.story strong { font-style: normal; }
details { background:#f7f1e3; border:1px solid #e2d3b0; border-radius:6px; padding:.5rem .9rem; margin:.6rem 0 1.2rem; }
summary { cursor:pointer; font-weight:bold; color: var(--maroon); }
code { background:#f3ead6; padding:.05rem .3rem; border-radius:3px; font-size:.9em; }
pre { background:#f3ead6; padding:.8rem; overflow:auto; border-radius:6px; }
hr { border:none; border-top:1px solid #d9c9a8; margin:2rem 0; }
.cover { text-align:center; padding: 90px 20px 60px; page-break-after: always; }
.cover h1 { font-size: 3rem; border:none; margin-bottom:.2rem; }
.cover .sub { font-size:1.35rem; color:#5b2a1a; font-style: italic; margin-bottom: 2.5rem; }
.cover .by { font-size:1.05rem; color: var(--muted); }
.cover svg { margin: 2rem auto; }
.toc { page-break-after: always; }
.toc ol { list-style:none; padding-left:0; }
.toc li { margin:.25rem 0; }
.toc li.part { font-weight:bold; color: var(--maroon); margin-top: 1rem; font-size:1.05rem; }
.toc a { text-decoration:none; color: var(--ink); }
.toc a:hover { color: var(--maroon); }
.toc ol ol { padding-left: 1.4rem; font-size:.92rem; color: var(--muted); }
.frontnote { font-size:.95rem; color:#4b3a2e; border:1px solid #e2d3b0; padding:1rem 1.2rem; border-radius:8px; background:#fbf5e8; }
.chapter { page-break-before: always; }
.legend { font-size:.9rem; }
.dot { font-weight:bold; font-size:1.05em; }
.dot.g { color:#15803d; } .dot.y { color:#b45309; } .dot.r { color:#b91c1c; }
.coverpage { text-align:center; page-break-after: always; margin:0; padding:0; }
.coverpage img { width:100%; max-width:820px; margin:0 auto; display:block; }
.titlepage { text-align:center; padding: 140px 20px 60px; page-break-after: always; }
.titlepage h1 { font-size:2.8rem; border:none; }
.titlepage .sub { font-size:1.25rem; font-style:italic; color:#5b2a1a; margin: .5rem 0 3rem; }
.titlepage .author { font-size:1.4rem; letter-spacing:.08em; color:#3b2314; }
.copyright { font-size:.85rem; color:#4b3a2e; page-break-after: always; padding-top: 40vh; }
.dedication { text-align:center; font-style:italic; font-size:1.2rem; padding: 35vh 40px; page-break-after: always; }
@media print {
  html { font-size: 11.5pt; }
  .page { max-width: none; padding: 0; }
  a { color: inherit; }
  details { display:block; }
  details > *:not(summary) { display:block; }
  summary { list-style:none; }
  h1, h2, h3 { page-break-after: avoid; }
  img, svg, table, blockquote { page-break-inside: avoid; }
  @page { size: A4; margin: 18mm 16mm 20mm 16mm; }
  .coverpage img { max-width:none; width:100%; height:auto; }
}
"""

BOX_CLASSES = [("🧭", "tip"), ("💡", "fact"), ("⚠️", "warn"), ("🪔", "consult"), ("📕", "lalkitab"), ("✍️", "practice"), ("📖", "story"), ("🔍", "why")]

def strip_label_emoji(html_text):
    """The emoji are parsing markers in the source; the published book shows clean labels."""
    def repl(m):
        body = m.group(2)
        body = re.sub(r"<strong>\s*[🧭🔍📖💡🪔📕✍️⚠]\uFE0F?\s*", "<strong class=\"lbl\">", body, count=1)
        return f"<blockquote{m.group(1)}>{body}</blockquote>"
    return re.sub(r"<blockquote([^>]*)>(.*?)</blockquote>", repl, html_text, flags=re.S)

def slugify(s):
    s = re.sub(r"[^\w\s-]", "", s.lower())
    return re.sub(r"[\s_]+", "-", s).strip("-")

def inline_svgs(html_text):
    def repl(m):
        src = m.group(1)
        alt = m.group(2) or ""
        path = os.path.normpath(os.path.join(BOOK, src))
        if not os.path.exists(path):
            path = os.path.join(IMAGES, os.path.basename(src))
        if os.path.exists(path) and path.endswith(".svg"):
            svg = open(path, encoding="utf-8").read()
            svg = re.sub(r"<\?xml[^>]*\?>", "", svg).strip()
            # give the svg a title for accessibility
            if alt and "<title>" not in svg[:400]:
                svg = re.sub(r"(<svg[^>]*>)", r"\1<title>" + html.escape(alt) + "</title>", svg, count=1)
            return f'<figure role="img" aria-label="{html.escape(alt)}">{svg}</figure>'
        return m.group(0)
    return re.sub(r'<img[^>]*src="([^"]+)"[^>]*alt="([^"]*)"[^>]*/?>', repl, html_text)

def classify_boxes(html_text):
    def repl(m):
        body = m.group(1)
        for emoji, cls in BOX_CLASSES:
            if emoji in body[:60]:
                return f'<blockquote class="{cls}">{body}</blockquote>'
        return m.group(0)
    return re.sub(r"<blockquote>(.*?)</blockquote>", repl, html_text, flags=re.S)

DOTS = {"🟢": '<span class="dot g" title="good">●</span>', "🟡": '<span class="dot y" title="mixed">◐</span>', "🔴": '<span class="dot r" title="difficult">○</span>'}
def dots(html_text):
    for k, v in DOTS.items():
        html_text = html_text.replace(k, v)
    return html_text

def convert(md_text):
    md = markdown.Markdown(extensions=["tables", "fenced_code", "attr_list", "md_in_html", "sane_lists", "toc"],
                           extension_configs={"toc": {"toc_depth": "1-2", "slugify": lambda v, s: slugify(v)}})
    out = md.convert(md_text)
    out = inline_svgs(out)
    out = classify_boxes(out)
    # italic caption lines directly after a figure
    out = re.sub(r"(</figure>)\s*<p><em>(.*?)</em></p>", r'\1<p class="caption"><em>\2</em></p>', out, flags=re.S)
    out = dots(out)
    out = strip_label_emoji(out)
    return out, md.toc_tokens

PARTS = {
    1: "Part I: Foundations", 6: "Part II: Core Tools", 13: "Part III: Timing",
    18: "Part IV: Life Questions", 22: "Part V: Lal Kitab, Remedies and the Consulting Room",
}

def cover_svg():
    # a simple decorative north-indian diamond as a cover ornament
    S = 260; ox = 0
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 {S} {S}">
<rect x="4" y="4" width="{S-8}" height="{S-8}" fill="#fffaf0" stroke="#7f1d1d" stroke-width="3"/>
<line x1="4" y1="4" x2="{S-4}" y2="{S-4}" stroke="#7f1d1d" stroke-width="2"/>
<line x1="{S-4}" y1="4" x2="4" y2="{S-4}" stroke="#7f1d1d" stroke-width="2"/>
<polygon points="{S/2},4 {S-4},{S/2} {S/2},{S-4} 4,{S/2}" fill="none" stroke="#7f1d1d" stroke-width="2"/>
<text x="{S/2}" y="{S/4+6}" text-anchor="middle" font-family="Georgia" font-size="18" fill="#b8860b">ॐ</text>
</svg>'''

def main():
    no_pdf = "--no-pdf" in sys.argv
    print_6x9 = "--print" in sys.argv
    files = sorted(glob.glob(os.path.join(BOOK, "*.md")))
    chapters = []
    for f in files:
        text = open(f, encoding="utf-8").read()
        body, toc = convert(text)
        m = re.match(r"#\s+(.*)", text)
        title = m.group(1).strip() if m else os.path.basename(f)
        num = None
        mm = re.match(r"Chapter\s+(\d+)", title)
        if mm: num = int(mm.group(1))
        chapters.append(dict(file=f, title=title, num=num, body=body, toc=toc, id=slugify(title)))

    # TOC
    toc_html = ['<nav class="toc"><h1>Contents</h1><ol>']
    for ch in chapters:
        if ch["num"] in PARTS:
            toc_html.append(f'<li class="part">{html.escape(PARTS[ch["num"]])}</li>')
        if ch["num"] is None and ch["title"].startswith("Appendix") and not any("Appendix" in c["title"] for c in chapters[:chapters.index(ch)]):
            toc_html.append('<li class="part">Appendices</li>')
        toc_html.append(f'<li><a href="#{ch["id"]}">{html.escape(ch["title"])}</a>')
        subs = [t for t in ch["toc"][0]["children"]] if ch["toc"] else []
        if ch["title"].startswith("Appendix D") or ch["title"].startswith("Appendix B"):
            subs = []
        if subs:
            toc_html.append("<ol>")
            for s in subs:
                toc_html.append(f'<li><a href="#{s["id"]}">{html.escape(s["name"])}</a></li>')
            toc_html.append("</ol>")
        toc_html.append("</li>")
    toc_html.append("</ol></nav>")

    today = datetime.date.today().strftime("%B %Y")
    cover_html = ""
    if os.path.exists(COVER):
        import base64
        b64 = base64.b64encode(open(COVER, "rb").read()).decode()
        cover_html = f'<section class="coverpage"><img src="data:image/jpeg;base64,{b64}" alt="Cover: {TITLE}"></section>'
    front = f"""
{cover_html}
<section class="titlepage">
  <h1>{TITLE}</h1>
  <div class="sub">{SUBTITLE}</div>
  {cover_svg()}
  <div class="author">{AUTHOR}</div>
</section>
<section class="copyright">
  <p><strong>{TITLE}: {SUBTITLE}</strong><br>Copyright &copy; {YEAR} {AUTHOR}. All rights reserved.</p>
  <p>No part of this book may be reproduced, stored or transmitted in any form without the prior written permission of the author, except for brief quotations in reviews.</p>
  <p>First edition, {today}.</p>
  <p><strong>A note on what this book is and is not.</strong> This book teaches Vedic astrology (Jyotish) as a way of understanding tendencies and timings. It is not medical, legal, financial or psychological advice, and nothing in it should be used to make decisions about health, money or law in place of a qualified professional. Every person named in the examples is a composite, and the three case-study charts are constructed for teaching.</p>
  <p><strong>Sources.</strong> The backbone is Parashari astrology (<em>Brihat Parashara Hora Shastra</em>). Anything drawn from <em>Lal Kitab</em> (Pt. Roop Chand Joshi, Urdu editions 1939 to 1952) appears only inside boxes labelled <strong>From Lal Kitab</strong> with the source stated. Jaimini, Tajaka and KP appear where named.</p>
  <p class="legend"><strong>Boxes used in this book:</strong> Anushka's rule of thumb · Why? · Story · Did you know? · Common beginner mistake · Consultation tip · From Lal Kitab (red dashed border) · Practice. <strong>Colour dots:</strong> {DOTS["🟢"]} good or friendly · {DOTS["🟡"]} mixed or neutral · {DOTS["🔴"]} difficult or hostile.</p>
</section>
<section class="dedication">
  <p>For everyone who bought the books and understood nothing.<br>This one is for you.</p>
</section>
"""
    body_html = []
    for ch in chapters:
        # give the H1 an id
        b = re.sub(r"<h1(.*?)>", f'<h1 id="{ch["id"]}"\\1>', ch["body"], count=1)
        body_html.append(f'<article class="chapter">{b}</article>')

    print_css = ""
    if print_6x9:
        print_css = "@media print { @page { size: 6in 9in; margin: 0.75in 0.6in 0.7in 0.6in; } html { font-size: 10.5pt; } .page { padding:0; } }"
    doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE}: {SUBTITLE}</title><style>{CSS}</style></head>
<body><div class="page">{front}{"".join(toc_html)}{"".join(body_html)}</div></body></html>'''
    os.makedirs(DIST, exist_ok=True)
    out_html = os.path.join(DIST, "Kundali-Made-Simple-print-6x9.html" if print_6x9 else "Kundali-Made-Simple.html")
    open(out_html, "w", encoding="utf-8").write(doc)
    words = sum(len(re.sub(r"<[^>]+>", " ", c["body"]).split()) for c in chapters)
    print(f"wrote {out_html}  ({len(chapters)} sections, ~{words:,} words, {os.path.getsize(out_html)/1e6:.1f} MB)")
    if not no_pdf and os.path.exists(CHROME):
        out_pdf = os.path.join(DIST, "Kundali-Made-Simple-print-6x9.pdf" if print_6x9 else "Kundali-Made-Simple.pdf")
        cmd = [CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
               f"--print-to-pdf={out_pdf}", "--virtual-time-budget=10000", f"file://{out_html}"]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if os.path.exists(out_pdf):
            print(f"wrote {out_pdf}  ({os.path.getsize(out_pdf)/1e6:.1f} MB)")
            if print_6x9:
                os.remove(out_html)
        else:
            print("PDF failed:", r.stderr[-800:])

if __name__ == "__main__":
    main()
