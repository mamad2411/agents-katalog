# Règles permanentes pour Cursor dans ce projet Unity

## 1. Toujours faire un plan avant de coder

Avant de modifier du code, commence toujours par écrire un plan clair.

Le plan doit expliquer :
- quel est le problème ;
- quels fichiers seront modifiés ;
- quelles classes ou systèmes sont concernés ;
- dans quel ordre les modifications seront faites ;
- quels risques il faut éviter.

Ne commence pas directement à coder sans plan.

Si pendant la tâche quelque chose semble incohérent, cassé ou différent de ce qui était prévu, arrête-toi et refais un nouveau plan avant de continuer.

---

## 2. Travailler par petites étapes

Pour les tâches compliquées, divise toujours le travail en petites étapes simples.

Ne mélange pas plusieurs gros problèmes dans une seule modification.

Quand une tâche est complexe :
- analyse d’abord le système existant ;
- identifie les fichiers importants ;
- propose une solution simple ;
- modifie seulement ce qui est nécessaire ;
- évite les gros refactors inutiles.

Le but est de garder le projet stable et compréhensible.

---

## 3. Boucle d’auto-amélioration

Chaque fois qu’une erreur est trouvée et corrigée, transforme cette erreur en leçon.

Ajoute cette leçon dans une section appelée :

`Tasks for Lessons`

Chaque leçon doit contenir :
- l’erreur exacte ;
- pourquoi elle est arrivée ;
- comment elle a été corrigée ;
- quelle règle appliquer pour éviter que cela se reproduise.

Au début d’une nouvelle tâche, relis les leçons existantes et applique-les automatiquement.

---

## 4. Ne jamais dire que c’est fini sans vérification

Ne marque jamais une tâche comme terminée sans avoir vérifié que ça fonctionne.

Avant de dire que la tâche est terminée :
- vérifie les erreurs de compilation ;
- vérifie les erreurs Unity Console ;
- vérifie les références nulles possibles ;
- vérifie que les scripts utilisent les bons noms de classes ;
- vérifie que les méthodes appelées existent vraiment ;
- vérifie que les composants nécessaires sont indiqués dans l’Inspector.

Si les tests ne peuvent pas être exécutés, explique clairement ce qui n’a pas pu être testé.

---

## 5. Règles spéciales pour le code Unity/C#

Quand tu écris du code Unity/C# :
- donne toujours les fichiers complets ;
- ne donne jamais seulement quelques lignes à remplacer ;
- garde les noms de classes existants ;
- garde l’architecture existante autant que possible ;
- évite les changements énormes inutiles ;
- rends les scripts propres, robustes et faciles à comprendre ;
- utilise des champs visibles dans l’Inspector quand c’est utile ;
- ajoute des protections contre les références nulles ;
- évite de casser les autres systèmes du projet.

Ne supprime jamais plus de 100 lignes d’un fichier sans expliquer clairement pourquoi et sans proposer une alternative plus sûre.
