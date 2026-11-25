---
name: llm-mechanical-designer
description: Designs and optimizes 2-D trusses with an LLM-in-the-loop FEM workflow (Jadhav & Barati Farimani, "Large Language Model Agent as a Mechanical Designer") — the agent proposes nodes, members and discrete cross-sections, an exact truss FEM scores each design, and ranked history plus optimize/constraint prompts drive iterative refinement. Use when the user wants a truss or frame layout designed, wants to minimize stress, mass or stress-to-weight under constraints, or asks to reproduce the paper's tasks.
---

# LLM Agent as a Mechanical Designer (truss design loop)

Paper: Y. Jadhav, A. Barati Farimani, *Large Language Model Agent as a Mechanical Designer*, J. Engineering Design (2026), arXiv:2404.17525. Reference code: github.com/BaratiLab/LLLM-Agent-Mechanical-Designer. **You are the LLM in the loop.** The FEM is code (`scripts/truss_fem.py`), and its stresses match the paper's reference code to 1e-4.

## When to use
- "Design a truss that carries X with max stress Y and mass under Z."
- "Minimize the stress-to-weight ratio of this bracket truss."
- Reproducing or teaching Task 1 / Task 2 from the paper (`t1v1`–`t1v3`, `t2v1`–`t2v3`).
- Any 2-D pin-jointed structure with discrete section sizes. Write the task as JSON with the same keys as `scripts/tasks.py` and pass `--custom-task task.json`.

## Workflow
1. **Start a run.**
   ```bash
   python scripts/design_loop.py init --task t1v1 --run runs/t1v1
   ```
   This writes `runs/t1v1/prompt_next.md` (the INITIAL prompt).
2. **Answer the prompt yourself.** Work through the scratchpad sections in order (they're there so the geometry reasoning happens before the numbers), then save only the JSON block to `design.json`. Keep fixed nodes exactly where they are, and use area IDs from the table.
3. **Evaluate. Never estimate stresses yourself.**
   ```bash
   python scripts/design_loop.py eval --run runs/t1v1 design.json
   ```
   The output gives the FEM result, the critical members, the ranked history, and `mode_next`: OPTIMIZE if the design is feasible, CONSTRAINT if not. It also writes the next prompt.
4. **Repeat steps 2–3** using `prompt_next.md`. Change a few things per iteration. In OPTIMIZE mode, set `"stop": true` once improvements fall below about 2%; stopping is refused while the design is infeasible. The budget is 25 iterations.
5. **Report.**
   ```bash
   python scripts/design_loop.py best --run runs/t1v1     # best_design.json + best.png
   ```
   Report the best design table (nodes, members, area IDs, member stresses), max |σ|, mass, and SWR against the limits, the number of iterations and FEM calls, and the plot. A good comparison point from the paper: the LLM loop needed tens of FEM calls, where NSGA-II used 500 generations × 100 population.

## Design heuristics the paper's best runs used
- Deepen the truss over the load node; raising an apex cuts chord forces.
- Put a direct diagonal from the load node to each support.
- Size by force: big areas on the 2–3 critical members, IDs 1–2 elsewhere.
- Fewer members is often better. Minimal triangulated layouts sat on the low-mass Pareto edge.
- Keep coordinates simple (two decimals), since LLMs are weak at fine floating-point tuning. Refine positions in small, deliberate steps.

## Conventions (identical to the reference code)
Load `[m, a]` → Fx = m·cos a, Fy = m·sin a (so `[-10, -45]` points up-left). A pinned support fixes x and y; a roller fixes y. Stress is axial, tension positive, with E = 29.6e6. Mass = Σ L·A(area id). Units follow the paper ("Pa", "m").

## Limits
2-D, linear-elastic, pin-jointed. No buckling check: add an Euler check for compression members if the user needs one (P_cr = π²EI/L²). The prompt templates are re-written from the paper's structure, not copied verbatim.
