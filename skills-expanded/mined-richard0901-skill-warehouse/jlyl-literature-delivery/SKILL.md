---
name: jlyl-literature-delivery
description: "Use when Codex needs to obtain a literature PDF and normal routes failed: Open Access/full-text links are unavailable, AI4Scholar cannot download it, or an authorized institutional/source workflow is needed as a last resort. Uses the JLYL literature delivery site through the Browser Use plugin with user-provided credentials or an existing logged-in session."
---

# JLYL Literature Delivery

## Overview

Use this skill as the final authorized-access fallback for literature PDF retrieval. The JLYL site accepts DOI, PMID, PMCID, titles, or links through its "文献传递" form and then processes requests automatically or by staff review.

Do not store account passwords, CAPTCHA answers, or downloaded copyrighted PDFs inside the skill. Do not automate Sci-Hub or any paywall-bypass route; limit this workflow to Open Access sources, AI4Scholar-supported sources, and the user's authorized JLYL account/session.

## Workflow

1. Try ordinary legal sources first: publisher full text, PubMed/PMC, DOI landing page, arXiv/bioRxiv/medRxiv, institutional links already available to the user, and Open Access mirrors.
2. If the user invoked `$ai4scholar` or the task is literature-focused, run the relevant AI4Scholar lookup/download route before JLYL.
3. Use JLYL only when earlier routes fail or the user explicitly asks to use JLYL.
4. Open `https://jlyl.jlss.vip/jss/#/helpCenter` with Browser Use.
5. If not logged in, use the user's provided credentials for this site or ask the user to log in. If a CAPTCHA appears, stop and ask the user to solve it in the browser; do not read, solve, bypass, or guess CAPTCHA text.
6. After login, click "文献传递" if the page is not already there.
7. On the "文献传递" page, paste one request per line into the main textbox. Prefer DOI or PMID. Use PMCID, exact title, or article URL only when DOI/PMID is unavailable.
8. Submit the request. If the page redirects or shows a confirmation, verify that submission succeeded.
9. Open "个人中心-文献传递列表" to check status. If the request is pending, tell the user it has been submitted and may need robot or manual processing.
10. If a download button/link is available for the requested item, download the PDF to the user-requested folder or the current task folder. Use a clear filename containing first author or short title plus year when available.
11. Verify the downloaded file exists and is a readable PDF before claiming success.

## Browser Notes

- The public entry page observed on 2026-04-28 shows a "文献传递" form with a textbox placeholder: "在此粘贴文献信息（支持批量，请一行一条）".
- The site says requests can be submitted in batches, one demand per line.
- User-confirmed usage: after login, click "文献传递", then input DOI or PMID.
- The site recommends DOI over PMID over title over link; prefer DOI/PMID for reliability.
- After submission, the site says status can be checked in "个人中心-文献传递列表".
- Login may require username, password, and image CAPTCHA. CAPTCHA is an explicit handoff point to the user.

## AI4Scholar Integration

When the user gives a title or identifier but has not already checked AI4Scholar, use the narrowest applicable AI4Scholar tool first:

```bash
node /Users/rr/.codex/skills/ai4scholar/scripts/ai4scholar.js search_semantic_paper_match '{"query":"<title or DOI>"}'
```

Use the returned DOI, PMID, PMCID, arXiv ID, or publisher URL to improve the JLYL request. If AI4Scholar can directly retrieve an Open Access/preprint PDF, use that instead of JLYL.

## Completion Report

Report:

- The source path used: Open Access, AI4Scholar, or JLYL.
- The identifier submitted, such as DOI or PMID.
- Whether JLYL returned an immediate download or a pending/manual-processing status.
- The local PDF path if a file was downloaded.
- Any blocker, especially CAPTCHA, login failure, account permission, or pending fulfillment.
