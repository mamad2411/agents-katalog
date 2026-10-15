---
name: syncfusion-winui-ai-assistview
description: Guide for implementing the Syncfusion WinUI AI AssistView control for creating AI chat interfaces and conversational UI. Use this skill when implementing AI chat interfaces, AI assistants, conversational UI, or chatbots in WinUI applications. Essential for creating AI-powered chat experiences, integrating AI services, displaying AI responses, showing typing indicators, providing AI suggestions, or implementing conversational interfaces with AI services in WinUI.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing WinUI AI AssistView

## When to Use This Skill

Use this skill when the user needs to:
- Create an AI chat interface or conversational UI
- Implement an AI assistant or chatbot
- Integrate with AI services (OpenAI, Azure AI, etc.)
- Display AI-generated responses with formatting
- Show typing indicators during AI processing
- Provide AI-driven suggestions for quick responses
- Add custom toolbars for chat actions (copy, regenerate, like/dislike)
- Allow users to stop long-running AI responses
- Build customer support bots or help systems
- Create intelligent conversational applications

**Always apply this skill when the user mentions:** AI chat, AI assistant, chatbot, conversational UI, AI responses, chat interface, AI integration, typing indicator, AI suggestions, or AI-powered conversations in WinUI applications.

## Component Overview

**SfAIAssistView** is a Syncfusion WinUI control that provides a comprehensive AI chat interface for building intelligent and responsive applications with AI services. It offers a user-friendly conversational UI with built-in support for suggestions, typing indicators, response toolbars, and customizable appearance.

**Namespace:** `Syncfusion.UI.Xaml.Chat`  
**NuGet Package:** `Syncfusion.Chat.WinUI`  
**Platform:** WinUI 3 Desktop (.NET 5+, Windows App SDK 1.0+)

**Key Advantage:** Provides a complete AI chat experience out-of-the-box with built-in toolbars, suggestions, typing indicators, and stop responding features—no need to build a chat UI from scratch.

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and NuGet package setup (Syncfusion.Chat.WinUI)
- Namespace imports (Syncfusion.UI.Xaml.Chat)
- Basic SfAIAssistView initialization
- CurrentUser and Messages properties
- Creating ViewModel with TextMessage and Author classes
- First complete AI chat example
- License registration

### AI Suggestions
📄 **Read:** [references/suggestions.md](references/suggestions.md)
- Suggestions property for AI-driven suggestions
- Displaying quick response options
- Bottom-right corner positioning
- Dynamic suggestion updates
- Handling suggestion selection
- Use cases for expediting conversation flow

### Response Toolbar
📄 **Read:** [references/response-toolbar.md](references/response-toolbar.md)
- Built-in toolbar items (Copy, Regenerate, Like, Dislike)
- ResponseToolbarItem class and properties
- Custom toolbar items with ItemTemplate
- IsResponseToolbarVisible property
- ResponseToolbarItemClicked event
- Customizing toolbar appearance
- Adding custom actions to responses

### Input Toolbar
📄 **Read:** [references/input-toolbar.md](references/input-toolbar.md)
- InputToolbarItem class for custom input actions
- Adding toolbar items to text input area
- InputToolbarPosition (Left, Right)
- IsInputToolbarVisible property
- InputToolbarItemClicked event
- InputToolbarHeaderTemplate for file uploads
- Custom input area actions

### Typing Indicator and Stop Responding
📄 **Read:** [references/typing-and-stop-responding.md](references/typing-and-stop-responding.md)
- TypingIndicator property for AI processing feedback
- ShowTypingIndicator boolean property
- Real-time feedback during AI response generation
- EnableStopResponding property
- StopResponding event and command
- StopRespondingTemplate customization
- Canceling ongoing AI responses

### Theming and Events
📄 **Read:** [references/theming-and-events.md](references/theming-and-events.md)
- RequestedTheme property (Dark, Light themes)
- Theme support in App.xaml
- PromptRequest event
- InputMessage and Handled properties
- Validating user input before processing
- Custom actions on prompt submission
- Theme customization

## Quick Start Example

```xaml
<Page
    xmlns:syncfusion="using:Syncfusion.UI.Xaml.Chat">
    <Grid>
        <syncfusion:SfAIAssistView 
            x:Name="aiAssistView"
            CurrentUser="{Binding CurrentUser}"
            Messages="{Binding Chats}"
            Suggestions="{Binding Suggestions}"
            ShowTypingIndicator="{Binding IsProcessing}"
            TypingIndicator="{Binding TypingIndicator}"/>
    </Grid>
</Page>
```

```csharp
using Syncfusion.UI.Xaml.Chat;
using System.Collections.ObjectModel;

public class ViewModel : INotifyPropertyChanged
{
    private ObservableCollection<object> chats;
    private Author currentUser;
    private IEnumerable<string> suggestions;
    private TypingIndicator typingIndicator;
    private bool isProcessing;

    public ViewModel()
    {
        this.CurrentUser = new Author { Name = "User" };
        this.Chats = new ObservableCollection<object>();
        this.TypingIndicator = new TypingIndicator { Author = new Author { Name = "AI" } };
        this.Suggestions = new ObservableCollection<string>();
        InitializeChat();
    }

    private async void InitializeChat()
    {
        // User asks a question
        this.Chats.Add(new TextMessage 
        { 
            Author = CurrentUser, 
            Text = "What is WinUI?" 
        });
        
        // Show typing indicator
        IsProcessing = true;
        await Task.Delay(1000);
        
        // AI responds
        IsProcessing = false;
        this.Chats.Add(new TextMessage 
        { 
            Author = new Author { Name = "AI" }, 
            Text = "WinUI is a user interface layer that contains modern controls and styles for building Windows apps." 
        });
        
        // Update suggestions
        Suggestions = new ObservableCollection<string> 
        { 
            "What is the future of WinUI?", 
            "What is XAML?", 
            "What is the difference between WinUI 2 and WinUI 3?" 
        };
    }

    public ObservableCollection<object> Chats
    {
        get => chats;
        set { chats = value; RaisePropertyChanged(nameof(Chats)); }
    }

    public Author CurrentUser
    {
        get => currentUser;
        set { currentUser = value; RaisePropertyChanged(nameof(CurrentUser)); }
    }

    public IEnumerable<string> Suggestions
    {
        get => suggestions;
        set { suggestions = value; RaisePropertyChanged(nameof(Suggestions)); }
    }

    public TypingIndicator TypingIndicator
    {
        get => typingIndicator;
        set { typingIndicator = value; RaisePropertyChanged(nameof(TypingIndicator)); }
    }

    public bool IsProcessing
    {
        get => isProcessing;
        set { isProcessing = value; RaisePropertyChanged(nameof(IsProcessing)); }
    }

    public event PropertyChangedEventHandler PropertyChanged;
    private void RaisePropertyChanged(string propertyName) =>
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
}
```

## Common Patterns

### 1. Basic AI Chat with Messages
```xaml
<syncfusion:SfAIAssistView 
    CurrentUser="{Binding CurrentUser}"
    Messages="{Binding Chats}"/>
```

```csharp
public class ViewModel
{
    public Author CurrentUser { get; set; } = new Author { Name = "John" };
    public ObservableCollection<object> Chats { get; set; } = new();

    public ViewModel()
    {
        Chats.Add(new TextMessage { Author = CurrentUser, Text = "Hello!" });
        Chats.Add(new TextMessage { Author = new Author { Name = "Bot" }, Text = "Hi! How can I help you?" });
    }
}
```

**When to use:** Simple AI chat without suggestions or typing indicators.

### 2. AI Chat with Typing Indicator
```xaml
<syncfusion:SfAIAssistView 
    CurrentUser="{Binding CurrentUser}"
    Messages="{Binding Chats}"
    ShowTypingIndicator="{Binding IsAIProcessing}"
    TypingIndicator="{Binding TypingIndicator}"/>
```

```csharp
private async void SendMessageToAI(string userMessage)
{
    Chats.Add(new TextMessage { Author = CurrentUser, Text = userMessage });
    
    // Show typing indicator
    IsAIProcessing = true;
    
    // Call AI service
    var aiResponse = await CallAIService(userMessage);
    
    // Hide typing indicator and show response
    IsAIProcessing = false;
    Chats.Add(new TextMessage { Author = new Author { Name = "AI" }, Text = aiResponse });
}
```

**When to use:** Show real-time feedback while AI generates responses.

### 3. AI Suggestions for Quick Responses
```xaml
<syncfusion:SfAIAssistView 
    CurrentUser="{Binding CurrentUser}"
    Messages="{Binding Chats}"
    Suggestions="{Binding CurrentSuggestions}"/>
```

```csharp
private void UpdateSuggestions(string lastAIResponse)
{
    // Generate contextual suggestions based on AI response
    CurrentSuggestions = new ObservableCollection<string>
    {
        "Tell me more",
        "Show me an example",
        "What are the alternatives?"
    };
}
```

**When to use:** Expedite conversation flow with contextual quick responses.

### 4. Custom Response Toolbar with Actions
```xaml
<syncfusion:SfAIAssistView 
    CurrentUser="{Binding CurrentUser}"
    Messages="{Binding Chats}"
    IsResponseToolbarVisible="True"
    ResponseToolbarItemClicked="ResponseToolbar_ItemClicked"/>
```

```csharp
private void ResponseToolbar_ItemClicked(object sender, ResponseToolbarItemClickedEventArgs e)
{
    switch (e.Item.ItemType)
    {
        case ResponseToolbarItemType.Copy:
            CopyToClipboard(e.Message.Text);
            break;
        case ResponseToolbarItemType.Regenerate:
            RegenerateAIResponse(e.Message);
            break;
        case ResponseToolbarItemType.Like:
            SendFeedback("like", e.Message);
            break;
        case ResponseToolbarItemType.Dislike:
            SendFeedback("dislike", e.Message);
            break;
    }
}
```

**When to use:** Allow users to interact with AI responses (copy, regenerate, rate).

### 5. Custom Input Toolbar with File Upload
```xaml
<syncfusion:SfAIAssistView IsInputToolbarVisible="True">
    <syncfusion:SfAIAssistView.InputToolbarItems>
        <syncfusion:InputToolbarItem Tooltip="Attach file">
            <syncfusion:InputToolbarItem.ItemTemplate>
                <DataTemplate><Button Click="AttachFile_Click"><SymbolIcon Symbol="Attach"/></Button></DataTemplate>
            </syncfusion:InputToolbarItem.ItemTemplate>
        </syncfusion:InputToolbarItem>
    </syncfusion:SfAIAssistView.InputToolbarItems>
</syncfusion:SfAIAssistView>
```

**When to use:** Allow users to attach files to AI prompts. See [input-toolbar.md](references/input-toolbar.md) for full implementation.

### 6. Stop Responding Feature for Long AI Responses
```xaml
<syncfusion:SfAIAssistView 
    CurrentUser="{Binding CurrentUser}"
    Messages="{Binding Chats}"
    EnableStopResponding="True"
    StopResponding="StopResponding_Event"/>
```

```csharp
private CancellationTokenSource aiCancellationToken;

private async void SendToAI(string prompt)
{
    aiCancellationToken = new CancellationTokenSource();
    
    try
    {
        var response = await CallAIServiceAsync(prompt, aiCancellationToken.Token);
        Chats.Add(new TextMessage { Author = new Author { Name = "AI" }, Text = response });
    }
    catch (OperationCanceledException)
    {
        Chats.Add(new TextMessage { Author = new Author { Name = "AI" }, Text = "Response canceled." });
    }
}

private void StopResponding_Event(object sender, EventArgs e)
{
    aiCancellationToken?.Cancel();
}
```

**When to use:** Allow users to cancel long-running AI responses.

### 7. PromptRequest Event for Input Validation
```csharp
private void PromptRequest_Event(object sender, PromptRequestEventArgs e)
{
    if (string.IsNullOrWhiteSpace(e.InputMessage.Text))
    {
        e.Handled = true;
        ShowError("Please enter a message.");
    }
}
```

**When to use:** Validate or preprocess user input before AI processing.

### 8. OpenAI Integration Pattern
```csharp
private async Task<string> CallOpenAI(string prompt)
{
    var client = new OpenAIClient(apiKey);
    var response = await client.CompleteChatAsync("gpt-4", new ChatCompletionOptions
    {
        Messages = { new SystemChatMessage("You are a helpful assistant."), new UserChatMessage(prompt) }
    });
    return response.Value.Content[0].Text;
}
```

**When to use:** Integrate with OpenAI GPT models. See [theming-and-events.md](references/theming-and-events.md) for theme configuration.

## Key Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `Messages` | ObservableCollection&lt;object&gt; | null | Collection of chat messages (TextMessage objects). |
| `CurrentUser` | Author | null | Current user author information. Required to distinguish user messages from AI responses. |
| `Suggestions` | IEnumerable&lt;string&gt; | null | AI-driven suggestions displayed in bottom-right corner for quick responses. |
| `ShowTypingIndicator` | bool | false | Shows/hides typing indicator during AI processing. |
| `TypingIndicator` | TypingIndicator | null | Typing indicator configuration (author, text). |
| `IsResponseToolbarVisible` | bool | true | Shows/hides response toolbar (Copy, Regenerate, Like, Dislike). |
| `ResponseToolbarItems` | ObservableCollection&lt;ResponseToolbarItem&gt; | Built-in items | Custom toolbar items for response actions. |
| `IsInputToolbarVisible` | bool | false | Shows/hides input toolbar in text input area. |
| `InputToolbarItems` | ObservableCollection&lt;InputToolbarItem&gt; | null | Custom toolbar items for input area (e.g., attach file). |
| `InputToolbarPosition` | ToolbarPosition | Right | Position of input toolbar (Left or Right). |
| `InputToolbarHeaderTemplate` | DataTemplate | null | Custom template for input area header (e.g., file upload info). |
| `EnableStopResponding` | bool | false | Enables stop responding button to cancel ongoing AI responses. |
| `StopRespondingTemplate` | DataTemplate | null | Custom template for stop responding button. |
| `StopRespondingCommand` | ICommand | null | Command executed when stop responding button is clicked. |
| `RequestedTheme` | ElementTheme | Default | Theme for the control (Light, Dark, or Default). Set in App.xaml. |

## Key Events

| Event | Description |
|-------|-------------|
| `PromptRequest` | Fired when user submits a prompt. Provides InputMessage and Handled properties. |
| `ResponseToolbarItemClicked` | Fired when response toolbar item is clicked. Provides item details. |
| `InputToolbarItemClicked` | Fired when input toolbar item is clicked. Provides item details. |
| `StopResponding` | Fired when stop responding button is clicked. Use to cancel AI operations. |

## Common Use Cases

### AI Chatbots and Assistants
- Customer support chatbots
- Virtual assistants
- Help desk automation
- FAQ bots
- Product recommendation assistants

**Best Approach:** Use Messages for conversation history, Suggestions for common queries, typing indicator for feedback.

### AI-Powered Development Tools
- Code generation assistants
- Documentation generators
- Code review bots
- Debugging assistants

**Best Approach:** Enable response toolbar for copying code, regenerating responses. Use input toolbar for file/code uploads.

### Educational AI Tutors
- Interactive learning assistants
- Homework help bots
- Language learning tutors
- Subject-specific tutors

**Best Approach:** Use suggestions for learning paths, response toolbar for rating answers, typing indicator for engagement.

### Content Generation
- Writing assistants
- Email drafters
- Social media content creators
- Marketing copy generators

**Best Approach:** Enable copy/regenerate in response toolbar, use suggestions for content variations.

### Data Analysis and Insights
- Business intelligence assistants
- Data query interfaces
- Report generation bots
- Analytics helpers

**Best Approach:** Use input toolbar for data uploads, stop responding for long queries, response toolbar for export actions.

## Implementation Tips

1. **Message Management:** Use ObservableCollection for Messages to automatically update UI when adding/removing messages.

2. **Typing Indicator:** Show during async AI calls, hide when response arrives. Bind to ViewModel boolean property.

3. **Suggestions:** Update dynamically based on conversation context. Clear after user selects or after few exchanges.

4. **Error Handling:** Use PromptRequest event to validate input. Catch AI service errors gracefully.

5. **Performance:** For long conversations, consider implementing message pagination or limiting visible message count.

6. **AI Service Integration:** Use async/await for AI service calls. Implement cancellation tokens with stop responding feature.

7. **Response Toolbar:** Default items (Copy, Regenerate, Like, Dislike) work automatically. Handle ResponseToolbarItemClicked for custom logic.

8. **Input Toolbar:** Use for frequently needed actions like file upload, voice input, or emoji picker.

9. **Theme Support:** Set RequestedTheme in App.xaml for app-wide theme. Control auto-adapts to light/dark mode.

10. **Accessibility:** Set Author.Name for screen readers. Ensure sufficient contrast in custom templates.

## Related Documentation

- **Getting Started:** See [references/getting-started.md](references/getting-started.md) for setup and basic usage
- **Suggestions:** See [references/suggestions.md](references/suggestions.md) for AI-driven quick responses
- **Response Toolbar:** See [references/response-toolbar.md](references/response-toolbar.md) for response actions
- **Input Toolbar:** See [references/input-toolbar.md](references/input-toolbar.md) for input area customization
- **Typing & Stop:** See [references/typing-and-stop-responding.md](references/typing-and-stop-responding.md) for indicators and cancellation
- **Theming & Events:** See [references/theming-and-events.md](references/theming-and-events.md) for themes and events
