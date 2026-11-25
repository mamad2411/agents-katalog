# 🔧 Istruzioni Setup MCP - BHM v.2

**Data**: 2026-01-07  
**Progetto Supabase**: `hjteuounjwkadmsbsmdm`

---

## 📋 STEP 1: Crea il file mcp.json

Il file `.cursor/mcp.json` è ignorato da git per sicurezza. Devi crearlo manualmente:

### Windows (PowerShell)
```powershell
# Copia il template
Copy-Item .cursor\mcp.json.template .cursor\mcp.json
```

### Oppure manualmente
1. Copia il file `.cursor/mcp.json.template`
2. Rinominalo in `.cursor/mcp.json`

---

## 🔑 STEP 2: Ottieni i Token Necessari

### Supabase Personal Access Token
1. Vai su: https://supabase.com/dashboard/account/tokens
2. Clicca **"Generate new token"**
3. Nome suggerito: `Cursor MCP - BHM v.2`
4. Copia il token (inizia con `sbp_...`)

### GitHub Personal Access Token
1. Vai su: https://github.com/settings/tokens
2. Clicca **"Generate new token (classic)"**
3. Seleziona permessi:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `read:org` (Read org and team membership)
   - ✅ `read:user` (Read user profile data)
4. Imposta scadenza: 90 giorni (raccomandato)
5. Copia il token (inizia con `ghp_...`)

---

## ✏️ STEP 3: Configura i Token

Apri `.cursor/mcp.json` e sostituisci:

```json
{
  "mcpServers": {
    "supabase": {
      "env": {
        "SUPABASE_ACCESS_TOKEN": "sbp_TUO_TOKEN_QUI"  // ⬅️ SOSTITUISCI
      }
    },
    "github": {
      "env": {
        "GITHUB_TOKEN": "ghp_TUO_TOKEN_QUI"  // ⬅️ SOSTITUISCI
      }
    }
  }
}
```

---

## 🔄 STEP 4: Riavvia Cursor

1. Salva il file `.cursor/mcp.json`
2. Chiudi completamente Cursor
3. Riapri Cursor
4. Attendi 10-15 secondi per il caricamento MCP

---

## ✅ STEP 5: Verifica Configurazione

### Metodo 1: Settings UI
1. Apri **Settings** (Ctrl+,)
2. Vai su **MCP**
3. Dovresti vedere tutti i server con stato **verde** (🟢):
   - ✅ supabase
   - ✅ playwright
   - ✅ github
   - ✅ filesystem

### Metodo 2: Test Query
Prova a chiedere a Cursor:
```
"Lista le tabelle del mio database Supabase"
```

Se vedi le tabelle (booking_requests, admin_users, etc.), la configurazione funziona! 🎉

---

## 🔧 MCP Configurati

| MCP Server | Funzionalità | Comando |
|------------|-------------|---------|
| **Supabase** | Database queries, migrazioni, Edge Functions | `@supabase/mcp-server-supabase` |
| **Playwright** | Browser automation, E2E testing | `@playwright/mcp` |
| **GitHub** | Repository management, issues, PRs | `@modelcontextprotocol/server-github` |
| **Filesystem** | File operations nel progetto | `@modelcontextprotocol/server-filesystem` |

---

## 🛡️ Note Sicurezza

### ✅ Best Practices
- **Read-only mode** abilitato per Supabase (previene modifiche accidentali)
- **Project-scoped** limitato a `tucqgcfrlzmwyfadiodo`
- **Token privati** mai committati su git
- **Filesystem** limitato alla directory BHM-v.2

### ⚠️ Attenzioni
- **NON** usare `SUPABASE_ANON_KEY` per MCP (usa PAT)
- **NON** committare `.cursor/mcp.json` su git
- **Rinnova** token GitHub ogni 90 giorni
- **Usa** PAT diversi per prod/dev se necessario

---

## 🚨 Troubleshooting

### MCP non si connette
```powershell
# Verifica che npx sia disponibile
npx --version

# Verifica Node.js
node --version

# Dovrebbe essere >= 18
```

### Supabase MCP fallisce
- ✅ Verifica PAT valido su https://supabase.com/dashboard/account/tokens
- ✅ Controlla che project-ref sia corretto: `tucqgcfrlzmwyfadiodo`
- ✅ Riavvia Cursor dopo modifiche

### GitHub MCP fallisce
- ✅ Verifica token con permessi corretti
- ✅ Controlla rate limit: https://api.github.com/rate_limit
- ✅ Token non scaduto

### Playwright MCP fallisce
```powershell
# Installa browsers Playwright
npx playwright install chromium
```

### Filesystem MCP fallisce
- ✅ Verifica path: `C:\Users\matte.MIO\Documents\GitHub\BHM-v.2`
- ✅ Controlla permessi directory
- ✅ Path usa doppi backslash `\\`

---

## 📊 Testing

### Test Supabase MCP
Chiedi a Cursor:
```
"Mostrami lo schema della tabella booking_requests"
```

### Test Playwright MCP
Chiedi a Cursor:
```
"Apri la pagina localhost:3000 e fai uno screenshot"
```

### Test GitHub MCP
Chiedi a Cursor:
```
"Mostrami gli ultimi 5 commit del repository"
```

### Test Filesystem MCP
Chiedi a Cursor:
```
"Leggi il contenuto di package.json"
```

---

## 🔄 Manutenzione

### Aggiornamento MCP
I server MCP si aggiornano automaticamente con `@latest`, ma puoi forzare:
```powershell
npx -y @supabase/mcp-server-supabase@latest
```

### Rotazione Token
- **GitHub**: Ogni 90 giorni
- **Supabase**: Quando necessario (nessuna scadenza automatica)

### Backup Configurazione
Salva `.cursor/mcp.json` in un password manager sicuro

---

## 📚 Risorse

- **Supabase MCP Docs**: https://supabase.com/docs/guides/getting-started/mcp
- **MCP Protocol**: https://modelcontextprotocol.io/
- **Supabase PAT**: https://supabase.com/dashboard/account/tokens
- **GitHub Tokens**: https://github.com/settings/tokens
- **Playwright MCP**: https://playwright.dev/

---

**✅ Setup completato con successo quando tutti i server MCP mostrano stato verde!**





