---
description:
globs:
alwaysApply: false
---


this is an mvp, only do things that are very bessary for the app to do what it is suposed to do and avoid all the fancy stuff



# 🤖 Agent Rules for AI Platform Development

## 🎯 PROJECT MISSION
Build a **minimal, functional Zoho-like platform** with AI agents in **2 months**. Focus on core functionality, not perfection.

---

## 📋 CORE DEVELOPMENT PRINCIPLES

### 1. **SIMPLICITY FIRST**
- ❌ **NO** complex features unless explicitly in the plan
- ❌ **NO** advanced animations, fancy UI effects, or over-engineering
- ✅ **YES** to minimal, clean, functional interfaces
- ✅ **YES** to the simplest solution that works

### 2. **SCOPE DISCIPLINE**
- **STICK TO THE PLAN** - If it's not in `project_details.md` or `project_plan.md`, don't build it
- **NO FEATURE CREEP** - Resist adding "nice-to-have" features
- **MVP MINDSET** - Build the minimum viable version first
- **NO PREMATURE OPTIMIZATION** - Make it work, then make it better (if time allows)

### 3. **TIME-BOXING**
- **Maximum 1 day per module** - If something takes longer, simplify it
- **No rabbit holes** - If stuck for >2 hours, find a simpler approach
- **Progress over perfection** - A working simple feature beats a perfect incomplete one

---

## 🏗️ TECHNICAL GUIDELINES

### 4. **AUTHENTICATION STRATEGY**
- **Use Auth0** for main dashboard authentication (as specified)
- **Simple token-based auth** for subdomain apps
- **NO complex SSO implementations** - Use the simplest auth flow that works
- **Auto-account creation** for subdomain apps based on main dashboard user data

### 5. **ARCHITECTURE RULES**
- **Keep it simple** - No microservices, no complex patterns
- **Use existing components** - Leverage what's already built
- **Minimal database schema** - Only essential fields
- **RESTful APIs** - Standard HTTP methods, no GraphQL complexity

### 6. **UI/UX CONSTRAINTS**
- **Use existing UI components** from `components/ui/`
- **NO custom design systems** - Stick to Tailwind + shadcn/ui
- **Mobile-responsive by default** but don't over-optimize
- **Consistent layouts** - Reuse dashboard patterns

---

## 📱 MODULE DEVELOPMENT RULES

### 7. **MODULE CREATION PROCESS**
1. **Start with the simplest version** - Basic CRUD operations
2. **Use placeholder content** for complex features
3. **Focus on navigation and basic functionality**
4. **AI features should be simple prompts/responses** - No complex ML models

### 8. **INTEGRATION PRINCIPLES**
- **Mock external APIs** first, implement later if time allows
- **Use webhooks sparingly** - Only for essential real-time features
- **Simple data sync** - Basic API calls, no complex orchestration

---

## 🚫 THINGS TO AVOID

### 9. **FORBIDDEN FEATURES** (Unless explicitly required)
- Complex animations or transitions
- Advanced search/filtering (basic search only)
- Real-time collaboration features
- Complex permissions systems (simple role-based only)
- Advanced analytics or reporting (basic stats only)
- File upload/management systems (unless core to module)
- Complex forms with validation (keep forms simple)
- Advanced caching mechanisms
- Complex error handling (basic try/catch only)

### 10. **TECHNICAL DEBT TOLERANCE**
- **Hardcoded values are OK** for MVP
- **Duplicate code is acceptable** if it saves time
- **Basic error handling** - Don't build comprehensive error systems
- **Simple state management** - Use React state, avoid complex state libraries

---

## ✅ SUCCESS METRICS

### 11. **DEFINITION OF DONE**
For each module:
- [ ] Basic navigation works
- [ ] Core functionality demonstrated
- [ ] Responsive on desktop/mobile
- [ ] Integrates with auth system
- [ ] Can be accessed from main dashboard

### 12. **PRIORITY ORDER**
1. **Auth system + Dashboard navigation** (Week 1)
2. **Core business modules** (Sales, Finance, HR) (Weeks 2-4)
3. **AI agent placeholders** (Week 5-6)
4. **Subdomain integration** (Week 7)
5. **Testing & deployment** (Week 8)

---

## 🛠️ DEVELOPMENT WORKFLOW

### 13. **DAILY RULES**
- **Start with the hardest/riskiest part** of each module
- **Build in 4-hour blocks** - Complete small features quickly
- **Test as you build** - Don't accumulate testing debt
- **Document decisions** but keep it brief

### 14. **WHEN STUCK**
1. **Ask: "What's the simplest version?"**
2. **Look for existing patterns** in the codebase
3. **Use placeholder/mock data** to unblock UI development
4. **Focus on happy path** - edge cases can wait

---

## 🎯 AGENT BEHAVIOR GUIDELINES

### 15. **CODE GENERATION RULES**
- **Prefer editing existing files** over creating new ones
- **Use TypeScript** but don't over-type everything
- **Follow existing patterns** in the codebase
- **Keep functions small and focused**
- **Use modern React patterns** (hooks, functional components)

### 16. **DECISION MAKING**
- **When in doubt, choose the simpler option**
- **Prefer proven solutions** over cutting-edge tech
- **Ask for clarification** only if it blocks critical functionality
- **Default to "good enough"** rather than perfect

---

## 🚀 FINAL REMINDER

**THIS IS A 2-MONTH SPRINT** - Every decision should optimize for:
- **Speed of development**
- **Functional completeness**
- **User experience basics**
- **Meeting the deadline**

**NOT for:**
- Code perfection
- Advanced features
- Complex optimizations
- Future-proofing

---

*Remember: A working simple platform in 2 months is infinitely better than a perfect incomplete one.*
