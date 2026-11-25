---
name: relate
description: "typed relationship map: how/why one note relates to its vault neighbors"
argument-hint: "<note> [--n=8]"
metadata:
  internal: true
---
Relate from the vault: $ARGUMENTS

Map how and why this note relates to its most relevant neighbors in the vault. Resolve the note, then pull its top 8 related notes via silica's relatedness (the fusion of embeddings + co-occurrence), or as many as the arguments ask for with --n=. Read the target and each neighbor enough to judge the link, and note which neighbors the target already [[wikilinks]].
Output in chat a Markdown table: | Neighbor | Relation | Why | Link |. For Relation pick the type that fits; common ones: prerequisite, elaborates, contradicts, sibling, example-of, depends-on, alternative-to. Why is one line grounded in the notes. Link is [[the neighbor]] if already linked, else 'latent'. Cite every neighbor as a [[wikilink]]. If a neighbor is `contested: true` or contradicts the target, say so in the Why column, and offer to record the contradiction with silica_flag_note; only run it once the reader says so.
READ-ONLY apart from that flag: do not create, edit, patch, or move any note.
