# Background Agent Instructions

## Session Handoff Protocol

### 🎯 Primary Objective
Continue autonomous development of EMU Alerts with full YOLO mode enabled.

### 📋 Current State (Session Handoff)

**Project**: EMU Alerts - Emergency Management Unit Alert System  
**Repository**: https://github.com/ynotfins/EMU_v0  
**Branch**: main  
**Mode**: YOLO + Full Autonomous ⚡  
**Dev Server**: http://localhost:3000  

### ✅ Completed (This Session)
1. Memory Bank initialized (6 core files + REFERENCE.md)
2. Fixed 38 TypeScript errors (0 errors now)
3. Installed & configured ESLint
4. Configured VS Code extensions (12 enabled, 46 disabled)
5. Installed tsx for check-env script
6. Synced with GitHub (4 commits pushed)
7. Enabled YOLO + autonomous mode
8. Cleaned up root directory (removed screenshots)
9. Anchored reference docs in Memory Bank

### 🔄 Current Status
- ✅ TypeScript: 0 errors
- ✅ ESLint: Installed (8 lint errors, 5 warnings - code quality)
- ✅ Dev Server: Running
- ✅ Git: Clean working tree, synced
- ✅ Memory Bank: Complete and current
- ⏳ Firebase: Not connected yet (mock data)
- ⏳ v0 Integration: Pending user action

---

## 🚀 Agent Operating Mode

### YOLO Autonomous Rules
Follow `.cursor/rules/yolo-autonomous-mode.mdc`:
- Fix errors immediately without asking
- Refactor proactively
- Install dependencies as needed
- Commit frequently (logical units)
- Push batches (3-5 commits)
- Document after implementation
- Move fast, ship fast

### Commit Conventions
Follow `.cursor/rules/commit-conventions.mdc`:
- Use conventional commit format
- Commit on: feature complete, bug fixed, types fixed, refactor done
- Push strategy: batch related commits
- Atomic commits: one logical change per commit

---

## 📚 Knowledge Base

### Memory Bank Location
`docs/memory-bank/`
- projectbrief.md - Core purpose & goals
- productContext.md - User problems & solutions  
- systemPatterns.md - Architecture & patterns
- techContext.md - Tech stack & setup
- activeContext.md - Current work & issues
- progress.md - Status & roadmap
- REFERENCE.md - Anchored docs index

### Reference Documentation
`docs/`
- README.md - Project overview
- WIRING.md - Firestore schemas & security rules
- EXTENSIONS.md - Firebase Extensions setup
- ROUTES.md - Complete route tree
- COMPONENTS.md - Component catalog
- API_MAP.md - Hooks → Firestore mapping
- TESTPLAN.md - Testing scenarios
- ENV.md - Environment variables

---

## 🎯 Priority Task Queue

### P0 - Critical (Start Here)
1. ✅ Fix remaining ESLint errors (6 in favorites pages, 1 in sidebar)
2. Review Memory Bank activeContext.md for current issues
3. Check for any blocking TypeScript errors
4. Verify dev server is running

### P1 - High Priority
1. Implement Firebase Firestore queries (replace mock data)
   - Start with `useProfile()` hook
   - Then `useIncidents()` hook
   - Reference: `docs/WIRING.md` and `docs/API_MAP.md`
2. Set up Firebase project (when env vars provided)
3. Deploy Firebase security rules
4. Test real-time listeners

### P2 - Medium Priority
1. Add Google Maps integration (MapCard, LiveMap)
2. Implement FCM push notifications
3. Set up Firebase Storage for file uploads
4. Implement e-signature workflow

### P3 - Low Priority
1. Add offline PWA support
2. Implement command palette
3. Add analytics tracking
4. Set up error monitoring

---

## 🔧 Development Workflow

### Session Start Checklist
```bash
# 1. Read Memory Bank
Read all files in docs/memory-bank/

# 2. Check git status
git status
git log --oneline -5

# 3. Verify dev server
curl http://localhost:3000

# 4. Run checks
npm run typecheck
npm run lint  # (optional, warnings OK)

# 5. Review active issues
Check activeContext.md for blockers
```

### Work Session Pattern
```
1. Pick task from priority queue
2. Implement immediately (YOLO mode)
3. Test as you build
4. Commit working state
5. Update Memory Bank if significant
6. Move to next task
```

### Session End Checklist
```bash
# 1. Commit all work
git add .
git commit -m "type: description"

# 2. Push to GitHub (if 3+ commits)
git push origin main

# 3. Update Memory Bank
Update activeContext.md with current state
Update progress.md with completed items

# 4. Document handoff
Note any blockers or pending decisions
```

---

## 🚨 Known Issues & Blockers

### ESLint Warnings (Non-blocking)
- 6 errors: EmptyState component defined inside render (favorites pages)
- 1 error: Math.random() in useMemo (sidebar.tsx)
- 5 warnings: Unused variables, exhaustive deps

### Missing Configuration
- Firebase environment variables not set
- Google Maps API key not configured
- FCM VAPID key not generated

### Pending User Actions
- v0.dev integration (user to connect GitHub repo)
- Firebase project setup (user to create project)
- Domain configuration (4axe.com → future)

---

## 📊 Success Metrics

Track these metrics in Memory Bank progress.md:
- TypeScript errors: 0 (maintain)
- Features implemented vs planned
- Firebase integration progress
- Test coverage (when tests added)
- Performance (lighthouse scores when ready)

---

## 🔗 Important Commands

```bash
# Development
npm run dev              # Start dev server
npm run build            # Production build
npm run typecheck        # Check types
npm run lint             # Check code quality
npm run check-env        # Verify env vars

# Git
git status               # Check status
git log --oneline -10    # Recent commits
git diff                 # Uncommitted changes
git add .                # Stage all
git commit -m "msg"      # Commit
git push origin main     # Push to GitHub

# Firebase (when ready)
firebase login           # Login to Firebase
firebase init hosting    # Initialize hosting
firebase deploy          # Deploy to Firebase
```

---

## 💡 Decision Framework

When facing decisions, use this hierarchy:

1. **Does Memory Bank provide guidance?** → Follow it
2. **Does reference doc (WIRING, etc) specify?** → Follow it
3. **Does YOLO mode allow auto-decision?** → Decide and implement
4. **Is it reversible with git?** → Try it, commit, iterate
5. **Could it break production?** → Implement with tests
6. **Could it lose data?** → Document and ask user

---

## 🎮 Agent Autonomy Level

**FULL AUTONOMY ENABLED** ⚡

You have permission to:
- ✅ Write/modify any code file
- ✅ Install/update dependencies
- ✅ Create/delete files
- ✅ Refactor architecture
- ✅ Fix bugs immediately
- ✅ Add features proactively
- ✅ Commit and push changes
- ✅ Update documentation

**Require user confirmation for**:
- 🛑 Deleting production data
- 🛑 Force pushing to main
- 🛑 Changing auth/payment logic
- 🛑 Removing security features

---

## 📞 Handoff Communication

When returning control to user, provide:
1. **Summary of work completed** (bullet list with ✅)
2. **Commits made** (count and brief description)
3. **Current state** (TypeScript errors, build status, etc)
4. **Next recommended steps**
5. **Any blockers or decisions needed**

Format:
```
# Session Complete

## ✅ Completed
- Fixed X TypeScript errors
- Implemented Y feature
- Refactored Z component

## 📊 Status
- TypeScript: 0 errors
- Commits: 5 (pushed)
- Tests: All passing

## 🔜 Next Steps
1. Continue with Firebase integration
2. Review user feedback
3. Deploy when ready

## 🚧 Blockers
- Need Firebase API keys for real-time features
- Awaiting design approval for X
```

---

## 🔄 Background Agent Ready

This agent is configured for:
- Autonomous development
- Aggressive iteration
- Fast shipping
- Quality maintenance
- Full documentation
- Clean git history

**Status**: Ready to build 🚀  
**Mode**: YOLO ⚡  
**Autonomy**: FULL 💪

