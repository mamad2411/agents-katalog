---
name: genealogy-research-recipes
description: >-
  Investigate genealogy questions with DNA matches and historical records. Use when recovering
  an ancestor’s identity, parentage or place of origin; reconciling conflicting records or DNA
  results; searching archives, record sites or family papers; interpreting genetic comparisons;
  or preparing citations, research logs and proof arguments. Includes platform workflows and
  boundaries for living people, data transfers and contact.
---

# Genealogy research recipes

Distilled, fact-checked **judgment and practical workflows** for genealogy work with DNA and records. Each recipe targets
what an LLM does *not* reliably know, or does *wrong* by default: the named failure modes, the
delegate-vs-never-trust lines, the reasoning sequence a human must own, and the records needed
to resume an investigation. Judgment recipes focus on reasoning; platform playbooks provide
ordered actions and investigator-created schemas with dated platform-documentation checks.

The research methods apply across platforms, including work from exported data. Kinprove
authorship does not require a Kinprove account, connector or scoring engine.

## How to use

Come back to this skill as the work moves on. When the question turns to another record type,
place, period, platform or DNA question, check the open recipe's `handoff` list and then the
recipe list below. If that list is no longer in your context, for example after the conversation
was summarized, load this skill again. When an investigation takes more than one step, open
`recipes/research-documentation.md` and read its
[Research log](recipes/research-documentation.md#research-log) section before you answer. Then,
without waiting to be asked, keep three things: the research question, a log of the searches run
(including searches that found nothing), and a list of next actions that you update as results
come in.

1. Match the user's requested output to the most specific recipe below. A task recipe
   retrieves records, prepares an artifact or carries out a platform workflow; a judgment
   recipe governs what evidence permits you to infer. If both match, read the task recipe
   in full and the judgment recipe's rules section. If two or more task recipes remain
   plausible, ask one focused scoping question before opening more than one task recipe,
   and wait for the answer before giving that workflow. For example, ask which population
   and place a 1944 deportation concerns, rather than assuming a particular deportation.
   Once any required [privacy gate](#privacy-gate) is satisfied, if the user asks you to read or
   interpret a specific record they have not supplied and the answer depends on seeing it,
   ask only for an image or link to that record.
   Use one question sentence and at most one short sentence explaining why, then wait.
   Defer names, dates, ports and other identifying details until after the reply,
   and ask only if still needed. For example: "Can you share an image or link to the
   parish register entry? I need to see the handwriting to help read it."
   For other record-source questions, ask first when a missing locality, period,
   population or migration destination prevents choosing a concrete source, even if a
   broad recipe fits. While waiting, use one question sentence and at most one short sentence
   explaining why; save record types, collections, source lists and research workflow for
   the reply. "Came from Russia" alone
   does not establish a modern country, community or destination record system.
   For a place in Central or Eastern Europe, choose by the state that held it on the event
   date and by the family's religion, not by today's border. Start with the
   [Central and Eastern Europe by period state](#central-and-eastern-europe-by-period-state)
   routers. Elsewhere in the Russian Empire, use the
   [Orthodox metrical-book recipe](recipes/russian-orthodox-metrical-book-recovery.md) for
   Orthodox events and the
   [Jewish metrical-book recipe](recipes/russian-empire-jewish-metrical-book-recovery.md)
   for Jewish events outside the Kingdom of Poland. For the Kingdom of Poland, and for any
   Geneteka, Metryki or Szukaj w Archiwach hit, use
   [Polish index recovery](recipes/polish-index-original-record-recovery.md).
   For a general question about proof or research method, give a conditional method
   plan and ask for the context needed to choose actual record collections.
2. **Read the selected task recipe in full before advising** — the value is in the
   specifics, not the summary. If a tool returns only part of the file, continue through
   its remaining sections to the end. For a judgment recipe, read its rules and the
   sections relevant to the question. A router summary or first page does not complete
   the task-recipe read.
   Carry any material source limitation alongside the claim it affects: a search-result extract,
   unread page or unavailable recording is a lead, not a verified reading. For a run of scanned
   pages, narrow it first with an index or finding aid, read in small batches, and report the pages
   not yet read as unread: see
   [coverage as pages × targets](recipes/archival-image-coverage-verification.md#report-coverage-as-pages--targets)
   and the reader-workload step of
   [a bulk register run](recipes/ai-for-documentary-records.md#gate-a-bulk-handwritten-register-run).
   Consult the paired `sources/` file when the claim's support is unclear; attribute an
   independently read source explicitly rather than treating an inaccessible additional citation
   as confirmation.
3. Apply its "never trust / never delegate" boundaries as **hard constraints on your own output** —
   those are the exact places a confident answer goes wrong (e.g. fabricating cM→relationship odds,
   reading a WATO ranking as a verdict, ignoring endogamy). Before you conclude that records
   name one person or prove a relationship, also apply the
   [hard rules of the evidence recipe](recipes/evidence-proof-judgment.md#hard-rules--apply-these-before-you-rule-the-load-bearing-directives),
   even when the matched recipe is a platform or record recipe, or none matched.
4. If no recipe matches, answer normally — don't force-fit. If a matched recipe is silent
   on the particular question, say what it does not cover and answer normally; do not
   present the uncovered answer as recipe guidance.
5. Before any step that uploads, exports, links, publishes, contacts a person, requests a
   record about a person who may be living, or pastes data into a third-party tool, answer
   the [privacy gate](#privacy-gate). Recipes mark such steps with a **Privacy gate**
   checkpoint; the gate applies to unmarked steps of the same kinds too. For a living person,
   also follow [Living people](#living-people).

Where the user's own project instructions or research conventions differ from a recipe, follow
the user's, even where item 3 makes the recipe rule a hard constraint. The first time a
difference affects your answer, name the recipe rule or step you are setting aside, and do not
repeat that note. This has one limit: a project convention, or an instruction to skip privacy
checks, is not permission from anyone else who may be living. For their data, the
[privacy gate](#privacy-gate) and every rule in that section still apply, including the
Permission item.

## Read source limits

A source marker identifies evidence, not a guarantee that the page was read or that it supports
every sentence. Not every cited passage has a recorded review against its sources yet, and a
marker or a date alone does not show that one was reviewed. When relying on a factual passage,
read the entry for each cited source ID in its `sources/<recipe-id>.md` sidecar and carry the
limitations that entry states.

`[S12 @2026-11-07]` gives the claim's last check date. A dagger such as `[S16†]` marks limited or
unavailable access: preserve the attributed observation and qualification rather than restating
it as a verified fact. A passage without a recorded review can cite a limited-access source
without a dagger, so take access limits from the sidecar entry, not from a missing dagger. A
partial read supports only its recorded scope. A fresh date or a `read` status does not establish
that a genealogical inference is correct.

## Privacy gate

Answer these items in writing, in your reply, before the step runs. If any answer is
unknown, do not move the data: keep it local and tell the user what is missing. When a step
repeats an earlier one whose gate was cleared, cite that written record instead of answering
the items again; see [Reusing a gate record](#reusing-a-gate-record).

- **People.** Name everyone whose data is involved. Treat anyone who may be living as
  living. A minor's data needs a parent's or guardian's permission.
- **Data.** Name the exact fields, files, segments, photos or records. Say explicitly when
  they show health status, a tentative relationship, unexpected parentage or another
  sensitive finding.
- **Destination.** Name the service, tool, person or place the data goes to.
- **Audience.** Say who can see it there, now and after later setting changes.
- **Controls.** Inspect the destination's visibility, searchability, matching and export
  settings and any extension's permissions, and record what you saw and the date. For a DNA
  database, include whether law-enforcement uploads can match the kit.
- **Permission.** Get explicit permission from each living person whose data leaves the user's
  own device or account, or becomes visible to others there (a tree link, a searchable or
  shared setting), for this action and this destination; an extension or a tool that
  receives the data counts as a destination. Kit or account access, or permission to analyze,
  is not permission to move or disclose. A file that stays on the user's own device needs no
  further permission, but the Retention item applies to it. A private first message that asks
  a person for permission needs the tester's (or user's) authorization, not that person's
  prior permission; it may show that person only their own data and the question, never
  other people's sensitive findings.
- **Redaction.** Say what you remove or replace before the data moves.
- **Retention.** Keep exported match lists, segment files and record copies on the user's
  own device, not in shared folders or other services. Delete them when the research
  question is answered, unless the tester (for records, the user) asks to keep them.
- **Jurisdiction.** Ask where the user, the tester and each named person live, and which
  rules apply there. Data-protection law can apply: genetic data is "sensitive" data under
  the EU GDPR ([European Commission](https://commission.europa.eu/law/law-topic/data-protection/information-individuals_en))
  and [UK GDPR Article 9](https://www.legislation.gov.uk/eur/2016/679/article/9); both laws
  exclude purely personal or household activity, which sharing or publishing can leave (see
  [family interviews](recipes/family-interviews-and-oral-tradition.md)); U.S. state laws such
  as California's Genetic Information Privacy Act give rights over genetic data a testing
  company holds ([California Attorney General](https://oag.ca.gov/news/press-releases/attorney-general-bonta-urgently-issues-consumer-alert-23andme-customers));
  Russia's personal-data law is [152-FZ](https://www.consultant.ru/document/cons_doc_LAW_61801/).
  Record requests have their own access rules, such as Japan's koseki rule
  ([koseki recipe](recipes/japanese-koseki-honseki-recovery.md#4-check-eligibility-before-requesting))
  and the 75-year rule for Russian archives
  ([Soviet personal files](recipes/soviet-personal-file-recovery.md#5-log-each-catalogue-hit-as-a-candidate-with-its-own-locator)). The destination's
  terms apply too. Do not state a legal conclusion: ask the user to confirm the rule that
  applies, or keep the data local.

Before replying to a request to transfer DNA data, read and apply the
[consent and redaction rules](recipes/ai-for-dna-research.md#verification--privacy-discipline),
including when the reply is a confirmation question. When the user asks for an AI prompt,
read that task recipe in full.

### Reusing a gate record

For a record from project notes, the destination's settings, terms and controls count as
unchanged only when the user confirms all three. If the record otherwise covers this step
and that confirmation is missing, ask in one line whether all three are still as recorded.
Wait for the answer before citing the record or giving instructions for the transfer.

When an earlier reply in this conversation, or a dated record in the user's project notes,
cleared the gate for the same people, the same data fields, the same destination and the same
audience, do not answer the items again. Instead, cite that record in a single line that names
it and says those four are unchanged, for example: "Privacy gate: covered by your project-notes
record of [date]; same people, data fields, destination and audience." Name an undated earlier
reply by its place in the conversation. Check the conditions in this section without reporting
them, and write nothing else about the gate: no restated answers, permissions or settings checks.
Cleared means every item was answered, none was left unknown, and any permission the Permission
item requires covers repeating this use at this destination. A refusal, a missing answer, or a
permission given for one transfer only does not clear the gate.

Answer the full gate again when any of those four changes, for example a new match in the
list, an added column, another service, account or workspace, or a wider audience. Also answer
it again when any other answer in the record no longer holds (for example, someone named in it
moved to another country), when the data now shows a sensitive finding that the record does not
name, or when the destination's settings, terms or controls may have changed since the recorded
inspection.

A project convention, or an instruction to skip or shorten privacy checks, is not a gate record:
it is not permission from anyone else who may be living. A statement that the gate was answered
before, without the written record, is not a gate record either.

### Living people

Stay on the family-history question and the materials the user supplied. Do not look up a
living person's current address, phone number, email, workplace, online accounts,
movements or finances, and do not trace minors on the web. Do not use people-search or
contact-aggregator services. Never use leaked or breached data, another person's account or
session, or a false pretext. When the question itself concerns a living person (unknown
parentage, a planned contact), identify them only as far as the question needs and keep the
data to the minimum.

Contact a living person only through a route the person or the tester already has, the
testing site's own messaging, or a relative who agrees to pass the message on. The identity
that must be easy to check is the sender's. Stage a contact about DNA (a DNA match, a kit
manager, or a relative asked to test or approached about a DNA or parentage question) through
[DNA match outreach staging](recipes/dna-match-outreach-staging.md). For any other contact,
such as a cousin asked for a photograph, a record submitter or a donor, apply that recipe's
consent and disclosure rules and its log, and skip what applies only to DNA tests (a tester's
agreement, kit pair, site, shared cM).

### Record requests

When a record may be about a living person, request only what the family question needs.
Never request a record to find a living person or to learn about their present life. Name
the record's own access rule (closure period, who is entitled, the subject's consent) and
follow it. An office's rule on who may order a record is not the subject's permission: the
Permission item still applies to each living person the request names. Until every item is
answered, the request stays an unsent draft on the user's device. Send only the identity and
kinship proof the custodian asks for. The Retention item and the next rule apply to what arrives.

### Third persons in sensitive files

Informers, witnesses, interrogators and co-accused named in repression, interrogation,
police or compensation files are not republished, and are not named in a report or tree
shared with others. Refer to them by role, for example "a witness".

<!-- recipe-catalog:start -->
## Recipes: Research method

### Evidence and proof

- `recipes/evidence-proof-judgment.md` — Judge identity, conflicting records, indirect or negative evidence and DNA-plus-document proof before stating any genealogical conclusion.
- `recipes/genealogy-standards-audit.md` — Audit a report, proof or documented tree against professional standards by tracing each claim to examined sources and reasoning.
- `recipes/source-citation.md` — Write citations that let a reader retrieve the source and see which evidence each citation supports.
- `recipes/research-documentation.md` — Keep a log and report of searches, results and analysis so an investigation can resume.
- `recipes/finnish-commemorative-plaque-evidence.md` — Use Finnish installation reports, inscriptions and dated building records to identify the person, event and site commemorated by a wall plaque.

### AI and long projects

- `recipes/agent-research-project.md` — Keep a months-long AI-agent genealogy project honest: evidence rules, Markdown notes, status words, corrections and safe tree writes.
- `recipes/ai-for-documentary-records.md` — Use AI safely on records: handwriting transcription and translation, OCR full-text search, AI-indexed records, record hints and photo restoration.

### Search coverage and name searches

- `recipes/archival-image-coverage-verification.md` — Check archival case boundaries, image order and which pages were actually inspected before calling a search complete.
- `recipes/corpus-seeded-name-search.md` — Recover attested name spellings that searches miss across scripts and OCR by separating encoding, orthography and field behaviour.
- `recipes/surname-distribution-locality-leads.md` — Rank localities to search from dated surname-distribution sources for an uncommon surname.
- `recipes/maiden-name-recovery.md` — Find a woman's birth surname when records give her husband's, through marriage, children's, census, newspaper, probate and U.S. Social Security records and Italian, Chinese and Japanese naming customs.

### Family trees and research planning

- `recipes/rootsmagic-tree-reconciliation-workflow.md` — Reconcile selected facts and sources between RootsMagic, Ancestry TreeShare and FamilySearch.
- `recipes/ftm-research-workflows.md` — Use Family Tree Maker to keep Ancestry record images locally, compare a FamilySearch branch, list people by place, search and merge records, undo edits and share with relatives.
- `recipes/wikitree-dna-tester-links.md` — Register a DNA test on the actual tester's WikiTree profile and verify its FamilyTreeDNA or GEDmatch link destination.
- `recipes/gedcom-research-export.md` — Export research findings to a GEDCOM file, or bring a supplied one into research, without changing what they prove.
- `recipes/descendancy-gap-worklist.md` — Turn "research the descendants" into a ranked list of gaps tied to the records each lifespan crosses.
- `recipes/genealogical-numbering-systems.md` — Decode Ahnentafel, Henry, Register and NGSQ numbers when extracting people and relationships from a pedigree chart, descendancy list or compiled genealogy.
- `recipes/ancestry-pro-tools-tree-worklists.md` — Build place or tag worklists, audit Tree Checker flags, and review the scope of Ancestry Pro Tools maps and charts.
- `recipes/cousin-relationship-paths.md` — Calculate cousin degree and removal, and distinguish double or half cousin paths when pedigrees intersect more than once.
- `recipes/myheritage-profile-hint-extraction.md` — Review the evidence behind a MyHeritage Hint, compare conflicting values and save only the supported facts or relationships.
- `recipes/myheritage-country-coding-place-audit.md` — Use MyHeritage Country Coding to review uncoded locality names and modern flags that can misrepresent historical jurisdictions.

## Recipes: DNA

### DNA reasoning

- `recipes/unknown-parentage-wato.md` — Place an unknown parent, an adoptee's birth family or an unplaced ancestor in a tree with DNA matches and WATO hypotheses.
- `recipes/ai-for-dna-research.md` — Use AI on DNA work: what to delegate, what never to trust, endogamy, segment attribution and comparing related testers.
- `recipes/ydna-mtdna-interpretation.md` — Read a haplogroup, Y-STR or mtDNA match for what it can and cannot show about a relationship in genealogical time.
- `recipes/xdna-phasing-judgment.md` — Judge X-DNA matches and visual or parental phasing: what a segment, X match or phased map can confirm or rule out.
- `recipes/dna-comparison-controls.md` — Reconcile conflicting DNA results across testing companies and tools with exact tests, controls and marker coverage.

### DNA testing sites and tools

- `recipes/23andme-match-research.md` — Research 23andMe matches: the comparisons the site permits, numerical matrices, segment painting and preserving dated results.
- `recipes/ancestry-dna-match-investigation.md` — Investigate AncestryDNA matches: closest relatives, shared-match groups, collateral names, notes, tester links and missing match rows.
- `recipes/ftdna-practical-dna-workflows.md` — Keep FamilyTreeDNA match and segment exports, tree links, Family Matching and Y-DNA Group Time Tree observations reproducible.
- `recipes/gedmatch-practical-dna-workflows.md` — Work reproducibly in GEDmatch: kit baselines, one-to-one checks, segment search, tag groups, triangulation, phasing and Lazarus kits.
- `recipes/myheritage-dna-match-investigation.md` — Investigate MyHeritage DNA matches: the right kit, filtered shortlists, shared-match values, triangulation and Theory of Family Relativity.
- `recipes/dnapainter-practical-dna-workflows.md` — Use DNA Painter to map segments, combine phased maps, estimate missing intervals, plan tests and check shared-cM ranges.
- `recipes/myheritage-kit-processing-and-downloads.md` — Identify how MyHeritage processed a kit, distinguish its raw autosomal file from CRAM, and check options for a legacy result.
- `recipes/banyandna-complex-pedigree-analysis.md` — Test a pedigree with more than one relationship path using BanyanDNA validation and alternative placements with documented autosomal comparisons.

### Ethnicity, admixture and match outreach

- `recipes/interpreting-ancestry-composition-estimates.md` — Decide what an ethnicity or ancestry-composition estimate, including GEDmatch admixture output, can show about origins and parentage, and what needs matches or records.
- `recipes/admixture-model-run-scope.md` — Record the run scope of a G25, calculator or qpAdm admixture result before reading it.
- `recipes/ethnicity-estimate-version-comparison.md` — Save, date and compare successive AncestryDNA, MyHeritage or FamilyTreeDNA ethnicity-estimate versions.
- `recipes/dna-match-outreach-staging.md` — Stage and draft outreach to a DNA match, a match's account manager or an untested relative.

## Recipes: Record websites, libraries and maps

### Record websites

- `recipes/ancestry-record-search-recovery.md` — Recover Ancestry records a search missed by checking collection scope and coverage before loosening dates, places or names.
- `recipes/familysearch-practical-record-workflows.md` — Recover FamilySearch catalog, image-only and full-text records, cite the exact view, and repair Source Linker and Family Tree errors.
- `recipes/myheritage-historical-record-search.md` — Recover MyHeritage historical records hidden by collection coverage, search fields, name variants, languages or OCR.
- `recipes/newspapers-com-search-recovery.md` — Find notices on Newspapers.com that name searches miss, after checking which titles and issues are actually covered.
- `recipes/geni-practical-research-workflows.md` — Use Geni for name variants, relationship paths, citations, projects, merge decisions, tree conflicts and GEDCOM exports.
- `recipes/find-a-grave-memorial-corrections.md` — Send evidence-backed Find a Grave corrections and route management requests to the right recipient.
- `recipes/newspaper-finder-title-coverage.md` — Use Newspaper Finder to discover alternate hosts for a historical newspaper and verify whether a host carries the target issue.
- `recipes/us-national-archives-finding-aids-and-microfilm.md` — Resolve a U.S. National Archives series or film reference into an exact entry, roll and access route.
- `recipes/familysearch-research-wiki-locality-routing.md` — Use FamilySearch Research Wiki jurisdiction and record-type pages to locate online and offline holdings before running a name search.
- `recipes/rootstech-on-demand-session-recovery.md` — Find a relevant RootsTech session across location, language and speaker filters and check for a recording or downloadable handout.
- `recipes/rootsweb-broken-link-recovery.md` — Recover a vanished RootsWeb publication, society page or tree lead through archived URLs and successor hosts.
- `recipes/elephind-historical-newspaper-search.md` — Choose Elephind’s keyword or semantic search, check the indexed newspaper title and verify the article at its host.
- `recipes/filae-historical-record-search.md` — Choose the Filae collection that covers a French event, narrow by relatives and carry the result to the underlying record.
- `recipes/finland-astia-creator-and-material-search.md` — Find a Finnish National Archives holding by separating the record creator from the material description and checking the resulting archive hierarchy.
- `recipes/finnish-astia-archival-unit-recovery.md` — Find a Finnish archival unit from its call number, series or creator and determine how to consult it when Astia search or images fail.

### Books, periodicals and manuscripts

- `recipes/published-book-catalogue-and-full-text-discovery.md` — Find a published local history, compiled genealogy or family book across catalogues and full text.
- `recipes/periodical-index-search-retrieval.md` — Search a genealogical periodical index such as PERSI and retrieve the article.
- `recipes/manuscript-collection-recovery.md` — Find personal, family and organisational papers that may mention an ancestor, including ledgers, daybooks and claim folders.
- `recipes/local-repository-uncatalogued-holdings.md` — Ask a local library, society or archive about its uncatalogued holdings after its catalogue returns nothing.
- `recipes/historical-newspaper-section-search.md` — Choose historical newspaper sections for social ties, business activity, missing immigrants, and out-of-town deaths.
- `recipes/olympic-participation-records.md` — Check Olympic results and trials, then route Olympic publications and archival files to the right finding aid.
- `recipes/slavevoyages-person-and-voyage-linkage.md` — Choose the named-person dataset that fits the route, then trace the candidate through the underlying record and voyage.
- `recipes/slavery-convention-territorial-record-recovery.md` — Find the records a jurisdiction created while accepting, excluding or implementing obligations under the 1926 Slavery Convention.

### Places and maps

- `recipes/historical-place-name-resolution.md` — Resolve a place named in a record, letter, Bible or biography to dated, same-named candidates from period gazetteers.
- `recipes/historical-map-record-recovery.md` — Read a historical map, atlas, plat or fire-insurance sheet as dated evidence, and trace a detached archival map to its case.

## Recipes: Records by country and region

### Central and Eastern Europe by period state

- `recipes/galicia-bukovina-habsburg-record-routing.md` — Route a Galician or Bukovinian event by date, confession and custodian, and decide the army before searching WWI records.
- `recipes/bessarabia-moldova-record-routing.md` — Route a Bessarabian, Moldovan or left-bank Dniester event by date, district and present custodian.
- `recipes/historic-hungary-record-routing.md` — Route a record from the pre-1920 Kingdom of Hungary by county, successor state and record type.
- `recipes/austrian-confessional-register-routing.md` — Route an Austrian or Czech-lands birth, marriage or death to the confessional or civil register that legally recorded it.
- `recipes/polish-index-original-record-recovery.md` — Recover an original Polish register entry from Geneteka, Metryki or Szukaj w Archiwach, or document the retrieval gap.
- `recipes/polish-parish-and-civil-register-routing.md` — Identify the relevant Polish registration district by date and confession, then locate the parish, civil or archival copy.
- `recipes/romanian-chamber-of-labour-personnel-files.md` — Find a Romanian artisan’s or apprentice’s file through the Chamber of Labour office, its credential series and its name index.
- `recipes/bialystok-cholera-committee-record-recovery.md` — Find a named household in Białystok county's 1831 cholera reports, tally and orphan records, then reconcile the dated statements.
- `recipes/cmolas-estate-inventory-recovery.md` — Find the Cmolas estate inventory and compare its numbered entries, kinship terms and child counts with dated parish records.
- `recipes/czech-estate-corvee-record-recovery.md` — Use Bohemian and Moravian estate records to separate the labor a holding owed from the work its occupants performed.
- `recipes/czech-historical-census-recovery.md` — Find a Czech census schedule by year, historical district and house number, then interpret residence, home municipality and language in their own columns.
- `recipes/czech-newspaper-criminal-case-recovery.md` — Recover Czech press coverage of an incident, trial, verdict and prison transfer, then carry the reported dates and court into the archival search.
- `recipes/czech-parish-death-entry-reading.md` — Separate death, discovery, burial, rites and informants in Czech parish entries and follow a reported cause to its supporting record.
- `recipes/estonian-byname-and-surname-recovery.md` — Use Estonian revision lists, farm moves and surname assignments to distinguish a place-bound byname from a name a family carried.
- `recipes/estonian-surname-and-household-recovery.md` — Connect an Estonian surname to its assignment record and trace the earlier household through manor revisions, parish books and farm bynames.

### Russian Empire and Soviet Union

- `recipes/russian-orthodox-metrical-book-recovery.md` — Locate and read a Russian Orthodox metrical entry through the period parish, the consistory copy and its margin notes.
- `recipes/russian-empire-jewish-metrical-book-recovery.md` — Find the crown rabbinate that registered a Jewish community in the event year, check whether its books survive and list substitutes.
- `recipes/russian-revision-list-household-chaining.md` — Chain a non-Jewish revision-list household across copies, sections and revisions.
- `recipes/russian-orthodox-confession-list-reading.md` — Read Russian Orthodox confession lists household by household across years and check them against revision lists and metrical books.
- `recipes/russian-household-list-transcription-audit.md` — Audit a transcription of a Russian confession list or revision tale against the images, keeping names, kin terms and counts as written.
- `recipes/russian-village-family-reconstitution.md` — When a Russian peasant's birth or parentage record is missing, rebuild the village's couples and households from every register role.
- `recipes/muscovite-census-settler-origin-recovery.md` — Push a Ural or Siberian peasant line before 1719 through Muscovite census, fiscal and fugitive-inquiry books.
- `recipes/russian-estate-registration-status.md` — Read a Russian-Empire estate label as a dated registration status and pick the record series by when it was acquired.
- `recipes/russian-volost-town-administration-records.md` — Find household-level lists in volost, village-society and town-administration fonds when metrical books or revision lists stop.
- `recipes/old-believer-sectarian-record-recovery.md` — Recover Old Believer and Edinoverie families from raskol series in consistory, revision, district and police fonds.
- `recipes/orthodox-clergy-record-recovery.md` — Rebuild a Russian Orthodox cleric's dated chain of posts and household from directories, eparchial gazettes and clergy registers.
- `recipes/russian-imperial-service-record-recovery.md` — Recover a pre-1917 official's formulary or service list through the employing institution's fond.
- `recipes/school-university-record-recovery.md` — Find a pupil or student through school, educational-district, duplicate-copy, yearbook and later personal-file records.
- `recipes/russian-empire-emigrant-origin-recovery.md` — Trace a Russian Empire emigrant from U.S. arrival records, including Canadian transit, back to an exact home locality, mainly 1880–1924.
- `recipes/soviet-personal-file-recovery.md` — Rebuild a Soviet-era life from institutional personal files when ZAGS or metrical records are lost.
- `recipes/russian-military-repression-record-episodes.md` — Read Russian WWI, Soviet WWII and repression records as separate dated episodes before merging them into one life.
- `recipes/chechen-ingush-1944-deportation-records.md` — Trace a Chechen or Ingush family through the 1944 deportation and special settlement, under old and new place names.

### Jewish records

- `recipes/russian-empire-jewish-identity-attribution.md` — Resolve a Russian-Empire Jewish ancestor whose name fits neither candidate branch, using registration records, naming customs and careful DNA tests.
- `recipes/jewish-genealogy-conditional-hypotheses.md` — Test Jewish naming, ancestral-town and DNA clues as separate conditional hypotheses before linking a family.
- `recipes/jewishgen-search-family-reconstruction.md` — Recover families a JewishGen name-and-town search missed: name variants, mixed-field batches, wives' natal families and married daughters.
- `recipes/beider-given-name-variants.md` — Expand searches with recorded Ashkenazi given-name forms from Beider's male and female indexes.
- `recipes/hebrewbooks-search-recovery.md` — Recover HebrewBooks names or passages missed by OCR, catalogue spelling or a query that never reached search.
- `recipes/rabbinic-literature-person-search.md` — Find and interpret passages about a Jewish ancestor, rabbinic office or claimed lineage in rabbinic and Hasidic books.
- `recipes/holocaust-testimony-source-interpretation.md` — Interpret a Yad Vashem result through its testimony, wartime list or survivor source and statement dates.
- `recipes/israel-immigration-list-research.md` — Search MyHeritage's Israel immigration lists and decide whether an arrival entry for Mandatory Palestine or Israel records an immigrant, a returning resident or a tourist.
- `recipes/lithuanian-jewish-household-registers.md` — Use LitvakSIG and MyHeritage household registers to trace dated residence and distinguish missing records from unindexed coverage.
- `recipes/holocaust-register-and-survivor-list-recovery.md` — Separate ghetto residence, imprisonment, death and postwar survivor registration while retrieving the underlying Holocaust-era record.
- `recipes/arolsen-confiscated-effects-recovery.md` — Identify a Nazi persecution victim in the Arolsen personal effects collection and follow the archive’s return procedure.

### Ukrainian archives

- `recipes/jewish-archival-list-triage.md` — Select Ukrainian archival cases that hold named Jewish lists, separating title, place and document evidence.
- `recipes/elib-ukrainian-archive-reference-books.md` — Retrieve Ukrainian archival guides from ELIB and identify the correct volume, part and fund scope.

### Germany

- `recipes/german-register-image-recovery.md` — Trace an emigrant's German place name to its church or civil register entry through locality, record office and register version.
- `recipes/german-emigrant-origin-sources.md` — Trace a German emigrant's home town through emigration files, indexes and the origin parish register.
- `recipes/german-local-census-registration-recovery.md` — Recover German nominal census lists, residential-registration entries and related settlement or trade-permission files.
- `recipes/german-military-record-period-routing.md` — Route a German soldier to the surviving series for his period, army and rank, including hospital books.
- `recipes/nazi-era-ancestry-proof-records.md` — Find and read a Nazi-era Ahnenpass or certified ancestry proof, and route the search by the role that required it.
- `recipes/german-official-gazette-notice-search.md` — Read German gazette personnel, expulsion and expatriation notices as dated acts by a named authority.
- `recipes/german-compensation-file-recovery.md` — Carry a Lastenausgleich or Berlin Wiedergutmachung index hit to the file behind it.
- `recipes/old-german-handwriting-comparison.md` — Compare a disputed Old German word with script samples, generated candidate forms and examples in the same hand.

### Britain and Ireland

- `recipes/england-wales-gro-index-recovery.md` — Read England and Wales GRO and FreeBMD index entries as registration observations.
- `recipes/english-nonregister-record-recovery.md` — Take an English or Welsh question past the parish register to poor-law, apprenticeship, church-court probate, dissenter and Catholic records.
- `recipes/uk-census-and-1939-register-interpretation.md` — Read England and Wales censuses from 1841 to 1921 and the 1939 Register under each year's own rules.
- `recipes/scottish-parish-statutory-record-recovery.md` — Recover a Scottish birth, baptism, marriage or death across Old Parish, statutory, corrected-entry and kirk-session records.
- `recipes/scottish-high-court-precognitions-trial-papers.md` — Find a Scottish High Court of Justiciary criminal case in the precognitions, trial papers and minute books, and read what each record does and does not show.
- `recipes/irish-civil-registration-jurisdiction-recovery.md` — Carry an Irish civil-registration index entry or townland lead to the matching certificate and its jurisdiction chain.
- `recipes/irish-catholic-parish-image-recovery.md` — Find an Irish Catholic baptism or marriage in the National Library of Ireland's parish-register images.
- `recipes/irish-probate-and-deed-recovery.md` — Recover an Irish will, administration or deed after the 1922 losses through surviving calendars, will books and the Registry of Deeds.
- `recipes/irish-emigrant-origin-locality.md` — Resolve an Irish place named by an emigrant's records or family tradition to a searchable locality.
- `recipes/irish-land-valuation-occupancy-series.md` — Read Griffith's Valuation, tithe books, valuation revisions and estate rentals as dated occupancy series.
- `recipes/irish-1901-1911-census-returns.md` — Search, retrieve and read the Irish 1901, 1911 and 1926 census returns.
- `recipes/convict-transportation-record-chain.md` — Rebuild a transported British convict's sentence as a chain of dated record episodes.
- `recipes/british-colonial-slave-registers.md` — Trace an enslaved ancestor through the British colonial slave registers of 1813–1834 and the compensation records.
- `recipes/british-army-first-world-war-service-records.md` — Route a First World War British Army soldier, nurse or Household Cavalry member to the surviving series for their service.
- `recipes/piracy-and-privateering-records.md` — Use a commission, vessel history and surviving court papers to distinguish a commissioned capture from piracy and follow a sailor’s disposition.
- `recipes/british-raf-air-force-list-recovery.md` — Reconstruct British RAF officer rank and seniority from dated Air Force Lists, then choose the personnel series that fits the person.
- `recipes/jersey-occupation-registration-card-recovery.md` — Trace a Jersey resident or child through German Occupation registration cards and household entries.
- `recipes/british-army-wwii-casualty-lists.md` — Trace a British Army casualty through successive wartime lists and reconcile changes in status by service number.
- `recipes/durham-home-guard-record-recovery.md` — Trace a County Durham Home Guard candidate from the name index to the original WO 409 enrolment form and identify the unit.
- `recipes/england-wales-historical-divorce-recovery.md` — Trace an England or Wales divorce from an index hit to the court papers and distinguish allegations, petitions and decrees.
- `recipes/english-chancery-equity-suit-recovery.md` — Find an English Court of Chancery dispute by party, then retrieve its pleadings, depositions, orders and decrees as separate records.

### Western and Northern Europe

- `recipes/french-departmental-record-routing.md` — Route French civil, census, military, notarial, property and prison records by creator, département, series and access rule.
- `recipes/french-belgian-civil-act-extraction.md` — Extract French or Belgian civil acts field by field, follow marginal notes and copies, and use Paris reconstructions for lost originals.
- `recipes/dutch-civil-church-record-recovery.md` — Recover Dutch civil acts through ten-year indexes and marriage supplements, and the church registers kept before civil registration.
- `recipes/amsterdam-archival-record-recovery.md` — Follow an Amsterdam City Archives index hit, tree claim or burial card back to its own register entry.
- `recipes/italian-stato-civile-parish-record-recovery.md` — Send an Italian birth, marriage or death to the register legal in that place and year, then search conscription and population registers.
- `recipes/spanish-civil-parish-record-routing.md` — Route a Spanish or Andorran vital, padrón, notarial, military or Civil War record to the body that holds it on the event date.
- `recipes/portuguese-parish-civil-register-recovery.md` — Find a baptism, marriage or death in mainland Portugal, the Azores or Madeira in the parish books or the civil register.
- `recipes/scandinavian-parish-record-recovery.md` — Reconstruct a Swedish household through the household-examination, birth, marriage, death and moving registers.
- `recipes/danish-church-book-probate-recovery.md` — Find a Danish ancestor's church-book entries, civil marriage and probate by choosing the register copy, South Jutland civil register and probate authority that apply to the date.
- `recipes/scandinavian-patronymic-farm-name-record-recovery.md` — Find a Danish, Norwegian, Swedish or Icelandic emigrant's home-parish entries under patronymic, farm and soldier names.
- `recipes/swedish-military-record-routing.md` — Route a Swedish soldier, sailor, officer or conscript to the military series that survive for his type and period.
- `recipes/french-succession-and-absence-tables.md` — Use a French registration-office index to distinguish a recorded death from declared absence and retrieve the referenced succession declaration.
- `recipes/swiss-place-of-origin-record-recovery.md` — Distinguish Swiss communal citizenship from birthplace and residence, then choose the municipal, cantonal or parish record for the question.
- `recipes/danish-census-household-recovery.md` — Find Danish census households by name or historical address and read household position and occupation against the schedule for each census year.
- `recipes/finnish-astia-archival-image-recovery.md` — Find a Finnish register image after an Astia miss by checking the series tree, contributor indexes and item access separately.
- `recipes/finnish-court-book-recovery.md` — Find a Finnish district or appellate court entry through its historical jurisdiction, court-book copies, card indexes or publication registers.
- `recipes/finnish-debt-imprisonment-records.md` — Follow a historical Finnish debt proceeding through enforcement, confinement and bankruptcy records to determine what happened to the debtor and the debt.
- `recipes/finnish-diocesan-circulars-and-observances.md` — Use Turku and Porvoo circulars to test whether a Finnish thanksgiving or commemoration was diocesan and verify local observance in newspapers.
- `recipes/finnish-factory-and-craft-listings.md` — Find a nineteenth-century Finnish establishment, owner or practitioner by choosing a named factory list, trade directory or craft register.
- `recipes/finnish-farm-subdivision-record-recovery.md` — Find the survey map and minutes behind a named Finnish farm share and separate the recorded subdivision from any earlier inheritance division.
- `recipes/finnish-crown-farm-purchase-recovery.md` — Use Finnish land-register annotations to find a Crown farm’s hereditary purchase in Swedish or Finnish records.
- `recipes/finnish-fire-insurance-record-recovery.md` — Trace Finnish properties through Swedish-era and Finnish insurers’ notices, policies, appraisals, plans and payout reports to document buildings and fire damage.
- `recipes/finnish-folk-poetry-informant-recovery.md` — Trace a historical folk-poetry informant through SKVR entries, collection notes and the collector’s published accounts.
- `recipes/finnish-great-northern-war-refugee-recovery.md` — Trace a family displaced from Finland through wartime relief lists and Swedish parish evidence, then check for a documented return.
- `recipes/finnish-henkikirja-record-recovery.md` — Find a Finnish henkikirja by historical parish, district, year and volume signum, and distinguish index gaps from missing roll entries.

### United States: people, vital and church records

- `recipes/us-census-practical-workflows.md` — Find and read U.S. census households: missing entries, district browsing, the 1890 gap, special schedules and changed surnames.
- `recipes/usa-immigration-search-recovery.md` — Trace U.S. immigration and naturalization by sea, air or land border, and read manifests, verification marks and federal files.
- `recipes/us-vital-registration-coverage.md` — List every U.S. birth and death registration authority and series before calling a record missing.
- `recipes/us-obituary-search-and-interpretation.md` — Judge whether a U.S. obituary should exist, find it through relatives' notices, cards of thanks and funeral cards, and read it as an informant's account.
- `recipes/us-church-record-custody.md` — Work out the denominational branch, congregation and current custodian of a U.S. church record.
- `recipes/missing-marriage-jurisdiction-search.md` — Replace a marriage missing from the couple's home county with a dated, ranked list of candidate jurisdictions.
- `recipes/early-new-england-town-records.md` — Read early New England town books across parent, daughter and neighbouring towns, and decode Torrey's marriage notation.
- `recipes/quaker-meeting-record-recovery.md` — Recover a Quaker ancestor from men's and women's monthly-meeting minutes and both removal-certificate series.
- `recipes/us-tribal-enrollment-record-recovery.md` — Find a claimed Native American ancestor on the right tribal roll and read what enrollment, rejection or absence proves.
- `recipes/us-freedpeople-record-recovery.md` — Trace an African American family back across the 1870 boundary.
- `recipes/ark-and-dove-passenger-reconstruction.md` — Use the Ark and Dove compilation and original Maryland records to distinguish a voyage claim from early settlement or descent.
- `recipes/enslavement-record-disclosure.md` — Make privately held records of enslaved people discoverable through source-cited extracts, archival deposits and documented tree links.
- `recipes/mayflower-and-great-migration-genealogies.md` — Choose a passenger branch or an immigrant arrival series, then test the claimed line against the correct child lists.
- `recipes/new-york-city-vital-certificate-extraction.md` — Recover both New York City marriage filings in 1908–1937 and extract birthplace and sibling clues from historical birth certificates.
- `recipes/pennsylvania-marriage-licenses-and-returns.md` — Recover Pennsylvania county marriage packets from 1885 and compare them with early state copies and older marriage bonds.
- `recipes/american-voter-register-eligibility.md` — Check voting and registration eligibility in the relevant year before using a U.S. voter-register entry or omission as residence evidence.
- `recipes/us-social-security-application-recovery.md` — Choose between a Social Security death index, Numident extract and original SS-5 when researching a deceased person’s birth or parents.
- `recipes/us-historical-passport-application-recovery.md` — Find U.S. passport applications through March 1925 and separate recorded identity, companions and planned travel from the journey itself.
- `recipes/declaration-signer-descendant-records.md` — Find lineage leads for a named Declaration signer in the Leach manuscripts and the indexed society application files.

### United States: military, land, courts and law

- `recipes/us-military-service-type-record-routing.md` — Route pre-1900 U.S. military service by service type to its own record series and custodian.
- `recipes/us-civil-war-service-record-episodes.md` — Read Civil War draft registration, service cards, roster remarks and unit events as separate episodes.
- `recipes/us-20th-century-military-service-reconstruction.md` — Rebuild a 20th-century U.S. Army or Air Force service record from sources outside a burned, thin or restricted personnel file.
- `recipes/us-military-pension-file-recovery.md` — Carry a service clue or pension index card to the right application file and inventory its documents.
- `recipes/dar-ancestor-record-interpretation-and-correction.md` — Interpret red notices and error codes on a DAR Ancestor Database record, and route new evidence or corrections to DAR through applications, supplementals or the Corrections Genealogist.
- `recipes/virginia-revolutionary-public-service-claims.md` — Trace a Revolutionary Virginia public service (impressed property) claim across court booklets, certificates, Commissioner's Books and offline rejected claims, and date a commissioner's office from its act.
- `recipes/us-federal-land-entry-file-recovery.md` — Follow a GLO patent, bounty-land number or final-proof notice to the federal land-entry case file.
- `recipes/georgia-texas-state-land-grant-recovery.md` — Find and read an original Georgia or Texas land grant, and read each lottery entry, headright class or certificate under its own act.
- `recipes/state-archives-county-records-guides.md` — Read a state archives' county-records guide to see which series it holds for a U.S. county, as originals or microfilm, and choose how to retrieve each.
- `recipes/court-case-file-recovery.md` — Recover a U.S. state or local civil, divorce, criminal or incapacity case file through the records that point to it.
- `recipes/us-guardianship-records.md` — Read a colonial or U.S. guardianship record for what it shows about a ward's age, parents, guardian and property, and find the rest of the file.
- `recipes/us-federal-court-case-file-recovery.md` — Take a lead to the right U.S. federal court for the period, its National Archives records and the case file.
- `recipes/criminal-court-prison-record-recovery.md` — Trace a U.S., English, Welsh or Swedish arrest or imprisonment to its court, prison and pardon records; a state or local court's case file belongs to court case-file recovery.
- `recipes/state-legislative-private-act-petitions.md` — Recover a state legislative private act, such as a legitimation, name change, divorce or pension, and its petition.
- `recipes/us-period-law-record-reading.md` — Read a U.S. record's legal terms, courts, bonds, age and inheritance rules under the law of its place and date.
- `recipes/confederate-hospital-record-recovery.md` — Route a Confederate treatment clue to the hospital’s patient registers, case books and separate wartime papers.
- `recipes/southern-claims-commission-case-files.md` — Route a Southern Claims Commission claimant to the correct case file and use witness testimony to reconstruct wartime events.
- `recipes/us-army-civil-war-court-martial-files.md` — Follow a general court-martial notation from a Civil War service card to the index and its Army case papers.
- `recipes/world-war-two-us-navy-battle-records.md` — Correlate wartime U.S. Navy muster and deck records with an action report before attributing participation to a sailor.
- `recipes/boston-tea-party-participant-evidence.md` — Trace a Boston Tea Party participant claim from compiled lists to the evidence for the person’s role on 16 December 1773.
- `recipes/colonial-and-state-military-bounty-land.md` — Distinguish a colonial or state military land award from a federal warrant and trace the soldier, heir, assignee and tract separately.
- `recipes/colonial-virginia-patent-and-northern-neck-recovery.md` — Find the issuer of a colonial Virginia land grant and use its patent, warrant, survey or headright evidence to identify the tract and parties.
- `recipes/us-army-quartermaster-record-recovery.md` — Use the Quartermaster General’s claims, contracts, correspondence and personnel series to trace Army suppliers, employees or officers.
- `recipes/us-military-headstone-application-recovery.md` — Route a U.S. military headstone application by death and application dates, then compare its service and burial identifiers.
- `recipes/us-treasury-accounting-military-claims.md` — Find Treasury audit, paymaster or pension-account records for a U.S. military payment or claim, using the office and transaction date.
- `recipes/us-marine-corps-muster-and-wwi-unit-records.md` — Recover a U.S. Marine’s dated unit from muster rolls, then trace First World War assignments and death records.
- `recipes/us-postmaster-appointments-and-office-sites.md` — Find a U.S. postmaster by office and date, distinguish appointment from confirmation, and locate the office in site reports.
- `recipes/wyoming-valley-susquehanna-company-claims.md` — Distinguish Wyoming Valley company share ownership, settlement and Pennsylvania title by following the relevant lists and tract papers.
- `recipes/civil-war-published-medical-case-recovery.md` — Search the Civil War Medical and Surgical History by patient and injury, then match case narratives and table rows to service evidence.
- `recipes/colonial-tavern-license-recovery.md` — Use Maryland, Delaware and Virginia tavern compilations to identify a keeper, then recover the license and the applicable local rate schedule.
- `recipes/dunmores-war-payroll-and-claims.md` — Trace a 1774 expedition participant or supplier through Virginia’s commissioners’ ledger and separate West Augusta records.

### Canada, Latin America, Asia and Oceania

- `recipes/canadian-provincial-record-routing.md` — Route a Canadian vital or estate record, war personnel file, Métis or First Nations record, or Home Child to its province, custodian and access category.
- `recipes/canadian-census-interpretation.md` — Read a historical Canadian census line as a de jure listing, and browse by geography when a name search misses.
- `recipes/french-canadian-register-recovery.md` — Recover French-Canadian ancestors from combined registers, French-post and Notre-Dame de Montréal entries and notarial acts.
- `recipes/hispanic-catholic-register-recovery.md` — Find a Mexican or other Hispanic Catholic ancestor across parish books and civil registers.
- `recipes/brazilian-parish-civil-registry-recovery.md` — Find a Brazilian parish or civil birth, marriage or death entry, and rebuild a family when parish books are lost.
- `recipes/australia-nz-record-routing.md` — Route an Australian or New Zealand vital, electoral, arrival, Māori Land Court or Aboriginal agency record to its holder and date window.
- `recipes/chinese-lineage-jiapu-records.md` — Recover a Chinese emigrant's character-written name and ancestral village before searching lineage genealogies (jiapu).
- `recipes/japanese-koseki-honseki-recovery.md` — Recover the kanji name and full historical domicile (honseki) before requesting a Japanese family register (koseki).
- `recipes/philippine-surnames-and-registers.md` — Use parish and civil records to trace a Philippine family through surname adoption or continuity across 1849.
- `recipes/samoan-matai-and-gafa-research.md` — Follow Samoan chiefly titles and village clues from diaspora records into customary land, church and family sources.
- `recipes/acadian-records-across-the-expulsion.md` — Locate an Acadian household before deportation, then link it to records at a destination or later resettlement.
- `recipes/canadian-arrival-record-routing.md` — Choose a Canadian ocean or land arrival series by port and date, and seek substitutes before interpreting a missing entry.
- `recipes/canadian-great-war-project-cross-border-enlistment.md` — Search for a possibly U.S.-born Canadian Expeditionary Force volunteer and confirm the candidate in the original service file.
- `recipes/india-great-famine-household-record-recovery.md` — Follow a household across famine-era district, relief, land and migration records without assigning a cause from disappearance alone.
- `recipes/american-revolutionary-loyalist-record-recovery.md` — Trace wartime allegiance, evacuation and resettlement through British, Canadian and colonial records for American Revolutionary Loyalists.
- `recipes/australian-first-world-war-embarkation-recovery.md` — Use an Australian Imperial Force embarkation roll to identify a land-service member and trace later units, casualty records and honours.
- `recipes/australian-wartime-internment-record-recovery.md` — Distinguish a civilian internee from a captured serviceman and use Australian detention, registration and appeal series to reconstruct the person’s records.
- `recipes/buenos-aires-passenger-arrival-recovery.md` — Trace a historical Buenos Aires sea arrival from the CEMLA index to Argentina’s passenger entry books or later migration records.

## Recipes: Record types in any country

### Church and congregation registers

- `recipes/catholic-parish-diocesan-record-recovery.md` — Search for a Catholic sacrament across the parish, nearby parishes, the diocesan copy, the successor custodian and dispensation files.
- `recipes/catholic-sacramental-cross-notations.md` — Follow a Catholic baptism–marriage cross-notation to the other sacrament's entry in another parish.
- `recipes/immigrant-congregation-origin-records.md` — Find an immigrant's hometown in the registers of U.S. congregations chosen by language community, dates and address.
- `recipes/intercountry-adoption-record-discrepancies.md` — Compare birth and placement records, adoption papers and attributed family accounts when an intercountry adoption may have been irregular.
- `recipes/catholic-vocation-and-clergy-records.md` — Choose the sources for a named Catholic priest, missionary or religious in Spanish-language archives and separate ordination, assignments, licences and profession.

### Burials, directories, land and probate

- `recipes/burial-evidence-packet.md` — Recover a cemetery entry, its photo or inscription, and the plot and register locators needed to check a burial.
- `recipes/memorial-card-and-coffin-plate-evidence.md` — Read a memorial, mourning or funeral card or a coffin plate from a family collection as evidence of a death and route its leads to the death's records.
- `recipes/city-directory-observation-workflow.md` — Build a comparable series of city-directory names, addresses and occupations from checked editions and sections.
- `recipes/land-index-book-series-recovery.md` — Trace a land record through both index directions to the right instrument and book, or a federal patent to its entry file.
- `recipes/deed-content-relationship-clues.md` — Read a deed's type, consideration, terms, parties and parcel for dated clues to heirship, probate, migration or land identity.
- `recipes/tax-roll-observation-workflow.md` — Read town, township or county tax lists as a liability-bounded annual series for each jurisdiction and tax type.
- `recipes/marks-and-brands-record-recovery.md` — Carry a livestock marks-and-brands index entry to the actual registration or a described copy.
- `recipes/probate-case-document-inventory.md` — Recover every document behind a probate index, will or bond and list them as a case inventory with open leads.
- `recipes/cemetery-survey-and-transcription.md` — Map and number a whole cemetery survey so another researcher can match each transcription, image or recording to its marker.
- `recipes/coroner-death-investigation-record-recovery.md` — Use coroner and medical examiner indexes, case numbers and local access rules to recover a death investigation, with routes for Los Angeles, Humboldt and British Columbia.

### Births outside marriage and institutions

- `recipes/illegitimacy-record-recovery.md` — Find the bastardy bonds, court cases, support orders and church entries a birth outside marriage could create.
- `recipes/institutional-patient-record-recovery.md` — Find asylum or state-hospital patient records through custodians, courts and newspapers, including Dutch admission correspondence.
- `recipes/child-placement-and-orphan-train-records.md` — Find an orphanage admission, foster placement or orphan-train file and establish whether a separate legal adoption followed.

### Family papers, photographs and oral history

- `recipes/family-collection-intake-and-capture.md` — Inventory, plan the capture of and hand over an inherited family collection of albums, photographs, papers or scans.
- `recipes/family-photograph-attribution-and-dating.md` — Attribute and date an inherited family photograph from captions, provenance and the photographer's imprint.
- `recipes/family-papers-and-bible-register-dating.md` — Separate writing, mailing and event dates in letters, envelopes, address books, family Bible registers and inscribed books.
- `recipes/family-interviews-and-oral-tradition.md` — Record a relative's interview, a supplied recording or an inherited story with its speaker, prompter and chain of transmission.
- `recipes/repository-photograph-collection-search.md` — Search repository photograph collections for an ancestor, home, shop or community by place and subject.
- `recipes/family-archives-material-storage.md` — Choose protective enclosures for fragile family originals while preserving the evidence that links loose items to their original homes.
- `recipes/mylio-historical-photo-date-and-worklist.md` — Use Mylio Photos to keep uncertain original photo dates, review queues, event groups and a local backup for a scan project.
- `recipes/vaud-foundling-baptism-and-naming-records.md` — Follow a Vaud foundling’s baptismal note into a dated naming or placement inquiry and identify which relationship each record establishes.

<!-- recipe-catalog:end -->

## Version and updates

This copy is version 2.2.0, released 2026-11-22.

Many installations do not update by themselves. If today's date is more than 7 days after
that release date, end your first answer in the conversation with one short note: this copy
of the recipes was released on that date, and a newer version may be available. Give the
update step for the user's installation, or the applicable options if the host is unclear:

- Copies installed from a plugin directory (Anthropic's Claude directory or the ChatGPT/Codex
  plugin directory): updates arrive through that directory.
- Claude Code: `claude plugin update genealogy-research-recipes@kinprove`. For automatic
  updates, run `/plugin`, open **Marketplaces**, select `kinprove` and choose
  **Enable auto-update**.
- Claude.ai or the Claude desktop app: on the Plugins page, select **Check for updates** on
  the `kinprove` marketplace, or turn on **Sync automatically**.
- Hermes Agent: `hermes plugins update genealogy-research-recipes`.
  If Hermes reports no update, check the
  [Hermes Marketplace listing](https://hermes-agent.nousresearch.com/marketplace/genealogy-research-recipes)
  for the version available through the catalog.
- OpenClaw: `openclaw plugins update genealogy-research-recipes`.
  ClawHub releases can lag GitHub; if no change is reported, reinstall from the repository:
  `openclaw plugins install git:github.com/Kinprove/genealogy-research-recipes --force`.

Give this note once per conversation, after the answer itself. Skip it when you do not know
today's date. Do not check for a newer version over the network yourself.

## What a recipe is (and isn't)

- **Fact-checked.** Each recipe separates independently verified claims from figures reported by a
  cited source but not independently verified. Honor that line — don't present a source-reported
  transcript figure (a specific cM number, a percentage) as a rule.
- **Judgment, not fundamentals.** Recipes carry the non-obvious judgment an unaided answer gets
  wrong, not the well-documented basics you already produce reliably.
- **Platform procedures are dated.** Playbooks pair concrete actions with source-linked records.
  Verify available controls for the selected kit/account and preserve the actual observation scope.

## Attribution

These recipes are original Kinprove-authored distillations, licensed FSL-1.1-MIT (see `LICENSE`).
Third-party facts and methods are credited in each recipe's `sources/<slug>.md`; any
reproduced third-party data is carved out in `NOTICE`.
