# Database Design Rules

Gunakan prinsip:

- normalization first
- optimize later

---

## Wajib

- foreign key
- indexes
- timestamps
- soft delete jika diperlukan

---

## Jangan

- menyimpan data yang dapat dihitung ulang
- membuat kolom duplikat
- menggunakan JSON tanpa alasan

---

## Naming

Tables:

- snake_case
- plural

Columns:

- snake_case

Foreign key:

- user_id
- wallet_id
- category_id