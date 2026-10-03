#!/usr/bin/env python3
"""
comic_export_ops.py: helpers for the central export step (see comic/PANEL-PIPELINE.md, step 4).

  python3 tools/comic_export_ops.py pending [N]          -> list up to N panel ids that have a sidecar but no PNG
  python3 tools/comic_export_ops.py add_pages id1 id2 ... -> JSON list of add_page operations (sizes per aspect)
  python3 tools/comic_export_ops.py fills PAGEIDS id1 id2 ... -> JSON list of insert_fill ops; PAGEIDS = comma-separated Canva page ids in the same order
"""
import sys, os, json, glob
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PD=os.path.join(ROOT,"comic","panels")
SIZE={"PORTRAIT_3_4":(1200,1600),"LANDSCAPE_3_2":(1800,1200),"LANDSCAPE_2_1":(2000,1000),"SQUARE_1_1":(1400,1400),
      "LANDSCAPE_4_3":(1600,1200),"PORTRAIT_9_16":(1080,1920)}
import yaml
_LAYOUT={}
for _f in glob.glob(os.path.join(ROOT,"comic","script","*.yaml")):
    for _p in yaml.safe_load(open(_f,encoding="utf-8")) or []:
        _LAYOUT[_p["id"]]=_p["layout"]
RATIO={"single":"PORTRAIT_3_4","two":"LANDSCAPE_3_2","three":"LANDSCAPE_2_1","four":"SQUARE_1_1","grid6":"LANDSCAPE_4_3","fact":"LANDSCAPE_4_3"}
def side(pid):
    d=json.load(open(os.path.join(PD,pid+".json")))
    if not d.get("aspect"):
        d["aspect"]=RATIO.get(_LAYOUT.get(pid.split("-")[0],"fact"),"LANDSCAPE_4_3")
    return d
def pending(n=None):
    ids=[]
    for f in sorted(glob.glob(os.path.join(PD,"p*.json"))):
        pid=os.path.basename(f)[:-5]
        if not os.path.exists(os.path.join(PD,pid+".png")) and side(pid).get("media_id"):
            ids.append(pid)
    return ids[:n] if n else ids
cmd=sys.argv[1]
if cmd=="pending":
    n=int(sys.argv[2]) if len(sys.argv)>2 else None
    ids=pending(n); print(" ".join(ids)); print(len(ids),"pending",file=sys.stderr)
elif cmd=="add_pages":
    ops=[]
    for pid in sys.argv[2:]:
        w,h=SIZE[side(pid).get("aspect","LANDSCAPE_4_3")]
        ops.append({"type":"add_page","width":w,"height":h,"background_color":"#FFFFFF","title":pid})
    print(json.dumps(ops))
elif cmd=="fills":
    pages=sys.argv[2].split(","); ids=sys.argv[3:]
    assert len(pages)==len(ids),(len(pages),len(ids))
    ops=[]
    for pg,pid in zip(pages,ids):
        w,h=SIZE[side(pid).get("aspect","LANDSCAPE_4_3")]
        ops.append({"type":"insert_fill","page_id":pg,"asset_type":"image","asset_id":side(pid)["media_id"],"alt_text":pid,"left":0,"top":0,"width":w,"height":h})
    print(json.dumps(ops))
