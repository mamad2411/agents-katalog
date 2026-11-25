---
name: skill-service-coder
description: Implement code inside a generated service coder's allowed scope while following component test policy and handoff obligations.
category: workflow
---

# Skill: Service Coder

Use inside generated `coder-<service>` agents.

## Workflow

```text
Read service assignment
Read component knowledge
Confirm allowed write scope
Read design assets (if UI task)
Implement only assigned scope
Reuse existing patterns
Follow component test policy
Write coder-handoff-<component>.yaml and return to Coder Leader
```

## Design-Aware Implementation (UI tasks)

When the task folder contains design assets:

```text
1. READ local files only — never call Figma API directly:
   - .maestro/work/tasks/<task-id>/assets/design-context.md     ← Code reference
   - .maestro/work/tasks/<task-id>/assets/mockup-*.png           ← Visual reference
   - .maestro/work/tasks/<task-id>/assets/design-tokens.json     ← Colors, spacing, typography
   - .maestro/work/tasks/<task-id>/assets/image-assets.yaml      ← Icon/image inventory
   - .maestro/work/tasks/<task-id>/screen-map.yaml               ← Screen inventory

2. FOR assigned flow folder (e.g., assets/flow-1-cart/):
   - design-context.md → Use code snippets as implementation reference
   - mockup-*.png → Visual verification target
   - states.md → Implement loading/error/empty states from text descriptions

3. HANDLE ICONS & IMAGES — strategy depends on figma_tier in image-assets.yaml:

   ┌─────────────────────────────────────────────────────────────────────┐
   │ figma_tier: high (200 calls/day)                                   │
   │                                                                     │
   │ Coders CAN call Figma MCP during implementation:                   │
   │ a. Icons: call get_screenshot on individual icon nodes → save SVG  │
   │    - Or use icon library if match exists (preferred)               │
   │ b. Complex sections: call get_screenshot for visual reference      │
   │ c. Product images: still use CMS/API (not Figma placeholders)     │
   │                                                                     │
   │ Benefit: real-time visual verification during coding               │
   └─────────────────────────────────────────────────────────────────────┘

   ┌─────────────────────────────────────────────────────────────────────┐
   │ figma_tier: low (6 calls/month — Starter/Free)                     │
   │                                                                     │
   │ Coders NEVER call Figma MCP. Use ONLY local files.                 │
   │                                                                     │
   │ a. Icons: must already be in assets/icons/ (pre-exported by        │
   │    task-analysis) OR matched to icon library in image-assets.yaml  │
   │ b. Product images: implement with EXACT placeholder_spec:          │
   │    - Use placeholder_spec.width, height, aspect_ratio              │
   │    - Set object-fit from placeholder_spec.object_fit               │
   │    - Apply border, border_radius, background from spec             │
   │    - Use alt_text_pattern for accessibility                        │
   │    - Set loading="lazy"|"eager" from spec                          │
   │    → When real images replace placeholders, fit is 100% pixel-     │
   │      perfect because container dimensions are exact from Figma.    │
   │ c. If icon file is missing and no library match exists:            │
   │    - Use a text/emoji placeholder with correct dimensions          │
   │    - Add TODO comment: "// TODO: Replace with exported SVG"        │
   │    - Report in coder-handoff as missing_asset                      │
   │                                                                     │
   │ Benefit: zero MCP calls, swap-ready placeholder images             │
   └─────────────────────────────────────────────────────────────────────┘

   Common rules (both tiers):
   a. Check if project has icon library (lucide, heroicons, phosphor)
      - If icon matches → use library (smaller bundle, no API call)
   b. Product images → dynamic from product API, NOT Figma export
   c. Decorative elements (dividers, backgrounds) → CSS equivalents
   d. Always set proper alt text, lazy loading, aspect-ratio CSS

4. IMPLEMENT in order:
   a. Shared design tokens → CSS variables / theme config
   b. Primary screen (main state) → match design-context code
   c. Responsive variants → follow screen-map notes
   d. State variants (loading/error/empty) → follow states.md descriptions

4. REPORT in coder-handoff:
   - design_compliance: which screens matched, which deviated and why
   - screens_implemented: list from screen-map.yaml
```

### Example: Reading TASK-demo-figma assets

```text
# 1. Read design tokens first → set up theme
cat .maestro/work/tasks/TASK-demo-figma/assets/design-tokens.json
→ colors.accent = "#000e8a"
→ typography.h1 = { font: "Beatrice Deck Trial", size: "48px", weight: "800" }
→ component_specs.product_card_small = { width: "304px", height: "313px" }

# 2. Read image-assets.yaml → check figma_tier + icon strategy
cat .maestro/work/tasks/TASK-demo-figma/assets/image-assets.yaml
→ figma_tier: low
→ Group6 (logo): custom, must use pre-exported SVG from assets/icons/logo.svg
→ Group45 (wishlist): library_alternative = "lucide:Heart" → use Lucide
→ Product images: placeholder_spec = { width: 304, height: 313, aspect_ratio: "304:313",
     object_fit: "cover", border: "1px solid #d7d7d7", border_radius: "0px" }
→ Since figma_tier=low: implement <img> container with EXACT specs so real
  images swap in pixel-perfect

# 3. Read screen-map for assigned screens
cat .maestro/work/tasks/TASK-demo-figma/assets/screen-map.yaml
→ flow-1-home: 7 screens, shared components: ProductCard, NavArrow, SectionTitle

# 4. Read design-context for code reference per section
cat .maestro/work/tasks/TASK-demo-figma/assets/design-context.md
→ Section 4 "New This Week": 4-col grid, ProductCard with:
  - Image 304x313, border #d7d7d7
  - Category label (Inter Medium 12px #8a8a8a)
  - Product title (Beatrice Deck Trial Regular 16px)
  - Price (Inter Medium 14px, "$99")
  - Wishlist icon → lucide:Heart (from image-assets.yaml)

# 5. Implement ProductCard component
# Low tier: image container uses exact placeholder_spec dimensions
<div style="width:304px; height:313px; border:1px solid #d7d7d7;">
  <img src={product.imageUrl} alt={`${product.name} - ${product.category}`}
       loading="lazy" style="object-fit:cover; width:100%; height:100%;" />
</div>
# → When CMS provides real images, they fill the container 100% correctly

# 6. Report in coder-handoff:
  design_compliance:
    matched: [header, hero, new-this-week, footer]
    deviated:
      - section: "hero"
        reason: "Changed absolute positioning to CSS Grid for responsiveness"
  screens_implemented: [header, sidebar, hero, new-this-week, xiv-collections, our-approach, footer]
```

See full example at `.maestro/work/tasks/TASK-demo-figma/`.

## Coder-to-Leader Handoff

Sau khi hoàn thành implementation, mỗi service coder **bắt buộc** tạo file handoff:

```text
Path: .maestro/work/tasks/<task-id>/coder-handoff-<component>.yaml
Template: .maestro/engine/templates/coder-handoff.template.yaml
```

File handoff phải bao gồm:

- **steps_completed**: Steps nào đã hoàn thành
- **files_changed**: Danh sách files đã thay đổi (path + action)
- **summary**: Tóm tắt implementation
- **decisions**: Các quyết định đã tự đưa ra (và lý do)
- **integration_notes**: Contracts provided/consumed, env vars cần thiết
- **cross_service_requests**: Yêu cầu thay đổi từ service khác (nếu có)
- **risks**: Rủi ro cần Coder Leader biết
- **reuse_report**: Assets used, conventions followed, anti-patterns avoided
- **verification**: Evidence chứng minh code hoạt động

Coder Leader dùng các handoff files để:

1. Review integration points giữa các services
2. Phát hiện conflicts hoặc gaps
3. Tổng hợp thành `coder-results.yaml`
4. Quyết định sẵn sàng chuyển Dev Verification hay chưa

## Test policy

```text
If unit_tests_required is true, add or update tests using existing conventions.
If unit_tests_required is false, do not create new test files.
If unknown, ask Coder Leader or Coordinator before creating tests.
Manual verification must be documented when tests are not required.
```

## Stop when

```text
Task requires forbidden path changes
Cross-service contract needs another service update
Critical requirement is ambiguous
A blocker prevents safe implementation
```

## Reuse-before-create rule

Before creating new helper code, wrappers, validators, mappers, serializers, repositories, API clients, transaction helpers, event helpers, payment helpers, notification helpers, or test utilities, a service coder must check:

- The assigned component knowledge under component_deep_intelligence.
- The project reusable asset index in .maestro/memory/project/common/generics.md.
- The project conventions in .maestro/knowledge/conventions.md.
- The relevant task reuse_and_convention_analysis section.

If an existing reusable asset fits, reuse it. If a new reusable asset is needed, report it to Coder Leader with reason, proposed ownership, affected services, and migration impact before broad usage.

Coder results must document:

- Reusable assets used.
- Conventions followed.
- Anti-patterns avoided.
- Any new reusable asset created and why reuse was not possible.
