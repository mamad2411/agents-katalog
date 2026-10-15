---
name: syncfusion-aspnetcore-smart-paste
description: Implement the Syncfusion ASP.NET Core Smart Paste Button for AI-powered form auto-filling using clipboard data. Use this skill when configuring OpenAI/Azure OpenAI, creating form field annotations, customizing button appearance, implementing custom inference backends, or managing intelligent data mapping from clipboard to form fields.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion ASP.NET Core Smart Paste Button

## Overview

The Smart Paste Button is an intelligent, AI-powered UI control that automatically parses clipboard data and intelligently maps it to form fields using contextual understanding and semantic analysis. This skill guides you through implementing Smart Paste functionality in ASP.NET Core applications using Syncfusion components, with support for multiple AI providers and custom backends.

The Smart Paste Button provides:
- **Intelligent Data Mapping:** Contextual understanding to match clipboard data to form fields
- **Multiple AI Providers:** OpenAI, Azure OpenAI, Ollama, and custom IChatInferenceService backends
- **Form Field Annotations:** Explicit descriptions to improve AI accuracy and field intent understanding
- **Customizable Appearance:** Full Button component property inheritance for styling and theming
- **Clipboard Integration:** Automatic clipboard parsing and intelligent value distribution
- **Custom Inference Backends:** Extensible architecture for proprietary or on-premises AI services
- **Tag Helper Support:** Native ASP.NET Core TagHelper integration for Razor pages and MVC

## When to Use This Skill

Use this skill when you need to:
- Implement AI-powered form auto-filling from clipboard data
- Configure OpenAI or Azure OpenAI for Smart Paste functionality
- Set up Ollama or custom AI inference services
- Add intelligent field annotations for better AI accuracy
- Customize Smart Paste Button appearance and behavior
- Integrate Smart Paste into multi-field forms
- Implement a custom data inference backend
- Ensure proper integration with ASP.NET Core Razor Pages or MVC applications

## Component Overview

**Key Features:**
- Real-time clipboard parsing with AI interpretation
- Zero-configuration setup with default providers
- Support for structured and unstructured clipboard data
- Field annotation system for precise data mapping
- Extensible inference architecture
- Full accessibility compliance
- Theme and styling customization

**Common Properties:**
- `Content` - Button display text
- `CssClass` - CSS classes for styling
- `IconCss` - Icon class for button representation
- `Disabled` - Enable/disable state
- `EnableRtl` - Right-to-left language support

## Documentation Navigation

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Prerequisites and system requirements
- Installing Syncfusion.EJ2.AspNet.Core NuGet package
- Configuring AI services (OpenAI, Azure OpenAI, Ollama)
- Project setup with Razor Pages and MVC
- Tag helper registration
- CDN stylesheet and script configuration
- Creating your first Smart Paste implementation
- Basic form setup and Smart Paste integration

### Field Annotations
📄 **Read:** [references/annotation.md](references/annotation.md)
- Using data-smartpaste-description attribute
- Annotation best practices for improved accuracy
- Supported input types (text, textarea, select, radio, checkbox)
- Intent-based field descriptions
- Multi-language annotation strategies
- Field metadata for complex forms

### Button Customization
📄 **Read:** [references/customization.md](references/customization.md)
- Smart Paste Button appearance customization
- CSS class and icon configuration
- Inheriting Button component properties
- Styling and theming options
- Button text and label customization
- State and event handling

### Custom Inference Backend
📄 **Read:** [custom-inference-backend](https://ej2.syncfusion.com/aspnetcore/documentation/smart-paste/custom-inference-backend)
- IChatInferenceService interface implementation
- Custom AI provider integration
- Service registration in dependency injection
- Request/response format specifications
- Expected JSON structure for field mapping
- Handling complex inference scenarios
- Testing and debugging custom backends