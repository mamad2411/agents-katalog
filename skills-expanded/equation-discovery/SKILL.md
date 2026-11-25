---
name: equation-discovery
description: Discover interpretable equations from engineering or scientific data with the LLM-SR loop — you propose physically motivated equation skeletons as Python functions with free constants, the script fits the constants (BFGS, multi-start, sandboxed), scores train / in-domain / out-of-domain NMSE, keeps an experience buffer and builds the next prompt from the best programs; Pareto front of complexity vs error and polynomial baselines included. Based on LLM-SR (ICLR 2025 Oral) and LLM-SRBench (ICML 2025), Barati Farimani Lab with Reddy group. Use for constitutive laws, empirical correlations, process models, or "find an equation that fits this data and extrapolates".
---

# Equation discovery (LLM-SR)

LLM-SR (Shojaee et al., ICLR 2025 Oral) found that LLMs discover better equations by **writing
programs**: equation skeletons with free constants that an optimizer fits. Fitted scores flow back
into the next prompt. Prior knowledge (elasticity, saturation, Arrhenius, damping) drives the
proposals, and the data decides.

Here **you** are the LLM. `scripts/eqdisc.py` is the evaluator and the experience buffer. It needs
numpy, scipy and pandas; scikit-learn is used for the baselines. The method map and a worked
rehearsal are in `references/paper-notes.md`.

## Workflow
1. **Set up the problem.**
   ```bash
   python scripts/eqdisc.py init --dir run/ --train train.csv --test-id id.csv --test-ood ood.csv \
       --target stress --inputs strain,temp --desc "stress in an Al rod vs strain and temperature"
   python scripts/eqdisc.py fetch --problem stressstrain --dir run/        # or an LLM-SR benchmark
   ```
   - `--test-id` is the **validation** split used for feedback and selection. `--test-ood` is the
     **final test**: it is stored but hidden from `eval`, `prompt`, `top` and `pareto` until you run
     `final` once on the frozen equation.
   - Say what the final split tests. LLM-SR's stress–strain set holds out one temperature (0.667)
     inside the training range (0.067–1.0): that is interpolation to an unseen condition, not
     extrapolation. To test extrapolation, hold out the highest temperature, load or speed range.
2. **Get the baselines** with `baseline --dir run/` (linear, cubic polynomial, sparse cubic). They
   set the error and extrapolation bar.
3. **Loop for about 5–20 proposals:**
   - Run `prompt --dir run/` to get the spec and the best programs so far, worst first.
   - Look at the data (plot slices; check limits, signs, monotonicity), then write the next
     skeleton as `def equation(<inputs>, params): return ...` using `np` only, with at most 10
     params.
   - Score it: `eval --dir run/ --src '...'` (or `--file skel.py`) `--note "why this form"`.
   - Change one idea at a time and say why: add a term for a missed regime, make a coefficient
     temperature-dependent, swap a polynomial for a saturating form.
   - Guard domains: `np.abs` before fractional powers, `np.exp` with bounded arguments, no division
     by inputs that cross zero.
4. **Choose** with `pareto --dir run/ --out front.png`:
   - Prefer the **simplest** program on the train Pareto front whose **validation** error is low.
   - A small gain in train NMSE bought with five more params is usually overfitting.
5. **Report:**
   - the equation with fitted constants (`top --k 1` gives `params`, indexed as `params_used`);
   - NMSE on train and validation, then `final --id N` for the final-test NMSE (run once, after
     freezing the equation);
   - the physical reading of each term;
   - what it can't explain.

## Rules
- The data decides. Don't keep a term because it "should" be there if the fit doesn't need it, and
  say when a known law fails.
- Skeletons run in an isolated subprocess (`python -I`) with numpy only, no imports, IO or dunder
  access, and a time limit. Still, keep them to plain math.
- For benchmarking against LLM-SRBench, use its data and evaluation code
  (github.com/deep-symbolic-mathematics/llm-srbench). Report NMSE and symbolic accuracy the way
  that benchmark defines them.

Cite: Shojaee et al., *LLM-SR*, ICLR 2025 (arXiv:2404.18400); Shojaee et al., *LLM-SRBench*, ICML 2025 (arXiv:2504.10415).
