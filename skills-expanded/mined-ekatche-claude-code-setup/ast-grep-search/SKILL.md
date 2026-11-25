---
name: ast-grep-search
description: Use when searching for a code shape rather than a string — call signatures, wrappers, patterns to rewrite — or when reading a file's structure without opening it.
---

# ast-grep (`sg`) — recherche structurelle

`sg` lit l'AST, pas le texte. Il est le seul outil ici capable de trouver une
*forme* de code, et le seul capable de la réécrire.

## Chercher une forme

```bash
sg -p 'foo($$$ARGS)' -l python          # tous les appels à foo, quels arguments
sg -p 'if ($COND) { $$$ }' -l ts        # tous les if, quel que soit le corps
```

`$VAR` capture un nœud, `$$$VAR` capture une liste. Un motif écrit en texte
plat ne trouvera pas un appel réparti sur trois lignes ; le motif AST, si.

## Lire la structure sans lire le fichier

```bash
sg outline -l python chemin/fichier.py
```

Renvoie les définitions et leurs lignes. C'est ce qu'il faut avant une lecture
ciblée d'un gros fichier — pas une lecture intégrale.

## Réécrire

```bash
sg -p '<avant>' --rewrite '<après>' -l <lang> --interactive
```

Toujours `--interactive` d'abord : une réécriture AST touche chaque
correspondance du projet.

## Quand ne pas l'utiliser

Question en langage naturel : `mgrep`. Chaîne littérale exacte : `rtk grep`.
`sg` est précis sur la forme, muet sur l'intention.
