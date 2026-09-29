# Kundali Made Simple — Vedic Astrology from Your First Chart to Your First Consultation

A complete, illustrated beginner-to-consultant ebook on Vedic astrology (Jyotish), written in the voice of a veteran Indian astrologer. Parashari astrology is the backbone; **Lal Kitab** material appears only in clearly labelled boxes with its source stated.

## Read it

| Format | File |
|---|---|
| PDF (print-ready, A4) | `dist/Kundali-Made-Simple.pdf` |
| Single-file HTML (open in any browser, dark charts inline) | `dist/Kundali-Made-Simple.html` |
| Markdown chapters (GitHub renders these with the diagrams) | `book/` |

## Contents

**Part I — Foundations:** 1 Welcome · 2 The Twelve Signs · 3 The Nine Planets · 4 The Twelve Houses · 5 Reading Your First Chart and the Twelve Ascendants
**Part II — Core tools:** 6 Aspects and Conjunctions · 7 The 27 Nakshatras · 8 Functional Benefics and Malefics by Lagna · 9 House Lords · 10 Yogas · 11 Divisional Charts · 12 Planetary Strength
**Part III — Timing:** 13 Vimshottari Dasha · 14 Transits and Sade Sati · 15 Yogini, Jaimini and the Annual Chart · 16 Panchanga and Muhurta · 17 Prashna
**Part IV — Life questions:** 18 Career and Wealth · 19 Marriage and Relationships · 20 Health and Longevity · 21 Children, Education, Property, Travel and Spirituality
**Part V — The consulting room:** 22 Lal Kitab (clearly labelled) · 23 Remedies · 24 The Consultation · 25 Three Complete Case Studies
**Appendices:** A Quick Reference Tables · B Glossary · C Reading List, Cheat Sheets and the Consultation Checklist

## Rebuild the book

```bash
cd vedic-astrology-ebook
pip install markdown            # once
python3 tools/build.py          # → dist/*.html and (if Chromium is available) dist/*.pdf
```

Diagrams are generated with `tools/kundali_svg.py` (North/South Indian charts, Lal Kitab chart, aspect diagrams, zodiac and nakshatra wheels, dasha bars). Example:

```bash
python3 tools/kundali_svg.py north --lagna 8 \
  --planets "1:Su,Me;12:Ve;5:Ma(R);7:Ju(R);2:Sa;4:Ra;10:Ke;9:Mo" \
  --title "Chart A — Meera" --out images/my-chart.svg
```

`AUTHORING.md` is the style guide and fact contract every chapter follows; `book/90-appendix-a-quick-reference.md` holds the master tables all chapters agree with.

## A note on sources

The teaching voice is a persona; anecdotes are composites and the three case-study charts are constructed for teaching. Classical sources: *Brihat Parashara Hora Shastra*, *Brihat Jataka*, *Phaladeepika*, *Saravali*, *Jataka Parijata*, *Prashna Marga*. Lal Kitab references are to Pt. Roop Chand Joshi's Urdu editions (1939–1952); Hindi translations vary and the book says so wherever it matters.
