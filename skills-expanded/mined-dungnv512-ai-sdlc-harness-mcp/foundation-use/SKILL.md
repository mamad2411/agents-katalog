---
name: foundation-use
description: Explains how pticare's module_claim depends on the foundation_core/foundation_ui/foundation_design_system packages (git-ref pinned vs. local path override via pubspec_overrides.yaml and the nested foundation submodule) and the safe sequence to develop against and land a foundation change. Use when the user mentions foundation_core, foundation_ui, foundation_design_system, pubspec_overrides.yaml, the packages/foundation submodule, or asks how to bump/pin a foundation ref, dev module_claim and foundation together, or fix a "depends on ... from path ... from git" pub error.
---

# foundation-use

Cách `module_claim` (và host app `pticare` khi nó cũng có checkout local của
`foundation`) phụ thuộc vào ba package `foundation_core`, `foundation_ui`,
`foundation_design_system` — và cách sửa foundation mà không làm gãy build
của người khác.

## Trạng thái bình thường (không dev foundation)

`module_claim/pubspec.yaml` khai ba package đó bằng `git:` trỏ thẳng repo
`foundation` trên GitLab, pin theo `ref:` (một commit cụ thể) — **không**
`path:`. Đây là cách để bất kỳ host nào cũng cài được `module_claim` mà không
cần có submodule `foundation` nằm đúng chỗ trên máy.

Chỉ dùng ba package này: `foundation_core`, `foundation_ui`,
`foundation_design_system`. **Không** `foundation_backend`, **không** import
trực tiếp `foundation_form_dynamic` (module có `ClaimFormEngine` riêng — xem
ADR-002).

Đổi pin (vd. cần API mới từ foundation) = sửa **cả ba** `ref:` trong
`module_claim/pubspec.yaml` về **cùng một commit**. Sửa một trong ba mà quên
hai cái kia là dependency graph không compile — pub sẽ không tự báo lỗi này
nếu override đang che nó đi (xem phần "Bẫy" bên dưới).

## Dev foundation cùng lúc với module_claim

`packages/foundation` bên trong `module_claim` là **submodule của chính repo
module_claim** — dùng để sửa code foundation tại chỗ trong lúc dev, không
phải nguồn phụ thuộc lúc build:

```bash
git submodule update --init --recursive packages/module_claim
```

Bật override tạm bằng `packages/module_claim/pubspec_overrides.yaml`:

```yaml
dependency_overrides:
  foundation_core:
    path: packages/foundation/packages/foundation_core
  foundation_ui:
    path: packages/foundation/packages/foundation_ui
  foundation_design_system:
    path: packages/foundation/packages/foundation_design_system
```

File này nằm trong `.gitignore` của `module_claim` — đúng ý nghĩa "tạm khi
dev". Nếu một nhánh dev cần giữ trạng thái override để người khác pull xuống
dùng được, `git add -f` nó — đừng bỏ dòng ignore trong `.gitignore`, vì bỏ
ignore không tự động làm file "hết tạm".

## Host app (pticare) cũng cần override khi cắm module bằng path dep

Nếu `pticare` (host) cũng có `packages/foundation` local và cắm
`module_claim` qua `path:` thay vì `git:`, pub sẽ báo:

```
... depends on foundation_ui from path ... from git ...
```

— một package không được đến từ hai nguồn cùng lúc. Fix: thêm một
`pubspec_overrides.yaml` **ở gốc host**, trỏ sâu thêm một tầng
(`packages/module_claim/packages/foundation/...`), và **chép lại toàn bộ**
khối `dependency_overrides` đã có sẵn trong `pubspec.yaml` của host (vd.
override `get_it`/`injectable`) — `pubspec_overrides.yaml` **thay thế hẳn**
khối `dependency_overrides`, không cộng dồn với khối trong `pubspec.yaml`.

Vì host có submodule lồng (`module_claim` → `foundation`), lệnh init phải có
`--recursive`, và phải chạy **trước** `melos bootstrap`/`pub get` — thiếu thư
mục đích thì pub gãy ngay ở bước resolve, trước khi kịp báo lỗi rõ ràng.

## Xong việc: gỡ override, không phải xoá code

Khi đã xác nhận thay đổi ở `foundation` chạy đúng qua override:

1. Commit + push bên repo `foundation` trước.
2. Bump **cả ba** `ref:` trong `module_claim/pubspec.yaml` sang commit mới đó
   (không phải commit tạm dở dang — push xong rồi mới lấy hash).
3. **Xoá cả hai** `pubspec_overrides.yaml` (của `module_claim` lẫn của host,
   nếu host có).

Còn override nghĩa là build đang ăn code mà repo `foundation` chưa ai khác
lấy được — không phải trạng thái để merge.

## Bẫy đã gặp thật (đáng kiểm tra khi review một PR đụng foundation)

- **`pubspec_overrides.yaml` vừa nằm trong `.gitignore` vừa bị commit.** Git
  bỏ qua `.gitignore` cho file đã tracked, nên dòng ignore vô hiệu và không
  cảnh báo ai — file "tạm" âm thầm trở thành điều kiện build bắt buộc. Kiểm
  tra `git status` có sạch với file này không trước khi assume nó chỉ là dev
  convenience.
- **Ba `ref:` lệch nhau, hoặc lệch so với commit foundation mà code mới cần.**
  Nếu override đang bật, dependency graph khai báo (git ref) sai vẫn không bị
  phát hiện vì pub resolve theo path, không theo ref — chỉ lộ ra khi ai đó xoá
  override mà chưa bump ref.
- **`pubspec.lock` đổi từ `source: git` sang `source: path`** là dấu hiệu
  override đang bật trong commit đã push — không nên xuất hiện trên
  `develop`/nhánh release.

## Anti-patterns to refuse

- Sửa `ref:` chỉ một trong ba package `foundation_*` mà không sửa cả ba.
- Merge một nhánh còn `pubspec_overrides.yaml` được track mà chưa xoá, hoặc
  còn nằm trong `.gitignore` trong khi đã bị `git add -f`.
- Thêm `path:` trực tiếp trong `dependencies:` của `pubspec.yaml` thay vì qua
  `pubspec_overrides.yaml` — làm file chính không còn mô tả đúng trạng thái
  "build thật" (git ref) nữa.
- Import `foundation_backend` hoặc `foundation_form_dynamic` trực tiếp từ
  `module_claim` — module có lớp riêng cho hai việc đó (xem ADR-001, ADR-002).
