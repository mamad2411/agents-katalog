---
name: generate-system-map
description: Generates a standalone, interactive HTML map of your Claude Code automation setup: a radial SVG mind-map of your skills grouped into departments, a schedule view of every scheduled task, and a feedback panel that turns flagged issues into copy-ready fix prompts. Best if you run several skills and/or scheduled agents. Trigger on "/generate-system-map", "map my skills", "generate a system map", "visualize my automations", or "build a map of my setup".
---

# generate-system-map

Generates a personalized automation workflow map: a standalone HTML microsite with an interactive SVG mind map, schedule tab, and a feedback/issue-flagging system that outputs copy-ready fix prompts.

## What gets produced

A single `system-map.html` file. Open it in any browser, no server needed. Three tabs:
- **Workflow Map**: radial SVG mind map: center hub → dept nodes → leaf skill nodes. Layout auto-adapts: 1–8 departments supported with coordinate tables for each count.
- **Schedule**: table of every task's timing, frequency, and trigger source
- **Feedback**: flag issues on any node, then generate organized fix prompts per skill/file

## When to run

Run this when someone on the team wants their own copy of the workflow map customized for their system. The output file can be shared or opened locally.

---

## Execution steps

### 1. Discover the system

Read these in parallel:
- `~/.claude/skills/`: list all skill directories, then read each `SKILL.md` to understand what each skill does, its trigger type, and any timing info. In each `SKILL.md`, look for the DEPLOYMENT / trigger line that names the skill's `trig_*` routine ID and its timing (e.g. "weekday 8am ET via cloud routine trig_01...").
- `~/.claude/CLAUDE.md` if it exists: project name, company name, system overview
- `~/CLAUDE.md` if it exists: same
- Live cloud routines: load the `RemoteTrigger` tool via ToolSearch (query `select:RemoteTrigger`), then list the live routines to get each one's `trig_*` ID and cron schedule. This is the source of truth for what actually fires and when, cross-check it against the timing each `SKILL.md` claims.
- Local LaunchAgents: run `ls ~/Library/LaunchAgents/com.<yourname>.*` to find any local scheduled agents (e.g. the inventory LaunchAgent). Read each plist for its `StartCalendarInterval` timing and the script it runs.

### 2. Organize into departments

Group the discovered skills into departments based on what makes sense for their system. **Do not force exactly 4**, use however many naturally emerge (1–8 is the supported range). Better to have the right number of groups than to artificially merge or split things.

Grouping heuristics:
- Skills that fire on a timer/server schedule → one scheduler dept
- Skills in the same workflow (review → approve → notify) → one dept
- Skills using the same external service (all Slack skills, all email skills) → consider grouping
- Skills that are sub-skills or helpers called by others → can be a "Utilities" dept or merged into the parent dept

Each dept should have 1–6 leaf nodes. If a dept would have 7+, split it. If two depts each have 1 skill, consider merging them.

Identify for each skill:
- **Trigger type**: `auto` (fired by a cloud routine `trig_*` or a local LaunchAgent), `external` (Zapier/webhook), `manual` (user clicks), `queued` (deferred)
- **Timing**: exact time / frequency / days if auto; "on demand" / "real-time" if not
- **Files involved**: skill file path + any data files it reads/writes

### 3. Ask only if needed

If after reading all files you cannot determine:
- The company/team name → ask: "What's your company or team name for the map title?"
- The central hub name → ask: "What do you call your main dashboard or control panel?"
- How to group a skill → make a reasonable call and note it in the generated file as a comment

Do NOT ask for info you can derive from reading files.

### 4. Determine output path

If the user specified a path (e.g. `--path ~/Desktop/system-map.html`), use that.  
Otherwise write to `./system-map.html` in the current working directory.

### 5. Generate the HTML

Write a complete `system-map.html` using the template below, substituting all `[PLACEHOLDER]` values with the real discovered content.

---

## HTML template

The full file structure to generate. Replace every `[PLACEHOLDER]` with real content. Keep all CSS, JS logic, and modal infrastructure exactly as-is, only change data/content.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>[COMPANY_NAME]: Workflow Map</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 100%; height: 100%; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f8fafc; overflow: hidden; }
#tabbar { position: fixed; top: 0; left: 0; right: 0; height: 46px; z-index: 300; background: white; border-bottom: 1px solid #e2e8f0; display: flex; align-items: center; padding: 0 20px; gap: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
.logo { font-size: 13px; font-weight: 800; color: #0f172a; margin-right: 10px; }
.tab-btn { padding: 6px 14px; border-radius: 8px; border: none; background: none; font-size: 13px; font-weight: 600; color: #64748b; cursor: pointer; display: flex; align-items: center; gap: 5px; transition: background .1s, color .1s; }
.tab-btn:hover { background: #f1f5f9; color: #0f172a; }
.tab-btn.active { background: #4f46e5; color: white; }
.fb-badge { display: none; background: #ef4444; color: white; font-size: 10px; font-weight: 700; border-radius: 10px; padding: 1px 6px; line-height: 1.4; }
.tab-btn.active .fb-badge { background: rgba(255,255,255,0.3); }
.view { display: none; position: fixed; top: 46px; left: 0; right: 0; bottom: 0; }
.view.active { display: block; }
#map-view { overflow: auto; cursor: grab; user-select: none; }
#map-view:active { cursor: grabbing; }
#schedule-view, #feedback-view { overflow-y: auto; background: #f8fafc; }
svg { display: block; }
.dept-node, .leaf-node, .center-node { cursor: pointer; }
.dept-node rect, .leaf-node rect { transition: filter 0.15s; }
.dept-node:hover rect, .leaf-node:hover rect { filter: brightness(0.93) drop-shadow(0 3px 8px rgba(0,0,0,0.15)); }
.center-node:hover rect { filter: brightness(1.08) drop-shadow(0 4px 12px rgba(79,70,229,0.4)); }
.comment-btn { opacity: 0; transition: opacity .15s; cursor: pointer; }
.dept-node:hover .comment-btn, .leaf-node:hover .comment-btn, .center-node:hover .comment-btn { opacity: 1; }
.comment-btn circle { transition: fill .12s; }
.comment-btn:hover circle { fill: #e0e7ff !important; }
.sched-wrap { max-width: 860px; margin: 0 auto; padding: 32px 24px 80px; }
.sched-pg-title { font-size: 20px; font-weight: 800; color: #0f172a; margin-bottom: 4px; }
.sched-pg-sub { font-size: 13px; color: #64748b; margin-bottom: 16px; }
.sched-summary { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 32px; }
.sched-sum-pill { padding: 5px 12px; border-radius: 8px; font-size: 12px; font-weight: 600; }
.sched-sec-hdr { font-size: 10px; font-weight: 800; letter-spacing: 1.2px; text-transform: uppercase; color: #94a3b8; margin: 28px 0 10px 2px; }
.sched-row { background: white; border-radius: 12px; border: 1px solid #e2e8f0; padding: 14px 18px; margin-bottom: 8px; display: flex; align-items: center; gap: 14px; transition: border-color .12s, box-shadow .12s; }
.sched-row:hover { border-color: #c7d2fe; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
.sched-icon { font-size: 22px; flex-shrink: 0; width: 34px; text-align: center; }
.sched-info { flex: 1; min-width: 0; }
.sched-name { font-size: 14px; font-weight: 700; color: #0f172a; }
.sched-desc { font-size: 11px; color: #64748b; margin-top: 2px; line-height: 1.5; }
.sched-trig { font-size: 10px; color: #b0bec5; margin-top: 5px; font-family: ui-monospace, monospace; }
.sched-mid { display: flex; flex-direction: column; align-items: flex-end; gap: 5px; flex-shrink: 0; }
.sbadge { display: inline-block; padding: 2px 9px; border-radius: 6px; font-size: 10px; font-weight: 600; white-space: nowrap; }
.bd-auto     { background: #fef3c7; color: #92400e; border: 1px solid #fde68a; }
.bd-external { background: #fff7ed; color: #c2410c; border: 1px solid #fed7aa; }
.bd-manual   { background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; }
.bd-queued   { background: #ede9fe; color: #5b21b6; border: 1px solid #ddd6fe; }
.bd-subskill { background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; }
.sched-timing { flex-shrink: 0; width: 165px; text-align: right; }
.sched-time-main { font-size: 13px; font-weight: 700; color: #0f172a; line-height: 1.3; }
.sched-time-freq { font-size: 10px; color: #64748b; margin-top: 3px; }
.sched-time-days { font-size: 10px; color: #94a3b8; margin-top: 1px; }
.sched-cmt-btn { flex-shrink: 0; width: 28px; height: 28px; border-radius: 8px; border: 1px solid #e2e8f0; background: white; color: #94a3b8; font-size: 13px; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all .12s; }
.sched-cmt-btn:hover { background: #ede9fe; border-color: #a5b4fc; color: #4f46e5; }
.fb-wrap { max-width: 860px; margin: 0 auto; padding: 32px 24px 80px; }
.fb-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px; }
.fb-title { font-size: 20px; font-weight: 800; color: #0f172a; }
.fb-sub { font-size: 13px; color: #64748b; margin-top: 2px; }
.btn-generate { padding: 10px 20px; border-radius: 10px; border: none; background: #4f46e5; color: white; font-size: 13px; font-weight: 700; cursor: pointer; transition: background .12s; white-space: nowrap; }
.btn-generate:hover { background: #4338ca; }
.btn-generate:disabled { background: #cbd5e1; cursor: default; }
.fb-empty { text-align: center; padding: 60px 20px; color: #94a3b8; border: 2px dashed #e2e8f0; border-radius: 16px; background: white; }
.fb-empty-icon { font-size: 40px; margin-bottom: 12px; }
.fb-empty-title { font-size: 15px; font-weight: 700; color: #64748b; margin-bottom: 6px; }
.fb-empty-hint { font-size: 12px; line-height: 1.6; }
.fb-group-hdr { font-size: 10px; font-weight: 800; letter-spacing: 1px; text-transform: uppercase; color: #94a3b8; margin: 24px 0 8px 2px; }
.fb-card { background: white; border-radius: 12px; border: 1px solid #e2e8f0; padding: 14px 16px; margin-bottom: 8px; display: flex; align-items: flex-start; gap: 12px; }
.fb-card-left { flex: 1; }
.fb-node-name { font-size: 13px; font-weight: 700; color: #0f172a; }
.fb-cat { font-size: 10px; color: #94a3b8; margin-top: 1px; }
.fb-comment { font-size: 12px; color: #374151; margin-top: 8px; line-height: 1.6; background: #f8fafc; border-radius: 8px; padding: 8px 10px; border: 1px solid #f1f5f9; }
.fb-time { font-size: 10px; color: #94a3b8; margin-top: 6px; }
.fb-del { background: none; border: none; color: #cbd5e1; font-size: 16px; cursor: pointer; padding: 2px 6px; border-radius: 6px; flex-shrink: 0; margin-top: -2px; }
.fb-del:hover { background: #fef2f2; color: #ef4444; }
#comment-modal { display: none; position: fixed; inset: 0; z-index: 500; background: rgba(15,23,42,0.4); backdrop-filter: blur(4px); align-items: center; justify-content: center; }
#comment-modal.open { display: flex; }
#comment-card { background: white; border-radius: 16px; padding: 24px; width: 420px; max-width: 92vw; box-shadow: 0 20px 60px rgba(0,0,0,0.2); animation: pop .15s ease; }
.comment-card-hdr { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 16px; }
.comment-node-badge { font-size: 12px; font-weight: 700; color: #4f46e5; background: #ede9fe; padding: 3px 10px; border-radius: 6px; display: inline-block; margin-bottom: 4px; }
.comment-card-title { font-size: 15px; font-weight: 800; color: #0f172a; }
.comment-card-sub { font-size: 11px; color: #94a3b8; margin-top: 2px; }
.comment-x { background: none; border: none; color: #94a3b8; font-size: 20px; cursor: pointer; padding: 0 4px; line-height: 1; border-radius: 6px; }
.comment-x:hover { background: #f1f5f9; color: #0f172a; }
#comment-text { width: 100%; border: 1.5px solid #e2e8f0; border-radius: 10px; padding: 10px 12px; font-size: 13px; font-family: inherit; resize: vertical; outline: none; color: #0f172a; transition: border-color .12s; }
#comment-text:focus { border-color: #a5b4fc; }
.comment-actions { display: flex; gap: 8px; justify-content: flex-end; margin-top: 12px; }
.btn-secondary { padding: 8px 16px; border-radius: 8px; border: 1px solid #e2e8f0; background: white; font-size: 13px; font-weight: 600; color: #64748b; cursor: pointer; }
.btn-secondary:hover { background: #f8fafc; }
.btn-primary { padding: 8px 18px; border-radius: 8px; border: none; background: #4f46e5; color: white; font-size: 13px; font-weight: 700; cursor: pointer; }
.btn-primary:hover { background: #4338ca; }
#prompt-modal { display: none; position: fixed; inset: 0; z-index: 500; background: rgba(15,23,42,0.5); backdrop-filter: blur(6px); align-items: flex-start; justify-content: center; padding: 30px 20px; overflow-y: auto; }
#prompt-modal.open { display: flex; }
#prompt-card { background: #0f172a; border-radius: 18px; padding: 0; width: 760px; max-width: 96vw; box-shadow: 0 30px 80px rgba(0,0,0,0.4); animation: pop .18s ease; flex-shrink: 0; }
.prompt-card-hdr { display: flex; align-items: center; justify-content: space-between; padding: 20px 24px 16px; border-bottom: 1px solid rgba(255,255,255,0.08); }
.prompt-card-title { font-size: 16px; font-weight: 800; color: white; }
.prompt-card-sub { font-size: 11px; color: #64748b; margin-top: 2px; }
.prompt-hdr-btns { display: flex; gap: 8px; align-items: center; }
.btn-copy-all { padding: 7px 14px; border-radius: 8px; border: none; background: #4f46e5; color: white; font-size: 12px; font-weight: 700; cursor: pointer; }
.btn-copy-all:hover { background: #4338ca; }
.prompt-x { background: none; border: none; color: #64748b; font-size: 20px; cursor: pointer; padding: 0 4px; line-height: 1; border-radius: 6px; }
.prompt-x:hover { color: white; }
.prompt-list { padding: 20px 24px 24px; display: flex; flex-direction: column; gap: 16px; }
.prompt-block { background: #1e293b; border-radius: 12px; overflow: hidden; border: 1px solid rgba(255,255,255,0.07); }
.prompt-block-hdr { display: flex; align-items: center; justify-content: space-between; padding: 10px 16px; background: #334155; border-bottom: 1px solid rgba(255,255,255,0.07); }
.prompt-block-label { font-size: 12px; font-weight: 700; color: #e2e8f0; }
.prompt-block-meta { font-size: 10px; color: #94a3b8; }
.btn-copy { padding: 4px 12px; border-radius: 6px; border: none; background: rgba(255,255,255,0.1); color: #e2e8f0; font-size: 11px; font-weight: 600; cursor: pointer; }
.btn-copy:hover { background: rgba(255,255,255,0.18); }
.prompt-text { padding: 16px; font-size: 12px; font-family: ui-monospace, monospace; color: #94a3b8; line-height: 1.7; white-space: pre-wrap; word-break: break-word; }
.prompt-text .hi { color: #e2e8f0; font-weight: 600; }
.prompt-text .issue { color: #fbbf24; }
.prompt-text .file { color: #6ee7b7; }
#modal { display: none; position: fixed; inset: 0; z-index: 400; background: rgba(15,23,42,0.45); backdrop-filter: blur(6px); align-items: center; justify-content: center; }
#modal.open { display: flex; }
#card { background: #fff; border-radius: 18px; padding: 0; width: 520px; max-width: 92vw; max-height: 82vh; overflow-y: auto; box-shadow: 0 24px 80px rgba(0,0,0,0.22); animation: pop .18s ease; }
@keyframes pop { from { transform:scale(.93);opacity:0 } to { transform:scale(1);opacity:1 } }
.card-head { padding: 22px 22px 16px; border-bottom: 1px solid #f1f5f9; display: flex; align-items: flex-start; gap: 12px; }
.card-icon { font-size: 32px; line-height: 1; flex-shrink: 0; margin-top: 2px; }
.card-text { flex: 1; }
.card-title { font-size: 18px; font-weight: 800; color: #0f172a; line-height: 1.2; }
.card-sub { font-size: 11px; color: #94a3b8; margin-top: 3px; }
.card-close { background: none; border: none; color: #94a3b8; font-size: 22px; cursor: pointer; line-height: 1; padding: 2px 6px; border-radius: 6px; flex-shrink: 0; }
.card-close:hover { background: #f1f5f9; color: #0f172a; }
.card-body { padding: 18px 22px 22px; }
.card-flag { margin: 0 22px 16px; padding: 8px 12px; border-radius: 8px; border: 1px solid #e2e8f0; background: #f8fafc; display: flex; align-items: center; justify-content: space-between; }
.card-flag-txt { font-size: 11px; color: #94a3b8; }
.card-flag-btn { padding: 4px 12px; border-radius: 6px; border: 1px solid #e2e8f0; background: white; font-size: 11px; font-weight: 600; color: #64748b; cursor: pointer; }
.card-flag-btn:hover { background: #fef2f2; border-color: #fca5a5; color: #ef4444; }
.step { display: flex; gap: 12px; margin-bottom: 10px; padding: 12px; background: #f8fafc; border-radius: 10px; border: 1px solid #e2e8f0; }
.step-ic { font-size: 20px; flex-shrink: 0; margin-top: 1px; }
.step-title { font-size: 13px; font-weight: 700; color: #0f172a; margin-bottom: 3px; }
.step-desc { font-size: 11px; color: #64748b; line-height: 1.6; }
.pill { display: inline-block; padding: 1px 8px; border-radius: 20px; font-size: 10px; font-weight: 600; margin: 1px 2px 0; }
.svc { background: #ede9fe; color: #5b21b6; }
.out { background: #dcfce7; color: #166534; }
.fil { background: #f0fdf4; color: #166534; font-family: monospace; font-size: 9px; }
.wrn { background: #fef3c7; color: #92400e; }
</style>
</head>
<body>

<div id="tabbar">
  <span class="logo">[LOGO_EMOJI] [COMPANY_NAME]</span>
  <button class="tab-btn active" onclick="switchTab('map')">🗺 Workflow Map</button>
  <button class="tab-btn" onclick="switchTab('schedule')">📅 Schedule</button>
  <button class="tab-btn" onclick="switchTab('feedback')">💬 Feedback <span class="fb-badge" id="fb-badge"></span></button>
</div>

<!-- MAP VIEW -->
<div id="map-view" class="view active">
<svg id="svg" viewBox="0 0 1440 900" width="1440" height="900" xmlns="http://www.w3.org/2000/svg">
<defs>
  <pattern id="dots" x="0" y="0" width="24" height="24" patternUnits="userSpaceOnUse">
    <circle cx="1.5" cy="1.5" r="1.2" fill="#cbd5e1" opacity="0.55"/>
  </pattern>
  <filter id="sh"><feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#00000018"/></filter>
  <marker id="arr" markerWidth="7" markerHeight="5" refX="5" refY="2.5" orient="auto">
    <polygon points="0 0,7 2.5,0 5" fill="#94a3b8"/>
  </marker>
</defs>
<rect width="1440" height="900" fill="#f8fafc"/>
<rect width="1440" height="900" fill="url(#dots)"/>
<text x="720" y="36" text-anchor="middle" font-size="13" font-weight="700" fill="#1e293b" font-family="-apple-system,sans-serif">[COMPANY_NAME]: Automation Workflow</text>
<text x="720" y="54" text-anchor="middle" font-size="10" fill="#94a3b8" font-family="-apple-system,sans-serif">click any node to explore · hover to flag an issue</text>

<!-- [GENERATE ALL CONNECTOR LINES HERE] -->
<!-- [GENERATE ALL TRIGGER LABELS HERE] -->
<!-- [GENERATE CENTER NODE] -->
<!-- [GENERATE 4 DEPT NODES] -->
<!-- [GENERATE ALL LEAF NODES] -->

<!-- legend -->
<rect x="490" y="848" width="460" height="42" rx="10" fill="white" stroke="#e2e8f0" stroke-width="1"/>
<circle cx="514" cy="864" r="5" fill="#4f46e5"/>
<text x="526" y="868" font-size="9" fill="#64748b" font-family="-apple-system,sans-serif">hub</text>
<circle cx="556" cy="864" r="5" fill="#fef3c7" stroke="#d97706" stroke-width="1.5"/>
<text x="568" y="868" font-size="9" fill="#64748b" font-family="-apple-system,sans-serif">dept</text>
<circle cx="605" cy="864" r="5" fill="#fffbeb" stroke="#fcd34d" stroke-width="1.5"/>
<text x="617" y="868" font-size="9" fill="#64748b" font-family="-apple-system,sans-serif">skill</text>
<text x="720" y="880" text-anchor="middle" font-size="9" fill="#94a3b8" font-family="-apple-system,sans-serif">hover a node → click + to flag an issue · click node to explore · Esc closes any panel</text>
</svg>
</div>

<!-- SCHEDULE VIEW -->
<div id="schedule-view" class="view">
  <div class="sched-wrap" id="sched-content"></div>
</div>

<!-- FEEDBACK VIEW -->
<div id="feedback-view" class="view">
  <div class="fb-wrap" id="fb-content"></div>
</div>

<!-- COMMENT FORM MODAL -->
<div id="comment-modal" onclick="if(event.target===this)closeComment()">
  <div id="comment-card">
    <div class="comment-card-hdr">
      <div>
        <div class="comment-node-badge" id="comment-node-badge"></div>
        <div class="comment-card-title">Report an issue</div>
        <div class="comment-card-sub">Be specific: what's broken, slow, unclear, or wrong?</div>
      </div>
      <button class="comment-x" onclick="closeComment()">×</button>
    </div>
    <textarea id="comment-text" rows="4" placeholder="Describe the issue or improvement..."></textarea>
    <div class="comment-actions">
      <button class="btn-secondary" onclick="closeComment()">Cancel</button>
      <button class="btn-primary" onclick="submitComment()">Submit Issue</button>
    </div>
  </div>
</div>

<!-- PROMPT OUTPUT MODAL -->
<div id="prompt-modal" onclick="if(event.target===this)closePrompts()">
  <div id="prompt-card">
    <div class="prompt-card-hdr">
      <div>
        <div class="prompt-card-title">🛠 Fix Prompts</div>
        <div class="prompt-card-sub" id="prompt-card-sub"></div>
      </div>
      <div class="prompt-hdr-btns">
        <button class="btn-copy-all" onclick="copyAllPrompts()">Copy All</button>
        <button class="prompt-x" onclick="closePrompts()">×</button>
      </div>
    </div>
    <div class="prompt-list" id="prompt-list"></div>
  </div>
</div>

<!-- DETAIL MODAL -->
<div id="modal" onclick="if(event.target===this)closeModal()">
  <div id="card">
    <div class="card-head">
      <div id="ci" class="card-icon"></div>
      <div class="card-text">
        <div id="ct" class="card-title"></div>
        <div id="cs" class="card-sub"></div>
      </div>
      <button class="card-close" onclick="closeModal()">×</button>
    </div>
    <div class="card-flag">
      <span class="card-flag-txt">Something broken or unclear in this skill?</span>
      <button class="card-flag-btn" onclick="flagFromModal()">🐛 Flag Issue</button>
    </div>
    <div id="cb" class="card-body"></div>
  </div>
</div>

<script>
function switchTab(name) {
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById(name + '-view').classList.add('active');
  event.currentTarget.classList.add('active');
  if (name === 'feedback') renderFeedback();
}

// ── SKILL_MAP: update these with your real file paths ─────
// Format: 'node-id': { skill: 'skill-name', files: ['path/to/skill', 'path/to/data'] }
const SKILL_MAP = {
  // [GENERATE SKILL_MAP ENTRIES FROM DISCOVERED SKILLS]
  // Example:
  // 'my-skill': { skill: 'my-skill-name', files: ['~/.claude/skills/my-skill/SKILL.md'] },
};

let _commentTarget = null;

function getComments() {
  try { return JSON.parse(localStorage.getItem('system-feedback') || '[]'); } catch { return []; }
}
function saveComments(items) {
  localStorage.setItem('system-feedback', JSON.stringify(items));
  updateBadge();
}
function updateBadge() {
  const n = getComments().length;
  const b = document.getElementById('fb-badge');
  b.textContent = n || '';
  b.style.display = n ? 'inline-block' : 'none';
}
function openComment(nodeId, nodeName, category) {
  _commentTarget = { nodeId, nodeName: nodeName.replace(/&amp;/g, '&'), category };
  document.getElementById('comment-node-badge').textContent = nodeName.replace(/&amp;/g, '&');
  document.getElementById('comment-text').value = '';
  document.getElementById('comment-modal').classList.add('open');
  setTimeout(() => document.getElementById('comment-text').focus(), 80);
}
function closeComment() {
  document.getElementById('comment-modal').classList.remove('open');
  _commentTarget = null;
}
function submitComment() {
  const txt = document.getElementById('comment-text').value.trim();
  if (!txt || !_commentTarget) return;
  const items = getComments();
  items.push({ id: Date.now().toString(), nodeId: _commentTarget.nodeId, nodeName: _commentTarget.nodeName, category: _commentTarget.category, comment: txt, timestamp: new Date().toISOString() });
  saveComments(items);
  closeComment();
  const b = document.getElementById('fb-badge');
  b.style.background = '#22c55e';
  setTimeout(() => { b.style.background = ''; }, 800);
}

let _currentModalId = null, _currentModalName = null;
function flagFromModal() {
  if (!_currentModalId) return;
  closeModal();
  const mapping = SKILL_MAP[_currentModalId];
  const category = mapping ? mapping.skill : _currentModalId;
  openComment(_currentModalId, _currentModalName || _currentModalId, category);
}

function renderFeedback() {
  const items = getComments();
  const wrap = document.getElementById('fb-content');
  const canGenerate = items.length > 0;
  let html = `<div class="fb-header"><div><div class="fb-title">💬 Feedback</div><div class="fb-sub">${items.length} issue${items.length !== 1 ? 's' : ''} reported${items.length ? ', ready to generate fix prompts' : ''}</div></div><button class="btn-generate" onclick="generatePrompts()" ${canGenerate ? '' : 'disabled'}>✨ Generate Fix Prompts</button></div>`;
  if (items.length === 0) {
    html += `<div class="fb-empty"><div class="fb-empty-icon">🐛</div><div class="fb-empty-title">No issues reported yet</div><div class="fb-empty-hint">Hover over any node on the Workflow Map and click the <strong>+</strong> button.<br>Or use the <strong>📝</strong> buttons on the Schedule tab.</div></div>`;
  } else {
    const groups = {};
    for (const item of items) { const g = item.category || 'General'; if (!groups[g]) groups[g] = []; groups[g].push(item); }
    for (const [groupName, groupItems] of Object.entries(groups)) {
      html += `<div class="fb-group-hdr">${groupName}</div>`;
      for (const item of groupItems) {
        html += `<div class="fb-card"><div class="fb-card-left"><div class="fb-node-name">${item.nodeName}</div><div class="fb-cat">${SKILL_MAP[item.nodeId] ? SKILL_MAP[item.nodeId].skill : item.category}</div><div class="fb-comment">${item.comment.replace(/</g,'&lt;').replace(/>/g,'&gt;')}</div><div class="fb-time">Submitted ${timeAgo(item.timestamp)}</div></div><button class="fb-del" onclick="deleteComment('${item.id}')" title="Delete">×</button></div>`;
      }
    }
  }
  wrap.innerHTML = html;
}
function deleteComment(id) { saveComments(getComments().filter(i => i.id !== id)); renderFeedback(); }
function timeAgo(iso) {
  const diff = Date.now() - new Date(iso).getTime(), m = Math.floor(diff / 60000);
  if (m < 1) return 'just now'; if (m < 60) return `${m} min ago`;
  const h = Math.floor(m / 60); if (h < 24) return `${h}h ago`; return `${Math.floor(h/24)}d ago`;
}

let _allPromptsText = '';
function generatePrompts() {
  const items = getComments(); if (!items.length) return;
  const groups = {};
  for (const item of items) {
    const mapping = SKILL_MAP[item.nodeId] || { skill: item.category || 'general', files: [] };
    const key = mapping.skill;
    if (!groups[key]) groups[key] = { skill: mapping.skill, filesSet: new Set(mapping.files), items: [] };
    mapping.files.forEach(f => groups[key].filesSet.add(f));
    groups[key].items.push(item);
  }
  const groupList = Object.values(groups);
  let allText = '', html = '';
  groupList.forEach((g, i) => {
    const fileLines = Array.from(g.filesSet).map(f => `  • ${f}`).join('\n');
    const issueLines = g.items.map(it => `  • [${it.nodeName}] ${it.comment}`).join('\n');
    const promptText = `Working directory: [YOUR_PROJECT_DIR]\n\nSkill(s): ${g.skill}\n\nFiles to review:\n${fileLines}\n\nIssues to fix:\n${issueLines}\n\nRead each file above, identify the root cause of every reported issue, fix the code, and output a brief summary of what you changed and why.`;
    allText += `\n\n${'─'.repeat(60)}\nPROMPT ${i+1} / ${groupList.length}  ·  ${g.skill}\n${'─'.repeat(60)}\n\n${promptText}`;
    html += `<div class="prompt-block"><div class="prompt-block-hdr"><div><div class="prompt-block-label">Prompt ${i+1} / ${groupList.length}  ·  ${g.skill}</div><div class="prompt-block-meta">${g.items.length} issue${g.items.length!==1?'s':''} · ${g.filesSet.size} file${g.filesSet.size!==1?'s':''}</div></div><button class="btn-copy" onclick="copyPrompt(${i})">Copy</button></div><div class="prompt-text">${formatPromptHtml(promptText)}</div></div>`;
  });
  _allPromptsText = allText.trim();
  document.getElementById('prompt-card-sub').textContent = `${groupList.length} prompt${groupList.length!==1?'s':''} · ${items.length} total issue${items.length!==1?'s':''}`;
  document.getElementById('prompt-list').innerHTML = html;
  document.getElementById('prompt-modal').classList.add('open');
}
function formatPromptHtml(text) {
  return text.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
    .replace(/(Working directory:|Skill\(s\):|Files to review:|Issues to fix:|Read each file.*)/g, '<span class="hi">$1</span>')
    .replace(/(  • ~[^\n]+)/g, '<span class="file">$1</span>')
    .replace(/(  • \[[^\]]+\][^\n]*)/g, '<span class="issue">$1</span>');
}
function copyPrompt(idx) {
  const blocks = document.querySelectorAll('.prompt-text');
  if (blocks[idx]) { navigator.clipboard.writeText(blocks[idx].innerText).then(() => { const btn = document.querySelectorAll('.btn-copy')[idx]; btn.textContent = 'Copied!'; setTimeout(() => btn.textContent = 'Copy', 1500); }); }
}
function copyAllPrompts() {
  navigator.clipboard.writeText(_allPromptsText).then(() => { const btn = document.querySelector('.btn-copy-all'); btn.textContent = 'Copied!'; setTimeout(() => btn.textContent = 'Copy All', 1500); });
}
function closePrompts() { document.getElementById('prompt-modal').classList.remove('open'); }

// ── SCHEDULE DATA: fill in your tasks ────────────────────
// Each section groups tasks by trigger type.
// Fields: id, icon, name, dept, deptClass, type, typeClass, time, freq, days, desc, trig
const SCHED = [
  // [GENERATE SCHED SECTIONS FROM DISCOVERED SKILLS]
  // Example auto-scheduler section:
  // { section: '⏱  Auto-Scheduled', items: [
  //   { id:'my-skill', icon:'⏰', name:'My Skill', dept:'Auto-Scheduler', deptClass:'bd-dept-auto',
  //     type:'⏱ auto', typeClass:'bd-auto', time:'8:00 AM', freq:'Once daily', days:'Mon–Fri',
  //     desc:'What this skill does.', trig:'cloud routine trig_01... (or LaunchAgent com.<yourname>....)' },
  // ]},
];

function buildSchedule() {
  const wrap = document.getElementById('sched-content');
  const allItems = SCHED.flatMap(s => s.items);
  const auto = allItems.filter(i => i.typeClass === 'bd-auto').length;
  const ext = allItems.filter(i => i.typeClass === 'bd-external').length;
  const man = allItems.filter(i => i.typeClass === 'bd-manual').length;
  const que = allItems.filter(i => i.typeClass === 'bd-queued').length;
  let html = `<div class="sched-pg-title">📅 Schedule</div>
    <div class="sched-pg-sub">Every task in the system. When it fires, how often, and what triggers it.</div>
    <div class="sched-summary">
      ${auto ? `<span class="sched-sum-pill bd-auto">${auto} auto-scheduled</span>` : ''}
      ${ext  ? `<span class="sched-sum-pill bd-external">${ext} external trigger${ext!==1?'s':''}</span>` : ''}
      ${man  ? `<span class="sched-sum-pill bd-manual">${man} manual</span>` : ''}
      ${que  ? `<span class="sched-sum-pill bd-queued">${que} queued</span>` : ''}
    </div>`;
  for (const section of SCHED) {
    html += `<div class="sched-sec-hdr">${section.section}</div>`;
    for (const t of section.items) {
      html += `<div class="sched-row">
        <div class="sched-icon">${t.icon}</div>
        <div class="sched-info">
          <div class="sched-name">${t.name}</div>
          <div class="sched-desc">${t.desc}</div>
          <div class="sched-trig">${t.trig}</div>
        </div>
        <div class="sched-mid">
          <span class="sbadge ${t.deptClass}">${t.dept}</span>
          <span class="sbadge ${t.typeClass}">${t.type}</span>
        </div>
        <div class="sched-timing">
          <div class="sched-time-main">${t.time}</div>
          <div class="sched-time-freq">${t.freq}</div>
          <div class="sched-time-days">${t.days}</div>
        </div>
        <button class="sched-cmt-btn" onclick="openComment('${t.id}','${t.name}','${t.dept}')" title="Flag issue">📝</button>
      </div>`;
    }
  }
  wrap.innerHTML = html;
}
buildSchedule();
updateBadge();

// ── DETAIL MODAL DATA ─────────────────────────────────────
// One entry per node id. icon, title, sub, body (HTML using .step/.step-ic/.step-title/.step-desc/.pill classes)
const M = {
  // [GENERATE MODAL ENTRIES FROM DISCOVERED SKILLS]
  // Example:
  // 'my-skill': { icon: '⚙️', title: 'My Skill', sub: 'What it does in one line',
  //   body: `<div class="step"><div class="step-ic">1️⃣</div><div><div class="step-title">Step one</div><div class="step-desc">Detail here.<br><span class="pill svc">External Service</span></div></div></div>` },
};

function showModal(id) {
  const d = M[id]; if (!d) return;
  _currentModalId = id; _currentModalName = d.title;
  document.getElementById('ci').textContent = d.icon;
  document.getElementById('ct').textContent = d.title;
  document.getElementById('cs').textContent = d.sub;
  document.getElementById('cb').innerHTML = d.body;
  document.getElementById('modal').classList.add('open');
}
function closeModal() { document.getElementById('modal').classList.remove('open'); }

document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') { closeModal(); closeComment(); closePrompts(); }
});
updateBadge();
</script>
</body>
</html>
```

---

## SVG layout reference: flexible by dept count

viewBox="0 0 1440 900". Center hub at x=618 y=420 w=204 h=80 rx=18 (indigo #4f46e5, white text). Center point: 720,460.

**First, count your departments. Then pick the matching layout:**

---

### 1 department
Single dept centered below the hub.
- Dept: x=560 y=600 w=200 h=52
- Leaves: spread horizontally below dept, x=360/530/700/870 y=720 (up to 4), or stack vertically

---

### 2 departments
One on each side, vertically centered with the hub.
- Left dept: x=280 y=434
- Right dept: x=980 y=434
- Leaves left: x=70 y=(dept_cy - N*38 + 19)… stacked, spacing 76px
- Leaves right: x=1195 y=same pattern
- Connectors: left dept right edge → center left edge (618,460); right dept left edge → center right edge (822,460)

---

### 3 departments
Two on top, one on the bottom.
- Top-left dept: x=290 y=230
- Top-right dept: x=990 y=230
- Bottom-center dept: x=560 y=660 w=200
- Leaves top-left: x=80, stacked y=130,210,290,370
- Leaves top-right: x=1205, stacked y=130,200,270,340,410
- Leaves bottom: x=380,540,700,860 y=780 (horizontal row below dept)
- Connectors: top-left right edge → center left (618,440); top-right left edge → center right (822,440); bottom-center top edge → center bottom (720,500)

---

### 4 departments (the default)
Two on each side.
- Top-left: x=290 y=250
- Top-right: x=990 y=250
- Bottom-left: x=290 y=618
- Bottom-right: x=990 y=618
- Leaves top-left: x=80 y=150,250,350,450
- Leaves top-right: x=1205 y=132,202,272,342,412
- Leaves bottom-left: x=80 y=528,608,688,768
- Leaves bottom-right: x=1205 y=528,608,688
- Connectors: top depts → center sides at y≈440; bottom depts → center sides at y≈470

---

### 5 departments
Two top, two bottom, one center-right (or center-left).
- Top-left: x=290 y=160
- Top-right: x=990 y=160
- Center-left: x=100 y=440 w=170 (smaller dept)
- Bottom-left: x=290 y=700
- Bottom-right: x=990 y=700
- Leaves top-left: x=80 y=60,140,220 (3 max, tight)
- Leaves top-right: x=1205 y=60,130,200,270
- Leaves center-left: x=-30… shift left, use x=0 for leaves, dept at x=190
  - Dept: x=190 y=434; leaves: x=10 y=380,460,540
- Leaves bottom-left: x=80 y=780,840 (2–3, tight)
- Leaves bottom-right: x=1205 y=780,840
- Adjust viewBox to "0 0 1440 950" if content reaches near bottom

---

### 6 departments
Three on each side, stacked vertically.
- Left-top: x=290 y=140
- Left-mid: x=290 y=390
- Left-bot: x=290 y=640
- Right-top: x=990 y=140
- Right-mid: x=990 y=390
- Right-bot: x=990 y=640
- Leaves left-top: x=80 y=80,150,220
- Leaves left-mid: x=80 y=340,410,480
- Leaves left-bot: x=80 y=580,650,720,790
- Leaves right-top: x=1205 y=80,150,220
- Leaves right-mid: x=1205 y=340,410,480
- Leaves right-bot: x=1205 y=580,650,720
- Connectors: each dept's edge nearest center connects to center hub edge, roughly at the dept's vertical midpoint

---

### 7 departments
Three left, three right, one bottom-center.
- Left 3: x=290 y=140/370/600
- Right 3: x=990 y=140/370/600
- Bottom-center: x=560 y=760 w=200
- Leaves: same pattern as 6-dept but compress vertical spacing to 60px per leaf
- Bottom dept leaves: 2–3 nodes spread horizontally below it
- Use viewBox="0 0 1440 980"

---

### 8 departments
Four on each side.
- Left: x=290 y=110/290/480/670
- Right: x=990 y=110/290/480/670
- Each dept gets max 2–3 leaf nodes (space is tight)
- Compress leaf spacing to 55px
- Use viewBox="0 0 1440 980"
- Consider reducing leaf node height to 40 (rx=8) to fit

---

## Node dimensions

| Node type | width | height | rx | font-size title | font-size sub |
|-----------|-------|--------|----|-----------------|---------------|
| Center hub | 204 | 80 | 18 | 17 | 10 |
| Dept node | 160 | 52 | 13 | 13 | 9.5 |
| Leaf node | 155 | 46 | 10 | 11 | 9 |

For 7–8 depts with many leaves, shrink leaf to w=145 h=40 rx=8.

---

## Department color palette

Assign colors in this order (reuse if >8 depts):
1. Amber: fill=#fef3c7 stroke=#d97706 text=#78350f sub=#a16207, leaf fill=#fffbeb leaf-stroke=#fcd34d leaf-text=#78350f leaf-sub=#a16207
2. Green: fill=#d1fae5 stroke=#059669 text=#064e3b sub=#065f46, leaf fill=#ecfdf5 leaf-stroke=#6ee7b7 leaf-text=#064e3b leaf-sub=#047857
3. Pink: fill=#fce7f3 stroke=#db2777 text=#831843 sub=#9d174d, leaf fill=#fff1f2 leaf-stroke=#fca5a5 leaf-text=#9f1239 leaf-sub=#be123c
4. Blue: fill=#e0f2fe stroke=#0284c7 text=#0c4a6e sub=#075985, leaf fill=#f0f9ff leaf-stroke=#7dd3fc leaf-text=#0c4a6e leaf-sub=#0369a1
5. Violet: fill=#ede9fe stroke=#7c3aed text=#3b0764 sub=#5b21b6, leaf fill=#f5f3ff leaf-stroke=#c4b5fd leaf-text=#3b0764 leaf-sub=#6d28d9
6. Orange: fill=#ffedd5 stroke=#ea580c text=#431407 sub=#9a3412, leaf fill=#fff7ed leaf-stroke=#fdba74 leaf-text=#431407 leaf-sub=#c2410c
7. Teal: fill=#ccfbf1 stroke=#0d9488 text=#042f2e sub=#0f766e, leaf fill=#f0fdfa leaf-stroke=#5eead4 leaf-text=#042f2e leaf-sub=#0f766e
8. Rose: fill=#ffe4e6 stroke=#e11d48 text=#4c0519 sub=#881337, leaf fill=#fff1f2 leaf-stroke=#fda4af leaf-text=#4c0519 leaf-sub=#be123c

---

## Connector rules

**Dept → center** (stroke=#cbd5e1 stroke-width=2.5 stroke-linecap=round):
- Left-side dept: connect dept's right edge midpoint → center's left edge (x=618) at matching y
- Right-side dept: connect dept's left edge midpoint → center's right edge (x=822) at matching y
- Bottom-center dept: connect dept's top edge midpoint → center's bottom edge (y=500) at x=720
- For 6+ depts on same side: connect to the center edge at the dept's own vertical midpoint

**Leaf → dept** (stroke = dept's stroke color, stroke-width=1.8 stroke-linecap=round):
- Left-column leaves: leaf right edge (x=235) → dept left edge (x=290) at leaf's cy
- Right-column leaves: leaf left edge (x=1205) → dept right edge (x=1150) at leaf's cy
- Bottom-row leaves: leaf top edge → dept bottom edge

---

## Comment `+` button on every node

Every `<g class="dept-node">`, `<g class="leaf-node">`, and `<g class="center-node">` must have a nested `<g class="comment-btn">` as its last child:

```svg
<g class="comment-btn" onclick="event.stopPropagation();openComment('node-id','Node Name','Dept Name')">
  <circle cx="[rect.x + rect.width - 5]" cy="[rect.y + 9]" r="9" fill="white" stroke="[dept-stroke-color]" stroke-width="1.5"/>
  <text x="[same cx]" y="[cy+4]" text-anchor="middle" font-size="12" fill="[dept-text-color]" font-weight="700">+</text>
</g>
```

The `cx` = node rect x + node rect width − 5 (places it at the right edge of the rect). The `cy` = node rect y + 9.

---

## Quality checklist before writing the file

- [ ] All `[PLACEHOLDER]` tokens replaced
- [ ] Number of dept nodes matches what was discovered (not forced to 4)
- [ ] Layout coordinates match the correct layout table for the actual dept count
- [ ] No nodes overlap, minimum 20px gap between any two rects
- [ ] All content fits inside the viewBox (adjust viewBox height for 7–8 dept layouts)
- [ ] SKILL_MAP has an entry for every node id used in the SVG `onclick` calls
- [ ] SCHED has at least one section with one item
- [ ] M (detail modal data) has an entry for every node id used in `showModal()` calls
- [ ] Every leaf/dept/center node `onclick` calls `showModal('id')` with an id that exists in M
- [ ] Every node has a `+` comment button as its last child `<g class="comment-btn">`
- [ ] Every comment `+` button calls `openComment('id','Name','Category')`, ids match SKILL_MAP or use the dept name as category
- [ ] File paths in SKILL_MAP point to real locations on the teammate's system
- [ ] The `[YOUR_PROJECT_DIR]` placeholder in the prompt template is replaced with the actual working directory
- [ ] Connector lines terminate at actual node edges (not at centers or random coords)
- [ ] No orphaned connector lines (every line connects two nodes that actually exist)
