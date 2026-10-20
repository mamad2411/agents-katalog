---
name: animint-rq1-eval
description: Evaluates Vision Language Models' ability to perceive and categorize basic UI animation types from short video clips. It probes motion perception and recognition of primitive visual effects like movement, rotation, scaling, color change, fading, blurring, and morphing. Use when the user wants to benchmark on AniMINT, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2604.26148
  bibtex_key: liang2026animint
  confidence: high
---

# animint-rq1-eval

> Beyond Screenshots: Evaluating VLMs' Understanding of UI Animations — Chen Liang et al. (2026) (arXiv:2604.26148, 2026)

## What this evaluates

Evaluates Vision Language Models' ability to perceive and categorize basic UI animation types from short video clips. It probes motion perception and recognition of primitive visual effects like movement, rotation, scaling, color change, fading, blurring, and morphing.

## Datasets

- **AniMINT** — total 300; splits: test (-1); repo https://github.com/publicationacc/AniMINT

## Metrics

- `accuracy` **(primary)** — range: [0, 1]
  - Percentage of correctly identified animation types from the 7-option multiple-choice set.

## Input / output format

**Input**: A 3-second UI animation video clip sampled at 10 fps, paired with a multiple-choice prompt listing 7 animation types (A–G) with descriptions.

**Output**: First line: a single letter (A–G) indicating the chosen animation type. Second line: a textual explanation.

## Scoring recipe

```python
def compute_accuracy(predictions, gold_labels):
    correct = 0
    for pred, gold in zip(predictions, gold_labels):
        pred_label = pred.split('\n')[0].strip().upper()
        if pred_label == gold:
            correct += 1
    return correct / len(predictions)
```

## Common pitfalls

- Models may be biased by option ordering, requiring randomization across runs to ensure fair comparison.
- Scoring must strictly parse the first line for the label, ignoring the generated explanation.
- Fixed clip duration (3s) and sampling rate (10 fps) are critical; varying them changes task difficulty.

## Evidence (verbatim from paper)

> > You are given a sequence of frames, uniformly sampled at 10 frames per second from a video of an animation.  
> 
> Task:  
> Identify which single animation type best matches the video you observe.  
> 
> Options:
> 
> 1. A.
> 
> Move (object moves in any direction)
> 
> 2. B.
> 
> Rotate (object rotates along any axis)
> 
> 3. C.
> 
> Size (object changes sizes along any axis)
> 
> 4. D.
> 
> Color (object changes in hue, saturation, or brightness)
> 
> 5. E.
> 
> Fade (object change in transparency/opacity)
> 
> 6. F.
> 
> Blur (object change in sharpness or clarity)
> 
> 7. G.
> 
> Morph (object transformation from one shape/form to another)
> 
> 
> Output format:  
> First line: the single letter (A to G) that corresponds to the animation type.
> Second line: an explanation of why this animation type matches the video.

## Citation

```bibtex
@misc{liang2026animint,
  title={Beyond Screenshots: Evaluating VLMs' Understanding of UI Animations},
  author={Chen Liang et al. (2026)},
  year={2026},
  note={arXiv:2604.26148}
}
```

- arXiv: 2604.26148
