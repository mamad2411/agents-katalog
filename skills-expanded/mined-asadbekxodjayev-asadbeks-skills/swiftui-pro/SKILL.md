# SwiftUI Pro - Code Review

This is a comprehensive SwiftUI code review specification authored by Paul Hudson, licensed under MIT.

## Key Directives
- Reviews should validate Swift/SwiftUI code against modern APIs, maintainability, and performance standards
- Process follows 9 sequential checks: deprecated APIs, view optimization, data flow, navigation, design compliance, accessibility, performance, Swift conventions, and code hygiene
- Target iOS 26+ and Swift 6.2 with modern concurrency patterns
- Prioritize SwiftUI over UIKit unless explicitly requested
- Organize files by feature rather than type
- No third-party frameworks without user approval

## Output Requirements
- Organize findings by filename
- Format each issue with location, rule name, and before/after code examples
- End with prioritized summary of high-impact changes
- Only report genuine problems — avoid speculation or minor nitpicks
- Skip files without issues

## Reference Categories

The document includes reference categories covering:
- **Accessibility**: Dynamic Type, VoiceOver, Reduce Motion
- **Deprecated APIs**: iOS 26+ replacements
- **Design Guidelines**: HIG compliance
- **Code Hygiene**: Swift 6 idioms
- **Navigation**: NavigationStack, sheets, full-screen covers
- **Performance**: rendering, lazy loading, task cancellation
- **Data Flow / State Management**: @Observable, @State, @Binding, environment
- **Swift Idioms**: actors, async/await, structured concurrency
- **View Composition**: extracting subviews, avoiding body complexity
