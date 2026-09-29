# Publishing *Astrology, Gently* on Amazon KDP

Everything you need to upload is in `dist/` and `cover/` after running the build (see README). This page lists what goes where and the choices already made for you.

## Files to upload

| KDP product | What to upload | File |
|---|---|---|
| Kindle eBook | Manuscript (reflowable EPUB 3) | `dist/Astrology-Gently.epub` |
| Kindle eBook | Cover (JPG, 1600 × 2560 px, 1.6:1) | `cover/cover-front.jpg` |
| Paperback | Manuscript (interior PDF, 6 × 9 in, no bleed) | `dist/Astrology-Gently-print-6x9.pdf` |
| Paperback | Cover (full wrap PDF: back + spine + front, with 0.125 in bleed) | `cover/cover-paperback-wrap.pdf` |

The wrap cover's spine width depends on the final page count. Rebuild it after any interior change:

```bash
python3 tools/build.py --print            # note the page count it prints
python3 tools/print_wrap_cover.py 446     # use that page count
```

## Choices already made

- **Trim size:** 6 × 9 in (the standard for nonfiction; also the cheapest print cost per page).
- **Interior:** the diagrams are colour. Choose **premium colour** on KDP if you want them printed in colour; the standard black-and-white option also works because every judgement dot uses a different *shape* (filled, half, empty circle) and every chart is line-work.
- **Paper:** white.
- **eBook:** reflowable, so readers can change font size. All 125 diagrams are embedded as high-resolution PNGs. The answers to the practice questions are printed directly under the questions (Kindle has no collapsible blocks).
- **Language:** English. **ISBN:** let KDP assign a free one for the paperback (fill the barcode area on the back cover automatically); the eBook needs none.

## Suggested listing copy

**Title:** Astrology, Gently
**Subtitle:** A kind, beginner-friendly guide to understanding your chart and yourself
**Author:** Anushka Bharti

**Description (use the back-cover text, expanded):**

You bought the books everyone recommends. You opened them with real hope. And within ten pages you felt stupid. You are not stupid. Those books were written for students who already knew the sky. This one is written for everyone else.

*Astrology, Gently* teaches Vedic astrology (Jyotish) as a language with a small grammar: nine planets, twelve signs, twelve houses, twenty-seven stars. Every rule comes with its reason, whether that reason is astronomy, the internal logic of the system, or a named classical author. Every hard idea comes with a short story from a royal court you will not forget: who is whose enemy, which planets help each other, which planet serves which rising sign. Every table is colour-coded. Lal Kitab is clearly labelled wherever it appears, so you always know which system you are using.

Twenty-five chapters take you from the twelve signs to your first consultation: aspects, nakshatras, functional benefics by Lagna, house lords, yogas, divisional charts, planetary strength, Vimshottari dasha, transits and Sade Sati, Panchanga and Muhurta, Prashna, and then the questions people actually ask about career, money, marriage, health and children. Three complete case-study readings show the whole method at work. Four appendices give you every reference table, a glossary, cheat sheets, and all 115 memory stories in one place.

And if you never read for anyone but yourself and the people you love, you will still understand your own life a great deal better. That is the real reason this book was written.

**Categories (pick up to three):** Body, Mind & Spirit › Astrology › Eastern; Body, Mind & Spirit › Astrology › General; Religion & Spirituality › Hinduism.

**Keywords (seven slots):** vedic astrology for beginners · jyotish · kundali reading · learn astrology · lal kitab · nakshatra · vimshottari dasha

## Before you press publish

1. Open the EPUB in Kindle Previewer (free from Amazon) and page through a chapter with tables, one with a chart, and the practice answers.
2. Open the print PDF and check any page with a wide table at 100 % zoom.
3. Read the copyright page and About the Author once more; change anything you want in `tools/build.py` (copyright text) and `book/95-about-the-author.md`.
4. Decide on the price. Similar 400-page Kindle titles in this category sit between $7.99 and $14.99; paperback printing cost for 446 pages in premium colour is high, so check KDP's printing-cost calculator before setting the paperback price.
