# SD (Super Deformed) — curation hints

Unlike every other Gunpla grade, SD is not one line — it's an umbrella over
several **independently numbered sub-brands**, the same shape as HG's
HGUC/HGCE split (see [`../CLAUDE.md`](../CLAUDE.md)). Six are populated so
far, each its own nested collection:

```
sd/
  CLAUDE.md
  _collection.yaml
  bb-senshi/                    # BB Senshi — 1987–present, 422 kits
  cross-silhouette/             # SDCS — 2018–present, 17 kits
  g-generation/                 # SDGG — 1999–2002, 19 kits
  ex-standard/                  # SDEX — 2016–present, 3 kits
  sangokuden/                   # SDBBW — 2010–2013, 3 kits
  world-sangoku-soketsuden/     # SDSS — 2019–2021, 3 kits
```

Every sub-line is flat internally (one file per kit, no further nesting)
and follows MG/RG/EG/PG's established conventions: `<slugified-name>.yaml`
filenames (no number prefix — coverage varies per sub-line but no
sub-line hits 100%, see each one's numbers below), no `variants`
sub-entities (recolors/reissues are full items, same reasoning as
[`../rg/CLAUDE.md`](../rg/CLAUDE.md)), `attributes.scale: Non-scale`
throughout (SD is chibi/non-scale by definition — confirmed no exceptions
across all six sub-lines).

**Two unrelated Three Kingdoms-themed sub-lines exist — don't conflate
them.** `sangokuden/` (SDBBW, "Sangokuden Brave Battle Warriors", 2010) and
`world-sangoku-soketsuden/` (SDSS, "World Sangoku Soketsuden", 2019) share
a theme and even character overlap (both have a Liu Bei/Ryubi-themed kit)
but are separate product lines with separate numbering, nearly a decade
apart. Confirm which category (`Category:SD Gundam Sangokuden Brave
Battle Warriors` vs `Category:SD Gundam World Sangoku Soketsuden`) a kit
belongs to — don't guess from the Three Kingdoms character name alone.

## Sourcing: same MediaWiki API method, verify category vs. redirects vs.
## "Variants" cross-references per sub-line — no single source is reliable alone

Same [Gunpla Wiki](https://gunpla.fandom.com/) API method as every other
grade (see [`../rg/CLAUDE.md`](../rg/CLAUDE.md), [`../eg/CLAUDE.md`](../eg/CLAUDE.md),
[`../pg/CLAUDE.md`](../pg/CLAUDE.md)) — but this project has now hit three
different failure modes across five grades, and SD hit two of them at
once:

- A `Category:` page can be incomplete (EG's problem) — confirmed again
  here: `Category:SD Gundam BB Senshi` only had 55 of BB Senshi's ~95
  real English-documented pages tagged. **Cross-check with
  `action=query&list=allpages&apprefix=<name>` and resolve every result
  with `redirects=1`** before trusting a category count.
- A line's lineup gallery/list page can reference kits that don't exist
  under that grade at all (PG's problem) — not hit again here, but keep
  checking.
- **New this round**: sub-line categories can each be individually small
  and clean (SDCS/SDGG/SDEX/SDBBW/SDSS all matched their category counts
  exactly, no redirects or gallery surprises) — small, recent, single-era
  lines don't have the decades of page churn that produce the other two
  failure modes. Don't assume a small sub-line needs the same
  multi-source cross-referencing rigor as BB Senshi; checking the
  category count against the confirmed image/date coverage per kit was
  sufficient here.

## BB Senshi: a genuinely different scale of project — 412 numbered kits,
## only ~48 documented in English

BB Senshi is Bandai's oldest and longest-running Gunpla sub-line (1987–
present) and its wiki coverage is a small fraction of the real catalog —
Gunpla Wiki documents roughly 48 of 412 numbered kits in English with
images. This is not a gap of the same kind as RG's undated kits or EG's
missing dates; it required a genuinely different sourcing approach.

**The complete, gap-free official numbering (1–412, zero missing) came
from a Japanese fan-maintained checklist, not the English wiki**:
`https://www.katch.ne.jp/~yk-ts/sd-gundam-list/sd_gundam_bb_senshi_list.html`
(Shift_JIS encoded — decode with `errors='replace'` if `iconv` chokes on
stray bytes partway through). It gives, per catalog number, the kanji
name, a katakana pronunciation guide in parentheses when the name isn't
plain loanword katakana already, price, and release date (year stated
once then carried forward via month-only entries in later rows — track a
running "current year" variable while parsing). **The page mixes multiple
numbered lists in one HTML document** (the main 1–412 catalog, then
separate un-related numbered sections for raffle prizes, promotional
items, and other spin-off product numbering that resets back to 1) —
isolate the correct `<B>` section header
("プラモデル　ＳＤガンダムＢＢ戦士シリーズ") before parsing, don't just
regex the whole page. **10 catalog numbers cover two simultaneous
releases each** (a metallic "〜輝羅鋼極彩〜"/Kirakou Gokusai premium
recolor sold alongside the standard release, same number, no separate
date given for the recolor) — real duplicates, not a parsing bug.

**Katakana pronunciation guides are the ground truth for a name's
reading, kanji is not** — e.g. 頑駄無 (a made-up ateji/pun spelling) always
reads as "Gandamu"/"Gundam" throughout this entire line, confirmed by
cross-referencing every wiki-documented kit that includes this kanji
sequence. Prefer the source's own katakana reading over guessing kanji
pronunciation.

**Pure phonetic transliteration (tested: `pykakasi`) is not sufficient for
publication-quality names** — it can't segment invented compound pun-names
into readable multi-word English (e.g. it renders フルアーマーダブルゼータ
ガンダム as one unreadable run-on blob instead of "Full Armor Double Zeta
Gundam"), and even kanji-based segmentation heuristics only partially fix
it. **Translated all 374 non-wiki-documented names using LLM judgment
instead of algorithmic transliteration**, working from the 48
wiki-confirmed number→Japanese→English mappings as a style/convention
reference (dispatched as parallel batches of ~40 kits each, each batch
given the same 48-example style guide). Where a kit is a recognizable
canonical Gundam mobile suit, its standard English Gunpla name was used;
original SD-only characters (Musha/Sengokuden warriors, Sangokuden Three
Kingdoms figures) were translated/transliterated by domain convention
(頑駄無 → "Gundam", 武者 → "Musha", 大将軍 → "Daishougun", romanized not
literally translated, matching wiki precedent).

**Images**: only the 48 wiki-documented kits have one, resolved the same
`imageinfo` way as every other grade. **The remaining 364 have no image
and this is expected, not a gap to close** — most are ¥300–800 toys from
1987–2010s with no findable product photo anywhere online; per-kit image
research for a set this size and age was deliberately not attempted (Will's
call — see the collections audit memory, not fabricating or guessing at
what can't be verified). Revisit only if a comprehensive archival source
turns up (Bandai's own archives, a dedicated vintage-toy photo database),
not via incremental per-kit web search.

**Two names collided across different catalog numbers after translation**
(same English name, different kit, e.g. two separate "Blaze Zaku Phantom"
releases 2 years apart at #285 and #298) — disambiguated with a `(YYYY)`
release-year suffix, matching the convention the wiki's own 48
already use for genuine reissues (e.g. "RX-93 ν Gundam (1988)" vs.
"(2014)"). The 10 same-number Kirakou Gokusai pairs are disambiguated with
"(Kirakou Gokusai Ver.)" instead, since they share both name and release
year.
