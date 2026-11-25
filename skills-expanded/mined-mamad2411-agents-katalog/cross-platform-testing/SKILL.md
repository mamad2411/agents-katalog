---
name: cross-platform-testing
version: 1.0.0
min_mindforge_version: 10.4.0
status: stable
triggers: cross-platform testing, device farm testing, screenshot comparison test, platform-specific testing, mobile CI pipeline, Appium testing, Detox testing, XCTest UITest, mobile test automation, device matrix coverage, mobile E2E testing, visual regression mobile
---

# Skill — Cross-Platform Mobile Testing

## When this skill activates
This skill activates when implementing comprehensive mobile testing strategies, including device farm integration, screenshot testing, platform-specific behavior validation, or CI/CD pipelines for mobile apps.

## Mandatory actions when this skill is active

### Before writing any code
1. Define device matrix covering target OS versions, screen sizes, and hardware capabilities (prioritize based on user analytics)
2. Choose testing framework appropriate for platform (XCTest/XCUITest for iOS, Espresso/UIAutomator for Android, Detox/Appium for cross-platform)
3. Establish screenshot testing baseline images and tolerance thresholds for visual regression detection
4. Design test data strategy — use factories/fixtures, implement proper setup/teardown, ensure test isolation

### During implementation
- Write tests at appropriate levels: unit tests for business logic, integration tests for data flows, E2E tests for critical user journeys
- Implement proper test identifiers (testID, accessibilityIdentifier) in UI components for reliable element selection
- Use page object pattern or similar abstraction to decouple tests from UI implementation details
- Configure screenshot testing with proper device/OS-specific baselines to handle platform rendering differences
- Implement retry logic for flaky tests caused by animation timing, network delays, or platform quirks
- Set up parallel test execution on device farms (Firebase Test Lab, AWS Device Farm, BrowserStack) for faster feedback
- Handle platform-specific behaviors explicitly in tests (Android back button, iOS swipe gestures, permission dialogs)

### After implementation
- Run full test suite on representative device matrix, not just emulators/simulators
- Review test flakiness rates and fix or quarantine unstable tests
- Integrate tests into CI pipeline with proper failure reporting and artifact collection (screenshots, logs, videos)
- Validate test coverage for critical paths and high-risk areas (payments, authentication, data sync)

## Self-check before task completion
- [ ] Test suite runs reliably across multiple devices and OS versions with <5% flakiness
- [ ] Screenshot tests catch visual regressions without excessive false positives
- [ ] Platform-specific behaviors are tested correctly (back button, deep links, system gestures)
- [ ] CI pipeline provides clear failure reporting with screenshots/videos for debugging
- [ ] E2E tests cover critical user journeys end-to-end, including error scenarios
- [ ] Test execution time is reasonable (use parallelization, split test suites if needed)
