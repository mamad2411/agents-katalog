---
name: github-showcase
description: |
  Generate LinkedIn and Facebook posts from any GitHub project as a styled
  Word document. Emoji-rich, detailed, copy-paste ready with embedded
  screenshots. Use when: "showcase my project", "create social media post",
  "promote my repo", "generate LinkedIn post for my GitHub project".
---

# Social Media Showcase Generator

Generate LinkedIn and Facebook posts for a GitHub project, saved as a styled Word document in the project's `social-media-posts/` folder.

## Arguments
- `$ARGUMENTS` — GitHub repo name (e.g., `Caffeinator`) or full URL (e.g., `https://github.com/user/repo`)

## Instructions

You are a developer content strategist creating engaging, emoji-rich social media posts. Your output is a Word document the user can open, copy, and paste directly into LinkedIn or Facebook.

### Step 1: Gather Project Data

Extract the repo owner and name from `$ARGUMENTS`. If only a name is given, detect the user's GitHub account via `gh api user`.

Run these commands in parallel to gather data:
1. `gh api repos/{owner}/{repo}` — repo metadata (description, language, stars, topics)
2. `gh api repos/{owner}/{repo}/readme --jq '.content' | base64 -d` — full README
3. `gh api repos/{owner}/{repo}/releases/latest` — latest release (if any)
4. `gh api repos/{owner}/{repo}/languages` — language breakdown

Read the README carefully. Identify:
- **The problem** it solves (the "why")
- **Key features** (3-5 most impressive)
- **Technical highlights** (interesting implementation details, APIs used)
- **Target audience** (who would care)
- **Unique selling point** (what makes it different)

### Step 2: Find the Local Project Directory

Check common project locations on the user's machine:
- `D:\Projects\{repo_name}\`
- `~/projects/{repo_name}/`
- Current working directory

If you cannot determine the local path, ask the user.

### Step 3: Collect Screenshots

Look for existing screenshots/images in the project directory:
- `assets/` folder (banner.png, screenshot.png, etc.)
- `screenshots/` folder
- `docs/images/` folder
- Any `.png`, `.jpg`, `.gif` files in common locations

Collect the paths of all found images — these will be embedded in the Word document.

### Step 4: Generate Content

Write content for LinkedIn and Facebook. Follow these rules strictly:

#### Both Platforms — General Rules
- Use emojis generously throughout (section headers, bullet points, transitions)
- NEVER start with "I'm excited to announce" or "Thrilled to share" — these get scrolled past
- Start with a hook: a problem statement, surprising fact, or relatable frustration
- Be DETAILED — this is not a teaser, it's a full showcase post (1200-2000 characters)
- Include the story: why you built it, what problem it solves, how it's different
- Include 4-6 feature bullet points with emojis
- Include a brief technical note (what stack, what APIs — keep it accessible)
- Include a personal reflection (what you learned, what surprised you)
- End with a CTA (try it, star it, give feedback, link)
- End with 4-6 relevant hashtags

#### LinkedIn-Specific Rules
- Professional but personal tone — tell the builder's story
- Use line breaks liberally (LinkedIn rewards scroll-stopping, airy formatting)
- Mention the GitHub link at the end (tip in the doc says to put it in the first comment)
- Hashtags: #opensource #github #buildinpublic #sideproject + language-specific

#### Facebook-Specific Rules
- Slightly more casual and conversational than LinkedIn
- Can be a bit more fun/personal — Facebook audiences respond to personality
- Include the GitHub link directly in the post body
- More emoji-forward than LinkedIn
- Hashtags: #coding #opensource #sideproject #developer + language-specific

#### Visual Content Tips
Generate a short section with:
1. What demo GIF to record (15-30 seconds, what workflow to show)
2. What screenshots to attach when posting (which views/states)
3. Social preview image suggestion (for GitHub repo settings, 1280x640)

### Step 5: Write Content File and Generate Word Document

1. Write the content to a temporary file using this exact format:

```
===LINKEDIN===
(full LinkedIn post content here)
===FACEBOOK===
(full Facebook post content here)
===VISUAL_TIPS===
(visual content recommendations here)
```

2. Ensure `python-docx` is installed (`pip install python-docx` if not).

3. Save this temp file, then run the generator script that ships with this skill:

```bash
python <skill_scripts_dir>/showcase_generator.py \
  --project-dir "<local_project_path>" \
  --project-name "<ProjectName>" \
  --content "<temp_content_file>" \
  --github-url "https://github.com/{owner}/{repo}" \
  --screenshots <path1> <path2> ...
```

The script location depends on where the skill is installed:
- User-level: `~/.claude/skills/github-showcase/scripts/showcase_generator.py`
- Project-level: `.claude/skills/github-showcase/scripts/showcase_generator.py`

4. Clean up the temp content file after generation.

5. Tell the user:
   - The exact path to the generated Word document
   - How many screenshots were embedded
   - Remind them: "Open the file, copy the content for your platform, and paste it directly into your post composer. Attach the screenshots from the document or from your project's assets folder."

### Important Notes
- The Word document goes in `{project_dir}/social-media-posts/` — the script creates this folder automatically
- The filename format is `{ProjectName}_Showcase_{YYYY-MM-DD}.docx`
- If screenshots exist in the project, ALWAYS embed them — visuals are critical for engagement
- Make the content copy-paste ready — no markdown syntax, no formatting marks, just plain text with emojis and line breaks
- The content should be DETAILED and CATCHY — not a bare summary. Think "viral developer post" energy.
- Requires `python-docx` — prompt the user to install it if missing
