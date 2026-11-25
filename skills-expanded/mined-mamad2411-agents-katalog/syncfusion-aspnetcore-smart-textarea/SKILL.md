---
name: syncfusion-aspnetcore-smart-textarea
description: Implement the Syncfusion ASP.NET Core Smart TextArea for AI-powered inline or popup text autocompletion. Covers OpenAI, Azure OpenAI, Ollama, and custom IChatInferenceService backends, plus UserRole, UserPhrases, and suggestion display mode customization.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion ASP.NET Core Smart TextArea

## Overview

The Smart TextArea is an intelligent, AI-powered text input control that provides real-time sentence completion and text suggestions using semantic understanding. This skill guides you through implementing Smart TextArea functionality in ASP.NET Core applications with support for multiple AI providers, customizable suggestion modes, and extensible inference backends.

The Smart TextArea provides:
- **AI-Powered Completions:** Intelligent sentence and text suggestions using OpenAI, Azure OpenAI, Ollama, or custom backends
- **Multiple Suggestion Modes:** Inline pop-up or integrated display options for AI suggestions
- **User Role Configuration:** Role-based suggestion behavior (student, writer, developer, etc.)
- **Custom Phrases:** Predefined phrase suggestions based on user context and preferences
- **Full TextArea Features:** Floating labels, validation, RTL support, accessibility compliance
- **Tag Helper Support:** Native ASP.NET Core TagHelper integration for Razor Pages and MVC
- **Event System:** Suggestion selection, value change, focus, and blur events

## When to Use This Skill

Use this skill when you need to:
- Implement AI-powered text completion in ASP.NET Core applications
- Configure OpenAI or Azure OpenAI for Smart TextArea functionality
- Set up Ollama or custom AI inference services
- Customize suggestion display modes (inline vs popup)
- Configure user roles and custom phrases for context-aware suggestions
- Implement custom inference backends for proprietary AI models
- Add intelligent text authoring features to multi-line text inputs
- Integrate Smart TextArea into forms and content editors

## Component Overview

**Key Features:**
- Real-time AI sentence completion suggestions
- Inline and popup suggestion display modes
- Role-based suggestion intelligence (Student, Writer, Developer, Custom)
- Predefined custom phrases and snippets
- Full TextArea control feature inheritance
- Support for multiple languages and RTL layouts
- Event-driven suggestion handling
- Accessibility and keyboard navigation support

**Common Properties:**
- `Placeholder` - Default hint text
- `Value` - Current textarea content
- `OpenAIKey` / `AzureEndpoint` / `OllamaUrl` - AI service configuration
- `SuggestionMode` - 'Inline' or 'Popup' suggestion display
- `UserRole` - Role context (Student, Writer, Developer, Custom)
- `UserPhrases` - Custom phrase suggestions
- `ActionComplete` - Event when suggestion is applied
- `Change` - Event when content changes
- `Rows` / `Cols` - Textarea dimensions
- `ReadOnly` - Read-only state

## Documentation Navigation

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Prerequisites and system requirements
- Installing Syncfusion.EJ2.AspNet.Core NuGet package
- Configuring AI services (OpenAI, Azure OpenAI, Ollama)
- Project setup with Razor Pages and MVC
- Tag helper registration and configuration
- CDN stylesheet and script setup
- Creating your first Smart TextArea implementation
- Basic form integration with AI completions

### Features and Capabilities
📄 **Read:** [references/features.md](references/features.md)
- Core Smart TextArea features and properties
- Standard TextArea feature inheritance (floating labels, validation)
- User role configuration (Student, Writer, Developer, Custom)
- Suggestion display and interaction patterns
- Event handling and callbacks
- Multi-language and RTL support
- Accessibility features and keyboard navigation
- Form submission and value management

### Customization
📄 **Read:** [references/customization.md](references/customization.md)
- Suggestion display mode configuration (inline vs popup)
- User role and context configuration
- Custom phrases and snippet configuration
- TextArea appearance and styling options
- Placeholder text and label customization
- Size and dimension configuration
- Event handling and completion callbacks
- Theme and CSS class customization

### Custom Inference Backend
📄 **Read:** [custom-inference-backend](https://ej2.syncfusion.com/aspnetcore/documentation/smart-textarea/custom-inference-backend)
- IChatInferenceService interface implementation
- Custom AI provider integration
- Service registration in dependency injection
- Request/response format specifications
- Expected completion format and response structure
- Handling complex inference scenarios
- Testing and debugging custom backends
- Performance optimization strategies
