# Modul 1: Apa Itu Skill?

## Definisi
Skill adalah paket modular dan self-contained yang memperluas kemampuan AI agent (seperti Cursor, Claude Code, Windsurf, atau OpenClaw) dengan memberikan pengetahuan khusus, workflow, dan tools. Skill mengubah agent dari general-purpose menjadi spesialis di domain tertentu.

## Analogi
Bayangkan kamu baru hire karyawan baru yang sangat pintar tapi belum tahu SOP kantormu. Skill adalah **buku panduan** yang kamu kasih ke dia di hari pertama. Tanpa skill, dia bisa kerja tapi lambat dan banyak tanya. Dengan skill, dia langsung produktif.

## Apa yang Skill Berikan?
1. **Specialized Workflows**: Prosedur multi-langkah untuk domain spesifik (misal: cara deploy ke AWS).
2. **Tool Integrations**: Instruksi untuk bekerja dengan format file atau API tertentu.
3. **Domain Expertise**: Pengetahuan spesifik perusahaan/proyek (skema database, business logic).
4. **Bundled Resources**: Script, referensi, dan aset untuk tugas yang kompleks dan berulang.

## Skill vs Plugin vs Extension
| Aspek | Skill | Plugin/Extension |
| :--- | :--- | :--- |
| Target | AI Agent | Software/IDE |
| Format | Markdown + Script | Binary/Package |
| Instalasi | Copy folder | Package manager |
| Eksekusi | Agent membaca & menjalankan | Runtime auto-load |
| Fleksibilitas | Sangat tinggi (natural language) | Terbatas pada API yang disediakan |

## Kapan Harus Membuat Skill?
- Kamu mendapati dirimu **menjelaskan hal yang sama berulang-ulang** ke AI.
- Ada **prosedur multi-langkah** yang selalu sama urutannya.
- Kamu punya **script/tool** yang sering dipakai tapi AI tidak tahu caranya.
- Kamu ingin AI bisa **mengakses pengetahuan internal** (skema DB, API docs, dsb).

## Kapan TIDAK Perlu Membuat Skill?
- Tugasnya sudah bisa dilakukan AI dengan baik tanpa instruksi tambahan.
- Informasinya sudah tersedia secara umum (misal: cara pakai `git`).
- Tugasnya hanya sekali pakai (one-off).
