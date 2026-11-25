---
name: higgsfield-studio-soul-id
description: "Train a Soul on a person's face with Higgsfield, so later images and videos keep their identity. Triggers: 'create my Soul', 'train my face', 'make my digital twin', 'learn my appearance', 'put my face in generated images', 'create a character of me', 'soul id'. Part of Higgsfield Studio: training runs only after the user says yes, and every image made with the Soul is priced first and written to a ledger. Needs a Higgsfield paid plan, Node 18+ and the higgsfield command line tool."
license: MIT
compatibility: "Requires Node 18 or newer and the Higgsfield command line tool, through the higgsfield-studio skill in the same plugin. Soul training needs a paid Higgsfield plan. Needs network access."
metadata:
  author: itqanlab
  version: 1.1.0
  category: media
  display: "Higgsfield Soul ID"
  short: "Train a face once, reuse it in Higgsfield"
  starter: "train a Soul from these photos of me"
---

# Higgsfield Soul ID

Train a Soul once from 5 to 20 photos of one person, then use it in any Soul model (`text2image_soul_v2`, `soul_cinematic`) with `--soul-id <id>`.

Only train a Soul of the person asking, or of someone who has agreed to it. Ask if it is not clear.

## What it costs

Higgsfield gives no price for training in advance, so `act soul-id create` needs `--yes`, and the cost is measured from the account after it runs. We have not trained a Soul yet, so we have no measured figure. Tell the user that before they say yes. Images made with the Soul are cheap: `text2image_soul_v2` and `soul_cinematic` were quoted at 0.12 credits each on 2026-10-12.

Training goes through the guard like this, after the user's yes:

```
node ../higgsfield-studio/scripts/hf.mjs act soul-id create --name "Sara" --soul-2 --image a.jpg --image b.jpg ... --yes --why "Soul for the spring campaign"
```

## Before anything else

```
sh ../higgsfield-studio/scripts/setup-deps.sh --check
node ../higgsfield-studio/scripts/hf.mjs check
```

The first checks Node and the `higgsfield` tool, and `sh ../higgsfield-studio/scripts/setup-deps.sh` installs what is missing after asking. The second checks the sign-in. If Higgsfield is not signed in, the user signs in once with `higgsfield auth login`, which opens the browser. Never print the sign-in token or open the CLI's credential file.

## Spending credits

This skill is part of the Higgsfield Studio plugin. Every paid command runs through the main skill's guard, `node ../higgsfield-studio/scripts/hf.mjs`. It asks Higgsfield for the price before running, refuses above `--max` or below the reserve, never pays twice for the same request, and writes what each job really cost to `.higgsfield/ledger.jsonl` in the project. The full rules are in `../higgsfield-studio/SKILL.md`. The short form:

- Price first with `--dry`, using every parameter the real job will use. Tell the user the total for anything over about 5 credits.
- Put `--max N` (a little above the price), `--tag` and `--why "..."` on every paid job.
- Ask before spending more than about 10 credits, or 10% of what is left. `node ../higgsfield-studio/scripts/hf.mjs account` shows the balance.
- Anything outward or not undoable goes through `act` and needs `--yes`. Say what will happen and wait for the user's yes before adding it.
- Report in plain words, in the user's language: where the file is, what it cost, what is left. No JSON or job ids unless asked.

Free commands, such as lists, `model get`, presets and uploads, can run as `node ../higgsfield-studio/scripts/hf.mjs run <command>` or as `higgsfield <command>` directly.

## Updates

This skill is versioned with its plugin. Its version is `metadata.version` in the header of this file. The plugin's history, for every skill in it, is in `../higgsfield-studio/CHANGELOG.md`. To check for a newer version, open the address on its `Latest:` line and compare the top version with this one. Read every entry in between and tell the user what changed before anything is updated.

## Higgsfield's guide

Everything below is Higgsfield's official guide for this task, with its paid and outward commands already pointed at `node ../higgsfield-studio/scripts/hf.mjs`. The rules above win where the two differ.

# Higgsfield Soul Character

Train a face-faithful identity model. Reusable across all Soul-powered generations.

## Step 0 — Bootstrap

Before any other command:

1. If `higgsfield` is not on `$PATH`, install it:
   ```bash
   sh ../higgsfield-studio/scripts/setup-deps.sh
   ```
2. If `higgsfield account status` fails with `Session expired` / `Not authenticated`, ask the user to run `higgsfield auth login` (interactive) and wait for confirmation.
3. Soul training requires a paid plan (Basic+). If `higgsfield account status` shows free plan, tell the user before submitting.

## UX Rules

1. Be concise. No raw IDs in chat. Just say "Soul ready" with a name reference.
2. Detect language and respond in it. CLI flags stay English.
3. Ask for the smallest set of inputs: name + photos. Pick a sensible model variant.
4. Polling is silent — training takes minutes. Don't repeat status updates.

## Workflow

1. **Get name.** One word, used for later reference. Ask if missing.
2. **Get photos.** 5–20 face photos, varied angles and lighting. Local paths or already-uploaded IDs both work — `--image` accepts either.
3. **Pick variant.**
   - `--soul-2` — for image generation (default)
   - `--soul-cinematic` — for cinematic / video work
   Choose based on user's stated downstream use. Default to `--soul-2`.
4. **Submit.**
   ```bash
   node ../higgsfield-studio/scripts/hf.mjs act soul-id create --name "<name>" --soul-2 --image ./photo1.png --image ./photo2.png ...
   node ../higgsfield-studio/scripts/hf.mjs act soul-id create --name "<name>" --soul-2 --image <upload_id> --image <upload_id> ...
   ```
   CLI auto-uploads paths. Captures returned reference id.
5. **Wait.** `higgsfield soul-id wait <id>`. Silent. Default timeout 30m.
6. **Deliver.** "Soul `<name>` ready. Use in generate with `--soul-id <id>`."

## Use the Soul

Once trained, pass to `higgsfield-generate`:

```bash
node ../higgsfield-studio/scripts/hf.mjs create text2image_soul_v2 --prompt "..." --soul-id <ref_id> --quality 2k --wait
node ../higgsfield-studio/scripts/hf.mjs create soul_cinematic --prompt "..." --soul-id <ref_id> --quality 2k --wait
```

`--soul-id` is sent as the model's `custom_reference_id`. For a curated Soul style, list styles with `higgsfield preset list soul-v2` and pass the chosen id as `--style_id` on `text2image_soul_v2`. `--style_id` cannot be combined with `--image`.

## Listing existing Souls

```bash
higgsfield soul-id list                   # all references
higgsfield soul-id get <id>               # one by id
```

## Errors

- `Minimum Basic plan required` — user is on free plan; tell them.
- `Training failed` — check photos quality (5+ unique faces, well-lit).
- `Session expired` → `higgsfield auth login`.

## Reference docs

- `references/photo-guide.md` — what photos work best
- `references/troubleshooting.md` — common training failures
