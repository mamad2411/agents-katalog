---
name: flow-execute
description: Dùng khi có plan ở trạng thái APPROVED và tới lúc bắt tay làm, khi quay lại làm tiếp sau phiên mới hoặc sau khi ngữ cảnh bị nén, hoặc ngay trước khi commit, push, mở PR trong repo có `.flow/`. Người dùng hay nói "bắt đầu đi", "làm theo plan", "code đi", "làm tiếp", "chạy hết task".
---

# flow-execute — thi hành

Plan `APPROVED` thì tự đi hết danh sách task tới mức `autonomy.level`. Ngoài sáu điểm dừng dưới, không dừng để hỏi "làm tiếp không", vì người dùng đã duyệt cả danh sách.

| `autonomy.level` | Được làm tới |
|---|---|
| `local` | Commit trên nhánh cục bộ |
| `pr` | Push nhánh và mở PR |
| `merge` | Merge khi mọi cổng xanh, trừ phần thuộc `branches.ownerOnly` |

## Sáu điểm dừng phải hỏi

1. Sắp ghi lên nhánh được bảo vệ.
2. Việc tiếp theo vượt mức tự chủ.
3. Thao tác không đảo ngược trên môi trường dùng chung.
4. Cần trình duyệt tương tác trên môi trường thật.
5. Plan sai phạm vi, hoặc review chặn lặp lại.
6. Sắp vi phạm một luật critical.

## Pre-flight

Một lần ở đầu, chạy lệnh thật, không suy từ plan:

- `flow where`, nhánh hiện tại, cây làm việc sạch
- `flow plan status <slug> EXECUTING`
- `flow gates --changed --print execute`
- `flow verify` để có mốc trước khi sửa

Cây đang dùng chung với phiên khác thì sang skill `flow-worktree`.

## Vòng mỗi task

1. `flow task next <slug>`
2. Tìm trước khi viết: `flow dup find "<ý đồ>"`, grep. Gặp lỗi import thì sửa import, không tạo lại module.
3. Viết test, chạy thấy đỏ đúng lý do. Chi tiết ở skill `flow-test`.
4. Viết mã vừa đủ.
5. Chạy test thấy xanh.
6. Có helper mới: `flow task note <slug> "formatDueDate ở loan/format.ts" --kind helper`, để task sau và subagent khác tìm được.
7. `git add <tệp cụ thể>`. Không `git add -A`, vì sẽ cuốn theo thứ của người khác.
8. `flow check --staged`
9. `flow commitmsg --message "…"`
10. Commit theo `commit.*` của profile.
11. `flow task done <slug> <Tn> --commit <sha>`
12. Định kỳ, sau vài task hoặc sau task rủi ro: review độc lập bằng skill `flow-review`.

Công cụ cản trở hay tài liệu sai thì ghi ngay, không để trôi:

```
flow task note <slug> "…" --kind friction
```

Không sửa công cụ kiểm để qua. `check` đỏ thì sửa mã, hoặc hỏi người dùng nếu nghĩ công cụ sai.

## Phiên mới hoặc sau khi nén

`flow where`, rồi `flow task next <slug>`. Đó là đủ để tiếp tục. Không dựa vào trí nhớ về trạng thái; plan và git mới là nguồn đúng.

## Subagent song song

- Mỗi subagent một worktree, dùng skill `flow-worktree`.
- Giao đúng phạm vi: task nào, tệp nào, helper nào đã có, luật nào áp dụng.
- Sau mỗi đợt chạy `flow dup check --base <nhánh gốc>`, vì các subagent không nhìn thấy nhau và dễ viết trùng.
- Kết quả của subagent phải được kiểm lại bằng lệnh, không chỉ đọc báo cáo.

## Hết task

Chuyển sang skill `flow-post`. Chưa qua bước đó thì chưa được nói xong.
