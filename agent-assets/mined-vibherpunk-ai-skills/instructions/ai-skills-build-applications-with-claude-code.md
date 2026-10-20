# Copilot Instructions: Build Applications With Claude Code
Description: Learn how to configure and use Claude Code for free to build modular, scalable applications. This skill covers setup, best practices, and workflow optimization for AI-assisted development.

## Overview
This skill teaches you how to configure Claude Code for free using OpenRouter and build modular, scalable applications. You'll learn to set up the environment, structure your projects effectively, and optimize your workflow for AI-assisted development.

## Step-by-Step Workflow
1. **Set Up Claude Code**: Create a `.claude` folder and a `settings.json.local` file. Paste the configuration provided in the transcript.
2. **Obtain API Key**: Sign up on OpenRouter.ai, create an API key, and paste it into your `settings.json.local` file.
3. **Select Free Model**: On OpenRouter, search for free models like Nvidia's or MiniMax M2.5, and configure them in your settings.
4. **Set Base URL**: Use the provided base URL in your configuration.
5. **Test Configuration**: Run Claude Code in your terminal and verify the setup by interacting with the model.

## Code Snippets
```json
{
  "api_key": "your_api_key_here",
  "model": "MiniMax M2.5",
  "base_url": "https://api.openrouter.ai"
}
```

## Best Practices
- **Modular Structure**: Keep files small and focused, ideally under 600 lines of code. This helps the AI maintain context and reduces errors.
- **Understand Building Blocks**: Before prompting the AI, understand the core concepts of your application to avoid issues like race conditions.
- **One Task Per Session**: Break down features into small tasks, test each one, and push to GitHub before moving to the next task.

## Common Pitfalls
- **Large Files**: Avoid dumping everything into one file. This can cause the AI to lose context and hallucinate.
- **Lack of Understanding**: Not understanding core concepts can lead to flawed applications. Always know what to ask the AI.
- **Skipping Tests**: Failing to test each task can result in broken features. Always test before pushing to GitHub.

## Validation and Testing
- **Manual Testing**: After completing each task, manually test the feature to ensure it works as expected.
- **GitHub Backup**: Push each tested feature to GitHub to maintain a backup of your progress.

For more detailed guidance, refer to the [Core Concepts](references/core_concepts.md), [Practical Guide](references/practical_guide.md), and [Code Examples](references/code_examples.md).

## Reference Guides

### Code Examples

# Code Examples

## Configuration File
```json
{
  "api_key": "your_api_key_here",
  "model": "MiniMax M2.5",
  "base_url": "https://api.openrouter.ai"
}
```

## Modular File Structure
```plaintext
project/
│
├── .claude/
│   └── settings.json.local
├── src/
│   ├── auth.js
│   ├── database.js
│   ├── routes.js
│   └── utils.js
└── README.md
```

## Prompt Example
```plaintext
Create a modular authentication system with the following features:
- User registration
- User login
- Password reset
Ensure each feature is in a separate file and follows best practices for security.
```

## Testing Script
```bash
# Run tests for each module
npm test auth.js
npm test database.js
npm test routes.js
npm test utils.js
```

## GitHub Push Command
```bash
# Add, commit, and push changes to GitHub
git add .
git commit -m "Added authentication system"
git push origin main
```

### Core Concepts

# Core Concepts

## Modular Application Structure
Keeping your application modular is crucial for scalability and maintainability. Each file should focus on a single responsibility, making it easier for the AI to understand and work with the code. This approach also helps in debugging and updating the application.

## Understanding Building Blocks
Before prompting the AI, it's essential to understand the fundamental concepts of your application. For example, if you're building a multi-user application, understanding race conditions can help you craft better prompts and avoid data loss.

## One Task Per Session
Breaking down features into small, manageable tasks ensures that each part of the application is thoroughly tested and functional. This practice also provides a safety net, as you can revert to previous versions if something goes wrong.

## Context Window Management
AI models have a limited context window, meaning they can only process a certain amount of information at a time. Keeping files small and focused helps the AI maintain context and reduces the risk of errors.

## Pro Tips
- Add modularity rules to your prompts or a Claude MD file to avoid repetition.
- Always test each task manually before pushing to GitHub.
- Use GitHub as a backup to safeguard your progress.

### Practical Guide

# Practical Guide

## Setting Up Claude Code
1. **Create Configuration Folder**: Start by creating a `.claude` folder in your project directory.
2. **Configuration File**: Inside the `.claude` folder, create a `settings.json.local` file and paste the provided configuration.
3. **API Key**: Sign up on OpenRouter.ai, generate an API key, and add it to your `settings.json.local` file.
4. **Select Model**: Choose a free model from OpenRouter, such as Nvidia's or MiniMax M2.5, and configure it in your settings.
5. **Base URL**: Set the base URL to `https://api.openrouter.ai`.

## Building Modular Applications
- **File Structure**: Organize your project into small, focused files, each handling a single responsibility.
- **Prompting**: When prompting the AI, specify the modular structure to ensure the generated code aligns with your project's architecture.

## Testing and Validation
- **Manual Testing**: After completing each task, manually test the feature to ensure it functions correctly.
- **GitHub Backup**: Push each tested feature to GitHub to maintain a backup of your progress.

## Common Pitfalls
- **Large Files**: Avoid creating large files that exceed the AI's context window.
- **Lack of Understanding**: Ensure you understand the core concepts of your application before prompting the AI.
- **Skipping Tests**: Always test each task before moving on to the next one.

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[Claude Code Is Now 100% Free - Here's How](https://www.youtube.com/watch?v=t0Mesp118l4)** by Hasan Aboul Hasan