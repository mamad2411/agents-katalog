---
name: cx-conversation-embedding-pipeline
description: Use to design a pipeline that vectorises support conversations for semantic search or retrieval, with the chunking, PII and deletion decisions made before anything is embedded. Trigger for "make our support conversations searchable", "build a vector index over tickets", "semantic search across transcripts", RAG over support data, chunking transcripts, or an embedding index that returns unhelpful matches.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Vectorising support conversations

Semantic search over support history is genuinely useful: finding the precedent for an
unusual case, grounding an AI agent, or locating every conversation about a topic without
guessing keywords.

Two things make this harder than the usual document-embedding pipeline, and both need
deciding before the first vector is written.

**Conversations are not documents.** They are multi-party, interleaved, and the useful unit is
almost never the whole thread or the single message.

**An embedding is a copy.** Deleting a conversation and leaving its vectors in an index means
the content is still retrievable, so erasure and retention have to reach the index too — and
an index built by an external API means the content went to that API.

## Chunk on turn boundaries, not on character counts

Fixed-size chunking is the default in most tooling and it is wrong here. Splitting mid-turn
produces chunks containing half of the customer's problem and half of the agent's answer,
which retrieve badly and read worse.

- **The customer's opening turn is the highest-value chunk** for most retrieval, because it is
  the closest thing to the query someone will type. Index it separately and consider
  weighting it.
- **Group a customer turn with the agent's response** to it. Question and answer together
  is the unit that answers "how did we handle this".
- **Never split a turn across chunks.** Where a turn exceeds your model's window, split it on
  sentence boundaries and overlap.
- **Keep an unchunked summary** per conversation, embedded separately, for
  find-me-similar-cases retrieval. Chunk-level and conversation-level retrieval answer
  different questions.
- **Drop the noise before embedding**: signature blocks, quoted reply chains, legal
  disclaimers, and automated acknowledgements. Quoted history in particular means the same
  text is embedded once per reply, which floods retrieval with near-duplicates of the same
  conversation.
- **State-change events are not content.** Assignment and status records have no semantic value
  and dilute the index.

## Attach the metadata that makes retrieval usable

An embedding index over conversations with no filters is much less useful than it looks —
almost every real query is scoped.

Store alongside each vector: conversation id, source, channel, language, date, status,
resolution, product or contact-driver category, and whether the turn was internal.

Then **filter before or alongside the vector search**. "Similar cases resolved in the last six
months, on email, in German, excluding internal notes" is the actual query, and a pure
similarity search cannot express it.

Two metadata decisions worth making explicitly:

- **Internal notes must be separable.** Grounding a customer-facing bot on internal notes will
  surface internal reasoning to customers. Either exclude them from the index or make the
  flag mandatory in every query path.
- **Language.** Multilingual embedding quality varies by language, and mixing languages in one
  index without a language filter produces confident cross-language matches that are
  frequently wrong.

## Do the PII work before embedding, not after

The decisions, in order:

1. **Should this conversation be in the index at all?** Exclude special-category content,
   anything under legal hold or an open dispute, anything outside retention, and anyone who
   has objected or requested erasure.
2. **Redact before embedding.** A vector computed from unredacted text carries that content —
   and while it is not straightforwardly readable, treating an embedding as anonymous is a
   mistake. Redaction also improves retrieval, since names and account numbers are noise for
   semantic matching.
3. **Do not store the raw text in the index** if you can resolve it from the source at read
   time. An index holding both the vector and the full transcript is a second complete copy of
   your support history with its own access model.
4. **Know where the embedding is computed.** An external embedding API means every indexed
   conversation was transmitted to that provider. Check the provider's retention and
   training-use terms **as configured**, not as advertised.

Whether the whole arrangement is lawful — purpose, basis, transfer — is a determination for
whoever owns data protection. Raise it before building, not after.

## Deletion has to reach the index

The failure that will find you later:

- **Erasure and retention deletion must propagate to the index.** Deleting a conversation in
  the helpdesk while its vectors remain leaves it retrievable, which is a defensible thing to
  be asked about and an indefensible thing to have overlooked.
- **Keep the conversation id on every chunk** so deletion is a targeted operation rather than
  a rebuild.
- **Test the deletion path** — delete a conversation, then confirm its chunks are gone and it
  no longer retrieves. Assert this in a test rather than assuming the delete call worked.
- **Backfill and rebuild carefully.** A rebuild from a source snapshot taken before a deletion
  reintroduces deleted content. Rebuild from live source, or reapply the deletion list after.

## Freshness and drift

- **Conversations are mutable.** Reopened, added to, redacted. An index built once diverges
  from the source; decide the reindex trigger — updated-at based, event-driven, or periodic.
- **Redaction after indexing** must trigger a reindex of that conversation, or the pre-redaction
  content stays retrievable. This is the mutation people forget.
- **Changing the embedding model invalidates the whole index.** Vectors from two models are not
  comparable, so a model change is a full rebuild, not an incremental migration. Version the
  index by model and plan the cutover.

## Evaluate retrieval, or you will not know it is bad

An embedding index always returns something, which is why bad ones survive.

- **Build a small labelled set**: real queries with the conversations that should be found.
  Draw the queries from what people actually search for, and from the questions agents ask.
- **Measure recall at the k you actually use**, per language and per channel. A single
  aggregate number hides that one language is unusable.
- **Include hard negatives** — conversations that look similar and are not the answer.
- **Re-evaluate after any change** to chunking, model, or filtering. Chunking changes have
  larger effects than model changes, and are usually made casually.

## Present results to the user

1. **The PII decisions**, first: exclusions, redaction before embedding, whether raw text is
   stored, and where embeddings are computed — with the lawfulness question routed.
2. **The chunking strategy**, on turn boundaries, with the noise removed and the reasoning for
   the unit chosen.
3. **The metadata schema**, and the filters every query path will use — internal-note
   separation and language specifically.
4. **The deletion path**, with the propagation test.
5. **The reindex triggers**, including redaction-after-indexing and the model-change rebuild.
6. **The retrieval evaluation** — labelled set, recall at your k, per language and channel.
7. **What is deliberately excluded** from the index, and the retrieval consequence of excluding
   it.
