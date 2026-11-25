---
name: publier
description: Transmettre un brouillon — demande de relecture pour un curateur, publication pour un approbateur — après l'évaluation, sur un accord explicite et récent, en disant ce qui est irréversible. À utiliser quand on dit « publier », « faire relire », « transmettre », « envoyer à l'approbateur », « c'est bon, on y va ».
---

# Transmettre

Deux fins possibles pour un brouillon, selon le rôle. Ni l'une ni l'autre ne se fait sans être
passé par `evaluer` d'abord, et sans que la personne ait vu ses constats.

## Finir en curateur

`request_review` marque le brouillon prêt et **n'avertit personne** : l'approbateur le verra à son
prochain `start_here`. La note jointe est donc toute la passation. Écrivez-la comme un résumé de ce
qui a changé et de ce qui reste ouvert, pas « prêt pour relecture ».

`withdraw:true` la reprend.

## Finir en approbateur

`publish_draft` rend tout le brouillon public. Avant de confirmer :

- lisez à la personne les `checks` et les `warnings` du dry-run,
- assurez-vous que l'accord vaut pour **cette** publication, donné maintenant — pas quelque chose
  d'accepté plus tôt pour autre chose,
- dites clairement que ce n'est pas réversible.

Si le problème est une seule écriture et non tout le brouillon, `undo_last` reprend la plus récente
et laisse le reste en place. Il refuse, en nommant l'élément, quand une écriture plus tardive a
touché la même chose — c'est un signal pour regarder, pas pour forcer.

## Un brouillon ouvert peut être celui de quelqu'un d'autre

`start_here` dit qui a fait la dernière écriture. Si ce n'est pas vous, demandez avant de publier
ou de transmettre : ce serait publier son travail en cours.
