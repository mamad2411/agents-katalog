---
name: flow-report
description: Dùng khi người dùng cần báo cáo công việc đã làm — cuối ngày, standup sáng, cuối tuần, báo cáo miệng với cấp trên, hoặc tự xem lại một ngày đã làm gì. Chạy được cả ở repo chưa có `.flow/`. Người dùng hay nói "báo cáo", "report", "hôm nay làm gì", "daily", "standup", "on-going done pending", "tổng kết tuần".
---

# flow-report — báo cáo công việc

Máy gom dữ liệu, bạn viết thành lời, người dùng chọn nội dung. Bước này không sửa mã, không tự gửi báo cáo đi đâu.

## Luật

- Mỗi dòng phải truy được về nguồn: commit, PR, task, tag, hoặc lời người dùng. Việc chỉ có lời người dùng thì đánh dấu là tự khai trong lúc nháp.
- Hạn hoàn thành chỉ lấy từ người dùng. Chưa có thì hỏi, họ không nêu thì không ghi hạn.
- Ghi đúng mức đã đạt, ngay sau tên việc: "đã merge", "đã vào nhánh chính", "đã gắn tag vX". "Đã QA" và "đã deploy" chỉ ghi khi người dùng xác nhận. Không viết câu ngụ ý người dùng cuối đã dùng được khi chưa có xác nhận deploy.
- Không đoán giờ làm từ commit. Giờ làm chỉ lấy khi người dùng khai.
- Tiến độ chỉ ghi bằng số đếm thật, ví dụ 3/5 task. Không tự ước phần trăm.
- Mã ticket chỉ lấy từ `tickets` hoặc lời người dùng, không tự đặt.
- Chỉ báo cáo việc của chính người dùng. Không đưa tên hay việc của đồng nghiệp từ `otherAuthors` vào báo cáo.
- Tên việc nói điều đã làm được, không chép tiêu đề commit.
- Không in bí mật. Không nhắc tên quy trình hay công cụ này trong báo cáo, trừ khi đó chính là sản phẩm được báo cáo.

## 1. Đọc dữ liệu

Chạy cho ba khoảng để có số liệu đưa vào câu hỏi. Người dùng đã nêu khoảng thì chỉ chạy khoảng đó.

```
flow report collect --json --since today
flow report collect --json --since last-workday
flow report collect --json --since week
```

Người dùng làm nhiều repo trong một workspace thì thêm `--all`. `--since` còn nhận `yesterday`, `since-last`, hoặc `YYYY-MM-DD`, có thể kèm `--until YYYY-MM-DD`. `--day-starts-at 4` tính việc làm trước 4 giờ sáng vào ngày hôm trước.

| Trường | Cách xử lý |
|---|---|
| `repos[].commits` | Việc đã viết, tính theo giờ viết và giờ máy người dùng |
| `commits[].onDefault` | Đã vào nhánh chính |
| `commits[].pushed` | `false` là chưa đẩy lên |
| `commits[].pr`, `tickets` | PR và mã ticket liên quan; `pr: null` là chưa tìm được, không phải không có |
| `repos[].releases` | Tag trên nhánh chính tạo trong khoảng |
| `repos[].worktrees`, `stashes` | Việc dở tại thời điểm chạy lệnh |
| `repos[].pullRequests` | `available: false` nghĩa là chưa biết, không phải bằng 0; nêu `reason` cho người dùng |
| `pullRequests.open[]` | PR đang mở tại thời điểm chạy; `touched: true` là có cập nhật trong khoảng; `checks` là `passing`, `failing`, `pending`, `none` |
| `reviewDecision` | `APPROVED`, `CHANGES_REQUESTED`, `REVIEW_REQUIRED`; rỗng nghĩa là repo không yêu cầu duyệt, không có nghĩa là chưa ai xem |
| `pullRequests.reviewed` | PR của người khác mà người dùng đã review |
| `repos[].otherAuthors` | Người khác, hoặc chính người dùng với danh tính khác |
| `plans` | Tiến độ, việc còn mở, quyết định chờ, ghi chú theo ngày |
| `previous` | Báo cáo gần nhất; đọc phần hẹn ngày mai để đối chiếu |
| `language` | Ngôn ngữ của dự án, `null` khi chưa có `.flow/` |
| `redacted` | Lớn hơn 0 thì báo người dùng có giá trị giống bí mật trong commit |

`window.includesNow` là `false` khi báo cáo một khoảng đã qua: bỏ `worktrees`, `stashes`, và chỉ giữ PR đang mở có `touched: true`.

## 2. Hỏi mục đích, khoảng, tiêu chí

Theo mục "Hỏi người dùng" ở skill `flow`. Đã rõ từ lời người dùng thì bỏ câu đó. Ba câu này gửi trong một lần. Câu trả lời ở đây không ghi vào plan.

| Câu | Lựa chọn |
|---|---|
| Mục đích | Báo cáo ngày, Báo cáo miệng, Tự xem lại, Standup hoặc báo cáo tuần |
| Khoảng thời gian | "Theo mục đích" (mô tả ghi khoảng của từng mục đích), Hôm nay, Từ ngày làm việc gần nhất, Tuần này. Ba mục sau ghi số commit và số PR đã merge. Ngày cụ thể thì gõ vào ô khác |
| Tiêu chí | "Dùng bộ mặc định" (mô tả ghi bộ của từng mục đích), hoặc "Tuỳ chỉnh" |

Hai khoảng có cùng số liệu, ví dụ Hôm nay và Tuần này vào thứ Hai, thì gộp thành một lựa chọn.

Lựa chọn thứ tư gộp hai mục đích vì công cụ hỏi chỉ cho 4 lựa chọn; chọn nó thì bước 4 hỏi thêm là loại nào. CLI không có giới hạn đó thì liệt kê đủ 5 mục đích.

| Mục đích | Khoảng mặc định | Bộ tiêu chí mặc định |
|---|---|---|
| Báo cáo ngày | `today` | Blocker, Ngày mai |
| Báo cáo miệng | `today` | Blocker, Rủi ro |
| Tự xem lại | `today` | Ngày mai, Việc ngoài code |
| Standup | `last-workday` | Blocker |
| Báo cáo tuần | `week` | Trạng thái chung, Tiến độ, Rủi ro, Quyết định đã chốt |

Ba nhóm On-going, Done, Pending luôn có, không đưa vào câu hỏi. Tiêu chí mặc định cần dữ liệu mà không có thì bỏ và nói rõ.

Chọn "Tuỳ chỉnh" thì hỏi tiếp tối đa 3 câu chọn nhiều. Tiêu chí cần dữ liệu chỉ hiện khi có dữ liệu.

| Câu | Tiêu chí | Điều kiện hiện |
|---|---|---|
| Công việc | Ngày mai, Việc phát sinh | Luôn hiện |
| | Tiến độ | `plans[].total` lớn hơn 0 |
| | Bằng chứng | Có commit hoặc PR |
| Vướng mắc | Blocker, Rủi ro | Luôn hiện |
| | Quyết định đã chốt | Plan có ghi chú `decision` |
| Khác | Việc ngoài code, Giờ làm, Trạng thái chung | Luôn hiện |
| | Review, hỗ trợ | `pullRequests.reviewed` có mục, hoặc không đọc được PR |

`otherAuthors` trông giống chính người dùng thì hỏi, rồi chạy lại với `--author <tên hoặc email>`.

## 3. Gom thành việc

Dùng dữ liệu của khoảng đã chọn; khoảng chưa chạy ở bước 1, như ngày người dùng gõ, thì chạy thêm. Đọc `git show --stat <hash>`, rồi `git show <hash>` với cụm chưa rõ, để hiểu mỗi việc tạo ra kết quả gì.

- Gom commit, PR, task cùng mục đích thành một việc, kể cả khi nằm ở nhiều repo hay worktree.
- Commit cùng `pr` hoặc cùng `tickets` là một việc.
- Commit phát hành và commit cấu hình phụ thì gộp vào việc chính hoặc bỏ.
- Muốn ghi tag cho một việc thì kiểm bằng `git tag --contains <hash>`, không suy từ giờ tạo tag.

## 4. Hỏi việc đưa vào và việc đã xong

Một lần gọi, tối đa 4 câu:

| Câu | Lựa chọn |
|---|---|
| Standup hay báo cáo tuần | Chỉ hỏi khi bước 2 chọn mục gộp |
| Đưa việc nào vào | "Tất cả N việc" (mặc định), "Chọn từng việc" |
| Việc nào đã xong | Chọn nhiều. Từ 3 việc trở xuống: liệt kê từng việc và "Không việc nào". Nhiều hơn: "Tất cả", "Không việc nào", "Chọn từng việc" |
| Định dạng | Chỉ cho báo cáo ngày và tuần: Văn bản thường (mặc định), Markdown, Email |

Câu "Việc nào đã xong" chỉ gồm việc chưa tự vào Done theo bước 6. Mô tả mỗi lựa chọn ghi bằng chứng: "đã vào nhánh chính", "đã gắn tag v0.3.0", "PR đang mở, CI xanh".

Chọn "Chọn từng việc" thì gửi thêm một lần gọi, mỗi câu 2 đến 4 việc, tối đa 4 câu. Còn nhiều hơn thì gộp các việc gần nhau.

## 5. Hỏi điều máy không biết

Sau các câu trên, gửi một tin nhắn thường rồi dừng chờ, vì đây là thông tin tự do chứ không phải lựa chọn. Chỉ hỏi phần áp dụng:

- Hạn hoàn thành của việc On-going.
- Việc đã QA hay deploy.
- Chi tiết blocker và rủi ro, nếu đã chọn.
- Ngày mai, Giờ làm, Việc ngoài code, Việc phát sinh, nếu đã chọn.
- Đã làm gì khác mà code không thể hiện.
- Ngôn ngữ báo cáo, nếu chưa suy ra được.

Người dùng đưa sẵn ngữ cảnh, ví dụ `/flow-report xong API thanh toán, mai QA test`: vẫn chạy bước 1, coi lời họ là nguồn chính, không hỏi lại điều đã nói. Lời kể lệch với dữ liệu thì nêu cả hai để họ quyết, ví dụ họ nói xong nhưng PR còn mở.

## 6. Xếp nhóm

| Nhóm | Điều kiện |
|---|---|
| Done | Mọi phần của việc đã merge qua PR thì tự xếp vào đây. Việc đẩy thẳng lên nhánh chính hoặc có phần chưa merge phải được người dùng xác nhận |
| On-going | Chưa xong: PR đang mở, thay đổi chưa commit, plan đang chạy, hoặc việc không được chọn là xong |
| Pending | Việc đang kẹt hoặc chưa bắt đầu, ghi nhãn lý do |

- Nhóm trống thì ghi "Không có", không bỏ nhóm.
- Việc chưa bắt đầu đã nằm ở mục Ngày mai thì không lặp ở Pending.
- Việc On-going có `checks: failing` hoặc `reviewDecision: CHANGES_REQUESTED` thì nêu ra, vì đó là lý do chưa xong.
- Blocker ghi đủ: cần gì, từ ai, chờ từ ngày nào, cần trước khi nào, trễ thì ảnh hưởng gì. Thiếu thì hỏi, không tự nghĩ ra.
- Việc phát sinh là việc không có trong plan và không có trong lời hẹn của `previous`. Không có hai nguồn đó thì hỏi người dùng, không tự gắn nhãn.
- Trạng thái chung (Đúng tiến độ, Có rủi ro, Trễ) do người dùng chọn. Có thể gợi ý kèm căn cứ.

## 7. Viết

Dùng khuôn của mục đích đã chọn trong [templates](references/templates.md).

- Tên người báo cáo: tên người dùng đã nói, không có thì `identities.names[0]`.
- Ngày tiêu đề là ngày cuối nằm trong khoảng; `window.end` là mốc không tính vào. Báo cáo khoảng đã qua thì đổi mục "Ngày mai" thành "Tiếp theo".
- Có `tickets` thì đặt mã ở đầu dòng của bản gửi nhóm, bỏ khi báo cáo miệng.
- Nguồn của từng dòng đưa trong ghi chú kèm bản nháp, không nằm trong báo cáo trừ khi chọn Bằng chứng.
- Có tag mà người dùng nói chưa deploy thì ghi rõ "chưa deploy", để tag không bị hiểu là đã phát hành.
- Báo cáo nhiều repo thì ghi tên repo đầu dòng.
- Báo cáo gửi nhóm hoặc cấp trên dùng `language.team`. Tự xem lại dùng `language.user`. Không có thì theo ngôn ngữ người dùng đang viết. Người dùng nói khác thì theo người dùng.
- Cho người dùng xem bản nháp và sửa đến khi họ ưng.
- Có `previous` thì so với điều đã hẹn; việc đã hẹn mà chưa làm thì nêu trong lúc nháp để người dùng quyết có đưa vào không.

## 8. Lưu

`saveDir` khác `null` thì lưu vào `<saveDir>/<saveStem>-<kiểu>.md`, với kiểu là `daily`, `oral`, `review`, `standup`, `weekly`, rồi báo đường dẫn. Thư mục này chỉ nằm trên máy.

`saveDir` là `null` thì chỉ đưa báo cáo ra chat, không tạo `.flow/`, không tạo tệp trong repo.

## Ca khó

- Không có commit: không viết "không làm gì". Báo khoảng, danh tính và repo đã đọc, rồi hỏi họ đã làm gì. Có thể sai khoảng hoặc sai danh tính.
- `identities.missing` là `true`: hỏi tên hoặc email rồi chạy lại với `--author`.
- `window.fallback` là `true`: chưa có báo cáo trước, nói rõ khoảng đang dùng.
- Làm qua nửa đêm: có commit sát đầu ngày thì hỏi có tính vào ngày trước không, rồi chạy lại với `--day-starts-at`.
