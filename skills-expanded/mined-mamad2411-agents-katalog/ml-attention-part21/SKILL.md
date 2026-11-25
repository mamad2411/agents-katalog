---
name: ml-attention-part21
description: The Attention video, Machine Learning from Scratch part 21 (@machinelearningtogo) - the 16-line numpy script transcribed from the video, runnable with built-in checks, with a line-by-line explanation of query, key, value, match (scaled dot product), softmax and mix, using the sentence about the animal and the street. Use to learn or teach self-attention, or to reproduce the video's "it now" weights.
---

# Attention from scratch

Source: a 103-second video by @machinelearningtogo. Code in `scripts/attention_from_scratch.py`, transcribed from the final frame. Run: `python scripts/attention_from_scratch.py` (needs numpy). Checks at the bottom are mine and pass.

| Lines | Step | Plain meaning |
|---|---|---|
| 2 to 3 | words | The 10-word sentence, split |
| 4 to 7 | features `X` | Made-up 4-number descriptions (thing, alive, place, pronoun); unknown words get zeros |
| 8 to 10 | `Wq`, `Wk`, `Wv` | Hand-set matrices; in real models these are learned. `Wq` makes "it" ask for something alive |
| 11 | Q, K, V | Each word's query ("what am I looking for"), key ("what I offer"), value ("what I carry") |
| 12 | `S = Q @ K.T / sqrt(2)` | Match: how well each query fits each key, scaled |
| 13 | softmax | Turn matches into weights that add up to one |
| 14 | `new = A @ V` | Mix: each word becomes a weighted blend of values |
| 15 to 16 | print | Weights for "it" (index 7) and its new vector |

Result [Certain]: for "it", animal 0.85, street 0.05, every other word 0.01; new vector `[0.9 0.85 0.05 0.01]`. Matches the video's "animal 85%, street 5%".

## Limits

Real models learn the matrices from data, use many heads and hundreds of dimensions, and apply a causal mask so a word cannot see later words (mentioned in the video). The features here are invented to make the arithmetic readable. Use `/attention-explain`.
