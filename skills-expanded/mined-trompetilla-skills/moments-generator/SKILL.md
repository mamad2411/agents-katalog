---
name: moments-generator
description: Generate a fake WeChat Moments (朋友圈) screenshot image. Use when user wants to simulate a social media post with avatar, text, images, likes, and comments.
---

# Moments Generator Skill

This skill generates a realistic-looking WeChat Moments screenshot.

## Usage

1. **Prepare Resources**:
   - Ensure the user's avatar and any content images are saved locally (e.g., using `web_fetch` or `read`).

2. **Create Configuration**:
   Create a temporary JSON file (e.g., `temp_moments_config.json`) with the following structure:
   ```json
   {
     "avatar": "/path/to/avatar.png",
     "name": "User Name",
     "content": "This is the text of the moment.",
     "images": [
       "/path/to/image1.jpg",
       "/path/to/image2.jpg"
     ],
     "likes": ["Friend A", "Friend B"],
     "comments": [
       { "name": "Friend C", "text": "Nice photo!" },
       { "name": "Me", "text": "Thanks!" }
     ],
     "theme": "dark"
   }
   ```
   *Note: Supports 1-9 images. `images` can be empty. `theme` defaults to "light".*

3. **Generate Image**:
   Run the generation script:
   ```bash
   node /home/crishaocredits/.openclaw/workspace/skills/moments-generator/scripts/generate.js temp_moments_config.json output_moments.png
   ```

4. **Deliver**:
   Send the resulting `output_moments.png` to the user.

## Dependencies
- Node.js
- pureimage (Bundled)
- Fonts (Bundled/System)
