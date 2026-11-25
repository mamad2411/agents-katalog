---
name: haskie
description: >-
  The user's personal knowledge layer: the document collections they curated, searched before the web or your memory. Use it to answer, explore, plan or decide, to cite an answer to something they own, or when they speak of "my documents", "my collection" or "my sources". It covers every topic they have collected sources on{topics}.
---

# haskie: the user's personal knowledge layer

The always-loaded rule says when to search, which search to pick and how to judge what comes
back. This file is the tool reference.

## Session

The SessionStart hook prints "{announcement}" into your context. Pass that id unchanged. A call
without it shows in no session of the user's Sessions view. If the line is missing, pick one short
string (at most 128 characters) and reuse it for the whole conversation.

## Search tools

Each search tool's description says where it looks, how to split and word `q`, what `limit`
counts, and how `also_in` folds repeats. This section adds what those descriptions leave out: the
fields to read, and the defaults.

**`search_excerpts(q, context?, session_id?, collections?, limit?, document_ids?, section_ids?)`**
→ `excerpts`, `uncovered`, `missing_terms`, `searched` (the collections it covered). A match counts
as weak in `uncovered` when it scores under the bar its models were measured at.

- `limit`: sections, default 10, and never fewer than the parts.
- A passage is matching chunks that sit next to each other. A result held by several collections
  in scope comes back once.
- `document_ids` keeps to these documents, `section_ids` to these sections and every section
  under them, at most 100 of each: the `document_id` of any result or the `id` of a document
  row, the `id` of a section from `search_sections`, the `section_id` of an excerpt or span.
- cite: `document`, `header` ("parent > … > heading") and `location` ("doc p.3-4 L10-20", first
  passage to last). `section_id` names the excerpt's section.
- read: `score` is the best passage's. `collection` is whose index matched.
- `spans`: one per passage, in document order, each with `header`, `section_id`, `location`,
  `score`, and when there are any, `aspects` and `also_in`. The excerpt's `aspects` names the
  questions it answers; a span's `aspects` holds the positions in that list of the ones its
  passage answers (`[0, 2]`: the excerpt's first and third). An empty list or map is left out of
  every answer: no `aspects` for one question.
- The excerpts stay within `answer_budget_chars` (44,000 characters by default), short of the size
  Claude Code moves out of your context into a file; only the first section's best passage may go
  past it. Each section's best passage goes in before any section's next one; a passage that does
  not fit is left out whole.
- open: `markdown_file` (absolute path), at the lines `location` names (`L10-20`, 1-based).
- `missing_terms`: with a reranker on, the full-text find joins only when the reranker judges it
  an answer, and scores what the reranker gave it. Without one, its span scores 0. It can also
  hold a verb of the question ("pick"); the content words are the ones that count.
- Each place in `also_in` has `collection`, `document`, `header`, `location`, `score` (its own
  match to the query), `relation` to its parent, `similarity` (how strongly that relation holds),
  `to_parent` and `to_root`. Different authors rarely repeat each other's sentences, so `also_in`
  is often empty across documents: an empty one does not mean the sources disagree.
- A follow-up search sends back sections you already read. Aim it with `section_ids` or
  `document_ids` instead of asking the same question in other words.

**`search_sections(q, session_id?, collections?, limit?, document_ids?)`** → `sections` (in pick
order), `documents` (best first), `collections`, `searched` and `uncovered`. A map of a topic, near
topics included, with no text, and the documents that cover it. With a reranker on, it weighs every
chunk and drops none. `document_ids` keeps it to those documents.

- `limit`: sections, 1 to 40, default 15. At most two of one document while another has a section
  on the topic left.
- Per section: `id`, `document_id`, `header`, `location` (it names the document), `chars` (its
  length), `chunks` (how many of its chunks matched), `score`.
- `descriptors`: up to six words or phrases for what the section is about. They may repeat
  topics named in its `header`.
- Picks come by coverage, not by score, so `score` does not fall down the list. The fewer the
  documents, the more picks are back matter or, with no reranker, sections that share only a word
  with the topic.
- `related`: the sections the map did not pick that sit closest to this one, at most five, each
  with `id`, `header`, `location`, `score` and `similarity`. It means nearby, not repeated. A near
  copy lands here, and so can the best section on the topic.
- `related` differs from `also_in` in `search_excerpts`. A place in `also_in` passed a repeat
  test, so it can be skipped, or cited as another source when its `document` differs. A section
  in `related` passed no such test.
- `documents`: the ten documents the search matched most strongly, over every chunk it read, and any
  other document a listed section is in, so every section's `document_id` has its row. Per
  document: `document_id`, `document`, `description`, `score`, `chunks`, `sections` (how many of
  the map's sections are in it, 0 for none), `collections` and `markdown_file`. `score` is a sum
  by default, so read it with `chunks`. A document with 0 `sections` was reached but not mapped:
  map it alone with its id in `document_ids`.

**`set_session_collections(session_id, collections)`** → the selection now, at most 100 names. It
replaces the previous selection; it does not add to it. It scopes every later search of the
session.

## Catalogue tools

Paged tools take `page_size` (default 100, at most 1000), `cursor`, `sort` and `order`
(`asc`/`desc`). They return `items`, `next_cursor` (null on the last page) and `total`.

- **`list_collections(sort: name|created_at)`** → `name`, `description`, `created_at`, `counts`
  (`total`, `indexed`, `active`, `error`, `by_status`). This list is current; the trigger above is
  only as fresh as the session that loaded it.
- **`get_collection(collection)`** → `name`, `description`, `counts`, its `overrides`, the
  `effective` chunk settings, the `search` settings, `index_outdated`, `maintenance` and `index`
  statistics. It does not list the documents.
- **`list_collection_documents(collection, status?, sort: name|size|status|updated_at)`** → one
  membership per document: the `document` row, `status`, `error`, `added_at`, `updated_at`.
  `status` is how far this collection got indexing it (`pending`, `indexing`, `indexed`, `error`,
  `cancelled`), or `removing` while a detach removes it. It is not the import status.
- **`list_documents(status?, sort: name|size|status|updated_at)`** → document rows, each with
  `collections`: how many hold it. `status` is one of `queued`, `converting`, `embedding`,
  `imported`, `error`, `cancelled`, `deleting`.
- **`get_document(document)`** → one such row.
- A document row: `id`, `name`, `suffix`, `size`, `status`, `error`, `preview`, `parser`,
  `skip_ocr_pages`, `description`, `created_at`, `updated_at`.

## Write tools

Every write takes `session_id`, so the change shows in the conversation's history.

- **`add_document(path, name?, description?, parser?, skip_ocr_pages?)`** → the document row at
  `queued`. `path` is an absolute local file. The name is stored in lowercase-kebab-case with the
  original suffix, so use the returned row's `name` from then on. Converting and embedding run in
  the background: poll `get_document` until `imported`, `error` or `cancelled`.
- **`add_document_to_collection(collection, document)`** → `operation_id`. The document must be
  `imported` first. It is searchable there once its membership reads `indexed`: poll
  `list_collection_documents`.
- **`remove_document_from_collection(collection, document)`** → nothing. It detaches only; the
  document stays imported. It answers once the removal is queued: the membership reads `removing`
  until it is gone.
- **`describe_document(document, description)`** → the updated row. An empty description clears
  it. `search_sections` shows the description beside each document, so write one for anything an
  agent must choose between.
- Not over MCP: creating, describing, tuning, re-indexing or deleting a collection; deleting or
  re-importing a document; operations and settings. Point the user to the web UI.

## Log and gap tools

haskie keeps every search, so the collections can grow where they fall short.

- **`list_searches(session_id?, days?, limit?)`**: to recall what this conversation already
  searched.
- **`list_gaps(review?, days?, signals?)`**: when the user asks what the collections lack. Tell
  them which topics keep coming back; they are what to add next.
- **`replay_gaps(ids)`**: to check whether the collections answer a gap now.
- **`report_gap(session_id, question, verdict, missing?)`**: judges the newest search of this
  session that asked those exact words, whichever search tool ran it.
- **`review_gaps(ids, review)`**: to resolve a gap once `replay_gaps` shows it answered, or to
  dismiss one the collections are not meant to answer.

## Errors

A failed call is a tool error with a status code and a message that names the problem.

- **503**: an embedding or reranker model is still downloading or warming. Wait and retry. If the
  message says the model failed to load, retrying will not help: tell the user.
- **404**: no such collection or document, including a name in `collections`, or a document that
  is not in the collection. Check the name with `list_collections` or `list_documents`. From
  `report_gap`: no search in this session asked that question, word for word, in the last hour.
- **409**: the document name is taken, the same file is already imported (the message names that
  document: use it), or the document is not `imported` yet. From a search: a collection named in
  `collections` has no document to search yet (none indexed, or all on their way out); leave it
  out. From
  `report_gap`: that search failed, so there is nothing to judge.
- **422**: a bad argument. For example: `limit` out of range or below the number of parts, no
  parts or more than 5, a question over 500 characters, a `context` over 200 characters, a page
  size over 1000, an unknown `status` or `sort`, a `path` that is relative or missing, or a file
  type haskie cannot read.
