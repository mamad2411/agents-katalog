Use simple and easy-to-understand language.

# Fundamental Principles
- Write clean, simple, readable code  
- Reliability is the top priority – if you cannot make it reliable, do not build it  
- Implement features in the simplest possible way  
- Keep files small and focused (aim for <200 lines)  
- Test after every meaningful change  
- Focus on core functionality before optimization  
- Use clear, consistent naming  
- Think thoroughly before coding – write 2–3 short reasoning paragraphs before implementing non-trivial changes  
- Leave ego aside when debugging and fixing errors – assume you might be wrong and let the data guide you  

# Scalability & DRY
- Design solutions to be scalable from day one – avoid hardcoded limits and tightly coupled components  
- Follow the DRY (Don’t Repeat Yourself) principle – never duplicate logic when it can be shared  
- Extract reusable utilities, hooks, and components instead of copy–pasting code  
- Prefer modular, composable architecture so features can grow without rewrites  
- Keep boundaries clear between layers (API, services, UI) to make future scaling and refactoring easy  

# Error Fixing
- Consider multiple possible causes before deciding – do not jump to conclusions  
- Explain the problem in plain English before changing code  
- Make the minimal necessary change, touching as few lines as possible  
- Always verify the fix with targeted tests or reproduction steps  
- For unclear errors involving tools, libraries, or APIs, ask the user to perform a Perplexity web search (or similar) to obtain the latest up-to-date information  

# Building Process
- Understand requirements completely before starting  
- Plan the next step in detail before writing code  
- Break tasks into small, manageable chunks  
- Prioritize functionality over aesthetics until core features work reliably  
- Document key decisions and reasoning in simple terms as you go  
- Build incrementally – one piece at a time, testing thoroughly after each addition  
- Refactor regularly for clarity and efficiency, but **only** after confirming functionality  
- Stay mindful of dependencies and avoid overcomplicating integrations  
- Optimize for scalability only after the core system is stable  

# Collaboration
- Communicate assumptions and ask clarifying questions early  
- Review others’ code constructively and accept feedback with humility  
- Share progress frequently to keep stakeholders aligned  
- Use version control effectively to track, isolate, and manage changes  

# Performance
- Monitor performance early, but avoid premature optimization  
- Aim for solutions that are “fast enough” rather than theoretically perfect  
- Profile bottlenecks and address them methodically when needed  

# Security
- Keep sensitive data and credentials secure by default  
- Use established libraries and best practices instead of reinventing the wheel  
- Regularly review the codebase for vulnerabilities and unsafe patterns  

# Logging & Observability
- Use structured logging (JSON or key–value) to make logs machine-readable  
- Log only what is necessary – avoid noise and never log sensitive data  
- Every error should create a meaningful log entry with clear context  
- Include lightweight monitoring (basic metrics, simple health checks)  
- Ensure logs are consistent across backend, frontend, workers, and API layers  
- Logs should make it easy to understand what happened and why  

# Testing & Test Files
- Write simple, focused tests for core functionality before adding complexity  
- Include test files for critical utilities, components, and API endpoints  
- Prefer small, isolated tests over large integrated ones  
- Every new feature should include at least one test verifying expected behavior  
- When fixing a bug, add a test preventing regression  
- Use clear, descriptive test naming (e.g., `should_do_X_when_Y`)  
- Keep test files clean — tests serve as documentation  
- Run tests frequently, especially after meaningful changes  

# Problem Solving
- Start with a clear written definition of the problem  
- Explore solutions systematically and avoid hasty decisions  
- If stuck, step back or explain the issue to gain new perspective  

# Continuous Improvement
- After completing a project, reflect on what went well and what could be improved  
- Stay curious and keep learning from mistakes, peers, and new best practices  
- Regularly revisit older code to keep it clean, reliable, and efficient  

# Overall Attitude
- Embrace simplicity – unnecessary complexity is a liability  
- Be patient and thorough – rushing leads to errors  
- Strive for clarity in everything — code, documentation, reasoning, and communication  

---
alwaysApply: true
---
