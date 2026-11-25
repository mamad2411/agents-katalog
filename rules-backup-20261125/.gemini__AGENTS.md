# Aturan global AI

Semua aturan ada di `~/.agents/RULES.md` (kanonik, dipakai semua AI CLI).
Baca file itu sekali di awal sesi, lalu ikuti. Jangan menyalin isinya ke sini.

Ringkas: skill dicari lewat `python3 ~/.agents/skillq.py "<tugas>" -n 5` (0 token prompt),
output ≤15 baris, rencana dulu, verifikasi sebelum bilang selesai, MCP on-demand saja.
