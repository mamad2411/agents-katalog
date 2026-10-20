---
name: revit-xaml-styles
description: "Chuẩn hóa XAML styles cho Revit Add-In WPF — Theme.xaml + ThemeDark/ThemeLight với DynamicResource (switch runtime). Bao gồm bảng màu match Revit UI, typography Segoe UI, Buttons (Primary/Secondary/Icon/Danger), TextBoxes (Standard/Number/Search), Cards, Spacing tokens (4/8/16/24/32). TRIGGER when: viết/sửa file .xaml, task chứa 'style', 'theme', 'color', 'button style', 'dark mode', 'wpf style', hoặc cần copy ResourceDictionary templates. Khi bắt đầu project mới cần Theme.xaml, hoặc khi viết/sửa style XAML trong add-in. Keywords: xaml, wpf, style, theme, resourcedictionary, dark, light, dynamicresource."
user-invocable: true
when_to_use: "Khi bắt đầu project mới cần Theme.xaml, hoặc khi viết/sửa style XAML trong add-in."
category: revit
keywords: [xaml, wpf, style, theme, resourcedictionary, dark, light, dynamicresource]
metadata:
  author: hoang
  version: "1.0.0"
---

<!-- portable-host-contract:start -->
## Portable host contract

This skill is shared by Codex and Google Antigravity.

- Use the host's native task tracker. In Codex, use `update_plan`; in Antigravity, maintain the task-list artifact.
- Use native collaboration and user-input tools exposed by the host. Treat legacy tool names as capability descriptions, never literal calls.
- Resolve bundled resources from the project-local `.agents/skills/` tree. Do not create or write a user-global skill directory.
<!-- portable-host-contract:end -->

# Revit XAML Styles — Theme.xaml Standard

Bộ chuẩn ResourceDictionary cho mọi add-in WPF — đảm bảo UI nhất quán + switch dark/light runtime.

## Cấu trúc Resources/Themes/

```
Resources/Themes/
├── Theme.xaml              ← Master, merge tất cả
├── ThemeDark.xaml          ← Color tokens dark
├── ThemeLight.xaml         ← Color tokens light
├── Typography.xaml         ← Font + TextBlock styles
├── Spacing.xaml            ← Thickness tokens (4/8/16/24/32)
├── Buttons.xaml            ← Primary/Secondary/Icon/Danger buttons
├── TextBoxes.xaml          ← Standard/Number/Search textboxes
└── Controls.xaml           ← Card/Separator/Badge/Tag
```

## Master Theme.xaml

```xml
<ResourceDictionary
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
    <ResourceDictionary.MergedDictionaries>
        <!-- Default theme = Dark (match Revit 2024+) -->
        <ResourceDictionary Source="ThemeDark.xaml" x:Key="ColorTheme"/>
        <ResourceDictionary Source="Typography.xaml"/>
        <ResourceDictionary Source="Spacing.xaml"/>
        <ResourceDictionary Source="Buttons.xaml"/>
        <ResourceDictionary Source="TextBoxes.xaml"/>
        <ResourceDictionary Source="Controls.xaml"/>
    </ResourceDictionary.MergedDictionaries>
</ResourceDictionary>
```

## Switch theme runtime

`Services/ThemeService.cs`:

```csharp
public sealed class ThemeService : IThemeService
{
    private const string ThemeKey = "ColorTheme";

    public void Apply(AppTheme theme)
    {
        var uri = theme switch
        {
            AppTheme.Dark  => new Uri("pabs://application:,,,/MyAddIn;component/Resources/Themes/ThemeDark.xaml"),
            AppTheme.Light => new Uri("pabs://application:,,,/MyAddIn;component/Resources/Themes/ThemeLight.xaml"),
            _              => throw new ArgumentOutOfRangeException(nameof(theme))
        };

        var dict = new ResourceDictionary { Source = uri };
        var merged = Application.Current.Resources.MergedDictionaries;

        // Tìm + replace ColorTheme dictionary
        for (var i = 0; i < merged.Count; i++)
        {
            if (merged[i].Source?.OriginalString.Contains("Theme") == true &&
                (merged[i].Source.OriginalString.Contains("Dark") || merged[i].Source.OriginalString.Contains("Light")))
            {
                merged[i] = dict;
                return;
            }
        }
        merged.Add(dict);
    }
}

public enum AppTheme { Dark, Light }
```

Mọi style dùng `{DynamicResource ...}` → tự refresh khi swap.

## Naming convention

| Loại | Pattern | Ví dụ |
|---|---|---|
| Color key | `Color.<Semantic>` | `Color.Background`, `Color.Foreground.Primary`, `Color.Accent` |
| Brush key | `Brush.<Semantic>` | `Brush.Background`, `Brush.Border` |
| Spacing | `Spacing.<Size>` hoặc `Spacing.<Size><Direction>` | `Spacing.Small` (4), `Spacing.Medium` (8), `Spacing.MediumVertical` |
| Font size | `Font.Size.<Role>` | `Font.Size.Body` (14), `Font.Size.Heading` (20) |
| Style key | `<Element><Variant>` PascalCase | `PrimaryButton`, `SecondaryButton`, `SearchTextBox`, `Card` |
| Implicit style | KHÔNG dùng (tránh đụng Revit UI gốc) | ❌ `<Style TargetType="Button">` không có `x:Key` |

## Spacing tokens (multiples of 4)

| Token | Value | Khi dùng |
|---|---|---|
| `Spacing.XSmall` | 4 | Gap giữa icon + text trong button |
| `Spacing.Small` | 8 | Padding TextBox, button |
| `Spacing.Medium` | 16 | Margin giữa control trong panel |
| `Spacing.Large` | 24 | Padding Window content |
| `Spacing.XLarge` | 32 | Section separator |

Mỗi token có 4 variant: `Spacing.Medium`, `Spacing.MediumHorizontal` (= `16,0`), `Spacing.MediumVertical` (= `0,16`), `Spacing.MediumTop` (= `0,16,0,0`).

## Typography tokens

| Token | Size | Weight | Khi dùng |
|---|---|---|---|
| `Font.Size.Caption` | 11 | Normal | Helper text, footnote |
| `Font.Size.Body` | 14 | Normal | Default body text |
| `Font.Size.BodyStrong` | 14 | SemiBold | Label, emphasis |
| `Font.Size.Subheading` | 16 | SemiBold | Sub-section header |
| `Font.Size.Heading` | 20 | SemiBold | Section header |
| `Font.Size.Title` | 28 | Bold | Window title (nếu cần) |

Font family: `Segoe UI` (Windows native, match Revit UI).

## Style catalog

### Buttons

| x:Key | Use case |
|---|---|
| `PrimaryButton` | Main CTA (Save, Run, Generate) — accent color |
| `SecondaryButton` | Cancel, Close, secondary action |
| `IconButton` | Icon-only (16×16 / 24×24), no border |
| `DangerButton` | Delete, Reset — red accent |
| `LinkButton` | Text-only, hyperlink style |

### TextBoxes

| x:Key | Use case |
|---|---|
| `StandardTextBox` | Default input |
| `NumberTextBox` | Numeric only (validate trong ViewModel) |
| `SearchTextBox` | Search icon prefix + placeholder |
| `PasswordBox` | Inherits PasswordBox style |

### Other controls

| x:Key | Use case |
|---|---|
| `Card` | Border + padding + background — group content |
| `Separator` | Horizontal/vertical divider |
| `Badge` | Pill nhỏ hiển thị count/status |
| `Tag` | Inline label color-coded |

## Reference files

Sample XAML đầy đủ trong `references/styles/`:
- `references/styles/theme-dark-sample.md` — Dark theme palette
- `references/styles/theme-light-sample.md` — Light theme palette
- `references/styles/controls-sample.md` — Button styles full
- `references/styles/controls-sample.md` — TextBox styles full
- `references/styles/spacing-typography-sample.md` — Spacing + Typography

## Quy tắc tuyệt đối

| ✅ DO | ❌ DON'T |
|---|---|
| `{DynamicResource Brush.Background}` | `{StaticResource ...}` cho color/brush |
| `Background="{DynamicResource Brush.Surface}"` | `Background="#1E1E1E"` hardcode |
| `Padding="{DynamicResource Spacing.Medium}"` | `Padding="14,9,11,8"` random |
| `FontSize="{DynamicResource Font.Size.Body}"` | `FontSize="13"` random |
| Style có `x:Key` explicit | Implicit `<Style TargetType="Button">` toàn cục |
| Theme switch via `ThemeService` | Recreate Window để đổi theme |
| Test cả 2 theme trước commit | Chỉ test dark, ignore light |

## Workflow integration

Khi `cook` implement UI mới:
1. Đọc `Resources/Themes/` xem Theme.xaml đã có chưa.
2. Nếu chưa → tạo theo template ở `references/styles/`.
3. Mọi `<Window>`, `<UserControl>` mới phải merge `Theme.xaml` ở root.
4. Code review chebs: grep `StaticResource`, `#[0-9A-F]{6}`, hardcoded `FontSize`, `Margin="\d+,\d+`.
