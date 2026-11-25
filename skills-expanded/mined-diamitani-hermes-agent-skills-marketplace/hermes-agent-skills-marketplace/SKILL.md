---
name: hermes-agent-skills-marketplace
description: >
  Shareable packages of AI skills for Hermes Agent – organized by tier (Pro/Standard/Community) Use this skill when working with hermes agent skills marketplace tasks or workflows.
---

# Hermes Agent Skills Marketplace

**Shareable packages of AI skills for Hermes Agent** – curated from Pat Diamitani's GPT Portfolio (~185 GPTs → 124+ skills)

## 📦 Packages & Pricing Tiers

| Package | Tier | Price | Skills | Description |
|---------|------|-------|--------|-------------|
| **[Productive Pro](hermes-agent-productive/)** | 🚀 Pro | $299 | 143 | Productivity & development workflows |
| **[Business Pro](hermes-agent-business/)** | 🚀 Pro | $199 | 114 | Business operations & sales automation |
| **[Creative Standard](hermes-agent-creative/)** | ⭐ Standard | $99 | 44 | Creative, music, design workflows |
| **[Foundation Standard](hermes-agent-foundation/)** | ⭐ Standard | $49 | 10 | Hermes core & automation |
| **[Community Free](hermes-agent-community/)** | 🎉 Free | FREE | 20 | Lifestyle, education, home automation |
| **[Enterprise Bundle](.)** | 🏢 Enterprise | $499 | 331 | All 5 packages |

## 🎯 Target Users

- **Productive Pro**: AI engineers, developers, productivity experts  
- **Business Pro**: Business owners, sales teams, marketing professionals  
- **Creative Standard**: Musicians, designers, content creators  
- **Foundation Standard**: Beginners, automation enthusiasts  
- **Community Free**: Everyone, lifestyle enthusiasts  
- **Enterprise Bundle**: Organizations, agencies, full-stack AI teams  

## 📊 Skill Coverage

| Category | Pro Packages | Standard Packages | Community | Total |
|----------|--------------|------------------|-----------|-------|
| Productivity | ✅ | ✅ | ✅ | 75 |
| Software Development | ✅ | ✅ | ✅ | 38 |
| Music Industry | ✅ | ✅ | ✅ | 23 |
| Creative | ✅ | ✅ | ✅ | 21 |
| Business Tools | ✅ | ✅ | ✅ | 62 |
| GitHub | ✅ | | | 7 |
| Email/Marketing | ✅ | | | 2 |
| Lifestyle | | | ✅ | 12 |

## 🚀 Installation

```bash
# Install a specific package
cp -r hermes-agent-productive/ ~/.hermes/skills/

# Install all packages (Enterprise)
for pkg in hermes-agent-*; do cp -r $pkg/ ~/.hermes/skills/; done
```

## 💡 Usage

Load any skill in Hermes Agent:

```python
# In Hermes conversation
skill_view(name='prompt-builder-architect')
```



## ✅ Deployment Status

**Repository:** https://github.com/diamitani/hermes-agent-skills-marketplace  
**Commit:** `905283e` (Hermes Agent Skills Marketplace v1.0.0)  
**Last Push:** July 17, 2026  
**Skills Count:** 259 across 24 categories  

Ready for distribution on GitHub Marketplace, Gumroad, or direct licensing.


## 🤝 Contributing

Skills follow Hermes Agent skill format with YAML frontmatter. See `hermes-agent-skill-authoring` skill for guidelines.

## 📄 License

MIT License – free for personal use, commercial licensing available for enterprise.
