---
name: syncfusion-winforms-banner-text-provider
description: Guide for implementing Syncfusion WinForms BannerTextProvider (watermark text provider) control. Use this when working with watermark text, placeholder text, or hint text in editor controls. Covers setup, text modes (FocusMode/EditMode), color/font customization, and supported control types in Windows Forms applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion WinForms BannerTextProvider

## When to Use This Skill

Use this skill when:
- **User needs watermark/placeholder text** - Displaying hint text in empty editor controls
- **Implementing BannerTextProvider** - Adding banner text to TextBoxExt, ComboBoxAdv, CurrencyTextBox, or other editor controls
- **Customizing banner appearance** - Setting text color, font, visibility modes
- **Configuring text display modes** - Choosing between FocusMode (disappear on focus) or EditMode (disappear on input)
- **Supporting multiple editor controls** - Applying banner text across various Syncfusion or Microsoft controls
- **User mentions:** watermark, placeholder text, hint text, banner text, BannerTextProvider, BannerTextInfo

## Component Overview

The **BannerTextProvider** is an extender control that displays watermark text in editor controls. It provides visual hints when controls are empty and automatically hides the text when users interact with the control.

**Key Features:**
- **Text Modes:** FocusMode and EditMode for controlling when banner text disappears
- **Customization:** Text color, font, and visibility control
- **Multi-Control Support:** Works with 14+ editor controls (TextBoxExt, ComboBoxAdv, CurrencyTextBox, etc.)
- **Designer & Code Support:** Add via Form designer or programmatically

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Assembly deployment and NuGet installation
- Adding BannerTextProvider via Form Designer
- Adding BannerTextProvider via Code
- Assigning banner text to controls
- Basic BannerTextInfo setup

### Banner Text Configuration
📄 **Read:** [references/banner-text-configuration.md](references/banner-text-configuration.md)
- Text property and visibility control
- Setting text color (BannerTextInfo.Color)
- Customizing font (BannerTextInfo.Font)
- Mode property: FocusMode vs EditMode
- Complete configuration examples

### Supported Controls
📄 **Read:** [references/supported-controls.md](references/supported-controls.md)
- Complete list of 14+ supported controls
- Control categories (Editors, Menu, Ribbon, Toolbar)
- Compatibility matrix
- Best practices per control type
- Limitations and workarounds

### Practical Examples
📄 **Read:** [references/practical-examples.md](references/practical-examples.md)
- Complete end-to-end code examples
- Designer-based implementation walkthrough
- Code-based implementation patterns
- Multiple controls with different settings
- Dynamic banner text changes at runtime

### Customization and Tips
📄 **Read:** [references/customization-and-tips.md](references/customization-and-tips.md)
- Advanced styling techniques
- Performance optimization
- Common pitfalls and troubleshooting
- Edge cases and best practices
- Accessibility considerations

## Quick Start Example

```csharp
// 1. Create BannerTextProvider (usually in Form designer or Form_Load)
BannerTextProvider bannerTextProvider = new BannerTextProvider(this.components);

// 2. Create TextBoxExt control
TextBoxExt textBox = new TextBoxExt()
{
    Size = new System.Drawing.Size(200, 30),
    Location = new System.Drawing.Point(20, 20)
};
this.Controls.Add(textBox);

// 3. Set banner text
BannerTextInfo bannerInfo = new BannerTextInfo()
{
    Text = "Enter your name...",
    Visible = true,
    Font = new System.Drawing.Font("Verdana", 9, System.Drawing.FontStyle.Italic),
    Color = System.Drawing.Color.Gray,
    Mode = BannerTextMode.EditMode  // Disappears when user types
};

bannerTextProvider.SetBannerText(textBox, bannerInfo);
```

## Common Patterns

### Pattern 1: Simple Placeholder Text
When you need basic hint text that disappears on user input:
```csharp
bannerTextProvider.SetBannerText(textBox, 
    new BannerTextInfo("Type here...", true));
```

### Pattern 2: Styled Watermark (EditMode)
For a more prominent watermark that only hides when content is added:
```csharp
var bannerInfo = new BannerTextInfo(
    Text = "Email address",
    Visible = true,
    Font = new Font("Verdana", 8.25f, FontStyle.Italic),
    Color = Color.RoyalBlue,
    Mode = BannerTextMode.EditMode
);
bannerTextProvider.SetBannerText(emailTextBox, bannerInfo);
```

### Pattern 3: Focus-Based Banner (FocusMode)
For temporary hints that disappear when control receives focus:
```csharp
var bannerInfo = new BannerTextInfo(
    Text = "Click to edit",
    Visible = true,
    Color = Color.LightGray,
    Mode = BannerTextMode.FocusMode  // Disappears on focus
);
bannerTextProvider.SetBannerText(textBox, bannerInfo);
```

### Pattern 4: Multi-Control Setup
Apply banner text to multiple editor controls efficiently:
```csharp
var controls = new[] { nameTextBox, emailTextBox, phoneTextBox };
var placeholders = new[] { "Full Name", "Email Address", "Phone Number" };

for (int i = 0; i < controls.Length; i++)
{
    bannerTextProvider.SetBannerText(controls[i],
        new BannerTextInfo(placeholders[i], true));
}
```

## Key Modes Explained

| Mode | Behavior | Best For |
|------|----------|----------|
| **FocusMode** | Banner text disappears when control receives focus | Quick hint text, temporary guidance |
| **EditMode** | Banner text disappears only when control contains text | Persistent watermarks, clear differentiation |

**Note:** Clear the control's default Text property before setting banner text for optimal results.

## Important Considerations

⚠️ **Clear default text:** Always clear the `Text` property of the control before setting banner text
⚠️ **Supported controls only:** BannerTextProvider works with 14+ specific controls (see supported-controls.md)
⚠️ **Assembly reference:** Requires `Syncfusion.Shared.Base` assembly
⚠️ **EditMode best practice:** Use EditMode when you need the banner to persist until the user enters text

---

**Next steps:** Start with [Getting Started](references/getting-started.md) to set up the component, then refer to other guides based on your specific needs.
