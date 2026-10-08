---
inclusion: always
---

# Obsidian Skills — Auto-Active

Vault aktif: `~/mamatXobsidian`

## Skills yang Tersedia (auto-load via ~/.kiro/skills/)

Gunakan skill ini OTOMATIS tanpa diminta, kapanpun relevan:

| Skill | Kapan Dipakai |
|-------|---------------|
| `obsidian-markdown` | Saat buat/edit file .md di vault Obsidian |
| `obsidian-bases` | Saat kerja dengan file .base atau database view |
| `json-canvas` | Saat buat/edit file .canvas, mind map, diagram |
| `obsidian-cli` | Saat perlu baca/tulis/cari note via CLI |
| `obsidian-vault` | Saat kerja dengan Dataview, Tasks, Templater, vault management |
| `defuddle` | Saat user kasih URL untuk dibaca/dianalisis → SELALU pakai ini, bukan WebFetch |

## Auto-Wire Rules

1. **URL diberikan** → pakai `defuddle` skill dulu, bukan fetch biasa
2. **File .md di vault** → pakai `obsidian-markdown` syntax rules
3. **File .canvas** → pakai `json-canvas` format
4. **File .base** → pakai `obsidian-bases` format  
5. **Dataview query** → lihat `obsidian-vault` references/dataview.md
6. **Templater syntax** → lihat `obsidian-vault` references/templater.md
7. **Properties/frontmatter** → lihat `obsidian-vault` references/properties.md

## Vault Structure

```
~/mamatXobsidian/
├── 00 - Inbox/          ← capture cepat
├── 01 - Clippings/      ← web clips (Articles, YouTube, Twitter, Reddit)
├── 02 - Notes/          ← Fleeting, Literature, Permanent
├── 03 - Projects/
├── 04 - Areas/
├── 05 - Resources/      ← AI Tools, Tech, Traccia
├── 06 - Archives/
├── 07 - MOC/            ← Map of Content (index)
├── 08 - Daily/          ← daily + weekly notes
├── 09 - Templates/      ← Web Clip, Daily Note, Note, Weekly
└── Attachments/
```

## MCP skill-graph (Second Brain)

```json
{
  "mcpServers": {
    "skill-graph": {
      "command": "skill-graph",
      "env": { "SKILL_GRAPH_PATH": "~/mamatXobsidian" }
    }
  }
}
```

Tools: `skill_graph_index`, `skill_graph_scan`, `skill_graph_read`, `skill_graph_search`, `skill_graph_create`, `skill_graph_update`, `skill_graph_learn`

## Plugin Aktif (22 total)

**Scraping**: obsidian-slurp, auto-link-title, webpage-html-export  
**Data**: dataview, templater, quickadd, tasks, metadata-menu  
**Graph/MOC**: map-of-content, graph-analysis, juggl, strange-new-worlds  
**Skill Mgmt**: agentfiles, obsidian-skills-manager, obsidian-skill-graph  
**Utility**: tag-wrangler, outliner, calendar, periodic-notes, obsidian-git, style-settings, BRAT  
