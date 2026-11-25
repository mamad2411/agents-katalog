---
name: flow-sync
description: Dùng khi quay lại một repo có `.flow/` sau thời gian không đụng tới, sau khi kéo về nhiều thay đổi của người khác, hoặc khi `flow doctor` hay `flow context stale` cảnh báo tài liệu đã cũ. Người dùng hay nói "cập nhật tài liệu theo mã", "đồng bộ lại", "tài liệu còn đúng không", "vừa pull nhiều lắm", "sync".
---

# flow-sync — đồng bộ ngữ cảnh

## Xem cái gì lệch

```
flow sync
flow context stale
flow doctor
```

`sync` cho biết module nào đổi kể từ mốc đồng bộ. Repo chưa có mốc: đọc ngữ cảnh hiện có và kiểm với mã trước.

## Với từng module

1. Đọc diff từ mốc: `git diff <mốc>..HEAD -- <module>`.
2. Sửa `CONTEXT.md` đúng phần lệch, không viết lại cả tệp. Cập nhật `tệp:dòng` đã dời.
3. Thiếu `CONTEXT.md` thì sinh bằng skill `flow-context`.
4. Soát lại luật có scope liên quan: `flow rules find --path <module>`. Luật còn đúng không, cách kiểm còn chạy không.
5. Hợp đồng đổi thì cập nhật `.flow/contracts.md`.

Thấy điều mới đáng ghi thì dùng skill `flow-learn`.

## Đặt mốc

```
flow sync --mark
```

Chỉ chạy sau khi soát xong, vì mốc là lời khẳng định rằng ngữ cảnh đã khớp mã tại đây. Đặt mốc khi chưa soát thì những lần sync sau sẽ bỏ sót phần lệch.

Chưa soát hết thì không đặt mốc, báo lại phần còn lại.

## Báo cáo

```
Mốc:             <từ đâu tới đâu>
Module đã soát:  <danh sách>
Đã sửa:          <tệp, phần nào>
Đã sinh:         <tệp mới>
Luật đổi:        <id, sửa gì>
Hợp đồng đổi:    <gì>
Chưa soát:       <module, vì sao>
Mốc mới:         <đã đặt hay chưa>
```
