# SKILL FLOW — alur kerja WAJIB semua AI

> Dibuat otomatis dari `~/.agents/skill-flow.json` (edit di sana, lalu `python3 ~/.agents/skill-flow.py --render`).

## Selalu

- `caveman-token-optimizer`, `verification-loop`

## Alur (urut, jangan dilompati)

1. PAHAMI: rapikan maksud user (prompt-booster). Ambigu & berisiko → tanya 1 pertanyaan; selain itu asumsi wajar + sebutkan.
2. PILIH SKILL: cocokkan kategori di bawah + skill_for_task. Muat maks 3-4 skill paling relevan (bukan semua).
3. RUJUK SUMBER: baca file asli sebelum mengubah; library/API → dokumen resmi terbaru (documentation-lookup/context7); fakta → web + sumber. Dilarang mengarang angka/API.
4. RENCANA: tugas >3 langkah → rencana singkat dulu (create-implementation-plan).
5. EKSEKUSI: perubahan kecil & terarah, ikuti gaya kode sekitar, jangan melebar dari permintaan.
6. VERIFIKASI: jalankan test/build/lint atau cek hasil nyata (verification-loop). Gagal → perbaiki akar masalah, bukan tambal.
7. POLES: UI → anti-ui-slop + de-sloppify; tulisan → avoid-ai-writing + content-humanizer.
8. LAPOR: ringkas, jujur (yang gagal/dilewati disebut), sertakan sumber untuk klaim.

## Kategori → skill

| Kategori | Pemicu (contoh) | Skill |
|---|---|---|
| rencana | rencana, plan, planning, arsitektur, architecture, desain sistem | `create-implementation-plan`, `brainstorming`, `spec`, `prd` |
| kode | kode, code, coding, fitur, feature, implement | `search-first`, `documentation-lookup`, `coding-standards` |
| frontend | ui, ux, frontend, tampilan, halaman, page | `frontend-design`, `anti-ui-slop`, `de-sloppify`, `responsive-design`, `accessibility` |
| react-next | react, next, nextjs, next.js, jsx, tsx | `react-patterns`, `nextjs-app-router-patterns` |
| vue | vue, nuxt, pinia | `vue-best-practices` |
| mobile | mobile, android, ios, react native, flutter, aplikasi hp | `mobile-design`, `react-native-patterns` |
| backend-api | backend, api, endpoint, rest, graphql, server | `api-design-principles`, `backend-patterns`, `error-handling` |
| database | database, db, sql, postgres, postgresql, mysql | `database-schema-design`, `sql-optimization` |
| python | python, django, fastapi, flask, pandas | `python-patterns` |
| go | golang, go | `golang-patterns` |
| typescript | typescript, ts, node, nodejs, javascript, js | `typescript-security-review` |
| debug | error, bug, crash, gagal, rusak, fix | `systematic-debugging`, `error-handling`, `logging-best-practices` |
| test | test, testing, tes, unit test, e2e, tdd | `tdd-workflow`, `writing-tests` |
| review | review, cek kode, audit kode, code review, pr, pull request | `code-review`, `adversarial-reviewer`, `pr-review` |
| refactor | refactor, rapikan kode, clean up, bersihkan kode, simplify, sederhanakan | `refactor`, `review-and-refactor` |
| keamanan | security, keamanan, aman, vulnerability, celah, secret | `security-review`, `secrets-scanner`, `dependency-audit` |
| performa | lambat, lemot, slow, performa, performance, optimasi | `performance-optimization` |
| devops | docker, deploy, deployment, ci, cd, github actions | `docker-best-practices`, `ci-cd`, `deployment-checklist-generator` |
| git | git, commit, branch, merge, rebase, push | `git-commit` |
| dokumentasi | readme, docs, dokumentasi, documentation, panduan, guide | `documentation-writer`, `readme-generator`, `avoid-ai-writing` |
| tulisan | tulis, tulisan, artikel, article, blog, essay | `avoid-ai-writing`, `content-humanizer`, `copy-editing`, `brand-voice` |
| marketing | marketing, iklan, ads, jualan, sales, landing copy | `copywriting`, `seo-audit`, `brand-voice` |
| sosmed | linkedin, instagram, twitter, tiktok, postingan, post | `linkedin-post-formatter`, `social-content`, `content-humanizer` |
| email | email, surat, balas email, reply, pesan formal | `email-drafter`, `avoid-ai-writing` |
| riset | riset, research, cari info, fakta, sumber, berita | `deep-research`, `doublecheck`, `web-search`, `literature-review` |
| data | data, analisis, analisa, analysis, statistik, chart | `data-analysis`, `data-visualization`, `doublecheck` |
| file-office | pptx, powerpoint, slide, presentasi, docx, word | `pptx`, `docx`, `pdf`, `xlsx` |
| gambar-video | gambar, image, foto, poster, logo, ilustrasi | `image-generation`, `ai-video-generation` |
| baca-file | screenshot, ocr, baca gambar, scan, lampiran | `baca-gambar` |
| prompt-ai | prompt, llm, agent, ai agent, chatbot, mcp | `prompt-engineering`, `mcp-builder`, `skill-creator` |
| memori | ingat, simpan, catat, lupa, memori, memory | `linkedin-obsidian-memory-graph`, `obsidian-automation`, `obsidian-llm-bridge` |
| perangkat | panas, ngelag, kipas, ram, cpu, bersih | `device-cool` |
| browser | buka web, cek situs, baca halaman, browser, otomasi web, scrape | `browser-use-local` |
| meeting | meeting, rapat, notulen, minutes | `meeting-notes` |
| konteks | context penuh, token habis, hemat token, compact, kepanjangan | `context-budget`, `strategic-compact` |

## Cara memuat skill

- MCP `skill-catalog`: `skill_for_task("<tugas>")` → `skill_load("<nama>")`.
- Tanpa MCP: `~/.agents/skill-search.sh "<kata kunci>"` lalu baca `~/.agents/skills-store/<nama>/SKILL.md`.
- Muat hanya skill yang cocok (maks ±7). Tugas campuran → gabungkan kategori.

## Sumber

- `~/.agents/skill-flow.json`
- `~/.agents/skills-store/<nama>/SKILL.md`
