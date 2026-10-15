---
name: "genzys-fleetops-docs"
description: "Generate, verify, and keep consistent the GenZys FleetOps FMS documentation set (PRD/FRD/SRD/Workflow per module + mobile driver docs + quick-reference). Use when working on the GenZysFleetOps repo (prd/, fleet-app/docs/) — e.g. 'lengkapi dokumentasi', 'buat PRD/FRD/SRD/workflow modul', 'catatan ringkas', 'sync docs ke 22 modul'. Enforces the authoritative 22-module scheme (MODULE-MAP-v2.md) and backend folder mapping so docs never drift from code."
---

# GenZys FleetOps — Documentation Generator & Guardian

Skill ini mengotomasi & menjaga konsistensi seluruh dokumentasi FMS GenZys:
PRD, FRD, SRD, Workflow **per modul**, dokumentasi **mobile driver**, dan
**quick-reference**. Dipakai setiap kali menambah/mengubah modul atau dokumentasi.

## When to Use

- "lengkapi dokumentasi" / "buat PRD/FRD/SRD/workflow untuk modul X"
- "catatan ringkas" / "quick reference"
- "sync docs ke modul backend" / "tambah modul baru Mxx"
- Memverifikasi dokumentasi tidak drift dari kode BE/FE.

## The Iron Law

```
SKEMA OTORITATIF = 22 MODUL (MODULE-MAP-v2.md) — SELALU.
Folder BE = sumber kebenaran mapping. PRD/FRD/SRD/WF/BE WAJIB 1:1.
JANGAN mengarang modul demi angka (bukan "50"). JANGAN edit file generated (skills-index*, BRD induk).
```

## Peta Otoritatif (22 modul → folder BE)

| # | Modul | Folder BE (`GenZysFleetOps.Modules/`) | Pages |
|---|---|---|---|
| M01 | Auth, RBAC & Access | `AccessOrganization` | 8 |
| M02 | Vehicle Master | `VehicleMaster` | 9 |
| M03 | Driver Management | `DriverMaster` | 9 |
| M04 | Trip Assignment | `AssignmentTrip` | 10 |
| M05 | Tracking & Live Map | `TrackingMap` | 7 |
| M06 | Geofence, Alert & Exception | `GeofenceAlert` | 8 |
| M07 | Fuel & Cost | `FuelCost` | 8 |
| M08 | Maintenance & WO | `MaintenanceWorkOrder` | 10 |
| M09 | Document & Compliance | `DocumentCompliance` | 8 |
| M10 | Dashboard & Reporting | `DashboardReporting` | 11 |
| M11 | Settings, Config & Audit | `AuditAdministration` | 8 |
| M12 | Notifications | `Notifications` | 6 |
| M13 | Fleet DNA / Health | `HealthEngine` | 6 |
| M14 | Route Optimization | `RouteOptimizer` | 6 |
| M15 | Billing, Rate Card | `BillingCostCenter` | 7 |
| M16 | Regulatory & Safety | `SafetyCompliance` | 6 |
| M17 | DVIR & Inspection | `DvirInspection` | 7 |
| M18 | Safety Events | `SafetyEvents` | 7 |
| M19 | Asset & Equipment | `AssetEquipment` | 7 |
| M20 | Driver Coaching | `CoachingWorkforce` | 7 |
| M21 | Customer Experience & POD | `CustomerExperiencePOD` | 7 |
| M22 | Fuel & Spend Mgmt | `FuelSpendMgmt` | 6 |

Total: **168 pages**, 146 kode FRD. Cross-cutting: CRC-01..05 (immutability, audit-first,
policy authz, ITelemetrySource, response envelope). Open decisions: OD-03/06/09/12/13.

## Struktur Dokumentasi (target)

```
prd/
├── DOCUMENTATION-INDEX.md      # master index + matriks PRD/FRD/SRD/WF → folder BE
├── QUICK-REFERENCE.md          # 1 halaman ringkas 22 modul + CRC + OD
├── 00-PRD-Index.md             # index PRD utama
├── PRD-M01..M22-*.md           # PRD per modul (root)
├── frd/FRD-M01..M22-*.md       # FRD per modul (kode + AC + wording + cross-cutting)
├── srd/SRD-M01..M22-*.md       # SRD per modul (arsitektur, entitas/tabel, API, teknis)
├── workflow/WF-M01..M22-*.md   # Workflow per modul (alur + diagram + state machine + BR)
├── FRD.md                      # FRD terpadu (sumber split frd/)
├── PRD.md / MODULE-MAP-v2.md   # PRD ringkas + peta otoritatif
├── BRD_...docx                 # BRD INDUK — JANGAN diubah
└── _legacy-schema-lama/        # arsip skema 25-modul lama (bahan saja)

fleet-app/docs/                 # mobile (repo terpisah, sudah ter-push)
├── BRD-Mobile.md  README.md  QUICK-REFERENCE.md
├── prd/PRD-Mobile-Driver-App.md + PRD-MOB-*.md (10 layar)
└── frd/FRD-MOB-*.md (10 layar)
```

## Workflow: Tambah / Lengkapi Modul

1. **Cek peta otoritatif** di atas + folder BE nyata (`ls GenZysFleetOps.Modules/`).
2. **Tarik sumber**: baca `FRD.md` (kode FRD-Mxx), `MODULE-MAP-v2.md` (pages),
   folder BE (`Domain/`, `Features/`, `*Module.cs`, `*Configuration.cs`, Controller).
3. **Generate 4 dokumen** untuk modul (jika belum ada):
   - **PRD-Mxx** (root): DACI, Background, Problem, JTBD, Scope (page↔FRD),
     Spesifikasi Field, State Alur, Impact Metrics, User Flow, Design,
     User Stories+AC, Wording, Dependency, Catatan Penutup.
   - **frd/FRD-Mxx**: tiap kode FRD-Mxx-nn + AC (Given/When/Then) + wording + cross-cutting.
   - **srd/SRD-Mxx**: Arsitektur (vertical slice/MediatR), Entitas→tabel, API+controller,
     Persyaratan teknis, Ketergantungan, EF config, Non-fungsional.
   - **workflow/WF-Mxx**: alur step-by-step + diagram ASCII + state machine + business rules.
4. **Frontmatter** setiap file: `tags/category/related` (wikilink `[[...]]`).
5. **Update index**: `DOCUMENTATION-INDEX.md` + `QUICK-REFERENCE.md` (matriks + 1-liner).
6. **Verifikasi** (lihat bagian Verifikasi).

## Template Cepat (per modul)

- **1-liner** (quick-ref): "<aksi inti>, <validasi/kunci>, <diferensiasi>".
- **FRD AC**: `Given <kondisi>, When <aksi>, Then <hasil spesifik + kode> (FRD-Mxx-nn).`
- **Wording**: kutip persis dari FRD/PRD — jangan improvisasi microcopy.
- **SRD API**: `RequireAuthorization("<resource>.read/write")` dari `Permissions.cs`.

## Verifikasi (WAJIB sebelum selesai)

```bash
# 1. jumlah dokumen per tipe = 22 (web) / sesuai layar (mobile)
ls -1 prd/PRD-M*.md prd/frd/*.md prd/srd/*.md prd/workflow/*.md | wc -l
# 2. tak ada artifact heredoc/error
 grep -rlE 'PRDEOF|command not found|No such file' prd/ fleet-app/docs/ || echo CLEAN
# 3. frontmatter valid (tiap file mulai '---')
for f in prd/frd/*.md prd/srd/*.md prd/workflow/*.md; do head -1 "$f" | grep -q '^---$' || echo "BAD: $f"; done
# 4. mapping folder BE 1:1
 ls GenZysFleetOps-be/src/GenZysFleetOps.Modules/   # cocokkan dgn peta di atas
```

## Mobile (fleet-app)

- Repo **terpisah** (`fleet-app`, remote sendiri) — commit/push di repo itu.
- Layar driver-facing resmi dari FRD `[Driver]`: M01-02, M03-09, M04-08/09, M17-02, M21-02
  + turunan wajar: Profile, Fuel Log (M07), Notifikasi (M12), Coaching (M20) = 10 layar.
- **Offline-first** wajib: DVIR, POD, Fuel Log (antrian sync idempotent).
- BRD-Mobile = **turunan** (refer BRD induk), bukan BRD baru.

## Pitfalls

- **Jangan** paksa "50 PRD" — skema otoritatif 22; granularitas naikkan lewat per-modul
  (PRD+FRD+SRD+WF = 4 dok/modul), bukan mengarang modul.
- **Jangan** edit `skills-index.db`, `skills-INDEX.md`, `skills-junk.txt`, BRD induk.
- **Jangan** klon katalog skill — wire via symlink (`link-skills-min.sh`).
- Nomor lama (M12=Inventory dst.) = skema usang → arsip `_legacy-schema-lama/`.
- Heredoc ganda: tulis file besar dalam 2 chunk (`>` lalu `>>`) untuk hindari race/truncation.

## Referensi

- `MODULE-MAP-v2.md` (peta otoritatif), `FRD.md` (kode), `Permissions.cs` (authz),
  `DOCUMENTATION-INDEX.md` (matriks), skill terkait: `documentation-writer`, `create-readme`.

> Skill menjaga dokumentasi FMS GenZys tetap lengkap, granular, dan 1:1 dengan kode.
