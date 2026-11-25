---
name: code-search
description: Use when searching, locating, or exploring code — choosing between mgrep, ast-grep, and literal grep.
---

# Recherche de code — par compétence, pas par prix

L'abonnement mgrep est payé : il passe en premier **là où il est le meilleur
instrument**, et nulle part ailleurs. Dépenser un crédit pour localiser un
symbole dont on connaît déjà le nom, c'est du gaspillage, pas de la
priorisation.

| Besoin | Outil |
|---|---|
| Question sémantique en langage naturel | `mgrep '<question>'` — **1er choix** |
| Motif structurel, une forme de code | `sg -p '<motif>' -l <lang>` — seul capable |
| Structure d'un fichier, sans le lire | `sg outline -l <lang> <fichier>` |
| Texte littéral exact | `rtk grep '<texte>' <chemin>` — après l'un des précédents |

`grep`, `rg` et `find -name` bruts sont bloqués tant qu'aucun appel supérieur
n'a eu lieu dans le tour. Le blocage n'est pas un conseil : le hook renvoie
`decision: "deny"` et l'appel n'a pas lieu.

Quota mgrep épuisé : c'est détecté automatiquement et les blocages se lèvent
seuls pendant 24 h. Inutile de contourner.
