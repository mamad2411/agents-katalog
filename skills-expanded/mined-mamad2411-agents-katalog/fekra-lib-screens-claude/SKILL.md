# Screens Folder Documentation

## Purpose
The `screens/` folder contains all UI screen implementations organized by feature domain. Each subfolder represents a major functional area of the Fekra application, from authentication to content generation.

## Key Components

### Authentication Flow (`auth/`)
- **welcome_screen.dart** - Onboarding screen with OAuth options (Apple, Google) and email sign-in entry point
- **sign_in_screen.dart** - Email-based authentication with form validation
- **sign_up_screen.dart** - User registration with account creation

### Main Navigation Hub (`home/`)
- **home_screen.dart** - Primary navigation screen with bottom tab bar (Ideas, Categories, Profile) and floating action button for recording
- **home_screen_new.dart** - Alternative/updated home screen implementation

### Core Feature Screens
- **recording/** - `recording_screen.dart` - Voice recording interface with audio controls and visualization
- **transcription/** - `transcription_screen.dart` - Speech-to-text processing and transcript editing
- **content_generation/** - `content_generation_screen.dart` - AI-powered PRD and implementation guide generation

### Content Management
- **ideas/** - Idea management screens
  - `ideas_list_screen.dart` - List view of all user ideas with filtering/sorting
  - `idea_detail_screen.dart` - Detailed view of individual ideas with PRD and implementation guides
- **categories/** - `categories_screen.dart` - Category management for organizing ideas

### User Management
- **profile/** - `profile_screen.dart` - User profile information and account management
- **settings/** - Comprehensive settings management with modular sections:
  - `settings_screen.dart` - Main settings container with all sections
  - `user_profile_section.dart` - Profile information management
  - `authentication_settings_section.dart` - Account and authentication settings
  - `app_preferences_section.dart` - App behavior and appearance preferences
  - `voice_recording_settings_section.dart` - Audio recording configuration
  - `ai_configuration_section.dart` - AI service settings and preferences
  - `data_management_section.dart` - Data storage and export/import options
  - `about_section.dart` - App information, version, and legal content

## Organization Pattern

### Feature-Based Structure
Each major feature has its own directory with related screens:
```
screens/
├── auth/           # Authentication flow
├── home/           # Main navigation
├── recording/      # Voice recording
├── transcription/  # Speech-to-text
├── content_generation/ # AI content creation
├── ideas/          # Idea management
├── categories/     # Category management
├── profile/        # User profile
└── settings/       # App configuration
```

### Modular Settings Design
The settings folder demonstrates excellent modularization:
- **Main Container**: `settings_screen.dart` orchestrates all sections
- **Feature Sections**: Each aspect of settings is in its own file
- **Reusable Components**: Settings components are centralized in widgets

### Navigation Hierarchy
1. **Entry Point**: `welcome_screen.dart` → Authentication
2. **Main Hub**: `home_screen.dart` → All primary features
3. **Feature Flows**: Recording → Transcription → Content Generation → Idea Detail
4. **Management**: Categories, Profile, Settings accessible from main navigation

## Navigation Flow

### Primary User Journey
```
Welcome Screen → Auth → Home Screen → Recording → Transcription → Content Generation → Idea Detail
                            ↓
                    Categories / Profile / Settings
```

### Screen Transitions
- **Bottom Navigation**: Ideas ↔ Categories ↔ Profile (via home_screen.dart)
- **Modal Navigation**: Recording, Transcription, Content Generation (full-screen modals)
- **Stack Navigation**: Welcome → Sign In/Up → Home, Idea List → Idea Detail
- **Settings Navigation**: Settings Screen → Various Setting Sections

### Navigation Implementation
- **HomeScreen** acts as the main navigation controller with bottom tabs
- **Floating Action Button** provides quick access to recording from any main tab
- **Modal presentations** for workflow screens (recording, transcription, generation)
- **Standard push navigation** for detail views and settings

## Screen Responsibilities

### Authentication Screens
- **WelcomeScreen**: Onboarding, OAuth, email entry point
- **SignInScreen**: Email/password authentication
- **SignUpScreen**: New account creation

### Core Workflow Screens
- **RecordingScreen**: Audio capture with real-time feedback
- **TranscriptionScreen**: Speech-to-text processing and editing
- **ContentGenerationScreen**: AI-powered content creation
- **IdeaDetailScreen**: Comprehensive idea view with all generated content

### Management Screens
- **IdeasListScreen**: Idea browsing, filtering, and organization
- **CategoriesScreen**: Category creation and management
- **ProfileScreen**: User account information
- **SettingsScreen**: Comprehensive app configuration

### Settings Sub-Screens
- **UserProfileSection**: Personal information management
- **AuthenticationSettingsSection**: Account security and authentication
- **AppPreferencesSection**: UI preferences and app behavior
- **VoiceRecordingSettingsSection**: Audio quality and recording settings
- **AIConfigurationSection**: AI service configuration and API settings
- **DataManagementSection**: Storage, backup, and data operations
- **AboutSection**: App information, version, terms, and support

## Duplication Check

### Potential Duplication Areas
- **Home Screens**: `home_screen.dart` and `home_screen_new.dart` suggest possible iteration/refactoring
- **No other significant duplication** - Each screen has a distinct purpose

### Design Consistency
- All screens follow consistent theming using `AppColors` and `AppConstants`
- Common navigation patterns and transition animations
- Consistent error handling using `ErrorHandler` utility
- Shared loading states and progress indicators

## Usage Patterns

### Screen State Management
```dart
// Provider pattern for state management
Consumer<AuthProvider>(builder: (context, authProvider, child) { ... })
Consumer2<AuthProvider, SettingsProvider>(builder: ...)
```

### Navigation Patterns
```dart
// Modal navigation for workflows
Navigator.of(context).push(PageRouteBuilder(...))

// Standard navigation for hierarchy
Navigator.of(context).push(MaterialPageRoute(...))

// Tab-based navigation in HomeScreen
setState(() { _currentIndex = index; })
```

### Error Handling Pattern
```dart
// Consistent error handling across screens
ErrorHandler.handleError(error, context: context);

// User feedback with action options
ScaffoldMessenger.of(context).showSnackBar(SnackBar(...))
```

### Loading State Pattern
```dart
// Loading overlays for async operations
LoadingOverlay(isLoading: provider.isLoading, child: ...)

// Progress indicators for multi-step processes
GenerationProgressIndicator(currentStep: step, totalSteps: total)
```

## Best Practices Observed

1. **Feature Isolation**: Each feature area is self-contained
2. **Modular Settings**: Settings broken into logical, manageable sections
3. **Consistent Theming**: All screens use centralized color and constant definitions
4. **State Management**: Proper use of Provider pattern for state management
5. **Error Handling**: Centralized error handling with user-friendly feedback
6. **Navigation Consistency**: Consistent navigation patterns and transitions
7. **Responsive Design**: Screens adapt to different screen sizes and orientations
8. **Accessibility**: Proper semantic labeling and focus management
9. **Performance**: Efficient state management and widget rebuilding
10. **Code Organization**: Clean separation of concerns with focused, single-purpose screens