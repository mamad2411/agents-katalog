---
name: tufte-graphical-competence
description: "Use when diagnosing why a team, publication, or product keeps shipping weak or dishonest data graphics; when chart production is owned by art, brand, or marketing alone; when a brief claims the audience won't understand, statistics are boring, or 'if you have to explain it, don't use it'; when auditing what share of a report's displays are relational; or when deciding who must review a data display before it ships."
tags: [tufte, graphical-competence, organizational-causes, integrity, relational-graphics, audience, review-process]
---
# Graphical Competence: Why Organizations Produce Bad Graphics

## Overview
Every other skill in this pack fixes a display; this one fixes the shop that made it. Tufte's diagnosis in VDQI Chapter 3 ("Sources of Graphical Integrity and Sophistication," pp. 79–87) is that lying and inept graphics are not primarily technical accidents — bias and stereotyping account for some distortions, but the primary causes are the prevailing skills, attitudes, and organizational structure of the people who design and edit statistical graphics (p. 79). Two working doctrines — *statistics are boring* and *graphics are for the unsophisticated* — hand control of data displays to a single expertise (the artistic), and the predictable products are graphics that lie, that use only the simplest designs, and that miss the real news in the data (p. 87). The remedy is structural: graphical competence demands three different skills at once, and the substantive and statistical two must actually participate.

Boundaries with siblings: the *mechanics* of graphical lies (Lie Factor, design variation, the six integrity principles of p. 77) live in **`tufte-graphical-integrity`**; single-artifact corruption detection lives in **`tufte-evidence-corruption`** (whose cross-book note defers to this chapter for the causal account); the institutional critique of slideware is **`tufte-cognitive-style`**. This skill carries the organizational diagnosis, the sophistication metric, and the staffing remedy.

## §1. The Diagnosis — Three Organizational Causes (pp. 79–81)

**1. Lack of quantitative skills among professional artists (p. 79).** What lurks behind the inept graphic, in Tufte's diagnosis, is missing judgment about quantitative evidence. Nearly all who produce graphics for mass publication trained exclusively in the fine arts, with little experience analyzing data — and even graphical-design textbooks are silent on how to think about numbers. The trade vocabulary ("creative," "concept," "style" in every permutation) is Big Think jargon for the small task of drawing a time-series a few data points long, and advancement goes to those who beautify data, never mind statistical integrity. Tufte's footnote sharpens the historical point: Playfair's original work did not contain the errors now routine, and evidence gathered by the American Statistical Association's graphics committee showed formal training in graphic presentation in marked decline (p. 79, fn. 1, citing Wainer) — the incompetence is a regression, not a baseline.

**2. The doctrine that statistical data are boring (pp. 79–80).** Exhibits: *Time*'s first full-time chart specialist describing the challenge as presenting statistics as a visual idea rather than a tedious parade of numbers; a design handbook opening its statistical-charts chapter with "Why are statistics so boring?" The doctrine's real function is political — it serves bureaucratic struggles over a publication's resources. If the numbers are dull, then an artist, indeed an Art Department and an Art Director, are required to animate them; the doctrine thereby moves data graphics under the control of artists rather than of the people who write the words and know the substance. As the art bureaucracy grows, style replaces content — and the word people, having lost the space, console themselves that statistics really are tedious (p. 80).

> "If the statistics are boring, then you've got the wrong numbers." — Tufte, *VDQI*, p. 80

Finding the right numbers takes as much specialized skill — statistical skill — and hard work as producing a beautiful design or covering a complex story (p. 80). Boredom is a sourcing failure, not a decoration deficit.

*Historical cost of the doctrines (p. 53).* Tufte dates the damage: the assumption that graphics were mainly devices for showing the obvious to the ignorant governed the graphically barren years from 1930 to 1970, sending the field down two fruitless paths — overdecorating charts so the supposed dullards would stay awake, and treating lie-detection as the field's main analytic task. It ended only when Tukey's work in the late 1960s made graphics respectable as instruments for reasoning about quantitative information. The doctrines this chapter names are not harmless attitudes; they stalled a discipline for four decades.

**3. The doctrine that graphics are only for the unsophisticated reader (pp. 80–81).** Exhibits: *Consumer Reports* producing the first test issue of its children's magazine with a sugar article longer on graphics than on information, for fear children might be overwhelmed by too many facts; an art director responsible for ~3,000 graphics a year (some 2.5 billion printed images) explaining that graphics exist to lure the reader's attention away from the advertising rather than to explain the news; a network TV news director's rule, "If you have to explain it, don't use it" (p. 81) — a line of thinking that terminates in the company-cafeteria pictograph Mary Eleanor Spear had already catalogued in 1952 as an unnecessary chart.

## §2. The Consequences (pp. 76–77, 81)

Tufte holds graphics to E. B. White's standard for prose — no one can write decently who distrusts the reader's intelligence or whose attitude is patronizing (p. 81). Contempt for the audience combined with quantitative unskill has deadly consequences: over-decorated and simplistic designs, tiny data sets, and big lies (p. 81).

- **Lies scale with circulation (p. 76).** A lying chart in a major paper lies 900,000 times over; on television, tens of millions — and the lies concentrate on the major public-policy issues (budgets, medical care, prices, fuel standards). The lies run systematic and predictable, nearly always overstating how fast things have recently changed.
- **Defense 1, demolished — "at least it shows the general direction" (p. 76).** Fifteenfold lies are too large to be called approximately correct, and numbers have magnitude as well as order. Getting only the direction right is the philosophy of what Tufte names the **Pravda School of Ordinal Graphics**: every chart has a crystal-clear direction coupled with fantasy magnitudes (illustrated by *Pravda*'s own industrial-output chart, May 24, 1982).
- **Defense 2, demolished — "the real numbers are printed on it" (p. 77).** Printing correct values on a lying design amounts to claiming that honesty in one spot licenses a fifteenfold lie everywhere else — a standard of integrity no writer would be allowed, and one designers should not be allowed either.
- **The censorship effect (p. 81).** The constraints operate like censorship, yielding elliptical, eccentric communication: illustrators who cannot handle a scatterplot force bivariate data into convoluted univariate designs — Tufte shows two 1980 specimens (an OECD tax-vs-growth display and a poll graphic) contorting two-variable questions into decorated bar arrangements.

## §3. Measuring Sophistication — the Relational-Graphic Metric (pp. 82–83)

Tufte operationalizes "graphical sophistication" as a measurable property of any publication or body of work:

**Sophistication share = the fraction of a publication's statistical graphics that are *relational* — linking two or more variables while being neither a time-series nor a map (p. 82).**

Relational designs matter because they are the graphics of analysis: they confront statements about cause and effect with evidence, showing how one variable affects another (p. 82). The form is neither new nor hard — in use since 1765, printed billions of times a year, and demonstrably understood by twelve-year-olds (p. 82).

The 1974–1980 survey (~4,000 sampled graphics across 15 news publications, representing an estimated 250–300 billion printed images):

| Publication | Relational share | Sample |
|---|---|---|
| *Akahata* (Japan, circulation 30,000) | 9.3% | 202 |
| *Asahi Shimbun* (Japan, 8,000,000) | 7.6% | 119 |
| *Der Spiegel* (Germany) | 5.7% | 454 |
| *The Economist* (Britain) | 2.0% | 342 |
| *Nihon Keizai Shimbun* (Japan) | 1.7% | 297 |
| *Le Monde* (France) | 0.7% | 144 |
| *Business Week* (U.S.) | 0.6% | 726 |
| *New York Times* (U.S.) | 0.5% | 422 |
| *Pravda*, *Frankfurter Allgemeine*, *The Times*, *Washington Post*, *Time*, *Die Zeit*, *Wall Street Journal* | 0.0% | 54–449 each |

Reference points: a random sample of 220 graphics from *Science* (1978–1980) ran 42% relational (p. 83); seven of the fifteen papers — *Pravda* through the *Wall Street Journal* — produced not one relational graphic in the sample, usually limiting themselves to time-series (p. 83). The metric's power is its bluntness: it cannot be argued with by pointing at production polish, and it transfers directly to a modern dashboard, annual report, or analytics product — count the displays that relate two variables versus those that decorate one.

## §4. The Audience Can Handle It (pp. 84–86)

The unsophisticated-reader doctrine fails on evidence from three directions:

1. **Children.** Japan treats statistics as a collective passion — a national Statistics Day, statistical conventions, and graph-drawing contests with ~30,000 entries; the year Tufte cites, first prize went to five 7-year-olds for "Mom, play with us more often," a graph of a 32-classmate survey, and the children's entry Tufte flags as relational correlated the day's temperature with cicada singing (p. 84).
2. **Textbooks and tests.** College texts run far ahead of newspapers — 82% relational in medicine and public-health articles, 68% in an introductory psychology text, 66% in Pauling's chemistry; high-school chemistry hits 77% (Table 2, p. 85). Standardized tests assume the skill: Japanese university entrance exams ran 100% relational, U.S. science tests 67% (Table 3, p. 86). Grade-school children may thus experience a greater density of relational graphics than a reader of the major U.S. dailies and weeklies (p. 84) — which is what licenses Tufte's verdict that most news publications outside Japan operate at a *pre-adult* level of intelligence in graphical design (p. 84).
3. **The actual readership.** About 80% of the Sunday *New York Times*' 1.5 million readers attended college; the audience for statistical graphics, the footnote concludes, is smarter than many illustrators assume (p. 84, fn. 12).

Tufte restates the calibration rule when defending his own novel designs against the "readers will be confused" objection: it is a frequent mistake to underestimate the audience — assume that if you understand a design, most other readers will too (p. 136).

> "Graphics should be as intelligent and sophisticated as the accompanying text." — Tufte, *VDQI*, p. 136

## §5. The Double Standard (pp. 77, 86)

Two double standards run in parallel at the same publications:

| Standard | Words get | Graphics get |
|---|---|---|
| Integrity (p. 77) | Writers may not lie anywhere | A design may lie fifteenfold so long as correct numbers appear in fine print |
| Sophistication (p. 86) | Serious, sometimes expert-demanding prose | The simplest, stupidest designs |

Tufte proves the sophistication gap from a single issue of the *New York Times*: prose confidently discussing petrodollar recycling and floating exchange rates, square-toed instrumental phrasing and continuo improvisation, sovereign immunity and retroactive damages, and a drug described as "dysphorogenic" — beside statistical graphics of pre-adult simplicity (p. 86). A publication that trusts its readers with that prose has no case for distrusting them with a scatterplot. The two-tier standard is diagnostic: wherever an organization's words are edited by experts and its charts by nobody quantitative, this chapter's three causes are operating.

## §6. The Remedy — Three Skills, Jointly in Control (p. 87)

The production conditions — illustrators without substantive or quantitative skills, dislike of quantitative evidence, contempt for the audience's intelligence — guarantee graphic mediocrity, breeding graphics that (1) lie; (2) stick to the simplest designs, typically unstandardized time-series of a few data points; and (3) miss the real news sitting in the data (p. 87). Using graphics merely to decorate a few numbers squanders their communicative power at exactly the moment more of the world is observed and assessed quantitatively (p. 87).

The remedy has two parts:

**Reject the doctrines.** Both blame the victims — the audience and the data — rather than the perpetrators (p. 87). Any brief containing "our users won't understand," "make the numbers exciting," or "if you have to explain it, don't use it" is restating them.

> "Graphical competence demands three quite different skills: the substantive, statistical, and artistic." — Tufte, *VDQI*, p. 87

**Restructure control.** Most graphical work sits under a single expertise — the artistic. Tufte's analogy: putting artist-illustrators in charge of a statistical graphic's design and content is roughly like putting typographers in charge of the content, style, and editing of prose (p. 87). Integrity and sophistication arrive only when substantive and quantitative expertise take a genuine part in the design.

| Skill | What it contributes | What ships when it is absent |
|---|---|---|
| Substantive | Knows what the data mean, what the real news is, which comparisons matter | Polished displays that miss the story; wrong numbers confidently shown |
| Statistical | Judges evidence quality, standardization, context, magnitude vs direction | Ordinal lies, unadjusted units, cherry-picked windows, tiny data sets |
| Artistic | Craft: proportion, line, type, layering, production | Correct but graceless, unread displays |

**Applied to a modern team:** every data display gets a reviewer who knows the subject and a reviewer who knows the statistics — not only a brand or visual-design review; chart style guides encode integrity and evidence rules, not just palettes; the relational-share metric (§3) becomes an auditable KPI for a product's dashboards or a report series; and "the audience won't get it" claims are tested against what the same audience's textbooks, tests, and prose already assume of them (§4–§5).

## §7. Do / Don't

| Do | Don't |
|---|---|
| Locate the cause of chronic bad graphics in skills, doctrine, and org structure | Treat each bad chart as an isolated craft slip |
| Staff or review every data display with substantive + statistical + artistic skill | Leave design and content of graphics to a single (artistic) expertise |
| Answer "boring data" complaints by finding the right numbers | Answer them with animation, decoration, or mascots |
| Calibrate audience capability against their textbooks, tests, and the prose beside the chart | Design down to an imagined unsophisticated reader |
| Hold graphics to the same integrity standard as the publication's words | Accept a lying design because the true values are printed on it |
| Count your product's relational displays and grow the share | Ship only time-series and decorated single numbers |
| Show magnitude and direction | Settle for crystal-clear direction with fantasy magnitudes |
| Name doctrine when you hear it ("statistics are boring," "don't explain") | Let doctrine pass as audience empathy |

## §8. Named Failure Modes

**FM1 — The Pravda School of Ordinal Graphics.** Defending a distorted display because the general direction is right. Numbers have magnitude as well as order; fifteenfold exaggeration is not "approximately correct." *Fix:* proportional representation, audited via `tufte-graphical-integrity` (p. 76).

**FM2 — The fine-print defense.** A lying visual design excused because accurate values are printed on it. Not lying in one place does not justify lying elsewhere (p. 77). *Fix:* the design itself must be proportional; labels defeat ambiguity, not culpability.

**FM3 — Art-department capture.** Data displays routed exclusively through art/brand/marketing, with no substantive or statistical voice in content decisions; style replaces content as the bureaucracy grows (p. 80). *Fix:* three-skill review gate (§6).

**FM4 — The boring-data doctrine.** Decorating weak numbers instead of doing the statistical work of finding strong ones (p. 80). *Fix:* treat boredom as a sourcing bug; change the numbers, not the ornament.

**FM5 — Audience contempt.** "If you have to explain it, don't use it" — designing below the audience's demonstrated level, producing unnecessary charts of single facts (p. 81). *Fix:* calibrate against §4's evidence; respect earns attention.

**FM6 — Univariate retreat.** Avoiding relational designs out of illustrator limitation, contorting two-variable questions into decorated one-variable bars (p. 81). *Fix:* when the question is "does X affect Y," the display links X and Y; see `tufte-causal-reasoning-in-graphics`.

**FM7 — Victim blaming.** Explaining graphical failure by the dullness of the data or the dimness of the audience rather than the skills and structure of the producers (p. 87). *Fix:* audit the perpetrators — the production process — first.

## §9. Application Checklist

| Check | Pass condition |
|---|---|
| Cause located | Chronic bad output traced to skills / doctrine / structure, not blamed on data or audience |
| Three skills present | Substantive, statistical, and artistic expertise all touch the display before it ships |
| Review gate | Someone quantitative can block a chart, not merely restyle it |
| Integrity parity | Charts held to the same lying standard as the organization's prose |
| Magnitude test | No display passing on direction alone; magnitudes proportional |
| Fine-print test | No design whose honesty depends on reading the printed values |
| Relational share | Fraction of displays linking ≥2 variables counted, benchmarked (news 0.0–9.3%, *Science* 42%), and rising |
| Audience calibration | Complexity ceiling justified by evidence of the audience, not by doctrine |
| Boredom response | "Boring" answered with better numbers, never with decoration |
| Doctrine audit | Briefs and style guides free of unsophisticated-reader and boring-data language |

---

Sources: *The Visual Display of Quantitative Information*, Edward Tufte, 2nd ed. — Chapter 2 conclusion (lie multiplication, the two defenses, the Pravda School), pp. 76–77; Chapter 3, "Sources of Graphical Integrity and Sophistication" (three causes, consequences, relational-sophistication tables for world press / textbooks / tests, the double standard, three-skill remedy), pp. 79–87.
