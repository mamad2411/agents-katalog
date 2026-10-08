# Git commit messages (bouton ✨ Generate Commit Message)

Respecter **strictement** ces règles Conventional Commits.

## Format obligatoire

```
type(scope): description
```

- **Langue** : anglais uniquement (sujet et corps).
- **Sujet** : impératif, minuscule après `:`, **sans point final**, ≤ 72 caractères.
- **Types autorisés** (uniquement) : `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.

## Scope

Si un scope est présent, il **doit** être exactement l'un de :

`src` · `tests` · `s3` · `deps` · `ci` · `root`

Mapper les chemins modifiés :

| Fichiers touchés | Scope |
|------------------|-------|
| `src/` | `src` |
| `tests/` | `tests` |
| `packages/nestjs_module_factorydrive-s3/` | `s3` |
| `package.json`, `yarn.lock` (dépendances) | `deps` |
| `.github/` | `ci` |
| `README.md`, `docs/`, règles IA, config racine | `root` |

Toujours inclure un scope valide quand un périmètre domine. L'omettre seulement si le changement est réellement transversal.

## Breaking changes

- Sujet : `feat(src)!: remove legacy disk token`
- Ou pied : `BREAKING CHANGE: …`

## Exemples valides

```
feat(src): add custom driver registration helper
fix(src): guard missing default disk in StorageManager
feat(s3): support SSE-KMS on putObject
docs(root): document forRootAsync configuration in README
build(deps): bump fs-extra to 11.3.4
chore(root): add conventional commit rules for AI assistants
```

## Anti-exemples

```
❌ feat(storage): add S3 driver          → scope invalide
❌ Add factorydrive module support        → pas de type/scope
❌ feat(src): fix signed url.             → point final interdit
```
