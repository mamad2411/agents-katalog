---
name: reprendre-corrections
description: Reprendre dans le graphe un document corrigé par un expert — `propose_from_document` quand le document porte ses ancres, le rendu PDF dans un sous-agent quand elle ne les porte pas, puis une seule modification groupée, et ne jamais contester ce qu'on n'a pas vu soi-même. À utiliser quand quelqu'un rend un .docx annoté ou corrigé, ou dit « voici les corrections », « l'expert a relu », « reprendre ses remarques », « intégrer les corrections ».
---

# Taking an expert's corrections back into the graph

The expert opened a produced sheet, corrected it in place, and handed it back. Your job is to turn
their corrections into graph edits — faithfully, and without inventing objections.

## D'abord : `propose_from_document`. C'est exact, pas approximatif.

Si le document a été produit par `render_document`, il porte l'identifiant de chaque nœud à
l'intérieur du fichier — invisible sur la page, conservé quand une personne édite autour. Alors
**ne devinez rien** : appelez `propose_from_document` avec son `relPath` et le serveur vous rend
l'appariement exact.

Il rend trois choses, et la différence entre elles est tout le sujet :

| | |
|---|---|
| **edit** | même nœud, mots différents. Sans ambiguïté — repris tel quel dans `editItems`, à la forme exacte qu'`edit_nodes` attend. |
| **missing** | le graphe l'a, le document ne l'a plus. **Signalé, jamais supprimé** : une coupe voulue et un faux mouvement se ressemblent dans un fichier Word. |
| **unplaced** | du texte qui n'appartient à aucun nœud. Signalé **sans parent** : deviner d'après la position, c'est ainsi qu'une phrase se retrouve sous la mauvaise leçon. |

Il **propose et n'écrit jamais**. L'application passe par `edit_nodes` comme toute autre
modification : l'expert voit le diff avant que quoi que ce soit soit publié.

Une réponse `anchored:false` veut dire que le document ne vient pas de `render_document` — passez
alors à la marche à suivre ci-dessous, qui est faite pour ce cas.

## Sinon : lisez le RENDU PDF, jamais une conversion Word ou LibreOffice.

Pour un document **sans ancres**, la règle qui suit n'est pas négociable, et elle est mécanique,
pas stylistique.

**Une conversion perd les tableaux.** Tout ce qui est mis en page dans un tableau disparaît du texte
extrait, sans la moindre erreur. Vous « découvrez » alors qu'il manque du contenu, et vous le
signalez — alors qu'il était là depuis le début, sur la page, dans un tableau. C'est arrivé, et les
fausses objections ont coûté une journée.

Donc : travaillez sur le **rendu PDF**. Si vous n'avez qu'un `.docx`, dites-le et demandez le PDF
plutôt que d'avancer sur du texte converti. `get_document_text` extrait d'un `.docx` par un
convertisseur et porte exactement cette limite — bon pour un coup d'œil, pas comme base d'une
objection.

*(La restriction ne vaut pas pour `propose_from_document` : il lit le XML du fichier, pas une
conversion, donc les tableaux ne lui échappent pas.)*

## Do the reading in a subagent

Pour un document sans ancres seulement. Dispatch the `lecteur` subagent: it reads the whole source
and returns **a structured edit proposal** — a list of `{ what changed, where, from, to }` — not a narrative.

This is the single largest token saving available: a bulk read that costs ~184,000 tokens inside a
subagent returns ~2,000 to the main thread. Read the source yourself only when the proposal points
at something you must verify with your own eyes.

## Then write it the shared way

From here on it is the procedure in `session-autorat`, « Proposer, puis écrire » : resolve every
target name in **one** `find_node` call, one `edit_nodes` batch with an item per node carrying only
the fields that change, shown in French and grouped by lesson before the confirm. Two reminders
that cost a day each when forgotten: never loop one edit per correction, and never delete and
re-add a node to "replace" it — that mints a new id and breaks every reference to it silently.

## Never raise an objection you have not seen

Before you tell the expert that something is missing, wrong, or inconsistent: **find it in the PDF
yourself.** Quote the page.

Four objections were raised last week that were not real, and each was caught only because a person
opened the PDF. An objection you cannot point at is a guess, and the expert has to spend their time
disproving it.

If the proposal and the document disagree, the document wins and the proposal is wrong.

## Then present it

Show the batch as the expert would recognise it — grouped by lesson, in their vocabulary, in French.
Get an explicit yes, then confirm. A correction that reverses an earlier decision gets a dated line
in the section's journal saying so (`composer-un-document`).
