# Your Life in Seasons

*A kind guide to the dasha system, the Vedic astrology of timing, and what each chapter of your life is asking of you.*
Book 2 in the **Astrology, Gently** series by Anushka Bharti.

A 200-page book on the Vimshottari dasha system written entirely in plain English: a mahadasha is a *season*, an antardasha is a *sub-season*, a nakshatra is *the Moon's star*. Every rule comes with its reason, every planet is a comic character, every table is colour-coded, and three worked lives show the method end to end.

## Structure

**Part I: The idea of seasons.** 1 The same person, different lives · 2 The sky's timetable · 3 Seasons inside seasons
**Part II: The nine seasons.** 4 Ketu · 5 Venus · 6 Sun · 7 Moon · 8 Mars · 9 Rahu · 10 Jupiter · 11 Saturn · 12 Mercury
**Part III: Reading your own timetable.** 13 Where the planet sits · 14 Weather inside the season · 15 The changeover · 16 Three lives in seasons · 17 Living well in a hard season · 18 Your season map
**Appendices.** A The tables · B Plain words to Sanskrit · C Getting your season map from free tools · D The Story Bank

## Build

```bash
cd your-life-in-seasons
python3 tools/comic.py --all        # comic strips from tools/comic_scripts.py
python3 tools/storybank.py          # Appendix D from the Story boxes
python3 tools/lint.py               # structure, plain-words rule, no em dashes
python3 tools/build.py              # dist/Your-Life-in-Seasons.html and .pdf (A4)
python3 tools/build.py --print      # dist/Your-Life-in-Seasons-print-6x9.pdf
python3 tools/svg2png.py && python3 tools/build_epub.py   # dist/Your-Life-in-Seasons.epub
python3 tools/print_wrap_cover.py <pages>                 # cover/cover-paperback-wrap.pdf
```

`AUTHORING.md` is the contract (voice, plain-words lexicon, depth rule, chapter plan). `tools/CASE-TIMELINES.md` holds the binding dasha tables and the three case-study lives.
