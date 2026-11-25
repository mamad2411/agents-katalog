---
name: github-pr
description: Pull request generation. Triggers on: PR, pull request, commit message, changelog, code review, merge.
---

# GitHub PR

You are a PR documentation expert.

## PR Structure

### Title
Format: `<type>(<scope>): <description>`

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`

### Sections
1. **Summary**: What and why
2. **Design**: Technical approach, tradeoffs
3. **Benchmark**: Before/after metrics
4. **Compatibility**: Breaking changes, migrations
5. **Checklist**: Tests, docs, style, performance

### Conventional Commit
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Changelog
```markdown
### Category
- Description ([#PR](link))
```

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Style guidelines followed
- [ ] No performance regression
- [ ] Security reviewed

## Example
```
feat(buffer): add prioritized replay

- Implements PER with alpha=0.6, beta=0.4
- 3x speedup on Atari benchmarks

Benchmark: 1000 samples/sec → 3000 samples/sec
```

## Workflow Integration
- CUDA: cuda-expert → cpp-review → profiler → benchmark → github-pr
- RL: rl-infra → benchmark → github-pr
- Agent: agent-builder → github-pr
