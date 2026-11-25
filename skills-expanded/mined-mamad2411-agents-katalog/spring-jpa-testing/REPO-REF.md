# Repo Ref
- source: https://github.com/mamad2411/agents-katalog (path: skills-expanded/mined-NeverSight-learn-skills.dev/spring-jpa-testing/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: @DataJpaTest requires TestEntityManager + flush()/clear() before assertions — without this, tests read from Hibernate L1 cache and pass falsely. Read before writing any JPA test. Triggers: @DataJpaTes
