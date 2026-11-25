---
name: cv-tailor
description: Build a tailored one-page LaTeX CV and matching cover letter from a job description, compile them with tectonic, and verify the PDF the way an ATS parser reads it. Use for any resume, CV, cover letter, LaTeX, or ATS document request. Never fabricates a fact that is not in the facts file.
---

# CV Tailor

Turns a job description into a one-page LaTeX CV and a matching cover letter, compiled and
verified. Every claim traces to `facts.md`.

## Prerequisites

- **`tectonic`** — the LaTeX engine. `brew install tectonic`, or see tectonic-typesetting.github.io.
  It is a single binary with no TeX Live install, and it runs with shell-escape disabled, which
  is why this skill uses it rather than `pdflatex`.
- **`pdftotext`** (poppler) — for the ATS verification pass. `brew install poppler`.
- **`facts.md` and `profile.yml`** in the working directory. Scaffold them from `examples/`
  if missing. Do not proceed without them.

## Load first, every build

1. **The `jd-analyser` output.** Build from its positioning brief, never from your own read of
   the JD. Skipping this is how a trainee role gets mis-built as a specialist role.
2. **`facts.md`**, including its Evidence Index and every caveat in it.
3. **`profile.yml`** for constraints and exclusions.
4. **The `human-voice` skill — load it, every build, before writing a single bullet.** It covers
   CVs as well as prose. Working from memory is the documented failure mode here, not a
   theoretical one.

## Non-negotiables

- **Never fabricate.** Only facts present in `facts.md`. No invented metrics, employers, or dates.
- **Never write a gap-disclosure sentence into the CV or cover letter.** Gaps get tracked
  internally, in the report, for the user's own judgement. They never appear on the page the
  employer reads. When a JD exposes a real gap, the fix is to find a genuine stronger proof
  point, not to write an apologetic paragraph.
- **Never submit.** This skill does not click Apply or Send, ever.
- **One page** unless the user explicitly asks otherwise.
- **No hidden text.** No white text, no zero-opacity layers, no off-page keyword stuffing.
  Current ATS platforms flag this as fraud, and it will end the application.
- **Compile with `tectonic`.** Never `\uppercase` inside `titlesec` — it breaks under tectonic.
  Use `\scshape`.
- **Result over template.** Every bullet needs a real outcome and a real number where `facts.md`
  supports one. What is *not* required is that every bullet wear the same grammar. Applying one
  sentence formula literally across a whole role produces exactly the uniform cadence that reads
  as machine-written. **Within each role, at least one bullet must break the shape.**
- **Keyword placement, not just presence.** The JD's top two or three terms belong in the profile
  line and the first bullet of the most relevant role. ATS scoring weights that placement higher
  than the same keyword buried in the last line of page one.

## Workflow

1. **Quick score first.** `jd-analyser`'s one line — FIT out of 100, band, confidence, reason.
   Wait for a go-ahead before building.
2. **Run `jd-analyser`.** Take its positioning brief as the spec.
3. **Copy the template**, do not start from scratch:
   ```bash
   cp assets/cv-template.tex             cv-<company-slug>.tex
   cp assets/cover-letter-template.tex   cl-<company-slug>.tex
   ```
4. **Fill from `facts.md`.** Mirror the JD's exact wording only where real evidence backs it.
   Mark anything unsupported as a gap in your report to the user; never invent evidence to close one.
5. **Compile:**
   ```bash
   tectonic cv-<company-slug>.tex
   tectonic cl-<company-slug>.tex
   ```
6. **Verify** with the pass below. Never ship a document that fails it.
7. **Report** the document scorecard below: exact filenames, compiler result, every check with
   its number, and any honest gaps. "1 page, 6/6 headings, 0 hidden characters, keyword coverage
   9/10 (90%), 5/8 bullets carry a number" — never "looks good".

## ATS verification pass

An ATS does not see your layout. It sees `pdftotext` output. Verify against that, not against
how the PDF looks.

```bash
PDF=cv-<company-slug>.pdf

# 0. Page count — must be 1
pdfinfo "$PDF" | grep '^Pages:'

# 1. Extraction must not be empty (a CV built from images scores zero)
pdftotext "$PDF" - | wc -w

# 2. Name, email and phone must appear in the first few lines
pdftotext "$PDF" - | head -5

# 3. Standard headings present and in order
pdftotext "$PDF" - | grep -inE '^(education|experience|projects|skills|languages|certifications)'

# 4. Hidden or zero-width characters — must be 0
#    (perl, not grep -P: stock macOS grep has no -P and errors out)
pdftotext "$PDF" - | perl -CS -ne '$n++ if /[\x{200B}-\x{200D}\x{FEFF}\x{00AD}]/; END { print $n+0, "\n" }'

# 4b. Ligature glyphs — must be 0. "ﬁnding" is one glyph to a parser, so a search
#     for "finding" misses it. The bundled templates turn common ligatures off.
pdftotext "$PDF" - | perl -CS -ne '$n++ if /[\x{FB00}-\x{FB06}]/; END { print $n+0, "\n" }'

# 5. Layout vs plain extraction must agree in word count (a big gap means
#    multi-column or table layout the parser will scramble)
A=$(pdftotext "$PDF" - | wc -w); B=$(pdftotext -layout "$PDF" - | wc -w)
echo "plain=$A layout=$B delta=$((A-B))"

# 6. No language claimed above the level recorded in facts.md
pdftotext "$PDF" - | grep -inE '(fluent|bilingual|native|C1|C2|B2)'
```

Then run the `human-voice` Part 2 pre-ship scan on the same PDF.

**Read the matches, never the exit code.** `grep | sort -u` exits 0 on empty input, so chaining
`&& echo FAIL` fires either way. Look at the output.

**Interpreting check 5:** a large delta means the parser is reading your columns as interleaved
text. Tab-aligned dates are fine for text search but can confuse portal autofill widgets that
infer structured fields from layout. If a portal is Workday- or SuccessFactors-shaped, consider
supplying a plain `.docx` alongside the PDF, with dates stacked rather than tab-aligned.

## Keyword coverage — the number an ATS ranks on

Matching engines rank a CV by how many of the posting's terms they can find in the extracted
text, weighting hard skills over soft ones and terms inside dated roles over a bare skills list.
Measure it on the PDF, not the `.tex`.

1. Write `terms.txt`, one term per line: every **hard skill, tool, method and the job title**
   from `jd-analyser`'s scorecard, **using the JD's exact spelling**. Mark each line `B` if
   `facts.md` backs it (credit > 0), `U` if it does not: `B	Power BI`, `U	Amplitude`.
2. Run:

```bash
pdftotext "$PDF" - | tr '\n' ' ' > cv.txt
while IFS=$'\t' read -r tag term; do
  if grep -qiF -- "$term" cv.txt; then echo "HIT   $tag  $term"; else echo "MISS  $tag  $term"; fi
done < terms.txt
```

3. Report two numbers:
   - **Backed coverage** = `B` hits / `B` terms. **Target 80% or more.** Match-rate tools
     recommend 75–80%; callback rates flatten above roughly 90, and chasing 100% produces a CV
     that reads like the posting pasted back.
   - **Raw coverage** = all hits / all terms. Informational only. The gap between the two is
     the honest ceiling — it is the part of the posting this candidate cannot answer.
4. **A `U` term that shows up as a HIT is a fabrication alarm.** Find where it came from and
   remove it, unless it is plainly incidental (the word appearing in a school name).
5. **Placement check:** the JD's top three backed terms should appear in the first 15 extracted
   lines (profile line plus the most relevant role), and at least once inside a dated role, not
   only in the skills block.

```bash
# Per term, not grep -c: -c counts matching LINES, so three terms on one line reads as "1"
pdftotext "$PDF" - | head -15 > top.txt
for t in "<term 1>" "<term 2>" "<term 3>"; do
  if grep -qiF -- "$t" top.txt; then echo "HIT   $t"; else echo "MISS  $t"; fi
done
```

Never add a `U` term to close the gap. The fix for low backed coverage is wording a real bullet
in the JD's own vocabulary. The fix for low raw coverage is a different job.

## Document scorecard — report this, every build

One table, every row a number. This is what the user reads first.

| Check | Result | Pass bar |
|---|---|---|
| Pages | 1 | 1 |
| Extracted words | 540 | > 0 |
| Contact in first 5 lines | yes | yes |
| Headings found, in order | 6/6 | all |
| Hidden / zero-width characters | 0 | 0 |
| Ligature glyphs | 0 | 0 |
| Plain vs layout word delta | 0 | ≈ 0 |
| Language claims above `facts.md` | 0 | 0 |
| **Backed keyword coverage** | 9/10 (90%) | ≥ 80% |
| Raw keyword coverage | 9/13 (69%) | info |
| Top-3 terms in first 15 lines | 3/3 | 3/3 |
| Unbacked terms present | 0 | 0 |
| Bullets carrying a number or named outcome | 5/8 | ≥ half |
| Bullets over two lines | 0 | 0 |
| `human-voice` Part 2 banned terms / em-dashes | 0 / 0 | 0 / 0 |
| Roles where every bullet shares one shape | 0 | 0 |

Then **Writing improvements**: at most three, each tied to a specific bullet, quoting the line and
the replacement. Priority order: (1) a bullet with no outcome where `facts.md` records one;
(2) a backed JD term that is missing or sits only in the skills block — move it into the dated
bullet that proves it; (3) a rhythm fix from `human-voice` Part 2. Never propose a number or a
tool `facts.md` does not hold.

## Design pattern

The bundled template follows the conventions that survive ATS parsing:

- Latin Modern through `fontspec` with common ligatures off, so every word extracts as plain
  letters. Single column, no tables in the body, no text boxes, no headers or footers
- Contact row hyperlinked, but never a bare URL printed as visible text
- Small-caps section headings with a rule underneath, standard heading names
- Dark, mid, and light greys only — colour that survives a black-and-white print
- Tight but not cramped spacing; one page is a constraint, not a target to overflow

Edit the template's variables at the top. Do not restructure the body unless you have a reason
you can state.

## Assets

- `assets/cv-template.tex` — one-page CV skeleton
- `assets/cover-letter-template.tex` — matching cover letter

Both are plain LaTeX source. Read them before running them, as you should with any file that
goes through a typesetter.
