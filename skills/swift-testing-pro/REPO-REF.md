# Repo Referensi: twostraws/swift-testing-agent-skill

Repo: https://github.com/twostraws/swift-testing-agent-skill
Ref lokal: /Users/chaali0324/.agents/repo-refs/twostraws_swift-testing-agent-skill
API: curl "localhost:27126/repos/readme?name=twostraws_swift-testing-agent-skill"
Dibuat: 2026-09-16

## Cuplikan README
# twostraws/swift-testing-agent-skill

Source: https://github.com/twostraws/swift-testing-agent-skill
Fetched: 2026-09-16

## README
<p align="center">
    <img src="assets/logo.svg" alt="Swift Testing Pro - Agent Skill for Claude Code, Codex, and Gemini" height="100" />
</p>

<h1 align="center">Swift Testing Agent Skill for AI Coding Assistants</h1>

<p align="center">
    <img src="https://img.shields.io/badge/swift-6.2+-8e44ad.svg" alt="Designed for Swift 6.2 and later." />
    <a href="https://twitter.com/twostraws">
        <img src="https://img.shields.io/badge/Contact-@twostraws-95a5a6.svg?style=flat" alt="Twitter: @twostraws" />
    </a>
</p>

An agent skill that helps AI coding assistants like Claude Code, Codex, Cursor, and Gemini write better tests using Swift Testing. Covers `@Test`, `#expect`, `#require`, parameterized testing, traits, exit tests, confirmations, and more, targeting the mistakes LLMs actually make.

Also available:

- [SwiftUI Pro](https://github.com/twostraws/SwiftUI-Agent-Skill)
- [SwiftData Pro](https://github.com/twostraws/SwiftData-Agent-Skill)
- [Swift Concurrency Pro](https://github.com/twostraws/Swift-Concurrency-Agent-Skill)

Find more agent skills for Swift and Apple platform development at [Swift Agent Skills](https://github.com/twostraws/Swift-Agent-Skills).


## Installing Swift Testing Pro

### Claude Code

Add the Swift Testing Agent Skill marketplace, then install the plugin:

```
/plugin marketplace add twostraws/Swift-Testing-Agent-Skill
/plugin install swift-testing-pro@swift-testing-agent-skill
```

### Codex, Gemini, Cursor, and others

```bash
npx skills add https://github.com/twostraws/swift-testing-agent-skill --skill swift-testing-pro
```

If you get the error `npx: command not found`, it means you don’t currently have Node installed. You need to run this command to install Node through Homebrew:

```bash
brew install node
```

And if *that* fails it usually means you need to [install Homebrew](https://brew.sh) first.

When using `npx`, you can select exactly which agents you want to use during the installation. You can also select whether the skill should be installed just for one project, or whether it should be made available for all your projects.

Alternatively, you can clone this whole repository and install it however you want.

If you're using Xcode, watch the YouTube video on [How to Install and Use Agent Skills in Xcode](https://www.youtube.com/watch?v=nKVZBKoB6P4) for a walkthrough.


## Usin
