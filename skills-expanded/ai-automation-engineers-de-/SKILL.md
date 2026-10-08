# Cursor Rules für Git Commits - Conventional Commits Standard

## Git Commit Message Standards

### Befolge die Conventional Commits Spezifikation v1.0.0

Alle Git Commit Messages müssen dem folgenden Format folgen:
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Commit Types:
- **feat**: Neue Funktion für den User (entspricht MINOR in SemVer)
- **fix**: Bug-Fix (entspricht PATCH in SemVer)
- **docs**: Dokumentationsänderungen
- **style**: Code-Formatierung, Leerzeichen, etc. (keine Logikänderungen)
- **refactor**: Code-Refactoring ohne neue Features oder Bug-Fixes
- **test**: Hinzufügen oder Ändern von Tests
- **chore**: Build-Prozess, Hilfswerkzeuge, Dependencies
- **ci**: CI/CD Konfigurationsänderungen
- **perf**: Performance-Verbesserungen
- **build**: Änderungen am Build-System
- **revert**: Rückgängigmachung eines Commits

### Breaking Changes:
- Verwende `!` nach dem Type/Scope für Breaking Changes: `feat!:` oder `feat(api)!:`
- Oder füge `BREAKING CHANGE:` im Footer hinzu

### Scope (optional):
- Beschreibt den Bereich der Änderung: `feat(auth):`, `fix(api):`, `docs(readme):`
- Verwende Klammern um den Scope

### Description:
- Kurze Beschreibung in Imperativ (max 50 Zeichen)
- Kleinbuchstaben, kein Punkt am Ende
- Deutsch oder Englisch konsistent verwenden

### Body (optional):
- Detaillierte Erklärung der Änderungen
- Verwende Imperativ-Form
- Erkläre das "Was" und "Warum", nicht das "Wie"

### Footer (optional):
- Breaking Changes: `BREAKING CHANGE: description`
- Issue-Referenzen: `Fixes #123`, `Closes #456`
- Reviewed-by, Refs, etc.

### Beispiele:
```
feat(auth): add OAuth2 login support

fix: resolve memory leak in profile component

docs: update API documentation for new endpoints

feat!: remove deprecated user API

BREAKING CHANGE: The old user API endpoints have been removed
```

### Regeln:
1. Verwende Präsens ("add" nicht "added")
2. Keine Großbuchstaben am Anfang der Description
3. Kein Punkt am Ende der Description
4. Breaking Changes klar markieren
5. Scope sollte ein Noun sein, das einen Codebereich beschreibt
6. Body und Footer sind optional, aber bei komplexen Changes empfohlen

### Automatische Tools:
- Commitlint wird verwendet zur Validierung
- Semantic Release für automatische Versionierung
- Changelog-Generierung basiert auf Commit Types