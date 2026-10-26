---
name: push-green
description: WAJIB OTOMATIS dipakai tanpa slash setiap kali akan git push, buka PR, atau merge ke GitHub. Menjalankan cek lokal dulu, menolak push kalau gagal, lalu memantau CI sampai status HIJAU. Trigger: push, git push, pr, pull request, merge, ci, github actions, check merah, hijau, gagal, workflow failed, x merah 0/1.
version: 1.0.0
tags: [git, github, ci, preflight, guardrail]
---

# Push Green (wajib hijau, dilarang merah)

Aturan keras: **jangan pernah push ke GitHub dalam keadaan gagal.** Ikon ✗ merah
(`0/1` checks passed) adalah keadaan yang DILARANG. Target selalu ✓ hijau.

## Kapan jalan otomatis

User bilang push / pr / merge / "udah bisa di-push?" / minta rilis. Agent langsung
jalankan alur di bawah. Jangan tanya, jangan langsung `git push`.

## Alur wajib (4 langkah, urut)

```sh
S=~/.agents/skills-store/push-green/scripts

$S/preflight.sh          # 1. cek lokal — exit != 0 = JANGAN PUSH
git push                 # 2. baru push
$S/watch.sh              # 3. tunggu CI sampai success
$S/watch.sh --report     # 4. lapor hasil (hijau/merah + link)
```

Kalau `preflight.sh` gagal: **stop**. Laporkan perintah yang gagal, exit code, dan
potongan error. Perbaiki dulu, ulangi dari langkah 1. Jangan `--no-verify`,
jangan `git push --force` untuk "menghilangkan merah".

Kalau `watch.sh` melaporkan merah: jalankan `gh run view <id> --log-failed`,
perbaiki akar masalahnya, commit, ulangi dari langkah 1. Jangan menutup PR atau
menonaktifkan workflow supaya kelihatan hijau.

## Yang dicek preflight.sh

- konflik merge tertinggal (`<<<<<<<`) di file berubah — termasuk file untracked
- `git diff --check` (whitespace error)
- stack terdeteksi → lint, typecheck, test, build lewat `mamat-eval` (mode penuh,
  karena CI juga menjalankan test/build). `PUSH_GREEN_FAST=1` untuk mode cepat (lint saja).
- repo tanpa stack / tanpa script → lolos (bukan gagal)

## Yang dilakukan watch.sh

- `gh run list` untuk branch aktif, poll tiap 10 s, timeout 15 menit
- `success` → exit 0
- `failure` / `cancelled` / `timed_out` → cetak URL + 40 baris log gagal, exit 1
- tidak ada workflow di branch itu → exit 0 dengan catatan "no CI"

## Larangan

- Push sebelum `preflight.sh` hijau.
- Bilang "selesai" / "sudah aman" selama check masih ✗ atau masih `in_progress`.
- Menambah `continue-on-error`, `if: false`, atau menghapus step test demi hijau.
- `--no-verify`, `--force`, atau amend commit yang sudah ter-push.
