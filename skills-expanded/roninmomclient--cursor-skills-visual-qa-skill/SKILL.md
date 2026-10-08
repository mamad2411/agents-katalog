---
name: visual-qa
description: Visually verify Ronin Mom UI changes. Use after public-facing changes, before declaring design work complete, or when screenshots reveal layout, responsive, image, typography, or interaction defects.
---

# Visual QA

1. Start the real app with a repository-supported command.
2. Inspect every changed public route at representative mobile, tablet, and desktop sizes.
3. Compare the first viewport and full page.
4. Check overflow, clipping, overlap, image cropping, broken images, font loading, sticky or fixed elements, menus, focus, hover, and content density.
5. Stress article cards with long titles and article pages with realistic MDX.
6. Check browser console and network errors when tools are available.
7. Capture screenshots or record exact route and viewport evidence.
8. Fix in-scope defects, then repeat each failed check.

Distinguish application defects from preview or environment failures. A passing build is not visual validation.
