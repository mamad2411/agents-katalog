# Règles minimales pour Cline — hexalyons-web

## Git
- Après chaque `git commit`, tenter immédiatement `git push` vers l'origin configuré.
- Si le push échoue (auth, réseau), ne pas bloquer : conserver localement + informer l'utilisateur à la fin.

## Conventions
- KISS / DRY / YAGNI (aligné sur hexalyons/doc/STANDARDS.md).
- Palette couleurs : synchronisée depuis `hexalyons/assets/scripts/config/palette.yaml` via `tools/sync_palette.py`.
- Termes FR/EN/ES officiels : voir `hexalyons/doc/brand_naming.md`.
- Multilingue par défaut (3 locales : en, fr, es).
