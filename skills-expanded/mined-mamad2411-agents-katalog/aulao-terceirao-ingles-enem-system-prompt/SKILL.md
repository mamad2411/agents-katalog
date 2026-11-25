# System Prompt for ENEM English Prep WebApp

## Project Overview
You are building a static web application for ENEM (Brazilian National High School Exam) English language preparation. This will be a flashcard-style Q&A system hosted on GitHub Pages, designed for use in a final classroom review session.

## Project Context
- **Target Audience**: Brazilian high school students (3rd year) preparing for ENEM
- **Purpose**: Interactive classroom review tool for English language questions
- **Deployment**: Static site on GitHub Pages (no backend/database)
- **Language**: Bilingual (Portuguese-BR and English-US) with dynamic toggle
- **Question Format**: Multiple choice (5 options: A, B, C, D, E) - standard ENEM format

## Technical Requirements

### Technology Stack
- **HTML5**: Semantic markup, accessibility-focused
- **CSS3**: Modern, responsive design with mobile-first approach
- **Vanilla JavaScript**: No frameworks, ES6+ syntax
- **Data Storage**: All questions stored in embedded JSON (from CSV source)
- **Hosting**: GitHub Pages compatible (static files only)

### Key Constraints
1. **No Backend**: Everything must work client-side only
2. **No LocalStorage**: GitHub Pages restrictions - use in-memory JavaScript objects only
3. **No External Dependencies**: Self-contained, no CDN requirements beyond optional fonts
4. **Offline Capable**: Should work without internet after initial load

## Core Features to Implement

### 1. Question Bank System
- Load 54 questions from embedded JSON data (converted from CSV)
- Shuffle questions randomly on each session start
- Display questions one at a time in flashcard format
- Show question text, all 5 options (A-E), and category/difficulty tags

### 2. Bilingual Toggle System
- Global language switch (PT-BR ⇄ EN-US)
- Toggle button in header/navigation
- Instant translation without page reload
- Persist language preference during session (in-memory only)
- All UI elements must translate (buttons, labels, tips, etc.)

### 3. Flashcard Interface
- **Front**: Show question text + 5 multiple choice options
- **Interaction**: Click option to select answer
- **Feedback**: Immediately show if correct/incorrect with color coding
  - Correct answer highlighted in green
  - Wrong answer (if selected) highlighted in red
  - Show correct answer if user was wrong
- **Explanation**: Display explanation text after answer submission
- **Navigation**: "Next Question" button to advance
- **Progress**: Show question counter (e.g., "Question 5 of 54")

### 4. Tips & Strategies Section
Create a dedicated section accessible via navigation with exam-day tips:

**Mental Health & Anxiety Management:**
- Breathing exercises (4-4-4-4 square breathing technique)
- Positive self-talk phrases
- Visualization techniques
- Mindfulness reminders

**Focus & Concentration:**
- Pomodoro-style time management for the exam
- Strategic pause techniques
- How to handle "mental blanks"
- Priority question ordering (easy → medium → hard)

**Physical Preparation:**
- Sleep hygiene tips for night before
- Nutrition recommendations (light, energizing meals)
- Hydration reminders
- Stretching exercises during exam

**Exam Strategy:**
- Time management for 5 English questions
- Reading techniques (skimming, scanning)
- How to eliminate wrong answers
- When to skip and return to difficult questions
- Avoiding anxiety from other candidates' pace

### 5. Motivational Design Elements
- Encouraging color scheme (blues, greens, vibrant accents)
- Progress indicators showing advancement
- Positive feedback messages ("Great job!", "Keep going!", "You got this!")
- Clean, modern UI that reduces cognitive load
- Emoji/icons for emotional support (✅ ❌ 💪 🎯 📚)

### 6. User Experience Flow
```
Home Page
  ├─→ Language Toggle (PT-BR / EN-US) in header
  ├─→ "Start Review" Button (prominent CTA)
  ├─→ "Exam Tips" Button (secondary navigation)
  └─→ About/Instructions section

Question Interface (after Start)
  ├─→ Progress bar (X of 54)
  ├─→ Category tag + Difficulty badge
  ├─→ Question text
  ├─→ 5 radio button options (A-E)
  ├─→ "Submit Answer" button
  ├─→ Feedback section (after submit)
  ├─→ Explanation text
  └─→ "Next Question" button

Tips Section
  ├─→ Tabbed or accordion sections
  ├─→ Mental Health tips
  ├─→ Focus strategies
  ├─→ Physical prep
  └─→ Exam strategies

End Screen
  ├─→ Completion message
  ├─→ Performance summary (X/54 correct)
  ├─→ "Start Again" button
  └─→ Motivational message
```

## Design Guidelines

### Visual Design
- **Color Palette**: 
  - Primary: #2563eb (blue - confidence, trust)
  - Secondary: #10b981 (green - growth, positivity)
  - Accent: #f59e0b (amber - energy, warmth)
  - Correct: #22c55e (green)
  - Incorrect: #ef4444 (red)
  - Background: #f9fafb (light gray)
  - Text: #1f2937 (dark gray)

- **Typography**:
  - System fonts: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif
  - Clear hierarchy (h1: 2.5rem, h2: 2rem, body: 1rem)
  - Line height 1.6 for readability

- **Layout**:
  - Centered content, max-width 768px for questions
  - Generous whitespace
  - Card-based components with subtle shadows
  - Responsive grid for multi-column layouts on larger screens

### Accessibility
- Semantic HTML5 elements
- ARIA labels where appropriate
- Keyboard navigation support
- High contrast text (WCAG AA minimum)
- Focus indicators on interactive elements

## Data Structure

### Question Object Format (from CSV)
```javascript
{
  id: Number,
  category: String,
  difficulty: String, // "Easy" | "Medium" | "Hard"
  text_en: String,
  text_pt: String,
  question_en: String,
  question_pt: String,
  option_a_en: String,
  option_a_pt: String,
  option_b_en: String,
  option_b_pt: String,
  option_c_en: String,
  option_c_pt: String,
  option_d_en: String,
  option_d_pt: String,
  option_e_en: String,
  option_e_pt: String,
  correct_answer: String, // "A" | "B" | "C" | "D" | "E"
  explanation_en: String,
  explanation_pt: String
}
```

## Implementation Instructions

### File Structure
```
/
├── index.html          # Main page
├── css/
│   └── styles.css      # All styles
├── js/
│   ├── data.js         # Embedded questions JSON
│   ├── app.js          # Main application logic
│   └── i18n.js         # Translation/language switching
├── README.md           # Project documentation
└── assets/             # Optional: images, icons
```

### Code Quality Standards
- Use ES6+ features (const/let, arrow functions, template literals)
- Modular code with clear separation of concerns
- Comments for complex logic
- Consistent naming conventions (camelCase for JS, kebab-case for CSS)
- DRY principle - avoid repetition

### Testing Checklist
- [ ] All 54 questions load correctly
- [ ] Random shuffle works on page load
- [ ] Answer selection and validation works
- [ ] Correct/incorrect feedback displays properly
- [ ] Language toggle switches all text instantly
- [ ] Progress tracking updates correctly
- [ ] Tips section accessible and readable
- [ ] Responsive on mobile, tablet, desktop
- [ ] No console errors
- [ ] Works offline after initial load

## Development Workflow
1. Create basic HTML structure
2. Embed questions data from CSV into data.js
3. Build core question display and navigation
4. Implement answer validation logic
5. Add bilingual toggle system
6. Create tips/strategies section
7. Style with responsive CSS
8. Test on multiple devices
9. Optimize for GitHub Pages deployment

## GitHub Pages Deployment Notes
- Main branch / root folder or docs/ folder
- No build process needed (static files)
- Test locally with: `python3 -m http.server 8000`
- Access via: `https://[username].github.io/[repo-name]/`

## Motivational Tone
Throughout the app, maintain an encouraging, supportive tone:
- "You're doing great!"
- "Every question is a learning opportunity"
- "Trust your preparation"
- "You've got this! 💪"
- "Stay calm and focused"

## Additional Features (Optional Enhancements)
If time permits, consider:
- Dark mode toggle
- Confetti animation on quiz completion
- Sound effects for correct/incorrect answers (optional, user-controlled)
- Print-friendly version of tips
- Share functionality (share progress on social media)

## Remember
This is a teaching tool meant to empower students, reduce anxiety, and provide meaningful practice before the ENEM. Keep the UX simple, the design motivating, and the experience encouraging. The goal is confidence building, not added stress.

---

**Start building with confidence! Follow this system prompt to create an engaging, effective ENEM English prep tool. Good luck! 🎓**
