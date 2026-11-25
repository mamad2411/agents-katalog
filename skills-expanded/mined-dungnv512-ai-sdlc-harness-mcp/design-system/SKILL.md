---
name: design-system
description: Design tokens (color, typography, spacing, radius), Widgetbook stories, theme usage for Flutter apps. MANDATORY TRIGGERS - "design system", "tokens", "theme", "ThemeData", "color palette", "typography", "Widgetbook", "story", "use case".
allowed-tools: Read, Glob, Write, Edit
---

# Skill: design-system

## When to use

Building or modifying any widget. Adding a Widgetbook story. Picking
a color or text style.

## Inputs

- widget name
- intended states (default, hover, pressed, disabled, error)

## Rules

- **Colors**: only from `config/theme/colors.dart`. No raw `Color(0xff...)`
  inside features. New tokens require a design review note in the
  PR.
- **Typography**: only from `config/theme/typography.dart` (Inter).
  Use `Theme.of(context).textTheme.<role>`.
- **Spacing**: 4-px grid: `Spacing.xs(4)`, `sm(8)`, `md(12)`,
  `lg(16)`, `xl(24)`, `xxl(32)`.
- **Radius**: `Radii.sm(8)`, `md(12)`, `lg(16)`, `pill`.
- **Dark mode**: every token has a light + dark value.

## Widgetbook stories

For each new public widget, add a story under
`widgetbook/features/<slug>/<widget>_story.dart`:

```dart
@UseCase(name: 'Default', type: PostCard)
Widget postCardDefault(BuildContext context) =>
    PostCard(post: _samplePost());
```

Stories must cover: default, loading, empty, error, RTL, large text
scale.

## Output checklist

- [ ] Color/text/spacing only from tokens
- [ ] Light + dark previews in Widgetbook
- [ ] Semantics labels added
- [ ] Tap targets >= 44 dp

## See also

- `golden-tests` (snapshots derived from stories)
