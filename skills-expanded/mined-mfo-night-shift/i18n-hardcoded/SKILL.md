---
name: i18n-hardcoded
description: "Extract hardcoded French strings to i18n YAML. Use when user says 'extract i18n', 'translate hardcoded', or provides a .rb/.erb file with French text."
allowed-tools: Agent, Bash(git status:*), Bash(git add:*), Bash(git restore --staged:*), Bash(git commit:*), Bash(git diff:*), Bash(git log:*), Bash(grep:*), Bash(bundle exec rspec:*), Bash(bundle exec rubocop:*), Bash(bundle exec rake lint:apostrophe:fix), Bash(bin/rails runner:*), Bash(curl:*), Bash(echo:*), Bash(stat:*), Bash(touch:*), Bash(.claude/skills/screenshot-gist/create-gist.sh:*), Bash(bash .claude/skills/screenshot-gist/create-gist.sh:*), Bash(.claude/skills/screenshot-gist/push-gist.sh:*), Bash(bash .claude/skills/screenshot-gist/push-gist.sh:*), Bash(cp:*), Bash(ls:*), Edit(app/*), Edit(spec/*), Edit(config/*), Write(app/*), Write(spec/*), Write(config/*), Write(pr-description.md)
---

# Extraction i18n : textes francais hardcodes

**Contexte :** Extraire les textes francais en dur d'un fichier Ruby ou ERB vers les fichiers YAML i18n.

**Input :**
- Fichier a traiter : `$ARGUMENTS` (ex: `app/mailers/user_mailer.rb`)
- Scope : francais uniquement (v1)

**Regles Bash** : memes regles que haml-migration :
- Pas de `$()` (command substitution)
- Pas de `;` ou `&&` pour chainer
- Pas de pipes complexes
- 1 commande simple = 1 appel Bash
- Ne JAMAIS utiliser `git -C` — le working directory est deja le repo cible
- **INTERDIT** : `kill`, `pkill`, `lsof`, `bin/dev`, `overmind`, `env` — ne JAMAIS tenter de lancer, tuer ou diagnostiquer des processus
- **Permission refusee** : ne JAMAIS reessayer une commande refusee. Abandonner immediatement.

**Regle screenshots** : **TOUJOURS** deleguer les captures Playwright a l'agent `visual-verify`. Ne JAMAIS appeler les outils `mcp__playwright__*` directement — ils polluent le contexte avec du base64. Utiliser :
```
Agent(subagent_type: "visual-verify", prompt: "port: <PORT>, urls: ['/path'], selector: 'body', output_dir: 'tmp/<nom>/', prefix: 'before'")
```
Si l'agent retourne `{"status": "playwright_unavailable"}` → ecrire `pr-description.md` en notant "screenshots non disponibles" et terminer **sans commit**.

**Regle serveur** : le serveur est deja lance par nightshift. Verifier avec `curl -s -o /dev/null -w '%{http_code}' http://localhost:$PORT/` — si pas de reponse, **ARRETER** immediatement.

---

## Setup (avant le workflow)

**1. Serveur** — identifier le port : `grep '^PORT=' .env.development.local`. Le serveur tourne sur ce port. Si le fichier n'existe pas, utiliser 3000 par défaut. Utiliser `http://localhost:<PORT>/...` pour toutes les URLs.

**2. Auto-login** — verifier :
```bash
grep auto_sign_in_dev_user config/initializers/dev_auto_login.rb
```
Si absent → appliquer le skill `/dev-auto-login`. Ce skill ignore l'initializer via `.git/info/exclude` : il ne doit **jamais** modifier le `.gitignore` versionné, qui partirait dans le commit i18n.

**3. Playwright** — tester via visual-verify :
```
Agent(subagent_type: "visual-verify", prompt: "port: $PORT, urls: ['/'], selector: 'body', output_dir: 'tmp/test/', prefix: 'check'")
```
Si retour `playwright_unavailable` → noter et continuer sans screenshots. Sinon supprimer `tmp/test/`.

**5. Gist** — lancer le skill `/screenshot-gist <NomFichier>` pour creer le gist et cloner dans `tmp/<nom>/`.

---

## Workflow (1 fichier)

### Etape 1 : Analyse du fichier

1. **Lire le fichier** cible
2. **Identifier les textes francais hardcodes** :
   - Strings entre guillemets contenant du francais (`"Votre dossier..."`, `"Erreur"`, etc.)
   - Sujets d'emails (`subject = "..."`, `@subject = "..."`)
   - Labels, titres, messages flash, confirmations turbo
   - Attributs `data: { turbo_confirm: "..." }`
   - Prefixes/suffixes (`"Erreur : "`, `"Attention : "`)
3. **Exclure** :
   - Strings deja i18n (`t("...")`, `I18n.t(...)`)
   - Commentaires Ruby
   - Noms de fichiers, chemins, identifiants techniques
   - Strings uniquement ASCII sans mots francais
   - Constantes techniques (`"application/pdf"`, `"text/html"`)
4. **Si aucun texte hardcode trouve** : ecrire `pr-description.md` avec "Aucun texte hardcode trouve" et terminer **sans commit** — ne PAS faire `git add` ni `git commit`. Le pipeline detectera `no_diff` automatiquement.

### Etape 2 : Screenshot AVANT (preuve visuelle)

Capturer le rendu actuel AVANT toute modification.

**Trouver la page de preview :**

- **Mailer** (`app/mailers/`) : `localhost:$PORT/rails/mailers/<mailer_name>/<action>`
  - Exemple : `localhost:$PORT/rails/mailers/notification_mailer/send_accepte_notification`
  - Consulter `spec/mailers/previews/<mailer_name>_preview.rb` pour la liste des actions disponibles
  - Si le preview n'existe pas ou crash → skip le screenshot, documenter dans la PR

- **ViewComponent** (`app/components/`) : chercher dans cet ordre :
  1. Page reelle utilisant le composant (consulter `data/routes-reference.txt`)
  2. Preview ViewComponent : `localhost:$PORT/rails/view_components/<nom>/<variant>`
  3. Si aucun preview → skip le screenshot, documenter dans la PR

- **Vue ERB** (`app/views/`) : page reelle via `data/routes-reference.txt`

**Capturer via visual-verify** (jusqu'a 3 points d'entree) :

```
Agent(subagent_type: "visual-verify", prompt: "port: $PORT, urls: ['/rails/mailers/...', '/path2'], selector: 'body', output_dir: 'tmp/<nom>/', prefix: 'before'")
```

L'agent gere le viewport, la navigation et les captures. Il retourne la liste des fichiers crees (`before-1.png`, `before-2.png`, etc.).

### Etape 3 : Determiner la structure i18n cible

**Convention de l'app** (a respecter strictement) :

#### Pour les vues (`app/views/`)
- Fichier YAML FR : `config/locales/views/<controller>/<action>.fr.yml` (s'il existe deja) OU `config/locales/views/<controller>/fr.yml`
- Fichier YAML EN : meme chemin avec `.en.yml` au lieu de `.fr.yml`
- Scope : lazy lookup `.key` → resolu en `<controller>.<action>.<key>`
- Exemple :
  ```yaml
  # config/locales/views/users/dossiers/fr.yml
  fr:
    users:
      dossiers:
        show:
          submit_button: "Envoyer le dossier"
  ```
  ```yaml
  # config/locales/views/users/dossiers/en.yml
  en:
    users:
      dossiers:
        show:
          submit_button: "Submit the file"
  ```
  ```erb
  <%= t(".submit_button") %>
  ```

#### Pour les composants ViewComponent (`app/components/`)
- **Sidecars scindes par locale** (convention dominante du repo, ~160 composants) : **un fichier par locale**, a plat a cote du `.rb` :
  - FR : `app/components/<chemin>/<nom>_component.fr.yml` avec un bloc `fr:`
  - EN : `app/components/<chemin>/<nom>_component.en.yml` avec un bloc `en:`
- **NE JAMAIS** mettre `fr:` et `en:` dans un seul `<nom>_component.yml` — c'est l'ancienne forme, minoritaire, a ne pas reproduire.
- Scope : lazy lookup `.key` (ViewComponent resout automatiquement les deux fichiers)
- Exemple :
  ```yaml
  # app/components/dsfr/alert/alert_component.fr.yml
  fr:
    error_prefix: "Erreur : "
    info_prefix: "Information : "
  ```
  ```yaml
  # app/components/dsfr/alert/alert_component.en.yml
  en:
    error_prefix: "Error: "
    info_prefix: "Information: "
  ```
  ```ruby
  when :error then t(".error_prefix")
  ```

#### Pour les mailers (`app/mailers/`)
- Fichier YAML FR : `config/locales/views/<mailer_name>/<action>.fr.yml` OU le fichier existant le plus proche
- Fichier YAML EN : meme chemin avec `.en.yml`
- Sujets : utiliser `default_i18n_subject` quand possible, sinon `I18n.t("<mailer>.<action>.subject")`
- Corps : les textes dans les templates `.html.erb` / `.text.erb` associes suivent la convention views
- Exemple :
  ```yaml
  # config/locales/views/user_mailer/fr.yml
  fr:
    user_mailer:
      archive_available:
        subject: "Votre archive est disponible"
  ```
  ```yaml
  # config/locales/views/user_mailer/en.yml
  en:
    user_mailer:
      archive_available:
        subject: "Your archive is available"
  ```
  ```ruby
  # Avant
  @subject = "Votre archive est disponible"
  # Apres
  @subject = default_i18n_subject
  ```

#### Pour les controllers/services (`app/controllers/`, `app/services/`)
- Fichier YAML : le plus proche fichier `fr.yml` existant dans `config/locales/`
- Scope : chemin complet `I18n.t("controllers.<controller>.<action>.<key>")`

### Etape 4 : Verifier la structure YAML existante

**CRITIQUE** : avant d'ecrire, lire le fichier YAML cible s'il existe.

1. **Si le fichier YAML existe** : parser la structure, trouver le bon noeud d'insertion
2. **Si une cle identique existe avec la meme valeur** → skip (idempotent)
3. **Si une cle identique existe avec une valeur differente** → ne PAS ecraser, choisir un nom de cle different (suffixe `_v2` ou plus descriptif)
4. **Si le fichier YAML n'existe pas** : le creer avec la bonne structure

### Etape 4b : Chercher les traductions existantes reutilisables

**AVANT de creer une nouvelle cle**, verifier si une traduction equivalente existe deja dans le projet.

Pour chaque texte francais a extraire :

1. **Chercher la valeur exacte** dans les fichiers de traductions partages avec le tool Grep :
   - Pattern : `"Votre dossier"` dans les fichiers `config/locales/fr.yml`, `config/locales/en.yml`, `config/locales/shared.fr.yml`, `config/locales/shared.en.yml`

2. **Si une cle existante correspond** (meme valeur ou valeur equivalente) :
   - Reutiliser la cle existante avec son scope complet : `I18n.t("shared.dossier.votre_dossier")` au lieu de creer une nouvelle cle
   - Ne PAS dupliquer la traduction dans un nouveau fichier YAML

3. **Si aucune cle existante ne correspond** → creer la nouvelle cle normalement (Etape 5)

### Etape 5 : Extraction

Pour chaque texte hardcode identifie :

1. **Choisir un nom de cle** : court, descriptif, snake_case
   - `"Envoyer le dossier"` → `submit_dossier`
   - `"Erreur : "` → `error_prefix`
   - `"Votre archive est disponible"` → `archive_available` (ou `subject` si c'est un sujet mail)
2. **Ajouter la cle au YAML francais** (`fr.yml` ou section `fr:`) avec la valeur francaise
   - **Casse d'une valeur autonome** : si le texte extrait etait un fragment en milieu de phrase (commence par une minuscule apres un prefixe genre `"Source : "`, `"Origine : "`) mais devient une **valeur autonome** affichee dans un label / tag / badge / cellule, **mettre une majuscule initiale**. Verifier la casse des cles soeurs dans le meme fichier et rester coherent (ex: si `source: Annuaire des Entreprises` existe deja capitalise, alors `source: Référentiels géographiques nationaux`, pas `référentiels...`).
3. **Ajouter la cle au YAML anglais** (`en.yml` ou section `en:`) avec la traduction anglaise
   - Traduire le texte francais en anglais naturel (pas du mot-a-mot)
   - **Noms propres non traduits** : les noms de services, institutions, marques, produits, sigles restent **identiques** en FR et EN — ne PAS traduire. Ex: `Annuaire des Entreprises`, `Banque de France`, `INSEE`, `Infogreffe`, `URSSAF`, `FranceConnect`, `France Titres` gardent la meme valeur dans la section `en:`. En cas de doute sur le statut « nom propre » d'un texte, le laisser tel quel plutot que de le traduire (une traduction erronee d'un nom de service est pire qu'une non-traduction).
   - Appliquer la meme regle de casse qu'en FR (point 2) a la valeur anglaise autonome.
   - Conserver les interpolations `%{variable}` identiques
   - Pour les sidecar ViewComponent : ecrire dans le fichier scinde `<nom>_component.en.yml` (bloc `en:`), miroir de `<nom>_component.fr.yml` — jamais dans un `.yml` unique
4. **Valeur contenant du HTML → suffixe `_html` obligatoire** :
   - Si la valeur extraite contient des balises (`<strong>`, `<br>`, `<abbr>`, `<span class="fr-sr-only">`…), la cle DOIT se terminer par `_html` (ex: `libelles_description_html`). Sinon le helper echappe la valeur et l'usager voit `&lt;strong&gt;` a l'ecran.
   - Le suffixe s'applique aux DEUX locales ET a l'appel dans le code : `<%= t(".libelles_description_html") %>`.
   - Valable uniquement avec le helper de vue `t()` / `translate` (ERB, HAML, ViewComponent). `I18n.t` n'a PAS ce comportement : dans un service, un job ou un mailer hors template, ne pas mettre de HTML dans la valeur du tout.
   - Interpolation : le helper `translate` echappe automatiquement les valeurs interpolees dans une cle `_html` — `t(".x_html", libelle: user_input)` est sur.
   - Alternative preferable quand la balise enveloppe le segment ENTIER : garder la balise dans le template et la cle sans markup — `<strong><%= t(".x_label") %></strong>`. Le suffixe `_html` reste la regle des que le markup est en milieu de phrase.
5. **Remplacer dans le code** :
   - Vue ERB : `<%= t(".cle") %>`
   - Ruby (vue lazy) : `t(".cle")`
   - Ruby (scope explicite) : `I18n.t("scope.cle")`
   - Mailer subject : `default_i18n_subject` ou `I18n.t("mailer.action.subject")`
6. **Gerer l'interpolation** :
   - `"Dossier #{dossier.number}"` → cle `dossier_number: "Dossier %{number}"` + `t(".dossier_number", number: dossier.number)`
   - `"#{count} dossier(s)"` → cle avec `count:` pour pluralisation Rails
   - Interpolation complexe (HTML, helpers) → skip, ne pas extraire

### Etape 6 : Validation

**OBLIGATOIRE — ne JAMAIS skip**

1. **Verifier chaque cle i18n** : relire les YAML FR et EN et confirmer que CHAQUE `t(".cle")` insere dans le code a bien une entree correspondante dans les deux fichiers. Si une cle manque (FR ou EN) → **FAIL** (corriger avant de continuer).

2. **Linter apostrophes** :
   ```bash
   bundle exec rake lint:apostrophe:fix
   ```

3. **Tests** (si identifiables) :
   ```bash
   bundle exec rspec spec/path/to/relevant_spec.rb
   ```
   - Si un test echoue a cause du texte hardcode change (ex: `have_text("Envoyer")`) → fixer le test :
     - Remplacer `have_text("Envoyer")` par `have_text(I18n.t("scope.cle"))` ou par le nouveau texte
   - Si le test echoue pour une autre raison → investiguer, ne pas ignorer

4. **Rubocop** (sur les fichiers modifies uniquement) :
   ```bash
   bundle exec rubocop <fichier_modifie.rb>
   ```

### Etape 7 : Commit

```bash
git add <fichier_modifie>
git add <fichier_yaml_fr>
git add <fichier_yaml_en>
git add <specs_modifiees>  # si applicable
git commit -m "i18n(<scope>): extract hardcoded strings from <NomFichier>"
```

Un seul commit par fichier traite. Inclure le fichier source + YAML FR + YAML EN + specs modifiees — **et rien d'autre**.

Avant de committer, verifier qu'aucune modif hors scope n'est stagee :
```bash
git status --short
```
Ne jamais stager `.gitignore`, `bun.lock`, ni un fichier de setup dev. Si l'un d'eux est stage, le retirer avec `git restore --staged <fichier>`.

### Etape 8 : Screenshot APRES + comparaison

1. **Reprendre les memes pages** que l'etape 2 (memes URLs, meme ordre)
2. **Capturer via visual-verify** avec prefix `after` :
   ```
   Agent(subagent_type: "visual-verify", prompt: "port: $PORT, urls: ['/memes/urls'], selector: 'body', output_dir: 'tmp/<nom>/', prefix: 'after'")
   ```
3. **Comparer avant/apres** :
   - `stat -f%z` sur chaque paire before/after (1 appel Bash par fichier)
   - Identique au byte = le rendu n'a pas change (preuve forte)
   - Si difference : comparer visuellement avec `Read` sur les PNG
     - i18n ne devrait RIEN changer visuellement (meme texte, juste la source change)
     - Si regression visible → c'est un bug d'extraction (cle manquante, interpolation cassee) → **fixer**

4. **Si fix necessaire** :
   - Corriger le fichier source ou YAML
   - Relancer validation (etape 6)
   - Reprendre screenshot after
   - Commit le fix : `git commit -m "fix(i18n): fix extraction <NomFichier> — <description>"`

### Etape 9 : Push gist + pr-description.md

**1. Pousser les screenshots sur le gist** : lancer `push-gist.sh` avec tous les PNG de `tmp/<nom>/`.

**2. Ecrire `pr-description.md`** a la racine du worktree :

   Pour construire les URLs des images du gist :
   - Recuperer le gist ID depuis l'URL (derniere partie du path)
   - Format des URLs raw : `https://gist.githubusercontent.com/<user>/<gist-id>/raw/<filename>`

   **Template :**
   ```markdown
   ---
   title: "Tech: extraire les textes en dur de <NomFichier> vers i18n"
   ---

   # Probleme

   Textes francais en dur dans `<fichier>` — bloque l'internationalisation et l'accessibilite (les lecteurs d'ecran dependent des traductions structurees).

   # Solution

   Skill [`/i18n-hardcoded`](https://github.com/mfo/night-shift/blob/main/.claude/skills/i18n-hardcoded/SKILL.md)

   Extraction de N cles i18n vers `<fichier_yaml>`.

   ### Cles extraites

   | Cle | FR | EN |
   |-----|----|----|
   | `scope.cle1` | "Texte francais" | "English text" |
   | `scope.cle2` | "Autre texte" | "Other text" |

   ### Validation visuelle — RESULTAT

   **Avant :**
   ![before](https://gist.githubusercontent.com/<user>/<gist-id>/raw/before-1.png)

   **Apres :**
   ![after](https://gist.githubusercontent.com/<user>/<gist-id>/raw/after-1.png)

   **Couverture :**
   - ✅ `localhost:$PORT/rails/mailers/...` — preview mail
   - ⏭️ raison du skip (si applicable)

   [Voir tous les screenshots](https://gist.github.com/<user>/<gist-id>)

   ### Validation technique

   - [x] Chaque `t()` a sa cle YAML correspondante
   - [x] Apostrophes typographiques verifiees
   - [x] Tests passes
   - [x] Rubocop OK
   - [x] Screenshots avant/apres identiques

   Generated with [Claude Code](https://claude.com/claude-code)
   ```

**3. Fermer Playwright** : deleguer a visual-verify :
   ```
   Agent(subagent_type: "visual-verify", prompt: "close the browser")
   ```

---

## Regles critiques

1. **Jamais de "translation missing" en prod** : chaque `t()` DOIT avoir sa cle YAML. Verifier AVANT le commit.
2. **Respecter la structure existante** : ne pas creer une nouvelle hierarchie YAML si une existe deja. S'inserer dedans.
3. **Pas de duplication** : avant de creer une cle, chercher la valeur dans `config/locales/fr.yml`, `config/locales/shared.fr.yml`. Si une cle existante porte la meme traduction → reutiliser (cf. Etape 4b). Ne jamais dupliquer.
4. **1 fichier = 1 run** : traiter un seul fichier par execution. Ne pas elargir le scope.
5. **Toujours les deux locales, en fichiers scindes** : chaque cle extraite doit exister en FR et EN. Ne jamais creer un `fr.yml` sans son `en.yml` correspondant. Pour les sidecar ViewComponent : **deux fichiers** `<nom>_component.fr.yml` et `<nom>_component.en.yml` — jamais un seul `.yml` melangeant `fr:` et `en:`.
6. **Pas de texte technique** : ne pas extraire les constantes, chemins, formats techniques.
7. **Interpolation simple uniquement** : `#{variable}` → `%{variable}`. Si l'interpolation contient du HTML ou des helpers complexes → skip cette string.
8. **Noms propres non traduits** : services / institutions / marques / sigles (`Annuaire des Entreprises`, `Banque de France`, `INSEE`, `URSSAF`, `FranceConnect`…) restent identiques FR/EN. En cas de doute, ne pas traduire.
9. **Casse coherente** : une valeur autonome affichee comme label/tag/badge prend une majuscule initiale, meme si le fragment d'origine etait en minuscule au milieu d'une phrase. S'aligner sur la casse des cles soeurs du meme fichier.
10. **HTML dans la valeur → cle suffixee `_html`** : une valeur contenant des balises doit avoir une cle terminee par `_html`, dans les deux locales et dans l'appel `t()`. Sans le suffixe, le helper echappe le markup et l'usager voit `&lt;strong&gt;` au lieu du gras. Ne s'applique qu'au helper de vue `t()` — jamais a `I18n.t` (cf. Etape 5 point 4).
