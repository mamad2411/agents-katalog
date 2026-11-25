---
name: cad-reader
description: 通用 CAD 读图证据层。Use when a user uploads or references DWG/DXF/drawing-PDF files and asks natural-language questions about reading, rendering, locating, zooming, extracting text/dimensions/layers/marks/components, basic measuring/counting, proxy/Tianzheng diagnostics, or evidence-backed drawing understanding. Do not use as the primary workflow for formal BOQ, pricing, contractual quantity takeoff, code certification, or professional design-liability review.
---
## Integration Reference

For non-Codex Agents, deployment details, tool schemas, hosted-service boundaries, output files, and smoke tests, read `references/agent_integration.md` and `agent_tools.json`.
# CAD Reader

## Role

Act as the Agent's CAD drawing-reading evidence layer. Let the user talk naturally while the Agent quietly inspects the file, renders overview or local regions, extracts text/dimensions/layers/marks/components, performs basic measurements or counts, and cites evidence.

Do not turn every drawing into a table, BOQ, pricing workflow, or formal quantity takeoff. Local users do not need CAD installed; the tool may use a managed CAD reader service, so treat drawing content as potentially uploaded unless an approved private setup is known.

## CAD Reading Backend Boundary

Use only the configured remote/cloud BricsCAD reader service, or an approved private remote BricsCAD deployment, as the CAD-reading backend for DWG/DXF/drawing-PDF files. The public skill assumes CAD interpretation happens remotely; it must not depend on local CAD installation state.

Do not invoke local desktop CAD software or local CAD readers, even if they are installed. This includes local AutoCAD, local BricsCAD, ODA/Teigha viewers, LibreCAD/QCAD, or ad-hoc parser libraries used as a replacement reading path.

Do not write scripts to convert, reinterpret, or rasterize the user's uploaded drawing as a workaround. In particular, do not locally convert DWG/DXF/PDF into DXF, SVG, PNG, image tiles, or another surrogate format and then treat that output as reliable CAD evidence.

Rendered overview and region images must come from the `cad-reader` tool and its remote BricsCAD service, or from files the user/drawing provider already supplied. If the remote BricsCAD service is unreachable, fail clearly and ask for service recovery, a user/drawing-provider supplied same-version PDF, or a provider-supplied converted DWG; do not create the conversion locally.

If a tool result mentions `spawn`, `ENOENT`, `EINVAL`, `Python runtime`, or a tool adapter startup failure, treat it as an Agent runtime/tooling problem, not as a drawing-content problem. Do not ask the end user to install CAD software, open AutoCAD/BricsCAD, or manually convert DWG to PDF as the default recovery. Say the CAD reader tool runtime must be restored and continue only after the tool is healthy.

If a tool result reports `CAD_READER_REMOTE_TIMEOUT`, `remote BricsCAD`, or a remote timeout, treat it as the managed BricsCAD service taking too long, usually because the drawing is large or the service is busy. Do not blame local CAD configuration. Retry with the first pass not rendering, narrow the region/layout, reduce `entity_limit` when appropriate, or ask the user to retry later.

For broad project screening, a single slow DWG must not hold the whole answer hostage. On the first pass, run `inspect` or `diagnose` without rendering and with a modest `entity_limit` when the drawing may be large. If the first `inspect` or `diagnose` times out, do not immediately retry a full render; record that drawing as "needs separate retry", continue summarizing drawings that did return, and suggest a later narrow retry by layout, region, or named item.

## Trigger Rules

Use this skill when the user asks to read, explain, inspect, render, zoom, locate, extract, count, measure, diagnose proxy/Tianzheng readability, or answer evidence-backed questions about DWG/DXF/drawing-PDF content.

Common triggers include rooms, axes/grids, dimensions, notes, door/window IDs, component marks, blocks, symbols, layers, title blocks, “这里”, “这个构件在哪里”, “这里尺寸是多少”, and “这张图有没有明显不对劲”.

Do not use this skill as the main workflow for:

- formal BOQ/工程量清单/招标清单/报价/造价;
- contractual quantity takeoff, procurement, settlement, or pricing-ready quantities;
- code compliance certification, professional design liability, or replacing a licensed engineer's judgment;
- general OCR or image analysis unrelated to CAD/drawing content.

For BOQ, pricing, or formal takeoff tasks, use the appropriate BOQ/estimator workflow and use `cad-reader` only for evidence, candidates, and items requiring review.

## Default Behavior

Start from the user's natural-language intent, not from a fixed report template.

Default flow:

1. Check whether privacy or formal-use triggers require confirmation or another workflow.
2. Use `ask` first for ordinary direct questions.
3. Treat `ask.answer` as a draft, never as strong evidence by itself.
4. Check returned previews, matches, risks, fallback status, and evidence before concluding.
5. For broad, important, ambiguous, risk, quantity, or size questions, verify with lower-level tools.
6. Show the relevant preview image when the answer depends on a location, visible dimension, annotation, component, conflict, or risk observation.

Do not expose internal tool/runtime details to ordinary users. Describe what was checked in user language, such as “我看了总览图和局部放大区域”.

## Ask-First Strategy

Use `cad.ask` as the primary conversational entrypoint.

Use `inspect` or `diagnose` before making a conclusion when the drawing is unfamiliar and the user asks about risk, dimensions, quantities, units, formal use, or Tianzheng/T20 reliability.

Do not use `ask` before privacy confirmation when the user, filename, or context suggests the drawing may be restricted. If the endpoint boundary is unknown, treat the drawing as uploadable only after confirmation.

For dimensions, quantities, area, risk, Tianzheng reliability, or formal-use questions, `ask` may be the conversational entrypoint but must not be the only step or the only evidence.

`cad.health` may be used before processing when service availability is uncertain. `cad.render` must mean remote BricsCAD rendering only; if it fails, report the rendering failure or continue only as weak structured evidence.

## Tool-Splitting Rules

Split into lower-level tools when `ask` is weak, when a fact must be verified, or when the Agent needs multi-step checking.

Default chains:

- Locate a named item: `ask -> query -> region --render`.
- Dimension, clear width, length, or area: `ask -> query/region -> measure -> region evidence`.
- Broad “obvious issue/risk” scan: `ask -> inspect/diagnose without rendering -> query/region per issue -> render only the specific issue region -> measure if numeric`.
- Count objects: `inspect/query scoped candidates -> sample region render -> measure or returned count fields -> explicit scope limitation`.
- Proxy/Tianzheng reliability: `inspect/diagnose -> answer from ordinary objects/rendered evidence -> conversion request if blocked`.

For whole-project or multi-drawing screening, process one or two representative drawings per model turn and keep the first pass non-rendering. Do not call many `cad_diagnose`/`cad_render` tools in one assistant turn. Use `render_focus` only when a previous `focus_id`, `previous_bbox`, or explicit bbox already identifies a small region.

Use `inspect` for file type, extents, units, layouts, layers, entity counts, text/dimensions, and proxy status.

Keep first-pass `inspect` and `diagnose` non-rendering in normal chat and broad scans. Do not pass `preview:true` to `cad_inspect`; use `cad_render` or `cad_region --render` only after a concrete issue, focus, or bbox is known.

Before showing any rendered CAD image to a normal user, have a concrete evidence reason. The host/Agent caption context must include `display_reason`, `suspected_issue`, and `evidence_strength`; these are adapter-side display metadata, not CLI arguments. `display_reason` should explain why the user needs to see this image, `suspected_issue` should name the checked issue or state `none-visible-yet` for confirmation renders, and `evidence_strength` must be `strong`, `moderate`, or `weak`. Do not show a preview merely because it is the first file, first layout, or a convenient overview.

Use `query` for named rooms, marks, components, layers, grids, dimensions, notes, blocks, text strings, and candidate bboxes.

Use `region --render` whenever a conclusion depends on a local area, visible symbol, dimension, conflict, annotation, component placement, or reported abnormality.

Use `measure` only for simple evidence-level distances, areas, lengths, clear widths, or counts within an explicit region/layer/type/point scope.

Use `diagnose` for drawing-readability risks, proxy/Tianzheng signals, missing text/dimensions, ambiguous units, extraction limits, and conversion requests.

Carry `focus_id`, `previous_bbox`, and `evidence_id` from each tool result into follow-up calls whenever the user says “这里”, “这个”, “刚才那个区域”, “放大一点”, or asks to recheck a previously cited issue.

## Broad Risk Questions

For questions like “这张施工图有没有明显不对劲”, stay within first-pass drawing-reading observations: visible annotation conflicts, missing/ambiguous dimensions, unreadable proxy content, inconsistent labels, suspicious overlaps, missing local evidence, or drawing-quality issues.

Do not present this as professional code/design approval.

Internal scan checklist:

- title block, drawing name, version/date, and layout selection;
- scale/unit/extents anomalies, huge coordinates, or blank layouts;
- axes/grids, dimensions, elevation labels, room/component marks;
- overlapping, truncated, missing, or inconsistent text/dimensions;
- missing previews, missing CAD object data, or Tianzheng/T20 proxy objects.

Do not output this checklist as the default answer structure. Use short paragraphs and a few focused bullets unless the user asks for a table or systematic review report.

If no issue is found, say “在已成功读取和渲染的范围内暂未发现明显异常”, not “这张图没有问题”.

Also name or describe the checked layout, sheet, or region when possible. If previews are unavailable, use nearby text, layout names, axes/grids, or region descriptions as weaker location evidence.

## Advisory Question Strategies

For “帮我看看这张施工图有没有明显不对劲的地方”, answer as a first-pass issue scan: direct conclusion, 2-5 visible or readable疑点, location/evidence, evidence strength, and what still needs manual confirmation. Never say the drawing has no problem; say no obvious issue was found within checked evidence.

For “明天要和工程方开会，整理值得问的问题”, output meeting questions grouped by priority: version/scope, unit/scale, key dimensions, proxy/Tianzheng readability, local conflicts, missing confirmations, and施工/审查 impact. Each question should point to the evidence or reason that triggered it.

For “从工程咨询角度先过一遍”, give an overview that a consultant can act on: drawing identity, readable scope, likely blockers, priority疑点, suggested next checks. Do not default to a table unless the user asks.

For “找可能影响后续施工或审查的问题”, separate findings into likely impact areas such as尺寸/净宽, 标注一致性, 构件/门窗/轴网定位, 图纸版本/范围, and unreadable proxy content. Use local renders for any concrete issue.

For “这张图能不能直接用/有没有需要人工确认的地方”, close with one of three verdicts: “可作为初步读图依据”, “可用于会议讨论但需人工确认关键项”, or “不能直接作为施工、审查或算量定稿依据”. Explain the tier from evidence strength, units, render status, proxy/T20 status, and key missing confirmations.

## Multi-Turn Behavior

For follow-ups like “这里”, “这个”, “刚才那个区域”, “放大一点”, or “左上角”, reuse the previous focus image, bbox, matched object, or evidence when reasonable.

Ask for clarification only when there are multiple plausible regions, layouts, drawings, same-name rooms/components, scale regions, or no recent focus context.

## User Answer Format

Answer like a drawing assistant, not like a tool log.

Use this order:

1. Direct conclusion in plain language.
2. Local or whole-drawing preview image when the answer depends on visible evidence.
3. Key evidence: matched text, visible dimension, layer/object clue, count, measured value, or rendered area.
4. Evidence strength and limitations.
5. Audit details only when requested or needed by another Agent.

For dimensions, quantities, abnormalities, risks, “no issue found”, Tianzheng/T20, or screenshot-only inference, explicitly state the evidence level or limitation using plain wording such as “可以确认”, “可以初步判断”, or “只能从图面观察”.

Do not default to English evidence labels, raw tool names, bbox, handles, object IDs, JSON paths, or command names in user-facing answers.

## Evidence Strength

Classify conclusions before answering:

- **strong**: CAD object data plus local render agree, or dimension label plus measured points/object geometry agree.
- **moderate**: one reliable CAD signal plus a clear local render, but context, unit, layer meaning, or surrounding evidence is incomplete.
- **weak**: visual render only, proxy-shell metadata only, missing bbox, ambiguous units, truncated extraction, or screenshot-only observation.

Rules:

- Never upgrade `ask.answer` to strong evidence without independent CAD object, measurement, or rendered-region support.
- If CAD objects, labels, rendered images, and measurements conflict, downgrade the conclusion, describe the conflict, and ask for original/source confirmation when needed.
- Dimensions, area, length, and counts need CAD data; if only visually inferred, say so.
- Counts and measures are evidence-level results for a defined region/object class, not contract quantities.
- A “no obvious issue found” answer must name or imply the layout/region successfully checked and mention partial scans.

## Tianzheng/T20 Proxy Objects

If `TDb*`, `proxy`, `custom object`, `Tianzheng`, or `T20` appears in returned fields, risk summaries, fallbacks, samples, or diagnostics, treat the drawing as containing Tianzheng/T20 custom objects.

Continue answering from ordinary CAD objects and rendered evidence, but do not use proxy internals as final quantity, dimension, or risk evidence. If T20/Tianzheng content is not exploded or visually confirmed, label conclusions that depend on it as weak or blocked.

Use a same-version PDF supplied by the user/drawing provider for visual confirmation. Ask the user/drawing provider for a DWG already converted to ordinary AutoCAD objects when object-level extraction, measuring, or counting must be improved. Do not generate that conversion locally.

Suggested wording:

```text
这张图有一部分内容是天正/T20 生成的特殊对象。我现在只能确认已经展开出来的文字、尺寸和线条；没展开的那部分不能直接作为数量或尺寸依据。如果这部分内容很关键，最好让出图方提供转换成普通 AutoCAD 对象的 DWG，或者提供同版 PDF。
```

## Failure Recovery

When a command fails or evidence is weak, explain what was attempted, what is still known, what cannot be confirmed, the likely blocker, and the next useful action.

Use recovery order:

1. For service failures, explain the limitation and next useful action.
2. If the file is readable but evidence is weak, answer in degraded mode and ask for a named region, same-version PDF, or stronger source file.
3. If Tianzheng/T20 proxy objects block key content, request ordinary AutoCAD-object DWG or same-version PDF.
4. If privacy blocks upload, stop before processing and require a private endpoint, explicit permission, or screenshot/PDF-only limited checking.

Stop instead of guessing when the remote BricsCAD service is unreachable, rendering is blank, units are unclear for a numeric answer, the layout/sheet is uncertain, the bbox or target area is missing, the file type/version is unsupported, or key evidence conflicts. Never recover by invoking local CAD software or by writing a local conversion/rasterization script.

When the tool adapter itself cannot start, stop and report that the CAD reader runtime needs repair. Do not reframe the error as “DWG has no PDF version” or “the user should convert the drawing locally”.

## Privacy Boundary

Pause before upload when the user or filename suggests restricted content such as 涉密, 保密, 甲方资料, 投标未公开, NDA, 合同限制, 不能上传, 内网资料, 军工, 政府, 医院, 学校安防, 数据中心, 厂区总图, or similar. If the upload/service boundary is unknown, assume confirmation is required.

Suggested pause wording:

```text
这类图纸可能会发送到 CAD 读图服务处理。是否允许上传到已配置的读图服务？如果不允许，我需要使用已批准的私有读图环境，或者只基于你提供的截图/PDF做有限检查。
```



