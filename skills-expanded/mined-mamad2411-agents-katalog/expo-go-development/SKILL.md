---
name: expo-go-development
description: Expert in Expo Go development for React Native apps. Covers when to use Expo Go vs development builds, best practices, common limitations, and migration strategies.
risk: unknown
source: community
date_added: '2026-08-07'
---

## Use this skill when

- Developing React Native apps with Expo
- Deciding between Expo Go and development builds
- Setting up new Expo projects
- Converting HTML UI mockups to React Native/Expo
- Needing guidance on Expo Go limitations and compatibility
- Migrating from Expo Go to development builds

## Do not use this skill when

- Working with pure native iOS/Android development without Expo
- Needing custom native modules not supported by Expo
- Task is unrelated to React Native or Expo development

## Instructions

### Expo Go vs Development Builds

**Expo Go** is best for:
- Quick prototyping and development
- Learning React Native
- Apps using only standard Expo SDK packages
- Testing with commonly used libraries (reanimated, gesture handler, etc.)
- Push notifications, deep links, and routing via Expo Router

**Development Builds** are required when:
- Using local Expo modules (custom native code in `modules/`)
- Need Apple targets (widgets, app clips, extensions)
- Using third-party native modules not included in Expo Go
- Custom native configuration that can't be expressed in `app.json`

### Best Practices

1. **Always try Expo Go first** before creating custom builds
2. **Use TypeScript** for better type safety and developer experience
3. **Use file-based navigation** with Expo Router
4. **Configure ESLint and Prettier** for consistent code style
5. **Set up CI/CD** with linting, tests, and TypeScript checks
6. **Add error boundaries** for better error handling
7. **Check library compatibility** using React Native Directory

### When to Switch from Expo Go

You need `npx expo run:ios/android` or `eas build` ONLY when:
- Local Expo modules are needed
- Custom native configuration is required
- Third-party native modules not in Expo Go
- Apple-specific features (widgets, app clips)

### Development Workflow

1. **Start with Expo Go**: Run `npx expo start` and scan QR code
2. **Test thoroughly** in Expo Go before custom builds
3. **Only create custom builds when required**
4. **Use expo-dev-client** for development builds when needed

### Limitations of Expo Go

- Fixed set of native libraries (cannot add custom native code)
- Some third-party libraries with native code won't work
- Cannot change app name, icon, or other native properties
- Limited to pre-compiled native modules

### Migration to Development Builds

1. Install `expo-dev-client` library
2. Generate native android/ios directories
3. Build native app using `npx expo run:ios` or `npx expo run:android`
4. Or use EAS Build for cloud builds

### Code Style Guidelines

- Use kebab-case for file names (e.g., `comment-card.tsx`)
- Always use import statements at the top
- Remove old route files when restructuring navigation
- Never use special characters in file names
- Configure tsconfig.json with path aliases
- Prefer aliases over relative imports for refactors

### HTML to React Native Conversion

When converting HTML mockups to React Native/Expo:
- Replace HTML elements with React Native components
- Convert CSS to React Native StyleSheet
- Use `View` instead of `div`, `Text` instead of `span/p`
- Convert inline styles to StyleSheet objects
- Handle event handlers with camelCase naming
- Use `className` becomes `style` in React Native

### Common Patterns

- **Navigation**: Use Expo Router with file-based routing
- **Styling**: Use StyleSheet.create() or styled-components
- **State Management**: Context API, Redux, or Zustand
- **API Calls**: Use async/await with fetch or axios
- **Icons**: Use @expo/vector-icons or react-native-vector-icons