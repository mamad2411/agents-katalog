---
name: sky-desktop-app
description: >-
  Masaüstü uygulama: Tauri 2 ve Electron seçimi, ana süreç/arayüz iletişimi (Tauri komutları,
  Electron IPC + contextBridge), güvenlik (capabilities, contextIsolation, sandbox, CSP), sistem
  tepsisi, menüler ve global kısayollar, bildirimler, otomatik güncelleme, kod imzalama ve macOS
  notarization, Windows yükleyici, çok platformlu CI build. "Masaüstü uygulama", "Electron",
  "Tauri", "Windows/Mac uygulaması" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Masaüstü Uygulama

## Seçim

| | Tauri 2 | Electron |
|---|---|---|
| Boyut | küçük (sistem WebView) | büyük (Chromium gömülü) |
| Bellek | düşük | yüksek |
| Arka uç | Rust komutları + eklentiler | Node.js |
| Görünüm | WebView farkları olabilir | her yerde aynı Chromium |
| Mobil | iOS/Android de | yok |
Varsayılan **Tauri**; Node'a derin bağımlılık veya Chromium'a özgü özellik gerekiyorsa **Electron**.

## Tauri

```rust
#[tauri::command]
async fn export_report(month: String) -> Result<String, String> {
    let path = build_report(&month).await.map_err(|e| e.to_string())?;
    Ok(path.display().to_string())
}
// tauri::Builder::default().invoke_handler(tauri::generate_handler![export_report])
```
```ts
import { invoke } from "@tauri-apps/api/core";
const path = await invoke<string>("export_report", { month: "2026-11" });
```
İzinler `src-tauri/capabilities/*.json` ile en az yetki (fs kapsamı belirli klasör, shell kapalı).
Eklentiler: fs, dialog, notification, store, updater, global-shortcut, deep-link, sql.

## Electron

```ts
// main.ts
const win = new BrowserWindow({
  webPreferences: { preload: path.join(__dirname, "preload.js"), contextIsolation: true, nodeIntegration: false, sandbox: true },
});
ipcMain.handle("report:export", async (_e, month: string) => exportReport(validateMonth(month)));
// preload.ts
contextBridge.exposeInMainWorld("api", { exportReport: (m: string) => ipcRenderer.invoke("report:export", m) });
```
Güvenlik: katı CSP, dar API, IPC girdisini doğrula, uzak içerik yükleme yok, `shell.openExternal` URL doğrulaması.
Paketleme: Electron Forge veya electron-builder.

## Masaüstü hissi

Yerel menü ve kısayollar (⌘N, ⌘,), sistem tepsisi/menü çubuğu simgesi, global kısayol, yerel bildirimler, dock rozeti,
dosya sürükle-bırak, pencere durumunu hatırlama, koyu mod, derin bağlantı (`myapp://`), dosya ilişkilendirme, çevrimdışı SQLite.

## Güncelleme ve dağıtım

- İmzalı otomatik güncelleme (Tauri updater / electron-updater), "Yeni sürüm hazır · Yeniden başlat", beta/stable kanalları.
- macOS: Developer ID imzası + **notarization**, universal build. Windows: kod imzalama (SmartScreen), MSI/NSIS. Linux: AppImage, deb, Flatpak.
- CI: GitHub Actions matrisi (macOS/Windows/Ubuntu), tauri-action veya electron-builder ile release taslağı.
