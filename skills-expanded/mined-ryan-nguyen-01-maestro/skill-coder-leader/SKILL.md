---
name: skill-coder-leader
description: Coordinate generated service coder agents for single-service and multi-service implementation tasks.
category: workflow
---

# Skill: Coder Leader

Use after task analysis is complete.

## Responsibilities

```text
Map task to generated coder agents
Create implementation plan
Create service assignments
Sequence dependency-sensitive changes
Resolve cross-service requests
Collect coder handoff files (coder-handoff-<component>.yaml)
Review integration points across handoffs
Review code quality and architecture alignment across coder outputs
Consolidate into coder-results.yaml
Send to dev verification
```

## Collecting Coder Handoffs

Mỗi service coder sau khi hoàn thành sẽ bàn giao qua file:

```text
.maestro/work/tasks/<task-id>/coder-handoff-<component>.yaml
```

Coder Leader phải:

1. **Review từng handoff**: Đọc summary, decisions, risks, integration_notes
2. **Cross-check contracts**: Contracts provided bởi service A phải match contracts consumed bởi service B
3. **Phát hiện gaps**: Env vars thiếu, schema mismatch, API contract conflicts
4. **Resolve cross_service_requests**: Nếu coder X request thay đổi từ service Y
5. **Review code quality + architecture**: Kiểm tra maintainability, layering, conventions, reuse
6. **Tổng hợp coder-results.yaml**: Aggregate status từ tất cả handoffs
7. **Quyết định readiness**: Tất cả coders done + contracts aligned + quality review pass → ready cho Dev Verification

## Design Assets for UI Tasks

When task-analysis.yaml contains design_references:

```text
1. CHECK assets exist: .maestro/work/tasks/<task-id>/assets/
   - design-context.md, mockup screenshots, screen-map.yaml
   - If missing → request Task Analysis to extract first

2. INCLUDE in service-assignments.yaml:
   - Point each coder to their relevant flow folder
   - Example: coder-frontend → assets/flow-1-cart/, assets/flow-2-shipping/

3. MULTI-SCREEN tasks: Use screen-map.yaml to:
   - Assign screen groups (flows) to coders
   - Shared components → assign to one coder, others consume
   - Design tokens → shared across all coders

4. VERIFY in coder handoffs:
   - Coder followed design-context.md code references
   - Responsive/state variants match screen-map descriptions
```

### Example: TASK-demo-figma assignment

```text
# task-analysis.yaml đã chứa design_references với local_assets

# 1. CHECK assets
ls .maestro/work/tasks/TASK-demo-figma/assets/
→ design-context.md, design-tokens.json, screen-map.yaml  ✓

# 2. service-assignments.yaml
assignments:
  - coder: coder-frontend
    screens:
      - flow-1-home (all 7 screens)
    shared_components:
      - ProductCard (2 variants: small + large)
      - NavArrow, SectionTitle
    design_assets:
      tokens: ".maestro/work/tasks/TASK-demo-figma/assets/design-tokens.json"
      context: ".maestro/work/tasks/TASK-demo-figma/assets/design-context.md"
      screen_map: ".maestro/work/tasks/TASK-demo-figma/assets/screen-map.yaml"
    notes: |
      - Implement design tokens first (tailwind.config extend)
      - ProductCard reused across 3 sections — build once
      - Convert absolute positioning → CSS Grid/Flexbox
      - Font Beatrice is trial — confirm license or swap

# 3. VERIFY coder handoff
  ✓ design_compliance present
  ✓ screens_implemented matches screen-map.yaml (7/7)
  ✓ design tokens applied via tailwind.config
  ✓ ProductCard reused (not duplicated)
```

See full example at `.maestro/work/tasks/TASK-demo-figma/`.

## Rules

```text
Service coders do not coordinate directly.
Coder Leader owns integration consistency.
Coder Leader owns code-quality and architecture review before Dev Verification.
Shared code changes require explicit scope or approval.
Do not mark Code Done.
```
