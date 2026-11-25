---
name: sync-accelevents
description: Use when pulling Accelevents speaker headshots, social data, bios, and schedule metadata into the AI Engineer Europe source data and photo assets.
---

# Sync Accelevents Speaker Data (Europe)

Pulls speaker headshots and social data from the Accelevents API into the Europe conference schedule.

## Prerequisites

- `ACCELEVENTS_API_KEY` environment variable must be set (stored as a Devin secret)
- Python 3 with Pillow installed (`pip install Pillow`) for image optimization

## Steps

1. **Checkout a new branch**
   ```bash
   cd /home/ubuntu/repos/aiecode2025
   git checkout main && git pull origin main
   git checkout -b devin/$(date +%s)-sync-accelevents
   ```

2. **Run the sync script**
   ```bash
   cd /home/ubuntu/repos/aiecode2025/src/pages/europe/source/_scripts
   python3 sync_accelevents.py --save-snapshot
   ```
   This will:
   - Fetch all speakers from the Accelevents API
   - Download/replace headshots that speakers uploaded to the portal
   - Optimize oversized images (>200KB) for the grid view, keeping originals in `large/`
   - Update `schedule.json` with social/bio data (only fills blanks, doesn't overwrite)
   - Save an API snapshot to `_accelevents/accelevents_speakers_latest.json`

   **Flags:**
   - `--dry-run` — show what would change without writing anything
   - `--headshots-only` — skip social/bio updates
   - `--data-only` — skip headshot downloads
   - `--save-snapshot` — save raw API response
   - `--optimize-existing --data-only` — optimize oversized existing photos

3. **Re-export the CSV**
   ```bash
   cd /home/ubuntu/repos/aiecode2025/src/pages/europe/source
   python3 _scripts/export_csv.py
   ```

4. **Run typecheck**
   ```bash
   cd /home/ubuntu/repos/aiecode2025
   SKIP_ENV_VALIDATION=1 npx tsc --noEmit
   ```

5. **Commit all changes**
   ```bash
   cd /home/ubuntu/repos/aiecode2025
   git add public/speakers/europe/ src/pages/europe/source/schedule.json src/pages/europe/source/_accelevents/ src/pages/europe/source/schedule_export.csv
   git commit -m "sync: pull speaker headshots + social data from Accelevents API"
   git push origin HEAD
   ```

6. **Create PR and verify**
   - Create PR into `main`
   - Start the dev server: `SKIP_ENV_VALIDATION=1 pnpm dev`
   - Navigate to `http://localhost:3000/europe#speakers`
   - Verify the speaker globe renders with updated headshots, no broken images
   - Take a screenshot and share with the user

## Key Paths

- Script: `src/pages/europe/source/_scripts/sync_accelevents.py`
- Schedule source of truth: `src/pages/europe/source/schedule.json`
- Photos (optimized for grid): `public/speakers/europe/`
- Photos (full-size for lightbox): `public/speakers/europe/large/`
- API snapshot: `src/pages/europe/source/_accelevents/accelevents_speakers_latest.json`
- CSV export: `src/pages/europe/source/schedule_export.csv`

## Notes

- The script matches API speakers to schedule speakers by: `acceleventsSpeakerId` > email > name
- Only 8 of 109 speakers had uploaded headshots as of the first run — this number will grow over time
- `pnpm lint` does not work on Next.js 16; use `npx tsc --noEmit` for type checking instead
- The `europe:source:sync-public` script referenced in some docs does not exist; the sync script writes directly to `public/speakers/europe/`
