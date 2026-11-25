---
name: emplaw-customize
version: 1.0.0
description: Tailor the employment-legal plugin's outputs to a firm's house style, default jurisdiction, template library, and reviewer sign-off chain.
author: matrixx0070
tags: [configuration, house-style, templates, jurisdiction, formatting]
capabilities: []
---

## When to use
Use this after the org profile exists and you want every generated document to match the firm's voice, formatting, and default state law — letterhead, tone, terminology, template set, and who signs off. This is the style and defaults layer, not the fact-gathering layer. **Not for:** capturing org headcount and triggered laws (that is emplaw-cold-start-interview); drafting a single policy (emplaw-policy-drafting); reviewing a handbook (emplaw-handbook-updates); opening a matter (emplaw-matter-workspace).

## Method
1. Set the default jurisdiction. Decision point: if the org profile lists one operating state, use it as default; else prompt the operator to pick a primary and enable a per-document jurisdiction override.
2. Set tone: formal-legal, plain-language, or hybrid. Decision point: if the audience is employees, default to plain-language; if regulators or counsel, default to formal-legal.
3. Register the template library: which base templates are approved, and any client-specific clauses to inject.
4. Define terminology map (e.g., "team member" vs "employee", "separation" vs "termination").
5. Configure letterhead, header/footer, citation style, and file-naming convention.
6. Define the reviewer sign-off chain and the attorney-escalation gate. Decision point: if a document type is advice-adjacent, require named-counsel sign-off before release; else allow reviewer-only.
7. Save as the plugin's style profile and generate one sample output to confirm.

## Example
A 200-person retailer sets default jurisdiction to Illinois, plain-language tone for handbook content, formal-legal for demand responses, terminology "associate," corporate letterhead, and a two-step sign-off: HR reviewer then employment counsel for any termination or accommodation letter. A sample separation letter renders in the associate terminology on letterhead, gated for counsel sign-off.

## Pitfalls
- **Baking one state's rules into a multi-state default.** A default jurisdiction is a starting point, not a substitute for per-state review; keep the override on.
- **Letting tone override accuracy.** Plain-language rewrites can drop a required statutory phrase; preserve mandated notice language verbatim.
- **Skipping the sign-off chain.** Advice-adjacent output released without counsel review creates unauthorized-practice and malpractice exposure.
- **Terminology drift.** Renaming "termination" to "separation" everywhere can misalign with statutory terms in a formal filing; scope the map by document type.

## Output format
```
EMPLAW STYLE PROFILE — <org>
Default jurisdiction: <state>   Override enabled: <y/n>
Tone: <formal-legal | plain-language | hybrid by doc-type>
Approved templates: <list>   Injected clauses: <list>
Terminology map: <term -> preferred; ...>
Format: letterhead <ref>, citation style <ref>, file-naming <pattern>
Sign-off chain: <reviewer -> counsel for: doc-types>
Escalation gate: counsel sign-off required before releasing <advice-adjacent doc-types>
```

## Reference
Style choices never override substance. Mandated content persists regardless of tone: FLSA-required wage notices, ADA interactive-process language, FMLA eligibility/designation notices, and state posting/notice requirements. Default-jurisdiction reference points for common defaults: CA (FEHA 5+, mandated harassment-training language), NY/NYC (4+ thresholds, sexual-harassment policy mandates), TX/IL/etc. vary. Citation style should follow the firm's standard (e.g., Bluebook) for any formal document. This is general reference, not tailored legal advice — escalate to licensed counsel before releasing any advice-adjacent document, and never let formatting defaults substitute for jurisdiction-specific review.
