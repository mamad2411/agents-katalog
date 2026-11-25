---
name: flow-worktree
description: Dùng khi có từ hai luồng việc trở lên trên cùng một repo — nhiều phiên agent, nhiều subagent độc lập, sửa gấp giữa lúc đang làm dở, đo một ref khác mà không động vào cây hiện tại, hoặc khi cây làm việc đang bị phiên khác dùng. Người dùng hay nói "chạy song song", "tách ra làm riêng", "làm cùng lúc mấy việc", "worktree".
---

# flow-worktree — việc song song

Một việc song song một worktree, vì hai tiến trình chung một cây làm việc sẽ ghi đè nhau mà không ai báo lỗi.

## Lệnh

```
flow wt new <slug> --repo <repo> --base <ref>
flow wt list
flow wt context <slug>
flow wt done <slug>
```

- `wt new`: tạo worktree và nhánh, mang theo tệp ngữ cảnh cục bộ, vì git bỏ qua chúng nên chúng không tự sang.
- `wt context`: xem trước tệp ngữ cảnh nào sẽ chép về cây chính, tệp nào xung đột.
- `wt done`: đóng worktree. Chỉ dùng `--force` khi người dùng đồng ý.

## Điều `wt done` đảm bảo

- Đối chiếu ba chiều ngữ cảnh: bản gốc lúc tách, bản trong worktree, bản ở cây chính. Chỉ một bên đổi thì lấy bên đó.
- Không ghi đè khi cả hai bên cùng đổi, mà để lại cho bạn xử lý.
- Gỡ link trước khi xoá, vì xoá cưỡng bức có thể đi xuyên link và xoá nội dung thật ở cây gốc.

## Trong worktree

- `cd` bằng đường dẫn tuyệt đối, và kiểm `pwd`, vì lệnh chạy nhầm cây sẽ sửa nhầm việc.
- Cài phụ thuộc riêng. Link phụ thuộc từ cây khác làm phép đo sai, vì mã chạy với phiên bản không phải của nhánh này.
- Tắt consumer nền khi dùng chung CSDL, nếu không nó sẽ lấy mất thông điệp của cây kia.
- Điều phối số migration với các nhánh song song, vì hai migration cùng số sẽ va nhau lúc merge.
- Dev server đang chạy có thể phục vụ từ cây khác. Xác nhận thư mục của tiến trình trước khi tin kết quả.
- Kiểm nhánh trước mỗi commit: `git branch --show-current`.

## Subagent

- Mỗi subagent một worktree, phạm vi rõ.
- Không để hai subagent cùng sửa một tệp. Cần sửa chung thì xếp tuần tự.
- Sau mỗi đợt, `flow dup check --base <nhánh gốc>` như ở skill `flow-execute`.

## Khi buộc phải chung cây

- Commit sớm, commit nhỏ, để việc của mình không bị cuốn vào thay đổi của người khác.
- Ghi mốc `git rev-parse HEAD` trước khi bắt đầu, để biết phần nào là của mình.
- `git add` đúng tệp của mình, không dùng `-A`.
- `git status` có thể báo sai do stat cache khi có tiến trình khác đang ghi. Đừng stash hay revert thứ không phải của mình.
- Đo baseline bằng worktree riêng thay vì checkout đè lên cây đang làm:

```
flow wt new baseline --base <ref>
```
