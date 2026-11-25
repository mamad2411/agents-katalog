---
name: chaoxing-public
description: Use when automating 学习通 (Chaoxing/SuperStar MOOC) platform tasks — course/task scanning, homework submission, exam status auditing, and automated workflows. Connects via browser relay (Chrome Relay or similar) to the user's logged-in browser. Covers reliability patterns: hidden-input verification, AJAX wait, DOM re-query, QID randomization, and automatic failure recovery.
version: 2.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [chaoxing, xuexitong, exam, homework, education, automation, browser-relay]
    related_skills: []
---

# 学习通 (Chaoxing) Automation Skill

## Overview

Automates 学习通 (超星学习通 / SuperStar MOOC) platform interactions using a browser relay (Chrome Relay, OpenClaw browser tools, or similar) connected to the user's logged-in browser. This skill covers:

- **Status scanning**: batch-check all courses for pending homework/exams
- **Homework submission**: auto-fill rich-text or attachment homework and submit
- **Exam workflows**: entry, question extraction, auto-answer, submit, score verification
- **Reliability patterns**: hidden-input verification, AJAX sync waiting, DOM re-query after mutations, QID randomization handling
- **Failure recovery**: detect low scores / empty answers, identify retake availability, auto-retry with corrected approach

**Design philosophy**: Browser-first. Never attempt direct HTTP API calls (the `uf` cookie is TLS-fingerprint-bound). All interactions go through the user's existing browser session via a relay. No external API keys are required for core workflows (CAPTCHA solving is optional and pluggable).

## When to Use

- Automating 学习通 homework/assignment submission
- Scanning courses for pending tasks and auditing completion status
- Batch-answering exams with reliability verification
- Debugging why submissions failed (empty answers, lost saves, low scores)
- Building an agent that maintains a student's 学习通 account

**Don't use for:**
- Platforms other than 学习通 (智慧树/知到 uses different APIs)
- Tasks that require human judgment (essay grading, creative writing evaluation)
- Direct API access (always go through browser relay)

## Platform Architecture

### Key URL Patterns

| Page | URL Pattern |
|------|-------------|
| Personal Space | `https://i.chaoxing.com/base` |
| Course List | `https://mooc2-ans.chaoxing.com/mooc2-ans/mycourse/stu` |
| Course Page | `https://mooc2-ans.chaoxing.com/mooc2-ans/mycourse/stu?courseid={id}&clazzid={id}` |
| Exam List (per course) | `https://mooc1.chaoxing.com/exam-ans/mooc2/exam/exam-list?courseid={id}&clazzid={id}&cpi={cpi}&ut=s` |
| Exam Test | `https://mooc1.chaoxing.com/exam-ans/exam/test/examcode/examnotes?courseId={id}&...` |
| Exam Preview | `https://mooc1.chaoxing.com/exam-ans/mooc2/exam/preview?courseId={id}&classId={id}` |
| Homework List (per course) | `https://mooc1.chaoxing.com/mooc2/work/list?courseId={id}&classId={id}&enc={enc}` |
| Homework Task | `https://mooc1.chaoxing.com/mooc-ans/mooc2/work/task?courseId={id}&workId={id}&answerId={id}&enc={enc}` |
| Homework Editor | `https://mooc1.chaoxing.com/mooc-ans/mooc2/work/dowork?courseId={id}&...&standardEnc={enc}` |

### Auth & Session

- The `uf` cookie is browser-fingerprint-bound — direct HTTP calls fail
- Always use browser relay (Chrome Relay / Playwright CDP / OpenClaw browser tools)
- The `enc` parameter is session-bound and expires; capture it fresh per session

### Navigation (SPA)

The base page is a Single Page Application. Course content loads in an iframe (`#frame_content`). Sidebar navigation items use CSS IDs:
- 课程: `#first2257786`
- 考试: `#first222318`

---

## Workflow 1: Full Status Scan (Homework + Exams)

### Step 1: Collect Course Inventory

Build a course inventory with `courseId` and `clazzId` for each course. This can be extracted from the course list page or maintained as a config file (see `examples/course-inventory.example.json`).

### Step 2: Batch-Scan Exam Lists

From any `mooc1.chaoxing.com` page, use same-origin `fetch()` to check all courses:

```javascript
async function checkAllExams(courses) {
  var results = [];
  for (var c of courses) {
    var url = 'https://mooc1.chaoxing.com/exam-ans/mooc2/exam/exam-list?courseid='
      + c.courseId + '&clazzid=' + c.clazzId + '&cpi=' + c.cpi + '&ut=s';
    var resp = await fetch(url, {credentials: 'include'});
    var html = await resp.text();
    // CRITICAL: strip <script> tags before parsing — JS templates may contain false keyword matches
    var clean = html.replace(/<script[\s\S]*?<\/script>/g, '');
    var bodyText = clean.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
    var hasNoExam = bodyText.indexOf('暂无考试') > -1;
    results.push({name: c.name, noExam: hasNoExam});
  }
  return results;
}
```

**Status indicators** in the parsed text:
- `待做` = pending, needs to be done
- `未开始` = not yet started
- `已完成` = completed
- `已过期` = expired
- `暂无考试` = no exams

### Step 3: Batch-Scan Homework Lists

Homework lists require an `enc` parameter from the course page. Navigate to each course, click the 作业 tab, capture the iframe URL, then parse items:

```javascript
// From course page, get homework iframe URL
var iframeSrc = document.querySelector('iframe[id*=zy]')?.src;

// Navigate to that URL, then extract items:
var items = [];
document.querySelectorAll('li').forEach(function(li) {
  var dataUrl = li.getAttribute('data');
  if (dataUrl) {
    var text = li.innerText.trim();
    items.push({
      name: text.split('\n')[0],
      status: text.includes('未交') ? 'pending' :
              text.includes('待批阅') ? 'submitted' :
              text.includes('已完成') ? 'done' : 'unknown',
      url: dataUrl
    });
  }
});
```

### Step 4: Classify Each Pending Task

For each pending homework URL, do a same-origin `fetch()` to check if it's still submittable:

```javascript
async function classifyTask(url) {
  var resp = await fetch(url, {credentials: 'include', redirect: 'follow'});
  var html = await resp.text();
  var doc = new DOMParser().parseFromString(html, 'text/html');
  doc.querySelectorAll('script,style').forEach(n => n.remove());
  var text = (doc.body?.innerText || '').replace(/\s+/g, ' ');
  var status = 'unknown';
  if (resp.url.includes('/work/prompt') || /提交成功|等待教师批阅/.test(text))
    status = 'submitted_prompt';
  else if (resp.url.includes('/work/view') || /作业详情|我的答案|正确答案/.test(text))
    status = 'submitted_view';
  else if (resp.url.includes('/work/dowork') || /暂时保存|提交 作业|作业作答/.test(text))
    status = 'needs_submit';
  return {status, finalUrl: resp.url};
}
```

---

## Workflow 2: Homework Submission

### Type A: Rich-Text / Attachment (UEditor)

Many courses use UEditor (百度富文本编辑器). The editor iframe ID is `#ueditor_0` (or `#ueditor_1`, etc. for multi-question).

**Fill content:**
```javascript
var iframe = document.querySelector('#ueditor_0');
if (iframe) {
  var doc = iframe.contentDocument || iframe.contentWindow.document;
  doc.body.innerHTML = '<p>Answer content here...</p>';
  var ta = document.querySelector('textarea');
  if (ta) ta.value = doc.body.innerHTML;
}
```

**Upload attachments:**
```javascript
// Use the page's upload API. Extract form action and token:
var formAction = document.querySelector('#submitForm')?.getAttribute('action');
var token = document.querySelector('input[name="token"]')?.value;
// Upload via FormData to the action URL
```

### Type B: Quiz/Test (Clickable Options)

Same structure as exams — `.questionLi` containers with `.answerBg` clickable options.

### Submit Pattern (Two-Step)

The submit button is an `<a role="button">` with text "提交". A confirmation dialog appears with a second "提交":

```javascript
// Step 1: Click the submit button
document.querySelector('[role="button"]').click();

// Step 2: Wait for dialog, then click confirm
setTimeout(function() {
  document.querySelectorAll('a, button').forEach(function(b) {
    if (b.innerText?.trim() === '提交' && b.getBoundingClientRect().height > 0) b.click();
  });
}, 1000);
```

**Verify submission:**
```javascript
// After submit, the page should navigate to /work/prompt
// with text "提交成功" / "等待教师批阅"
```

---

## Workflow 3: Exam Entry

### Entry Flow

```
Exam list page → goTest() opens new tab → examnotes page →
agree checkbox → start button → confirm dialog → (CAPTCHA) → exam page
```

### Programmatic Entry

```javascript
// From exam list page, extract goTest() parameters from the page HTML:
var match = html.match(/goTest\('(\d+)','(\d+)',(\d+),'([^']*)','(\d+)',(\w+),'([^']*)'\)/);

// Call goTest() — new tab opens
goTest(courseId, examId, 0, endTime, paperId, false, enc);
```

### Agreement + Start

```javascript
// Click the agreement div (not a real checkbox)
document.querySelector('.face_agreement').click();

// Click the start button (enabled after agreement)
document.querySelector('#startBtn').click();

// Confirm dialog: find and click "进入考试" or "开始重考"
// Note: there may be duplicate buttons — click the LAST visible one
var targets = [];
document.querySelectorAll('*').forEach(function(el) {
  if ((el.innerText?.trim() === '进入考试' || el.innerText?.trim() === '开始重考')
      && el.children.length === 0) targets.push(el);
});
if (targets.length >= 2) targets[targets.length - 1].click();
```

---

## Workflow 4: Answer Injection (Exam)

### ⚠️ CRITICAL — Three Failure Modes

See `references/reliability-pitfalls.md` for detailed explanation and fixes. Quick summary:

1. **saveSingleSelect not global** — use `bg.click()` instead of calling directly
2. **AJAX answer sync** — wait 5+ seconds after answering before submitting
3. **DOM reference staleness** — re-query by ID after each click

### The Correct Answering Pattern

```javascript
// 1. Load all questions
topreview();

setTimeout(function() {
  // 2. Collect QIDs in DOM order (never hardcode — random per retake)
  var singleQids = [], multiQids = [], map = {};
  document.querySelectorAll('.answerBg').forEach(function(bg) {
    var oc = bg.getAttribute('onclick') || '';
    var m1 = oc.match(/saveSingleSelect\(this,\s*'([^']+)'\)/);
    var m2 = oc.match(/clickSaveMultiSelect\(this,\s*'([^']+)'\)/);
    if (m1 && !singleQids.includes(m1[1])) singleQids.push(m1[1]);
    if (m2 && !multiQids.includes(m2[1])) multiQids.push(m2[1]);
  });

  // 3. Map answers by index to collected QIDs
  var singleAnswers = ['A','B','C',...]; // from question extraction
  var multiAnswers = ['ABC','BCD',...];
  for (var i = 0; i < singleQids.length; i++) map[singleQids[i]] = singleAnswers[i];
  for (var i = 0; i < multiQids.length; i++) map[multiQids[i]] = multiAnswers[i];

  // 4. Answer using bg.click() — NOT direct function calls
  document.querySelectorAll('.answerBg').forEach(function(bg) {
    var oc = bg.getAttribute('onclick') || '';
    var m1 = oc.match(/saveSingleSelect\(this,\s*'([^']+)'\)/);
    var m2 = oc.match(/clickSaveMultiSelect\(this,\s*'([^']+)'\)/);
    var q = m1 ? m1[1] : (m2 ? m2[1] : null);
    if (!q || !map[q]) return;
    var label = bg.querySelector('span')?.innerText?.trim() || '';
    if ((m1 && label === map[q]) || (m2 && map[q].includes(label))) bg.click();
  });

  // 5. CRITICAL: Wait for AJAX sync, then verify hidden inputs
  setTimeout(function() {
    // Verify: hidden input values must NOT be '0' or empty
    var ok = 0;
    document.querySelectorAll('div.questionLi').forEach(function(q) {
      var hi = q.querySelector('input[id^=answer]');
      if (hi && hi.value && hi.value !== '0') ok++;
    });
    console.log('Verified: ' + ok + '/' + totalQuestions);

    // 6. Submit if all verified
    if (ok === totalQuestions) {
      document.querySelector('.completeBtn')?.click(); // or finalSubmit()
      setTimeout(function() {
        // Confirm dialog
        document.querySelectorAll('a, button').forEach(function(b) {
          if (b.innerText?.trim() === '确定') b.click();
        });
      }, 1500);
    }
  }, 5000);
}, 2000);
```

### Sequential Single-Question Save (for per-question exams)

When questions appear one at a time, use this async loop:

```javascript
(async function() {
  function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }
  async function waitAjax(maxMs) {
    var start = Date.now();
    while (window.jQuery && jQuery.active > 0 && Date.now() - start < maxMs)
      { await sleep(80); }
    await sleep(120);
  }

  var answers = ['A','B','C',...]; // pre-computed per-question answers

  for (var i = 0; i < answers.length; i++) {
    // Answer current question
    document.querySelectorAll('.answerBg').forEach(function(bg) {
      var label = bg.querySelector('span')?.innerText?.trim()?.charAt(0);
      if (label === answers[i]) bg.click();
    });
    await waitAjax(3000);

    // Navigate to next question (or submit on last)
    if (i < answers.length - 1) {
      document.querySelectorAll('a').forEach(function(a) {
        if (a.innerText?.trim() === '下一题') a.click();
      });
      await sleep(800);
    }
  }

  await waitAjax(5000);
  // Submit from last question or preview page
})();
```

### QID Randomization (CRITICAL)

Each exam retake generates **completely new QIDs**. Never hardcode QIDs across attempts. Always collect from the current page in DOM order and map answers by index.

---

## Workflow 5: Score Verification & Retake

### Verify Scores

After submission, check the result page or detail page:

```javascript
// From exam detail page (after submit)
var scoreMatch = document.body.innerText.match(/(\d+(?:\.\d+)?)\s*分/);
var score = scoreMatch ? parseFloat(scoreMatch[1]) : null;

// Check for empty answers (空选)
var emptyAnswers = [];
document.querySelectorAll('.answerBg, .questionLi').forEach(function(q) {
  if (q.innerText.includes('我的答案:') && !q.innerText.match(/我的答案:\s*[A-E对错]/))
    emptyAnswers.push(q);
});
```

### Check Retake Availability

```javascript
// From exam list, check if retake button exists
var retakeBtn = document.querySelector('[onclick*="reTest"]');
var retakeAvailable = retakeBtn !== null;

// Check remaining time
var timeMatch = document.body.innerText.match(/剩余\s*(\d+)\s*小时/);
var hoursRemaining = timeMatch ? parseInt(timeMatch[1]) : 0;
```

### Retake Strategy

1. Detect low score (< passing threshold) or empty answers
2. Check if retake button exists and time remains
3. If available: click retake → re-enter exam → re-extract questions (QIDs changed!) → re-answer → resubmit
4. If not available: mark as "unfixable" (no retake entry or expired)

---

## CAPTCHA Handling

The exam-entry CAPTCHA is a slider puzzle (`captcha.chaoxing.com`). It's the only manual-interaction step in the exam pipeline.

**Two solving approaches:**

1. **Fully automated** via Capsolver backend pipeline (requires API key, **minimum $6 top-up, no free tier**)
2. **Manual fallback** via Playwright CLI headed browser (user completes slider, **free**)

### Quick Start — Playwright CLI (Recommended for Claude Code, Open Code, etc.)

For agents **without** built-in browser control (Claude Code, Open Code, etc.), use the Playwright CLI solution:

```bash
# Install Playwright CLI (one-time)
npm install -g @playwright/cli
playwright install chromium

# Manual mode: opens headed browser, user completes slider
python scripts/playwright_captcha.py --manual --url "<examnotes_url>"

# Auto mode: uses Capsolver API (requires key)
export CAPSOLVER_KEY="CAP-..."
python scripts/playwright_captcha.py --auto --url "<examnotes_url>"
```

### Quick Start — Chrome Relay (For OpenClaw, Hermes, etc.)

For agents **with** built-in browser control (OpenClaw, Hermes, etc.), use the Capsolver pipeline directly:

> ⚠️ Capsolver requires minimum $6 top-up (no free tier). For a free option, use Playwright CLI above.

```bash
# Set your Capsolver key
export CAPSOLVER_KEY="CAP-..."

# Run from terminal (requires Chrome Relay running)
python scripts/captcha_pipeline.py <examnotes_tab_id>
```

### When to Use Which Approach

| Agent Type | Browser Control | Recommended Approach |
|------------|----------------|---------------------|
| Claude Code | None (Playwright CLI available) | `playwright_captcha.py --manual` |
| Open Code | None (Playwright CLI available) | `playwright_captcha.py --manual` |
| OpenClaw | Built-in browser tools | `captcha_pipeline.py` + Chrome Relay |
| Hermes | Built-in browser tools | `captcha_pipeline.py` + Chrome Relay |
| Custom Agent | Varies | Choose based on available tools |

### Playwright CLI Workflow

The `playwright_captcha.py` script provides two modes:

**Manual Mode** (`--manual`):
1. Opens a headed Chrome browser via Playwright CLI
2. Navigates to the exam page
3. User completes the slider CAPTCHA manually
4. Script detects when verification is complete
5. Returns control to the calling agent

**Auto Mode** (`--auto`):
1. Opens a headless browser
2. Extracts CAPTCHA ID from the page
3. Calls `captcha_pipeline.py` to solve via Capsolver
4. Injects the validation token
5. Triggers exam entry

### Capsolver Pipeline Architecture

```
Browser Page                    Backend Pipeline
─────────────                   ────────────────
showCXCaptcha()
  ↓
fetch conf → captchaId ─────→  Step 1: Get server time
fetch image → bg+sm URLs ───→  Step 2: Get image token + URLs
                                Step 3: Download images (RAW format)
                                Step 4: Capsolver VisionEngine → distance
                                Step 5: CAPTCHA verify API → validate token
                                Step 6: Return validate ←
  ↓
Inject validate into page
  ↓
jumpExam('true') → enter exam
```

### Pipeline Architecture

```
Browser Page                    Backend Pipeline
─────────────                   ────────────────
showCXCaptcha()
  ↓
fetch conf → captchaId ─────→  Step 1: Get server time
fetch image → bg+sm URLs ───→  Step 2: Get image token + URLs
                                Step 3: Download images (RAW format)
                                Step 4: Capsolver VisionEngine → distance
                                Step 5: CAPTCHA verify API → validate token
                                Step 6: Return validate ←
  ↓
Inject validate into page
  ↓
jumpExam('true') → enter exam
```

### jumpExam Flow

```
examCheck=0, captchaCheck=0 → skip CAPTCHA → reTestAction → exam
     ↑
     │ (after injecting real validate token)
```

### CAPTCHA Bypass (Retakes Only)

Setting `examCheck=0` + `captchaCheck=0` skips the CAPTCHA UI, but the server may reject first entries with "无权限访问". For retakes specifically, `reVersionReTest` AJAX often bypasses CAPTCHA checks:

```javascript
document.querySelector('#examCheck').value = '0';
document.querySelector('#captchaCheck').value = '0';
jumpExam('true'); // 'true' = retake flow
```

---

## Browser Relay Integration

### Playwright CLI (Universal — Claude Code, Open Code, etc.)

For agents without built-in browser control, use Playwright CLI:

```bash
# Install (one-time)
npm install -g @playwright/cli
playwright install chromium

# Open browser (headed for manual work, headless for automation)
playwright-cli open --browser=chrome "<url>"  # headed
playwright-cli open "<url>"                    # headless

# Navigate
playwright-cli goto "<url>"

# Execute JS
playwright-cli eval "return document.title"

# Click by ref (from snapshot)
playwright-cli click <ref>

# Get page snapshot
playwright-cli snapshot

# Take screenshot
playwright-cli screenshot

# Close browser
playwright-cli close
```

**Advantages:**
- No external relay server needed
- Works with any agent that can run shell commands
- Supports both headed (manual) and headless (automated) modes
- Built-in snapshot/eval for DOM interaction

### Chrome Relay (Edge)

The relay CLI connects to the user's existing browser:

```bash
# List tabs
node "$HOME/.chrome-relay/cli-edge-12123.js" tabs

# Navigate
node "$HOME/.chrome-relay/cli-edge-12123.js" navigate --tab <id> "<url>"

# Execute JS (returns via console)
node "$HOME/.chrome-relay/cli-edge-12123.js" js --tab <id> "return document.title"

# Click by selector
node "$HOME/.chrome-relay/cli-edge-12123.js" click --tab <id> "<selector>"
```

### OpenClaw / Browser Tools

When using OpenClaw or similar agent frameworks with built-in browser tools, use the equivalent operations:
- `browser_navigate` → navigate
- `browser_snapshot` / `browser_click` → read page and click
- `browser_console` with expression → evaluate JS
- `browser_vision` → screenshot for visual inspection

---

## Reliability Patterns

See `references/reliability-pitfalls.md` for the full catalog. Key takeaways:

| Pitfall | Detection | Fix |
|---------|-----------|-----|
| Empty single-choice answers | Score << expected after submit | Use `bg.click()`, wait 5s for AJAX before submit |
| Stale DOM references | Only Q1 answered | Re-query via `getElementById()` after each click |
| QID mismatch on retake | Wrong answers on detail page | Always collect QIDs from current page in DOM order |
| CSS-only verification | `check_answer` class set but hidden input = "0" | Verify `input[id^=answer].value` not CSS class |
| iframe content invisible | Cross-origin blocks content access | Navigate to iframe src URL directly |
| Expired homework | "未交" but deadline passed | Check for "已过期" text before attempting submit |
| False status matches | Script templates contain keywords | Strip `<script>` blocks before text search |\n\n---\n\n## Workflow 6: Document/PPT Auto-Complete\n\nFor document-type task points (PPTX, DOC, PDF) that require \"viewing\" to complete:\n\n### Method A: Scroll-to-Bottom (Single Section)\n\n```javascript\nvar inner = document.querySelector('iframe#iframe')\n    .contentDocument.querySelector('iframe.ans-attach-online');\nvar sf = inner.contentDocument.querySelectorAll('iframe')[1]; // screen/file iframe\nsf.contentDocument.body.scrollTop = sf.contentDocument.body.scrollHeight;\nsf.contentDocument.body.dispatchEvent(new Event('scroll', {bubbles: true}));\ninner.contentWindow.finishJob();\n```\n\n### Method B: job/document API (Most Reliable)\n\nNavigate the tab directly to the API URL:\n```\nhttps://mooc1.chaoxing.com/mooc-ans/job/document?jobid={jobid}\n  &knowledgeid={kid}&courseid={cid}&clazzid={clid}\n  &jtoken={jtoken}&checkMicroTopic=true&microTopicId=&courseEngineInfo=false\n```\n\nExtract `jobid`, `jtoken`, `knowledgeid` from `mArg.attachments` and `mArg.defaults` in the knowledge cards iframe.\n\n### Multi-Section Chapters (板块)\n\nChapters may have multiple sections shown as tabs (e.g., \"PPT\", \"jupyter代码\", \"nltk相关语\"). Each section has its own task points.\n\n**Detect sections**: Look for `changeDisplayContent` in the studentstudy page onclick handlers.\n\n**Navigate sections**:\n```javascript\n// Switch to section 4 of 4\nchangeDisplayContent(4, 4, '{knowledgeId}', '{courseId}', '{clazzId}', '');\n// Then extract mArg.attachments for each section and call job/document API\n```\n\n---\n\n## Workflow 7: Video Auto-Complete\n\n```javascript\nvar inner = document.querySelector('iframe#iframe')\n    .contentDocument.querySelector('iframe.ans-insertvideo-online');\nvar v = inner.contentDocument.querySelector('video');\nv.load();         // force metadata load\nv.muted = true;\nv.play();         // start playback\n// Wait ~15s for video to finish (duration typically ~60s)\n// On 'ended' event:\ninner.contentWindow.ed_complete();\n```\n\n---\n\n## Verification Checklist

- [ ] Browser relay is connected and can access 学习通 pages
- [ ] Course inventory has valid courseId/clazzId for target courses
- [ ] Scanning strips `<script>` tags before keyword matching
- [ ] Homework submission verified by re-fetching the task page
- [ ] Exam answers verified via hidden input values (not CSS)
- [ ] AJAX wait period respected before submitting
- [ ] QIDs collected fresh from current page (not cached from prior attempt)
- [ ] Retake availability checked (button exists + time remaining)
- [ ] Low scores auto-flagged for retake or marked as unfixable

---

## Reference Files

- `references/captcha-solving.md` — **Complete CAPTCHA slider auto-solve pipeline** (Capsolver + verify API + jumpExam reverse-engineering)
- `references/browser-relay-patterns.md` — Browser relay integration patterns
- `references/homework-workflow.md` — Detailed homework submission pipeline
- `references/exam-status-audit.md` — Batch scanning and status classification
- `references/reliability-pitfalls.md` — Full pitfall catalog with detection and fixes
- `references/privacy-sanitization.md` — How to sanitize personal data before sharing

## Scripts

- `scripts/captcha_pipeline.py` — **CAPTCHA auto-solve backend pipeline** (conf → image → Capsolver → verify → inject) — requires Chrome Relay
- `scripts/playwright_captcha.py` — **Playwright CLI CAPTCHA solution** (manual + auto modes) — for Claude Code, Open Code, etc.
- `scripts/scan_homework_status.py` — Batch-scan homework status across courses
- `scripts/verify_submission.py` — Verify submission status via same-origin fetch
- `scripts/relay_helpers.py` — Browser relay helper functions (Chrome Relay / OpenClaw)

## Examples

- `examples/course-inventory.example.json` — Template for course inventory config
- `examples/config.example.yaml` — Configuration template with placeholders
