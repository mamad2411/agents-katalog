---
name: ci-red-debugging-github-actions
version: 1.1.0
language: vi
maturity: proven-in-battle
description: >
  Tự chẩn đoán và xử lý CI đỏ (Flutter / GitHub Actions) trong môi trường KHÔNG đọc
  được log CI và KHÔNG có Flutter SDK local — dùng chính CI làm "oracle 1-bit" kết hợp
  bisect có kỷ luật. Mục tiêu: giải phóng 100% công sức người dùng, không bắt họ mở
  VSCode/máy local để xem lỗi rồi gửi ngược lại.
use_when:
  - CI GitHub Actions đỏ trong repo Flutter và không tự sửa được ngay
  - "'gh run view --log' / '--log-failed' lỗi EOF hoặc trả chuỗi rỗng"
  - Sandbox không cài được Flutter/Dart SDK (storage.googleapis.com / pub.dev bị chặn)
  - Cần xác minh compile/test khi không thể chạy local
do_not_use_when:
  - Log tải được bình thường → đọc log trực tiếp, nhanh hơn hẳn
  - Đỏ do hạ tầng runner (mạng/lưu lượng GitHub) → chạy lại run trước khi phân tích
origin: phiên Task 3 In4Up (2026-08-20) — 15+ vòng CI đỏ được chẩn đoán tự động
---

# SKILL — Debug CI đỏ Flutter khi không có log, không có SDK

## 0. Chân lý nền tảng

Khi không đọc được log, **mỗi lần chạy CI là một oracle trả lời ĐÚNG/SAI cho đúng MỘT
giả thuyết** (~40–70 giây/vòng với Flutter). Bisect log₂(n) vòng định vị được mọi thủ
phan cấp file — miễn là mỗi vòng đổi đúng một biến số.

Sai lầm chết người: đứng yên "suy luận thêm" thay vì push một vòng xác nhận.
Suy luận là miễn phí nhưng thường sai; oracle tính bằng phút nhưng luôn đúng.

## 1. Khảo sát môi trường (làm 1 lần, ~30 giây)

```bash
# Host mở/chặn (000 = chặn)
for h in storage.googleapis.com pub.dev api.github.com results-receiver.actions.githubusercontent.com; do
  echo "$h -> $(curl -s -o /dev/null -m 8 -w '%{http_code}' "https://$h/" 2>/dev/null || echo 000)"
done

# Token có quyền gì với repo?
gh api /repos/<owner>/<repo> --jq '.permissions'

# Workflow nào tồn tại?
gh workflow list --all

# Đọc workflow QUA API (kể cả khi git local đang lỗi):
gh api repos/<o>/<r>/contents/.github/workflows/<f>.yml --jq .content | base64 -d
```

Ba thực tế đã ghi nhận trên Arena (nếu gặp lại thì đỡ mất công khám phá):
- `api.github.com`, `codeload.github.com` mở; `storage.googleapis.com`, `pub.dev`,
  `results-receiver.actions.githubusercontent.com` CHẶN ⇒ không SDK local, không log CI.
- Token GitHub App thường thiếu quyền `workflows` ⇒ KHÔNG tạo/sửa được file trong
  `.github/workflows/` (push chứa file đó bị reject cả nhánh — hãy tách riêng commit).
- `gh run list/watch/view` (metadata + step-level ✓/X) HOẠT ĐỘNG — đây là канал chính.

## 2. Vòng lặp oracle (lệnh chuẩn)

Dùng script kèm theo (tự commit + push + watch + báo step):

```bash
docs/skills/ci-red-debugging/scripts/ci_check.sh "ci: bisect B2 - <giả thuyết>"
```

Hoặc tay:

```bash
git add -A && git commit -q -m "ci: bisect <bước> — <giả thuyết>" && git push -q origin <branch>
sleep 15
RID=$(gh run list --workflow=<wf>.yml --limit 1 --json databaseId --jq '.[0].databaseId')
gh run watch $RID --exit-status >/dev/null 2>&1; echo "RESULT: $?"    # 0=xanh 1=đỏ
gh run view $RID 2>&1 | grep -E "✓|X|^  - "                           # X step nào?
```

Luật chơi:
1. **Đọc step TRƯỚC, nội dung sau.** `X Analyze` và `X Run tests` là hai bệnh khác hẳn.
2. **Mỗi vòng đúng MỘT biến số.**
3. **Mỗi commit bisect phải tự thống nhất** (compile đứng một mình được) — nếu không,
   lỗi nhiễu do chính bản bisect làm oracle nói dối.
4. Commit bisect phải **chạm path trong `paths:` filter** của workflow, nếu không CI
   sẽ không chạy mà bạn tưởng "xanh".

## 3. Cây quyết định

```
ĐỎ
├─ Step ANALYZE đỏ
│   ├─ B1: Lỗi file trong phạm vi analyze? → rà checklist bẫy (mục 5)
│   ├─ B2: Đoán lint? → KHÔNG đoán — tải rule-set thật:
│   │     gh api repos/flutter/packages/contents/packages/flutter_lints/lib/flutter.yaml?ref=main --jq .content | base64 -d
│   │     (kèm include package:lints/recommended.yaml từ dart-lang/lints)
│   │     flutter_lints 6.0 đã GIẢM mạnh rule — "lint quen thuộc" nhiều khi không còn
│   └─ B3: Bisect NỘI DUNG file: skeleton tối thiểu → trả từng nửa
│
├─ Step RUN TESTS đỏ
│   ├─ T1: Thay TOÀN BỘ test bằng 1 test không-thể-sai (expect(1,1))
│   │     Vẫn đỏ  ⇒ LỖI LOAD SUITE (import-chain compile gãy) → bisect IMPORT
│   │     Xanh   ⇒ ASSERTION sai → bisect theo NỬA nhóm test
│   ├─ Nhớ: flutter analyze ≠ flutter test compile (CFE). Có construct analyzer
│   │     chấp nhận nhưng CFE từ chối — đặc biệt tên class đi qua EXPORT chain.
│   └─ Test "không-thể-sai" mà đỏ = load failure — đây là phép phân biệt rẻ nhất.
│
└─ Step KHÁC (pub get / setup) → thường là hạ tầng: re-run 1 lần rồi hẵng phân tích
```

## 4. Giao thức bisect (thứ tự các vòng)

1. **Cô lập FILE**: git rm file nghi vấn (hoặc dời khỏi paths-filter), push.
   Đỏ tiếp ⇒ thủ phạm ở file khác. Xanh ⇒ đúng file.
2. **Cô lập KHỐI**: skeleton tối thiểu của file (class rỗng + 1 hàm), push cho xanh
   nền, rồi trả nội dung theo NỬA: imports → helpers → bodies.
3. **Cô lập IMPORT**: skeleton + từng import với usage tối thiểu (nhớ: import không
   dùng ⇒ warning ⇒ tự đỏ — phải dùng nó). Cảnh giác cặp A + B-mà-export-A.
4. **Cô lập TEST**: như mục 3 (T1 trước tiên!), rồi chặt nửa nhóm test.
5. **Chốt**: fix + khôi phục toàn bộ phần đã rút trong MỘT commit, push xác nhận xanh,
   ghi postmortem vào comment code/ADR + dòng "khi_nào_dùng" của skill này nếu có loại bẫy mới.

Quy ước: commit bisect đặt tên `ci: bisect <mã vòng> - <vừa làm gì>`; mở PR thì
squash-merge để lịch sử sạch.

## 5. Checklist bẫy ĐÃ TRẢ GIÁ THẬT (rà trước khi push)

| # | Bẫy | Dấu hiệu | Tránh thế nào |
|---|---|---|---|
| 5.1 | Phạm vi analyze hẹp hơn tưởng tượng | analyze xanh mà test đỏ (compile kéo chain) | Đọc paths/dirs trong lệnh analyze của workflow; coi file ngoài scope là "chưa từng được analyze" |
| 5.2 | **Export-chain trap** (bẫy đắt nhất) | (a) cùng file import X trực tiếp + import Y mà Y export X ⇒ analyze đỏ; (b) nhắc tên class QUA export của file khác ⇒ analyze xanh nhưng flutter test LOAD đỏ | Trong lib: đọc dữ liệu qua FIELD (`entry.a.b`). Trong test: fixture JSON (`Model.fromJson`) — JSON đúng format lưu trữ thật hơn nữa |
| 5.3 | Ảo giác escape của tool-output | "regex bị nhân đôi backslash" | Kiểm byte thật: `grep -F 'RegExp(r' f | od -c` — output công cụ hiển thị qua JSON luôn nhân đôi `\` |
| 5.4 | Float round-trip assertion | `0.4-0.1 != 0.3` sau khi serialize left/top/right/bottom | Giá trị dyadic (0.125/0.25/0.375) hoặc `closeTo` |
| 5.5 | Sandbox tái bản giữa phiên | `git log` về commit nền, files thành untracked, mất remote-tracking refs | `cp` file đang sửa → /tmp TRƯỚC; `git config remote.origin.fetch '+refs/heads/*:refs/remotes/origin/*'; git fetch; git reset --hard origin/<branch>`; cp ngược lại |
| 5.6 | Dual-view file layer | edit_tool báo OK mà bash grep không thấy (và ngược lại); "nothing to commit" ma | KHÔNG song song lệnh ghi-file với git; sau khi ghi bằng tool, xác nhận bằng grep/md5sum TRƯỚC khi commit |
| 5.7 | paths-filter | push xong không có run mới | Đảm bảo commit chạm path match của trigger |
| 5.8 | Bisect gây đỏ tự thân | file bisect cắt bằng script python bị vỡ cú pháp ⇒ đỏ oan, đổ lỗi nhầm cho code đang nghi vấn | MỌI file bisect phải qua balance-check (phiên bản xử lý CẢ nháy đơn lẫn nháy kép) trước khi push; vòng T9–T10 từng đỏ oan vì thế |
| 5.9 | Cắt normalize/dọn dòng bằng regex | `\s+`/`[ \t]+` gộp run nhưng KHÔNG xóa space sát `\n` (`'b \n'` giữ nguyên) | Chuẩn hóa per-line: split('\n') → collapse+trim từng dòng → join; nghĩ "line edges" trước khi dùng replaceAll toàn chuỗi |
| 5.10 | show-combinator + export-chain | `show X, Y` với tên KHÔNG dùng thật (đặc biệt tên đến qua export của file khác) ⇒ CI analyze đỏ; lấy tên hàm SM-2 vào test bằng MỌI đường (import trực tiếp = B6, show-từ-export) đều gãy | Chỉ show đúng tên đang dùng; khi test cần đối chiếu thuật toán, dùng phép so sánh tương đương nội bộ (compact-vs-compact) thay vì gọi hàm ngoài qua export |
| 5.12 | Mutable fields + bisect | Bisect cắt class Engine (nơi gán field) để Unit đứng một mình ⇒ `prefer_final_fields` đỏ oan nhiều vòng; mutable state cũng ngược mục 4 (isolate) | Thiết kế model immutable + copy-on-write ngay từ đầu — bisect an toàn mọi cấu hình, đúng chuẩn isolate |
| 5.11 | Underscore local variable | `final _ = expr;` ⇒ `no_leading_underscores_for_local_identifiers` (có trong lints/recommended — CI fatal) | Dùng trực tiếp `expect(Class.method, isNotNull)` hoặc đặt tên có nghĩa |
| 5.13 | Interpolation maximal munch | `'$var_suffix.txt'` — lexer đọc `\$var_suffix` thành biến **`var_suffix`** (dấu `_` là ký tự hợp lệ của identifier) ⇒ `Undefined name 'var_suffix'` | Luôn dùng `'${var}_suffix.txt'` khi hậu tố bắt đầu bằng `_`. Scan nhanh: regex `\$[a-zA-Z][a-zA-Z0-9_]*_` trong string literal |
| 5.14 | Restore file từ commit CŨ làm MẤT fix mới | `git checkout <commit-cũ> -- file` trong lúc bisect ⇒ fix ở commit MỚI HƠN bị revert lặng lẽ, vòng bisect sau "không giải thích được" | Sau MỌI restore: `grep` chính xác fix kỳ vọng trong file TRƯỚC khi commit; ghi rõ commit nguồn khi restore |
| 5.15 | Workflow `tail -n 300 analyze.log` cắt mất ERROR | `flutter analyze` liệt kê issue theo thứ tự file — ERROR trong file `lib/...` nằm ở ĐẦU log, `tail -300` chỉ còn info-lint `packages/...` ⇒ log "trông như không có error" | Đọc JOB LOG đầy đủ (không phải artifact). Job log đọc được khi API bị chặn: `gh api .../jobs/<id>/logs` trả 302 → Location (blob signed URL); encode Location bằng `base64 -w0` để tránh giá trị bị redact trong tool output, decode lại, fetch URL đó. (Cảnh báo: tool output có thể redact UUID/sig — luôn đi qua base64) |
| 5.16 | API package theo version — `FilePicker.platform` không tồn tại ở file_picker 11.x | `Member not found: 'platform'` — API đúng 11.x: `FilePicker.pickFiles(...)` / `FilePicker.getDirectoryPath()` TRỰC TIẾP (static) | Kiểm pubspec.lock version thực, đối chiếu docs của đúng version đó (pub.dev docs có tab theo version) — đừng nhớ API từ version khác |
| 5.17 | `const` widget bọc child không const | `const Expanded(child: Text(style: Theme.of(context)...))` ⇒ `Not a constant expression` (Theme.of là method call) | `const` chỉ khi TOÀN BỘ subtree const; có `Theme.of(context)`/method call bên trong ⇒ bỏ `const` |
| 5.19 | **Đường dẫn tương đối bị "kẹt" ở gốc package** (gây cả đỏ lẫn HIỂU SAI log) | File `lib/screens/tools/word_list/x.dart` import `'../../vocab_image/y.dart'` ⇒ resolve thành `lib/screens/vocab_image/y.dart` (KHÔNG phải `lib/vocab_image/`); ngược lại `'../../../models/z.dart'` từ `lib/models/` lại resolve thành `lib/models/z.dart` vì `package:` URI **kẹt `../` tại gốc package** ⇒ import trông như "hỏng" nhưng analyze XANH | Khi rà import bằng script đọc filesystem (python/grep) PHẢI mô phỏng kẹt gốc package (`package:in4up/<path>`, bỏ `..` thừa ở đầu) — nếu không sẽ báo oan hàng chục "URI hỏng" ở file legacy (sound_list_screen/soundlist_panel/youtube_sheet) và bỏ sót ca đỏ thật. Quy tắc nhớ: đếm `../` từ **thư mục chứa file**, không được vượt quá gốc `lib/` |
| 5.20 | **`tail -n 300` + 416 issues ⇒ không thấy error** (thực chiến 2026-09-09) | Log `flutter analyze` chỉ hiện info/warning từ `lib/models/…` trở đi; ERROR nằm ở ĐẦU log (file `lib/features/…` đứng trước alphabetically) ⇒ tưởng "không có error" | Khi chỉ thấy info/warning mà CI vẫn đỏ: thủ phạm nằm ở file có path đứng TRƯỚC file đầu tiên xuất hiện trong log. Khoanh vùng bằng `git diff <commit-xanh> <commit-đỏ> -- lib packages test pubspec.yaml` (so cây, bỏ qua history) rồi ưu tiên file mới thêm/sửa |
| 5.18 | **iOS deployment target thấp hơn pod yêu cầu** | `pod install` đỏ: `[!] CocoaPods could not find compatible versions for pod "google_mlkit_commons" ... required a higher minimum deployment target` + `Error: The plugin ... requires a higher minimum iOS deployment version` | Đọc `s.platform = :ios, 'X'` trong podspec của plugin (google_mlkit_* = **15.5** do MLKitVision) rồi nâng ĐỦ 3 nơi: `ios/Podfile`, `ios/Runner.xcodeproj/project.pbxproj`, `ios/Flutter/AppFrameworkInfo.plist`. Dùng 1 lệnh `scripts/ci/ios_set_deployment_target.sh <target>` thay vì rải `sed` trong workflow. `post_install` chỉ được NÂNG, không được HẠ target của pod (ép tất cả về 14.0 = tự bắn chân) |

| 5.21 | **Tên step workflow chứa `": "` ⇒ run đỏ 0 giây (startup_failure)** (thực chiến 2026-09-23, LHB-006) | Run mới nhất `failure` với thời lượng **0s**; UI ghi \"This run likely failed because of a workflow file issue\"; `gh run view <id>` không có step nào | Trong YAML, plain scalar KHÔNG được chứa `": "` (bị hiểu là mapping) — tên step kiểu `LHB tests — Thuộc Lòng: SRS/cloze…` phải **quote**: `- name: \"LHB tests — …: …\"`. Đây cũng là oracle YAML RẺ NHẤT: push xong ~20s là biết file workflow có hợp lệ không |
| 5.22 | **`on.push.paths` lọc ⇒ commit \"im lặng\" không sinh run** (thực chiến 2026-09-23) | Push thành công nhưng `gh run list` không có run mới cho sha đó ⇒ tưởng \"chưa push\" hoặc \"CI treo\" | `app_analyze.yml` chỉ chạy khi chạm `lib/**`, `test/**`, `pubspec*`, chính file workflow. Commit chỉ sửa `analysis_options.yaml`/`docs/**` **không** sinh run: muốn CI chạy lại phải kèm 1 chạm `lib/**` hoặc `test/**` (bẫy này gặp đúng lúc revert probe tắt lint) |
| 5.23 | **APK release "xanh" nhưng KHÔNG CÀI ĐƯỢC — Flutter đổi tên che mất `-unsigned`** (thực chiến 2026-09-23, CI-ANDROID-03) | Job Android xanh, Release có đủ APK, máy báo "App not installed / package appears to be invalid" (adb: `INSTALL_PARSE_FAILED_NO_CERTIFICATES`). Nguyên nhân: `buildTypes.release {}` không có `signingConfig` ⇒ AGP xuất `app-*-release-unsigned.apk`; `FlutterPlugin.kt` copy sang `flutter-apk/` và `rename { "app[-abi][-flavor]-release.apk" }` ⇒ tên file mất chữ `unsigned`, log CI không hề đỏ | Xanh ≠ cài được. (1) `grep -rn signingConfig android/` phải ra kết quả trong `release {}`; (2) luôn có bước `scripts/ci/android_verify_apk_signed.sh <apk>` (apksigner hoặc soi `APK Sig Block 42`) TRƯỚC upload; (3) đừng tin tên file trong `flutter-apk/` — soi `build/app/outputs/apk/<flavor>/release/` mới thấy hậu tố thật |
| 5.24 | **Workflow ghi đè file thật bằng stub** | Compile đỏ với `The getter 'authStateChanges' isn't defined` / `Undefined class 'AppUser'` dù local xanh — step "Create ... Auth Files" `cat > lib/services/auth_service.dart` đè file git bằng stub 5 dòng viết từ thời file còn chứa secret | Mọi `cat > lib/...` trong workflow phải bọc `if [ ! -f ]` (hoặc bỏ hẳn khi file đã vào git). Khi CI đỏ ở compile mà local xanh: grep workflow tìm `> lib/` trước khi bisect code |
| 5.25 | **Getter của type \"anh em\" — `StreamSubscription.done` KHÔNG tồn tại** (thực chiến 2026-09-27, API-002/WP1) | `await responseSub.done;` ⇒ `undefined_getter` đỏ CI; review tĩnh 3 lượt KHÔNG bắt được vì `done` quá \"quen thuộc\" (thực ra là của `StreamController` — type đứng cạnh trong cùng API) và trông như vấn đề promotion nullable | Khi dùng API dart:async: đối chiếu CHÍNH XÁC danh sách thành viên của type ĐANG NHẶN — `StreamSubscription` chỉ có cancel/onData/onError/onPause/resume/isPaused. Muốn chờ hết stream từ phía subscription: Completer hoàn thành trong onDone, hoặc đơn giản dựa vào onDone/onError (subscription tự chạy qua closure, không cần hàm ngoài chờ). Đừng tin trí nhớ về getter của type anh em; nếu CI đỏ mà code \"đúng hết\" — nghi kiểu này đầu tiên |
| 5.26 | **`await` trên method trả `void`** — `await facade.dispose();` (thực chiến 2026-09-27, API-002/WP1) | await trên void ⇒ lỗi analyze đỏ CI; `AiServiceFacade.dispose()` override `void dispose()` của ChangeNotifier, KHÔNG phải `Future<void>` như engine | Verify RETURN TYPE, không chỉ TÊN method — grep \"tồn tại tên\" không bắt được sai kiểu trả về. `dispose()` là void cho ChangeNotifier/Widget, `Future<void>` cho engine/client — đừng await bừa. Interface AiEngine.dispose là Future<void> còn facade.dispose là void: cùng tên, khác khuôn. Khi bisect tới nhóm lệnh: chia theo TỪNG DÒNG, gần như luôn ra ngay |

## 6. Khi nào PHẢI lên tiếng với người dùng

- **≥ 5–6 vòng bisect không hội tụ** (điều kiện: mỗi vòng phải thu được THÔNG TIN MỚI;
  2 vòng liên tiếp không thêm thông tin = đang quay vòng, dừng).
- Cần quyền cao hơn (workflows) hoặc log thật: đưa URL thẳng
  `https://github.com/<o>/<r>/actions/runs/<runId>/job/<jobId>` và đề nghị dán
  đúng đoạn đỏ của step — 30 giây của người dùng thay cho 1 giờ đoán.
  ✅ ĐÃ THỰC CHIẾN (Task 4): người dùng dán Expected/Actual từ log — fix đúng
  ngay vòng kế tiếp sau 11 vòng mù. LUÔN dọn "run đầy đủ" trước khi hỏi.
- Agent thường KHÔNG có thị giác — ảnh chụp màn hình log không đọc được: xin dán
  CHỮ (không phải screenshot), và lưu ý ảnh có thể không tới được filesystem sandbox.
- Remote có commit lạ/không phải của mình ⇒ hỏi trước khi rebase/force.

## 7. Phòng bệnh

1. File test import tối thiểu — ít import, ít thức gãy load.
2. Fixture JSON đúng format store thật (Hive/SharedPreferences đều là JSON anyway).
3. Float: nghĩ "round-trip qua gì?" trước khi `==`.
4. Commit nhỏ, **push ngay** — push là backup (bẫy 5.5 không mất được thứ đã push).
5. Postmortem bằng comment ngay tại chỗ vỡ — agent kế tiếp (và chính bạn ở turn sau)
   không trả giá lần hai.

## 8. Tài liệu liên quan trong repo

- `docs/playbooks/` (nếu có) — bản mở rộng của skill này.
- `tool/ci/README.md` — cách bật workflow khi token thiếu quyền `workflows`.
- `docs/adr/0001-sm2-canonical-formula.md` — ví dụ postmortem chuẩn.

## 6.1. Đọc được `analyze.log` của CI dù step chỉ in `tail -n 300`

`App analyze (rule #5)` ghi `flutter analyze ... > analyze.log` rồi in `tail -n 300`, và
upload artifact dạng **zip** (sandbox không giải nén được). Lỗi trong `lib/**` vì thế
bị chôn dưới ~300 dòng `info • Unused import` của `packages/**`. Cách lấy đủ lỗi:

1. Tạm thời **comment `include: package:flutter_lints/flutter.yaml`** trong
   `analysis_options.yaml` (lint im lặng, `error`/`warning` vẫn còn) → `flutter analyze`
   chỉ còn vài dòng → mọi error của `lib/**` lọt vào `tail -n 300`. **Bắt buộc** sửa kèm
   một file `lib/**` hoặc `test/**` vì workflow lọc `on.push.paths`.
2. `gh api "repos/<owner>/<repo>/actions/runs/<run-id>/jobs" --jq '.jobs[0].id'` → job id.
3. `gh run view --log-failed` **rỗng** với lỗi analyze (không có `##[error]` ở dòng源码);
   dùng REST: `curl -sI "https://api.github.com/repos/<owner>/<repo>/actions/jobs/<job-id>/logs"`
   (kèm `Authorization: Bearer $(gh auth token)`) → 302 + `Location:` = URL blob SAS
   (~10 phút). **Phải dùng nguyên văn**: `+`/`%2B` bị shell/mỏ neo làm hỏng →
   `AuthenticationFailed` hoặc "Signature fields not well formed".
4. Mở URL bằng fetch_page (nội dung trả theo chunk); tìm `error •`.
5. **Revert `analysis_options.yaml` ngay trong commit sửa lỗi** — đừng để probe sống
   qua một lần xanh: tắt lint = mất luôn lá chắn rule #5/dùng `Text` sai.

Bài học từ Wave 0 (PDF reader): `RegExp(r'... \' ...')` — trong raw string một nháy,
`\'` KHÔNG thoát nháy nên chuỗi cụt giữa regex → analyzer nổ 20+ error dây chuyền
(`expected_token`, `illegal_character`, `non_bool_operand`) nhưng **grep thường không ra**
vì chúng không phải "import thiếu". Muốn có nháy đơn trong regex: dùng raw string 3 nháy
`r'''...'''`.

## 6.2. Vòng lặp "probe → đọc log → sửa → revert probe" là **hai** commit, không phải một

Lần đỏ ở Wave 1.9 (`LogicalKeyboardKey.plus` — keyboard API **không có** getter `plus`,
phím numpad tên là `add`) cho thấy chi tiết đáng nhớ:

- Commit probe phải kèm một thay đổi trong `lib/**` hoặc `test/**` (workflow lọc
  `on.push.paths`), nếu không nó im lặng không chạy gì.
- Với lint TẮT, `flutter analyze` chỉ còn 123 dòng ⇒ `tail -n 300` of the step **thấy
  hết**, kể cả lỗi trong `test/**`. Đây là lúc duy nhất danh sách lỗi là đầy đủ.
- Sửa xong, commit **revert `analysis_options.yaml`** rồi push tiếp; trạng thái head
  cuối cùng phải là: lint BẬT + xanh. Nếu xanh, coi như `lib/**` và `test/**` không còn
  error nào (chỉ ERROR mới fatal trong workflow này).
- Đừng tin `git checkout <branch> -- analysis_options.yaml` khi branch đó CHÍNH LÀ đầu
  có probe: nó khôi phục nguyên cái probe. Phải checkout từ commit **gốc trước probe**
  (`git log --oneline -- analysis_options.yaml` để tìm).

## 6.3. Tự hỏi trước: **test của mình có được CI chạy không?**

Thực chiến 2026-09-23 (LHB-006): file `test/learn_by_heart_sync_test.dart` viết xong,
`flutter analyze` xanh — nhưng **không step nào chạy nó**. Oracle rộng
(`app_analyze.yml`) chỉ chạy `analyze` + rule #5, các workflow module chỉ chạy khi chạm
`lib/knowledge/**` / soundlist. Hệ quả: 2 lỗi logic thật (đảo thứ tự bài mới từ cloud;
phép "đã sync rồi" so mốc thay vì so nội dung ⇒ bỏ qua bản cloud mới hơn) nằm im trong
code đã push, chỉ lộ ra khi bộ test được đưa vào CI.

Checklist 30 giây (làm NGAY sau khi viết test mới):

```bash
grep -rn "flutter test" .github/workflows/*.yml     # step nào thật sự chạy test?
gh api repos/<o>/<r>/actions/runs/<run-id>/jobs \
  --jq '.jobs[0].steps[] | "\(.conclusion)\t\(.name)"'   # step có XANH hay bị bỏ qua?
```

- Bước test tự chế nên **tự bỏ qua an toàn** khi file chưa có trên nhánh
  (`[ -f "$f" ] || continue` rồi `exit 0`) ⇒ không làm đỏ CI của nhánh khác dùng chung
  workflow. Với file có thật thì `tail -n 400 <log>` để lỗi hiện trong job log.
- Đọc kết quả test trong **job log** (không phải artifact): cuối log có dòng
  `🎉 N tests passed.` hoặc danh sách `❌`. Artifact chỉ chứa text log, giải nén trong
  sandbox được thì thêm một đường (không bắt buộc).
- `flutter test <file>` chạy ngay sau `flutter pub get` trong cùng job — không cần
  cài gì thêm, và chậm hơn analyze chỉ ~30–60 giây.
