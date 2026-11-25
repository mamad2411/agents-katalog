---
name: sx-configuration
description: Use when the user needs to generate or validate Protheus data dictionary configuration scripts -- covering SX2 (table headers), SX3 (fields), SIX (indexes), SXG (field groups), SXA (form folders/tabs), SX1 (report questions), SX5 (generic tables), SXB (F3 lookup queries), and SX7 (triggers). Also triggers on Portuguese phrasing like "criar campo customizado", "cadastrar tabela customizada", "dicionario de dados", "criar indice SIX", "gatilho de campo", "tabela generica SX5", "consulta F3", or field-prefix names like ZA1/ZZ1.
---

# SX Configuration

This skill provides templates and validation rules for generating Protheus data dictionary configuration scripts: SX2 table headers, SX3 field definitions, SIX indexes, SXG field groups, SXA form folders/tabs, SX1 report parameter questions, SX5 generic tables, SXB standard F3 lookup queries, and SX7 field triggers. It covers required field values, naming conventions (3-char aliases, `Z`-prefixed custom tables, `XX_FIELD` naming), share-mode semantics (`C`/`E`/`M`), and common pitfalls such as creation order (SX2 before SX3 before SIX) and hardcoded physical table names.

Activate this skill when the user is registering a new custom table, adding custom fields, defining indexes, grouping fields for cross-table validation, organizing MVC form tabs, setting up report parameter questions, creating a generic lookup table, or configuring an F3 query or field trigger. It does not cover programmatic READ access to the dictionary at runtime (`Posicione`, `TamSx3`, FW APIs) -- see `protheus-reference/sx-dictionary.md` for that.

| Reference file | Read when |
|---|---|
| reference.md | Always -- SX2/SX3/SIX/SXG/SXA/SX1/SX5/SXB/SX7 field templates, share modes, naming rules, and common pitfalls |
