---
name: update-architect-pack
description: Holt die neueste Version des Claude Architect Pack aus dem GitHub-Repo und aktualisiert die installierten Files. Respektiert User-Overrides (CLAUDE.user.md, _user-overrides/). Aktivieren bei "update architect pack", "neue Version holen", "pack aktualisieren", "architect-pack updaten".
---

# Update-Architect-Pack — Updater-Skill

Holt die neueste Version des Claude Architect Pack aus dem GitHub-Repo
und aktualisiert installierte Files. **Niemals** werden User-Overrides
(`CLAUDE.user.md`, `_user-overrides/`, Memory) angefasst.

## Wann aktivieren

- "update architect pack" / "pack aktualisieren"
- "neue Version holen" / "architect-pack updaten"
- Periodisch (z.B. einmal pro Woche)
- Nach einem Hinweis "es gibt eine neue Pack-Version"

## Voraussetzungen

- `~/claude-architect-pack/` vorhanden (sonst zuerst `init-architect-pack` ausfuehren)
- `~/claude-architect-pack/.install-config.json` vorhanden (von Initial-Install gepflegt)

## Step-by-Step

### 1. Pre-Flight

```bash
[ -d ~/claude-architect-pack ] || { echo "Pack nicht installiert. Erst /init-architect-pack ausfuehren."; exit 1; }
[ -f ~/claude-architect-pack/.install-config.json ] || { echo ".install-config.json fehlt — Re-Init noetig."; exit 1; }

cat ~/claude-architect-pack/.install-config.json
```

Daraus: Workspace-Pfad, Skill-Pfad (global/lokal).

### 2. Aktuellen Stand sichern (vor Update)

```bash
cd ~/claude-architect-pack
git fetch origin
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)
if [ "$LOCAL" = "$REMOTE" ]; then
  echo "Pack ist bereits aktuell ($LOCAL)."
  exit 0
fi
echo "Update verfuegbar: $LOCAL -> $REMOTE"
git log --oneline $LOCAL..$REMOTE
```

### 3. Repo updaten

```bash
cd ~/claude-architect-pack
git pull origin main
```

### 4. MANIFEST.yml laden

```bash
cat ~/claude-architect-pack/MANIFEST.yml
```

Daraus 2 Listen:
- `template_managed`: diese Files werden aus dem Pack ueberschrieben
- `user_owned`: diese Files werden NIE angefasst

### 5. Workspace-Files aktualisieren

Pro File in `template_managed`:
```bash
WS="$(jq -r '.workspace_path' ~/claude-architect-pack/.install-config.json)"
SRC="$HOME/claude-architect-pack/workspace-template/<file>"
DST="$WS/<file>"

# Backup vor Ueberschreiben (.bak)
[ -f "$DST" ] && cp "$DST" "$DST.bak.$(date +%Y%m%d-%H%M%S)"
cp "$SRC" "$DST"
```

Pro File in `user_owned`: **nichts tun**, nicht anfassen.

### 6. Skills updaten

```bash
SKILLS_DIR="$(jq -r '.skills_dir' ~/claude-architect-pack/.install-config.json)"

for skill in autonomous-execution audit-creator audit-worker cleanup-after-welle project-setup bootstrapNewProject generateProjectDataMap heartbeatWorkspace init-architect-pack update-architect-pack; do
  cp -r "$HOME/claude-architect-pack/.claude/skills/$skill" "$SKILLS_DIR/"
done
```

### 7. Diff-Bericht

Pro veraenderter Datei: 1 Zeile im Bericht.

```bash
git -C ~/claude-architect-pack log --oneline $LOCAL..$REMOTE --no-merges | head -10
```

### 8. Cleanup (optional)

Files unter `deprecated_remove` aus MANIFEST.yml: User fragen ob sie geloescht werden sollen.

### 9. Verifikation

```bash
ls "$WS/CLAUDE.md" "$WS/_runbooks/INDEX.md"
[ -f "$WS/CLAUDE.user.md" ] && echo "CLAUDE.user.md erhalten" || echo "FEHLT — Problem!"
ls -la "$SKILLS_DIR/audit-creator/SKILL.md"
```

### 10. Erfolgs-Bericht im Chat

```
Architect Pack aktualisiert.
- Vorher: <commit-sha>
- Nachher: <commit-sha>
- Commits: <N> neue Commits
- Files updated: <N>
- User-Overrides erhalten: PASS (CLAUDE.user.md, _user-overrides/, Memory)
- Backups in: <pfad>/*.bak.YYYYMMDD-HHMMSS
- Naechster Schritt: Falls Probleme -> manuell rollback ueber .bak Files
```

## User-Override-Sicherheit

Diese Files / Verzeichnisse werden **niemals** ueberschrieben:
- `<workspace>/CLAUDE.user.md`
- `<workspace>/_user-overrides/**`
- `<workspace>/Projekte/**`
- `<workspace>/projects/**`
- `<workspace>/_runbooks/custom-*.md`
- `<workspace>/_runbooks/local-*.md`
- `<workspace>/_control/credentials-map.md`
- `<workspace>/_control/server-config.md`
- `<workspace>/_control/projects/**`
- `~/.claude/projects/**/memory/**`

Wenn der User einen dieser Pfade manuell veraendert hat, bleibt seine Aenderung.

## Rollback bei Problemen

Bei jedem Update werden `.bak`-Dateien geschrieben. Rollback:

```bash
WS="<workspace-pfad>"
find "$WS" -name "*.bak.*" -type f | sort | tail -5  # neueste Backups
# Pro File:
cp "$WS/CLAUDE.md.bak.20260511-120000" "$WS/CLAUDE.md"
```

## Was NICHT passiert

- Kein Hard-Delete
- Kein Force-Sync (User-Overrides immer respektieren)
- Kein automatischer Run gegen neue Major-Versions ohne User-Bestaetigung

## Verifizieren

- [ ] `git log` im Pack-Repo zeigt neue Commits
- [ ] Template-Files im Workspace haben neue Mtime
- [ ] User-Override-Files haben unveraendert (Mtime gleich, Content gleich)
- [ ] Backups vorhanden falls Rollback noetig
- [ ] Bericht im Chat gepostet
