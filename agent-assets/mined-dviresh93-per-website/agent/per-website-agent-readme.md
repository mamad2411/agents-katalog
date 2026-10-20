# Agent System Overview

**Version:** 1.1
**Last Updated:** 2025-10-28

This directory contains specialized agent definitions for automating job search and interview preparation workflows.

---

## 🎯 What Are Agents?

**Agents** are autonomous AI workers that handle complex, multi-step tasks using available tools (commands, files, MCP tools).

**Key Difference from Commands:**
- **Commands** (like `/profile`, `/apply`) load context into the main conversation
- **Agents** work in isolated context, use commands as tools, return results

---

## 📁 Available Agents

| Agent | Command | Purpose | When to Use |
|-------|---------|---------|-------------|
| **Resume Agent** | `/resume [job]` | Generate tailored resumes | Every job application |
| **Network Agent** | `/network [type] [details]` | Draft LinkedIn messages | Recruiter outreach, follow-ups |
| **Interview Coach Agent** | `/interview [company] [type]` | Interview preparation | Practice before interviews |
| **Portfolio Agent** | `/portfolio [action]` | Update portfolio website | Add projects, sync with resume |

---

## 🚀 How to Use Agents

### Resume Generation
```
/resume [paste job description]

Agent will:
1. Analyze job requirements
2. Generate customized scratchpad for review
3. Wait for your approval
4. Generate professional PDF

Time: 20-30 minutes with review
```

### Networking
```
/network connection "Hiring manager at Amazon"
/network follow-up "After applying 5 days ago"
/network thank-you "After phone screen with Sarah"

Agent will:
1. Draft 2-3 message variations
2. Keep it short and human-sounding
3. Iterate based on your feedback

Time: 5-10 minutes
```

### Interview Preparation
```
/interview casium live-coding
/interview amazon system-design
/interview google behavioral

Agent will:
1. Discover existing company prep OR create new structure
2. Load company-specific context
3. Conduct teaching or mock interview
4. Save session notes

Time: 30-60 minutes per session
```

### Portfolio Maintenance
```
/portfolio add-project "GridCOP in production"
/portfolio update-skills "Add CrewAI and MCP"
/portfolio review "Check consistency with resume"

Agent will:
1. Propose changes (show diff)
2. Wait for approval
3. Update JSON files safely

Time: 10-15 minutes
```

---

## 🏗️ Architecture

### Commands = Reusable Tools

General tools that agents use:
- `/profile` - Load user background
- `/apply` - Load resume workflow
- `/context` - Load repo structure

### Company Context = Self-Contained

Company-specific prep lives in company folders:
- `interview-prep/companies/casium/` (existing)
- `interview-prep/companies/amazon/` (auto-created when needed)
- No separate `.claude/commands/{company}.md` files needed!

### Agents = Specialized Workers

Each agent:
- Has specific domain expertise
- Uses tools autonomously
- Works in isolated context
- Returns results to main chat

---

## 📚 Agent Definitions

### Resume Agent (`resume-agent.md`)
- **Workflow:** 7 steps from analysis to PDF
- **Tools:** /profile, /apply, Read, Write, MCP tool
- **Key Feature:** Scratchpad review checkpoint
- **Output:** Professional PDF resume

### Network Agent (`network-agent.md`)
- **Workflow:** Understand → Draft → Iterate
- **Tools:** /profile, Read (networking templates)
- **Key Feature:** Multiple variations (casual, professional, brief)
- **Output:** 2-3 message options

### Interview Coach Agent (`interview-coach-agent.md`)
- **Workflow:** Discover company → Load context → Coach → Save notes
- **Tools:** /profile, Read, Write, Glob
- **Key Feature:** Company context discovery (existing vs. new)
- **Output:** Practice session with notes

### Portfolio Agent (`portfolio-agent.md`)
- **Workflow:** Analyze → Propose → Approve → Update
- **Tools:** /profile, Read, Write
- **Key Feature:** Diff-based approval (show before write)
- **Output:** Updated portfolio JSON files

---

## 🎓 Best Practices

### For Resume Generation
- Always review scratchpad before approving
- Check for false metrics or title inflation
- Verify format standards (3-3-3-2 bullets)
- Edit scratchpad file directly if needed

### For Networking
- Choose variation that matches relationship
- Personalize with specific details
- Keep it short (3-5 sentences max)
- Test: would you want to receive this message?

### For Interview Prep
- Use teaching mode for learning concepts
- Use mock interview mode for realistic practice
- Save notes after each session
- Review previous notes before next session

### For Portfolio Updates
- Review diff carefully before approving
- Verify consistency with resume
- Never approve changes you don't understand
- Portfolio is production site - be cautious

---

## 🔧 How Agents Work (Technical)

### Agent Invocation
1. User runs routing command (e.g., `/resume [job]`)
2. Routing command uses Task tool to launch agent
3. Agent loads definition from this directory
4. Agent executes workflow autonomously
5. Agent returns results to main chat

### Agent Context
- Each agent has isolated context (separate from main chat)
- Agent can call SlashCommand (loads tools into agent context)
- Agent can use Read/Write/Glob (accesses files directly)
- Agent's work doesn't clutter main conversation

### Company Discovery (Interview Agent)
1. Agent uses `Glob("interview-prep/companies/{company}/**")`
2. If found → reads `{company}/README.md` and `{company}/CLAUDE.md`
3. If not found → creates folder structure, gathers context
4. All context persists in files (survives restarts)

---

## 📖 Reference Documentation

**Complete Specification:** `.claude/AGENT_ARCHITECTURE_SPEC.md`
- Full architecture details
- Workflow specifications
- Design decisions and rationale
- Implementation phases
- Testing strategies

**Individual Agent Files:**
- `resume-agent.md` - Resume generation workflow
- `network-agent.md` - Networking message drafting
- `interview-coach-agent.md` - Interview preparation coaching
- `portfolio-agent.md` - Portfolio maintenance

---

## ✅ Quick Reference

### Resume Generation Workflow
```
/resume [job] → Analyze → Scratchpad → Approve → PDF
```

### Networking Workflow
```
/network [type] [details] → Draft variations → Choose/modify → Send
```

### Interview Prep Workflow
```
/interview [company] [type] → Discover context → Practice → Save notes
```

### Portfolio Update Workflow
```
/portfolio [action] → Propose (diff) → Approve → Update JSON
```

---

## 🎯 Success Metrics

**You'll know the system is working when:**
- Resume generation takes 20-30 minutes (down from 1-2 hours)
- All resumes follow consistent format (3-3-3-2 bullets)
- Networking messages sound human (not AI-generated)
- Interview prep context persists across sessions
- Portfolio updates require approval (safety checkpoint)

---

## 🐛 Troubleshooting

### Agent not responding?
- Check that routing command exists (`.claude/commands/{agent}.md`)
- Check that agent definition exists (`.claude/agents/{agent}-agent.md`)
- Verify Task tool is available

### Company context not loading?
- Check folder exists: `interview-prep/companies/{company}/`
- Check `CLAUDE.md` exists in company folder
- Use Glob to verify: `Glob("interview-prep/companies/{company}/**")`

### Resume format inconsistent?
- Check baseline resume: `job-prep/applications/_resources/baseline-resume-data.json`
- Check format standards: `job-prep/applications/_resources/FORMAT-STANDARDS.md`
- Remind agent to verify format checklist

### Portfolio changes not applying?
- Check if approval was given (agent waits for approval)
- Verify JSON structure is valid
- Check file permissions on `data/` directory

---

## 📝 Notes

- **Agents use tools** - They call `/profile`, `/apply`, etc. via SlashCommand
- **Company context is self-contained** - No separate command files needed
- **Everything persists** - All context in files, survives restarts
- **Human-in-the-loop** - Approval checkpoints for quality and safety
- **Consistent and scalable** - Add new companies/agents without changing existing code

---

**Questions?** Check the full specification in `.claude/AGENT_ARCHITECTURE_SPEC.md` or ask in main conversation.
