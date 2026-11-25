---
name: spaces
description: "Jira'daki tüm projeleri + Confluence space'leri listele, açık task sayısıyla birlikte. Triggers: spaces, jira spaces, jira projeleri, proje listesi, hangi projeler var."
argument-hint: "[jira | confluence | all]"
---

# /spaces — Jira & Confluence Space Listesi

## Akış

### Argüman `confluence` veya bos → Confluence space'leri
`mcp__atlassian__getConfluenceSpaces` ile tüm space'leri çek → tablo göster:

```
| Space        | Key  | Tür      |
|--------------|------|----------|
| Claude Config| CC   | global   |
| ...          | ...  | ...      |
```

### Argüman `jira` → Jira projeleri + açık task sayısı
1. `mcp__atlassian__getVisibleJiraProjects` ile tüm projeleri çek
2. Her proje için açık task sayısını al (JQL: `project = {KEY} AND status != Done`)
3. Tablo göster, açık task sayısına göre sırala (çok → az):

```
| Proje           | Key  | Açık | Son Task        |
|-----------------|------|------|-----------------|
| Vocab           | VOC  | 294  | VOC-294         |
| ApApp           | AC   | 123  | AC-123          |
| ...             | ...  | ...  | ...             |
```

### Argüman `all` → Her ikisi
Önce Jira, sonra Confluence göster.

## Kurallar
- Max 10 tool call
- Sıralama: açık task sayısı desc (Jira), isim asc (Confluence)
- 0 açık task'lı projeler en alta
