---
name: syncfusion-winforms-card-layout
description: Implement stack-based card layout management in Windows Forms applications using Syncfusion CardLayout to organize controls as visible cards, navigate between cards, and configure layout modes for wizard controls and property pages.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing CardLayout in Windows Forms

## When to Use This Skill

Use this skill when you need to:
- Create a stack-based card layout that displays one card (control) at a time
- Build wizard-style interfaces with sequential card navigation
- Implement property pages with card switching
- Organize multiple panels or controls as cards within a container
- Navigate programmatically between different views or screens

## Component Overview

`CardLayout` is a layout manager that organizes controls in a stack-of-cards appearance. Each control added to the layout becomes a "card," and only one card is visible at a time. The container acts as a stack of cards, with the first component added being initially visible. Cards can be configured with custom names, images, and sizing behavior.

**Key Capabilities:**
- Set unique names for each card
- Navigate between cards (First, Next, Previous, Last)
- Configure layout modes (Default or Fill)
- Maintain aspect ratio for child controls
- Get/set selected card by name or index

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Assembly and NuGet package installation
- Adding CardLayout via designer or code
- Creating and configuring container panel
- Adding child controls as cards
- Basic card navigation with Next/Previous methods

### Configuring CardLayout
📄 **Read:** [references/configuring-cardlayout.md](references/configuring-cardlayout.md)
- Setting custom card names with SetCardName
- Getting card names and components
- Working with card indices (NextCardIndex, PreviousCardIndex)
- Aspect ratio maintenance (MaintainAspectRatio)
- Layout modes: Default vs Fill
- Setting preferred and minimum sizes

### Card Navigation
📄 **Read:** [references/card-navigation.md](references/card-navigation.md)
- Selecting cards by name using SelectedCard property
- Navigation methods: First(), Next(), Previous(), Last()
- Using SmartTag in designer for card selection
- Code-based navigation with buttons
- ComboBox integration for card selection
- Runtime card switching

### Child Controls Configuration
📄 **Read:** [references/child-controls.md](references/child-controls.md)
- Adding child controls as cards to the layout
- Image settings for cards
- PreferredSize and MinimumSize configuration
- Container and child control setup
- Styling child controls

## Quick Start Example

```csharp
using Syncfusion.Windows.Forms.Tools;
using System.Windows.Forms;

public class CardLayoutForm : Form
{
    private CardLayout cardLayout1;
    private Panel cardLayoutPanel;
    private Panel card1;
    private Panel card2;

    public CardLayoutForm()
    {
        // Initialize CardLayout
        cardLayout1 = new CardLayout();
        cardLayoutPanel = new Panel();
        cardLayoutPanel.BackColor = Color.White;
        cardLayoutPanel.Dock = DockStyle.Fill;

        // Set container
        cardLayout1.ContainerControl = cardLayoutPanel;

        // Create cards (panels)
        card1 = new Panel();
        card1.BackColor = Color.LightBlue;
        card1.Controls.Add(new Label { Text = "Card 1", AutoSize = true });

        card2 = new Panel();
        card2.BackColor = Color.LightGreen;
        card2.Controls.Add(new Label { Text = "Card 2", AutoSize = true });

        // Add cards to the main panel
        cardLayoutPanel.Controls.Add(card1);
        cardLayoutPanel.Controls.Add(card2);

        // Set card names
        cardLayout1.SetCardName(card1, "FirstCard");
        cardLayout1.SetCardName(card2, "SecondCard");

        // Navigate between cards
        cardLayout1.SelectedCard = "FirstCard";
        cardLayout1.Next(); // Display SecondCard

        // Add to form
        this.Controls.Add(cardLayoutPanel);
    }
}
```

## Common Patterns

### Pattern 1: Wizard Interface
Create sequential steps where users navigate forward/backward through cards:
```csharp
private void NextButton_Click(object sender, EventArgs e)
{
    this.cardLayout1.Next();
}

private void PreviousButton_Click(object sender, EventArgs e)
{
    this.cardLayout1.Previous();
}
```

### Pattern 2: Dropdown Card Selection
Allow users to select cards from a dropdown list:
```csharp
private void CardSelectionComboBox_SelectedIndexChanged(object sender, EventArgs e)
{
    string selectedCardName = CardSelectionComboBox.SelectedItem.ToString();
    this.cardLayout1.SelectedCard = selectedCardName;
}
```

### Pattern 3: Fill Container
Make cards stretch to fill the entire container:
```csharp
this.cardLayout1.LayoutMode = CardLayoutMode.Fill;
```

## Key Properties

| Property | Type | Description |
|----------|------|-------------|
| `SelectedCard` | string | Gets/sets the current visible card by name |
| `LayoutMode` | CardLayoutMode | Gets/sets layout mode (Default or Fill) |
| `NextCardIndex` | int | Returns the index of the next card |
| `PreviousCardIndex` | int | Returns the index of the previous card |
| `ContainerControl` | Control | Gets/sets the container for the layout |

## Key Methods

| Method | Purpose |
|--------|---------|
| `First()` | Display the first card |
| `Next()` | Display the next card |
| `Previous()` | Display the previous card |
| `Last()` | Display the last card |
| `SetCardName(Control, string)` | Assign a custom name to a card |
| `GetCardName(Control)` | Get the name of a card |
| `GetCardNames()` | Get all card names as array |
| `GetComponentFromName(string)` | Get control by card name |
| `SetMaintainAspectRatio(Control, bool)` | Configure aspect ratio maintenance |
