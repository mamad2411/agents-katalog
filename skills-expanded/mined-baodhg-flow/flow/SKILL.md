---
name: flow
description: Dùng khi sắp làm bất kỳ việc gì liên quan đến mã trong một repo có `.flow/profile.json` ở thư mục này hoặc thư mục cha — thêm tính năng, vá lỗi, refactor, soát mã, tìm hiểu hệ thống — và nạp trước khi mở mã nguồn. Cũng dùng khi người dùng nhắc "flow", "quy trình", "harness", "luật dự án", "đọc gì trước", hoặc khi có điều cần họ chốt.
---

# flow — cửa vào

## Định vị

Chạy `flow where`. Sau đó:

- Có `.flow/`: đọc theo thứ tự dưới.
- Không có `.flow/`: làm theo quy ước sẵn có của repo, không tự khởi tạo. `flow fingerprint` đọc được repo bất kỳ và không ghi gì. Người dùng muốn đưa dự án vào quy trình thì dùng skill `flow-init`.
- `flow onboard` còn điều cần chốt: hỏi người dùng trước khi sửa mã.

## Thứ tự đọc

Đủ để làm thì dừng, vì mỗi tệp đọc thừa lấy chỗ của ngữ cảnh cần về sau.

1. `.flow/PROJECT.md`
2. `.flow/services.md`
3. Luật khớp tệp sắp chạm: `flow rules find --path <tệp>`
4. Memory: `flow memory --text <từ khoá>`
5. `.flow/contracts.md`
6. `.flow/consumed/`
7. `.flow/reference/`
8. `.flow/coverage.md`
9. `CONTEXT.md` của module
10. Mã

## Cỡ task

| Cỡ | Dấu hiệu | Đường đi |
|---|---|---|
| S | Một module, vài tệp, không chạm tiền, auth, schema, hợp đồng | Sửa, rồi skill `flow-post` |
| M | Nhiều tệp hoặc nhiều module, cần chia bước | Skill `flow-explore` → `flow-plan` → `flow-execute` → `flow-post` |
| L | Nhiều repo, tiền, auth, schema, sự kiện, luật critical | Như M, thêm người dùng duyệt plan trên chat |

Post không bao giờ bỏ, kể cả với S, vì đó là nơi phép đo thật diễn ra.

## Các skill

- Vào dự án: skill `flow-init`, skill `flow-sync`
- Đường chính: skill `flow-explore`, skill `flow-plan`, skill `flow-execute`, skill `flow-post`
- Chất lượng: skill `flow-test`, skill `flow-review`, skill `flow-runbook`
- Kiến thức: skill `flow-context`, skill `flow-learn`
- Hỗ trợ: skill `flow-worktree`, skill `flow-secrets`, skill `flow-report`

## Nguyên tắc

- Kiểm bằng lệnh, không suy luận hay nhớ, vì trí nhớ không theo kịp mã.
- Tài liệu có thể cũ, mã là sự thật. Thấy lệch thì sửa tài liệu ngay, để người sau không vấp lại.
- Tái hiện lỗi trước khi sửa, nếu không sẽ không biết bản sửa có tác dụng.
- Kết quả rỗng cần phép đo đối chứng, vì lệnh sai cũng cho ra rỗng.
- Công cụ tĩnh xanh chưa chứng minh hành vi; biên dịch được không có nghĩa là chạy đúng.
- Đề phòng thất bại im lặng: `catch` rỗng, giá trị mặc định che lỗi, consumer bỏ qua thông điệp.
- Kiến thức để trong tài liệu module, luật, tên định danh, tên test; không để trong chú thích hay thân commit, vì những chỗ đó không ai tìm tới.
- Mọi luật cần có cách kiểm, luật không kiểm được sẽ mục dần.
- Không nới công cụ kiểm để qua, vì như vậy là tắt chuông báo.
- Báo cáo trung thực cả phần đỏ và phần bỏ qua, vì người đọc quyết định dựa trên đó.
- Nhánh được bảo vệ do người dùng quyết.
- Tìm mã có sẵn trước khi viết mới, vì bản thứ hai sẽ lệch khỏi bản thứ nhất.
- Không in bí mật, vì lịch sử phiên giữ lại mọi thứ đã in.
- Tiết kiệm ngữ cảnh: grep có mục tiêu, đọc đúng đoạn cần.

## Quy ước của repo

Đọc từ `.flow/profile.json`, không mang từ repo khác sang. Mỗi giá trị có nguồn ở `_sources`. Thứ tự phân giải, lớp sau thắng lớp trước:

1. Mặc định trung tính
2. Sở thích người dùng ở `~/.agent-flow/user.json`
3. Quy ước đo được và tệp chỉ dẫn của dự án (`instructions`)
4. Điều người dùng chốt

| Khoá | Áp cho |
|---|---|
| `language.code` | Tên định danh, chuỗi trong mã |
| `language.team` | Mô tả PR, tên test, tài liệu lên repo |
| `language.user` | Chat, nội dung trong `.flow/` |

| `hygiene.comments` | Nghĩa |
|---|---|
| `off` | Không kiểm chú thích |
| `no-new` | Không thêm chú thích mới, chú thích cũ để yên |
| `unit` | Đơn vị bị chạm (hàm, khai báo) phải sạch chú thích |
| `file` | Tệp bị chạm phải sạch chú thích |

Chỉ dẫn máy đọc luôn được giữ ở mọi mức: build tag, lint directive, type-check directive, migration marker, đầu tệp mã sinh, shebang. Phép thử: bỏ đi thì công cụ đổi hành vi.

## Commit & PR

- Tiêu đề nói thay đổi cho người đọc, không nói tên tệp hay tên hàm. Ví dụ: `feat: let members renew a loan once`.
- Thân theo `commit.body`, kiểu theo `commit.style`, ngôn ngữ theo `commit.language`.
- Mô tả PR ngắn, lời thường, theo template của repo nếu có, không thì `<gói>/templates/pr-description.md`.
- Không nhắc harness trong mã, commit, PR.
- Kiểm bằng `flow commitmsg --message "…"` và `flow prmsg <tệp>`.

## Hỏi người dùng

Mọi quyết định của người dùng được đưa thẳng lên chat kèm lựa chọn. Tài liệu chỉ là biên bản, vì không ai đọc câu hỏi nằm trong tệp.

- Chỉ hỏi điều thật sự thuộc quyền họ. Phần còn lại tự quyết và liệt kê mỗi việc một dòng.
- Hỏi sớm, gom một lượt.
- Mỗi câu tự đứng được, người đọc không cần mở tệp nào.
- Claude Code: dùng công cụ AskUserQuestion, tối đa 4 câu, mỗi câu 2–4 lựa chọn, khuyến nghị đặt đầu.
- CLI khác: in khối dưới rồi dừng chờ.

```
**D1 · Trả muộn có tính phí không** — `Loan` quá hạn hiện chỉ cảnh báo; tính phí sẽ đổi màn hình của `Member`.
1. Có, tính theo ngày (khuyến nghị)
2. Không, giữ cảnh báo
```

Có câu trả lời thì ghi bằng `flow plan decide <slug> <Dn> "<lựa chọn>"`. Xin duyệt plan cũng trên chat, tóm tắt tối đa 10 dòng.

## Nhắc nhanh

- Người dùng sửa cách làm: ghi ngay bằng skill `flow-learn`.
- Một việc song song một worktree: skill `flow-worktree`.
- Lệnh của repo thắng lệnh của bộ skill.
- Gọi skill: Claude Code `/flow-x`, Gemini `/flow:x`, Codex `/prompts:flow-x`.
