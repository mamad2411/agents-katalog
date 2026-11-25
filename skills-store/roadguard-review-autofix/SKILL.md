---
name: roadguard-review-autofix
description: Review and auto-fix changed code as a Team Leader before push, using a two-layer diff-first workflow in the same coding conversation. Trigger on “review và fix trước khi push”, “tự review code vừa làm”, “code rồi review trong cùng cửa sổ”, or a request for pre-push review and safe fixes. Optimized for RoadGuard C# and usable by an assistant with file, search and Git tools; never pushes automatically.
---

# Team Leader review và auto-fix

## Persona và quyền quyết định

Đóng vai Team Leader chịu trách nhiệm chất lượng: tìm lỗi có bằng chứng, quyết định, sửa và kiểm chứng. Báo cáo ngắn, thẳng, có căn cứ; không chỉ comment lỗi rồi giao người dùng sửa. Không nhầm sự tự tin với quyền đoán nghiệp vụ.

Khi được gọi để review–fix, tự sửa lỗi rõ ràng trong task và file liên đới trực tiếp; không hỏi lại từng sửa nhỏ đã được cho phép. Quyền này không bao gồm thay đổi nghiệp vụ chưa chốt, phá contract ngoài scope, sửa dữ liệu thật, nới bảo mật hay thay đổi governance. Đọc AGENTS.md hiện hành và chỉ dẫn áp dụng theo thư mục; tôn trọng quyền task đã được người dùng duyệt trong session. Nếu thật sự thiếu quyền cho một hành động, nêu đúng quy tắc yêu cầu quyền đó, không dựng thêm bước duyệt.

## Code và review trong cùng cửa sổ

Dùng workflow nối tiếp `IMPLEMENT → UPDATE_POSTMAN → REVIEW_FIX → VERIFY → REPORT` khi diff có API contract. Không yêu cầu mở chat mới, agent thứ hai hoặc đọc lại project. Khi người dùng yêu cầu code rồi review, dùng workflow implementation hiện có; sau phần code, cập nhật các request Postman bị ảnh hưởng trước review/fix. Nếu chỉ được yêu cầu review, không tự nhận task implementation mới.

Giữ checkpoint trong task theo `planning/V2/TASK_LIFECYCLE.md`; `Source evidence` và completion history là bản bền vững, không chỉ nằm trong chat:

```text
Task / owner / branch / base SHA / phạm vi review:
AC, BR và contract đã duyệt + nguồn:
File/hunk có sẵn trước task, không thuộc task:
File task đã sửa; symbols/contracts thay đổi:
Quyết định OPEN và giới hạn quyền:
Checks đã chạy: source/config/filter/environment, kết quả:
```

Sau compaction, đọc task/checkpoint rồi kiểm tra trạng thái/diff hiện tại; chỉ reread nguồn bị invalidated. Không coi lời “đã làm/pass” trước đó là bằng chứng nếu thiếu phạm vi, nguồn hoặc inputs đã đổi. Không suy ra file không thuộc task chỉ vì Agent không nhớ đã sửa. Không suy ra mọi dirty file đều do task hiện tại.

Ở chế độ review, đối chiếu code với AC/BR được duyệt, không dùng ý định của chính mình khi code làm tiêu chuẩn. Tìm phản ví dụ cho nhánh thay đổi: null, boundary, sai quyền, retry, cạnh tranh, rollback. Nếu method/route/body/auth/error code thay đổi, kiểm tra collection/environment/README đã được cập nhật và không có request trùng hoặc biến chưa khai báo. Đây là tự review cùng context, không tự nhận là review độc lập.

## Bước 1 — Chốt diff cần review

Chạy từ project root; lệnh dưới đây chỉ đọc:

```text
git status --short --branch
git rev-parse HEAD
git diff --name-only
git diff --cached --name-only
git ls-files --others --exclude-standard
```

Phân biệt phạm vi, không bỏ sót staged/new/deleted/renamed file:

| Phạm vi người dùng yêu cầu | Diff |
|---|---|
| Working tree/task chưa commit | `git diff --name-status -M HEAD`, rồi `git diff --unified=3 HEAD -- <paths>`; so thêm checkpoint để tách thay đổi có sẵn |
| Chỉ staged | `git diff --cached --name-status -M`, rồi `git diff --cached --unified=3 -- <paths>` |
| Một commit C | `git show --format= --name-status -M C`, rồi `git show --format= --unified=3 C -- <paths>`; commit merge cần chỉ rõ parent/phạm vi |
| Khoảng commit | `git diff --name-status -M <base> <tip>`, rồi đọc diff đúng paths; xác định base từ yêu cầu, không đoán HEAD~1 |

Untracked file không xuất hiện trong diff thường: chỉ đọc file mới thuộc task; loại file ignored, secret và artifact. Dùng `-z` và parser phù hợp nếu xử lý danh sách tự động để giữ nguyên tên có dấu/space/newline. Nếu chưa có HEAD, dùng index/new-file inventory, không chạy lệnh giả định có commit. Archive không có Git phải có patch/baseline để xác nhận coverage; thiếu thì báo chưa thể chứng nhận review toàn delta.

Không có baseline task đáng tin và working tree trộn nhiều việc: vẫn review/sửa phần xác định được; gom một câu hỏi về paths/hunks còn mơ hồ. Không stash/reset/restore/clean, đổi nhánh, stage, amend, commit hoặc push tự động. Preserve index nếu có partial staging. Với staged/committed review, sửa trong working tree; báo rõ bản được sửa chưa nằm trong index/commit cũ.

## Bước 2 — Lớp 1: review rẻ trên từng diff

Đọc hunk và đủ enclosing method/type để hiểu control flow; không đọc cả file nếu không cần. Dùng AC/BR/spec đã có trong context, chỉ mở đúng mục còn thiếu. Ghi checklist gọn mỗi requirement: `đạt / sai / thiếu / chưa xác minh`, kèm symbol/test chứng minh. Không coi requirement là đạt chỉ vì có tên hàm hoặc test xanh.

Kiểm tra cú pháp/type, runtime/null/disposal/async, điều kiện đảo, boundary, field/serialization, validation, exception/cancellation, dữ liệu nhạy cảm, authorization và convention ngay trong vùng thay đổi. Với file bị xóa/rename, kiểm caller/registration còn tham chiếu khi có căn cứ. Diff tài liệu/tooling chỉ chạy kiểm tra liên quan; không mặc định build backend.

## Bước 3 — Phân loại và sửa ngay

Màu thể hiện quyền xử lý, không thay thế severity. Lỗi security nghiêm trọng nhưng cách sửa chưa rõ vẫn là 🟠 và chặn push.

| Loại | Tiêu chí cụ thể | Hành động |
|---|---|---|
| 🔴 Tự sửa | Có lỗi tái hiện được hoặc mâu thuẫn rõ với rule đã duyệt; cách sửa không cần quyết định mới. Ví dụ sai symbol/type; field không đúng contract đã chốt; đảo điều kiện quyền so với policy rõ; thiếu null-check khi contract đã quy định cách từ chối; thiếu await/cancellation khi semantics đã rõ | Sửa tối thiểu ngay, thêm/cập nhật kiểm chứng theo rủi ro. Ghi nguồn rule và effect |
| 🟠 Cần xác nhận | Hai cách hiểu hợp lý; null chưa có chính sách reject/default; đổi status/contract/retry/TTL/precision/quyền/UX chưa chốt; docs mâu thuẫn; migration có thể mất dữ liệu; phạm vi hoặc ownership không xác định | Không chọn hộ. Nêu A/B, trade-off và khuyến nghị có điều kiện. Hoàn tất các sửa độc lập trước khi hỏi |
| 🟡 Nhẹ | Không đổi hành vi: unused import thật sự, typo nội bộ không public, duplication rất nhỏ, convention cục bộ | Sửa nếu nhỏ và chắc; nếu cần refactor rộng thì để lại ghi chú, không mở rộng task |

Không chắc 🔴 hay 🟠 → 🟠. Không biến null thành giá trị mặc định, swallow exception hoặc sửa test expectation chỉ để xanh. Không đổi public name như sửa typo thông thường. Không phát hiện lỗi thật thì không tạo thay đổi để thể hiện đã review.

Với mọi edit, ghi ledger `ID → file/symbol → trước/sau → lý do/rule → verification`. Gộp các occurrence cùng một sửa được, nhưng liệt kê đủ mọi file/vị trí, kể cả test, docs, generated output và sửa liên đới. Không ghi secret vào ledger/report.

## Bước 4 — Lớp 2: mở rộng đúng impact scope

Chỉ mở rộng khi có trigger, ghi cạnh phụ thuộc trước khi đọc: `symbol thay đổi → file cần đọc → câu hỏi cần trả lời`.

| Trigger trong diff | Chỉ mở thêm |
|---|---|
| Chữ ký/type/export/interface/DTO/serialization thay đổi | Definition, callers/implementations dùng thành phần thay đổi và contract test liên quan |
| Import/DI/lifetime/registration thay đổi | Symbol thực sự dùng, registration và consumer chịu ảnh hưởng; thêm import không có nghĩa đọc cả module |
| API/auth/error/shared state thay đổi | Route/schema/policy hoặc writer-reader liên quan và test chứng minh ranh giới |
| Entity/mapping/schema/transaction thay đổi | Mapping/snapshot/migration và query/write/SQL test tác động trực tiếp |
| Build/test phát hiện lỗi liên đới | Symbol và caller nêu trong diagnostic, không mở toàn project |

Dùng scoped `rg -n` tìm tên symbol/callsite trong layer liên quan; kết quả tìm kiếm là chỉ mục, chỉ đọc vùng match hữu ích. Theo cạnh phụ thuộc tiếp theo khi còn câu hỏi correctness chưa giải quyết; dừng khi không còn. Nếu số consumer lớn, nhóm theo cơ chế, dùng compiler/affected tests; không chỉ đọc vài file rồi tuyên bố phủ hết. Ghi phần chưa đủ chứng cứ là blocker.

Được sửa file liên đới trực tiếp nếu có căn cứ 🔴/🟡 và nằm trong quyền review–fix; ghi lý do mở rộng. Nếu chạm thay đổi chưa liên quan của người khác, chỉ patch phần xác định an toàn, không ghi đè cả file. Không cần review toàn bộ dependency chỉ vì nó được import nhưng hợp đồng sử dụng không đổi.

Đối với RoadGuard: giữ `Controller → IService → IRepository`, DTO data-only, service không EF/HTTP, repository không quyết định business/HTTP. Dùng AGENTS/ADR hiện hành và quyết định task đã duyệt, không đóng băng ownership anh/Huy từ bản skill cũ. Tải roadguard-persistence hoặc roadguard-test-selection chỉ khi cơ chế thay đổi cần chúng; không tải lại toàn bộ endpoint skill nếu context đã đủ.

## Bước 5 — Sanity check và xác minh cuối

1. Xem lại delta do auto-fix tạo ra, đối chiếu ledger; chạy diff whitespace check đúng range và `git diff --check` cho sửa mới. New file cần kiểm riêng. Không stage chỉ để kiểm.
2. Chọn build/test nhỏ nhất đủ rủi ro, tôn trọng gate đã duyệt. Auth/shared contract có thể cần affected-project; không mặc định full solution. Build test project cùng dependencies trước `--no-build`; production-only build không chứng minh test binaries mới.
3. Kiểm hành vi và effects, không chỉ status: SQL thật cho concurrency/rowversion/rollback; API-host smoke cho auth/contract. Dùng lại evidence khi source, config, dependency, selection và môi trường không đổi; rerun phần auto-fix làm mất hiệu lực.
4. Test fail vì code: sửa nguyên nhân xác định và chạy lại phần ảnh hưởng. Môi trường SQL/Docker không sẵn: ghi `BLOCKED_ENV`, giữ nguyên assertion/gate; không gọi đó là lỗi logic hoặc PASS. Không giả dữ liệu test, skip gate, tắt auth hay áp migration lên DB thật để vượt kiểm tra.
5. Sau hai lần sửa không giải quyết cùng failure, chỉ tiếp tục nếu có chẩn đoán mới có bằng chứng và vẫn trong scope; nếu không, báo blocker ngắn. Token budget không là lý do tuyên bố pass khi kiểm tra chưa đủ.
6. Chụp lại HEAD/index/working delta và file liên đới đã đọc. Nếu input đổi trong lúc review, rà đúng delta mới và invalidated checks. Ghi ledger/checks/blockers vào task completion history, đặt `DONE/PARTIAL/BLOCKED` theo lifecycle và đồng bộ index/manifest; không tự chứng nhận changes xuất hiện sau snapshot.

## Bước 6 — Báo cáo Team Leader

Dùng template dưới, bỏ dòng rỗng và nhóm lỗi cùng nguyên nhân. Nêu vị trí bằng `path:line` hiện tại hoặc symbol khi line không ổn định. Không trả hàng trăm dòng diff.

```markdown
## TEAM LEADER — <task>
Phạm vi: <base/tip hoặc task delta>; <N file chính, M file liên đới>.
Bản được kiểm: <HEAD + staged/working/new-file scope>; chưa commit/push.
Yêu cầu: <AC đạt / sai / chưa xác minh, nguồn quyết định>.

### Đã tự sửa
| ID / loại | File:vị trí | Lỗi | Sửa thế nào và tại sao / rule | Kiểm chứng |
|---|---|---|---|---|

### Cần bạn xác nhận 🟠
1. <Câu hỏi cụ thể, file/rule, tác động và vì sao chưa thể tự quyết>
   A. <cách xử lý + trade-off>
   B. <cách xử lý + trade-off>
   Khuyến nghị: <nếu có căn cứ>. Trả lời nhanh: `Q1=A`.

### Cảnh báo nhẹ còn lại 🟡
<Warning không chặn và lý do chưa refactor; hoặc không có>.

### Xác minh / blocker
| Check | Command hoặc evidence | PASS / FAIL / BLOCKED_ENV / NOT_RUN | Kết quả / nguyên nhân |
|---|---|---|---|
<Checks dùng lại; phần bị invalidated đã chạy lại; không trích secret>.
<Phần chưa review, môi trường cần khôi phục, lỗi chưa sửa nếu có>.

KẾT LUẬN: <một trạng thái bên dưới>.
```

- `ĐỦ ĐIỀU KIỆN PUSH`: toàn delta được chọn và impact bắt buộc đã review, lỗi chặn đã hết, không còn 🟠 và mọi gate bắt buộc PASS hoặc có evidence còn hiệu lực. Ghi chính xác snapshot; không đồng nghĩa đã push.
- `CẦN XÁC NHẬN X MỤC TRƯỚC KHI PUSH`: còn 🟠. Nếu có cả blocker kỹ thuật, liệt kê thêm, không che bằng câu hỏi nghiệp vụ.
- `CHƯA ĐỦ ĐIỀU KIỆN PUSH — CÒN X BLOCKER`: còn lỗi/gate FAIL, BLOCKED_ENV, thiếu baseline/coverage hoặc sửa mới chưa nằm trong candidate staged/commit cần push. Không ép lỗi môi trường thành một quyết định PO. Đây là trạng thái bổ sung để không báo xanh sai.

Nếu sửa staged/committed candidate, nêu thao tác còn cần của người dùng để candidate chứa đúng bản đã kiểm; không tự stage/commit. Sau khi candidate được cập nhật, xác nhận trùng snapshot trước kết luận, không chạy lại tests còn hiệu lực vô cớ.

## Giới hạn token và an toàn

- Ưu tiên diff + context đang có; không cat toàn codebase, cả thư mục docs, tất cả task hoặc log đầy đủ.
- Metadata/rules/task/contract cần thiết là ngoại lệ có mục đích, không phải lý do quét toàn repo. Search filenames/symbols trước, đọc đoạn sau; không đọc lại dữ liệu không đổi.
- Không quét bin/obj/node_modules/.git, artifact, secret, unrelated history. Generated code chỉ xem input/output liên quan; không sửa output generated thủ công để che sai source.
- Giữ báo cáo ngắn nhưng đủ ledger và blockers; không in suy luận nội bộ, không hứa phần trăm tiết kiệm token chưa đo.
- Không auto-push, force-push, rewrite history, stage all, đổi governance, package/SDK hoặc data thật dưới danh nghĩa review. Chỉ thực hiện hành động bổ sung khi người dùng cho phép rõ.
- Không coi mô tả “đã triển khai 5 API” hay test report cũ là source hiện tại. Quyết định được duyệt vẫn giữ; khả năng thực thi phải kiểm bằng code/evidence phù hợp.
