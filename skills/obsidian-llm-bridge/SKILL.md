---
name: obsidian-llm-bridge
description: WAJIB OTOMATIS dipakai tanpa slash saat user butuh baca/tulis/query Obsidian vault dari AI. Bridge via Local REST API (port 27123) + skill-graph-api (27125) + file langsung. Trigger: obsidian, vault, baca note, tulis note, query graph, dataview.
version: 1.0.0
tags: [obsidian, llm-bridge, rest-api, graph]
---

# Obsidian-LLM Bridge (wajib hubung)

Dua vault: mamatXobsidian (besar, 10090 skill stubs) + AgentsMemory
(ringan, LinkedIn + Memory + Daily).

## Cara akses (urutan)

1. File langsung (tercepat, tanpa server):
   cat ~/Documents/AgentsMemory/Memory/*.md
   cat ~/mamatXobsidian/05*/Skills/<nama>.md
2. skill-graph-api (port 27125, sudah jalan via launchd):
   curl localhost:27125/search?q=X
   curl localhost:27125/related?skill=X
   curl localhost:27125/load?skill=X
   curl localhost:27125/stats
3. Obsidian Local REST API (port 27123, butuh Obsidian TERBUKA
   + plugin rest-api ON + API key di data.json):
   curl -H "Authorization: Bearer KEY" localhost:27123/vault/FILE.md
   Kalau Obsidian tutup = DOWN, fallback ke cara 1-2.

## Sumber pengetahuan lokal (gratis, tanpa internet)

| API | Port | Isi |
|---|---|---|
| skill-graph-api | 27125 | 10.048 skill (/search /related /load) |
| repo-ref-api | 27126 | repo-refs 14K repo (/repos/search /repos/readme /repos/tree) |

Contoh:
  curl "localhost:27126/repos/search?q=fastapi"
  curl "localhost:27126/repos/readme?name=fastapi_fastapi"

repo-refs = README + struktur 14K repo GitHub terkurasi, ringan
(~10KB/repo, tanpa git). Dipakai kalau butuh contoh nyata library.

## Aturan hemat

Max baca 5 file. Response cap 2000 chars. Jangan load 10090 stubs
sekaligus. Dataview query sempit FROM folder, bukan full vault.
Plugin berat (excalidraw, git) default OFF via plugin.sh.
