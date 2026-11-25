---
name: readme-doc
description: |
  Generate a complete README.md file for any software project. Use whenever the user asks to create, write, generate, or draft a README.md — the first document people see when they discover your project. Covers project overview, installation, usage, configuration, contributing guidelines, and getting started.

  This skill triggers when users need to document: project setup, installation instructions, quick start guide, usage examples, configuration options, contributing guidelines, or "how do I get started with this project".

  Do NOT trigger for detailed technical design (use Design.md), architecture docs (use Architecture.md), or comprehensive API docs (separate API documentation).

---

# README.md Author Skill

You are a technical writer creating the front door to a software project.

## Philosophy

A README.md answers: **"What is this project, and how do I use it?"**

It covers:
- **What it does** - Purpose and key features
- **Why it exists** - Problem it solves
- **How to get started** - Installation and quick start
- **How to use it** - Basic usage and examples
- **How to contribute** - For open source projects
- **Where to get help** - Support and community

The audience is **anyone discovering your project** — potential users, contributors, or evaluators. A great README is the difference between adoption and abandonment.

## Structure

A README.md has **10 core sections**:

1. **Header** - Project name, badges, tagline
2. **Overview** - What it is and why it matters
3. **Features** - Key capabilities
4. **Quick Start** - Get running in 5 minutes
5. **Installation** - Detailed setup instructions
6. **Usage** - How to use it with examples
7. **Configuration** - Options and settings
8. **Contributing** - How to contribute (if open source)
9. **License** - Legal information
10. **Support** - Where to get help

## Workflow: Interview → Draft → Validate

### Step 1: Interview the User

Gather project context before writing:

**Required context:**
- **What's the project?** (name, type: library, CLI tool, web app, etc.)
- **What problem does it solve?** (the "why")
- **Who is the audience?** (developers, end users, specific domain)
- **Tech stack?** (language, framework, platform)
- **Current state?** (alpha, beta, production-ready)

**Optional but helpful:**
- **Installation method?** (npm, pip, docker, binary download)
- **Is it open source?** (affects Contributing section)
- **License?** (MIT, Apache, GPL, proprietary)
- **Notable features?** (unique selling points)
- **Dependencies?** (prerequisites users need)

If sparse info, make reasonable assumptions (note them) and proceed.

### Step 2: Build the Document Structure

```markdown
# [Project Name]

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/user/repo/releases)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/user/repo/actions)

> [One-line tagline that captures what this project does]

[Optional: Hero image or demo GIF showing the project in action]

---

## Overview

[2-3 paragraphs explaining what the project is, what problem it solves, and why someone should care]

**[Project Name]** is a [type of tool/library/app] that [primary purpose]. It helps [target audience] by [key benefit].

Unlike [alternatives], [Project Name] offers [unique value proposition]. Built with [tech stack], it's designed to be [key qualities: fast, simple, reliable, etc.].

### Why [Project Name]?

- **Problem 1:** [Pain point in existing solutions]
  - **Solution:** [How this project addresses it]

- **Problem 2:** [Another pain point]
  - **Solution:** [How this project addresses it]

---

## Features

- ✅ **[Feature 1]** - [Brief description of capability]
- ✅ **[Feature 2]** - [Brief description of capability]
- ✅ **[Feature 3]** - [Brief description of capability]
- 🚧 **[Upcoming Feature]** - [Planned capability] (coming soon)

---

## Quick Start

Get up and running in under 5 minutes:

```bash
# Install
npm install [package-name]
# or
pip install [package-name]
# or
docker pull [image-name]

# Run
[command to start]

# Open browser
http://localhost:3000
```

That's it! See [Installation](#installation) for detailed setup instructions.

---

## Installation

### Prerequisites

Before installing, ensure you have:
- **[Tool 1]** - version X.X or higher ([installation link](https://example.com))
- **[Tool 2]** - version Y.Y or higher
- **[Optional Tool 3]** - only needed for [specific use case]

Check your versions:
```bash
node --version  # Should be >= 18.0.0
npm --version   # Should be >= 9.0.0
```

### Option 1: Package Manager (Recommended)

#### npm (Node.js)
```bash
npm install [package-name]
# or for global installation
npm install -g [package-name]
```

#### pip (Python)
```bash
pip install [package-name]
# or with pipenv
pipenv install [package-name]
```

#### Homebrew (macOS)
```bash
brew install [package-name]
```

#### apt (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install [package-name]
```

### Option 2: Download Binary

Download the latest release from [GitHub Releases](https://github.com/user/repo/releases):

**macOS:**
```bash
curl -L https://github.com/user/repo/releases/download/v1.0.0/app-macos.tar.gz | tar xz
sudo mv app /usr/local/bin/
```

**Linux:**
```bash
curl -L https://github.com/user/repo/releases/download/v1.0.0/app-linux.tar.gz | tar xz
sudo mv app /usr/local/bin/
```

**Windows:**
Download `app-windows.zip`, extract, and add to PATH.

### Option 3: Docker

```bash
docker pull [image-name]:latest
docker run -p 3000:3000 [image-name]
```

### Option 4: Build from Source

```bash
# Clone the repository
git clone https://github.com/user/repo.git
cd repo

# Install dependencies
npm install  # or pip install -r requirements.txt

# Build
npm run build  # or python setup.py build

# Run
npm start  # or python main.py
```

### Verify Installation

```bash
[command] --version
# Should output: [package-name] version X.X.X
```

---

## Usage

### Basic Usage

[Simplest possible example that does something useful]

```[language]
import { feature } from '[package-name]';

// [Comment explaining what this does]
const result = feature.doSomething('input');
console.log(result);
```

Output:
```
[Expected output shown here]
```

### Common Use Cases

#### Use Case 1: [Name]
[Description of what this accomplishes]

```[language]
[Code example]
```

#### Use Case 2: [Name]
[Description of what this accomplishes]

```[language]
[Code example]
```

#### Use Case 3: [Name]
[Description of what this accomplishes]

```[language]
[Code example]
```

### Command-Line Interface (if applicable)

```bash
# Basic command
[tool] [action] [arguments]

# With options
[tool] [action] --option value --flag

# Examples
[tool] generate --type api --output ./src
[tool] deploy --env production --region us-west-2
```

#### Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `[command1]` | [What it does] | `[tool] [command1] --arg` |
| `[command2]` | [What it does] | `[tool] [command2] --arg` |
| `[command3]` | [What it does] | `[tool] [command3] --arg` |

### API Usage (if library)

#### Core Functions

##### `functionName(param1, param2)`
[Description of what the function does]

**Parameters:**
- `param1` (type): [Description]
- `param2` (type, optional): [Description] (default: `value`)

**Returns:** `returnType` - [Description of return value]

**Example:**
```[language]
const result = functionName('value1', 'value2');
```

##### `anotherFunction(options)`
[Description]

**Parameters:**
- `options` (object):
  - `option1` (type): [Description]
  - `option2` (type): [Description]

**Example:**
```[language]
const result = anotherFunction({
  option1: 'value',
  option2: true
});
```

---

## Configuration

### Configuration File

Create a `[config-file-name]` in your project root:

```[format]
{
  "option1": "value",
  "option2": true,
  "option3": 123,
  "nested": {
    "subOption": "value"
  }
}
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `option1` | string | `"default"` | [What this controls] |
| `option2` | boolean | `false` | [What this enables/disables] |
| `option3` | number | `100` | [What this sets] |
| `nested.subOption` | string | `null` | [What this configures] |

### Environment Variables

Configure via environment variables (takes precedence over config file):

```bash
export APP_OPTION1="value"
export APP_OPTION2="true"
export APP_LOG_LEVEL="debug"
```

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_OPTION1` | [Description] | `value` |
| `APP_OPTION2` | [Description] | `false` |
| `APP_LOG_LEVEL` | Logging verbosity (debug, info, warn, error) | `info` |

---

## Examples

### Example 1: [Scenario Name]

[Brief description of what this example demonstrates]

```[language]
[Full working example with comments]
```

**Output:**
```
[Expected output]
```

### Example 2: [Scenario Name]

[Brief description]

```[language]
[Full working example]
```

### More Examples

See the [examples](./examples) directory for more complete examples:
- [Basic usage](./examples/basic.md)
- [Advanced features](./examples/advanced.md)
- [Integration guide](./examples/integration.md)

---

## Development

### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/user/repo.git
cd repo

# Install dependencies
npm install  # or pip install -r requirements-dev.txt

# Run in development mode
npm run dev

# Run tests
npm test

# Lint code
npm run lint

# Format code
npm run format
```

### Project Structure

```
project-root/
├── src/              # Source code
│   ├── core/         # Core functionality
│   ├── utils/        # Utility functions
│   └── index.js      # Entry point
├── tests/            # Test files
├── docs/             # Documentation
├── examples/         # Usage examples
├── .github/          # GitHub workflows
├── package.json      # Dependencies
└── README.md         # This file
```

### Testing

```bash
# Run all tests
npm test

# Run specific test file
npm test -- path/to/test.js

# Run with coverage
npm run test:coverage

# Watch mode
npm run test:watch
```

### Building

```bash
# Development build
npm run build:dev

# Production build
npm run build:prod

# Build and watch for changes
npm run build:watch
```

---

## Contributing

We welcome contributions! Here's how you can help:

### Ways to Contribute

- 🐛 **Report bugs** - [Open an issue](https://github.com/user/repo/issues/new?template=bug_report.md)
- 💡 **Suggest features** - [Open a feature request](https://github.com/user/repo/issues/new?template=feature_request.md)
- 📝 **Improve documentation** - Fix typos, clarify instructions
- 🔧 **Submit pull requests** - Fix bugs or add features

### Development Process

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub, then clone your fork
   git clone https://github.com/YOUR-USERNAME/repo.git
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

3. **Make your changes**
   - Write code following our [style guide](CONTRIBUTING.md#style-guide)
   - Add tests for new functionality
   - Update documentation as needed

4. **Test your changes**
   ```bash
   npm test
   npm run lint
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   # Follow conventional commits: feat, fix, docs, style, refactor, test, chore
   ```

6. **Push and create a pull request**
   ```bash
   git push origin feature/your-feature-name
   # Then open a PR on GitHub
   ```

### Coding Standards

- Follow [language-specific style guide]
- Write tests for all new features
- Maintain test coverage above 80%
- Update documentation for API changes
- Use meaningful commit messages

### Pull Request Guidelines

- PR title should follow [Conventional Commits](https://www.conventionalcommits.org/)
- Include description of changes and motivation
- Reference related issues (e.g., "Fixes #123")
- Ensure all tests pass
- Request review from maintainers

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## Troubleshooting

### Common Issues

#### Issue 1: [Error message or problem]

**Symptoms:**
- [What you see when this happens]

**Solution:**
```bash
[Commands to fix it]
```

Or [explanation of what to do].

---

#### Issue 2: [Another common problem]

**Symptoms:**
- [Description]

**Solution:**
[Step-by-step fix]

---

### Still Having Issues?

1. Check [GitHub Issues](https://github.com/user/repo/issues) for similar problems
2. Search [Stack Overflow](https://stackoverflow.com/questions/tagged/package-name)
3. Join our [Discord community](https://discord.gg/invite-link)
4. [Open a new issue](https://github.com/user/repo/issues/new)

---

## FAQ

**Q: [Common question]?**  
A: [Clear answer with example if relevant]

**Q: [Another question]?**  
A: [Answer]

**Q: [Another question]?**  
A: [Answer]

---

## Roadmap

See [ROADMAP.md](ROADMAP.md) for planned features and timeline.

**Upcoming:**
- [ ] [Feature 1] (Q3 2026)
- [ ] [Feature 2] (Q4 2026)
- [ ] [Feature 3] (Q1 2027)

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for release history.

### Recent Releases

**v1.0.0** (2026-07-22)
- Initial release
- Core features implemented
- Full documentation

---

## License

This project is licensed under the [MIT License](LICENSE) - see the [LICENSE](LICENSE) file for details.

### Third-Party Licenses

This project uses the following open-source packages:
- [package-name](https://github.com/org/package) - [License Type]
- [another-package](https://github.com/org/package) - [License Type]

---

## Acknowledgments

- [Person/Project 1] - for [contribution/inspiration]
- [Person/Project 2] - for [contribution/inspiration]
- All [contributors](https://github.com/user/repo/graphs/contributors) who have helped improve this project

---

## Support

### Getting Help

- 📖 **Documentation:** [Full docs](https://docs.example.com)
- 💬 **Community:** [Discord](https://discord.gg/invite) | [Slack](https://slack.example.com)
- 🐛 **Bug Reports:** [GitHub Issues](https://github.com/user/repo/issues)
- 📧 **Email:** support@example.com
- 🐦 **Twitter:** [@projectname](https://twitter.com/projectname)

### Security

To report security vulnerabilities, please email security@example.com instead of using the issue tracker. See [SECURITY.md](SECURITY.md) for details.

---

## Links

- **Homepage:** https://example.com
- **Documentation:** https://docs.example.com
- **GitHub:** https://github.com/user/repo
- **NPM:** https://www.npmjs.com/package/[package-name]
- **PyPI:** https://pypi.org/project/[package-name]

---

## Star History

If you find this project useful, please consider giving it a ⭐️ on GitHub!

[![Star History Chart](https://api.star-history.com/svg?repos=user/repo&type=Date)](https://star-history.com/#user/repo&Date)

---

**Made with ❤️ by [Your Name/Organization](https://github.com/user)**
```

---

## Best Practices

### 1. **Lead with Value**
   - First paragraph answers "what is this?"
   - Second paragraph answers "why should I care?"
   - Show value before asking for time investment

### 2. **Progressive Disclosure**
   - Quick Start for the impatient (5 minutes)
   - Installation for those who need details
   - Configuration for power users
   - Contributing for potential collaborators

### 3. **Show, Don't Tell**
   - Use code examples liberally
   - Include expected output
   - Add screenshots/GIFs where helpful
   - Real examples > abstract descriptions

### 4. **Make It Scannable**
   - Use headers and subheaders
   - Bullet points for lists
   - Tables for structured data
   - Code blocks for commands
   - Badges for quick status info

### 5. **Badges Add Credibility**
   - Build status (passing = confidence)
   - Version number (shows active development)
   - License (legal clarity)
   - Coverage (quality signal)
   - Downloads (popularity signal)

### 6. **Keep It Updated**
   - Version numbers current
   - Examples that actually work
   - Links that aren't broken
   - Installation steps tested recently

### 7. **Lower the Barrier**
   - Quick Start should be copy-paste ready
   - Minimal prerequisites
   - Clear error messages in examples
   - Link to prerequisites installation

### 8. **Think About Discovery**
   - Keywords for search engines
   - Tags for package managers
   - Clear project description
   - Related projects/alternatives

---

## Conversation Flow

When the user asks for a README.md:

**1. Understand the Project**
Ask: "What's the project? (library, CLI tool, web app, etc.)"

**2. Gather Context**
- "What problem does it solve?"
- "Who is the target audience?"
- "What's the tech stack?"
- "How do people install it? (npm, pip, docker, etc.)"

**3. Clarify Scope**
Ask: "Is this open source? (affects Contributing section)"

**4. Generate the README**
- Start with compelling overview
- Add badges if applicable
- Include Quick Start (copy-paste ready)
- Detailed Installation with multiple options
- Usage examples (simple → complex)
- Configuration options
- Contributing guidelines (if open source)
- Troubleshooting common issues
- Support and community links

**5. Tailor to Project Type**
- **Library:** Focus on API docs and code examples
- **CLI Tool:** Focus on commands and flags
- **Web App:** Focus on deployment and environment setup
- **Framework:** Focus on getting started tutorial

**6. Save and Suggest Next Steps**
Save as `README.md` and suggest: "Want me to create CONTRIBUTING.md or CHANGELOG.md next?"

---

## Tips by Project Type

### For Libraries
- Focus heavily on API documentation
- Multiple code examples showing different use cases
- Installation via package manager prominent
- Link to full API reference docs

### For CLI Tools
- Command reference front and center
- Each command with examples
- Installation via multiple methods
- Shell completion scripts if available

### For Web Applications
- Screenshots/demo GIF required
- Deployment instructions
- Environment variable configuration
- Link to hosted demo if available

### For Frameworks
- Getting started tutorial (step-by-step)
- Project structure explanation
- Comparison to alternatives
- Migration guides from competitors

---

## Common Mistakes to Avoid

❌ **No Quick Start**
   - People want to try it immediately
   - Add a 5-minute Quick Start section

❌ **Installation That Doesn't Work**
   - Test installation steps yourself
   - Include version requirements
   - Show expected output

❌ **Abstract Examples**
   - Use real, working code
   - Show actual output
   - Make it copy-paste ready

❌ **Wall of Text**
   - Break into sections
   - Use headers and lists
   - Add visual breathing room

❌ **Missing Prerequisites**
   - List everything needed
   - Include version numbers
   - Link to installation guides

❌ **Outdated Information**
   - Keep version numbers current
   - Test examples regularly
   - Update screenshots/GIFs

❌ **No Context**
   - Explain what problem it solves
   - Show why it's better than alternatives
   - Give the "why" not just the "what"

---

## Output Instructions

When generating a README.md:

1. **Interview for context** (project type, purpose, audience)
2. **Start with compelling overview** (what, why, who)
3. **Add badges** (if applicable and links available)
4. **Quick Start section** (5-minute copy-paste example)
5. **Detailed installation** (multiple methods if applicable)
6. **Usage examples** (simple to complex progression)
7. **Configuration** (options and environment variables)
8. **Contributing** (if open source)
9. **Troubleshooting** (common issues)
10. **Support links** (community, docs, issues)
11. **Save as `README.md`** in project root

---

## Follow-Up Documents

After creating README.md, suggest:
- **CONTRIBUTING.md** - Detailed contribution guidelines
- **CHANGELOG.md** - Release history
- **CODE_OF_CONDUCT.md** - Community standards
- **LICENSE** - Legal terms
- **SECURITY.md** - Security policy
