-----

## name: zoology
description: >
Expert zoology assistant for academic researchers. Use this skill whenever the user needs:
taxonomic classification or species identification, literature review or synthesis of animal
biology research, scientific writing (papers, field notes, reports, grant sections),
wildlife conservation analysis, ethological or behavioral study design, phylogenetic
interpretation, ecological analysis, or any rigorous academic treatment of animal biology.
Trigger for any zoology, wildlife, or animal biology question where academic depth,
correct nomenclature, and scientific rigor are expected — even if the user doesn’t
explicitly say “zoology”.
license: MIT
compatibility: opencode
metadata:
audience: researchers
category: biology

# Zoology — Academic Research Assistant

Covers: **Taxonomy & Nomenclature · Literature Review · Scientific Writing · Behavioral Research · Conservation Analysis · Phylogenetics · Field Methods**

-----

## Taxonomic Classification & Nomenclature

### Binomial Nomenclature Rules (ICZN)

- Genus capitalized, species epithet lowercase: *Panthera leo*
- Always italicize in print; underline in handwriting
- Authority and year on first use in formal writing: *Panthera leo* (Linnaeus, 1758)
- Subspecies as trinomial: *Panthera leo leo* (Linnaeus, 1758)
- After first use, abbreviate genus: *P. leo*
- Common names are not regulated — always provide the scientific name in academic work

### Taxonomic Hierarchy

```
Domain → Kingdom → Phylum → Class → Order → Family → Genus → Species
                                                     ↓
                             Intermediate ranks: Suborder, Infraorder,
                             Superfamily, Subfamily, Tribe, Subtribe
```

### Current Authoritative Sources by Taxon

|Group        |Primary Authority            |Database                                            |
|-------------|-----------------------------|----------------------------------------------------|
|All animals  |ICZN                         |[iczn.org](https://iczn.org)                        |
|Mammals      |Wilson & Reeder / ASM        |[mammaldiversity.org](https://mammaldiversity.org)  |
|Birds        |IOC World Bird List          |[worldbirdnames.org](https://worldbirdnames.org)    |
|Reptiles     |Reptile Database             |[reptile-database.org](https://reptile-database.org)|
|Amphibians   |AmphibiaWeb / ASW            |[amphibiaweb.org](https://amphibiaweb.org)          |
|Fishes       |FishBase / Catalog of Fishes |[fishbase.org](https://fishbase.org)                |
|Invertebrates|WoRMS (marine), GBIF         |[marinespecies.org](https://marinespecies.org)      |
|All taxa     |GBIF, ITIS, Catalogue of Life|[catalogueoflife.org](https://catalogueoflife.org)  |


> Always verify current accepted names — taxonomy changes frequently with molecular revisions. Note synonymies when relevant.

### Handling Taxonomic Uncertainty

- **Incertae sedis**: position uncertain within a higher group — use the phrase explicitly
- **cf.**: *cf. Ursus arctos* — the specimen is comparable to but not confirmed as the species
- **aff.**: *aff. Ursus arctos* — the specimen has affinity to but is distinct from the species
- **sp. nov.**: new species not yet formally described
- Note when a taxon is paraphyletic or polyphyletic in modern molecular treatments

-----

## Literature Review

### Search Strategy by Resource

**Primary databases (peer-reviewed):**

- **Web of Science** — best for citation tracking, impact metrics
- **Scopus** — broad coverage, good for systematic reviews
- **Google Scholar** — broadest coverage; include grey literature, theses
- **PubMed** — essential for physiology, neurobiology, parasitology
- **Zoological Record** (Clarivate) — taxonomy-focused, comprehensive back to 1864

**Specialist resources:**

- **BioOne** — ecology, conservation, field biology journals
- **JSTOR** — historical literature, essential for pre-1990 taxonomy
- **biodiversitylibrary.org** — historical natural history literature, free
- **IUCN Red List** — species accounts, population data, conservation status
- **GBIF / iNaturalist** — occurrence records, range data

### Search Term Construction

```
("Panthera leo" OR "African lion" OR "lion*")
AND (behav* OR etholog* OR territorial*)
AND (savanna OR grassland OR "sub-Saharan")
NOT captiv*

# Use MeSH terms in PubMed for physiology/parasitology topics
# Use quotation marks for phrases; truncation (*) for word variants
# Filter: Article type = Original Research; exclude reviews for primary evidence
```

### Literature Synthesis Standards

- Distinguish **primary literature** (original research) from **reviews** and **grey literature**
- Note sample sizes and geographic scope — small or regional studies may not generalize
- Flag when findings come from captive animals being applied to wild populations
- Track taxonomic changes: a species cited as *X* in 1990 may now be *Y* — check synonymies
- For behavioral claims, note whether data are observational or experimental
- Preferred citation format in zoology: **author-date (Harvard)** or journal-specific; never use footnote style

-----

## Scientific Writing

### Paper Structure and Conventions

**Abstract**: Structured or unstructured depending on journal. Include: study question, methods summary, key quantitative findings, and significance. Never cite references in an abstract.

**Introduction**: Funnel from broad context → specific gap → study objectives. End with explicit aim/hypothesis statements. Cite the primary literature establishing the gap, not textbooks.

**Methods**:

- Specify study site with coordinates and habitat description
- Give sample sizes, sex ratios, age classes where relevant
- Provide ethical approval statement (IACUC number or equivalent)
- Include statistical software, version, and package names
- Describe how animals were identified to individual (marks, tags, genetics)

**Results**: Report statistics fully — test statistic, df, p-value, effect size, CI:

```
Males were significantly heavier than females
(t₄₂ = 4.31, p < 0.001, d = 1.32, 95% CI [8.2, 23.4 kg]).
```

Never interpret in Results — save interpretation for Discussion.

**Discussion**: Lead with your main finding restated plainly. Compare with prior work, explain discrepancies. Address limitations honestly. End with implications and future directions — not a summary of your own results.

### Field Notes — Standard Format

```
Date: 2024-03-15
Time: 06:42 local (UTC+3)
Location: [Site name], [GPS coordinates — WGS84 decimal degrees]
Observer(s): [Initials]
Weather: 18°C, partly cloudy, wind NW ~10 km/h, visibility excellent
Species: Lycaon pictus (African wild dog)
Individual ID: Pack "Ruaha North", alpha female (ear tag #R-07)

Observation:
Alpha female initiated hunt at 06:42. Pack of 8 individuals (4 adults,
4 sub-adults) moved NE at ~8 km/h. Target prey: Thomson's gazelle
(Eudorcas thomsonii), single adult female. Hunt lasted 4 min 22 sec.
Outcome: unsuccessful — prey escaped into dense bush at 06:47.

Behavioral notes:
[Ethogram codes if applicable]

Voucher/media:
Photos: DSC_4421–4438
GPS track: ruaha_20240315_0642.gpx
```

### Conservation Reports

Structure for IUCN-style or agency reports:

1. **Species Account**: taxonomy, distribution, population size/trend
1. **Threats Assessment**: use IUCN threat classification scheme (1.1–11.4)
1. **Conservation Actions**: existing (in-place) vs. needed
1. **Data Gaps**: explicit statement of what is unknown
1. **Recommendations**: specific, actionable, prioritized
1. **Red List Criteria**: state which criterion (A–E) applies and why

-----

## Behavioral Research & Ethology

### Sampling Methods (after Altmann 1974)

|Method                |Use                                         |Bias                                     |
|----------------------|--------------------------------------------|-----------------------------------------|
|**Focal animal**      |Complete behavioral budget for an individual|Observer fatigue; sampling must be random|
|**Scan sampling**     |Group activity budget at intervals          |Misses rare/brief behaviors              |
|**Behaviour sampling**|Record rare behaviors whenever they occur   |Overrepresents conspicuous animals       |
|**Ad libitum**        |Opportunistic notes                         |Not quantifiable; supplement only        |

**Key rule**: state your sampling method explicitly in Methods. Mixing methods without justification is a common reviewer complaint.

### Ethogram Construction

- Define behaviors **mutually exclusively and exhaustively** (MEE)
- Use operational definitions: observable, not inferred (*“approaches within 1 m”* not *“shows interest”*)
- Distinguish **states** (duration matters: resting, foraging) from **events** (instantaneous: vocalization, attack)
- Establish inter-observer reliability before data collection: Cohen’s κ > 0.80 is standard

### Statistical Considerations for Behavioral Data

- Behavioral data are rarely normally distributed — test before assuming
- Repeated observations of the same individual are **not independent**: use mixed models with individual as random effect
- Circular statistics for temporal/directional data (e.g., activity rhythms, orientation)
- Correct for multiple comparisons (Bonferroni, FDR) when testing multiple behaviors
- Report effect sizes, not just p-values; behavioral ecology increasingly requires this

-----

## Phylogenetics & Systematics

### Reading a Phylogeny

- Branch lengths = evolutionary distance (in molecular trees) or are arbitrary (in cladograms)
- Node support: **bootstrap values** ≥ 70 or **posterior probability** ≥ 0.95 considered supported
- Polytomies (>2 branches from one node) indicate unresolved relationships, not simultaneous divergence
- Outgroup must be specified and justified
- Always note the gene(s) or genomic region used — mitochondrial vs. nuclear trees sometimes conflict

### Reporting Molecular Systematics Results

- Specify substitution model (e.g., GTR+Γ) and how it was selected (AIC/BIC in ModelTest)
- Report both maximum likelihood and Bayesian analyses when possible
- Deposit sequences in GenBank; cite accession numbers
- Note if morphological and molecular evidence conflict — this is scientifically significant

-----

## Wildlife Conservation Analysis

### IUCN Red List Criteria (Summary)

|Criterion|Basis                                                     |
|---------|----------------------------------------------------------|
|A        |Population reduction (past or projected)                  |
|B        |Geographic range restriction + fragmentation/decline      |
|C        |Small population + decline                                |
|D        |Very small population or range                            |
|E        |Quantitative analysis (PVA) showing extinction probability|

### Population Viability Analysis (PVA)

- Software: **VORTEX** (most common), **RAMAS**, **Insightmaker**
- Required inputs: survival rates by age/sex, fecundity, carrying capacity, catastrophe probabilities
- Report: median time to extinction, probability of extinction at 50/100 years, minimum viable population (MVP)
- Sensitivity analysis is mandatory — show which parameters most affect outcomes
- PVA outputs are highly sensitive to input quality; be explicit about data limitations

### Threat Classification

Use the **IUCN-CMP Unified Classification of Direct Threats** (v3.3) for consistency:

- 1. Residential & commercial development
- 1. Agriculture & aquaculture
- 1. Biological resource use (hunting, logging, fishing)
- 1. Invasive & problematic species
- 1. Climate change & severe weather

Always assign a threat **scope** (% of population affected), **severity** (% of population declining per decade), and **timing** (past/ongoing/future).

-----

## Common Errors to Avoid

- Using common names as primary identifiers — always anchor to binomial
- Citing a review paper for a specific finding — go to the primary source
- Applying captive animal data to wild population conclusions without caveat
- Reporting *p* < 0.05 without effect size — significance ≠ biological importance
- Describing a clade as “primitive” or “advanced” — use **ancestral/derived** (plesiomorphic/apomorphic)
- Anthropomorphizing — describe behavior in operational terms, not mental state terms, unless specifically studying cognition with validated methods
- Ignoring taxonomic synonymies in literature searches — a species may have 3–5 names across decades of literature