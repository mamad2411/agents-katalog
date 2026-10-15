---
name: qiaomu-ai-access
description: |
  Use this qiaomu skill workflow when the user wants to check whether their
  local or browser environment looks like a China user before accessing AI
  models, using yArna/isChinaUser first, then asking for explicit consent before
  safe privacy-hygiene guidance. Trigger on requests such as "我是中国人但想用顶级AI",
  "检测中国用户特征", "用 isChinaUser 检测", "qiaomu-ai-access", "AI access region
  signal check", or "先检测再问我要不要整理隐私特征". Do not provide VPN/proxy,
  geofence bypass, sanctions evasion, account-region spoofing, KYC/payment
  misrepresentation, CAPTCHA/device-fingerprint bypass, or platform-risk
  evasion instructions; offer compliant alternatives instead.
metadata:
  author: 向阳乔木
  copyright: Copyright (c) 向阳乔木
  x: https://x.com/vista8
  github: https://github.com/joeseesun/
  upstream_dependency: yArna/isChinaUser
---

# Qiaomu AI Access

Detect first, ask second, stay inside legal and platform boundaries.

## Router Rules

- Use this skill when the user's goal is environment-signal transparency before using AI websites, APIs, or top AI models.
- Use it when the user asks to identify "中国用户特征", "China user signals", "AI access signals", browser language/timezone/font/emoji signals, or `isChinaUser` results.
- If the user asks directly for VPN/proxy purchase, IP masking, account-region laundering, KYC/payment misrepresentation, CAPTCHA bypass, device-fingerprint evasion, or sanctions/geofence bypass, do not run an evasion workflow. Briefly refuse that part and offer the safe detection and privacy-hygiene workflow.
- Do not treat nationality, ethnicity, residence, or legal eligibility as something this skill can determine. It only reports runtime signals.

## Workflow

1. State the boundary in one sentence: this skill checks signals and can suggest compliant privacy hygiene, but it does not help bypass service restrictions or misrepresent identity/location.
2. Run the detector from the repository root after dependencies are installed:

   ```bash
   npm install
   npm run detect:browser -- --output reports/latest-ai-access-check.md
   ```

   If the user explicitly agrees to remote network probes, run:

   ```bash
   npm run detect:full -- --output reports/latest-ai-access-check.md
   ```

3. Show the user the high-level status, coverage level, and signal table. Treat `runtime`, `browser`, and `network` coverage separately; do not overstate skipped or unavailable layers.
4. Ask this exact confirmation before any follow-up hygiene advice:

   ```text
   是否继续做合规隐私卫生检查？我可以帮你减少 prompt、浏览器偏好和工作区说明里不必要的地域信号；不会帮助绕过平台地域限制、伪装 IP/身份、规避风控或违反服务条款。
   ```

5. If the user says yes, provide only non-destructive, compliant steps:
   - prefer official AI services, models, regions, and payment paths available to the user;
   - use English prompts/UI preferences when the goal is English model behavior or documentation quality;
   - keep a separate browser profile for AI work to reduce cookie/history/permission mixing;
   - remove unnecessary location claims from prompts, docs, and profile snippets when they are not relevant;
   - explain that changing system language/timezone to misrepresent location or bypass controls is outside this skill.
6. If the user says no or seems unsure, stop after the report and offer to save it for later.

## Output Contract

- `reports/latest-ai-access-check.md` when the detector is run with `--output`.
- A concise status: `china-signals-detected`, `no-china-signal-detected`, or `inconclusive`.
- A coverage table for `runtime`, `browser`, and `network`.
- A signal table with source, value, and notes.
- The required consent prompt.
- Clear unavailable/missing-evidence labels for browser-only or network-only signals not measured in the current run.

## Runtime Notes

- The first-step detector imports the npm package `is-china-user`.
- Node.js can reliably inspect timezone and limited runtime locale data.
- Browser coverage uses a temporary Playwright Chromium/headless-shell context, injects the installed `is-china-user` package bundle into that page, and does not read a personal browser profile.
- DOM/canvas-based emoji and font checks should be interpreted from the browser layer, not from Node-only runs.
- Optional network probing is off by default because it creates real remote requests and is noisy under proxies, extensions, DNS failures, or offline conditions.
- The upstream package currently has no declared license in GitHub/npm metadata, so this skill depends on it without vendoring its source.

## Validation

Run before publishing changes:

```bash
npm test
npm run smoke:browser
npm run validate:skill
npm run eval:trigger
npm run export:ir
npm run secret:scan
```

## Release Boundary

- Public claims must match the validation output.
- Do not publish secrets, local browser profiles, cookies, `.env` files, network credentials, or screenshots containing account data.
- Keep the README Chinese-first bilingual for Qiaomu-owned public releases.
