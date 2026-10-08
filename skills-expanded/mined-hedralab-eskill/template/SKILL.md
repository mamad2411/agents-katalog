---
name: template-skill          # ← ĐỔI: chữ thường + gạch nối, PHẢI = tên thư mục (xem references/naming.md)
description: >               # ← ĐỔI: ≤1024 · ngôi THỨ 3 · "làm gì" + "khi nào dùng" + trigger (Cursor + agentskills)
  Does X and Y when Z. Use when the user mentions A, B, or asks to C.
  # Ví dụ Cursor: "Review code for quality. Use when reviewing PRs or code changes."
# disable-model-invocation: true   # ← Cursor: bật = chỉ khi gọi tên; OMIT = agent được tự bật từ context
# license: MIT
# compatibility:
# metadata:
#   author: <your-name>
#   version: "1.0"
---

# <Tên skill> — 1 dòng giá trị

## <Mảng 1 — theo kim chỉ nam đã chọn>

**Quy tắc:**
1. ...
2. ...

**Code mẫu:**
```python
# ví dụ ngắn chạy được
```

**Ví dụ input → output:**
```
Input: ...
Output: ...
```

**Checklist:**
- [ ] ...

## <Mảng 2>

...

## Bẫy — đừng lặp (tài sản lớn nhất của skill)

1. **Triệu chứng lỗi** — fix: ...
2. **Triệu chứng lỗi** — fix: ...

## References (nếu cần — ref 1 cấp, đường dẫn tương đối)

- `references/xxx.md` — mô tả ngắn khi nào mở file này
