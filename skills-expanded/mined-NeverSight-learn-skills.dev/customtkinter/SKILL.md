---
name: customtkinter
description: Build GUI apps with CustomTkinter widgets (CTk, CTkButton, CTkEntry, CTkFrame, CTkTabview, etc.), themes, appearance mode, and packaging. Use when the user requests Python GUI, CustomTkinter, CTk, or modern desktop interface with tkinter.
---

# CustomTkinter

## Quick Start

```python
import customtkinter

app = customtkinter.CTk()
app.geometry("600x500")
app.title("My App")
# thêm widgets...
app.mainloop()
```

Cài đặt: `pip install customtkinter`

## Quy tắc chung

1. **Dùng CTk() thay vì Tk()** – Theme chỉ áp dụng khi dùng CTk. Không dùng `tkinter.Tk()`.
2. **Một instance CTk duy nhất** – Chỉ một cửa sổ chính, gọi `.mainloop()` một lần.
3. **Cửa sổ phụ** – Dùng `CTkToplevel(master)`. Không gọi mainloop cho toplevel.
4. **Layout** – Dùng `pack()`, `grid()`, hoặc `place()` như tkinter chuẩn.

## Cấu trúc app với class

```python
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x500")
        self.title("My App")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # thêm widgets...

app = App()
app.mainloop()
```

## Màu sắc

- **Single color**: `fg_color="red"` hoặc `fg_color="#FF0000"`
- **Tuple (light, dark)**: `fg_color=("#DB3E39", "#821D1A")` – tự chọn theo appearance mode

## Theme và Appearance

```python
# Trước khi tạo CTk()
customtkinter.set_appearance_mode("system")  # "dark" | "light" | "system"
customtkinter.set_default_color_theme("blue")  # "blue" | "green" | "dark-blue" | "path/to.json"
```

## Toplevel – tránh mở trùng cửa sổ

```python
def open_toplevel(self):
    if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
        self.toplevel_window = ToplevelWindow(self)
    else:
        self.toplevel_window.focus()
```

## Tài liệu bổ sung

- Chi tiết API widgets, windows, colors, packaging: [reference.md](reference.md)
- Mẫu code: app cơ bản, form, tabview, scrollable frame, dialog: [examples.md](examples.md)
