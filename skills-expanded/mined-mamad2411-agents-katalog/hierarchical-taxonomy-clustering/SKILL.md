---
skillx:
  name: hierarchical-taxonomy-clustering
  purpose: Build a unified multi-level taxonomy from multi-source hierarchical category paths using weighted hierarchical representations, recursive clustering, and representative naming.
  scope_in:
    - merge category-path data from multiple sources into one shared bounded-depth taxonomy
    - produce both record-level assignments and a deduplicated hierarchy view
    - enforce structural naming quality (not only embedding similarity)
  scope_out:
    - not for single-source cleaning where no cross-source merge is needed
    - not for direct mapping into a fixed pre-defined taxonomy with known labels
    - not for open-ended ontology invention without concrete path inputs
  requires:
    - hierarchical category-path text (or equivalent fields that can be normalized into paths)
    - ability to compute text embeddings and run hierarchical/recursive clustering
    - enough runtime/memory for dataset scale
  preferred_tools:
    - pandas
    - sentence-transformers
    - scipy clustering
    - nltk or equivalent normalization tooling
  risks:
    - overcommitting to one parameter set despite poor fit
    - hidden assumption failures in path quality or depth consistency
    - ancestor/descendant naming collisions and sibling ambiguity
    - source imbalance that lets one platform dominate the unified taxonomy
    - producing tidy clusters that fail representativeness/usability constraints
  examples:
    - input: merge Amazon/Facebook/Google Shopping category paths into a five-level unified taxonomy.
      expected_behavior: normalize paths, build weighted hierarchical representations, cluster recursively, generate non-colliding names, and export both full assignments and hierarchy outputs.
---

# Decision Rule

Use this skill when the task is explicitly a **multi-source taxonomy merge** with hierarchical paths.
Before committing, verify:
1. inputs can be normalized into comparable path segments,
2. output depth and deliverables are clear,
3. clustering-based merge is acceptable.

If any are unclear, ask clarifying questions before running a full pipeline.

# Assumptions to Surface

State assumptions explicitly (do not hide them in implementation):
- path delimiters and text noise can be normalized reliably,
- higher levels should usually carry more weight than deeper levels,
- recursive per-level clustering is more appropriate than one flat global clustering,
- cluster labels should be representative and human-usable, not only frequent tokens.

If an assumption is weak for this dataset, branch to a lighter or adjusted variant and say why.

# Minimal Execution Contract

Keep the core pipeline, but treat detailed parameter values as tunable:
1. **Normalize**: standardize delimiters, clean text, harmonize depth handling, deduplicate.
2. **Represent**: build hierarchical text representations and apply level-aware weighting.
3. **Cluster recursively**: assign categories level by level rather than a single flat pass.
4. **Name clusters**: derive representative names; avoid ancestor duplication and sibling collisions.
5. **Export**: provide both full record assignments and a unique hierarchy table.

Do not imply that one exact weight schedule, cluster count range, or linkage option is universally mandatory.

# Branch / Abstention Discipline

- If path quality is too inconsistent to support meaningful recursive clustering, pause and request data cleanup constraints.
- If output depth/quality criteria are unspecified, ask for target depth and acceptance thresholds.
- If runtime constraints make full recursion infeasible, propose and label a bounded approximation (e.g., reduced depth or sampled tuning) before execution.
- If a simpler baseline is better aligned (e.g., fixed-taxonomy mapping task), abstain from this methodology and switch.

# Anti-Patterns

- Forcing full methodology when fit conditions are not met.
- Presenting guessed assumptions as facts.
- Optimizing only intrinsic clustering neatness while ignoring naming clarity and taxonomy usability.
- Copying heavy reference choices verbatim without checking dataset/task fit.

# Acceptance

A good run should show:
- method applied only after fit checks,
- assumptions stated and resolved or explicitly left open,
- outputs include both assignment-level and hierarchy-level artifacts,
- naming/structure constraints reviewed (ancestor duplication, sibling distinctness, representativeness),
- branch/abstain behavior used when prerequisites fail.