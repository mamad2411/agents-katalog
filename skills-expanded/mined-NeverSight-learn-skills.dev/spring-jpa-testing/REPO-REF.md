# Repo Ref
- source: https://github.com/NeverSight/learn-skills.dev (path: data/skills-md/spring-ai-community/spring-testing-skills/spring-jpa-testing/SKILL.md, branch: main)
- mined: 2026-10-14
- desc: @DataJpaTest requires TestEntityManager + flush()/clear() before assertions — without this, tests read from Hibernate L1 cache and pass falsely. Read before writing any JPA test. Triggers: @DataJpaTes
