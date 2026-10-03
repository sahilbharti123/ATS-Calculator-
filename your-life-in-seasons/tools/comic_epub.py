#!/usr/bin/env python3
"""comic_epub.py: fixed-layout EPUB 3 for Kindle from comic/pages/pNNN.png (one image per page) + cover.
   python3 tools/comic_epub.py  -> dist/Your-Life-in-Seasons-comic.epub"""
import os, glob, zipfile, uuid, datetime
from PIL import Image
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES=sorted(glob.glob(os.path.join(ROOT,"comic","pages","p*.png")))
COVER=os.path.join(ROOT,"cover","cover-comic-front.jpg")
OUT=os.path.join(ROOT,"dist","Your-Life-in-Seasons-comic.epub")
W,H=1800,2700
TITLE="Your Life in Seasons: The Comic"; AUTHOR="Anushka Bharti"; UID="urn:uuid:"+str(uuid.uuid5(uuid.NAMESPACE_URL,"your-life-in-seasons-comic"))
def xhtml(title, img, w, h):
    return f'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops"><head><title>{title}</title>
<meta name="viewport" content="width={w}, height={h}"/>
<style>html,body{{margin:0;padding:0;width:{w}px;height:{h}px}} img{{width:{w}px;height:{h}px;display:block}}</style></head>
<body><img src="{img}" alt="{title}"/></body></html>'''
os.makedirs(os.path.dirname(OUT),exist_ok=True)
with zipfile.ZipFile(OUT,"w") as z:
    z.writestr("mimetype","application/epub+zip",compress_type=zipfile.ZIP_STORED)
    z.writestr("META-INF/container.xml",'<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>')
    manifest=[]; spine=[]
    # cover
    cw,ch=Image.open(COVER).size
    z.write(COVER,"OEBPS/images/cover.jpg"); manifest.append('<item id="cover-img" href="images/cover.jpg" media-type="image/jpeg" properties="cover-image"/>')
    z.writestr("OEBPS/cover.xhtml",xhtml("Cover","images/cover.jpg",cw,ch)); manifest.append('<item id="cover" href="cover.xhtml" media-type="application/xhtml+xml"/>'); spine.append('<itemref idref="cover"/>')
    for i,f in enumerate(PAGES,1):
        name=os.path.basename(f)[:-4]
        im=Image.open(f).convert("RGB"); buf=os.path.join(ROOT,"dist","_tmp.jpg"); im.save(buf,"JPEG",quality=88)
        z.write(buf,f"OEBPS/images/{name}.jpg"); os.remove(buf)
        z.writestr(f"OEBPS/{name}.xhtml",xhtml(f"Page {i}",f"images/{name}.jpg",W,H))
        manifest.append(f'<item id="i{name}" href="images/{name}.jpg" media-type="image/jpeg"/>')
        manifest.append(f'<item id="{name}" href="{name}.xhtml" media-type="application/xhtml+xml"/>')
        spine.append(f'<itemref idref="{name}" properties="{"page-spread-right" if i%2 else "page-spread-left"}"/>')
    nav='<?xml version="1.0" encoding="utf-8"?><html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops"><head><title>Contents</title></head><body><nav epub:type="toc"><ol><li><a href="cover.xhtml">Cover</a></li>'+"".join(f'<li><a href="{os.path.basename(f)[:-4]}.xhtml">Page {i}</a></li>' for i,f in enumerate(PAGES,1) if i==1 or i%10==0)+'</ol></nav></body></html>'
    z.writestr("OEBPS/nav.xhtml",nav); manifest.append('<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>')
    now=datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    opf=f'''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid" prefix="rendition: http://www.idpf.org/vocab/rendition/#">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="uid">{UID}</dc:identifier><dc:title>{TITLE}</dc:title><dc:creator>{AUTHOR}</dc:creator><dc:language>en</dc:language>
<meta property="dcterms:modified">{now}</meta>
<meta property="rendition:layout">pre-paginated</meta><meta property="rendition:orientation">portrait</meta><meta property="rendition:spread">auto</meta>
<meta name="fixed-layout" content="true"/><meta name="original-resolution" content="{W}x{H}"/><meta name="book-type" content="comic"/><meta name="primary-writing-mode" content="horizontal-lr"/>
</metadata>
<manifest>{"".join(manifest)}</manifest>
<spine>{"".join(spine)}</spine></package>'''
    z.writestr("OEBPS/content.opf",opf)
print("wrote",OUT,len(PAGES),"pages",f"{os.path.getsize(OUT)/1e6:.1f} MB")
