---
name: xslt-dita-helper
description: Provides XSLT and XPath assistance for DITA 1.3 transformations, including DITA-OT plugin development. Use this skill when you need XPath expressions for DITA element selection, XSLT template match patterns using DITA class attributes, transformation override guidance for DITA-OT, or help with specialization class attribute values.
compatibility: No runtime dependencies. Generates XSLT 1.0/2.0 code and XPath expressions for use in DITA-OT or standalone processors.
---

## Overview

Generates and validates XSLT patterns for DITA content transformation.

## Key principle: always match by `@class`, not by element name

DITA elements carry a `@class` attribute encoding the specialization hierarchy. Matching by element name breaks with specializations; matching by `@class` is robust.

```xslt
<!-- ✅ Robust — works for all specializations of task/taskbody -->
<xsl:template match="*[contains(@class, ' task/taskbody ')]">
  <div class="taskbody"><xsl:apply-templates/></div>
</xsl:template>

<!-- ❌ Fragile — breaks if a specialization renames the element -->
<xsl:template match="taskbody">
  <div class="taskbody"><xsl:apply-templates/></div>
</xsl:template>
```

## Class attribute reference

See [references/CLASS-ATTRIBUTES.md](references/CLASS-ATTRIBUTES.md) for the full table.

Quick reference for common elements:

| Element | `@class` token to match |
|---|---|
| Any topic | `topic/topic` |
| concept | `concept/concept` |
| task | `task/task` |
| taskbody | `task/taskbody` |
| step / cmd | `task/step` / `task/cmd` |
| reference | `reference/reference` |
| refbody | `reference/refbody` |
| refsyn | `reference/refsyn` |
| properties table | `reference/properties` |
| troubleshooting | `troubleshooting/troubleshooting` |
| troubleSolution | `troubleshooting/troubleSolution` |
| map / topicref | `map/map` / `map/topicref` |

## XSLT patterns reference

See [assets/xslt-patterns.xsl](assets/xslt-patterns.xsl) for ready-to-use templates.

## DITA-OT plugin override guidance

To override a built-in DITA-OT template in a plugin:

1. Set `plugin.xml` to declare a `xsl/xslhtml` extension point
2. Import `xsl/dita2htmlImpl.xsl` in your stylesheet
3. Write a higher-priority template: `<xsl:template match="..." priority="10">`

See [references/DITA-OT-PLUGIN.md](references/DITA-OT-PLUGIN.md) for full plugin scaffolding steps.

## Common edge cases

- `contains(@class, ' task/cmd ')` — note the **surrounding spaces** in the string literal; they are required to avoid partial matches
- Processing instruction `<?dita-ot ...?>` nodes: use `processing-instruction('dita-ot')` in your XPath
- `@outputclass` is the DITA hook for custom CSS classes — pass it through with `<xsl:attribute name="class" select="@outputclass"/>`
