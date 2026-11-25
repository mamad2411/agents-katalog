---
name: rekordbox-embedding-clustering
description: Auto-sort an unsorted pile of tracks using embeddings — feel-BPM folding, genre-family taxonomy, 2-level cosine k-means with distinctive naming, and a UMAP sound-map visualizer. Use when clustering tracks or building "sounds like" browsing.
---

# Clustering and auto-sorting by sound

Reference implementations: `scripts/recluster_nocategory.py` (the full
pipeline), `scripts/rebuild_nocat_bpm.py` (incremental variant),
`scripts/viz_precompute.py` + `scripts/viz_app.py` (sound map).

## Always add-only

Build sorted views as NEW playlists (`by-genre/`, `by-bpm/`, `by-sound/`);
never move or modify the source playlist or any other playlist. The user
decides what to file where.

## Feel-BPM first

Stored BPM lies constantly about half/double-time (cloud rap "140" feels 70;
some house "62" feels 124). Before any BPM bucketing, fold to feel-BPM with
genre-anchored rules:
- hip-hop/halftime families ≥ 118 → halve
- house/techno/trance/psy/hardcore/dubstep < 95 → double
- dnb/juke < 120 → double

Optionally fix the stored value permanently where an independent ML tempo
estimate confirms (rb ≈ 2× essentia tempo within 5%): `scripts/bpm_halftime_fix.py`.
Do NOT extend halving to dnb/dubstep — 174/140 are conventional there.

## Two-level by-sound clustering with distinctive naming

1. Global cosine k-means over L2-normed embeddings (sweep K and eyeball —
   K ≈ 26 suited a few-thousand-track pile; scale with pile size).
2. Name each cluster by its dominant **distinctive** sub-genre (≥ 30% share,
   ignoring generic tags like "Electronic"/"House"): cloud-rap, bassline,
   psy-trance, ambient…
3. **The naming rule:** if a cluster can be meaningfully named → own folder;
   else → fold into the base genre-family folder. Same-name clusters merge.
   This is what prevents `hip-hop-2`, `hip-hop-3` numbered junk.
4. Tempo-split each folder into feel-BPM leaves (median-named, sparse bands
   merged, min leaf ~8 tracks).

For genre-primary splits where sub-genre labels exist, invert it: split by
sub-genre first, and k-means only the big generic bucket (see the pattern in
`scripts/recluster_nocategory.py`).

## Incremental additions

Once a clustering is accepted, FREEZE it. New tracks join the nearest existing
cluster by centroid cosine (≥ 0.55), and are left unfiled otherwise. Never
re-run k-means on an accepted layout — names and memberships churn.

## The sound map

UMAP → 2-D scatter (Dash/Plotly), colored by genre/cluster/mood; click →
nearest-neighbor "sounds like" list (cosine over full embeddings, not the 2-D)
+ in-browser audio streaming (Flask `send_file` with `conditional=True`).
Useful for digging, spotting mislabels, and validating clusters before apply.
