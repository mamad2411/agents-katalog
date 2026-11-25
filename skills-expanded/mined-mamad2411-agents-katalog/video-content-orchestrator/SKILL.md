---

name: "video-content-orchestrator"

description: "Orchestrates video content production, including downloading, editing, and creating landing pages from video."

version: 1

created: "2026-07-31"

updated: "2026-07-31"

---

## When to Use

Use for any task involving video content production, including downloading, editing, and creating video-based landing pages.



## Procedure

1. Identify the video task: Download, Edit, or Landing Page Creation.

2. For Downloading: Use `video-downloader` to fetch content from supported platforms.

3. For Editing: Use `video-edit` to apply captions, liquid-glass effects, and GSAP motion.

4. For Landing Pages: Use `video-to-landing-page` to create a scroll-driven hero section from a video clip.

5. Synthesize the final video asset and ensure it meets the target platform's specifications.



## Pitfalls

- Ensure video files are in supported formats (mp4, mov, mkv).

- Check that the system has enough storage for high-resolution video processing.

- Verify that all captions are correctly synchronized with the audio stem.



## Verification

1. The video file is correctly rendered and playable.

2. Captions are synchronized and visually consistent with the brand style.

3. The landing page correctly scrubs the video frames on scroll.


## Memory Sync

After completing key technical findings, architectural decisions, code refactorings, or risk assessments, you **MUST** trigger the local memory capture.

1. Save the final summary or artifact as a Markdown file in the project directory.
2. Invoke the capture script:
   ```bash
   python3 ~/memory_system/capture_knowledge.py <file_path>
   ```
3. This ensures that new learnings, policies, and technical snippets are automatically routed to the correct local storage (OKF or ChromaDB).
