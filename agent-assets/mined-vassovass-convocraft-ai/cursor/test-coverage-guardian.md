version: 1

rules:
  - id: test-coverage-guardian
    name: Test Coverage Guardian
    description: |
      Runs the unit test suite with coverage on every push and blocks the push if total coverage is below 80%.
    trigger: prePush
    run: npm run test -- --coverage --color=false
    coverage_threshold: 80
    success_message: "✅ Coverage ≥ 80%. Push allowed."
    failure_message: "❌ Coverage below 80%. Add tests or adjust threshold."
 