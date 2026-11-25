---
name: interview
description: Interview the user to learn about their work style, preferences, and priorities, then create a personalized profile
disable-model-invocation: true
allowed-tools: AskUserQuestion, Write, Read, Glob, Bash
---

# User Interview Skill

Conduct a comprehensive interview to understand the user's work style, preferences, and priorities. Create a detailed profile that helps Claude provide better assistance.

## Overview

This skill has three phases:

1. **Environmental Analysis** (Silent) - Gather data about the user's system, tools, and work patterns
2. **Interactive Interview** (User-facing) - Ask targeted questions based on findings
3. **Profile Creation** - Generate profile files and configure CLAUDE.md:
   - **`~/.claude/USER_PROFILE_QUICK.md`** - Quick Reference (300-500 tokens)
   - **`~/.claude/USER_PROFILE.md`** - Full Profile (2000-3000 tokens)
   - **Update `~/.claude/CLAUDE.md`** - Add directive to read profile files at session start

## ⚠️ CRITICAL: Sequential Execution Only

**DO NOT run tool calls in parallel during this skill.**

The `/interview` skill makes many tool calls during environmental analysis. Running them in parallel causes a Claude Code bug where tool_result blocks become orphaned from their tool_use blocks, corrupting the conversation state.

**Required approach:**
- Run checks in small sequential batches (3-5 tool calls maximum per batch)
- Wait for each batch to complete before sending the next batch
- Never send more than 5 tool calls in a single message

## Phase 1: Environmental Analysis

**Do this FIRST, before introducing yourself.**

Silently analyze the user's environment to gather context. See [environmental-analysis.md](environmental-analysis.md) for the complete checklist.

Key areas to analyze:
- Operating system and package management
- Development tools and languages
- Shell configuration and dotfiles
- Git repositories and commit patterns (**verify authorship!**)
- **Local development workflow** (testing, building, running services)
- **Deployment practices & YOLO factor** (CI/CD, risk tolerance, work vs private)
- **AI tool usage & AI YOLO factor** (how much AI, how carefully reviewed)
- **Communication tone & style** (formality, directness, energy level)
- **Problem-solving approach** (debugging style, learning style)
- **Proactivity boundaries** (scope tolerance, permission levels)
- **Code preferences** (explanation order, abstraction level, complexity)
- Work patterns and timing from commits/history
- Security and privacy tools
- Work vs private project separation

**CRITICAL**: When analyzing git commits, verify authorship first. Many repos may be cloned projects where the user contributed nothing. See detailed instructions in environmental-analysis.md.

**NEW COMPREHENSIVE ANALYSIS**: environmental-analysis.md now includes detailed sections (29-39) for:
- **Work vs Private separation** (§29): Different practices for professional vs personal projects
- **Deployment YOLO factor** (§30): Risk tolerance with deployments (5-point scale)
- **AI usage patterns** (§31): How much they use AI tools (Copilot, Claude, etc.)
- **AI YOLO factor** (§31): How carefully they review AI code (blind trust vs thorough review)
- **Tone & communication style** (§32): Formality, energy, directness - CRITICAL for how Claude responds
- **Debugging communication** (§33): How much hand-holding when explaining errors
- **Code explanation preferences** (§34): Top-down vs bottom-up, code-first vs concept-first
- **Proactivity boundaries** (§35): When to go beyond requests vs stick to exact ask
- **Scope tolerance** (§36): Comfortable with broad changes or prefer focused fixes
- **Learning style** (§37): Docs-first, example-driven, experiment-first, theory-first
- **Complexity preferences** (§38): Simple code vs abstractions, DRY vs clarity
- **Frustration patterns** (§39): How to help when they're stuck

### Running the Analysis

**CRITICAL: Run checks SEQUENTIALLY, not in parallel** to avoid conversation state bugs.

- Run checks in small batches (3-5 at a time maximum)
- Wait for each batch to complete before starting the next batch
- Don't show raw data to user (package lists, full history)
- Look for patterns: frequency, categories, sophistication
- Note what's NOT there (missing tools reveal priorities)
- Cross-reference multiple sources for accuracy

**Suggested batch order:**
1. Basic system info (OS, shell, locale)
2. Development tools check (languages, packages)
3. Config files (zshrc, gitconfig, ssh config)
4. Shell history analysis
5. Git commit analysis (one repo at a time)
6. Timing and workflow patterns
7. AI usage and deployment patterns

## Phase 2: Interactive Interview

After completing environmental analysis, introduce the interview:

### Introduction Template

Present your findings conversationally:
- "I see you're running [OS] with [WM/DE]"
- "You have [X] projects, primarily working with [languages/tools]"
- "Your git commits show [pattern] - I analyzed [N] commits you authored across [M] projects"
- "Your system locale is [locale] - is English your preference for responses?"

Make it personal and show you've done your homework.

### Interview Stages

Conduct the interview in 3-5 question stages to avoid overwhelming the user. Each stage should have 2-3 questions max.

#### Stage 1: Communication & Tone (2-3 questions) - MOST CRITICAL

**This determines how Claude communicates with them - getting it wrong ruins the experience.**

Core questions:
- Language preference (if non-English locale detected)
- Response detail level: "Do you prefer concise get-to-the-point responses, or detailed explanations?"
- Tone preference: "Should I keep responses professional/formal, conversational/friendly, or very casual?"
- Error communication: "When there's an error - full explanation with steps, or just point to the problem?"

**Present your inferences and ask for confirmation:**
- "Your commits are brief and direct - should I match this style?"
- "I noticed you use occasional emoji (🐛) - is that your typical style?"
- "You seem to [write detailed commit messages / be very concise] - prefer responses that way too?"

**Adapt the interview tone immediately based on their first answer!**

#### Stage 2: Code Explanation & Learning (2-3 questions)

Core questions:
- Code explanation order: "When I explain code, do you prefer: see the code first, or understand the concept first?"
- Learning style: "When learning something new: read docs first, jump into examples, or trial-and-error?"
- Change presentation: "For code changes, show: full updated files, or just the specific changes?"

**Tailor based on findings:**
- If tutorial repos found: "I see tutorial projects - prefer step-by-step guides?"
- If experimental commits: "Lots of 'try' commits - learn by experimentation?"
- If detailed READMEs: "Your docs are thorough - prefer detailed explanations?"

#### Stage 3: Proactivity & Scope (2-3 questions)

Core questions:
- Proactivity: "When fixing something, should I: fix ONLY that, improve related code too, or go for comprehensive fixes?"
- Scope comfort: "Comfortable tackling multiple related issues at once, or prefer one focused thing at a time?"
- Permissions: "What should I always ask about vs just do?" (e.g., adding dependencies, breaking changes, refactoring)

**Tailor based on findings:**
- If small focused commits: "I see focused commits - prefer targeted fixes?"
- If large multi-file commits: "Comfortable with broader changes?"
- If work/private separation: "Different preferences for work vs personal projects?"

#### Stage 4: Deployment & AI Usage (2-4 questions)

Core questions:
- Deployment YOLO: "How do you typically deploy? Tests + staging first, or sometimes YOLO directly to prod?"
- AI tool usage: "Do you use AI coding assistants like Copilot or Claude? For what tasks?"
- AI review practices: "How do you review AI code? Read and test thoroughly, quick skim, or trust it works?"
- Work vs private: "Different practices for work vs personal projects?"

**Tailor based on findings:**
- If no CI/CD found: "I notice no CI/CD configs - do you deploy manually?"
- If AI co-authors in commits: "I see you work with [Copilot/Claude] - how much do you rely on it?"
- If AI commits followed by fixes: "I notice some fixes after AI code - do you test AI suggestions thoroughly?"
- If work and private repos found: "Different deployment practices for work vs personal?"
- If many "fix prod" commits: "How do you handle production incidents?"
- If heavy AI usage: "Can you debug code that AI generated, or do you need AI to fix it?"

#### Stage 5: Complexity & Code Philosophy (2-3 questions)

Core questions:
- Abstraction preference: "Code style: simple and obvious, or appreciate elegant abstractions and patterns?"
- DRY vs clarity: "How much code duplication is OK before abstracting?"
- Dependencies: "Adding libraries: do it freely, or prefer keeping dependencies minimal?"

**Tailor based on findings:**
- If many design patterns in code: "I see you use design patterns - architecture-oriented approach?"
- If minimal dependencies: "Light on dependencies - prefer simplicity?"
- If heavy abstraction: "Appreciate clever solutions or prefer explicit code?"

#### Stage 6: Values & Priorities (2-3 questions)

Core questions:
- Top priority: "What matters most: code quality, shipping fast, simplicity, performance, or reliability?"
- Pet peeves: "What bothers you most: over-engineering, verbose code, breaking changes, or something else?"
- Expertise areas: "What are you expert in vs currently learning?"

**Use observations:**
- "You have profiling tools - is performance a priority?"
- "I see linters configured - are you strict about code quality?"
- If Go projects dominant: "You seem to work primarily in Go - expert level?"
- If Kubernetes tools present: "What's your preferred K8s workflow?"

### Interview Tips

- Keep questions clear and specific
- Provide examples in option descriptions
- Reference specific findings: "I see you use vim extensively..."
- Allow flexibility - if they skip questions, that's fine
- Pay attention to how they answer - communication style itself is data
- Be conversational, not interrogative

## Phase 3: Profile Creation

After gathering responses, create profile files and configure CLAUDE.md:

1. **`~/.claude/USER_PROFILE_QUICK.md`** - Quick Reference (300-500 tokens)
2. **`~/.claude/USER_PROFILE.md`** - Full Profile (2000-3000 tokens)
3. **`~/.claude/CLAUDE.md`** - Update/create to reference the profile files

See [profile-template.md](profile-template.md) for the complete structure.

### How the Profile System Works

**File Reading Flow**:

1. **Every session start**: Claude Code auto-loads `~/.claude/CLAUDE.md`
2. **CLAUDE.md says**: "Read USER_PROFILE_QUICK.md"
3. **Claude reads**: USER_PROFILE_QUICK.md (300-500 tokens) - now knows your preferences
4. **USER_PROFILE_QUICK.md mentions**: Full profile exists at USER_PROFILE.md
5. **When Claude needs details**: Uses Read tool to fetch specific info from USER_PROFILE.md

**Key Point**: Only the Quick Reference is auto-loaded. The Full Profile is read on-demand using the Read tool when Claude needs deeper context.

### Two-Tier Profile Structure

**CRITICAL**: The profile has TWO data files with different purposes:

#### 1. 🎯 QUICK REFERENCE (300-500 tokens)
**Purpose**: Read at EVERY session start. Must be scannable in 10 seconds.
**Contains**: The 20% of info that affects 80% of interactions

**Must include**:
- ✅ Tone & communication style (formal/casual, verbose/terse, emoji yes/no)
- ✅ Proactivity level & permission boundaries (what to do vs ask)
- ✅ Response format preferences (code-first/concept-first, detail level)
- ✅ Scope tolerance (focused/broad)
- ✅ Top 2-3 languages/tools
- ✅ Work vs private key differences
- ✅ Top priority & pet peeve
- ✅ 2-3 quick actionable tips

**Format**: Use scales (1-5), icons, bullet points. Dense but scannable.

#### 2. 📚 FULL PROFILE (comprehensive, ~2000-3000 tokens)
**Purpose**: Reference when needed for deeper context
**Contains**: All detailed findings, evidence, system info

**Includes**:
- Complete system overview (OS, tools, packages)
- Detailed workflow analysis
- All learning/debugging/complexity preferences
- Complete commit/git analysis with evidence
- Environment variables, SSH config, etc.

### Profile Distillation Process

**Think of it like:**
- Quick Reference = "How to talk to this person"
- Full Profile = "Why and detailed context"

**Creating the Quick Reference**:
1. **From interview responses**: Prioritize stated preferences
2. **From code analysis**: Extract the clearest patterns
3. **From cross-validation**: Only include high-confidence findings
4. **Distill ruthlessly**: If it doesn't affect daily interactions, it goes in Full Profile

**Example decision making**:
- ✅ Quick Ref: "Casual tone, use emoji occasionally" (affects every message)
- ❌ Quick Ref: "Has 47 npm packages installed" (rarely relevant)
- ✅ Quick Ref: "Proactivity level 4 - can improve related code" (affects every suggestion)
- ❌ Quick Ref: "Commits mostly 22:00-02:00" (interesting but not actionable)
- ✅ Quick Ref: "Hates over-engineering" (critical pet peeve)
- ❌ Quick Ref: "Uses pacman + yay for packages" (Full Profile detail)

### Profile Quality for Quick Reference

**Good Quick Reference** (actionable):
```
Tone: 💼 Professional-Friendly
Response: Balanced detail, code-first
DO: Be direct, use standard patterns, explain trade-offs
DON'T: Over-engineer, expand scope without asking
Proactivity: 3 (Balanced) - add tests/docs, ask about refactoring
```

**Bad Quick Reference** (vague):
```
Tone: Professional
Response: They like good explanations
DO: Be helpful
DON'T: Be confusing
```

The profile combines:
- **Environmental facts** (observed data: OS, packages, tools) → Full Profile
- **Analyzed patterns** (inferred from commits, history, configs) → Both sections
- **Interview responses** (stated preferences and priorities) → Prioritize Quick Ref

### Profile Quality Guidelines

- **Be specific**: "Uses pacman + yay for AUR packages" not "uses package managers"
- **Include data**: "Top command: git (23% of history)" not "uses git a lot"
- **Cite sources**: "Based on 73 commits you authored" not "based on commit history"
- **Make inferences explicit**: "Likely focuses on backend (Go + K8s, no frontend frameworks)"
- **Note contradictions**: "VSCode installed but vim used 90% based on history"
- **Verify authorship**: Only attribute commits/code they actually wrote

### Privacy & Security

**NEVER include:**
- Passwords, API keys, tokens, credentials
- Private SSH keys or fingerprints
- Specific server hostnames, IPs, domains
- Email addresses beyond .gitconfig
- Sensitive paths or project names
- Command arguments with credentials

**OK to include:**
- Tool names and versions
- General workflow patterns
- Public dotfile preferences
- Package categories
- System configuration

## Token Budget & Practical Usage

### Target Profile Size

**Quick Reference**: 300-500 tokens (strict limit!)
- At ~4 chars/token, this is ~1200-2000 characters
- Should fit on one screen
- Scannable in 10-15 seconds

**Full Profile**: 2000-3000 tokens
- Complete but concise
- Remove unnecessary detail
- Keep evidence but summarize

**Total Profile**: ~2500-3500 tokens ideal
- Fits comfortably in context
- Can be read at session start without dominating the conversation
- Leaves room for actual work

### How Claude Will Use It

**Every session start**:
1. Read Quick Reference (300-500 tokens)
2. Immediately know: tone, proactivity, detail level, key preferences
3. Apply throughout conversation

**When relevant**:
- Reference Full Profile sections as needed
- "They're learning Rust" → check expertise section
- "Debugging an error" → check debugging communication preferences
- "Should I refactor this?" → check proactivity boundaries

### Writing the Profile

**Be ruthless about brevity**:
- "Casual, emoji OK" NOT "Uses casual tone with occasional emoji for emphasis in commit messages"
- "Proactivity: 4/5" NOT "Comfortable with proactive improvements and refactoring"
- "Pet peeve: Over-engineering" NOT "Dislikes when code is over-engineered with unnecessary abstractions"

**Use dense formats**:
- Scales: "YOLO: 3/5" instead of paragraphs
- Icons: 🎯💼😊🤖📚 for tone categories
- Bullet points, not prose
- Sections, not essays

**Remove redundancy**:
- If it's in Quick Reference, don't repeat in Full Profile
- If it can be inferred, don't state it
- If it's rarely relevant, omit it

## Final Steps

1. **Generate the profile** following the two-tier structure
2. **Review Quick Reference**: Can you read it in 15 seconds? If not, cut more.
3. **Check token count**:
   - Quick Reference: 300-500 tokens (strict!)
   - Full Profile: 2000-3000 tokens
   - Total: ~2500-3500 tokens

4. **Save profile files**:
   - **Quick Reference** → `~/.claude/USER_PROFILE_QUICK.md` (300-500 tokens)
   - **Full Profile** → `~/.claude/USER_PROFILE.md` (2000-3000 tokens)

5. **Update `~/.claude/CLAUDE.md`**:
   - Read existing CLAUDE.md if it exists (user may have custom directives)
   - Add/update a section that references ONLY the quick reference:

   ```markdown
   # User Profile (Auto-generated by /interview)

   Read `~/.claude/USER_PROFILE_QUICK.md` at session start for interaction preferences.

   ---
   ```

   - Place this at the TOP of CLAUDE.md (so it's read first)
   - **ONLY tell Claude to read the quick reference** (not the full profile)
   - The quick reference will mention the full profile exists
   - Preserve any existing user content below the `---` separator
   - If CLAUDE.md doesn't exist, create it with just this directive

6. **Show user the Quick Reference** in your response so they can review it
   - Display the content of USER_PROFILE_QUICK.md
   - Ask: "Does this accurately capture how you want me to interact with you?"
   - They can correct any misunderstandings immediately

7. **Inform user** about the file structure:
   ```
   Files created/updated:
   - ~/.claude/CLAUDE.md (updated to reference profiles)
   - ~/.claude/USER_PROFILE_QUICK.md (your interaction preferences)
   - ~/.claude/USER_PROFILE.md (full detailed profile)
   ```

8. Mention they can:
   - Edit USER_PROFILE_QUICK.md anytime to change how I interact
   - Edit USER_PROFILE.md for detailed context updates
   - Keep their own directives in CLAUDE.md (profile section is marked)
   - Run `/interview` again to regenerate the profile files
   - CLAUDE.md automatically loads these files at every session start

### Post-Interview Message Template

After saving the profile, say something like:

> I've created your user profile! Here's what I set up:
>
> **Files created/updated**:
> - `~/.claude/CLAUDE.md` - Updated to load your profile files at session start
> - `~/.claude/USER_PROFILE_QUICK.md` - Your interaction preferences (Quick Reference)
> - `~/.claude/USER_PROFILE.md` - Full detailed profile
>
> **Here's your Quick Reference** (what I'll read every session):
>
> [Show the content of USER_PROFILE_QUICK.md here]
>
> Does this accurately capture how you want me to work with you? You can edit `USER_PROFILE_QUICK.md` anytime to adjust my behavior.
>
> Your `CLAUDE.md` now tells me to read these files at startup, but any existing directives you had are preserved. The full profile has all the detailed analysis which I'll reference when needed.

## Reference Files

- [environmental-analysis.md](environmental-analysis.md) - Complete checklist of what to analyze
- [analysis-tips.md](analysis-tips.md) - How to interpret findings and patterns
- [profile-template.md](profile-template.md) - Output format and structure

## Key Principles

1. **Verify before attributing** - Don't give credit for work they didn't do
2. **Multiple sources** - Cross-reference git, history, configs, conversation
3. **Explicit about uncertainty** - "Likely..." vs "Confirmed..."
4. **Respect privacy** - Analyze patterns, not sensitive data
5. **Be helpful** - The profile should make future interactions better

---

*See detailed analysis instructions and tips in the reference files above.*
