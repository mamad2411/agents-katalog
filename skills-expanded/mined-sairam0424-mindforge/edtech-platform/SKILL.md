---
name: edtech-platform
version: 1.0.0
min_mindforge_version: 10.2.0
status: stable
triggers: edtech platform, learning management system, adaptive learning algorithm, assessment engine, educational content delivery, student progress tracking, course management, LMS architecture, online learning platform, competency framework, learning path design, educational analytics
---

# Skill — EdTech Platform

## When this skill activates
This skill activates when building learning management systems (LMS), adaptive learning algorithms, assessment/quiz engines, course content delivery platforms, student progress tracking, competency frameworks, learning path recommendations, or educational analytics dashboards.

## Mandatory actions when this skill is active

### Before writing any code
1. Design learning object model: courses → modules → lessons → activities (video, reading, quiz, assignment), with prerequisite dependencies (DAG validation), completion criteria per activity type (watch 80% of video, pass quiz with 70%, submit assignment), and progress rollup to course level
2. Model assessment engine: question bank with metadata (difficulty, topic tags, bloom's taxonomy level), quiz generation (random selection from pool, fixed seed for consistency), scoring rubrics (multiple choice auto-grade, short answer manual review, peer assessment), and partial credit support
3. Map adaptive learning logic: knowledge graph (concepts and prerequisite relationships), learner profiling (mastery level per concept, learning velocity, preferred modalities), content recommendation (serve easier/harder content based on performance), and remediation paths (loop back to foundational concepts on failure)

### During implementation
- Implement content delivery with engagement tracking: video player with playback position persistence (resume from last position), event logging (play, pause, seek, speed change, completion), transcripts with search, captions in multiple languages, quality selection (adaptive bitrate for mobile), and download for offline access
- Build assessment engine with anti-cheating measures: randomize question order, shuffle answer choices, time limits per question, lockdown browser detection (fullscreen enforcement, tab switch detection), plagiarism detection (Turnitin API, cosine similarity for text), and proctoring integration (webcam monitoring, eye tracking)
- Design progress tracking with granular analytics: store activity completion events (user_id, activity_id, timestamp, score, time_spent), aggregate to module/course level, calculate metrics (completion rate, average score, time to completion), identify at-risk students (falling behind pace, multiple failed attempts), trigger interventions (reminder emails, instructor notifications)
- Implement competency-based progression: define competencies with proficiency levels (novice, intermediate, advanced, expert), map learning activities to competencies, assess mastery through multiple evidence points (quiz scores, assignment grades, peer reviews), unlock next level only when threshold met (80% proficiency)
- Build discussion forums with moderation: threaded conversations, upvote/downvote, instructor endorsements, tag filtering (question, announcement, discussion), spam detection (rate limiting, keyword filters, ML-based flagging), and content moderation queue

### After implementation
- Validate learning analytics accuracy: verify completion tracking (activity marked complete only when criteria met), score calculation (weighted averages for modules/courses), progress rollup (course progress reflects all module progress), and leaderboard consistency (rank students by total points, handle ties)
- Test adaptive learning effectiveness: measure learning velocity (time to achieve 80% mastery per concept), retention rate (re-test after 1 week), engagement metrics (video watch time, quiz attempts, forum participation), compare adaptive vs linear paths (A/B test for cohort outcomes)
- Execute accessibility compliance audit: WCAG 2.1 AA conformance (video captions, keyboard navigation, screen reader support), alternative formats (transcripts, audio descriptions), color contrast checks (4.5:1 for text), and assistive technology testing (NVDA, JAWS)

## Self-check before task completion
- [ ] Learning object hierarchy implemented: courses → modules → lessons → activities with prerequisite enforcement (DAG validation)
- [ ] Content delivery tracks engagement: video playback position, event logs, transcript search, adaptive bitrate, offline download
- [ ] Assessment engine supports multiple question types: multiple choice, short answer, essay, peer assessment, with auto-grading and manual review workflows
- [ ] Anti-cheating measures active: randomized questions, time limits, lockdown browser, plagiarism detection, proctoring integration
- [ ] Progress tracking granular: activity-level completion events, aggregate metrics at module/course level, at-risk student identification
- [ ] Adaptive learning functional: knowledge graph, learner profiling, content recommendation based on mastery, remediation paths
- [ ] Competency-based progression: proficiency levels, evidence-based mastery assessment, unlock gates for next level
- [ ] Accessibility compliant: WCAG 2.1 AA (captions, keyboard nav, screen reader), alternative formats, color contrast
