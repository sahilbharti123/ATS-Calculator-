# Your Life in Seasons: the comic book. Bible.

This is the contract for every page. Read it before writing or drawing anything.

## What the book is

A full comic book, not a prose book with strips. About 120 pages, 6 x 9 in, full colour. It teaches the
Vedic dasha system (the planetary "seasons" of a life) through the nine planets as comic characters who
take turns running the reader's life, and through You, the reader, who has to live with them. Every page
is panels, speech bubbles and short captions. There is no narrator paragraph anywhere. The teaching point
of a page lives in the last caption, one line, deadpan.

The prose book in `book/` stays in the repository as a companion. The comic is the product.

## Who it is for

Someone in a hard year who wants to understand what time it is in their life, and would rather laugh
than be lectured. No Sanskrit is needed. Every Sanskrit word appears once, in a small footnote box, with
the plain word beside it, and after that the plain word is used (season, sub-season, sub-sub-season,
the Moon's star, rising sign, room).

## The pitch in one page

Your life has a management team of nine. They take turns. Each one runs the show for a fixed number of
years (Ketu 7, Venus 20, Sun 6, Moon 10, Mars 7, Rahu 18, Jupiter 16, Saturn 19, Mercury 17; always in
that order; the one who starts depends on where the Moon was when you were born). Inside each manager's
term, the other eight take turns as deputy, in the same order, starting with the manager. Inside the
deputy's term, a third one takes turns as the intern. So on any given day your life is being run by a
manager, a deputy and an intern, and how it feels is the three of them in one room.

## The cast (fixed; never change a costume or a voice)

Reference sheets: `cover/characters/<Name>.png`. Canva media ids for image-to-image references:
Saturn MAHW8uO0kJ8 · Sun MAHW8lW6x60 · Moon MAHW8oobytk · Mars MAHW8uKI2_g · Mercury MAHW8ob-FW4 ·
Jupiter MAHW8nJAiog · Venus MAHW8pXxy8g · Rahu MAHW8nDqRKg · Ketu MAHW8rnmg-M · You MAHW8pxRN9w.

| Character | Look | Voice and running gag | Runs for |
|---|---|---|---|
| **You** | Young Indian woman, mustard kurta, jeans, sling bag, sometimes a small brown dog | Dry, tired, reasonable. The only sane person in the room. Says "Why." as a statement. | the whole book |
| **Sun** (the King) | Golden skin, radiant crown, royal red and gold | Announces himself. Needs applause. Hates being ignored. "Did everyone see what I did?" | 6 years |
| **Moon** (the Queen Mother) | Silver-white saree, crescent in hair, always has a tiffin or a shawl | Feels everything, feeds everyone, calls at 11 pm to ask if you ate. Mood changes with the tide. | 10 years |
| **Mars** (the Commander) | Red skin, brass armour, red cape, a whistle | Everything is a drill. 5 am. Picks fights with furniture. Loves You in the way a coach loves a player. | 7 years |
| **Mercury** (the Prince) | Green, young, sharp kurta, three phones, a notebook | Talks fast, starts six things, finishes four. Copies whoever he sits next to. | 17 years |
| **Jupiter** (the Priest) | Big, yellow-gold robes, kind beard, a book and a laddoo | Wise, generous, slightly too fond of sweets and of giving advice nobody asked for. Makes things bigger, including waistlines. | 16 years |
| **Venus** (the Minister of Pleasure) | Pink and gold saree, jasmine, chai, phone | Charm. Shopping. Romance. Good taste. Allergic to budgets. "Treat yourself" is a policy. | 20 years |
| **Saturn** (the Judge) | Dark blue skin, old, grey beard, black robe, a ledger, a crow, a slow walk | Speaks slowly and rarely. Never cruel, never in a hurry, never wrong about what you avoided. Makes You do the thing. The reader's secret favourite by the end. | 19 years |
| **Rahu** (the Stranger with the shopping bags) | Smoky purple, no lower body (smoke), designer sunglasses, foreign shopping bags, a drone | Wants everything, especially what is abroad, new, or forbidden. Hype. Brilliant and exhausting. | 18 years |
| **Ketu** (the Sadhu with no head) | Saffron robes, a glowing light where the head should be, bare feet, a begging bowl | Wants nothing. Answers questions with silence or one word. Quietly removes things from your flat while you sleep. | 7 years |

The planets are **not** the Hindu gods and are never named as deities. They are "the planets", drawn in
an Indian mythological cartoon style. No religious ritual is shown; no stones, mantras or remedies are
sold. The "practice" in a hard season is always ordinary: sleep, walk, call your mother, finish the thing.

## Tone rules

1. Funny first, true always. Every gag must be astrologically correct. Check `tools/CASE-TIMELINES.md`
   and `tools/REFERENCE-TABLES-FROM-BOOK-1.md`; the prose chapters in `book/` are the fact source for
   each planet's season (how it feels in body, mind, home, love, work, money; its wrong rooms; its
   practices).
2. Deadpan captions, Instagram-astrology-meme register, but never mean. The joke is on the planets, or on
   all of us; never on the reader for being poor, single, ill or unmarried.
3. **No fear.** Never predict death, divorce, bankruptcy, accidents or illness. A hard season is a season
   with a homework, drawn as a homework (Saturn handing over a ledger), not as doom.
4. No em dashes anywhere, in bubbles or captions. Short sentences. A bubble holds at most 18 words.
5. Plain words only, Sanskrit once in a footnote box: mahadasha = season (manager), antardasha =
   sub-season (deputy), pratyantardasha = sub-sub-season (intern), nakshatra = the Moon's star,
   lagna = rising sign, bhava = room, Sade Sati = Saturn's seven and a half years, gochar = weather.
6. Indian everyday settings: a 2BHK flat, a Mumbai local, an office with a broken AC, a wedding, a
   bank queue, a mother's kitchen, a gym at 5 am, an airport, a temple step (only as a quiet place to
   sit), a hospital waiting room (never a bed), a Swiggy delivery at the door.
7. The three case lives (Meera, Arjun, Devika) appear only in Part 3, briefly, as "three friends of You".

## Page grammar

Pages are built from a small set of layouts so the compositor can draw them:

- `single`: one big panel + title caption at top + punchline caption at bottom. For arrivals and gags.
- `two`: two stacked panels (setup / payoff).
- `three`: three panels in a row (the classic strip) + bottom caption.
- `four`: 2 x 2 grid. For "how it feels" pages (body, home, love, work) and for 4 sub-seasons.
- `grid6`: 3 x 2 grid of small panels, for the fast "the other deputies" pages.
- `fact`: a half-page panel + a boxed plain-words fact (the one place numbers and the Sanskrit word go).

Every page ends with a **bottom caption**: the lesson in one deadpan sentence (max 22 words).

## Script format (`comic/script/*.yaml`)

```yaml
- id: p041
  part: 2
  chapter: mars
  layout: three
  title: "Mars season, Venus deputy, Sun intern"
  panels:
    - scene: "You at an office desk at 9 pm. Mars slams a clipboard GYM 5 AM on the desk. Venus lounges on the desk edge with chai and a dating app. The Sun bursts through the door in a blaze."
      chars: [You, Mars, Venus, Sun]
      bubbles:
        - {who: Mars, text: "Training at five. Non-negotiable."}
        - {who: Venus, text: "After which, brunch. Also non-negotiable."}
        - {who: Sun, text: "AND I have arrived."}
        - {who: You, text: "It is a Tuesday."}
  caption: "Manager, deputy, intern. Your week is whatever the three of them agree on, which is nothing."
  footnote: "mahadasha = season (the manager) · antardasha = sub-season (the deputy) · pratyantardasha = sub-sub-season (the intern)"
```

`scene` is written for the image model: who is where, doing what, in which setting, with a clear empty
area for bubbles. No text in the image. `bubbles` are drawn by the compositor, in order, anchored to the
named speaker.

## Structure (about 120 pages)

**Part 1. The management team (pp. 1 to 16).**
Cover · title · "Meet the team" (double page, all nine + You) · how the turns work (the fixed order, the
years) · where You board (the Moon's star picks who starts) · the balance at birth gag ("you joined in
the middle of Venus's term; she is not restarting for you") · deputies and interns · the one plain-words
fact page · "How to find yours" (free app, three screenshots as drawn panels).

**Part 2. The nine seasons (pp. 17 to 104).** One chapter per planet, in Vimshottari order from Ketu, each about 9 to 10 pages:
1. **Arrival** (`single`): the planet takes the keys from the previous one. Handover gag.
2. **How it feels** (`four`): body, home, love, work.
3. **Money and mind** (`two`).
4. **The deputies** (`grid6` + `three`): the eight sub-seasons, in order, one panel each; the two or three
   that matter most get a full `three` page (e.g. Venus/Saturn, Saturn/Mars, Rahu/Saturn, Mars/Venus/Sun).
5. **The wrong room** (`two`): the 6/8/12 rule drawn as the deputy being given the storeroom to sleep in.
6. **Where the planet sits** (`fact`): on your side or testing you, by rising sign, as a tiny colour table.
7. **Homework** (`three`): what to actually do. Ordinary. Funny.
8. **Last year and handover** (`single`): the next planet is already in the hallway with luggage.

**Part 3. Living with the team (pp. 105 to 120).**
The intern (sub-sub-seasons) explained with the Mars/Venus/Sun page · the changeover year · Saturn's
seven and a half years (a weather visit, not a manager) · "Three friends of You" (Meera, Arjun, Devika,
one page each: their current manager/deputy and what it asks) · your own season map (a worksheet page) ·
the closing page (Saturn and Venus on a bench; "It was never random").

## Art pipeline

1. Panels are generated with Canva `generate-image`, image-to-image, passing the media ids of every
   character in the panel plus the style line. Prompt = style line + scene + "Leave empty space for
   speech bubbles. No text or lettering in the image."
2. Style line: "Comic book panel, cel-shaded Indian mythological cartoon style, clean bold outlines,
   flat colours with soft shading, modern Indian setting, expressive faces, keep every character's face,
   skin colour and costume exactly as in the reference images."
3. `tools/comic_pages.py` composes pages from the script and the panel images: borders, gutters,
   bubbles with tails to the speaker, title and bottom captions, footnote box, page number.
4. Output: `dist/Your-Life-in-Seasons-comic-print-6x9.pdf` (one page per sheet, 300 dpi) and a
   fixed-layout EPUB for Kindle.
