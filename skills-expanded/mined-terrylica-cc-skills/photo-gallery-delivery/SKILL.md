---
name: photo-gallery-delivery
description: End-to-end playbook for getting a set of photos to someone who can't use what you sent — pull the originals from a cloud album, convert HEIC to JPEG, build a browsable gallery plus a password-protected ZIP, host it on an unlisted URL, and share it through a gist gateway that holds the password. Orchestrates the amazon-photos-album-download, heic-to-jpeg-bundle, and cloudflare-workers-publish skills. Use when a recipient (dealer, adjuster, client) reports they can't open or download your photos, or when you want a clean unlisted JPEG gallery plus bulk download. TRIGGERS - share photos with someone, recipient cant open photos, jpeg gallery delivery, send photos as downloadable link, unlisted photo gallery, deliver photo set, heic recipient problem.
allowed-tools: Bash, Read, Write, Edit, AskUserQuestion
---

# photo-gallery-delivery

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

The full playbook for **delivering a photo set to a real recipient** when "just share the
album" isn't working — because the files are HEIC, the share app forces a login, or the
recipient's software can't ingest what you sent. It stitches three focused skills into one
flow and adds the **gist-gateway + password** delivery model.

## When to use

- A recipient says they **can't open / can't download / can't convert** your photos
  (classic: iPhone **HEIC** vs. Windows appraisal/CRM software).
- You want to hand over a **clean, unlisted JPEG gallery** (viewable in any browser, no app,
  no login) **plus a bulk ZIP** — to a dealer, insurance adjuster, client, or contractor.
- You're already sharing a **gist / landing page** with people and want it to lead to JPEGs
  instead of a format they can't use.

## The pipeline

```
cloud album ──▶ download originals ──▶ HEIC→JPEG + gallery + ZIP ──▶ unlisted host ──▶ gist gateway
 (share link)   amazon-photos-          heic-to-jpeg-bundle          cloudflare-        (link + password)
                album-download                                       workers-publish
```

Each stage is its own skill; this skill is the glue + the decisions between stages.

### 1. Pull the originals — `productivity-tools/amazon-photos-album-download`

Get a verified local copy of every original from the public Amazon Photos share link.
Store them **outside any git repo** (originals carry GPS/plate/VIN EXIF).

```bash
ALBUM_URL="https://www.amazon.ca/photos/share/<id>" ALBUM_OUT="$HOME/.cache/album/originals" \
  bun "$(find ~/.claude ~/eon -path '*/amazon-photos-album-download/scripts/download-album.ts' | head -1)"
```

### 2. Convert + bundle — `media-tools/heic-to-jpeg-bundle`

Make a gallery (2048px view tier + thumbnails) and a password-protected ZIP sized to fit the
host's per-file cap.

```bash
bash "$(find ~/.claude ~/eon -path '*/heic-to-jpeg-bundle/scripts/make-bundle.sh' | head -1)" \
  --src "$HOME/.cache/album/originals" \
  --title "2023 Corolla Cross — trade-in photos" \
  --zip --password "<PICK-A-PASSWORD>" --zip-cap-mib 25
```

### 3. Host it unlisted — `devops-tools/cloudflare-workers-publish`

Deploy the `_bundle/site/` directory (gallery + per-photo JPEGs + the ≤25 MiB ZIP). You get
an unlisted `https://<name>.<slug>.workers.dev/` URL. **Mind the 25 MiB/file cap** (CFW-16):
the gallery and a downscaled ZIP fit; a full-resolution ZIP does not — host that on R2 / a
GitHub Release / your own server and link it from the gallery. See
[large files & ZIP delivery](../../../devops-tools/skills/cloudflare-workers-publish/references/large-files-and-zip-delivery.md).

### 4. Share through the gist gateway

If you already share a **gist** (or any landing page) with recipients, make it the gateway:

- Add a **"📸 Photos (JPEG)"** section: the **gallery URL**, the **ZIP URL**, and the **ZIP
  password**.
- Keep the **password only on the gist**, never on the Workers page (password-on-the-gateway,
  see the cloudflare skill). The gist becomes the one place that has both link and password.
- If a short link (tinyurl) already points at the gist, every previously-sent link upgrades
  for free.

```bash
gh gist edit <gist-id> -f <file.md> /tmp/updated-gist.md
```

## Decisions to surface (use AskUserQuestion)

- **Resolution / tiers**: web-res gallery only, or also a full-resolution ZIP for the
  recipient's own analysis? Full-res can't sit on Workers (size) — confirm a large-file host.
- **Hosting**: unlisted Workers (recommended) vs. public GitHub Release (world-readable —
  avoid for PII) vs. own server.
- **Gating**: password-protected ZIP with the password on the gist, vs. open download.
- **Privacy**: these photos often show plate / VIN / home — keep originals out of git, prefer
  unlisted hosting, and don't index publicly.

## Worked example (June 2026)

A used-car buyer's Amazon Photos album of **125 HEIC** trade-in photos was unusable to dealers
whose appraisal software couldn't open HEIC (the documented #1 blocker in their outreach).
Flow: pulled all 125 originals (byte-verified) → converted to a 2048px JPEG gallery + a
**24 MiB** ZipCrypto ZIP (`--zip-cap-mib 25` downscaled it to fit) → deployed gallery + ZIP to
`vehicle-appraisal.example-account.workers.dev` (the 109 MiB full-res ZIP hit the 25 MiB cap, so
it was kept off Workers) → updated the dealer-facing gist with the gallery link, ZIP link, and
the password. Because a tinyurl already pointed at the gist, ~22 already-sent dealer links
upgraded to JPEGs with nothing re-sent.

## Post-Execution Reflection

After a delivery, before closing:

1. **Did the recipient succeed?** If they still struggled, note the exact tool/format and fix
   the relevant stage skill (not this one, unless the orchestration itself was wrong).
2. **Did a stage's external dependency drift?** (Amazon API, Workers cap, gist tooling.) Log
   it in that stage skill's own notes/evolution-log.
3. Only update this SKILL.md for real, reproduced changes to the end-to-end flow.
