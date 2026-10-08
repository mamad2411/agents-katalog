---
name: forge-audit
description: Check the current codebase against your .forge.json design system. Finds raw hex values that should be tokens, spacing off your scale, fonts not in your system, and missing token references.
user-invokable: true
---

# /forge-audit — Design System Audit

Scan every CSS file in the project and check:

1. **Colors**: Any hex/rgb value not in your palette or tokens → violation
2. **Spacing**: Any padding/margin/gap not in your spacing scale → violation
3. **Typography**: Any font-family not matching your system's display/body/mono → violation
4. **Font sizes**: Any font-size not matching your type scale steps → violation
5. **Shadows**: Any box-shadow not matching your elevation system → warning
6. **Radii**: Any border-radius not in your radius scale → warning

Output: structured report with file, line, current value, and suggested token replacement.
