---
name: gdm-science-bundle
description: >
  Vendor of the google-deepmind/science-skills bundle (37 skills for scientific
  research). Use when a user asks about any of: AlphaGenome single-variant
  effect analysis (RNA-seq / DNase / ChIP / TF effects, splicing disruption,
  UBERON/CL ontology resolution for non-coding variants), AlphaFold DB fetch
  and analyze, ChEMBL bioactivity queries, ClinicalTrials.gov lookups,
  ClinVar variant interpretation, dbSNP, EMBL-EBI Ontology Lookup Service
  (OLS4), ENCODE cCREs, Ensembl REST, Foldseek structural search, gnomAD,
  GTEx, Human Protein Atlas, InterPro, JASPAR transcription-factor profiles,
  literature search (arXiv / bioRxiv / EuropePMC / OpenAlex), NCBI sequence
  fetch (EFetch), openFDA, OpenTargets, PDB, protein sequence MSA / similarity
  search, PubChem, PubMed, PyMOL structural visualization, QuickGO, Reactome,
  STRING, UCSC conservation & TFBS, UniBind, UniProt, or any workflow
  combining them. Always read the per-skill SKILL.md under skills/<name>/ and
  invoke Python only through `uv run`.
---

# GDM Science Bundle (vendored)

A vendored copy of the [google-deepmind/science-skills](https://github.com/google-deepmind/science-skills)
bundle (pin: see `UPSTREAM_PIN.txt`). This directory is the long-tail fallback:
**for the 5 sub-plugins with first-class zorai support (alphagenome, alphafold,
uniprot, clinvar, chembl) prefer the matching `plugins/zorai-plugin-science/`
sub-plugin for typed settings and structured responses**. For every other
sub-skill in this bundle, follow the workflow below.

## How to use a sub-skill in this bundle

1. **Read the skill's `SKILL.md` first.** Layout:
   `skills/<skill_dir>/SKILL.md` — the file's YAML frontmatter is the routing
   contract; the markdown body is the full workflow with steps, error fixes,
   and report templates. Never skip this read.
2. **Invoke Python only through `uv run`.** The deepmind scripts use PEP 723
   inline `# /// script ... # ///` blocks, so `uv run` will resolve and
   install the right deps in an isolated cache (`~/.cache/uv/`). Never use
   bare `python3` or `pip install`.
3. **Read each skill's Prerequisites before running.** Most skills need
   `uv` on PATH (zorai runtime has it), a `~/.env` file with the relevant
   API key, and possibly a notification step that records the skill was used.
4. **Never read, `cat`, `echo`, `printenv`, or `os.environ.get` the `.env`
   file or its keys.** Deepmind scripts load credentials via `dotenv` inside
   the script — they pull keys from disk but do not surface them in the
   agent's context. Keep it that way.
5. **When running in zorai's sandbox**, credential injection is handled by
   the plugin settings system (see `zorai_plugin_science` sub-plugins);
   for the long-tail skills here, use `dotenv`'s normal on-disk load.

## Inventory of sub-skills in this bundle

| Sub-skill (kebab-case) | Path under this bundle | Notes |
|---|---|---|
| `alphafold-database-fetch-and-analyze` | `skills/alphafold_database_fetch_and_analyze/` | Compute, also has a zorai sub-plugin. |
| `alphagenome-single-variant-analysis` | `skills/alphagenome_single_variant_analysis/` | Compute + API key, also has a zorai sub-plugin. |
| `chembl-database` | `skills/chembl_database/` | REST, also has a zorai sub-plugin. |
| `clinical-trials-database` | `skills/clinical_trials_database/` | REST. |
| `clinvar-database` | `skills/clinvar_database/` | REST, also has a zorai sub-plugin. |
| `dbsnp-database` | `skills/dbsnp_database/` | REST (NCBI EFetch). |
| `embl-ebi-ols` | `skills/embl_ebi_ols/` | REST (OLS4). |
| `encode-ccres-database` | `skills/encode_ccres_database/` | REST. |
| `ensembl-database` | `skills/ensembl_database/` | REST. |
| `foldseek-structural-search` | `skills/foldseek_structural_search/` | Compute (Foldseek binary). |
| `gnomad-database` | `skills/gnomad_database/` | REST. |
| `gtex-database` | `skills/gtex_database/` | REST. |
| `human-protein-atlas-database` | `skills/human_protein_atlas_database/` | REST. |
| `interpro-database` | `skills/interpro_database/` | REST. |
| `jaspar-database` | `skills/jaspar_database/` | REST. |
| `literature-search-arxiv` | `skills/literature_search_arxiv/` | REST. |
| `literature-search-biorxiv` | `skills/literature_search_biorxiv/` | REST. |
| `literature-search-europepmc` | `skills/literature_search_europepmc/` | REST. |
| `literature-search-openalex` | `skills/literature_search_openalex/` | REST (key optional). |
| `ncbi-sequence-fetch` | `skills/ncbi_sequence_fetch/` | REST (EFetch). |
| `openfda-database` | `skills/openfda_database/` | REST. |
| `opentargets-database` | `skills/opentargets_database/` | REST (GraphQL). |
| `pdb-database` | `skills/pdb_database/` | REST. |
| `protein-sequence-msa` | `skills/protein_sequence_msa/` | Compute. |
| `protein-sequence-similarity-search` | `skills/protein_sequence_similarity_search/` | Compute. |
| `pubchem-database` | `skills/pubchem_database/` | REST. |
| `pubmed-database` | `skills/pubmed_database/` | REST. |
| `pymol` | `skills/pymol/` | Compute (PyMOL binary). |
| `quickgo-database` | `skills/quickgo_database/` | REST. |
| `reactome-database` | `skills/reactome_database/` | REST. |
| `string-database` | `skills/string_database/` | REST. |
| `ucsc-conservation-and-tfbs` | `skills/ucsc_conservation_and_tfbs/` | REST. |
| `unibind-database` | `skills/unibind_database/` | REST. |
| `uniprot-database` | `skills/uniprot_database/` | REST, also has a zorai sub-plugin. |
| `uv` | `skills/uv/` | **Internal.** Sets up `uv`. zorai runtime already provides it. |
| `scienceskillscommon` | `skills/scienceskillscommon/` | **Internal.** Shared helpers for other skills. Do not invoke directly. |
| `workflow-skill-creator` | `skills/workflow_skill_creator/` | **Meta-skill.** Skip; the agent does not need to author new skills mid-task. |

## Shared runtime rules

- All scripts expect to be run from the **skill directory** (or with `--project $SKILL_DIR` for ad-hoc). The skill's own `SKILL.md` will tell you which.
- Output artifacts should go under the **user's working directory** (or the path the user specifies). Do not pollute `skills/`.
- Confirm with the user before invoking anything with a real cost or rate limit
  (AlphaGenome API calls, OpenAlex bulk pulls, Foldseek server queries, etc.).
- If a sub-skill's `SKILL.md` says to record a `LICENSE_NOTIFICATION.txt` in
  the skill directory, **skip the file write** when running through zorai
  (the bundle is read-only inside the repo); instead, mention the upstream
  license URL to the user once per session.

## License & attribution

- **Code in this bundle** — Apache License 2.0 (see `LICENSE`).
- **Documentation in this bundle** — Creative Commons Attribution 4.0
  International (CC-BY-4.0).
- **Individual database providers have their own terms.** See
  `SKILL_LICENSES.md` for the full list. You are responsible for ensuring
  that any data retrieved through these skills is used in compliance with
  the upstream provider's terms.
- **Upstream repo**: https://github.com/google-deepmind/science-skills
- **Pin**: see `UPSTREAM_PIN.txt` for the exact commit hash this bundle was
  vendored at. To refresh, re-vendor at a newer commit and update the pin.
