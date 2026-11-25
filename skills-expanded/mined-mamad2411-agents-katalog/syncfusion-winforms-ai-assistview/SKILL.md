---
name: syncfusion-winforms-ai-assistview
description: "Guide for implementing Syncfusion Windows Forms AI AssistView (SfAIAssistView) for building conversational AI interfaces in desktop applications. Use this when creating chat interfaces, AI assistants, or chatbots with Windows Forms. Supports OpenAI and Azure OpenAI integration, typing indicators, chat suggestions, message bubbles, and custom views for interactive messaging experiences."
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing AI AssistView

The Syncfusion Windows Forms AI AssistView (SfAIAssistView) is a sophisticated conversational interface control for building AI-powered chat applications with support for suggestions, typing indicators, custom views, and seamless OpenAI/ChatGPT integration.

## When to Use This Skill

Use this skill when the user needs to:
- Build AI-powered chat interfaces in Windows Forms applications
- Integrate OpenAI, ChatGPT, or Azure OpenAI services into desktop apps
- Create conversational UI with message bubbles and chat history
- Display AI-driven response suggestions for quick user responses
- Show typing indicators during async AI response generation
- Customize chat message appearance with custom BotView and UserView
- Handle user prompts with validation and custom actions
- Build intelligent assistants with banner customization
- Implement real-time chat experiences with data binding

## Component Overview

**Key Features:**
- **Suggestions**: Display selectable response suggestions to expedite conversation flow
- **Typing Indicator**: Show loading animation during AI processing
- **Banner Customization**: Customizable header with welcome messages and AI service info
- **Custom Views**: Create custom BotView and UserView for message presentation
- **Theme Support**: Automatic light/dark theme adaptation
- **OpenAI Integration**: Seamless connection with OpenAI services via Semantic Kernel
- **Events**: PromptRequest event for input validation and custom actions
- **Data Binding**: Full support for ObservableCollection and INotifyPropertyChanged

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Assembly deployment and NuGet packages
- Creating Windows Forms project with SfAIAssistView
- Adding control via Designer and Code
- Creating ViewModel with message collection
- Message binding and Author configuration
- Basic chat implementation

### Suggestions
📄 **Read:** [references/suggestions.md](references/suggestions.md)
- Displaying AI-driven suggestions
- Binding suggestions to ViewModel
- Quick response scenarios
- Dynamic suggestion updates

### Typing Indicator
📄 **Read:** [references/typing-indicator.md](references/typing-indicator.md)
- ShowTypingIndicator property
- Async communication feedback
- Customizing indicator appearance
- Author and DisplayText configuration

### Customization
📄 **Read:** [references/customization.md](references/customization.md)
- BannerView customization with SetBannerView
- Creating custom BotView with SetBotView
- Creating custom UserView with SetUserView
- Interactive buttons in bot responses
- Custom styling and layouts

### Events
📄 **Read:** [references/events.md](references/events.md)
- PromptRequest event handling
- Input validation
- Custom action triggers
- Handled property usage

### OpenAI Integration
📄 **Read:** [references/openai-integration.md](references/openai-integration.md)
- Connecting to OpenAI/ChatGPT
- Microsoft Semantic Kernel setup
- API credentials configuration
- NonStreamingChat implementation
- Async response handling
- Complete working example

## Quick Start Example

### Basic Chat Interface

```csharp
using Syncfusion.WinForms.AIAssistView;
using System.ComponentModel;
using System.Collections.ObjectModel;

namespace AIAssistViewDemo
{
    public partial class Form1 : Form
    {
        ViewModel viewModel;
        
        public Form1()
        {
            InitializeComponent();
            viewModel = new ViewModel();
            
            // Create AI AssistView
            SfAIAssistView sfAIAssistView1 = new SfAIAssistView();
            sfAIAssistView1.Dock = DockStyle.Fill;
            this.Controls.Add(sfAIAssistView1);
            
            // Bind messages
            sfAIAssistView1.DataBindings.Add("Messages", viewModel, "Chats", 
                true, DataSourceUpdateMode.OnPropertyChanged);
        }
    }
    
    // ViewModel
    public class ViewModel : INotifyPropertyChanged
    {
        private ObservableCollection<object> chats;
        private Author currentUser;
        
        public ViewModel()
        {
            this.Chats = new ObservableCollection<object>();
            this.CurrentUser = new Author { Name = "John" };
            this.GenerateMessages();
        }
        
        private async void GenerateMessages()
        {
            // User message
            this.Chats.Add(new TextMessage 
            { 
                Author = CurrentUser, 
                Text = "What is Windows Forms?" 
            });
            
            await Task.Delay(1000);
            
            // Bot response
            this.Chats.Add(new TextMessage 
            { 
                Author = new Author { Name = "Bot" }, 
                Text = "Windows Forms is a GUI framework for building Windows desktop applications." 
            });
        }
        
        public ObservableCollection<object> Chats
        {
            get => this.chats;
            set
            {
                this.chats = value;
                RaisePropertyChanged("Chats");
            }
        }
        
        public Author CurrentUser
        {
            get => this.currentUser;
            set
            {
                this.currentUser = value;
                RaisePropertyChanged("CurrentUser");
            }
        }
        
        public event PropertyChangedEventHandler PropertyChanged;
        
        public void RaisePropertyChanged(string propName)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propName));
        }
    }
}
```

## Common Patterns

### Pattern 1: Chat with Suggestions

```csharp
// In ViewModel
private IEnumerable<string> suggestion;

public IEnumerable<string> Suggestion
{
    get => this.suggestion;
    set
    {
        this.suggestion = value;
        RaisePropertyChanged("Suggestion");
    }
}

// Set suggestions after bot response
Suggestion = new ObservableCollection<string> 
{ 
    "Tell me more", 
    "What are alternatives?" 
};

// In Form
sfAIAssistView1.DataBindings.Add("Suggestions", viewModel, "Suggestion", 
    true, DataSourceUpdateMode.OnPropertyChanged);
```

### Pattern 2: Typing Indicator During AI Processing

```csharp
// In ViewModel
private bool showTypingIndicator;

public bool ShowTypingIndicator
{
    get => this.showTypingIndicator;
    set
    {
        this.showTypingIndicator = value;
        RaisePropertyChanged("ShowTypingIndicator");
    }
}

// Usage
ShowTypingIndicator = true;
var response = await GetAIResponse(userMessage);
Chats.Add(new TextMessage { Author = botAuthor, Text = response });
ShowTypingIndicator = false;

// In Form
sfAIAssistView1.DataBindings.Add("ShowTypingIndicator", viewModel, 
    "ShowTypingIndicator", true, DataSourceUpdateMode.OnPropertyChanged);
    
sfAIAssistView1.TypingIndicator.Author = new Author 
{ 
    Name = "Bot", 
    AvatarImage = Image.FromFile(@"Assets\bot.png") 
};
sfAIAssistView1.TypingIndicator.DisplayText = "Typing";
```

### Pattern 3: Custom Banner

```csharp
BannerStyle customStyle = new BannerStyle
{
    TitleFont = new Font("Segoe UI", 14F, FontStyle.Bold),
    SubTitleFont = new Font("Segoe UI", 12F, FontStyle.Italic),
    ImageSize = AvatarSize.Medium,
    SubTitleColor = Color.Gray,
    TitleColor = Color.DarkBlue
};

string title = "AI Assistant";
string subTitle = "Powered by OpenAI";
sfAIAssistView1.SetBannerView(title, subTitle, 
    Image.FromFile(@"Assets\ai-icon.png"), customStyle);
```

### Pattern 4: Prompt Validation

```csharp
sfAIAssistView1.PromptRequest += (sender, e) =>
{
    var message = e.Message as TextMessage;
    if (message == null) return;
    
    // Validate input
    if (string.IsNullOrWhiteSpace(message.Text))
    {
        e.Handled = true; // Prevent adding to messages
        MessageBox.Show("Please enter a message.");
        return;
    }
    
    // Custom processing
    LogUserInput(message.Text);
};
```

## Key Properties and Methods

| Property/Method | Type | Description |
|-----------------|------|-------------|
| `Messages` | ObservableCollection<object> | Chat message collection |
| `Suggestions` | IEnumerable<string> | Response suggestion items |
| `ShowTypingIndicator` | bool | Shows/hides typing indicator |
| `TypingIndicator` | TypingIndicator | Typing indicator configuration |
| `User` | Author | Current user information |
| `SetBannerView()` | Method | Customize banner appearance |
| `SetBotView()` | Method | Set custom bot message view |
| `SetUserView()` | Method | Set custom user message view |
| `PromptRequest` | Event | Fires when user submits prompt |

## Common Use Cases

### Use Case 1: Customer Support Chatbot
Build an AI-powered customer support interface with suggestion chips for common questions and typing indicators during response generation.

### Use Case 2: Virtual Assistant
Create an intelligent desktop assistant with custom branded banner, personalized bot responses, and OpenAI integration for natural conversations.

### Use Case 3: Interactive Documentation
Implement a conversational documentation browser where users ask questions about software features and receive AI-generated explanations.

### Use Case 4: Training Simulator
Build interactive training applications where AI guides users through procedures with step-by-step conversational instructions.

## Installation

```powershell
Install-Package Syncfusion.SfAIAssistView.WinForms
```

For OpenAI integration:
```powershell
Install-Package Microsoft.SemanticKernel
```

## Troubleshooting

**Messages not displaying:**
- Verify data binding is set correctly
- Ensure ObservableCollection is used (not List<T>)
- Check that RaisePropertyChanged is called on collection updates

**Typing indicator not showing:**
- Set `ShowTypingIndicator = true` before async operation
- Configure `TypingIndicator.Author` property
- Ensure binding is established for ShowTypingIndicator

**Suggestions not appearing:**
- Bind Suggestions property to ViewModel
- Use IEnumerable<string> type
- Update suggestions after bot responses

**OpenAI connection issues:**
- Verify API key is valid and not expired
- Check API endpoint URL is correct
- Ensure Microsoft.SemanticKernel NuGet is installed
- Confirm network connectivity