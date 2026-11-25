---
name: repo-pinokio
description: How Pinokio (pinokiocomputer/pinokio, pinokio.computer) works, a one-click launcher for open-source AI apps and scripts, including its script-isolation and verification policy and the risks of running third-party scripts. Use when a user wants to install local AI tools (Stable Diffusion UIs, TTS, video models) without manual setup, or asks if Pinokio is safe.
---

# Pinokio (`pinokiocomputer/pinokio`)

Cloned shallow at `/home/user/pinokiocomputer/pinokio` (re-clone `git clone --depth 1 https://github.com/pinokiocomputer/pinokio`). It is an Electron app ("Launch Anything"); MIT-style licence in `LICENSE`. The note labelled it "pinokio.computer (ai tools)".

## What it is
A terminal-like application with a UI that runs JSON scripts which can run shell commands, download files and launch open-source projects. Two ways to run scripts: write your own, or install from the Discover page.

## Security model (from the README)
- Scripts run under `~/pinokio/api`; binaries from its package managers install under `~/pinokio/bin`.
- Verified Discover scripts must keep commands inside the app path, use per-app `venv`, and install packages inside the isolated environment. Publisher identity, transfer to the Pinokio Factory organisation and admin review are required.
- **Scripts can run anything.** Isolation is by convention, not a sandbox. Unverified scripts from arbitrary git URLs are arbitrary code execution.

## Rules for Claude
1. Recommend only Discover-listed (verified) scripts; read an unlisted script's JSON before telling the user to run it.
2. Never run Pinokio scripts yourself on this machine without explicit user approval.
3. GPU-heavy installs (video models such as `repo-wan21`) need disk and VRAM checks first.

## Related
`repo-wan21`, `ai-website-app-builders`, `free-utility-learning-resources`, `security-review`.
