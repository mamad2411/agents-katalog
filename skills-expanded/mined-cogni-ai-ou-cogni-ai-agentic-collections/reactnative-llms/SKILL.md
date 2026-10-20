---
name: reactnative-llms
description: >-
  React Native documentation.
  You MUST load this skill when interacting with React Native documentation, Core Components, or mobile APIs.
license: MIT
---

# React Native Docs

<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

## WHEN TO USE

- When developing mobile cross-platform applications using React Native.
- When you need documentation on React Native Core Components (e.g., `View`, `Text`, `FlatList`, `ScrollView`).
- When you need documentation on React Native APIs, Animations, Handling Touches, or linking libraries.

## WHEN NOT TO USE

- When working on standard web applications using React (use `react-llms` instead).

## Core Process

1. **Identify the Topic**: Determine which React Native feature or component you need to look up (e.g., `KeyboardAvoidingView`, Navigation, AppRegistry, Platform-Specific Code).
2. **Fetch the Documentation Index**: Use a web fetching tool to read the main `llms.txt` file listed in the References.
3. **Fetch Specific Documents**: From the index, extract the exact link for the topic and fetch the specific documentation markdown.
4. **Apply Context**: Apply the retrieved documentation to guide the task correctly.

## Core Principles

- **Targeted Loading**: React Native documentation is large. Rely on the `llms.txt` index to fetch only the specific files you need rather than attempting to fetch the entire corpus.

## References

To fully utilize this skill, you MUST read at least one of the links relevant to the current context:

- **React Native Documentation Index (llms.txt)**: [https://reactnative.dev/llms.txt](https://reactnative.dev/llms.txt)
  You MUST read this index when you need to read documentation on any React Native component or API.
  Index includes docs, getting-started, environment-setup, components-and-apis, handling-touches, animated, flexbox, etc.
