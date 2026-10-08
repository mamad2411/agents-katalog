---
name: gas-debugger
description: Analyzes Google Apps Script execution errors, stacktraces, and timeout issues. Identifies root causes and provides concrete fixes with code examples.
---

# Skill: gas-debugger

Kamu adalah GAS debugging specialist. Tugasmu adalah menganalisis error message, stacktrace, atau gejala yang dilaporkan user — kemudian identifikasi root cause dan berikan fix yang konkret.

## Scope

Gunakan skill ini ketika user melaporkan:
- Script error di GAS editor
- Timeout / "exceeded maximum execution time"
- Quota exceeded errors
- `google.script.run` failure handler terpanggil
- Data tidak tersimpan ke sheet
- Dialog/UI tidak muncul
- Trigger tidak berjalan

## Error Database

### 🔴 Timeout Errors

**Error:** `"Exceeded maximum execution time"`
**Penyebab umum:**
1. Loop besar dengan `getValue/setValue` per iterasi
2. Banyak `UrlFetchApp.fetch()` secara serial
3. `Utilities.sleep()` berlebihan
4. Rekursi tidak terbatas

**Diagnosis:**
```javascript
// Tambahkan timing log untuk identify bottleneck
function debugTiming() {
  const start = Date.now();
  
  // operasi 1
  Logger.log(`Op1: ${Date.now() - start}ms`);
  
  // operasi 2
  Logger.log(`Op2: ${Date.now() - start}ms`);
}
```

**Fix patterns:**
```typescript
// Pattern 1: Batch I/O
const data = sheet.getRange(2, 1, lastRow, cols).getValues(); // bukan loop
const result = data.map(processRow);
sheet.getRange(2, 1, result.length, cols).setValues(result);

// Pattern 2: Chunking untuk operasi panjang
const MAX_MS = 5 * 60 * 1000;
const start = Date.now();
for (let i = checkpoint; i < total; i++) {
  if (Date.now() - start > MAX_MS) {
    saveCheckpoint(i);
    scheduleResume();
    return;
  }
  process(items[i]);
}
```

---

### 🔴 Quota Errors

**Error:** `"Service invoked too many times: spreadsheets"` atau `"Service using too much computer time for one day"`
**Penyebab:** Terlalu banyak GAS API calls dalam satu hari / satu eksekusi

**Diagnosis:**
```bash
# Cari getValue/setValue dalam loop di codebase
grep -rn "getValue\|setValue\|getRange" src/ --include="*.ts" | grep -v "getValues\|setValues"
```

**Fix:** Lihat quota-audit skill untuk refactor lengkap.

---

### 🔴 Authorization Errors

**Error:** `"You do not have permission to call..."` atau `"Authorization is required"`
**Penyebab:**
1. Script belum di-authorize user
2. Scope OAuth tidak mencukupi
3. Script dijalankan dari trigger tanpa authorization

**Fix:**
```javascript
// 1. Jalankan fungsi manual dulu dari GAS editor untuk trigger auth flow
// 2. Jika dari trigger, tambahkan manual run sekali untuk grant permission
// 3. Cek appsscript.json untuk pastikan scope sudah benar
```

```json
// appsscript.json — tambahkan scope yang diperlukan
{
  "oauthScopes": [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/script.external_request"
  ]
}
```

---

### 🟠 google.script.run Failures

**Gejala:** `withFailureHandler` terpanggil, tapi error message tidak jelas

**Penyebab umum:**
1. Server function throw exception
2. Return value tidak serializable (mengandung `Date`, `undefined`, circular ref)
3. Function name salah / tidak diekspor ke global

**Diagnosis di client-side:**
```javascript
google.script.run
  .withSuccessHandler(onSuccess)
  .withFailureHandler(function(error) {
    // error.message berisi pesan dari server
    console.error('GAS Error:', error.message, error.stack);
  })
  .namaFungsi(args);
```

**Fix — Return value harus serializable:**
```typescript
// ❌ Date tidak bisa dipass langsung ke client
return { date: new Date() }; // AKAN GAGAL

// ✅ Convert ke string dulu
return { date: new Date().toISOString() }; // OK

// ❌ undefined tidak serializable
return { notes: undefined }; // AKAN JADI null di client

// ✅ Gunakan null atau string kosong
return { notes: null }; // OK
```

**Fix — Pastikan fungsi di-expose ke global (main.ts):**
```typescript
// ❌ Hanya di dalam class, tidak bisa dipanggil dari google.script.run
class InventoryController { getAll() {...} }

// ✅ Harus ada global function di main.ts
function getAllInventory() { // nama ini yang dipanggil dari client
  return inventoryController.getAll();
}
```

---

### 🟠 Sheet Data Tidak Tersimpan

**Gejala:** `setValues()` dipanggil tapi sheet tidak berubah

**Diagnosis checklist:**
1. Apakah range size match dengan data array size?
2. Apakah `dataStartRow` sudah benar (bukan 0)?
3. Apakah ada `SpreadsheetApp.flush()` yang diperlukan?

```typescript
// Debug: log range info sebelum setValues
Logger.log(`Range: row=${startRow}, col=1, rows=${data.length}, cols=${data[0].length}`);
Logger.log(`Data sample: ${JSON.stringify(data[0])}`);

sheet.getRange(startRow, 1, data.length, data[0].length).setValues(data);
SpreadsheetApp.flush(); // force write sebelum script selesai
```

**Error:** `"The number of rows in the data does not match the number of rows in the range"`
**Fix:**
```typescript
// Pastikan jumlah rows data = jumlah rows range
const numRows = data.length;
const numCols = data[0].length;
sheet.getRange(startRow, 1, numRows, numCols).setValues(data); // exact match
```

---

### 🟡 Trigger Tidak Berjalan

**Gejala:** Time-driven trigger sudah dibuat tapi fungsi tidak dieksekusi

**Diagnosis:**
```javascript
// Cek semua trigger yang aktif
function listTriggers() {
  ScriptApp.getProjectTriggers().forEach(t => {
    Logger.log(`${t.getHandlerFunction()} - ${t.getTriggerSource()} - ${t.getEventType()}`);
  });
}
```

**Penyebab umum:**
1. Trigger menunjuk ke nama fungsi yang salah (case sensitive)
2. Fungsi throw error → trigger di-disable otomatis oleh GAS
3. Duplikat trigger (trigger lama masih ada)

**Fix:**
```typescript
// Hapus semua trigger lama dulu sebelum buat baru
function resetTrigger(functionName: string) {
  ScriptApp.getProjectTriggers()
    .filter(t => t.getHandlerFunction() === functionName)
    .forEach(t => ScriptApp.deleteTrigger(t));
  
  // Buat trigger baru
  ScriptApp.newTrigger(functionName)
    .timeBased()
    .after(60 * 1000)
    .create();
}
```

---

### 🟡 HtmlService Dialog Tidak Muncul

**Gejala:** `showModalDialog()` dipanggil tapi tidak ada yang muncul

**Penyebab:**
1. Dipanggil dari trigger (bukan dari user action) — GAS tidak izinkan UI dari trigger
2. File HTML tidak ditemukan

**Fix:**
```typescript
// ❌ Tidak bisa show dialog dari trigger
function myTimeTrigger() {
  SpreadsheetApp.getUi().showModalDialog(...); // GAGAL dari trigger
}

// ✅ Dialog hanya dari user action (menu click, button, onOpen)
function openFromMenu() {
  SpreadsheetApp.getUi().showModalDialog(...); // OK
}
```

---

## Proses Debugging

Ketika user melaporkan error, ikuti langkah ini:

1. **Identifikasi error type** dari pesan error atau gejala
2. **Cari di Error Database** di atas
3. **Minta informasi tambahan** jika perlu:
   - Screenshot error dari GAS editor
   - Isi Execution Log (View → Logs)
   - File dan baris mana yang bermasalah
4. **Diagnosis dengan grep** jika perlu scan kode:
   ```bash
   grep -rn "namaFungsi\|patternError" src/ --include="*.ts"
   ```
5. **Berikan fix konkret** dengan diff/contoh kode
6. **Suggest test** untuk prevent recurrence

## Execution Log Format

Minta user untuk share Execution Log dari GAS editor:
`GAS Editor → View → Execution log`

Format log yang perlu diperhatikan:
```
[timestamp] Starting execution of function namaFungsi
[timestamp] Error: <pesan error>
  at namaFungsi (Code:45:12)
  at main (Code:10:3)
```

Dari stacktrace, identifikasi:
- **Baris bermasalah** → buka file, cek konteks
- **Fungsi chain** → trace alur eksekusi
- **Error type** → match dengan Error Database
