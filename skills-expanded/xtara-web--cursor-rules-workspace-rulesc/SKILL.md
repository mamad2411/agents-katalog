---
alwaysApply: true
---

READ THESE RULES BEFORE STARTING ANY WORK.

# Project Xtara - Workspace Rules Index

## 🏗️ PROJECT STRUCTURE

This workspace contains four main projects:

```
project-xtara/
├── xtara/                    # Next.js website (React/TypeScript)
├── career/                   # Flutter mobile app
├── career-ai/                # Python AI/ML scripts and services
└── xtara-firebase/           # Consolidated Firebase operations
└── assets/                   # Assets for the projects
└── data_models/              # Data structure reference for all projects
```

## Project Specific Rules

### Flutter - refer to
career/.cursor/flutter-build-rules.mdc
career/.cursor/flutter-ds-rules.mdc
career/.cursor/flutter-rules.mdc


## 🎯 RULE HIERARCHY

### **How Rules Work Together:**
1. **`ds-rules.mdc`** - Foundation Layer (Semantic design tokens) - **ALWAYS READ FIRST**
2. **`architecture-principles.mdc`** - Architecture Layer (DRY, reusability, modularity) - **ALWAYS READ SECOND**
3. **Platform Rules** - Implementation Layer (How to use tokens in each platform) - **READ BASED ON PROJECT**
4. **Project Rules** - Development Layer (Build, deploy, architecture) - **READ BASED ON PROJECT**

### **Conditional Rule Application:**

#### **📱 For Flutter App (career/)**
```
ds-rules.mdc → architecture-principles.mdc → flutter-ds-rules.mdc → flutter-rules.mdc
```
**❌ DON'T READ:** firebase-rules.mdc (unless working on Firebase integration)

#### **🌐 For Website (xtara/)**
```
ds-rules.mdc → architecture-principles.mdc → react-ds-rules.mdc (when created) → react-rules.mdc (when created)
```
**❌ DON'T READ:** flutter-rules.mdc, firebase-rules.mdc

#### **🤖 For AI Pipeline (career-ai/)**
```
ds-rules.mdc → architecture-principles.mdc → python-rules.mdc (when created)
```
**❌ DON'T READ:** flutter-rules.mdc, firebase-rules.mdc

#### **🔥 For Firebase Operations (xtara-firebase/)**
```
ds-rules.mdc → architecture-principles.mdc → firebase-rules.mdc
```
**❌ DON'T READ:** flutter-rules.mdc, react-rules.mdc

### **Rule Reading Order by Project:**

**📱 Flutter Development:**
1. `ds-rules.mdc` - "Use color-primary token"
2. `architecture-principles.mdc` - "Follow DRY principle, use reusable components"
3. `flutter-ds-rules.mdc` - "color-primary = kPrimaryColor in Flutter"
4. `flutter-rules.mdc` - "How to build and deploy Flutter app"

**🌐 React/Next.js Development:**
1. `ds-rules.mdc` - "Use color-primary token"
2. `architecture-principles.mdc` - "Follow DRY principle, use reusable components"
3. `react-ds-rules.mdc` - "color-primary = CSS variable in React" (when created)
4. `react-rules.mdc` - "How to build and deploy React app" (when created)

**🤖 Python AI Development:**
1. `ds-rules.mdc` - "Use semantic design tokens"
2. `architecture-principles.mdc` - "Follow DRY principle, use modular functions"
3. `python-rules.mdc` - "How to implement design tokens in Python" (when created)

**🔥 Firebase Development:**
1. `ds-rules.mdc` - "Use semantic design tokens"
2. `architecture-principles.mdc` - "Follow DRY principle, use modular functions"
3. `firebase-rules.mdc` - "How to deploy and configure Firebase"

## 🎯 PROJECT-SPECIFIC RULES

### **Node Setup**
**ALWAYS** run `nvm use 24` before any commands

### 📱 CAREER (Flutter App)
**Location**: `career/`
**Tech Stack**: Flutter, Dart, Firebase, GetX

**📋 Required Rules (Read in Order):**
1. `ds-rules.mdc` - Design system foundation (semantic tokens)
2. `architecture-principles.mdc` - Software architecture principles
3. `flutter-ds-rules.mdc` - Flutter implementation (how to use tokens)
4. `flutter-rules.mdc` - Development patterns, build commands, and architecture

**❌ Don't Read:** firebase-rules.mdc (unless working on Firebase integration)

**🔧 Quick Start:**
```bash
cd career
flutter pub get
flutter run -t lib/main_dev.dart
```

### 🌐 XTARA (Website)
**Location**: `xtara/`
**Tech Stack**: Next.js, React, TypeScript, Tailwind CSS

**📋 Required Rules (Read in Order):**
1. `ds-rules.mdc` - Design system foundation (semantic tokens)
2. `architecture-principles.mdc` - Software architecture principles
3. `react-ds-rules.mdc` - React implementation (when created)
4. `react-rules.mdc` - React development patterns (when created)

**❌ Don't Read:** flutter-rules.mdc, firebase-rules.mdc

**🔧 Quick Start:**
```bash
cd xtara
npm install
npm run dev
```

### 🤖 CAREER-AI (Python AI/ML)
**Location**: `career-ai/`
**Tech Stack**: Python, Google Cloud, Vertex AI, Firebase

**📋 Required Rules (Read in Order):**
1. `ds-rules.mdc` - Design system foundation (semantic tokens)
2. `architecture-principles.mdc` - Software architecture principles
3. `python-rules.mdc` - Python development patterns (when created)

**❌ Don't Read:** flutter-rules.mdc, firebase-rules.mdc

**🔧 Quick Start:**
```bash
cd career-ai
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
python run_pipeline.py
```

### 🔥 XTARA-FIREBASE (Firebase Operations)
**Location**: `xtara-firebase/`
**Tech Stack**: Firebase, Cloud Functions, Firestore

**📋 Required Rules (Read in Order):**
1. `ds-rules.mdc` - Design system foundation (semantic tokens)
2. `architecture-principles.mdc` - Software architecture principles
3. `firebase-rules.mdc` - Firebase commands, deployment, and configuration

**❌ Don't Read:** flutter-rules.mdc, react-rules.mdc

**🔧 Quick Start:**
```bash
cd xtara-firebase
npm run install:all
npm run deploy:functions
```

## 🎨 DESIGN SYSTEM

### **Unified Color Palette**
```
Ocean Navy:    #003763  (Primary)
Sky Blue:      #61B3E4  (Accent)
Coral Orange:  #EF7521  (Motivational)
Sun Gold:      #F6B333  (Secondary)
Ivory White:   #FFFFFF  (Contrast)
Seafoam Teal:  #3CA6A6  (Tertiary)
Cream Sand:    #F2E3D5  (Card background)
```

### **Typography**
- **Headings**: Merriweather (serif)
- **Body**: Inter (sans-serif)

## 🚀 DEPLOYMENT

### **Flutter App**
```bash
cd career
flutter build apk --release  # Android
flutter build ios --release  # iOS
# Upload to app stores
```

### **Website**
```bash
cd xtara
npm run build
# Deploy to hosting platform
```

### **Firebase**
```bash
cd xtara-firebase
npm run deploy:functions
npm run deploy:rules
npm run deploy:hosting
```

### **AI Pipeline**
```bash
cd career-ai
gcloud functions deploy <function_name> --runtime python39 --trigger-http
```

## 🔧 DEVELOPMENT WORKFLOW

### **Before Starting Any Task**
1. **Identify the correct project** (career, xtara, career-ai, xtara-firebase)
2. **Read design system foundation** (`ds-rules.mdc`) - **ALWAYS FIRST**
3. **Read architecture principles** (`architecture-principles.mdc`) - **ALWAYS SECOND**
4. **Read project-specific rules** (see above for each project) - **BASED ON PROJECT**
5. **Follow established patterns** within each project

### **Rule Reading Checklist by Project:**

**📱 For Flutter Development (career/):**
- ✅ Read `ds-rules.mdc`
- ✅ Read `architecture-principles.mdc`
- ✅ Read `flutter-ds-rules.mdc`
- ✅ Read `flutter-rules.mdc`
- ❌ Skip `firebase-rules.mdc` (unless Firebase integration)

**🌐 For React Development (xtara/):**
- ✅ Read `ds-rules.mdc`
- ✅ Read `architecture-principles.mdc`
- ✅ Read `react-ds-rules.mdc` (when available)
- ✅ Read `react-rules.mdc` (when available)
- ❌ Skip `flutter-rules.mdc`, `firebase-rules.mdc`

**🤖 For Python Development (career-ai/):**
- ✅ Read `ds-rules.mdc`
- ✅ Read `architecture-principles.mdc`
- ✅ Read `python-rules.mdc` (when available)
- ❌ Skip `flutter-rules.mdc`, `firebase-rules.mdc`

**🔥 For Firebase Development (xtara-firebase/):**
- ✅ Read `ds-rules.mdc`
- ✅ Read `architecture-principles.mdc`
- ✅ Read `firebase-rules.mdc`
- ❌ Skip `flutter-rules.mdc`, `react-rules.mdc`

### **Cross-Project Dependencies**
- **Color consistency**: Update all projects when changing the color palette
- **Typography**: Maintain font consistency across web and mobile
- **Content**: Sync career data between AI pipeline and mobile app
- **Firebase**: Ensure consistent data structure across all projects

## 📁 FILE ORGANIZATION

### **Never Create Files In Wrong Locations**
- **Flutter code** → `career/lib/`
- **Website code** → `xtara/src/`
- **Python scripts** → `career-ai/`
- **Firebase config** → `xtara-firebase/`

### **Asset Management**
- **Images**: Store in respective project's assets folder
- **Icons**: Use consistent icon libraries per project
- **Fonts**: Maintain typography consistency across projects

## 🚨 CRITICAL REMINDERS

1. **Always identify the correct project** before making changes
2. **Read design system foundation** (`ds-rules.mdc`) **FIRST** - applies to all projects
3. **Read architecture principles** (`architecture-principles.mdc`) **SECOND** - applies to all projects
4. **Read project-specific rules** based on which project you're working on
5. **Skip irrelevant rules** - don't read Flutter rules for React development
6. **Maintain consistency** across all projects
7. **Test thoroughly** before deploying
8. **Document changes** for future reference
9. **Use the unified color palette** across all projects
10. **Follow security best practices** for each platform 