# Repo Referensi: flutter/agent-plugins

Repo: https://github.com/flutter/agent-plugins
Ref lokal: /Users/chaali0324/.agents/repo-refs/flutter_agent-plugins
API: curl "localhost:27126/repos/readme?name=flutter_agent-plugins"
Dibuat: 2026-09-16

## Cuplikan README
# flutter/agent-plugins

Source: https://github.com/flutter/agent-plugins
Fetched: 2026-09-16

## README
# Flutter Agent Plugins

Agent plugins for Flutter, maintained by the Flutter team.

A collection of plugins designed to extend AI agent capabilities for Flutter development. These plugins bundle together skills, MCP server configuration, and rules to provide tailored workflows and instructions for happy path Flutter development. By giving the agent domain expertise and repeatable workflows, you drastically reduce mistakes and ensure agents reliably complete tasks following best practices.

Plugins can package various customizations together. A key component of these plugins is **Agent Skills**, which are simple folders of files that can be seen as complementary to MCP: where MCP gives an agent access to specialized tools, a Skill teaches the agent “how” to use tools for a specific task.

You can also install the [Dart skills](https://github.com/dart-lang/skills) for Dart tasks.

## Installation

Refer to [Get started developing with AI](https://docs.flutter.dev/ai/get-started) for detailed instructions on how to install the plugins for your preferred agent.

## Available Skills

| Skill | Description | Example prompt |
|---|---|---|
| [flutter-add-integration-test](skills/flutter-add-integration-test/SKILL.md) | Configures Flutter Driver for app interaction and converts MCP actions into permanent integration tests. Use when adding integration testing to a project, exploring UI components via MCP, or automating user flows with the integration_test package. | Add an integration test that validates the checkout experience |
| [flutter-add-widget-preview](skills/flutter-add-widget-preview/SKILL.md) | Adds interactive widget previews to the project using the previews.dart system. Use when creating new UI components or updating existing screens to ensure consistent design and interactive testing. | Create a preview for the ProductCard widget with different price states |
| [flutter-add-widget-test](skills/flutter-add-widget-test/SKILL.md) | Implement a component-level test using `WidgetTester` to verify UI rendering and user interactions (tapping, scrolling, entering text). Use when validating that a specific widget displays correct data and responds to events as expected. | Add a widget test for the CustomButton to verify the onTap callback is called |
| [flutter-apply-architecture-best-practices](skills/flutter-apply-architecture-best-practices/SKILL.md) |
