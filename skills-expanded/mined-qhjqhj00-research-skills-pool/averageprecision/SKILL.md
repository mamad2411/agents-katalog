---
name: averageprecision
description: Compute the AveragePrecision metric — provided by torchmetrics. Use when the user has predictions and ground-truth and needs to compute AveragePrecision, or asks how to score with AveragePrecision.
metadata:
  skill_kind: metric
  source_lib: torchmetrics
  import_path: torchmetrics.AveragePrecision
  source: library_introspection
---

# averageprecision

> Metric `AveragePrecision` from `torchmetrics` (torchmetrics.AveragePrecision)

## When to invoke this skill

The user has predictions + ground truth and asks to evaluate with AveragePrecision, or
mentions `torchmetrics.AveragePrecision` directly, or wants the standard torchmetrics implementation.

## Reference signature

```python
from torchmetrics import AveragePrecision

# AveragePrecision(task: Literal['binary', 'multiclass', 'multilabel'], thresholds: Union[int, list[float], torch.Tensor, NoneType] = None, num_classes: Optional[int] = None, num_labels: Optional[int] = None, average: Optional[Literal['macro', 'weighted', 'none']] = 'macro', ignore_index: Optional[int] = None, validate_args: bool = True, **kwargs: Any) -> torchmetrics.metric.Metric
```

## Library docstring

```
Compute the average precision (AP) score.

The AP score summarizes a precision-recall curve as an weighted mean of precisions at each threshold, with the
difference in recall from the previous threshold as weight:

.. math::
    AP = \sum_{n} (R_n - R_{n-1}) P_n

where :math:`P_n, R_n` is the respective precision and recall at threshold index :math:`n`. This value is
equivalent to the area under the precision-recall curve (AUPRC).

This function is a simple wrapper to get the task specific versions of this metric, which is done by setting the
``task`` argument to either ``'binary'``, ``'multiclass'`` or ``'multilabel'``. See the documentation of
:class:`~torchmetrics.classification.BinaryAveragePrecision`,
:class:`~torchmetrics.classification.MulticlassAveragePrecision` and
:class:`~torchmetrics.classification.MultilabelAveragePrecision` for the specific details of each argument
influence and examples.

Legacy Example:
    >>> from torch import tensor
    >>> pred = tensor([0, 0.1, 0.8, 0.4])
    >>> target = tensor([0, 1, 1, 1])
    >>> average_precision = AveragePrecision(task="binary")
    >>> average_precision(pred, target)
    tensor(1.)

    >>> pred = tensor([[0.75, 0.05, 0.05, 0.05, 0.05],
    ...                [0.05, 0.75, 0.05, 0.05, 0.05],
    ...                [0.05, 0.05, 0.75, 0.05, 0.05],
    ...                [0.05, 0.05, 0.05, 0.75, 0.05]])
    >>> target = tensor([0, 1, 3, 2])
    >>> average_precision = AveragePrecision(task="multiclass", num_classes=5, average=None)
    >>> average_precision(pred, target)
    tensor([1.0000, 1.0000, 0.2500, 0.2500,    nan])
```

## Quick recipe

```python
import torchmetrics as _m
score = _m.AveragePrecision(y_true, y_pred)
```

## Don'ts

- Don't reimplement when the library version handles edge cases (NaN, ties, empty inputs) better than a hand-rolled formula.
- Always check the library version's argument order — sklearn is `(y_true, y_pred)` while torchmetrics is `(preds, target)`.
