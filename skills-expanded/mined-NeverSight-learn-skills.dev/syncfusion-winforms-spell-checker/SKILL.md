---
name: syncfusion-winforms-spell-checker
description: Implement spell checking capabilities in Windows Forms applications using Syncfusion SpellCheckerAdv. Use this skill whenever the user needs to add spell checking to text controls, configure dictionaries, set up context menu suggestions, customize ignore options, or retrieve spelling suggestions. This skill covers attaching the control to RichTextBox/TextBox, managing multiple language dictionaries, enabling real-time context menus, and handling misspelled word suggestions.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion Windows Forms SpellChecker

The SpellCheckerAdv control provides Microsoft Office-style spell checking capabilities for Windows Forms text controls. This skill guides you through installation, control attachment, dictionary configuration, context menu integration, and customization options.

## When to Use This Skill

Use this skill when you need to:
- Add spell checking to RichTextBox or TextBox controls
- Configure dictionary sources (built-in English or custom dictionaries)
- Set up context menu-driven spell checking
- Customize ignore rules for special content (emails, URLs, numbers)
- Retrieve spelling suggestions and alternatives
- Support multiple languages via different dictionary formats

## Documentation Navigation

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and assembly references
- Adding control via designer or code
- Configuring SpellCheckerAdv with text controls
- Invoking spell check operations
- Basic implementation patterns

### Dictionary Configuration
📄 **Read:** [references/dictionary-setup.md](references/dictionary-setup.md)
- Setting up default English dictionary
- Adding Hunspell dictionaries for multiple languages
- Adding Ispell dictionaries
- Adding OpenOffice dictionaries
- Switching cultures at runtime
- Custom dictionary support

### Context Menu Integration
📄 **Read:** [references/context-menu-integration.md](references/context-menu-integration.md)
- Implementing ISpellCheckerAdvEditorTools interface
- Creating TextBoxSpellEditor wrapper class
- Setting up runtime context menus
- User-driven spell checking workflow
- Adding to dictionary from context menu

### Customization & Suggestions
📄 **Read:** [references/customization-suggestions.md](references/customization-suggestions.md)
- Ignore options (emails, URLs, mixed case, special symbols)
- Retrieving suggestion lists
- Phonetic word alternatives
- Anagram suggestions
- Custom word management

## Quick Start Example

**Basic Spell Check Setup:**

```csharp
using Syncfusion.Windows.Forms.Tools;

// 1. Create SpellCheckerAdv control
SpellCheckerAdv spellCheckerAdv = new SpellCheckerAdv();

// 2. Set dictionary path
spellCheckerAdv.DictionaryPath = "Syncfusion_en_us.dic";

// 3. Attach to RichTextBox and trigger spell check
RichTextBox richTextBox = new RichTextBox();
spellCheckerAdv.SpellCheck(new SpellCheckerAdvEditorWrapper(richTextBox));
```

**Context Menu Spell Checking:**

```csharp
// Implement ISpellCheckerAdvEditorTools
class TextBoxSpellEditor : ISpellCheckerAdvEditorTools
{
    private TextBoxBase textBox;
    
    public TextBoxSpellEditor(Control control)
    {
        Control = control;
    }
    
    public Control Control 
    { 
        get { return textBox; }
        set { textBox = value as TextBoxBase; }
    }
    
    public string Text
    {
        get { return textBox.Text; }
        set { textBox.Text = value; }
    }
    
    public string CurrentWord { get; set; }
    
    public void SelectText(int start, int length)
    {
        textBox.Select(start, length);
    }
}

// Enable context menu spell checking
TextBoxSpellEditor editor = new TextBoxSpellEditor(richTextBox);
spellCheckerAdv.PerformSpellCheckUsingContextMenu(editor);
```

## Common Implementation Patterns

### Pattern 1: Dialog-Based Spell Checking
User clicks a "Spell Check" button → SpellCheckerAdv dialog opens → User reviews and corrects misspelled words → Dialog closes.

```csharp
private void buttonSpellCheck_Click(object sender, EventArgs e)
{
    spellCheckerAdv.SpellCheck(new SpellCheckerAdvEditorWrapper(richTextBox));
}
```

### Pattern 2: Real-Time Context Menu
User right-clicks misspelled word → Context menu appears with suggestions → User selects correction or adds to dictionary.

```csharp
TextBoxSpellEditor editor = new TextBoxSpellEditor(richTextBox);
spellCheckerAdv.PerformSpellCheckUsingContextMenu(editor);
```

### Pattern 3: Multi-Language Support
Configure multiple dictionary cultures and switch at runtime based on user preference or content language.

```csharp
SpellCheckerAdv spellChecker = new SpellCheckerAdv();
spellChecker.Dictionaries = new DictionaryCollection();

// Add English dictionary
spellChecker.Dictionaries.Add(new HunspellDictionary()
{
    Culture = new CultureInfo("en-US"),
    DictionaryPath = @"en-US.dic",
    GrammarPath = @"en-US.aff"
});

// Add French dictionary
spellChecker.Dictionaries.Add(new HunspellDictionary()
{
    Culture = new CultureInfo("fr-FR"),
    DictionaryPath = @"fr-FR.dic",
    GrammarPath = @"fr-FR.aff"
});

// Switch to French at runtime
spellChecker.Culture = new CultureInfo("fr-FR");
```

## Key Props & Methods

| Element | Purpose | When to Use |
|---------|---------|------------|
| `DictionaryPath` | Set built-in dictionary location | Simple English spell checking |
| `Dictionaries` | Add custom dictionaries (Hunspell, Ispell, OpenOffice) | Multi-language support |
| `Culture` | Set active spell-check language | Language switching |
| `SpellCheck()` | Trigger spell-check dialog | User-initiated spell checking |
| `PerformSpellCheckUsingContextMenu()` | Enable context menu suggestions | Real-time spell checking |
| `GetSuggestions()` | Retrieve correction suggestions | Programmatic spell checking |
| `IgnoreEmailAddress`, `IgnoreUrl`, etc. | Skip special content types | Customized spell checking |

## Common Use Cases

1. **Email Client**: Right-click spell checking with custom dictionaries
2. **Document Editor**: Multi-language spell checking with context menu
3. **Form Validator**: Check user input before submission
4. **Content Management**: Ignore URLs and email addresses in content
5. **Multilingual App**: Switch spell-check language based on UI culture
