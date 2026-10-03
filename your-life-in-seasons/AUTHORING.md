# Authoring guide for *Your Life in Seasons* (Book 2 of the Astrology, Gently series)

This file is the contract every chapter follows. Read it fully before writing. Also read, for voice: `../vedic-astrology-ebook/book/00-a-love-letter.md` and `../vedic-astrology-ebook/book/01-welcome.md`. For facts: `tools/REFERENCE-TABLES-FROM-BOOK-1.md` (all planetary facts) and `tools/CASE-TIMELINES.md` (all dasha tables and the three case-study lives; binding).

## The book
**Title:** *Your Life in Seasons*
**Subtitle:** A kind guide to the dasha system, the Vedic astrology of timing, and what each chapter of your life is asking of you
**Author:** Anushka Bharti, a practising Vedic astrologer who taught herself after the classics failed her (never claim years of practice, chart counts or a guru lineage). Book 1 is *Astrology, Gently*; this is Book 2 and must stand alone (a reader may start here), while pointing to Book 1 for chart-reading depth.
**Reader:** an ordinary person, Indian or not, who may know nothing about astrology, who is in or near a hard or confusing stretch of life and wants to understand *why now* and *how long*. Also the Book 1 reader who wants depth on timing.
**Promise:** by the end the reader can find their own season and sub-season with a free app, understand what each of the nine seasons asks of a person, read the shape of their own life so far, prepare for the next changeover, and live a hard season without fear.
**Length:** the whole book is 50,000 to 55,000 words (about 200 printed pages). Chapters 1 to 3 and 13 to 18: 2,600 to 3,000 words. The nine season chapters (4 to 12): 2,500 to 2,900 words each. Appendices short. Do not exceed; depth comes from clarity, not length.

## Voice
First person, warm, plain, a fellow traveller a few steps ahead. Short sentences. Everyday Indian life for analogies (joint family, kitchen, school exams, office, trains, weddings, monsoon, WhatsApp family group). Honest about uncertainty. No fatalism ever: a hard season is a season with a task, not a verdict. No fear-selling. Anecdotes are composites ("a friend", "a woman I read for", "my own chart").

## THE PLAIN-WORDS RULE (the reader's central request; enforced by lint)
Indian astrology books fail readers with unexplained Sanskrit. This book uses **English words in the prose** and gives the Sanskrit **once, in parentheses, when a concept is introduced**, plus the glossary. After the introduction, use the English word only. The lexicon is binding:

| Say this in prose | Sanskrit (only in the first-use parenthesis and the glossary) |
|---|---|
| season (or "major season" when contrasting) | mahadasha |
| sub-season | antardasha |
| the small turns inside a sub-season (mention once in Ch 3) | pratyantardasha |
| the 120-year timetable | Vimshottari dasha |
| the Moon's star, your birth star | nakshatra |
| rising sign | Lagna |
| room (the twelve rooms of your chart) | bhava / house |
| sign | rashi |
| planet (the two shadow planets, Rahu and Ketu, keep their names) | graha |
| a planet that is on your side / a planet that tests you | functional benefic / functional malefic |
| the four pillar rooms (1, 4, 7, 10) | kendra |
| the three lucky rooms (1, 5, 9) | trikona |
| the three hard rooms (6, 8, 12) | dusthana |
| at its strongest place / at its weakest place / at home | exalted / debilitated / own sign |
| outshone by the Sun | combust |
| walking backwards | retrograde |
| the changeover, the turning point between seasons | dasha sandhi |
| the weather (the planets moving overhead now) | gochar / transit |
| Saturn's seven and a half years | Sade Sati |
| a practice (never "remedy" alone) | upaya |
| the planet that stands for X (the Sun stands for the father, and so on) | karaka |
| the chart's timetable, your season map | dasha chart |

Never use: maraka, dusthana, badhaka, yoga (as a technical term), varga, navamsa, ayanamsa, karakamsa, arudha, drishti (say "looks at" or "casts its gaze on"), yuti (say "sits with"), neecha, uccha, paksha. If a concept needs one of these, explain it in English and leave the Sanskrit out or put it in the glossary only. Lint flags any Sanskrit lexicon word that appears outside parentheses more than twice per chapter.

Planet names are English. Weekday and god names may appear in stories. The word *dasha* itself is allowed in prose because it is in the subtitle; introduce it in Chapter 1 as "the dasha system, which simply means the system of seasons" and then prefer "season".

## Depth: a reason for everything
Every rule gets its reason in a `> **🔍 Why?** ...` box or the paragraph after it: astronomical, the system's own logic, a named classical author (Parashara mainly), or tradition, and NAME which it is. Then one everyday parallel. Where the honest answer is "tradition gives this and no reason", say so (the 120 years, the order and lengths of the nine seasons).

## Stories and colour
The royal court cast from Book 1 continues (the King Sun, the Queen Mother Moon, the Commander Mars, the clever young Prince Mercury, the Royal Priest Jupiter, the Minister of Pleasure Venus, the old Judge of Labour Saturn, the smoke-headed Stranger Rahu, the headless Sadhu Ketu). A season is "the years when that courtier runs the household". Each chapter has 2 to 4 `> **📖 Story: Title.** ... **Rule:** ...` boxes (60 to 180 words). Every table that judges uses 🟢 🟡 🔴 dots (the build turns them into shapes). Boxes available (exact labels): `🧭 Anushka's rule of thumb:` · `🔍 Why?` · `📖 Story: Title.` · `💡 Did you know?` · `⚠️ Common mistake:` · `🪔 If you read for others:` · `✍️ Try this:` (exercises with `<details><summary>Answers</summary>` where there are answers; many "Try this" items are reflective and need no answers block).

## Hard rules
1. **No em dashes (—) anywhere.** Commas, colons, full stops, parentheses. En dashes only inside numeric ranges.
2. **No death, divorce, bankruptcy or illness predictions.** Say "a period to take health seriously", "a season that tests a marriage", never the event.
3. **No real living people.** Case studies are Meera, Arjun and Devika (constructed; data in `tools/CASE-TIMELINES.md`). Their timelines and planet positions are binding; compute anything else with python3 before writing it.
4. **Facts** agree with `tools/REFERENCE-TABLES-FROM-BOOK-1.md` and `tools/CASE-TIMELINES.md`. Dates are approximate ("around June 2027"); say so once per chapter.
5. **Markdown:** file `book/NN-slug.md`, first line `# Chapter N: Title`; `##` and `###` only; images `![alt](../images/chNN-name.svg)` on their own line followed by `*Figure N.x: caption*`; GFM tables.
6. Every chapter ends with `## In one breath` (5 to 7 bullets) and `## Try this` (3 to 5 reflective exercises; include an answers block only when exercises have factual answers).
7. **Software:** recommend free tools by name (Jagannatha Hora, AstroSage app, Drik Panchang) and describe where the dasha table appears; the Lahiri ayanamsa is "the standard Indian setting" (say ayanamsa once in Ch 2 only, in parentheses).

## The chart tool
`python3 tools/kundali_svg.py <kind> ...` as in Book 1 (north, south, dasha bar, aspect, housegroups, sadesati). The `dasha` kind draws the 120-year bar: `python3 tools/kundali_svg.py dasha --start-lord Mercury --title "..." --caption "..." --out images/chNN-x.svg`. For timelines with dates, hand-write SVGs (740 px wide, cream #fffaf0, border #b8956a, headings #1e2a5a navy, text #2b3350, season colours: Ketu #e9d5ff, Venus #fbcfe8, Sun #fed7aa, Moon #e5e7eb, Mars #fecaca, Rahu #c7d2fe, Jupiter #fde68a, Saturn #bfdbfe, Mercury #bbf7d0). Validate every SVG with `python3 -c "import xml.dom.minidom,sys;xml.dom.minidom.parse(sys.argv[1])" images/x.svg`. 2 to 4 figures per chapter; no SVG text may contain an em dash.

## Chapter plan (binding)

**Part I: The Idea of Seasons**
- **Ch 1. The same person, different lives.** Open with three short composite scenes: the same woman at 24, 31 and 40 behaving like three people. The premise: life moves in chapters, and Vedic astrology has a timetable for them. What the dasha system is in one paragraph (Parashara's 120-year timetable keyed to the Moon's star at birth), what it is not (a script; the theory of three kinds of karma in plain words), what the reader will be able to do by the end. Introduce the court cast in one Story. Introduce the plain-words promise and the Book 1 relationship. Why? boxes: why timing matters more than character for the questions people actually ask ("how long will this last?"); why the Moon is the starting point.
- **Ch 2. The sky's timetable: how the seasons work.** The nine planets as nine seasons with their lengths (Ketu 7, Venus 20, Sun 6, Moon 10, Mars 7, Rahu 18, Jupiter 16, Saturn 19, Mercury 17; total 120). The fixed order and why it never changes. How your first season is chosen (the Moon's star at birth; the 27 stars in three rounds of nine lords) and the balance at birth (walk Meera's: Moon at 21° Cancer in Ashlesha, Mercury's star; 9° of 13°20′ remaining = 67.5% of 17 years = 11.475 years), with the honest note that the 120 years and the lengths are tradition, not astronomy. How to find your seasons in a free app in five steps. A "which season am I in" quick table by age for each starting season. Figures: dasha bar; a hand-drawn "wheel of 120 years"; the Moon's star to first season table.
- **Ch 3. Seasons inside seasons.** Sub-seasons (the proportional rule, with the 9×9 table from CASE-TIMELINES as Figure/Table), the order (starts with the season's own lord), the small turns (one paragraph), how to read a dasha table from software, the changeovers as sensitive stretches, the two questions for any sub-season: is the sub-lord a friend of the season lord, and where does it sit from the season lord (the 6/8/12 "wrong room" rule, in plain words). Worked: Meera's Venus season opened into its nine sub-seasons with dates; her marriage in Venus/Rahu (2014 to 2017). Figures: Venus sub-season timeline; a "friend or stranger" grid of the nine planets (🟢🟡🔴).

**Part II: The Nine Seasons** (one chapter each, same skeleton: 1 the courtier and what the season asks of you; 2 how it feels: body, mind, home, love, work, money; 3 the arc: the first year, the middle, the last year; 4 when this planet is on your side vs when it tests you (by rising sign, in plain words, with a 12-row 🟢🟡🔴 table from the Book 1 functional-nature table); 5 the room it sits in changes the story (a compact 12-room table, one line each); 6 the sub-seasons that matter most inside it (3 or 4, with the 6/8/12 logic); 7 two or three stories (composite); 8 what to do and what not to do (practices, not stones); 9 one case-study life passing through this season with real dates from CASE-TIMELINES; In one breath; Try this.)
- **Ch 4. The Ketu season (7 years): the art of letting go.** The headless Sadhu; endings, detachment, spiritual pull, sudden exits, research and solitude; why it is often the season people misread as "nothing is happening". Case: Meera's Ketu season age 11.5 to 18.5 (June 2000 to June 2007; her Saturn's seven and a half years overlapped it).
- **Ch 5. The Venus season (20 years): the long bloom.** Love, marriage, comfort, beauty, money through pleasure, the danger of softness; why 20 years changes a person. Case: Meera's Venus season June 2007 to June 2027 (marriage 2016 in Venus/Rahu; Venus/Saturn 2020 to 2023 as the testing stretch; the changeover to the Sun around June 2027).
- **Ch 6. The Sun season (6 years): who am I when nobody is watching?** Identity, father, authority, visibility, health of the heart and spine; short but defining. Case: Devika's Sun season July 1998 to July 2004 (marriage 2003 to 2004 in Sun/Venus); Meera's coming Sun season from mid-2027 as a forward look.
- **Ch 7. The Moon season (10 years): the household of the mind.** Mother, home, moods, the public, nourishment, moves; the Moon's phase at birth matters here. Case: Devika's Moon season July 2004 to July 2014 (daughter born 2007 to 2008 in Moon/Jupiter); Arjun's childhood Moon season.
- **Ch 8. The Mars season (7 years): the commander takes charge.** Courage, conflict, property, siblings, surgery and accidents (phrased as "take care"), sport and ambition; a short, hot season. Case: Devika's Mars season July 2014 to July 2021 (surgery 2016 to 2018 in Mars/Saturn); Arjun's school-years Mars season.
- **Ch 9. The Rahu season (18 years): the great churning.** Hunger, ambition, foreign places, technology, confusion and illusion, sudden rises and falls; why Rahu "borrows" the nature of the planet whose sign it sits in; the most misunderstood season. Case: Arjun's Rahu season Dec 2013 to Dec 2031 (finished studies 2017 in Rahu/Jupiter, first job 2018, stuck 2022 to 2024 in Rahu/Mercury; Rahu/Venus 2025 to 2028 now); Devika's Rahu season July 2021 to July 2039 (property dispute 2020 to 2021 at the changeover).
- **Ch 10. The Jupiter season (16 years): growth and grace.** Teachers, children, faith, expansion, weight (literal and otherwise), generosity; why Jupiter's season can disappoint when Jupiter tests you. Case: Arjun's coming Jupiter season from Dec 2031; Devika's from July 2039 as a forward look.
- **Ch 11. The Saturn season (19 years): the long audit.** Work, limits, loneliness, maturity, elders, chronic matters, the slow rewards; Saturn's seven and a half years inside a Saturn season; why this is the season people fear and the one that builds the most. Case: none of the three is in it yet; use Meera's future Saturn season (2084) only as a note and construct a composite ("a man I read for, in Saturn/Saturn at 52").
- **Ch 12. The Mercury season (17 years): the clever years.** Learning, speech, trade, nerves, travel, youthfulness, scattered attention; Mercury takes the colour of its company. Case: Meera's Mercury season (birth to June 2000) as childhood; Arjun's at the end of life as a note.

**Part III: Reading Your Own Timetable**
- **Ch 13. Where the planet sits changes the season.** The three questions to ask about any season lord: which rooms does it own and sit in, how strong is it (home/strongest/weakest/outshone/walking backwards, in plain words), and who is it with. The "hidden agenda" refinement: the season lord also speaks for the planet whose star it sits in (label as the modern KP-influenced practice). Worked on all three case lives for their current seasons.
- **Ch 14. Weather inside the season.** The planets overhead now: Saturn (2½ years a sign), Jupiter (a year a sign), Rahu and Ketu (1½ years). Saturn's seven and a half years explained from the Moon; how a transit lands differently inside a friendly vs a testing season; the "two signatures" rule (Saturn and Jupiter both touching a room) for timing events. Approximate positions 2026 to 2030 with the instruction to check an app.
- **Ch 15. The changeover.** The last year of a season and the first year of the next as a bridge; what people typically feel; how to prepare (closing rituals in plain secular terms: review, gratitude, clearing, a letter to the next season); the special cases: Venus to Sun (comfort to identity), Rahu to Jupiter (hunger to meaning), Mars to Rahu, Saturn to Mercury. Case: Meera's Venus-to-Sun changeover around June 2027 as a live example.
- **Ch 16. Three lives in seasons.** Full season maps for Meera, Arjun and Devika from birth to now with the dated events from CASE-TIMELINES, read as stories, each ending with "what this season asks of her/him now" and "what the next one will ask". Figures: three hand-drawn life-timeline SVGs.
- **Ch 17. Living well in a hard season.** The three seasons people fear (Saturn, Rahu, Ketu) and the sub-seasons that bite; the mindset (a season has a task); daily practices matched to each planet (conduct, service, routine, the planet's day), when to seek medical or psychological help (plainly), what not to buy (stones sold out of fear), and how to speak to family members about their seasons without frightening them.
- **Ch 18. Your season map.** A workbook chapter: ten steps to build your own season map from an app printout, mark your life events, read your past seasons honestly, identify the current sub-season and its task, and write a one-page "letter to this season". A 20-question self-reading. A closing letter from the author.

**Appendices**
- **Appendix A. The tables.** The nine seasons and lengths; the 9×9 sub-season table; the Moon's star to first season table (27 rows: star, span, first season lord); a "season by age" ready-reckoner for all nine starting seasons; approximate transit positions 2026 to 2032 (flagged approximate).
- **Appendix B. Plain words to Sanskrit.** Every English term in the lexicon with its Sanskrit, a one-line definition and the chapter it appears in; 60 to 90 entries.
- **Appendix C. Getting your season map from free tools.** Step-by-step for Jagannatha Hora (desktop) and the AstroSage app (mobile), what to set (sidereal, Lahiri as the standard Indian setting, Vimshottari), where to read the table, how to print or screenshot it, what to do if the birth time is uncertain.
- **Appendix D. The Story Bank** (generated automatically from the Story boxes).

## Front and back matter (written by the coordinator)
`book/00-why-this-book.md` (preface), `book/95-about-the-author.md`.
