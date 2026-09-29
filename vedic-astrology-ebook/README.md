# Astrology, Gently: A kind, beginner-friendly guide to understanding your chart and yourself

A complete, illustrated beginner-to-consultant book on Vedic astrology (Jyotish) by **Anushka Bharti**, written for everyone who bought the classics and understood nothing. Every rule comes with its reason and an everyday parallel; every hard idea comes with a memory story from a royal court; every table is colour-coded. Parashari astrology is the backbone; **Lal Kitab** material appears only in clearly labelled boxes with its source stated. Ready for Amazon KDP (see `PUBLISHING.md`).

## Read it

| Format | File |
|---|---|
| Kindle eBook (reflowable EPUB 3) | `dist/Astrology-Gently.epub` |
| Paperback interior (6 × 9 in PDF) | `dist/Astrology-Gently-print-6x9.pdf` |
| Reading PDF (A4) | `dist/Astrology-Gently.pdf` |
| Single-file HTML (all diagrams inline) | `dist/Astrology-Gently.html` |
| Covers (eBook front JPG, paperback wrap PDF) | `cover/` |
| Markdown chapters (GitHub renders these with the diagrams) | `book/` |

## Contents

**Part I: Foundations:** 1 Welcome · 2 The Twelve Signs · 3 The Nine Planets · 4 The Twelve Houses · 5 Reading Your First Chart and the Twelve Ascendants
**Part II: Core tools:** 6 Aspects and Conjunctions · 7 The 27 Nakshatras · 8 Functional Benefics and Malefics by Lagna · 9 House Lords · 10 Yogas · 11 Divisional Charts · 12 Planetary Strength
**Part III: Timing:** 13 Vimshottari Dasha · 14 Transits and Sade Sati · 15 Yogini, Jaimini and the Annual Chart · 16 Panchanga and Muhurta · 17 Prashna
**Part IV: Life questions:** 18 Career and Wealth · 19 Marriage and Relationships · 20 Health and Longevity · 21 Children, Education, Property, Travel and Spirituality
**Part V: The consulting room:** 22 Lal Kitab (clearly labelled) · 23 Remedies · 24 The Consultation · 25 Three Complete Case Studies
**Appendices:** A Quick Reference Tables · B Glossary · C Reading List, Cheat Sheets and the Consultation Checklist · D The Story Bank (all 100+ memory stories in one place)

**How it teaches.** Every rule that is normally memorised: who is whose enemy, which conjunctions help, which planets serve which Lagna: comes as a short **📖 Story** from a royal court (the King Sun, the Queen Mother Moon, the Commander Mars, the Prince Mercury, the Priest Jupiter, the Minister of Pleasure Venus, the Judge Saturn, and the two strangers Rahu and Ketu), followed by the rule in one line. Every judging table is colour-coded 🟢 good · 🟡 mixed · 🔴 difficult, and the key diagrams (friendship web, conjunction grid, functional-nature table) use the same three colours.

## Rebuild the book

```bash
cd vedic-astrology-ebook
pip install markdown            # once
python3 tools/storybank.py      # regenerates Appendix D from the chapters' Story boxes
python3 tools/lint.py           # structure, facts-of-form, no em dashes
python3 tools/build.py          # → dist/Astrology-Gently.html and .pdf (A4)
python3 tools/build.py --print  # → dist/Astrology-Gently-print-6x9.pdf (KDP paperback interior)
python3 tools/svg2png.py        # renders diagrams to images_png/ for the EPUB
python3 tools/build_epub.py     # → dist/Astrology-Gently.epub (Kindle)
python3 tools/print_wrap_cover.py 446   # → cover/cover-paperback-wrap.pdf (use the print page count)
```

Diagrams are generated with `tools/kundali_svg.py` (North/South Indian charts, Lal Kitab chart, aspect diagrams, zodiac and nakshatra wheels, dasha bars). Example:

```bash
python3 tools/kundali_svg.py north --lagna 8 \
  --planets "1:Su,Me;12:Ve;5:Ma(R);7:Ju(R);2:Sa;4:Ra;10:Ke;9:Mo" \
  --title "Chart A: Meera" --out images/my-chart.svg
```

`AUTHORING.md` is the style guide and fact contract every chapter follows; `book/90-appendix-a-quick-reference.md` holds the master tables all chapters agree with.

## A note on sources

Anecdotes are composites and the three case-study charts are constructed for teaching. Classical sources: *Brihat Parashara Hora Shastra*, *Brihat Jataka*, *Phaladeepika*, *Saravali*, *Jataka Parijata*, *Prashna Marga*. Lal Kitab references are to Pt. Roop Chand Joshi's Urdu editions (1939–1952); Hindi translations vary and the book says so wherever it matters.
