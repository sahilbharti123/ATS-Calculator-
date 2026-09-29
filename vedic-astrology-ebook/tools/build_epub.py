#!/usr/bin/env python3
"""
build_epub.py — builds a reflowable EPUB 3 (Kindle-ready) from book/*.md.

  python3 tools/svg2png.py      # first: renders diagrams to images_png/
  python3 tools/build_epub.py   # → dist/Astrology-Gently.epub
"""
import os, re, glob, html, zipfile, uuid, datetime, sys
import markdown
from lxml import html as LH, etree

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, "book"); PNG = os.path.join(ROOT, "images_png"); DIST = os.path.join(ROOT, "dist")
COVER = os.path.join(ROOT, "cover", "cover-front.jpg")
TITLE = "Astrology, Gently"; SUBTITLE = "A kind, beginner-friendly guide to understanding your chart and yourself"
AUTHOR = "Anushka Bharti"; LANG = "en"; YEAR = "2026"
BOOK_ID = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_URL, "kundali-made-simple-anushka-bharti-2026"))

CSS = """
body { font-family: Georgia, serif; line-height: 1.5; margin: 0 1em; color:#222; }
h1 { font-size: 1.7em; color:#1e2a5a; margin: 1.2em 0 .6em; line-height:1.2; page-break-before: always; }
h2 { font-size: 1.3em; color:#1e2a5a; margin-top: 1.4em; }
h3 { font-size: 1.1em; color:#2b3350; }
p { margin: .6em 0; text-indent: 0; }
img { max-width: 100%; height: auto; display:block; margin: .8em auto .2em; }
p.caption { text-align:center; font-size:.9em; color:#555; font-style: italic; margin-top:.1em; }
table { border-collapse: collapse; width:100%; margin: .8em 0; font-size:.85em; }
th, td { border: 1px solid #bbb; padding: .3em .4em; vertical-align: top; }
th { background:#f3e6c8; }
blockquote { margin: .9em 0; padding: .6em .9em; border-left: 4px solid #b8860b; background:#fbf5e8; }
blockquote.tip { border-left-color:#0e7490; background:#eaf6fa; }
blockquote.why { border-left-color:#4338ca; background:#eef2ff; }
blockquote.fact { border-left-color:#7c3aed; background:#f3ecff; }
blockquote.warn { border-left-color:#b91c1c; background:#fdecec; }
blockquote.consult { border-left-color:#b45309; background:#fff3e0; }
blockquote.lalkitab { border:1px dashed #dc2626; border-left:4px solid #dc2626; background:#fff1f1; }
blockquote.practice { border-left-color:#15803d; background:#edfaf0; }
blockquote.story { border-left-color:#0f766e; background:#f0fdfa; font-style: italic; }
div.answers { border:1px solid #ddd; background:#f7f1e3; padding:.5em .9em; margin:.6em 0 1.2em; }
.dot { font-weight:bold; }
strong.lbl { font-variant: small-caps; letter-spacing:.04em; color:#1e2a5a; } .dot.g { color:#15803d; } .dot.y { color:#b45309; } .dot.r { color:#b91c1c; }
.titlepage { text-align:center; margin-top: 25%; }
.titlepage h1 { border:none; page-break-before: auto; font-size: 2.2em; }
.titlepage .sub { font-style: italic; color:#2b3350; font-size: 1.1em; margin-bottom: 2em; }
.titlepage .author { font-size:1.2em; letter-spacing:.05em; }
.copyright { font-size:.85em; color:#444; margin-top: 30%; }
.dedication { text-align:center; font-style:italic; font-size:1.1em; margin-top: 35%; }
.cover img { max-height: 100%; }
"""
BOX = [("🧭", "tip"), ("🔍", "why"), ("💡", "fact"), ("⚠️", "warn"), ("🪔", "consult"), ("📕", "lalkitab"), ("✍️", "practice"), ("📖", "story")]
DOTS = {"🟢": '<span class="dot g">●</span>', "🟡": '<span class="dot y">◐</span>', "🔴": '<span class="dot r">○</span>'}

def strip_label_emoji(html_text):
    """The emoji are parsing markers in the source; the published book shows clean labels."""
    def repl(m):
        body = m.group(2)
        body = re.sub(r"<strong>\s*[🧭🔍📖💡🪔📕✍️⚠]\uFE0F?\s*", "<strong class=\"lbl\">", body)
        return f"<blockquote{m.group(1)}>{body}</blockquote>"
    return re.sub(r"<blockquote([^>]*)>(.*?)</blockquote>", repl, html_text, flags=re.S)

def slug(s):
    s = re.sub(r"[^\w\s-]", "", s.lower()); return re.sub(r"[\s_]+", "-", s).strip("-")

def md2xhtml(md_text, images_used):
    md = markdown.Markdown(extensions=["tables", "fenced_code", "attr_list", "md_in_html", "sane_lists"])
    out = md.convert(md_text)
    # images: ../images/x.svg -> images/x.png
    def img(m):
        tag = m.group(0)
        src = (re.search(r'src="([^"]+)"', tag) or [None, ""])[1]; alt = (re.search(r'alt="([^"]*)"', tag) or [None, ""])[1]
        name = os.path.basename(src)[:-4] + ".png"
        if os.path.exists(os.path.join(PNG, name)):
            images_used.add(name)
            return f'<img src="images/{name}" alt="{html.escape(alt)}"/>'
        return ""
    out = re.sub(r'<img\b[^>]*?>', img, out)
    # box classes
    def box(m):
        body = m.group(1)
        for e, c in BOX:
            if e in body[:60]:
                return f'<blockquote class="{c}">{body}</blockquote>'
        return m.group(0)
    out = re.sub(r"<blockquote>(.*?)</blockquote>", box, out, flags=re.S)
    # captions
    out = re.sub(r"(<img[^>]*/>)\s*<p><em>(.*?)</em></p>", r'\1<p class="caption"><em>\2</em></p>', out, flags=re.S)
    # details -> visible answers block (Kindle has no <details>)
    out = re.sub(r"<details>\s*<summary>(.*?)</summary>(.*?)</details>", r'<div class="answers"><p><strong>\1</strong></p>\2</div>', out, flags=re.S)
    for k, v in DOTS.items(): out = out.replace(k, v)
    out = strip_label_emoji(out)
    # serialise as well-formed XHTML
    frag = LH.fragment_fromstring(out, create_parent="div")
    xhtml = etree.tostring(frag, method="xml", encoding="unicode")
    return xhtml

def page(title, body_xhtml, extra_class=""):
    return f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="{LANG}" xml:lang="{LANG}">
<head><meta charset="utf-8"/><title>{html.escape(title)}</title><link rel="stylesheet" type="text/css" href="style.css"/></head>
<body class="{extra_class}">{body_xhtml}</body></html>'''

def main():
    files = sorted(glob.glob(os.path.join(BOOK, "*.md")))
    images_used = set()
    chapters = []
    for i, f in enumerate(files):
        text = open(f, encoding="utf-8").read()
        title = re.match(r"#\s+(.*)", text).group(1).strip()
        body = md2xhtml(text, images_used)
        # give the h1 an id
        cid = f"c{i:02d}"
        body = body.replace("<h1>", f'<h1 id="{cid}">', 1)
        chapters.append(dict(id=cid, title=title, file=f"{cid}-{slug(title)[:40]}.xhtml", body=body))

    today = datetime.date.today().strftime("%B %Y")
    front = {
        "cover.xhtml": page("Cover", f'<div class="cover"><img src="images/cover.jpg" alt="Cover"/></div>', "cover"),
        "title.xhtml": page("Title page", f'<div class="titlepage"><h1>{TITLE}</h1><p class="sub">{SUBTITLE}</p><p class="author">{AUTHOR}</p></div>'),
        "copyright.xhtml": page("Copyright", f'''<div class="copyright">
<p><strong>{TITLE}: {SUBTITLE}</strong><br/>Copyright &#169; {YEAR} {AUTHOR}. All rights reserved.</p>
<p>No part of this book may be reproduced, stored or transmitted in any form without the prior written permission of the author, except for brief quotations in reviews.</p>
<p>First edition, {today}.</p>
<p><strong>A note on what this book is and is not.</strong> This book teaches Vedic astrology (Jyotish) as a way of understanding tendencies and timings. It is not medical, legal, financial or psychological advice, and nothing in it should be used to make decisions about health, money or law in place of a qualified professional. Every person named in the examples is a composite, and the three case-study charts are constructed for teaching.</p>
<p><strong>Sources.</strong> The backbone is Parashari astrology (<em>Brihat Parashara Hora Shastra</em>). Anything drawn from <em>Lal Kitab</em> (Pt. Roop Chand Joshi, Urdu editions 1939 to 1952) appears only inside boxes labelled <strong>From Lal Kitab</strong> with the source stated.</p>
<p><strong>Boxes used in this book:</strong> Anushka's rule of thumb · Why? · Story · Did you know? · Common beginner mistake · Consultation tip · From Lal Kitab (red dashed border) · Practice. <strong>Colour dots:</strong> {DOTS["🟢"]} good or friendly · {DOTS["🟡"]} mixed or neutral · {DOTS["🔴"]} difficult or hostile (on a black-and-white screen: full, half and empty circle).</p></div>'''),
        "dedication.xhtml": page("Dedication", '<div class="dedication"><p>For everyone who bought the books and understood nothing.<br/>This one is for you.</p></div>'),
    }
    # nav
    nav_items = "".join(f'<li><a href="{c["file"]}">{html.escape(c["title"])}</a></li>' for c in chapters)
    nav = f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="{LANG}" xml:lang="{LANG}">
<head><meta charset="utf-8"/><title>Contents</title><link rel="stylesheet" type="text/css" href="style.css"/></head>
<body><nav epub:type="toc" id="toc"><h1>Contents</h1><ol>
<li><a href="title.xhtml">Title page</a></li><li><a href="dedication.xhtml">Dedication</a></li>{nav_items}</ol></nav>
<nav epub:type="landmarks" hidden="hidden"><ol><li><a epub:type="cover" href="cover.xhtml">Cover</a></li><li><a epub:type="toc" href="nav.xhtml">Table of Contents</a></li><li><a epub:type="bodymatter" href="{chapters[0]["file"]}">Start</a></li></ol></nav>
</body></html>'''
    # ncx (for older readers)
    navpoints = "".join(f'<navPoint id="np{i}" playOrder="{i+1}"><navLabel><text>{html.escape(c["title"])}</text></navLabel><content src="{c["file"]}"/></navPoint>' for i, c in enumerate(chapters))
    ncx = f'''<?xml version="1.0" encoding="utf-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1"><head><meta name="dtb:uid" content="{BOOK_ID}"/><meta name="dtb:depth" content="1"/><meta name="dtb:totalPageCount" content="0"/><meta name="dtb:maxPageNumber" content="0"/></head>
<docTitle><text>{TITLE}</text></docTitle><navMap>{navpoints}</navMap></ncx>'''
    # opf
    manifest = ['<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
                '<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>',
                '<item id="css" href="style.css" media-type="text/css"/>',
                '<item id="cover-image" href="images/cover.jpg" media-type="image/jpeg" properties="cover-image"/>']
    spine = []
    for k in ["cover.xhtml", "title.xhtml", "copyright.xhtml", "dedication.xhtml"]:
        iid = k.replace(".xhtml", "")
        linear = ' linear="no"' if iid == "cover" else ""
        manifest.append(f'<item id="{iid}" href="{k}" media-type="application/xhtml+xml"/>'); spine.append(f'<itemref idref="{iid}"{linear}/>')
    spine.append('<itemref idref="nav"/>')
    for c in chapters:
        manifest.append(f'<item id="{c["id"]}" href="{c["file"]}" media-type="application/xhtml+xml"/>'); spine.append(f'<itemref idref="{c["id"]}"/>')
    for n in sorted(images_used):
        manifest.append(f'<item id="img-{slug(n)}" href="images/{n}" media-type="image/png"/>')
    opf = f'''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" xml:lang="{LANG}">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="bookid">{BOOK_ID}</dc:identifier>
<dc:title>{TITLE}: {SUBTITLE}</dc:title>
<dc:creator id="creator">{AUTHOR}</dc:creator>
<dc:language>{LANG}</dc:language>
<dc:date>{YEAR}</dc:date>
<dc:publisher>{AUTHOR}</dc:publisher>
<dc:rights>Copyright © {YEAR} {AUTHOR}. All rights reserved.</dc:rights>
<dc:description>A complete, illustrated beginner-to-consultant course in Vedic astrology (Jyotish), with a reason for every rule, memory stories, colour-coded tables, and Lal Kitab clearly labelled wherever it appears.</dc:description>
<meta property="dcterms:modified">{datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")}</meta>
<meta name="cover" content="cover-image"/>
</metadata>
<manifest>{"".join(manifest)}</manifest>
<spine toc="ncx">{"".join(spine)}</spine>
</package>'''
    os.makedirs(DIST, exist_ok=True)
    out = os.path.join(DIST, "Astrology-Gently.epub")
    with zipfile.ZipFile(out, "w") as z:
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", '<?xml version="1.0" encoding="utf-8"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>', zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/content.opf", opf, zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/nav.xhtml", nav, zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/toc.ncx", ncx, zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/style.css", CSS, zipfile.ZIP_DEFLATED)
        for k, v in front.items(): z.writestr("OEBPS/" + k, v, zipfile.ZIP_DEFLATED)
        for c in chapters: z.writestr("OEBPS/" + c["file"], page(c["title"], c["body"]), zipfile.ZIP_DEFLATED)
        z.write(COVER, "OEBPS/images/cover.jpg")
        for n in sorted(images_used): z.write(os.path.join(PNG, n), "OEBPS/images/" + n)
    # well-formedness check of every xhtml
    bad = 0
    with zipfile.ZipFile(out) as z:
        for n in z.namelist():
            if n.endswith((".xhtml", ".opf", ".ncx", ".xml")):
                try: etree.fromstring(z.read(n))
                except Exception as e: bad += 1; print("XML ERROR", n, e)
    print(f"wrote {out} ({os.path.getsize(out)/1e6:.1f} MB, {len(chapters)} sections, {len(images_used)} images, {bad} xml errors)")

if __name__ == "__main__":
    main()
