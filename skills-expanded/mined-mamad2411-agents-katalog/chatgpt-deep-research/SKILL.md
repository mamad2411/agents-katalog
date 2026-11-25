---
name: chatgpt-deep-research
description: Use this skill when you need to launch, continue, or inspect a ChatGPT Deep Research run in the browser, including prompt entry, plan start, notification checks, and result extraction.
---

# ChatGPT Deep Research

Use this skill when the task is any of the following:

- start a new ChatGPT Deep Research query in the browser
- continue a partially prepared Deep Research run and press `Start`
- confirm whether ChatGPT notifications will fire for a long-running research job
- extract the completed report text or key findings from a Deep Research result
- check whether ChatGPT exposes an alert, watch, or follow-up mechanism for a research topic

Do not use this skill for general web research outside ChatGPT. This workflow is specifically for operating ChatGPT's own Deep Research UI.

## Workflow

1. Open `https://chatgpt.com/` and confirm whether the user is already logged in.
2. If not logged in, navigate to the login flow and stop at the point where user authentication is required.
3. Open `Deep research` either from the sidebar or via `https://chatgpt.com/deep-research`.
4. Enter the user's prompt in the main Deep Research textbox.
5. If ChatGPT shows a plan review step, inspect it briefly and press `Start`.
6. For long-running jobs, check `Settings > Notifications > Responses` and confirm whether `Push` is enabled.
7. When the job completes, capture:
   - completion state
   - elapsed time
   - citation count if shown
   - key findings or the relevant extracted text
8. If the user asks whether alerts exist, inspect:
   - conversation options
   - Deep Research page controls
   - `Settings > Notifications`
   and distinguish between `completion notifications` and `saved search / topic alerts`.

## Extraction Notes

- Deep Research results usually render inside nested iframes. If the visible snapshot is truncated, use `browser_run_code` and inspect `page.frames()` to extract text from inner frames.
- When summarizing, prefer:
  - budget totals
  - named contractors
  - contract amounts or upper limits
  - dates and periods
  - official source counts or citation counts
- If the browser session resets, reopen the conversation URL directly before concluding the result is missing.

## Prompt Pattern

When the user wants a procurement-oriented report, ask ChatGPT for:

- target scope
- date range
- required columns
- primary sources only
- separation of confirmed facts vs inference

Example structure:

```text
<topic> に限定して調査してください。対象は <entities>、期間は <years> です。各案件について、発注主体、案件名、年度、調達方式、受託先、契約額または上限額、契約期間、業務範囲、一次資料URLを表で整理してください。一次資料が確認できない推測は分けて記載してください。
```

## Validation

Before telling the user the run is complete, verify all of the following:

- the conversation has a stable `https://chatgpt.com/c/...` URL
- the report shows a completed state rather than `Researching...`
- the summary you provide matches text visible in the rendered report
- any notification claim is based on a visible setting, not assumption
