---
name: rn-forge
description: Generate production-ready React Native screens with React Query, typed navigation, and enterprise standards
category: software-development
triggers:
  - "create react native screen"
  - "build mobile screen"
  - "generate rn"
---

# React Native Screen Generation

Generate complete React Native features following enterprise patterns.

## Instructions

1. Read `agents/rn-forge.md` for the full RN code generation workflow
2. Read `react/REACT_QUERY_RULES.md` and `react/REACT_NATIVE_PATTERNS.md`
3. React Query MANDATORY. FlatList for all dynamic lists. StyleSheet.create always
4. Data fetching at the leaf level — each component fetches its own data
5. Reuse existing components — search codebase first, refactor god components
6. Always include: Screen + Components + Hooks + Queries + Service + Tests
7. SafeAreaView, KeyboardAvoidingView, Platform.select for iOS/Android
8. Handle loading, error, empty states. Haptic feedback for confirmations
