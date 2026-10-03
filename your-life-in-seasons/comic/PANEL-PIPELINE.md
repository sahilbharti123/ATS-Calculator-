# Panel generation pipeline (for the generation agents)

Goal: for one script file (`comic/script/<file>.yaml`), produce one PNG per panel at
`comic/panels/<page id>-<n>.png` (n is the 1-based panel index) plus a sidecar
`comic/panels/<page id>-<n>.json`, using Canva through the MCP tools. Work in
`/home/user/ATS-Calculator-/your-life-in-seasons`.

## 0. Read first
- `comic/COMIC-BIBLE.md`: the cast table with each character's **Canva media id** (reference sheet) and look.
- Your script file. Each page has `layout` and `panels`, each panel has `scene` and `chars`.
- `comic/panels/p061-1.png` + `.json`: a finished example.
- Your job ends after step 2 (generation + sidecars + manifest). Export is done centrally (step 4).

## 1. Aspect ratio and page size per layout

| layout | `aspectRatio` for generate-image | container page (w x h) |
|---|---|---|
| single | PORTRAIT_3_4 | 1200 x 1600 |
| two | LANDSCAPE_3_2 | 1800 x 1200 |
| three | LANDSCAPE_2_1 | 2000 x 1000 |
| four | SQUARE_1_1 | 1400 x 1400 |
| grid6 | LANDSCAPE_4_3 | 1600 x 1200 |
| fact | LANDSCAPE_4_3 | 1600 x 1200 |

## 2. Generate every panel (mcp__Canva__generate-image, then mcp__Canva__get-generate-image-job)

Prompt = this template, filled in:

```
Comic book panel, cel-shaded Indian mythological cartoon style, clean bold outlines, flat colours with
soft shading, expressive faces, modern Indian setting. <SCENE> Characters from left to right: <CHARS>.
Keep each character's face, skin colour, costume and build exactly as in the reference images; the
reference images show the same characters. Leave calm, uncluttered space in the upper part of the
image for speech bubbles. No text, no letters, no signs, no logos, no speech bubbles in the image.
```

- `imageReferences`: one `{"type":"MEDIA","id":"<media id>"}` per character in the panel's `chars`, in the
  same order (ids from the bible). If `chars` is empty, omit the field.
- `aspectRatio` from the table.
- Poll `get-generate-image-job` with the jobId until SUCCESS (wait a few seconds between polls; use a
  short `sleep 8` via Bash between polls, never a long one). The result carries the new **media id**.
- Look at the returned thumbnail. Accept it if every listed character is present and recognisable,
  there are no extra people, and no lettering. Otherwise regenerate once with the problem named in the
  prompt (e.g. "exactly three characters", "no text on the whiteboard"). Accept the second try regardless
  and note it in the sidecar as `"note"`.
- Write the sidecar immediately: `comic/panels/<pid>-<n>.json` =
  `{"media_id": "...", "positions": {"Mars": 0.2, "You": 0.47, ...}, "aspect": "LANDSCAPE_2_1"}` where
  each position is your estimate of the character's head as a fraction of the image width (0 = left edge,
  1 = right edge), read from the thumbnail. This is what places the speech bubbles, so be careful.
- If a generation fails with a quota or rate-limit message, wait 60 seconds and retry once; if it fails
  again, stop generating, finish steps 3 to 5 for what you have, and say so in your report.

## 3. Pacing and quota (important)

Canva's image credits cool down if images are launched too fast: launch at most **one generate-image
call every 30 seconds** (`sleep 30` between launches). On "quota_cooldown", wait 90 s and retry once; if it
fails again, stop generating and report what you have. Never call `create-design` (its quota is exhausted
and it is not needed).

## 4. Export (done centrally, not by the generation agents)

Generation agents stop after step 2 and write `comic/panels/manifest-<script name>.json` with every
media id (`{"panels": {"<pid>-<n>": {"media_id": "..."}}}`). The coordinator then, in batches, adds pages
to the existing container design **DAHW851NwBY** (`read-design` with `open_transaction`, one `edit-design`
call with many `add_page` ops sized per layout, `read-design` for the new page ids, one `edit-design` call
with many `insert_fill` ops, `commit`), exports those pages as PNG at width 2400 and downloads them to
`comic/panels/<pid>-<n>.png`. `tools/comic_export_ops.py` prints the operation lists from the sidecars.

## 5. Check and report

Run `python3 tools/comic_pages.py pages <all your page ids>` and look at two or three of the rendered
pages in `comic/pages/` to confirm bubbles sit over the right speakers; adjust a sidecar's positions
if a tail points at the wrong character and re-render. Report: panels done, retries, anything that
looks wrong in the art (a missing character, odd anatomy, lettering), and any quota messages.

Never edit the script YAML or the bible; if a scene is impossible to draw, draw the closest thing and
report it.
