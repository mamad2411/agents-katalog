---
name: replace-so-dev-repos-6
description: Verified register of the "6 best GitHub repositories for developers" carousel (@replace.so, which promises six and shows five) - Maxun (web data extraction), PocketBase (single-file backend), OpenWhispr (voice to text), Open WebUI (self-hosted AI front end) and Jan (local AI desktop app) - with the real licence of each. Flags that Open WebUI's licence is a custom licence with a branding clause, Maxun is AGPL-3.0 and PocketBase is pre-1.0. Use when choosing among these tools or checking whether one is safe for commercial or white-label use.
---

# "6 best GitHub repositories for developers", checked

Source: @replace.so carousel; the cover promises six repos and the upload shows five (the cover's icons also show five). Repos cloned and licence files read on 4 October 2026. Nothing installed. Stars are as printed on the slides and unverified.

| Repo | Slide stars | Licence read | Last commit | Verdict |
|---|---|---|---|---|
| `getmaxun/maxun` | 17,639 | AGPL-3.0 | 2026-10-03 | Real. No-code scraping and structured data extraction. AGPL: modifying and offering it over a network requires offering your source |
| `pocketbase/pocketbase` | 61,261 | MIT | 2026-09-12 | Real. A Go backend in one executable with SQLite, realtime subscriptions and an admin UI. Its README warns full backward compatibility is **not guaranteed before v1.0.0** |
| `OpenWhispr/openwhispr` | 8,997 | MIT | 2026-10-02 | Real. Dictation and meeting transcription on macOS, Windows and Linux |
| `open-webui/open-webui` | 153,938 | **Custom Open WebUI License** | 2026-09-21 | Real, but **not a standard open-source licence**; see below |
| `janhq/jan` | 44,793 | Apache-2.0 | 2026-10-02 | Real. Open-source desktop app for running local models and connecting cloud ones |

## The Open WebUI licence

It is a BSD-style licence with an added clause (clause 4): you may not alter, remove, obscure or replace any "Open WebUI" branding in any deployment or distribution, except where the deployment has **no more than 50 end users in any rolling 30 days**, or you hold written permission from the copyright holder, or a third listed circumstance applies (the text continues beyond what I read). So: fine for personal or small-team use with the branding kept; **white-label or larger deployments need permission**. It is also not on the usual open-source lists because of that clause. [Certain] for the wording I read; read the full file before any commercial use.

## Other cautions

- **PocketBase is pre-1.0.** Pin the version and read release notes before upgrading a live app.
- **Maxun** is AGPL-3.0 and its README advertises a hosted cloud as well; the cloud is not what you self-host.
- **Jan** and **Open WebUI** both front local or cloud models; you still supply or run the model.
- The cover promises six; the sixth tool is unknown. Do not assume one.

## Which for which job

| Need | Pick |
|---|---|
| A backend for a small app, one file to deploy | PocketBase |
| Pulling structured data from websites without code | Maxun, after checking the site's terms |
| A browser front end for local models for a team | Open WebUI, within its branding terms |
| A desktop chat app for local models | Jan |
| Dictating into any app | OpenWhispr |
