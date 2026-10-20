---
name: basim-breaking-news-threads-repliz
description: Use when Basim asks to turn breaking news or emergency/public-safety news into a Threads post + educational thread and schedule it through Repliz.
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [threads, repliz, breaking-news, public-safety, basim]
    related_skills: [threads-content-and-scheduling]
---

# Basim Breaking-News Threads + Repliz Workflow

## Overview

Use this workflow when Basim asks for a Threads draft based on breaking news, especially public-safety events such as earthquakes, tsunami warnings, disasters, or urgent government advisories. The goal is to produce content that is useful, humane, non-exploitative, and safe to schedule through Repliz.

For Basim, the strongest format is usually:

1. Short main post that names the event and frames why the thread is useful.
2. Early context/data posts with verified facts from reputable sources.
3. Practical tutorial steps readers can save/share.
4. Calm emotional close: panic is human, but clear steps matter.

## When to Use

Use when Basim says things like:

- “cari berita ... buat draft post”
- “buatkan agar lebih emosional”
- “buatkan tips triknya agar bermanfaat”
- “buatkan tutorial lengkap ... buat post dan utas lanjutannya”
- “tambahkan informasi terkait data ...”
- “oke post” after approving a final draft

Do not use for unrelated evergreen posts, brand positioning posts, or non-news AI/business tips unless the content is explicitly tied to a live/current event.

## Source and Fact Workflow

1. Search first; do not rely on memory for live news.
2. Prefer official sources first:
   - BMKG for earthquake/tsunami in Indonesia
   - BNPB/BPBD for disaster response
   - official local government or verified agency accounts
3. If official source extraction is unavailable, use reputable media and clearly note the source attribution. Good pattern:
   - “Data wilayah saya ambil dari laporan Kompas yang mengutip konferensi pers BMKG.”
4. For fast-changing warnings, include a caveat:
   - “Status peringatan bisa berubah cepat; cek kanal resmi BMKG/BPBD sebelum bertindak.”
5. Avoid overstating certainty. If there is inconsistency between “Laut Sulawesi” and “Pantai Selatan Mindanao”, phrase carefully:
   - “wilayah Laut Sulawesi/Pantai Selatan Mindanao”
   - or “diberitakan terkait wilayah Laut Sulawesi; beberapa laporan menyebut sumber gempa di Pantai Selatan Mindanao.”

## Writing Style

Use Indonesian, casual but responsible.

Tone:

- Emotional, but not sensational.
- Helpful, not exploitative.
- Calm, direct, and saveable.
- Short paragraphs for Threads.

Avoid:

- Clickbait disaster wording.
- Blaming victims.
- “Semoga FYP” or engagement-bait on tragedy.
- Unsupported casualty/damage claims.
- Posting unverified screenshots, voice notes, or viral rumors.

Good emotional lines:

- “Ada momen ketika notifikasi gempa bukan cuma berita.”
- “Yang paling menakutkan dari kabar gempa bukan cuma angkanya, tapi jeda setelahnya: nunggu kabar keluarga.”
- “Panik itu manusiawi. Tapi kalau kita punya urutan langkah, panik tidak harus memimpin.”

## Recommended Thread Structure

### Main post

- Mention event, magnitude/date/time if verified.
- Explain the value of the thread.
- Keep under ~300 characters when possible.

Example:

```text
Gempa M 7,7 di wilayah Laut Sulawesi/Pantai Selatan Mindanao memicu peringatan dini tsunami dari BMKG, Senin 8 Juni 2026 sekitar 06.37 WIB.

Ini tutorial singkat yang bisa kamu simpan kalau kamu, keluarga, atau tim berada di area pesisir saat peringatan tsunami muncul.
```

### Data/context replies

Add 1–2 replies early with verified warning data.

Example:

```text
Data peringatannya: BMKG menyebut status Siaga untuk sejumlah wilayah, termasuk Minahasa, Bolaang Mongondow, Manado, Minahasa Utara, Minahasa Selatan, Buol, Kepulauan Sangihe, Gorontalo, Talaud, Tolo-Toli, Palu, Donggala, Ternate, dan Bitung.
```

Example:

```text
Status Waspada juga disebut untuk beberapa wilayah seperti Tidore, Bulungan, Nunukan, Halmahera, Tarakan, Halmahera Utara, Kutai Timur, Bontang, Berau, dan sebagian pesisir lain.

Artinya: jangan beraktivitas di pantai atau tepian sungai sampai ada info resmi aman.
```

### Tutorial replies

Use ordered steps, but do not need visible `1/`, `2/` prefixes unless requested.

Recommended steps for tsunami warning content:

1. Pastikan sumber info: BMKG, BPBD, BNPB, pemerintah daerah, aparat setempat.
2. Cek posisi: pantai, pelabuhan, muara, dataran rendah dekat laut.
3. Jangan debat dulu; bergerak ke tempat tinggi/titik evakuasi jika ada arahan.
4. Bawa barang seperlunya: identitas, HP, obat, powerbank, air, uang tunai.
5. Kabari keluarga dengan format singkat: lokasi, tujuan aman, baterai, update berikutnya.
6. Jika menghubungi keluarga terdampak, kirim arahan jelas, bukan kepanikan.
7. Jangan kembali terlalu cepat; tunggu pengumuman resmi berakhir.
8. Setelah aman, bantu rapikan informasi dan cek orang rentan.

### Closing checklist

Close with a saveable checklist:

```text
Simpan checklist kecil ini:

- cek info resmi
- jauhi pantai/muara
- cari tempat tinggi
- bawa barang penting saja
- kabari keluarga singkat
- hemat baterai
- jangan kembali sebelum dinyatakan aman

Panik itu manusiawi. Tapi kalau kita punya urutan langkah, panik tidak harus memimpin.
```

## Character Counting

Before presenting final drafts or scheduling:

- Count characters with a tool/script.
- Keep each post conservatively under 500 characters for Repliz safety.
- Report counts if the user is reviewing drafts.

Python snippet:

```python
for i, part in enumerate(parts, 1):
    print(f"Part {i}: {len(part)} chars")
```

## Repliz Scheduling Defaults

This workflow relies on the broader `threads-content-and-scheduling` skill for Repliz details.

Credential env keys used for Basim:

- `REPLIZ_ACCESS_KEY`
- `REPLIZ_SECRET_KEY`
- `REPLIZ_THREADS_ACCOUNT_ID`
- `THREADS_ACCOUNT_ID` as fallback/alias

When Basim explicitly approves with “oke post”, schedule to Repliz, not to the Telegram update topic.

If no time is specified:

1. Use the next near-future 15-minute slot at least ~10 minutes ahead in WIB.
2. Convert WIB to UTC for `scheduleAt`.
3. Schedule one Threads thread: main post in `description`, replies in `replies`.
4. Keep `title` and `topic` empty strings so internal labels do not leak.
5. Use:
   - `type: "text"`
   - `medias: []`
   - `additionalInfo.isAiGenerated: false`
6. Treat HTTP `200` or `201` with `scheduleId` as success.
7. Report local WIB schedule time and `scheduleId` only; never echo secrets.

## Secure Credential Handling

If Basim provides Repliz credentials and asks to save them:

1. Save them to `~/.hermes/.env`, not memory or the skill.
2. Set file permission to `600`.
3. Do not print the secret in tool output or final response.
4. Mention that because the secret was pasted into chat, rotating/regenerating it later is safer.

Example env keys:

```dotenv
REPLIZ_ACCESS_KEY=...
REPLIZ_SECRET_KEY=...
REPLIZ_THREADS_ACCOUNT_ID=...
THREADS_ACCOUNT_ID=...
```

## Common Pitfalls

1. **Scheduling without approval.** Draft/audit first. Only schedule after Basim explicitly approves.
2. **Leaking internal labels.** Never include title/topic metadata in the Threads body. Use empty `title` and `topic` for Repliz unless there is a specific reason.
3. **Posting stale emergency status.** Disaster warnings can change quickly. Re-check official/reputable sources before final publication.
4. **Over-emotional disaster content.** Emotional is okay; sensational or engagement-bait is not.
5. **Assuming official extraction works.** If web extraction fails, use browser/search and state source limitations.
6. **Saving secrets in memory/skill.** Secrets belong in `.env`; memory can note stable non-secret preferences only.
7. **Using Telegram topic delivery by mistake.** “Oke post” in this Basim/Repliz flow means schedule to Repliz if credentials are available.

## Verification Checklist

Before final response:

- [ ] Facts/data were checked with search/browser or official sources.
- [ ] Fast-changing warning caveat included when relevant.
- [ ] Thread parts are counted and under safe length.
- [ ] Repliz credentials/account ID are available if scheduling.
- [ ] Schedule time is in WIB for the user and UTC in API payload.
- [ ] API returned `scheduleId` with status `200` or `201`.
- [ ] Final response reports schedule ID and time, not secrets.
