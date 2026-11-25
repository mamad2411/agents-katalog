---
name: ml-six-key-lines
description: The six lines of code that carry six machine-learning algorithms, from the "Machine Learning from Scratch" part 23 video (linear regression, decision tree, random forest, gradient boosting, k-means, a 2-2-1 neural network), each with what the line does and a runnable numpy script that wraps the fragments in working context and checks they learn. Use when teaching or revising the basics of these algorithms, when someone asks what a line like `g = d.argmin(1)` or `p += .01 * grow()` means, or when a runnable minimal example of each is needed.
---

# Six ML algorithms in six key lines

Source: an 88-second video, part 23 of a "Machine Learning from Scratch" series (the handle on screen is @machinelearningtogo). It has no spoken explanation I could read; the content below is from the frames. The video itself says the full episodes are parts 1, 2, 3, 17, 18, 20 and 22.

**The lines are fragments, not a program.** They use names the video never defines (`grow`, `rng`, `d`, `C`, `X`, `t`, `f`, `i`, `sig`). `scripts/ml_six_key_lines.py` supplies the smallest context for each and asserts that it learns. Run it with `python3 scripts/ml_six_key_lines.py` (needs numpy).

| # | Part | Line as shown | What it does |
|---|---|---|---|
| 1 | Linear regression | `pred = w * x + b` | A straight line: slope times input plus offset. Training nudges `w` and `b` to shrink the error |
| 2 | Decision tree (18) | `L = X[i, f] > t` | One yes/no question: is feature `f` of row `i` above threshold `t`? The tree keeps the cut that separates the classes best |
| 3 | Random forest (20) | `V = np.sum([[*map(grow(rng.choice(400, 400)), X)] for _ in range(100)], 0)` | Grow 100 trees, each on `rng.choice(400, 400)` (400 rows drawn with replacement), let every tree vote on every row, add up the votes |
| 4 | Gradient boosting (22) | `for k in range(200): p += .01 * grow()` | 200 small trees, each fitted to what is still wrong; add 1% of each tree's answer to the running prediction |
| 5 | K-means (17) | `g = d.argmin(1)` then `for j in range(k): C[j] = X[g == j].mean(0)` | Assign each point to its nearest centre, then move each centre to the mean of its points; repeat |
| 6 | Neural network (3) | `a = sig(w[0]*x0 + w[1]*x1 + w[2])`, `b = ...`, `p = sig(w[6]*a + w[7]*b + w[8])` | Two hidden neurons feed one output neuron: nine weights in total |

## What the runnable version shows

Result of the last run (seeded, so repeatable):

| Algorithm | Check | Result |
|---|---|---|
| Linear regression | recover slope 2.5, offset 1.0 | 2.51 and 0.92 |
| Decision tree | one question on a 2-feature toy set | 0.73 accuracy |
| Random forest | 100 single-split trees, majority vote | 0.82 accuracy |
| Gradient boosting | 200 rounds at 0.01 | 0.86 accuracy |
| K-means | find three known blobs | centres within 0.5 of truth |
| Neural network | learn XOR, impossible without the hidden layer | outputs 0.01, 0.99, 0.99, 0.01 |

## Things the video does not say

- **[Certain] The trees here are single-split stumps** to keep each section small; real trees go deeper, so these accuracy figures say nothing about real-world performance.
- **[Certain] K-means can fail from a bad start.** With one random start, two centres landed in the same blob and the check failed; the script restarts 10 times and keeps the lowest error. The "round 1 / 9" in the video hides this.
- **[Certain] A 2-2-1 network can get stuck on XOR** for some random seeds; the script uses one that converges and asserts it.
- **[Likely] The forest line sums votes**, so a row is "yes" when the sum is at least 50 of 100.
