---
name: official-document-drafting
description: Use when drafting, revising, summarizing, standardizing, or reviewing Chinese official documents and formal workplace materials, including notices, reports, requests, replies, meeting minutes, briefings, special reports, work plans, summaries, speeches, and presentation materials. Prefer this Skill when the task needs a fixed document type, formal institutional tone, anti-fabrication discipline, structured Markdown output, Word-ready structure, or human-review warnings for official use.
meta:
  version: 1
  display_name: 公文写作
---

# Official Document Drafting

## Purpose

Draft and revise Chinese official documents and formal workplace materials with correct document-type selection, conservative facts, formal tone, clear structure, and XAgent artifact-friendly output.

This Skill is based on `zhaohui-yang/official-document-drafting`, but the XAgent built-in version is intentionally resource-only: no external command, install flow, font package, offline adapter, demo output, or default home-directory write path is part of this Skill.

## When To Use

Use for:

- Legal official-document types such as decision, order, announcement, notice, report, request, reply, letter, meeting minutes, and related formal documents.
- Common formal materials such as work plan, implementation plan, summary, briefing, special report, speech, presentation material, and official reply letter.
- Rewriting, polishing, condensing, expanding, standardizing, or reviewing an existing draft.
- Turning user-provided facts, meeting notes, news material, or work records into a formal Markdown draft.
- Preparing a Word-ready structure before handing the result to XAgent document or artifact tools.

Do not use for casual writing, creative copywriting, technical design documents, research papers, code documentation, legal advice, compliance conclusions, or final authority approval.

## Material Gate

Before drafting, identify:

- Target document type or likely document type.
- Issuing organization, recipient, date, matter, purpose, and writing direction.
- User-provided facts, dates, sources, policy references, meeting conclusions, names, and numbers.
- Required template, local style, review authority, confidentiality constraints, and whether Word output is requested.

If key facts are missing, keep placeholders such as `[主送单位]`, `[发文单位]`, `[日期]`, `[事项名称]`, and `[待核实]`. Do not fabricate missing facts to make the document look complete.

## Method

1. Decide whether the task is one of the 15 legal official-document types. If not, map it to a common formal material type.
2. Check the writing direction: upward, downward, horizontal, public release, meeting record, or internal reporting.
3. Apply the anti-fabrication rules in `references/official-document-rules.md`.
4. Load `references/document-types.md` when the document type is unclear or the structure needs verification.
5. Use the selected document type's usual structure. If no exact template fits, use a conservative formal skeleton with placeholders.
6. Write the final Markdown draft directly unless the user asks for outline, comments, or review notes.
7. If the user asks for Word, first produce clean Markdown. Let XAgent artifact/document tooling decide the concrete output path and conversion method.

## Output Rules

- Prioritize document-type correctness before style.
- Keep the tone formal, accurate, concise, and executable.
- Use standard heading hierarchy: `一、`, `（一）`, `1.`, `（1）`.
- Preserve required structure fields when unknown by using placeholders instead of deleting them.
- Separate fact, judgment, and recommendation in briefings and special reports.
- Do not write model self-explanations inside the official draft.
- If the draft may be formally issued, reported externally, affect rights or obligations, involve sensitive content, or include private information, state that authorized human review is required before use.

## Checks

Before completion, verify:

- The chosen document type matches the user's intent and writing direction.
- Reports do not contain approval requests; requests do not masquerade as reports; letters are not written as notices.
- No invented facts, dates, names, numbers, policy bases, document numbers, legal clauses, or meeting conclusions were added.
- Missing material is represented as placeholders or `待核实`.
- Title, recipient, body, attachments, signature, date, and contact note follow the selected document type.
- The Markdown structure can be reused as an XAgent artifact or converted by document tools.

## Boundary

This Skill owns writing workflow, document-type selection, conservative drafting rules, style guidance, and reusable document structures.

It does not own XAgent tool schemas, ToolResult fields, runtime path selection, file permissions, artifact storage, Word conversion implementation, font installation, external network search, legal validity, compliance approval, secrecy review, or final official issuance. It must not run shell, Python, curl, font-install, or document-export commands by itself; those actions belong to XAgent tools and the current session's explicit permissions.

## Resources

- `references/official-document-rules.md`: anti-fabrication, workflow, style, layout, output, and XAgent artifact boundaries.
- `references/document-types.md`: document-type routing and common structures for legal official documents and formal workplace materials.
