---
name: ac-vrnn-trajectory-prediction-eval
description: Evaluates a model's ability to predict multi-modal future trajectories of agents given historical positions. It probes the model's capacity to capture social interactions, scene constraints, and long-term motion dynamics across diverse environments. Use when the user wants to benchmark on ETH, UCY, Stanford Drone Dataset (SDD), STATS SportVU NBA, Intersection Drone Dataset (inD), TrajNet++, or asks about evaluating this task. Reports TopK ADE, TopK FDE.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2005.08307
  bibtex_key: bertuglia2020acvrnn
  confidence: high
---

# ac-vrnn-trajectory-prediction-eval

> AC-VRNN: Attentive Conditional-VRNN for Multi-Future Trajectory Prediction — Bertuglia et al. (2020) (arXiv:2005.08307, 2020)

## What this evaluates

Evaluates a model's ability to predict multi-modal future trajectories of agents given historical positions. It probes the model's capacity to capture social interactions, scene constraints, and long-term motion dynamics across diverse environments.

## Datasets

- **ETH** — total ?; splits: train (-1), test (-1)
- **UCY** — total ?; splits: train (-1), test (-1)
- **Stanford Drone Dataset (SDD)** — total ?; splits: train (-1), val (-1), test (-1)
- **STATS SportVU NBA** — total ?; splits: train (-1), test (-1)
- **Intersection Drone Dataset (inD)** — total ?; splits: train (-1), val (-1), test (-1)
- **TrajNet++** — total ?; splits: train (-1), test (-1)

## Metrics

- `TopK ADE` **(primary)** — range: meters or feet
  - Average Euclidean distance over all predicted points and ground-truth positions. Computed on the single best-of-N sampled trajectory (lowest error).
- `TopK FDE` **(primary)** — range: meters or feet
  - Euclidean distance between the predicted and ground-truth final destination. Computed on the single best-of-N sampled trajectory.
- `Avg NLL` — range: other
  - Average negative log-likelihood of ground-truth trajectories over the prediction horizon, evaluated using a probability distribution fitted to the N predicted samples.
- `TopK Col-I` — range: percent
  - Percentage of predicted trajectories that collide with neighbors' predicted trajectories within a fixed radius. Evaluated on the best-of-N sample.
- `TopK Col-II` — range: percent
  - Percentage of predicted trajectories that collide with neighbors' ground-truth trajectories within a fixed radius. Evaluated on the best-of-N sample.

## Input / output format

**Input**: Historical trajectory sequences of the target agent and surrounding agents, represented as (x, y, [z]) coordinates over t_obs time steps. Context includes neighboring agents' positions and scene topology.

**Output**: N sampled future trajectory sequences for the target agent over t_pred time steps, each represented as a sequence of (x, y, [z]) coordinates.

## Scoring recipe

```python
def compute_topk_metrics(predictions, gold, k=1):
    # predictions: list of N trajectories, each (t_pred, 2/3)
    # gold: ground truth trajectory (t_pred, 2/3)
    errors = []
    for traj in predictions:
        ade = np.mean(np.linalg.norm(traj - gold, axis=1))
        fde = np.linalg.norm(traj[-1] - gold[-1])
        errors.append((ade, fde))
    errors.sort(key=lambda x: x[0])
    return errors[0][0], errors[0][1]

def compute_collisions(pred_traj, neighbors_pred, neighbors_gold, radius):
    col_i = np.any(np.linalg.norm(
        pred_traj[:, None, :] - neighbors_pred[None, :, :], axis=2) < radius)
    col_ii = np.any(np.linalg.norm(
        pred_traj[:, None, :] - neighbors_gold[None, :, :], axis=2) < radius)
    return col_i, col_ii
```

## Common pitfalls

- Must select the best-of-N trajectory (TopK) before computing ADE/FDE, not average over all N samples.
- Observation and prediction lengths vary significantly across datasets (e.g., 8/12 frames for ETH/UCY vs 10/40 for NBA).
- Collision metrics (Col-I/Col-II) require neighbor trajectories; Col-I uses predicted neighbors while Col-II uses ground truth neighbors.
- Units differ by dataset: meters for ETH/UCY/SDD/inD, feet for NBA.

## Evidence (verbatim from paper)

> TopK Average Displacement Error (TopK ADE): Average Euclidean distance over all estimated points and ground-truth positions of a trajectory as proposed in Pellegrini et al. (2009): ... The above metrics are evaluated using the top-k (or best-of-N) i.e., we sample N trajectories and consider the ADE and FDE of the lowest-error trajectory.

## Citation

```bibtex
@misc{bertuglia2020acvrnn,
  title={AC-VRNN: Attentive Conditional-VRNN for Multi-Future Trajectory Prediction},
  author={Bertuglia et al. (2020)},
  year={2020},
  note={arXiv:2005.08307}
}
```

- arXiv: 2005.08307
