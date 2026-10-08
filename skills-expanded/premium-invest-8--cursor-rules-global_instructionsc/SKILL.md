# 🤖 PROJECT-WIDE MANDATORY INSTRUCTIONS

---

## 🛑 MANDATORY STEP 1: READ AI_DESIGN_RULES.MD
**EVERY AI AGENT MUST READ `AI_DESIGN_RULES.md` BEFORE MODIFYING ANY FILE.**
- You must acknowledge you have read it in your first response.
- You must strictly follow the **Isolation Rule** (one folder per page, one `.module.css` per page).

---

## 🛠️ AUTOMATION & EFFICIENCY RULES
To save user **Credits, Time, and Money**, follow these automation protocols:

1. **Auto-Navigate:** After any UI change, you MUST navigate the internal browser to the modified page (e.g., `http://localhost:3000/blog`) so the user can immediately see the changes in their view.
2. **Internal Verification:** You may use the browser internally to verify code correctness, but don't waste time/credits taking screenshots unless specifically asked or if you see an error you need to document.
3. **Approval Flow:** NEVER push to Git/Staging without a verbal "Okay" from the user. Use the phrase: "The changes are live in your dev browser. Does it look good to push to staging?"
4. **Efficiency:** Do not re-install npm packages or clear caches unless a build error specifically requires it.
5. **Conflict Resolution:** Resolve code conflicts manually using `read_file`. Do not use `git revert` or massive file overwrites.

---

## 🎨 DESIGN STANDARDS
- **Branding:** Gold gradients (`#DAA520`, `#C0A062`), Pure Black backgrounds, Glassmorphism (`backdrop-blur-20px`).
- **Mobile First:** Navigation must include the `LuxuryMobileDock`.
- **Isolation:** Page-specific CSS belongs in `.module.css`.

---

## 🧠 PERSISTENT MEMORY
- **Location:** `C:\Users\admin`
- **Branching:** Work on `staging` first.
- **Scripts:** Use `update-staging.ps1` for staging and `publish-to-main.ps1` for production.
