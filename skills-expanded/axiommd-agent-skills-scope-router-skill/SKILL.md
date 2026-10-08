---
name: scope-router
description: Decide whether a normalized input packet can go straight to feature package authoring or needs product charter and system blueprint first. Use when scope is still ambiguous and the next document type must be chosen explicitly.
---

# Scope Router

## Purpose

Read one `input.packet.yaml` and emit one routing decision.

This is a **review-only skill**.

## Read First

1. [references/ROUTING_RULES.md](references/ROUTING_RULES.md)
2. [assets/route.decision.yaml](assets/route.decision.yaml)
3. [assets/routing-checklist.md](assets/routing-checklist.md)

## Use This Skill When

- `input.packet.yaml` already exists
- the main question is “go straight to feature package or not?”
- the next document type must be fixed explicitly

## Do Not Use This Skill When

- there is no normalized packet yet
- the next step is already obvious and approved
- the task is to write the package itself

## Input Contract

Required:

- `input.packet.yaml`

Optional:

- current owner docs or repo evidence cited by the packet

## Output Contract

Write exactly one `route.decision.yaml` matching [assets/route.decision.yaml](assets/route.decision.yaml).

## Read Paths

- normalized `input.packet.yaml`
- bundled routing rules in [references/ROUTING_RULES.md](references/ROUTING_RULES.md)
- target repo evidence already cited by the packet, when needed for routing confidence

## Write Paths

- `<target_feature_path>/route.decision.yaml`
- `target_feature_path`는 `input.packet.yaml`의 `constraints`에서 파생하거나 호출자가 명시한다.
- 경로를 알 수 없을 때는 STOP하고 `target_feature_path`를 요청한다. 루트에 쓰지 않는다.

## Output Target

- one routing decision only
- no framing docs
- no feature package files

## Routing Rule

- choose `direct-package` when the request is already bounded enough
- choose `framing-first` when charter/blueprint is needed first
- choose `hold` when the packet is too weak to route safely

## Workflow

1. Read the packet.
2. Check boundedness, scope clarity, success clarity, and split readiness.
3. Fill `route.decision.yaml`.
4. If the AxiomMd toolkit is available, run:
   `python $AXIOM_MD/scripts/workflow_check.py route <path/to/route.decision.yaml>`
   (`$AXIOM_MD` = path to the AxiomMd repository root)
5. Re-check [assets/routing-checklist.md](assets/routing-checklist.md).

## Stop Conditions

- packet missing
- packet too weak to judge route
- target kind and scope contradict each other
- evidence is too weak to distinguish `framing-first` from `direct-package`
- `target_feature_path`를 파생할 수 없어 출력 경로가 불명확한 경우

## Final Rule

This skill does not author the next document.
It only chooses the next workflow path and next document set.
