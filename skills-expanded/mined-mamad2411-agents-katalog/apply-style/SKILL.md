---
name: apply-style
description: Applies the editor's visual language to a widget, a panel or a whole band Use when the user asks for styling, spacing, colour, or says that something looks wrong
---

Read @../../reference/concept/ModernStyle.md for what the editor is trying to look like, then @../../reference/shape/theme/Theme.md for how that reaches egui. Everything you need is already a value in @../../reference/shape/theme/Tokens.md; the work is picking the right one, not choosing a colour.

# Order

- Find the token that means what you want, by meaning and not by how it looks
- If no token means it, add it to @../../reference/shape/theme/LightTokens.md and @../../reference/shape/theme/DarkTokens.md together, or do not add it
- Change the mapping in @../../reference/shape/theme/Theme.md rather than the widget, whenever the change should apply to more than one widget
- Check it in both palettes before you say it is done

# Rules

- Never a literal colour, size or radius in a widget; see @../../reference/shape/ui/UiConventions.md
- Space things apart before you draw a line between them
- Hover and focus change the tint, never the size or the position
- Only opacity animates, and never for longer than a tenth of a second
- Contrast is checked, not judged by eye, in light and in dark
