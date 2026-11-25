---
name: h3-colab-studio
description: >-
  Build and operate a prompt-to-video workspace for MiniMax H3 with an agent
  execution bridge to Google Colab G4 running ComfyUI. Use when the user wants
  to generate single-shot or multi-shot MiniMax H3 videos on Colab, optimize
  story ideas into official H3 structured prompts, build a job-queue control
  app for H3 video production, or stitch and verify multi-shot H3 clips.
---

# H3 Colab Studio — Prompt-to-Video Workspace with an Agent Bridge

## What this builds

- Build three cooperating parts: a job-queue app the user drives, a prompt optimizer that rewrites ideas into the official MiniMax H3 prompt structure, and yourself as the execution bridge to Google Colab.

- Treat the app as the control surface only. GPU generation happens on Colab, never inside the app, and the app must say so plainly instead of faking a live generate button.

- Expect the payoff to be repeatable multi-shot videos. A single H3 generation is one continuous take with no cuts, so story structure comes from generating one clip per shot and stitching, which this workflow makes routine.

## Set up Colab and H3

- Confirm the user has a Google account with Colab compute units available, for example through Google AI Ultra or a Colab paid plan, and warn them that granted unit pools can expire (the Ultra grant lasts about 90 days).

- Read [the Colab runbook](references/colab-runbook.md) before the first run and follow it exactly. It carries the verified notebook choice, the model files, and the two failure fixes that cost real time when missed.

- Pick the G4 runtime (RTX PRO 6000 Blackwell, about 96 GB VRAM). Budget with the measured burn of about 8.9 units per hour rather than the roughly 10 units per hour the panel displays.

- Record the compute-unit balance before and after every session, and delete the runtime at the end of the session so billing stops.

- Keep all shots of one video inside a single session. Model downloads dominate setup time, so a fresh runtime per shot wastes units and minutes.

## Build the workspace app

- Read [the app blueprint](references/app-blueprint.md) and build the app to that spec:
  - **Local coding environments (Antigravity, Claude Code, Cursor, etc.)**: Build a lightweight persistent web app (for example, Vite or Next.js backed by local JSON or SQLite storage) with clean API routes or CLI helpers so job records persist on disk and you can read and update them directly.
  - **Hosted agent workspaces**: Use the host platform's persistent full-stack web app capability so job records survive across sessions and can be updated programmatically.

- Give the form these fields: idea text, mode (T2V first, I2V and FL2VA and Ref2VA marked as coming later), per-shot duration of 5, 8, 10 or 15 seconds, resolution tier (standard 864×480, high 1120×640, max 1376×768), aspect ratio, shot count (auto, 1, 3 or 5), seed (random or fixed), turbo toggle, and style.

- Show a live optimized-prompt preview beside the form, built from the structure in [the prompt spec](references/prompt-spec.md), and let the user edit the draft before submitting.

- Save every submission as a job with a status of queued, optimizing, running, done or failed, and expose an update interface (API route, CLI helper, or workspace action) that you use to backfill status, output specs, units consumed and a result note after execution.

- Seed the history with one real completed job once you have run one, so the queue never looks like a demo.

- Put a small bridge-status panel in the app naming the backend (Colab G4), the last measured unit balance with its date, and the three steps: submit here, ask the agent in chat to run job number N, agent generates and backfills the result.

## Write the H3 prompts

- Read [the prompt spec](references/prompt-spec.md) for the official H3 structure and the multi-shot method before writing any prompt.

- Structure every T2V prompt as a subject and scene definition, one block per shot with a shot-type label, an overall soundscape line, and a non-diegetic music line.

- Repeat the main character description word for word in every shot block, repeat the palette and style words in every block, and use one shared fixed seed for all shots of a video. Verbatim repetition plus a shared seed is what makes separately generated clips look like one film.

- Write shot blocks in English even when the user idea arrives in another language. H3 follows detailed English camera language more reliably.

- Keep each shot to one location and one main action. H3 renders a single continuous take per generation, so anything that needs a cut belongs in the next shot block.

## Execute a job and finish it

- Mark the job running in the app before opening Colab, then run the whole shot list in one session following [the Colab runbook](references/colab-runbook.md).

- Download each finished clip before queueing the next shot, and name files in shot order so stitching cannot scramble the sequence.

- Stitch the clips locally with [scripts/stitch.sh](scripts/stitch.sh) and verify the result with `ffprobe` (resolution, duration, fps, audio track) before calling it done.

- Backfill the job in the app with the final specs, the measured units consumed and an honest note, then deliver the video file to the user in chat with a per-shot quality read.

- Report failures with the exact error text and the state you left behind, including the balance after cleanup and whether the runtime was deleted.

## Measured reference points

- Treat these as single-run measurements from November 2026 on a G4, useful for planning rather than promises: 15 seconds at 864×480 sampled in about 4 to 5 minutes, 5 seconds at 1376×768 in about 3 minutes per shot, and 15 seconds at 1920×1088 in about 69 minutes.

- Expect a three-shot 15-second video at 1376×768 to consume roughly 5 compute units including setup when the session runs clean.

## Pitfalls

- Avoid the `keboqi/minimax-h3` Prism Studio notebook UI for H3. Its job binding code threw an `IndexError` before generation on every attempt in testing, while the direct ComfyUI route worked.

- Download the Turbo LoRA before the first queue. The working notebook omits it and the ComfyUI template blocks with a missing-model error until it exists.

- Check the `SaveVideo` node format field shows `mp4` before every queue. A blank field silently discards a finished generation after the full sampling time.

- Watch for Colab idle disconnects on long sampling runs. Reconnecting to the same runtime usually preserves the session, so reconnect before restarting anything.

## Browser & connector integration

- **Browser automation**: When your environment provides browser or GUI automation (such as Playwright MCP, Antigravity `/browser`, or desktop/browser agents), drive the Colab notebook and ComfyUI canvas directly while reporting progress at setup, queue, download, and runtime deletion checkpoints.
- **Guided manual handoff**: If no browser tool is connected, provide ready-to-paste notebook cells (including the Turbo LoRA fix) and clear per-shot ComfyUI parameter cards (`prompt`, `duration`, `megapixels`, `noise_seed`, `filename_prefix`) so the user can run the Colab step and hand you the downloaded MP4 clips to stitch and backfill.
- **Extensibility**: Use available MCP servers, plugins, or workspace connectors if the user wants automated cloud storage upload or external notifications after stitching.

## Websites

- [Google Colab](https://colab.research.google.com/) for the GPU runtime. Carry the account that owns the compute units and the exact notebook from the runbook, and verify the balance and GPU model in the session panel.

- [dseditor/minimax-h3-colab on GitHub](https://github.com/dseditor/minimax-h3-colab) for the working direct-ComfyUI notebook this workflow is built on.

- [MiniMax H3](https://www.minimax.io/) for the model and its official prompt-writing material. Prefer the official prompt structure over community folklore when they disagree.
