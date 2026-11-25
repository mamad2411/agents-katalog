---
name: deepsearch-ad-intel
description: Captures competitor ads from the public Meta Ad Library on one slow stream, transcribes the words spoken in video ads, saves images, and measures Pages, durations, shared script families, angles, EU reach and spend floors, with silent-limit detection. Use for "Facebook Ad Library", "Meta Ad Library", "bibliothèque publicitaire", "analyse les pubs des concurrents", "transcribe competitor ads", "who runs ads to this target", or "how much do they spend". Part of In-depth Deep Search.
---

# Ad intelligence

Turns the public ad library into counts you can defend: who advertises to this target, for how long, with which script, and how far a claim of spend can honestly go.

Read `../_shared/source-access.md` first. It lists what this data can and cannot show. Scripts are in `../_shared/scripts/`.

**Paths.** `$IDS` means `<this skill's base directory>/../_shared`. Run commands from the dossier folder, `research/<slug>/`.

## Setup

```bash
cd "$IDS/scripts/adlib" && npm install   # uses your installed Chrome. Set CHROME_PATH if it is elsewhere
```

Transcribing video ads also needs ffmpeg and `pip install faster-whisper`.

## 1. Plan the queries

Write a query file (example: `../_shared/templates/queries.example.json`). Cover these, per country:

| Query type | Example | Finds |
|---|---|---|
| Direct call-out, exact phrase | "you are a yoga teacher" | Sellers addressing the trade, and which title draws attention |
| Pain, exact phrase | "fill your classes" | Which problems sellers assume |
| Solution | "agency for yoga studios", "leads yoga" | Who sells the category |
| Trade plus outcome, any order | yoga teacher clients | Wider net, with more false positives |
| Page views | Known sellers, by Page id | Everything a Page runs, active and past |
| The demand side | Trade plus their own customers' words | Whether the target itself uses Meta, and for how long |

Exact-phrase counts can be compared with each other. Record the number displayed, even when you do not scroll.

## 2. Capture

Pick a canary: an exact phrase with thousands of results in that country, unrelated to your queries. `<CC>` is the country code, such as GB or FR. `--locale` sets the interface language, `fr-FR` by default or `en-US`, and it can read ads from any country.

```bash
node "$IDS/scripts/adlib/adlib_capture.js" --canary "PHRASE" --canary-country <CC> --canary-only   # check before anything else

node "$IDS/scripts/adlib/adlib_capture.js" --queries q.json --run sweep1 --out notes/ads \
     --canary "PHRASE" --canary-country <CC> --gap 15000 --max-queries 24
```

Run long sweeps in the background. Re-running with the same `--run` resumes.

**Exit codes are instructions.**

| Code | Meaning | What to do |
|---|---|---|
| 0 | Finished | Continue |
| 3 | Wall or captcha | Stop. Report it. Do not retry through it |
| 4 | Silent limit: the canary failed | Wait, retry a few times with long gaps, then report |
| 5 | Explicit rate limit | Keep what was served. Wait and resume later. Pagination limits are common, so expect them |
| 6 | Another stream is running | Wait for it. Never start a second one |
| 7 | The batch ended with queries left | Run it again with the same `--run` |

## 3. Read reach and payers

```bash
node "$IDS/scripts/adlib/adlib_details.js" --pages pages.json --out notes/ads --run details1 \
     --canary "PHRASE" --canary-country <CC>
```

This opens the public details panel of each ad, with EU reach, targeting, beneficiary and payer. It is slow, so limit it to Pages that matter (`cap` per Page, example in `../_shared/templates/pages.example.json`). Multi-version groups do not show reach. The first ads displayed are not a random sample, so say so. Each row of `details_<run>.jsonl` holds `reach` and `text`, the raw panel. Targeting, beneficiary and payer are in `text`, so read them there. Who pays matters: if each client's own company is the payer, the seller is not buying the media.

## 4. Transcribe and see the creatives

The text field misses what is spoken in videos and written on images, and for many sellers the hook lives there.

```bash
python3 "$IDS/scripts/ad_media.py" notes/ads/ads_*.jsonl --out notes/ads/media \
    --language <lang> --pages PAGE_ID --min-days 30 --images --limit 40
```

Transcribe the ads that matter most: the longest-running ones of the main sellers. Identical audio is transcribed once. Signed URLs expire, so do this soon after capture. A failed ad is retried on the next run. Look at saved images with your own vision. Transcripts are automatic: label them, and re-check any key sentence.

## 5. Analyse

```bash
python3 "$IDS/scripts/analyze_ads.py" notes/ads/ads_*.jsonl --out notes/ads/analysis \
    --logs "notes/ads/log_*.jsonl" --details "notes/ads/details_*.jsonl" \
    --angles angles.json --cpm 8,15,30 --transcripts notes/ads/media/transcripts
```

| Output | Use it for |
|---|---|
| `pages.csv` | Ads, active, first date, longest and median duration per Page |
| `families.csv` | Scripts clustered by text. Families on several Pages may signal a shared supplier |
| `angles.csv` | Your hooks and guarantees, counted with `angles.json` |
| `spend_floor.csv` | Reach-based spend floor at each CPM, labelled `[E]` |
| `coverage.md` | Displayed against captured per query. Publish this with your report |
| `ads.csv` | Every ad, with its URL, text and spoken words |

Then read a sample yourself, because counts cannot tell a seller from a look-alike.

## 6. Spot shared scripts honestly

Several small businesses running the same text may point to one supplier. Test it, with the alternatives: copying between peers, another supplier, a shared course.

Traces of a template worth looking for:
- A leftover from another client: a map of the wrong city, a wrong region, the wrong gender for the owner
- The same worked example with the same number across regions
- First use that follows the date someone joined a program
- Bursts on the same dates across Pages

State a confidence level per Page, and how it was matched. These are real small businesses, so keep "probable" visibly apart from "confirmed", and draw no conclusion on an individual without another proof.

## Report honestly

- Every count is a minimum. Say so next to it.
- Duration does not prove profit. A very short ad does not prove failure either.
- No spend, clicks or leads exist in public data. A spend figure is a floor from reach, with a CPM range.
- List queries never run and Pages left incomplete.

## Done when

- [ ] The canary was run, and zeros were checked against it
- [ ] Coverage is published, with displayed and captured counts
- [ ] Every ad cited has its library URL and exact text
- [ ] Spoken words of the key ads were transcribed and labelled automatic
- [ ] Limits met are stated with their time, and none was worked around
