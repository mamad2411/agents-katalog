---
name: codex-imagegen
description: "Generate or AI-edit images by delegating to the Codex CLI ($imagegen / gpt-image) — sample banners, hero visuals, demo assets, image-to-image edits. Use whenever a task needs image GENERATION or AI photo editing (Claude Code cannot generate images itself). 日本語の依頼例:「画像を生成して」「サンプル画像を作って」「この写真を加工して」「バナー/ヒーロー画像が必要」。NOT for resizing/compressing existing assets (use `images-media`)."
---

# Codex imagegen — delegate image generation, keep the code here

Claude Code cannot generate images. When a task needs generated or AI-edited images, delegate to the **Codex CLI's built-in `$imagegen` tool (gpt-image)**: it runs on the operator's ChatGPT subscription — no API key, no per-call billing, i2i editing included. Division of labor: code and prompts are authored here; pixels come from Codex.

## Invocation

- Scriptable default: `codex exec -C <workdir> -s workspace-write --skip-git-repo-check "<instruction>"` via `execFileSync` (array args, never shell strings). Timeout ~15 min per call; run batches sequentially (rate limits), support `--slug` re-runs and skip-existing + `--force`.
- Resolve the binary: `$CODEX_BIN` env → `codex` on PATH → `/Applications/Codex.app/Contents/Resources/codex` (macOS app bundles the CLI). Verify with `--version` before batching.
- MCP registration (`claude mcp add --transport stdio codex -- codex mcp-server`) is the interactive alternative; `codex exec` stays the default for reproducible pipelines.

## Sandbox isolation — non-negotiable

Point `-C` at a scratch dir (`os.tmpdir()` subdir), NEVER the repo. The instruction embeds content-derived text (templates, user-editable YAML), so prompt injection through content must not reach a repo-writable agent — with `-C repoRoot` an injected instruction could rewrite `package.json` and land RCE on the next `npm run dev`. The wrapper script alone copies finished artifacts from the scratch dir into the repo.

## Instruction anatomy (what actually controls quality)

1. **Verbatim prompt block**: wrap the exact prompt in `---` delimiters with "Use EXACTLY this prompt, verbatim, without rewriting it" — otherwise Codex paraphrases and the published prompt no longer matches the sample it claims to produce.
2. **Native sizes only**: gpt-image emits 1024x1024 / 1536x1024 / 1024x1536. Other ratios: generate the nearest orientation → center-crop → resize (`sips` on macOS, `sharp` elsewhere).
3. **Bleed instruction whenever cropping**: "the image will be center-cropped to WxH; treat the outer Npx as expendable bleed — background only; ALL text and critical elements inside the surviving central region." Without it, edge-anchored text gets cut (bottom ribbons are the classic casualty).
4. **i2i is two steps**: generate the source image first, then EDIT mode referencing the input path ("treat 'the attached photo' as the input image at <path>"). Keep the source artifact — before/after is the proof the edit works.
5. Close with "Save the final image to <path> (PNG). Do not edit any other files."

## Quality gate — generation is not done at exit 0

- Review every image visually before publishing. For Japanese text: character-by-character — models garble kanji, and a wrong glyph on a shipped banner is worse than none.
- Check the crop actually preserved all text, and (i2i) that the source subject/label survived the edit.
- Retakes are normal (budget 2–3 per image); re-run per slug, never the whole batch. Trial ONE image before any batch — composition bugs (missing bleed, wrong ratio) waste a full batch otherwise.
- Quota is the operator's ChatGPT plan: dozens of images per session is fine, plan accordingly.

## Pipeline sketch

```js
const work = path.join(os.tmpdir(), 'imagegen-work');           // sandbox, not the repo
execFileSync(codex, ['exec', '-C', work, '-s', 'workspace-write',
  '--skip-git-repo-check', instruction(prompt, workFile)], { timeout: 900_000 });
if (!existsSync(workFile)) throw new Error('not saved');
execFileSync('sips', ['-c', cropH, cropW, workFile]);            // center-crop to target ratio
execFileSync('sips', ['-z', finalH, finalW, workFile]);          // resize to target px
copyFileSync(workFile, repoTarget);                              // script does the repo write
```

Derive the filled prompt from the same single source the app renders (shared data + one fill function, parity-tested) — a stored copy of the prompt WILL drift from the template that generated it.
