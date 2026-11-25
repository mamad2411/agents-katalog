---
name: leeway-counterfactual-workspace
description: Inspectable structured workspace for counterfactual states, hypotheses, transformations, assumptions, predictions and candidate comparison before execution.
license: MIT
---
# LeeWay Counterfactual Workspace

Maintain BASELINE_OBSERVED_STATE separately from CANDIDATE_STATE[n]. Each candidate records parent, transformation/operator, assumptions, predicted outputs, constraints checked, failures, repairs, uncertainty and evidence dependencies.

Supported representation families include geometry/kinematics, graphs, finite-state machines, timelines, queues, ledgers, resource models, scene graphs, policy matrices and symbolic equations.

Never overwrite observed state with simulated state. Candidate promotion requires execution and post-state observation.
