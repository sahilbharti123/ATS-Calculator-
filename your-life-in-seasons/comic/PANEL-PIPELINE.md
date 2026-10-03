# Panel generation pipeline (for the generation agents)

Goal: for one script file (`comic/script/<file>.yaml`), produce one PNG per panel at
`comic/panels/<page id>-<n>.png` (n is the 1-based panel index) plus a sidecar
`comic/panels/<page id>-<n>.json`, using Canva through the MCP tools. Work in
`/home/user/ATS-Calculator-/your-life-in-seasons`.

## 0. Read first
- `comic/COMIC-BIBLE.md`: the cast table with each character's **Canva media id** (reference sheet) and look.
- Your script file. Each page has `layout` and `panels`, each panel has `scene` and `chars`.
- `comic/panels/p061-1.png` + `.json`: a finished example.

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

## 3. Put the panels in a container design (one design per script file)

1. `mcp__Canva__create-design` with brief "A completely blank white page with nothing on it, no text, no
   shapes, no images; an empty canvas for placing comic panel images." and format "Custom size 1600 x
   1200 px". Poll `mcp__Canva__get-create-design-async-job` (wait 15 s first) until it returns the design id.
2. `mcp__Canva__read-design` with `open_transaction: true` and fields `["page_metadata"]`. Note the
   `transaction_id`. Page 1 is Canva's own page; ignore it.
3. One `mcp__Canva__edit-design` call (`finalize: keep_open`, `page_index: 1`) whose `operations` list
   has one `add_page` per panel, in panel order, each with the page size for that panel's layout,
   `background_color "#FFFFFF"` and `title "<pid>-<n>"`. (Up to about 40 operations per call is fine;
   split into two calls if you have more.)
4. `read-design` with the transaction id and fields `["page_metadata"]` (and `design_content` with
   `page_indices` if page_metadata only lists page 1) to get every new page's id in order.
5. For each panel, `edit-design` (`finalize: keep_open`, `page_index: <its page number>`) with one
   `insert_fill` operation: `page_id`, `asset_type "image"`, `asset_id <media id>`, `alt_text "<pid>-<n>"`,
   `left 0, top 0, width <page w>, height <page h>`.
6. `edit-design` with `finalize: commit` and no operations.

## 4. Export and download

- `mcp__Canva__export-design` with `format: {"type":"png","lossless":true,"width":2400}` and `pages` =
  every page number except 1 (or omit `pages` and skip the first url). The result lists one URL per page
  in page order.
- Download each with Bash `curl -sS --max-time 120 -o comic/panels/<pid>-<n>.png "<url>"` (quote the
  URL). Then verify with PIL that each file opens and is 2400 px wide.
- Also save `comic/panels/manifest-<script name>.json`: `{"design_id": "...", "panels": {"<pid>-<n>":
  {"media_id": "...", "page": <page number>}}}` so panels can be re-exported later.

## 5. Check and report

Run `python3 tools/comic_pages.py pages <all your page ids>` and look at two or three of the rendered
pages in `comic/pages/` to confirm bubbles sit over the right speakers; adjust a sidecar's positions
if a tail points at the wrong character and re-render. Report: panels done, retries, anything that
looks wrong in the art (a missing character, odd anatomy, lettering), and any quota messages.

Never edit the script YAML or the bible; if a scene is impossible to draw, draw the closest thing and
report it.
