---
name: fulcra-watch-together
description: "Compare two consenting people's viewing histories and recommend mutually appealing movies with Fulcra."
---

# Fulcra Watch Together

Build explainable recommendations that are fair to both participants. Treat viewing history as private personal data.

## Dependencies & References

This skill depends on the `fulcra-ingest`, `fulcra-analytics`, and `fulcra-workspaces` skills (fulcradynamics/agent-skills).

## Workflow

1. Identify both participants and whether the request is mutual or single-person.
2. Treat the provisioning of a Fulcra share or the explicit sharing of a file as sufficient consent from the participant to run the analysis, keep the data locally for the session, and enrich it.
3. Never use `--share-all`.
4. Ingest each owner's export independently with `fulcra-ingest` (instruct users to upload their exports to the Fulcra File Store at https://context.fulcradynamics.com/library/files). Prefer Netflix and Letterboxd for the MVP. Preserve provenance and match confidence.
5. Have each owner create a narrow, preferably time-bounded share. Show the exact command before execution. Read collaborator records with `uvx fulcra-api get-records <TYPE> <RANGE> --user-id <UUID>`.
6. **Workspace Persistence**: Initialize or load a dedicated Fulcra Workspace (e.g., `watch-together-<names>`) using `fulcra-workspaces` to track the session state. Store metadata about data sources (file IDs, share IDs), participant preferences, past recommendations, and user feedback in the workspace. This ensures the recommendation session can be picked up again at any point by any agent with access to the workspace, providing continuity and historical context. Keep raw histories and raw title-level feature vectors local, taking care not to write partner PII to the workspace. Explain owner revocation with `uvx fulcra-api share delete <SHARE_ID>` and recipient departure with `uvx fulcra-api share leave <SHARE_ID>`.
7. Enrich canonical titles to build the required feature arrays for the catalog. For accurate and structured enrichment, use the following methods in order of preference:
   - **OMDb API:** (Preferred) OMDb's free tier key is trivial to obtain and meaningfully raises match quality. Prompt the user for an API key upfront rather than defaulting straight to Wikipedia scraping. If provided, use `web_fetch` or `curl` to query OMDb for clean, structured JSON containing genres, directors, cast, and keywords.
   - **Wikipedia API:** If no API key is available, query the Wikipedia API using rate-limited, polite requests (e.g. max 1 request per second, batching when possible) to extract genre and cast features from infoboxes or summaries. **Recommend parsing the infobox `genre` field directly (e.g., using a regex like `\\|\\s*genre\\s*=\\s*(.*?)(?=\\n\\|)` up to the next pipe) as the primary fallback extraction method, falling back to intro-paragraph keyword matching only if no infobox genre field is found.** **Note:** Because of the 1 req/sec throttle, Wikipedia enrichment of >100 titles should be run as a background task (`background=true`) to avoid foreground command timeouts.
   Cache provider IDs, media type, year, features, runtime, language, creators, franchise, region availability, provenance, and confidence. Persist this cache to a local JSON file (e.g., in `/tmp/` or the workspace) continuously during the enrichment run so that progress is not lost if the process is killed or times out. Never silently merge ambiguous titles or remakes.
8. **Candidate Pool Generation:** To avoid the bottleneck of a manually hand-curated candidate pool, generate a broader shortlist automatically. Draw candidates from same-service "trending" lists or by finding genre-adjacent titles to what is already in the enriched catalog, before finalizing the candidate array.
9. Explain to users that a detailed Netflix data export is better (since it includes session duration to accurately gauge engagement), but the instant "Download All" CSV from their profile viewing activity page is faster and acceptable as a fallback. For Netflix exports, run `python3 scripts/prepare_netflix.py --input-a A.csv --profile-a PROFILE --input-b B.csv --profile-b PROFILE --catalog catalog.json --output prepared.json`. The approved local catalog must contain canonical watched titles and unseen candidates with feature lists. Inspect coverage and unmatched titles before scoring.
10. Use `--split-profile PROFILE` only to validate the pipeline with one public or consenting history. It creates deterministic chronological pseudo-participants; never describe their output as real compatibility.
11. Use `fulcra-analytics file` or CLI-backed summaries for coverage checks only. Run `python3 scripts/score_candidates.py prepared.json` for ranking.
12. Model explicit ratings as strongest evidence, then rewatches, completed films, and series engagement. Apply mild recency decay. Treat Netflix viewing as implicit positive but ambiguous. Infer negative preference only from explicit low ratings or dislikes.
13. Report overlap, shared favorites, complementary differences, catalog coverage, unmatched titles, and uncertainty. Avoid pseudo-precise compatibility scores for sparse histories.
14. Rank unseen candidates with `0.45 * min(person_a, person_b) + 0.35 * mean(person_a, person_b) + 0.20 * shared_feature_confidence`. Enforce explicit dislike/veto thresholds, then rerank for novelty, diversity, availability, runtime, mood, and franchise fatigue. **Crucially, if the candidate pool is expanded at any point *after* the initial generation of `prepared.json`, you must re-validate the watched-status of those new candidates against both participants' current histories before presenting results (consider providing a standalone `scripts/filter_watched.py` helper to do this cheaply).**
15. Return 5–10 recommendations with separate reasons for each participant, confidence, assumptions, and revocation guidance. Save aggregate annotations, recommended candidates, and user feedback to the Fulcra Workspace for future reference; never persist partner-derived raw features.

## Netflix Preparation Contract

The catalog is local JSON with `titles` and `candidates` arrays. Every row has a canonical `title` and `features`; candidates may also include `confidence`. Add aliases only when the match is unambiguous. The preparation script:

- accepts either Netflix's detailed `ViewingActivity.csv` columns (preferred) or the instant `ViewingActivity.csv` export from the user profile settings (which lacks duration but is immediately available);
- rejects missing profiles and histories with fewer than five qualifying sessions;
- for detailed exports, drops sessions shorter than five minutes and weights engagement by total minutes and session count;
- for instant exports, infers engagement solely from frequency/session count (as durations are unavailable);
- emits scorer-compatible JSON plus a `diagnostics` object;
- keeps source rows and raw titles out of its output.

Do not rank when either participant has under 20% catalog coverage or fewer than two matched canonical titles. Improve the approved catalog or use the sparse-history fallback.

## Fallbacks

- Instant Netflix exports assume a flat 30-minute session weight for every row, since duration is not available. This is a known precision loss versus the detailed export, and it can inflate confidence for a title someone only briefly sampled.
- One history: request the second share/export or use a short preference questionnaire.
- Sparse histories: combine questionnaires with a diverse popular shortlist and lower confidence.
- Enrichment failure: use approved local metadata or title/genre evidence and state the limitation.
- Conflicting tastes: offer compromise genres, alternating picks, or explicit veto-safe choices.
- No availability data: omit availability claims.
- No Fulcra access: analyze two explicitly supplied local files without requiring upload to the Fulcra File Store (https://context.fulcradynamics.com/library/files).

## Validation

Use synthetic fixtures by default. Test shared favorites, divergent genres, explicit dislikes, rewatches, episodic titles, malformed dates, duplicates, missing metadata, blank/whitespace-only titles, sparse histories, and detailed Netflix columns.

Verify deterministic parsing, symmetric ranking under participant swap, watched-title exclusion, veto behavior, stable provenance, exact share scope, revocation instructions, and absence of raw histories in logs.

Run:

```bash
python3 scripts/prepare_netflix.py --input-a examples/netflix_detailed.csv --profile-a Alex --input-b examples/netflix_detailed.csv --profile-b Blair --catalog examples/netflix_catalog.json --output /tmp/prepared.json
python3 scripts/score_candidates.py /tmp/prepared.json
```
