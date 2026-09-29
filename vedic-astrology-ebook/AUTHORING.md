# Authoring guide for *Kundali Made Simple*

This file is the contract every chapter follows. Read it fully before writing.

## The book
**Title:** *Kundali Made Simple — Vedic Astrology from Your First Chart to Your First Consultation*
**Reader:** an absolute beginner who bought classic books and "understood nothing". Smart, curious, no Sanskrit, no prior astrology. Goal: by the last page they can read a chart end-to-end and sit for a paid consultation with confidence and ethics.
**Author voice:** a veteran Indian Jyotishi with 30 years of practice who has seen close to a million kundalis. First person ("I", "in my practice", "a client once came to me..."). Warm, plain-spoken, a little humorous, never pompous. Uses everyday Indian analogies (a king's court, a joint family, a cricket team, a railway timetable, a kitchen). Teaches like a patient uncle, not a textbook. Anecdotes are composites; never claim a real named client.
**Tradition:** Parashari (BPHS) is the backbone. Jaimini, Tajaka and Lal Kitab appear only where marked.

## Non-negotiable rules
1. **Plain English first, Sanskrit second.** Every technical term is introduced as: English meaning, then the Sanskrit in parentheses, e.g. "the rising sign (Lagna)". After introduction, use whichever is shorter. Never assume the reader remembers a term from another chapter—one-line reminders are welcome.
2. **Show, don't just tell.** Every concept gets at least one worked example on a chart. Use the chart tool (below) for diagrams. Aim for 3–6 diagrams per chapter.
3. **Facts must match `book/90-appendix-a-quick-reference.md`.** Degrees, lords, dasha years, friendships, house meanings, functional nature by Lagna, nakshatra lords—copy from there. Do not invent new tables that disagree.
4. **Lal Kitab attribution is strict.** Anything taken from Lal Kitab goes in its own box (format below) and NEVER blends into Parashari text. State the source as *Lal Kitab (Pt. Roop Chand Joshi, Urdu editions 1939–1952; Hindi translations vary)*. If a Lal Kitab point is commonly taught but you are not certain it is in the original text, say "as commonly taught in the Lal Kitab tradition".
5. **Honesty about uncertainty.** Where classical authors disagree (e.g. Rahu/Ketu exaltation, Moolatrikona of Moon, combustion orbs), say so in one line and give the mainstream view.
6. **No fatalism, no fear-selling.** Never write "you will die / divorce / go bankrupt". Teach the reader to phrase results as tendencies and periods, and to give remedies with humility. This is also what makes a consultant trusted.
7. **No real living people's charts.** Case studies use constructed charts (see Case Study Kit below).
8. Chapter length: 3,500–5,500 words. Sections short. Paragraphs 2–5 sentences.

## Recurring boxes (use blockquote + bold label; keep these exact labels)
- `> **🧭 Guruji's rule of thumb:** ...` — a memorable heuristic.
- `> **💡 Did you know?** ...` — an interesting fact (history, astronomy, culture). 1–3 per chapter.
- `> **⚠️ Common beginner mistake:** ...`
- `> **🪔 Consultation tip:** ...` — how to say this to a client, ethics, phrasing.
- `> **📕 From Lal Kitab:** ...` — the ONLY place Lal Kitab material may appear. End the box with "*(Source: Lal Kitab, Pt. Roop Chand Joshi, 1939–1952 Urdu editions; Hindi translations vary.)*"
- `> **📖 Story:** ...` — a MEMORY STORY (see "Stories and colour coding" below). Give each story a short bold title after the label, e.g. `> **📖 Story: The two courts.** ...`
- `> **✍️ Practice:** ...` — exercises at chapter end (3–5 items), with answers in a collapsible `<details><summary>Answers</summary> ... </details>` block.

Every chapter ends with:
1. `## In one breath` — a 5–8 bullet summary.
2. `## Practice` — exercises with answers.

## Stories and colour coding (reader's explicit request)
The reader learns hard, list-like material ONLY through stories and colour. So:
1. **Every concept that is normally memorised gets a story.** Planetary friendships and enmities, which conjunctions are helpful or harmful, functional benefics by Lagna, house meanings, aspect patterns, exaltation/debilitation signs, nakshatra lords, dasha order, yoga conditions, Lal Kitab pakka ghar, remedy rules. Tell it as a short vivid tale (60–200 words) in a `> **📖 Story:** ...` box — a king's court, a joint family, a village, a cricket team, a railway station — where the characters' behaviour *explains* the rule (why Venus and the Sun cannot be friends: the pleasure-minister and the king who demands discipline; why Saturn and Mars fight: the slow judge and the hot-headed commander; why Mercury turns against the Moon but the Moon does not hate Mercury: the son who resents the mother, the mother who still loves the son — the Tara/Budha myth). Aim for 3–6 Story boxes per chapter; more in chapters 3, 6, 8, 10, 13, 22.
2. **Recurring characters.** Use the same cast across the book: Sun = the King (Raja), Moon = the Queen Mother (Rani Ma), Mars = the Commander (Senapati), Mercury = the clever young Prince/Secretary (Rajkumar), Jupiter = the Royal Priest and Minister (Guru-ji), Venus = the Minister of Arts and Pleasure (Shukracharya), Saturn = the old Judge of Labour / the Servant who became a judge (Shani-ji), Rahu = the Smoke-headed Stranger at the gate, Ketu = the Headless Sadhu. The two "parties" at court: the Royal Party (Sun, Moon, Mars, Jupiter) and the People's Party (Mercury, Venus, Saturn). Houses are the rooms of a haveli; signs are the twelve districts of the kingdom; nakshatras are the streets; dashas are the railway timetable.
3. **Colour code everything judgemental.** In every table that says good/bad/neutral use the emoji dots — 🟢 benefic/friend/good, 🔴 malefic/enemy/difficult, 🟡 neutral/mixed — in the cell (they render everywhere, including GitHub). In SVGs use the same three: green #15803d / #bbf7d0, red #b91c1c / #fecaca, amber #b45309 / #fde68a. The planet colours in the chart tool are fixed (Sun orange, Moon grey, Mars red, Mercury green, Jupiter gold, Venus pink, Saturn navy, Rahu/Ketu purple) — refer to them in prose ("the navy Saturn").
4. **One picture per story where possible** (a colour-coded SVG table, a two-party court diagram, a friendship web with green/red lines).
5. After a story, state the rule in one plain line: "**Rule:** …". The story explains; the rule is what they will quote at the desk.

## Markdown conventions (the build script depends on these)
- File name: `book/NN-slug.md` (two-digit number). First line: `# Chapter N: Title` (appendices: `# Appendix X: Title`).
- Headings: `##` for sections, `###` for subsections. Never skip levels.
- Images: `![Descriptive alt text](../images/chNN-name.svg)` on its own line, followed by an italic caption line `*Figure N.x: caption*`.
- Tables: GitHub-flavoured markdown tables.
- Use the planet codes Su Mo Ma Me Ju Ve Sa Ra Ke in diagrams; spell names in prose.

## The chart tool
`python3 tools/kundali_svg.py <kind> ... --out images/chNN-name.svg` (run from the `vedic-astrology-ebook/` folder).

| kind | what it draws | key options |
|---|---|---|
| `north` | North Indian chart | `--lagna 5 --planets "1:Su,Me;4:Ju;7:Sa(R)" --highlight 1,5,9 --title --caption --sign-names` |
| `south` | South Indian chart (same input, converted) | same as north |
| `lalkitab` | Lal Kitab fixed-house chart | `--planets "1:Su;2:Ju"` |
| `aspect` | highlight houses aspected by a planet from a house | `--planet Sa --house 1` |
| `zodiac` | the 12-sign wheel with lords/elements | `--title --caption` |
| `nakshatra` | 27-nakshatra wheel with lords | |
| `dasha` | Vimshottari 120-year bar | `--start-lord Ketu` |
| `housegroups` | Kendra/Trikona/Dusthana/Upachaya | |
| `sadesati` | Saturn over natal Moon | |

Planets are given by **house** (1–12), the tool converts to signs from `--lagna` (1 Aries … 12 Pisces). `(R)` marks retrograde. Charts must be astronomically plausible: Mercury within one sign of the Sun (max ~28°), Venus within two signs (max ~48°), Rahu and Ketu always exactly opposite (7 houses apart).

## Case Study Kit (shared constructed charts — use these so chapters agree)
**Chart A — "Meera", born 12 Dec 1988, 06:40, Jaipur (constructed).** Lagna Scorpio 12°. Sun Scorpio (H1) 28°; Mercury Scorpio (H1) 9°; Venus Libra (H12) 22°; Mars Pisces (H5) 4° retrograde; Jupiter Taurus (H7) 8° retrograde; Saturn Sagittarius (H2) 5°; Rahu Aquarius (H4) 16°; Ketu Leo (H10) 16°; Moon Cancer (H9) 21° (Ashlesha nakshatra, Mercury's star). Themes: strong Lagna (Sun+Mercury), Jupiter in 7th, Moon exalted-ish in own sign in 9th; Mercury Mahadasha at birth with balance ~11½ years (Moon at 21° Cancer: (30−21)/13°20′ × 17 = 11.5 yrs), then Ketu 7 (age 11.5–18.5), Venus 20 (18.5–38.5), Sun 6 (38.5–44.5); career in teaching/consulting; marriage 2016 (Venus MD); Sade Sati roughly 2000–2007 (Saturn through Gemini, Cancer, Leo — the 12th, 1st, 2nd from her Cancer Moon); Ashtama Shani 2023–2025 (Saturn in Aquarius, 8th from Moon).
   Tool string: `--lagna 8 --planets "1:Su,Me;12:Ve;5:Ma(R);7:Ju(R);2:Sa;4:Ra;10:Ke;9:Mo"`
**Chart B — "Arjun", born 3 Mar 1995, 20:15, Pune (constructed).** Lagna Cancer 19°. Sun Aquarius (H8) 18°; Moon Taurus (H11) 6° (Krittika pada 3, Sun's star); Mars Leo (H2) 21° retrograde; Mercury Aquarius (H8) 2°; Jupiter Scorpio (H5) 22°; Venus Capricorn (H7) 24°; Saturn Aquarius (H8) 25°; Rahu Libra (H4) 12°; Ketu Aries (H10) 12°. Themes: Cancer lagna, Mars yogakaraka in 2nd, three planets in 8th (research/insurance/occult), Jupiter in 5th trikona, Venus (4th & 11th lord) in the 7th while the 7th lord Saturn sits combust in the 8th in its own sign Aquarius, Ketu in 10th. Balance of Sun dasha at birth ≈ 1.8 years ((10°−6°)/13°20′ × 6), then Moon 10 (age 1.8–11.8), Mars 7 (11.8–18.8), Rahu 18 (18.8–36.8), Jupiter 16 (36.8–52.8).
   Tool string: `--lagna 4 --planets "8:Su,Me,Sa;11:Mo;2:Ma(R);5:Ju;7:Ve;4:Ra;10:Ke"`
**Chart C — "Devika", born 22 Jul 1979, 23:55, Kolkata (constructed).** Lagna Aries 7°. Sun Cancer (H4) 5°; Moon Sagittarius (H9) 14° (Purva Ashadha, Venus's star); Mars Gemini (H3) 27°; Mercury Leo (H5) 1°; Jupiter Cancer (H4) 26°; Venus Gemini (H3) 15°; Saturn Leo (H5) 18°; Rahu Leo (H5) 3°; Ketu Aquarius (H11) 3°. Themes: Aries lagna, exalted Jupiter in 4th with Sun, Moon in 9th, Saturn+Rahu+Mercury in 5th (children/education struggles then success), Mars 3rd. Balance of Venus dasha at birth ≈ 19 years ((26°40′−14°)/13°20′ × 20), then Sun 6 (age 19–25), Moon 10 (25–35), Mars 7 (35–42), Rahu 18 (42–60), Jupiter 16 (60–76).
   Tool string: `--lagna 1 --planets "4:Su,Ju;9:Mo;3:Ma,Ve;5:Me,Sa,Ra;11:Ke"`
Chapters may add small illustrative charts of their own, but the full case studies in Chapter 25 use A, B, C.

## Tone samples
Good: "Think of the Lagna as the front door of the house. Whatever walks in must pass it. A strong front door and even a modest house feels safe."
Bad: "The Lagna, or Udaya Lagna, is the ecliptic degree rising on the eastern horizon at the epoch of nativity."
