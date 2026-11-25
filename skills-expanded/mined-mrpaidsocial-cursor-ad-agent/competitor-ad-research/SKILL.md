---
name: competitor-ad-research
description: Researches competitor ads through Meta Ad Library, preserving full body, headline, description, and caption variants; optionally extracts and downloads snapshot creatives; ranks objective adaptation leverage; merges evidence-backed agent annotations; and writes a Markdown brief that hands local files to image-ad-clone or Arcads clone-ad. Use when the user asks to research competitors, pull Meta Ad Library ads, rank long-running competitor creative, download Ad Library images or videos, build a competitor swipe file, or prepare competitor assets for cloning. Does not trigger for creating a new ad from scratch or publishing ads to Meta.
---

# Competitor ad research

Run a portable, auditable competitor workflow:

1. Resolve exact Meta page identities.
2. Pull all copy variants and useful delivery metadata.
3. Optionally extract/download image and video creatives.
4. Rank adaptation leverage from observable metadata.
5. Optionally merge visual annotations backed by a local file.
6. Write `BRIEF.md` with local clone-skill handoffs.

Read [reference.md](reference.md) for the data contract, page-confidence policy, fields, and score formula. Read [annotations.md](annotations.md) before creating annotations.

## Hard rules

1. **Never guess a page.** Accept a numeric ID, `Label=ID`, a successful direct Facebook handle lookup, or one unique exact normalized Ad Library page-name match. If resolution is ambiguous or merely similar, stop for that page and ask for its numeric ID.
2. **Keep credentials in `.env`.** Use `META_ACCESS_TOKEN`; never pass it on the command line, print it, or persist token-bearing snapshot URLs.
3. **Deduplicate by Ad Library ID.** Do not dedupe by copy, page, date, or creative URL.
4. **Preserve full copy.** Keep every returned body, headline, description, and link-caption string without truncation.
5. **Call longevity a proxy, never performance.** Commercial Ad Library longevity does not prove spend, conversions, ROAS, profitability, or a winning ad.
6. **Do not fabricate motifs.** Name a motif only after visually inspecting the exact local creative. Every motif annotation needs `observed_from` plus concrete visible `evidence`; the ranker enforces this.
7. **Handoff local files only.** Remote CDN or snapshot URLs are not clone inputs. Download first, then use paths emitted in `BRIEF.md`.
8. **Keep this workflow research-only.** Do not generate or publish an ad until the user selects a source and separately invokes the relevant clone skill.
9. **Write only beneath** `outputs/competitor-research/<run>/`.

## Preflight

From the repository root:

```bash
python3 --version
python3 -m pip install -r skills/competitor-ad-research/requirements.txt
```

Requirements:

- Python 3.9+
- Repo-root `.env` containing `META_ACCESS_TOKEN`
- Meta Ad Library API access for the token
- Competitor page IDs preferred; exact page names/handles are allowed but may remain unresolved

Before pulling, confirm:

- Competitor pages
- Reached countries (default `US`)
- Lookback period (default 365 days)
- Active/all ads
- Whether creative extraction and downloads are wanted

Use one descriptive, portable run name throughout, for example:

```bash
RUN="2026-07-12-meta-competitors"
```

## Phase 1 — Pull metadata and full copy

Prefer explicit IDs:

```bash
python3 skills/competitor-ad-research/scripts/research_competitors.py \
  --run "$RUN" \
  --page "Competitor One=123456789" \
  --page "Competitor Two=987654321" \
  --countries US \
  --days 365 \
  --max-ads-per-page 100
```

Exact names, handles, and Facebook page URLs are also accepted:

```bash
python3 skills/competitor-ad-research/scripts/research_competitors.py \
  --run "$RUN" \
  --page "Exact Facebook Page Name" \
  --page "@exacthandle"
```

The output is `outputs/competitor-research/<run>/ads.json`.

Inspect its `page_resolution` array before continuing:

- `resolved` + `explicit`/`high`: safe to continue.
- `unresolved`: review `candidates`, obtain the numeric Page ID, and rerun with `Label=ID`.
- Never select the highest-count fuzzy candidate merely because it appears first.

The pull strips credential-like query parameters from snapshot URLs. It follows pagination by cursor and globally deduplicates records by `ad_library_id`.

## Phase 2 — Optional creative extraction/download

Skip this phase when the user wants copy/metadata research only.

Install browser dependencies only when requested:

```bash
python3 -m pip install -r skills/competitor-ad-research/requirements-creatives.txt
```

Chrome/Chromium is required. Extract URLs without downloading:

```bash
python3 skills/competitor-ad-research/scripts/extract_creatives.py \
  --run "$RUN"
```

Extract and download clone-ready local files:

```bash
python3 skills/competitor-ad-research/scripts/extract_creatives.py \
  --run "$RUN" \
  --download
```

This writes `ads_with_creatives.json` and, with `--download`, files beneath:

```text
outputs/competitor-research/<run>/creatives/<page>/<ad-library-id>/
```

Use `--driver webdriver-manager` only if Selenium Manager cannot resolve ChromeDriver. Do not treat every DOM asset as the ad creative: visually inspect downloaded files before annotation or cloning.

## Phase 3 — Objective ranking and initial brief

Ranking is fully offline:

```bash
python3 skills/competitor-ad-research/scripts/rank_competitors.py \
  --run "$RUN" \
  --top 20 \
  --emit-annotation-template
```

It prefers `ads_with_creatives.json` when present, otherwise `ads.json`, and writes:

- `ranked_ads.json` — machine-readable score/components
- `BRIEF.md` — full-copy detail and local clone handoffs
- `annotations.template.json` — only when requested

The 100-point score uses:

- 45: commercial-library longevity proxy, linear and capped at 365 days
- 15: active/not-stopped signal
- 15: publisher-platform breadth
- 15: body/headline/description/caption completeness
- 10: creative readiness (local file > remote URL > snapshot)

Annotations never change this objective score.

## Phase 4 — Optional agent annotation

Only annotate downloaded creatives the agent actually opened and inspected.

1. Copy `annotations.template.json` to `annotations.json`.
2. Open each `observed_from` file visually.
3. Fill `motif` only with a directly visible pattern.
4. Fill `evidence` with concrete visible details supporting that motif.
5. Keep uncertain or unreviewed motif fields empty.
6. Add `why_relevant`, `adaptation_notes`, `priority`, `confidence`, or `selected` only when useful.

Rerank with annotations:

```bash
python3 skills/competitor-ad-research/scripts/rank_competitors.py \
  --run "$RUN" \
  --annotations "outputs/competitor-research/$RUN/annotations.json" \
  --top 20 \
  --overwrite
```

The ranker rejects unknown IDs, invalid confidence/priority values, and motifs lacking an existing associated `observed_from` file plus evidence.

## Phase 5 — Review and clone handoff

Read `outputs/competitor-research/<run>/BRIEF.md` with the user.

For a selected local image:

- Follow [`image-ad-clone`](../image-ad-clone/SKILL.md).
- Use the exact local image path printed in `BRIEF.md`.
- Separate reusable structure from competitor branding/claims.

For a selected local video:

- Follow [`arcads clone-ad`](../arcads-external-api/prompting/clone-ad/SKILL.md).
- Use the exact local video path printed in `BRIEF.md`.
- Re-analyze the file frame-by-frame; research annotations are not a substitute for clone-ad analysis.

Do not automatically invoke either clone workflow. First show the ranked brief, disclose that longevity is not performance, and ask the user which local source to adapt.

## Output layout

```text
outputs/competitor-research/<run>/
├── ads.json
├── ads_with_creatives.json          # optional
├── creatives/                       # optional downloads
├── annotations.template.json        # optional
├── annotations.json                 # optional agent input
├── ranked_ads.json
└── BRIEF.md
```

## Recovery

- **No page resolved:** ask for numeric Page IDs. Do not loosen matching.
- **Some pages unresolved:** keep their candidate evidence in `ads.json`; continue resolved pages only if the user agrees.
- **401/403:** replace/refresh `META_ACCESS_TOKEN` in `.env`; never paste it into commands or reports.
- **Rate limit/5xx:** the pull retries with bounded backoff; rerun with the same run and `--overwrite` only after confirming the old output can be replaced.
- **Selenium missing:** install `requirements-creatives.txt`; base pull/ranking do not require Selenium.
- **No creative found:** retain copy/metadata and the sanitized snapshot URL; do not invent a creative description.
- **Download failed:** retry extraction while the CDN URL is fresh; do not hand a remote URL to clone skills.

## Offline verification

These checks make no network calls:

```bash
python3 -m unittest discover \
  -s skills/competitor-ad-research/tests \
  -p "test_*.py" \
  -v

python3 skills/competitor-ad-research/scripts/research_competitors.py --help
python3 skills/competitor-ad-research/scripts/extract_creatives.py --help
python3 skills/competitor-ad-research/scripts/rank_competitors.py --help
```
