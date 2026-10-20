# Claude Development Guidelines

This file contains mandatory guidelines that Claude must follow when working on this project.

## ⚠️ CRITICAL: Pre-Commit Testing Checklist

**NEVER commit or push code without completing ALL of these steps:**

### 1. Build Verification ✅
```bash
npm run build
```
- ✅ Main process builds without errors
- ✅ Renderer process builds without errors
- ✅ No TypeScript compilation errors

### 2. Development Testing ✅
```bash
# Test that dev servers start correctly
npm run dev
```
- ✅ Vite dev server starts on port 3000
- ✅ Electron main process compiles and starts
- ✅ App window opens without crashes
- ✅ Basic UI renders correctly

### 3. Functionality Testing ✅
**For each new feature, manually verify:**
- ✅ UI components render as expected
- ✅ User interactions work (buttons, forms, etc.)
- ✅ Data loading and error states function
- ✅ No console errors in DevTools
- ✅ App doesn't crash during normal use

### 4. Code Quality Checks ✅
```bash
# Run linting if available
npm run lint || echo "No lint script found"

# Run type checking
npm run typecheck || echo "No typecheck script found"
```

### 5. Git Workflow ✅
```bash
# Stage changes
git add .

# Check what's being committed
git status
git diff --cached

# Commit with descriptive message
git commit -m "Clear, descriptive commit message"

# Push to remote
git push origin main
```

## 📋 Development Workflow

### Before Starting Any Task:
1. Update todo list with current task as "in_progress"
2. Understand the requirements clearly
3. Plan the implementation approach

### During Development:
1. Write code incrementally
2. Test each component as you build it
3. Handle error cases and edge cases
4. Add proper TypeScript types

### Before Committing:
1. **MANDATORY**: Complete the Pre-Commit Testing Checklist above
2. Update todo list to mark task as "completed"
3. Write clear commit message explaining what was implemented
4. Include any breaking changes or setup requirements

### After Pushing:
1. Verify the push was successful
2. Update project documentation if needed
3. Move to next task in todo list

## 🧪 Testing Commands

### Quick Development Test
```bash
# Start dev environment and verify it works
npm run dev
# Let it run for 10-15 seconds, then Ctrl+C
# Check that both Vite and Electron started without errors
```

### Full Build Test
```bash
# Clean build test
npm run build
ls -la dist/  # Verify build outputs exist
```

### Production Simulation
```bash
# Test the built version (when available)
npm run package || echo "Package script not yet implemented"
```

## 🚫 Never Do These Things:

1. **Never commit without testing** - This causes broken builds and wasted time
2. **Never push untested code** - Always verify functionality works as expected
3. **Never ignore build errors** - Fix all TypeScript and build issues before committing
4. **Never commit work-in-progress** - Only commit completed, tested features
5. **Never skip the Pre-Commit Checklist** - This is mandatory, not optional

## 📝 Commit Message Format

Use this format for all commits:
```
Complete [Week X Task Y]: [Brief description]

- [Specific change 1]
- [Specific change 2]  
- [Specific change 3]

✅ [Week X Task Y]: [Task name] - COMPLETED

[Optional: Additional details about implementation]

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## 🔧 Project-Specific Guidelines

### Stock Scanner App:
- Always test stock data fetching (even with mock data)
- Verify UI updates correctly with data changes
- Test add/remove watchlist functionality
- Check that refresh button works and shows loading states
- Ensure error messages display properly
- Test responsive behavior of the interface

### Performance Considerations:
- Keep API calls efficient with caching
- Avoid memory leaks in React components
- Test with multiple stocks in watchlist
- Monitor console for performance warnings

## 📊 Progress Tracking

- Always update TodoWrite tool when starting/completing tasks
- Mark tasks as "in_progress" when beginning work
- Mark tasks as "completed" only after full testing
- Never mark incomplete or broken features as complete

---

**Remember: Quality over speed. It's better to deliver one fully tested, working feature than multiple broken ones.**