---
name: "tutorial-patterns"
description: "Tutorial writing patterns: tutorial vs how-to, the working state principle, atomic steps, expected output, checkpoints, honest prerequisites, destination first, and anti-patterns such as the magic step. Use when writing or reviewing tutorial steps."
---

# Tutorial Patterns

## Tutorial vs. How-to Guide: The Critical Distinction

Before writing, identify which document is actually needed:

| Tutorial | How-to Guide |
|----------|-------------|
| "Build a REST API in Node.js" | "Add JWT authentication to your Express API" |
| For someone new to this | For someone who knows the domain |
| Explains why each step is done | Steps are efficient, minimal explanation |
| Has checkpoints, explores | Numbered steps, no detours |
| Learner reaches a complete artifact | Learner accomplishes a specific task |

A how-to guide written as a tutorial is too long. A tutorial written as a how-to guide leaves the learner without understanding.

## The Working State Principle

The most important structural rule: the project must be in a runnable, working state at the end of every section. Never leave the learner in a broken state between sections.

```markdown
# Bad: section ends in broken state
## Section 2: Add authentication

[Steps that add an auth middleware that references a function not yet created]

## Section 3: The auth function
[Creates the function that Section 2 needed]

# Good: each section is independently runnable
## Section 2: Add the auth middleware

[Step 1: Create the auth function placeholder]
[Step 2: Wire up the middleware using the placeholder]
[Checkpoint: verify the API still responds on localhost:3000]

## Section 3: Implement the auth logic

[Step 1: Replace placeholder with real implementation]
[Checkpoint: verify auth is now enforced]
```

## The Atomic Step Rule

Every step must be one action. If a step contains "and", it should be split:

```markdown
# Bad: compound step
3. Create the configuration file and add your database connection string.

# Good: split into atomic steps
3. Create the configuration file:
   ```bash
   touch .env
   ```

4. Add your database connection string to `.env`:
   ```bash
   DATABASE_URL="postgresql://user:password@localhost:5432/myapp"
   ```
```

Each atomic step has one command, one verification, one "what this means" sentence.

## The Expected Output Pattern

Every step that produces observable output must show what that output looks like. The learner must know it worked without having to guess:

```markdown
# Bad: step with no verification
5. Start the development server:
   ```bash
   npm run dev
   ```

# Good: step with expected output
5. Start the development server:
   ```bash
   npm run dev
   ```

   **Expected output:**
   ```
   ▲ Next.js 14.0.1
   - Local: http://localhost:3000
   - Network: http://192.168.1.5:3000
   ✓ Ready in 1.2s
   ```

   Visit `http://localhost:3000`. You should see the default Next.js page.

   > **Troubleshooting**: If you see `EADDRINUSE`, port 3000 is already in use.
   > Run `npx kill-port 3000` and try again.
```

## The Checkpoint Pattern

Checkpoints serve two functions:
1. They help learners verify they are on track before continuing
2. They provide an escape hatch (reference branch) if the learner is stuck

Place checkpoints after every 3-5 steps, or at every major section boundary:

```markdown
#### Checkpoint: After Step 5

Your project should be in this state:

- [ ] `package.json` includes `express`, `typescript`, `ts-node` as dependencies
- [ ] `tsconfig.json` exists with `"strict": true`
- [ ] `src/index.ts` starts a server on port 3000
- [ ] Running `npm run dev` shows "Server started on :3000"
- [ ] `curl http://localhost:3000` returns HTTP 200

If any of these are not working, compare with the
[checkpoint-step-5 branch](https://github.com/example/tutorial/tree/checkpoint-step-5).

Checkout to reset to this state:
```bash
git clone https://github.com/example/tutorial.git
git checkout checkpoint-step-5
npm install
```
```

## The Honest Prerequisites Pattern

Vague prerequisites cause tutorials to fail at step 3. Be specific about what the learner needs to know, and what they will not learn in this tutorial:

```markdown
# Bad prerequisites: vague
Prerequisites: JavaScript, Node.js, some SQL experience

# Good prerequisites: specific
**This tutorial assumes you know:**
- JavaScript ES2017+ (async/await, destructuring, arrow functions)
- What an HTTP endpoint is (method + URL + response)
- Basic SQL: SELECT, INSERT, WHERE

**You do not need to know:**
- TypeScript (we will introduce the necessary syntax as we go)
- Any specific ORM or database driver

**Install before starting:**
- Node.js 18+ -- run `node -v` to check
- PostgreSQL 14+ running locally (or use the Docker alternative below)

**Not sure if you are ready?** If you can complete
[this prerequisite exercise](link) comfortably, you are ready.
```

## The Destination-First Pattern

Show what the learner will build before asking them to follow steps. Motivation sustains effort through difficulty:

```markdown
# Good tutorial opening
By the end of this tutorial, you'll have a working search API
that accepts keyword queries and returns ranked results.

Here is the final query:
```bash
curl "http://localhost:3000/search?q=climate+change&limit=5"
```

And the response:
```json
{
  "query": "climate change",
  "results": [
    { "id": 1, "title": "...", "score": 0.94 },
    { "id": 2, "title": "...", "score": 0.87 }
  ],
  "total": 142
}
```
```

## Anti-Patterns

### The Magic Step
```
# Bad: command without context
8. Run `npx prisma generate`.

# Good: command with explanation
8. Generate the Prisma client from your schema:
   ```bash
   npx prisma generate
   ```
   This creates type-safe TypeScript types for all your database models.
   Every time you change `schema.prisma`, run this command to update the types.
```

### The Abandoned Learner
Every common error point needs a troubleshooting note. If the tutorial has been followed by 10 people and 3 got stuck at step 5, step 5 needs troubleshooting text.

### The Prerequisites Lie
If the learner needs to understand TypeScript generics to complete step 4, "TypeScript basics" is not an honest prerequisite. Either teach the concept in-context, add it to prerequisites explicitly, or redesign the step to avoid it.

### The Stale Tutorial
Pin all package versions and note the tutorial date. Undated tutorials with unpinned versions are traps:
```markdown
# In package.json
{
  "dependencies": {
    "express": "4.18.2",   // pin versions
    "typescript": "5.3.2"
  }
}

# At the top of the tutorial
**Last updated**: 2024-03-15
**Tested with**: Node.js 20.11, npm 10.2
```

## References
- [Diataxis Framework](https://diataxis.fr/) - The definitive framework for documentation types
- [The Good Docs Project](https://thegooddocsproject.dev/)
- [Write the Docs](https://www.writethedocs.org/)
- [Bloom's Taxonomy](https://en.wikipedia.org/wiki/Bloom%27s_taxonomy) - Learning hierarchy for tutorial design
