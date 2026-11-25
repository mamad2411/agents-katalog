# Clinical NLP

Information extraction from clinical free text. Covers note parsing and sectioning, biomedical named entity recognition, concept normalization to UMLS and ICD-10, assertion and negation detection, temporal relation extraction, adverse event identification, and de-identification. Written for public and credentialed research corpora, not for live patient records.

## When to Use This Skill

Activate when the user requests:
- Entity extraction from clinical notes, discharge summaries, or pathology reports
- scispaCy, medspaCy, cTAKES, MedCAT, or QuickUMLS pipelines
- Concept normalization to UMLS CUIs, SNOMED CT, RxNorm, or ICD-10
- Negation, uncertainty, or family-history assertion detection
- Adverse event or medication extraction from narrative text
- Temporal relation extraction from notes
- De-identification of clinical text
- Choosing between a rule-based pipeline and a clinical transformer

## Inputs

| Data Type | Format | Source |
|-----------|--------|--------|
| Clinical notes | Plain text, one note per record | MIMIC-IV-Note, n2c2 (both credentialed) |
| Annotated corpora | BRAT `.ann`, BioC XML, CoNLL | n2c2, BC5CDR, NCBI-Disease, MedMentions |
| Terminology | UMLS Metathesaurus (RRF) | NLM, licence required |
| Biomedical abstracts | PubMed XML | E-utilities, unrestricted |

---

## Before Any Code: The Access Question

```
Clinical text is not like expression data. The corpus decides what you can do.

  PubMed abstracts        open. No agreement. Use freely.
  BC5CDR, NCBI-Disease    open annotated corpora. Good for benchmarking NER.
  MedMentions             open, UMLS-linked. Good for entity linking.
  MIMIC-IV-Note           PhysioNet credentialed: CITI training + signed DUA.
                          Cannot be redistributed, posted, or pasted into a
                          hosted LLM API. The DUA prohibits it.
  n2c2 (formerly i2b2)    separate DUA through the hosting institution.
  UMLS Metathesaurus      free but licensed. Required by QuickUMLS, MedCAT
                          and the scispaCy UMLS linker. You must accept the
                          licence and download it yourself; no package ships it.

Two consequences that catch people:
  - Sending credentialed note text to an external API is a DUA breach, not a
    grey area. Run models locally on that text.
  - Never commit note text, even "de-identified" text, to a repository.
    De-identification is imperfect (below), and the DUA governs regardless.

Develop on the open corpora. Move to credentialed data only inside the
environment the DUA allows.
```

---

## Environment

Versions verified 2026-08.

```bash
pip install scispacy==0.6.2      # NER + UMLS linking, biomedical
pip install medspacy==1.3.1      # assertion, sectioning, clinical rules
pip install medcat==2.8.6        # supervised concept recognition + linking
pip install presidio-analyzer==2.2.364 presidio-anonymizer==2.2.364
```

```
DEPENDENCY CONFLICTS. These are real and will bite.

scispacy 0.6.2 requires:  spacy>=3.7,<3.9   numpy<2.0   python<3.13
medspacy 1.3.1 requires:  spacy<3.8         (on python < 3.12)
                          spacy>=3.8,<4.0   (on python >= 3.12)
negspacy 1.1.0 requires:  spacy>=3.8,<4.0   python>=3.10

  numpy<2.0 is the hard one. The rest of the scientific stack has moved to
  numpy 2.x, so scispaCy will not co-install with a current scanpy or
  pandas build. Give it its own virtual environment. Do not downgrade numpy
  in a shared environment to make it fit.

  scispaCy + medspaCy on python < 3.12 leaves exactly spacy 3.7.x as the
  only satisfying version. On python >= 3.12 it is 3.8.x. Pick the Python
  version deliberately rather than discovering this through a resolver error.

  negspacy and medspacy cannot coexist on python < 3.12 (one needs spacy
  >= 3.8, the other < 3.8). Use medspaCy's ConText; it supersedes negspacy
  for clinical text anyway.
```

### scispaCy models are not on PyPI

```bash
# The model version is NOT the package version. scispaCy is 0.6.2; the
# published models stop at 0.5.4. Building the URL from the package version
# gives a 404.
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_core_sci_sm-0.5.4.tar.gz
```

| Model | Use |
|---|---|
| `en_core_sci_sm` | fast general biomedical, development |
| `en_core_sci_md` | adds word vectors |
| `en_core_sci_lg` | larger vocabulary |
| `en_core_sci_scibert` | best accuracy, needs a GPU to be practical |
| `en_ner_bc5cdr_md` | chemicals and diseases only |
| `en_ner_bionlp13cg_md` | cancer genetics entity types |

`en_core_sci_*` finds *entity spans* without typing them. If you need typed entities (DISEASE vs CHEMICAL), add one of the `en_ner_*` models as a second pipeline; they are trained on different corpora and their labels do not merge automatically.

---

## Sectioning First

Clinical notes are not prose. A discharge summary contains a past medical history, a family history, an allergy list, and an assessment, and the same string means different things in each.

```python
import medspacy
nlp = medspacy.load()                    # pyrush sentencizer + target matcher + ConText
nlp.add_pipe("medspacy_sectionizer")

doc = nlp("Family History: colon cancer. Assessment: no evidence of colon cancer.")
for ent in doc.ents:
    print(ent.text, ent._.section_category)
```

```
Why this comes first: "colon cancer" under Family History is not a patient
diagnosis. A pipeline that extracts entities without section context will
report family history as active disease, and the error is invisible in
aggregate counts. Section first, then filter.
```

## Assertion and Negation

The single largest error source in clinical NLP. Most mentions of a disease in a note are *not* assertions that the patient has it.

```python
# medspacy.load() includes ConText by default; it sets five span attributes.
# Which trigger fires which attribute is not obvious - these are measured:
#   is_negated      "no evidence of pneumonia", "denies", "cannot exclude"
#   is_family       "mother had", "sister has", "family history of"
#   is_historical   "history of", "family history of" (sets family too)
#   is_hypothetical "if the patient develops sepsis", "return if fever"
#   is_uncertain    "will rule out sepsis", "suspicious for", "possible"
#
# "rule out X" is UNCERTAIN, not hypothetical. Only an if-construction
# makes it hypothetical. Getting this backwards mislabels every deferred
# diagnosis in a cohort.
for ent in doc.ents:
    print(ent.text, ent._.is_negated, ent._.is_family,
          ent._.is_historical, ent._.is_hypothetical, ent._.is_uncertain)
```

```
The five attributes ConText sets are is_negated, is_family, is_historical,
is_hypothetical and is_uncertain. Checking only is_negated is the common
half-fix: it catches "no pneumonia" and misses "mother had breast cancer"
and "if the patient develops sepsis".

Treat an entity as an active patient finding only when all five are False.
Write that as one predicate and reuse it, rather than checking flags
ad hoc at each call site.
```

```python
def is_active_finding(ent) -> bool:
    return not (ent._.is_negated or ent._.is_family or ent._.is_historical
                or ent._.is_hypothetical or ent._.is_uncertain)
```

ConText is a rule system (an implementation of the ConText algorithm, itself an extension of NegEx). It fails on constructions its rules do not cover — long-range scope, unusual phrasing, tables. A clinical transformer fine-tuned for assertion beats it on hard cases; ConText wins on transparency, speed, and needing no labelled data.

Two gaps worth knowing, both measured against medspaCy 1.3.1 defaults:

```
"Patient at risk for stroke."   -> all five attributes False
"Status post MI in 2019."       -> all five attributes False
```

A risk statement is not a diagnosis, and "status post" is by definition
historical, but neither phrasing is in the default rule set, so both are
reported as active findings. Add target-specific rules for the phrasings your
corpus actually uses, and audit a sample by hand before trusting the counts.
The failure is silent: nothing errors, the entity simply looks active.

## Concept Normalization

Extracting the string "MI" is not extraction. Normalizing it to a concept is.

```python
import spacy
nlp = spacy.load("en_core_sci_sm")
nlp.add_pipe("scispacy_linker",
             config={"resolve_abbreviations": True, "linker_name": "umls"})

linker = nlp.get_pipe("scispacy_linker")
doc = nlp("Patient with a history of MI.")
for ent in doc.ents:
    for cui, score in ent._.kb_ents[:3]:
        print(cui, score, linker.kb.cui_to_entity[cui].canonical_name)
```

```
linker_name has NO default (it is None in the signature). Omitting it does
not silently pick UMLS; construct the linker explicitly.

Available knowledge bases: umls, mesh, rxnorm, go, hpo. MeSH uses its own
identifiers, not CUIs, so a MeSH-linked pipeline will not join to a
CUI-keyed table.

Defaults worth knowing, from the EntityLinker signature:
  threshold=0.7   k=30   max_entities_per_mention=5
  resolve_abbreviations=True   filter_for_definitions=True

filter_for_definitions=True drops candidate concepts that have no definition
text. That silently removes valid but sparsely-documented concepts. If recall
matters more than precision, set it False and filter yourself.

kb_ents is a ranked list, not an answer. Taking [0] unconditionally accepts
whatever scored highest, including 0.71 on a garbage match. Apply your own
threshold, and keep the score in the output so downstream work can re-filter.
```

### Choosing a normalization tool

```
scispaCy linker    fast, no training, approximate string match to UMLS.
                   Good default. Weak on abbreviations and context-dependent
                   senses even with resolve_abbreviations.
MedCAT             self-supervised + optionally supervised. Better
                   disambiguation because it learns context. Needs UMLS or
                   SNOMED and a training step. v2 is a rewrite: code written
                   for v1.9.x does not run on 2.x.
QuickUMLS          approximate dictionary matching, simple and fast, but
                   1.4.2 dates from 2023. No assertion handling.
cTAKES             Java, Apache, actively maintained. Full clinical pipeline
                   with a long clinical track record. Heavier to deploy.
```

## ICD-10 Coding

```
Do not present automated ICD-10 output as billing codes.

Mapping a concept to a billable code depends on documentation rules,
specificity requirements, sequencing (primary vs secondary), and payer
policy that the note text alone does not determine. UMLS gives an ICD-10-CM
crosswalk, and that crosswalk is many-to-many.

State the output as candidate codes with the evidence span, ranked, for a
coder to adjudicate. That is a useful product. An unsupervised billing code
is a liability.
```

## Temporal Relations

```
The clinically important question is almost never "is this entity present"
but "when, relative to what".

  DocTime      is the event before, during, or after this note?
  Order        did the drug precede the event?

The i2b2 2012 temporal task and THYME framed this as TIMEX3 extraction plus
TLINK classification. Nothing rule-based does it well. If temporal ordering
drives your conclusion, use a fine-tuned model and report its agreement
against held-out annotation, not just its output.

A cheap and honest fallback: extract explicit dates and section context
only, and say the ordering is unresolved where no explicit date exists.
Silent guessing is worse than a stated gap.
```

## Adverse Events

```
Extracting a drug and a symptom from the same note is not an adverse event.
It is co-occurrence.

Minimum bar for a causal claim:
  - temporal order established (drug before event)
  - indication excluded (the symptom is not why the drug was given)
  - assertion checked (not negated, not family, not hypothetical)

The indication confound is the one most often missed: metformin and
hyperglycaemia co-occur constantly, and the direction is the opposite of an
adverse event. Filter against the drug's known indications before reporting
any signal.
```

## De-identification

```
HIPAA Safe Harbor removes 18 categories of identifier, including names,
all geography finer than state, all dates more specific than year (and any
age over 89), contact details, and record and device numbers.
Expert Determination is the alternative route and requires a qualified
person to certify a small re-identification risk.

Automated de-identification does not achieve either standard on its own.
Published systems report high recall, but Safe Harbor is a categorical
requirement, not a recall target: a note with one surviving name is not
de-identified. Automated tools are a first pass before human review, and
the DUA still governs the output.
```

```python
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

analyzer, anonymizer = AnalyzerEngine(), AnonymizerEngine()
text = "Patient Jane Roe, seen 2025-03-14, phone 555-0100."   # synthetic
results = analyzer.analyze(text=text, language="en")
print(anonymizer.anonymize(text=text, analyzer_results=results).text)
```

```
Tool status:
  presidio 2.2.364 (2026-07)  maintained, general-purpose PII, extensible
                              with custom clinical recognizers
  philter-ucsf 1.0.3          last released 2020-04-19. Built for clinical
                              notes and still cited, but unmaintained for
                              five years. Do not start new work on it;
                              use presidio with clinical recognizers added.

Presidio is not clinical out of the box. Provider names, MRNs, accession
numbers and institution names need custom recognizers. Test on annotated
data and report per-category recall, not one overall number, because the
categories fail unevenly.

Date shifting beats date removal for research use: shift every date in a
patient's record by the same random offset. Intervals survive, absolute
dates do not. Store the offset outside the corpus, or not at all.
```

## Rules or Transformers

```
Rule-based (medspaCy, cTAKES)
  + no labelled data, inspectable, deterministic, cheap
  + errors are fixable by editing a rule
  - brittle to phrasing outside the rules

Fine-tuned clinical transformer
  + better on varied phrasing and assertion
  - needs labelled data, GPU, and version discipline
  - errors are not individually fixable

Models, all ungated on HuggingFace:
  emilyalsentzer/Bio_ClinicalBERT   clinical notes (MIMIC-trained)
  dmis-lab/biobert-v1.1             biomedical literature
  microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract-fulltext
  UFNLP/gatortron-base              large clinical corpus
  stanford-crfm/BioMedLM            generative, biomedical

Bio_ClinicalBERT is trained on MIMIC notes. If you evaluate on MIMIC, your
test set overlaps its pretraining corpus, and the score is optimistic. Say
so, or evaluate on a different corpus.

transformers 5.x is a major version (5.15.0 current; last 4.x was 4.57.6).
Pin it. Examples written for 4.x may not run unchanged.

Start rule-based. It gives a baseline, an error analysis, and often enough
accuracy. Move to a transformer when the error analysis says phrasing
variety is the limit.
```

## Output Specification

| Output | Format | Description |
|--------|--------|-------------|
| `entities.csv` | CSV | note_id, span offsets, text, label, section |
| `assertions.csv` | CSV | the five ConText flags per entity |
| `normalized.csv` | CSV | entity, CUI, score, canonical name, KB used |
| `icd10_candidates.csv` | CSV | ranked candidate codes with evidence spans, marked for review |
| `deid_report.csv` | CSV | per-category recall against annotated data |
| `pipeline_versions.json` | JSON | package, model and KB versions pinned |

Keep character offsets on every entity. Without them a result cannot be traced back to its sentence, and no clinician will accept it.

## Validation Checks

```
Access
  Corpus licence identified before any code runs.
  Credentialed text never sent to an external API, never committed.

Pipeline
  Sectioning applied before entity filtering.
  All five assertion attributes checked, not is_negated alone.
  Entity offsets retained end to end.
  Linker constructed with an explicit linker_name.
  kb_ents thresholded, not indexed at [0].

Evaluation
  Scored against an annotated corpus, per entity type.
  Precision and recall reported separately; F1 alone hides which one failed.
  Pretraining overlap stated when evaluating a MIMIC-trained model on MIMIC.
  De-identification recall reported per identifier category.

Reproducibility
  spaCy, model, and KB versions pinned together. A model built for one
  spaCy minor version may load with a warning and behave differently.
```

## Common Pitfalls

### Access and privacy
1. **Pasting credentialed note text into a hosted API**: the PhysioNet and n2c2 DUAs prohibit redistribution, and an API call is redistribution. Run models locally on that text.
2. **Committing "de-identified" notes to a repository**: automated de-identification is imperfect and the DUA governs the derived text regardless. Keep note text out of version control entirely.
3. **Treating automated de-identification as Safe Harbor compliance**: Safe Harbor is categorical, so one surviving identifier fails it. Use automation as a first pass before human review.

### Installation
4. **Installing scispaCy into a shared scientific environment**: it pins `numpy<2.0` and `python<3.13`, which conflicts with a current stack. Give it a dedicated environment rather than downgrading numpy.
5. **Building the scispaCy model URL from the package version**: the package is 0.6.2, the models stop at 0.5.4, and the mismatched URL 404s. Model version and package version are independent.
6. **Installing medspaCy and negspacy together on Python < 3.12**: their spaCy pins are disjoint. Use medspaCy's ConText, which supersedes negspacy for clinical text.

### Extraction
7. **Reporting entities without section context**: "colon cancer" under Family History is not a patient diagnosis. Section first, then filter.
8. **Checking `is_negated` alone**: it misses family history, hypotheticals, and historical mentions. Require all five ConText attributes to be False before calling something an active finding.
9. **Assuming ConText's default rules cover your phrasing**: "Patient at risk for stroke" and "Status post MI in 2019" both come back with all five attributes False, so both read as active findings. The failure is silent. Audit a hand-labelled sample and add rules for your corpus's phrasings.
10. **Expecting typed entities from `en_core_sci_*`**: those models find spans without typing them. Add an `en_ner_*` model for types, and do not assume the label sets merge.
11. **Taking `kb_ents[0]` as the answer**: it is a ranked candidate list, and the top hit can score barely above threshold. Apply your own cutoff and keep the score.
12. **Omitting `linker_name`**: it has no default. The linker must be told which knowledge base to use, and MeSH identifiers are not CUIs.
13. **Leaving `filter_for_definitions=True` when recall matters**: it silently drops concepts that lack definition text.

### Interpretation
14. **Presenting automated ICD-10 output as billing codes**: coding depends on documentation and payer rules the text does not determine. Output ranked candidates with evidence spans for a coder.
15. **Calling drug–symptom co-occurrence an adverse event**: without temporal order and indication exclusion it is co-occurrence. Metformin and hyperglycaemia co-occur with the causality reversed.
16. **Evaluating a MIMIC-trained model on MIMIC**: Bio_ClinicalBERT was pretrained on those notes, so the test set overlaps pretraining. State the overlap or change corpus.
17. **Reporting F1 alone for extraction**: precision and recall fail for different reasons and need different fixes. Report both, per entity type.

## Related Skills

- [`variant-annotation`](../variant-annotation/SKILL.md): structured variant interpretation, where clinical text often supplies the phenotype
- [`meta-analysis`](../meta-analysis/SKILL.md): the same screening and extraction discipline applied to published literature
- [`survival-analysis`](../survival-analysis/SKILL.md): consumes outcomes and dates that clinical NLP extracts

## Public Datasets for Testing

| Dataset | Content | Access |
|---------|---------|--------|
| BC5CDR | Chemical and disease NER, PubMed abstracts | open |
| NCBI-Disease | Disease mention and normalization | open |
| MedMentions | UMLS-linked entities, PubMed abstracts | open |
| MIMIC-IV-Note | Deidentified hospital notes | PhysioNet credentialed + DUA |
| n2c2 / i2b2 | Assertion, temporal, medication tasks | DUA through the hosting institution |
| UMLS Metathesaurus | Terminology for linking | free licence, download required |
