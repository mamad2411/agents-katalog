---
name: spl-tele-infisical-onboarding
description: Richtet den Zugriff auf die SPL-Tele-Infisical-Instanz (infisical.spl-tele.com) für einen neuen Kollegen ein — erkennt automatisch Windows oder Linux, prüft/installiert die Infisical-CLI, fragt Server-Adresse, Client-ID und Client-Secret der persönlichen Machine Identity ab, speichert sie systemweit als Umgebungsvariablen und verifiziert am Ende live, auf welche Secrets (nur Namen, keine Werte) tatsächlich Lesezugriff besteht. Trigger-Phrasen Deutsch und Englisch, Beispiele: Infisical einrichten, Infisical Zugang, Infisical CLI installieren, SPL Infisical onboarding, Machine Identity einrichten, Infisical Setup, Secrets-Zugriff einrichten, infisical.spl-tele.com, Infisical Client-ID, Infisical Client-Secret, Infisical Onboarding neuer Kollege, setup infisical, infisical login einrichten. Nutze diesen Skill immer wenn ein SPL-Tele-Kollege zum ersten Mal (oder nach Rechnerwechsel) Zugriff auf die firmeneigene Infisical-Instanz braucht.
---

# SPL-Tele Infisical Onboarding

## Zweck

Einmaliges, wiederholbares Setup, damit ein Kollege auf seinem eigenen Rechner
(Windows oder Linux) mit seiner **persönlichen Machine Identity** auf die
SPL-Tele-Infisical-Instanz zugreifen kann — ohne dass Secret-Werte jemals in
den Chat, in Dateien oder in den Modell-Kontext gelangen.

Dieser Skill ist eigenständig (kein Lumi-Bezug, siehe Rollentrennung) und für
Weitergabe an Kollegen gedacht: keine personenbezogenen Pfade, keine fest
codierten Credentials.

## Voraussetzung

Der Kollege muss von einem Infisical-Admin bereits eine eigene **Machine
Identity** (Universal Auth) mit Read-Zugriff auf die für ihn relevanten
Projekte erhalten haben — inkl. Client-ID und Client-Secret, die ihm auf
sicherem Weg (nicht per offenem Chat/E-Mail-Klartext, wenn vermeidbar)
übergeben wurden. Dieser Skill erzeugt keine Machine Identity, er richtet nur
den lokalen Zugriff damit ein.

## Ablauf (Claude führt dies aus, nicht nur beschreiben)

Alle Schritte werden von Claude direkt über Bash/PowerShell ausgeführt, nicht
nur als Copy-Paste-Vorschlag generiert — vorausgesetzt, das Tool hat
Ausführungsrechte auf dem Rechner des Kollegen.

### Schritt 0 — Bereits eingerichtet?

Zuerst prüfen, ob `SPL_INFISICAL_CLIENT_ID`, `SPL_INFISICAL_CLIENT_SECRET` und
`SPL_INFISICAL_DOMAIN` bereits gesetzt sind (Windows: `Get-ItemProperty
HKCU:\Environment`; Linux: `printenv` bzw. rc-Datei durchsuchen). Falls ja:
direkt zu Schritt 5 (Verifikation) springen, nicht neu abfragen.

### Schritt 1 — OS-Erkennung (automatisch, keine Rückfrage an den Nutzer)

```powershell
# Windows
$IsWindowsHost = $true
```
```bash
# Linux — via uname
uname -s   # "Linux" erwartet
```

### Schritt 2 — Infisical-CLI-Check

```powershell
# Windows
infisical --version
```
```bash
# Linux
infisical --version
```

Exit-Code 0 und eine Versionsnummer → weiter zu Schritt 3. Fehler
("command not found" / nicht erkannt) → CLI installieren.

### Schritt 3 — CLI-Installation falls nicht vorhanden

**Windows** (winget bevorzugt, da kein Admin-Passwort-Prompt nötig, wenn
winget bereits vorhanden ist):

```powershell
winget install Infisical.infisical
```

Falls winget fehlt, Fallback über npm (Node.js muss vorhanden sein):

```powershell
npm install -g @infisical/cli
```

**Linux** (Debian/Ubuntu — offizielles Repo):

```bash
curl -1sLf 'https://artifacts-cli.infisical.com/setup.deb.sh' | sudo -E bash
sudo apt-get update && sudo apt-get install -y infisical
```

Fallback für andere Distros oder falls kein `sudo`/apt verfügbar (Node.js
muss vorhanden sein):

```bash
npm install -g @infisical/cli
```

Nach Installation Schritt 2 wiederholen, um Erfolg zu bestätigen.

### Schritt 4 — Abfrage der drei Werte beim Kollegen

Der Reihe nach im Chat abfragen (normale Textfrage, kein Auswahl-Widget, da
Freitext nötig):

1. **Server-Adresse** — mit Vorschlag `http://infisical.spl-tele.com/api`
   fragen, Kollege bestätigt oder korrigiert (z. B. falls intern über
   `infisical.intern.spl-tele.com` erreichbar und DNS dort auflöst).
2. **Client-ID** der persönlichen Machine Identity.
3. **Client-Secret** der persönlichen Machine Identity.

Vor der Client-Secret-Frage kurz explizit ankündigen: *"Der Wert erscheint
danach einmalig im Chat, ich werde ihn aber in keiner Antwort wiederholen und
nirgends in Dateien schreiben."*

### Schritt 5 — Persistieren als Umgebungsvariable (systemweit, User-Scope)

**Windows** — Registry (User-Scope, überlebt Neustarts) + sofort nutzbar in
dieser Session:

```powershell
[Environment]::SetEnvironmentVariable("SPL_INFISICAL_CLIENT_ID", $clientId, "User")
[Environment]::SetEnvironmentVariable("SPL_INFISICAL_CLIENT_SECRET", $clientSecret, "User")
[Environment]::SetEnvironmentVariable("SPL_INFISICAL_DOMAIN", $domain, "User")
$env:SPL_INFISICAL_CLIENT_ID = $clientId
$env:SPL_INFISICAL_CLIENT_SECRET = $clientSecret
$env:SPL_INFISICAL_DOMAIN = $domain
```

Da ein frisch gestarteter PowerShell-Prozess die Registry-Änderung nicht
automatisch erbt: bei jedem weiteren Tool-Aufruf in derselben Session per
Registry-Fallback lesen, nicht aus `$env:` verlassen:

```powershell
$r = Get-ItemProperty HKCU:\Environment
$clientId = $r.SPL_INFISICAL_CLIENT_ID
$clientSecret = $r.SPL_INFISICAL_CLIENT_SECRET
$domain = $r.SPL_INFISICAL_DOMAIN
```

**Linux** — Idempotent in die Shell-rc-Datei eintragen (bash oder zsh, je
nach `$SHELL`), nur anhängen wenn noch nicht vorhanden, plus sofort in der
aktuellen Session exportieren:

```bash
RC_FILE="$HOME/.bashrc"
[ "$(basename "$SHELL")" = "zsh" ] && RC_FILE="$HOME/.zshrc"

grep -q "SPL_INFISICAL_CLIENT_ID" "$RC_FILE" 2>/dev/null || cat >> "$RC_FILE" <<EOF
export SPL_INFISICAL_CLIENT_ID="$CLIENT_ID"
export SPL_INFISICAL_CLIENT_SECRET="$CLIENT_SECRET"
export SPL_INFISICAL_DOMAIN="$DOMAIN"
EOF

export SPL_INFISICAL_CLIENT_ID="$CLIENT_ID"
export SPL_INFISICAL_CLIENT_SECRET="$CLIENT_SECRET"
export SPL_INFISICAL_DOMAIN="$DOMAIN"
```

### Schritt 6 — Verifikation (Login + Secret-Namen lesen, niemals Werte)

```powershell
$token = infisical login --method=universal-auth --client-id=$clientId --client-secret=$clientSecret --domain=$domain --plain --silent
$headers = @{ Authorization = "Bearer $token" }
$workspaces = (Invoke-RestMethod -Uri "$domain/v1/workspace" -Headers $headers -Method GET).workspaces
foreach ($ws in $workspaces) {
  $details = Invoke-RestMethod -Uri "$domain/v1/workspace/$($ws.id)" -Headers $headers -Method GET
  foreach ($e in $details.workspace.environments) {
    $secretsResp = Invoke-RestMethod -Uri "$domain/v3/secrets/raw?workspaceId=$($ws.id)&environment=$($e.slug)" -Headers $headers -Method GET
    $names = $secretsResp.secrets | Select-Object -ExpandProperty secretKey
    # nur $names ausgeben (Secret-Namen), niemals $secretsResp.secrets.secretValue
  }
}
```

Analoges Vorgehen unter Linux via `curl` + `jq`, wobei `jq` **ausschließlich**
`.secretKey` extrahiert:

```bash
TOKEN=$(infisical login --method=universal-auth --client-id="$CLIENT_ID" --client-secret="$CLIENT_SECRET" --domain="$DOMAIN" --plain --silent)
curl -s -H "Authorization: Bearer $TOKEN" "$DOMAIN/v1/workspace" | jq -r '.workspaces[] | "\(.name) \(.id)"'
# je Workspace/Environment:
curl -s -H "Authorization: Bearer $TOKEN" "$DOMAIN/v3/secrets/raw?workspaceId=<ID>&environment=<ENV>" | jq -r '.secrets[].secretKey'
```

Ergebnis dem Kollegen als Tabelle zeigen: Projekt | Environment | Secret-Namen
(oder "keine Secrets" / "kein Zugriff" bei 403).

## Sicherheitsprinzipien (nicht verhandelbar)

- **Secret-Werte verlassen die Shell nie.** In den Modell-Kontext/Chat gelangen
  nur Ergebnisse (Secret-**Namen**, Anzahl, HTTP-Status) — niemals
  `secretValue`.
- **Keine Rückfrage nach bereits gesetzten Werten.** Schritt 0 zuerst prüfen.
- **Keine fremde Machine Identity verwenden.** Jeder Kollege nutzt
  ausschließlich seine eigene Client-ID/Secret — niemals die eines anderen
  Kollegen oder Credentials aus einem anderen Unternehmenskontext übernehmen
  (strikte Rollentrennung).
- **Keine Schreib-/Lösch-/Rotations-Operation.** Dieser Skill liest nur.
- Bei 401 (Login fehlgeschlagen): Client-ID/Secret erneut abfragen, nicht
  raten oder wiederholt automatisch retryen.
- Bei DNS-Fehler auf die Server-Adresse: Hinweis auf VPN/internes Netz geben,
  nicht stillschweigend eine andere Adresse raten.

## Fehlerbehandlung

| Symptom | Wahrscheinliche Ursache | Vorgehen |
|---|---|---|
| `infisical: command not found` nach Installation | PATH nicht aktualisiert | Neue Shell-Session starten, dann Schritt 2 wiederholen |
| DNS-Fehler bei Server-Adresse | Interner Host, kein VPN aktiv | Kollege nach VPN-Status fragen, alternative öffentliche Adresse `infisical.spl-tele.com` vorschlagen |
| `please provide client-id flag` trotz gesetzter Werte | Frischer Shell-Prozess hat Registry-Änderung (Windows) noch nicht geerbt | Registry-Fallback aus Schritt 5 nutzen |
| Login HTTP 401 | Client-ID/Secret falsch oder Identity deaktiviert | Werte erneut abfragen; bei wiederholtem Fehlschlag Admin kontaktieren |
| Workspace-Liste leer | Machine Identity ohne zugewiesene Projekte | Admin kontaktieren, keine Berechtigungen selbst ändern |
| 403 bei einzelnen Projekten | Identity hat dort keinen Zugriff — normal, kein Fehler | Als "kein Zugriff" in der Ergebnistabelle vermerken, nicht als Fehler behandeln |

## Verteilung an Kollegen

Empfehlung: Diesen Ordner (`spl-tele-infisical-onboarding/`) in ein
gemeinsames, versioniertes Repo legen (analog zum bestehenden
`claude-workstation-sync`-Muster), Kollegen clonen/pullen es und kopieren den
Ordner nach `~/.claude/skills/`. Eine "Upload"-Funktion für einzelne Skills
gibt es in Claude Code/Desktop nicht — Skills sind Dateien, keine
hochladbaren Artefakte über die UI.

## Versionierung dieses Skills

- **v1.0.0** (2026-07-14) — Initiale Version. Erstellt nach erfolgreichem
  Live-Onboarding der Machine Identity `Claude-Readonly` für Dimitri Rupp auf
  `infisical.spl-tele.com` (Windows). Deckt Windows + Linux, automatische
  OS-/CLI-Erkennung, Registry- bzw. rc-Datei-Persistenz und
  Namen-only-Verifikation ab.
