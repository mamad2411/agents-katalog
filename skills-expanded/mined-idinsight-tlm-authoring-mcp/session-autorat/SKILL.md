---
name: session-autorat
description: Discipline de session pour l'autorat de matériels pédagogiques avec le serveur TLM — s'orienter avant d'agir, résoudre les noms plutôt que réclamer des identifiants, montrer chaque modification en français avant de la confirmer, et ne publier que sur accord explicite. À utiliser au DÉBUT de toute session d'autorat et à chaque écriture dans le graphe, le catalogue ou l'historique des documents. Se déclenche notamment sur « où en suis-je », « reprendre le travail », « modifier le programme », « ajouter une leçon », ou toute demande qui va écrire.
---

# Session discipline

This applies to every authoring session. The other skills assume it and do not repeat it.

## Orient before you act

1. **`start_here`** — first call, always. It says where you are, what your role allows, whether a
   draft is open, and what is unfinished. Relay it as a situation report in the user's language.
2. **`get_graph_guide`** — before you read or change anything in the graph. This is where the
   subject's conventions live: its vocabulary, how its content is shaped, what coverage it expects.
   You do not know these. Do not answer from memory, and do not carry a rule from one subject to
   another.
3. **`namespace_stats`** — before writing any traversal. It is argument-free and cheap, and it saves
   you from a `walk_graph` that returns the wrong shape.
4. **Announce the subagents this session will use, and for what** — measuring a produced file,
   reviewing a render, reading a long external document — before you act. Commit the delegation
   while there is nothing to carry: once momentum builds, the main thread does the work itself and
   only notices afterwards, from the bill. The subagents work on FILES, never on the graph (see
   below), so what you delegate is file work.

`get_capabilities` answers "what is possible" for a machine; `start_here` answers "what do I do
next" for a person. Prefer `start_here` when talking to someone. When you do need the machine
answer, it returns a digest — pass `section:'editable'`, `'catalog'`, `'lifecycle'` and so on for
one area's detail rather than trying to fetch everything.

## Read a subtree in one call, not one call per hop

`walk_graph` takes a `maxDepth`, and that is how you read a container and everything under it in a
single call. **Descending one level per call is the defect this prevents.** A real session spent
dozens of reads assembling what a handful would have returned, because it walked down from the top
of the graph a hop at a time instead of jumping to the container and reading its subtree.

1. **`find_node`** for the name the expert used. That jump is what replaces the descent.
2. **`walk_graph`** from that id, `direction:'out'`, with `maxDepth` set to cover the subtree. How
   deep a container runs is a property of the graph, never something to assume: `truncated` in the
   response says the cap hid deeper nodes, so raise it and call again.
3. **`detail:'skeleton'`** whenever the question is structural — what is here, in what order, how
   many, which id is which. It drops authored prose and returns many times more nodes per page. Read
   in full only the few nodes you are going to write from.

Believe the three flags rather than retrying the same call: `truncatedByLimit` means page with the
cursor, `truncated` means raise `maxDepth`, `truncatedBySize` means a byte budget trimmed the page
and a larger `limit` cannot help.

## The subagents work on files, not the graph

`mesureur`, `lecteur`, `relecteur` and `terminologue` have Read but no graph tools. They act on
**files** — a rendered PDF, an uploaded `.docx`, a pile of notes — never on a `walk_graph`. The
graph and document reads stay in the main thread, because that is where the tool access lives: the
server reaches this session as a connector, and a plugin cannot hand a connector's tools to a
subagent, so a shipped agent that named a graph read would name nothing.

This decides WHAT to delegate. Give a subagent a job it can finish from a file you did not have to
read for it: measure a `.docx` you produced (`mesureur`), review a rendered page (`relecteur`),
check the terminology of a produced file (`terminologue`), read a long external document
(`lecteur`). Do NOT dump a graph payload to a file just to hand it over — you had to read it to
write it, so the context is already spent; read it in the main thread. And a subagent never calls
`set_context`: it makes no graph reads to scope.

## An open draft may be someone else's

`start_here` reports `draftActivity` — how many edits are staged, when, and by whom. **An open draft
is often live work from another session.** If the last edit is not yours, say so and ask before
adding to it. Never suggest publishing or discarding a draft to get a clean baseline: `publish` has
no undo and `discard_draft` is final.

## Never ask for an identifier

The expert has names, not ids. Asking for a UUID is a defect in the procedure, not a limitation.

- Ask for the **name**, in their words — « le chapitre 5 », « le guide de l'enseignant ».
- Resolve it with **`find_node`**. Several names at once go in **one** call via `queries` — its
  `unresolved` field names everything that did not land on exactly one node.
- When a name is ambiguous, the response says `ambiguous` and each candidate carries a containment
  `path`. **Ask which one, quoting the path.** Do not guess: picking wrong writes silently against
  another document, and nothing will error.

Speak the expert's words throughout — document, section, chapter, objective, lesson. Never TLM,
SFI, `hasPart`, node, label, or an id. Everything the server hands you is English; relay it in the
language the subject's guide is written in.

## Proposer, puis écrire — la procédure partagée

Toute écriture dans le graphe suit le même chemin, quelle que soit la capacité — construire le
programme, composer un document, reprendre des corrections — et quelle que soit la source de la
proposition. Les autres compétences renvoient ici au lieu de le répéter.

1. **Obtenir une proposition structurée** — une liste d'éléments nommés, jamais un récit. Trois
   sources, une seule forme de sortie :
   - **à la main** : l'expert dicte ; reformulez en liste et montrez-la avant d'aller plus loin ;
   - **depuis une recherche dans le graphe** : `find_node` sur les noms, `walk_graph` depuis l'id
     trouvé en `detail:'skeleton'` — ce qui existe borne ce qui reste à créer. Une recherche hors
     du graphe, quand le client en dispose, donne une proposition comme une autre, avec sa source ;
   - **depuis un document** (PDF, .docx, notes) : le sous-agent `lecteur`, qui renvoie la structure
     et jamais le contenu — son contrat dit la forme selon ce qu'on construit. Un .docx produit
     par le serveur porte ses ancres : `propose_from_document` d'abord, c'est exact.
2. **Résoudre les noms en un appel** — `find_node` avec `queries`. `unresolved` et `ambiguous`
   sont des questions à poser en citant le chemin de chaque candidat, jamais des choix à faire.
3. **Une écriture groupée** — `add_nodes`, `create_edges` ou `edit_nodes` avec leur tableau
   d'items, un niveau à la fois : un élément créé dans un lot ne peut pas être parent dans le même
   lot. Une modification est un `edit_nodes`, jamais une suppression suivie d'une recréation — cela
   change l'identifiant et casse en silence tout ce qui y renvoyait. Répéter une écriture par
   élément est le défaut que le lot évite.
4. **Montrer, puis obtenir un oui** — le dry-run, en français, dans le vocabulaire de l'expert,
   groupé comme il le reconnaît (par leçon, par document). Puis seulement le confirm, ci-dessous.
5. **Noter la décision** — si l'écriture touche un document ou une de ses sections pour une raison
   qui n'est pas évidente, une entrée dans son journal par `append_journal` (`composer-un-document`).

La forme de chaque élément vient de `get_capabilities section:'editable'` et les conventions de la
matière de `get_graph_guide` ; rien de cela n'est écrit dans une compétence.

## Every write is two-phase, and the second phase is yours to earn

A dry-run returns a diff and a `confirmationToken` and changes nothing. The confirm applies it.

**The token is not a proof that a human agreed** — the server issues no dialog of its own, so
anything it hands you, you could hand straight back. The gate is your cooperation. So:

1. Run the dry-run.
2. **Show what will change, in French, in the expert's vocabulary.** Not the raw diff — what they
   would recognise: which lesson, which section, what text becomes what.
3. Get an explicit yes.
4. Only then confirm. If the dry-run reported `payloadStored:true`, confirm with the token alone.

If the dry-run returns warnings or `irreversible:true`, read them out before asking.

## Know which writes have a draft behind them, and say so

| write | what it costs to be wrong |
|---|---|
| graph edits (`add_nodes`, `edit_nodes`, `move_node`, `add_section`, …) | staged on a draft — `undo_last` takes back one, `discard_draft` all of them, nothing reaches generation until publish |
| **catalog writes** (any tool with `catalog:`) | applies **and publishes** in one step: no draft, no `undo_last`, and other workspaces may be using the entry |
| **document and history writes** (`create_upload_url`, `log_generation`, `record_document_content`) | live immediately: no draft, no undo |
| `publish_draft` | makes the whole draft live |

For the bottom three, say plainly that there is no undo before asking for agreement.

## Publish only on explicit, recent consent

"Recent" means in this exchange — not agreement given earlier in the session for something else.
Publishing is an approver's act. If the expert is a curator, the right ending is `request_review`
with a summary note, not a publish.

## When you are unsure

Stop and ask. The expensive failures in this project were confident actions on unverified
assumptions, and every one of them was caught by a person looking at the actual artifact.
