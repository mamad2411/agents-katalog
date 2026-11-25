---
name: send-file
description: Send images, screenshots, charts, PDFs, or media files to the user on PiWeb and Discord (Piscord) using outbox markers ([[image: <path>]] / [[file: <path>]]).
version: 1.0.0
author: PiWeb
license: MIT
metadata:
  hermes:
    tags: [media, image, file, screenshot, attachment, piweb, discord, piscord]
---

# Send Images & Files to PiWeb / Discord (Piscord)

This skill guides the agent on how to correctly deliver local images, browser screenshots, generated charts, and files to the user in **PiWeb** and **Discord (Piscord)**.

---

## 🚨 Critical Rule: The Outbox Marker Convention

In PiWeb and Discord, the frontend/client **cannot access server local filesystem paths** (such as `/tmp/...` or `/home/...`) via standard Markdown links.

To send an image or file to the user, you **MUST** include the outbox marker in your response text:

```text
[[image: /absolute/path/to/image.png]]
[[file: /absolute/path/to/document.pdf]]
[[video: /absolute/path/to/recording.mp4]]
```

### What PiWeb & Discord Do With Outbox Markers:
1. **PiWeb**: Automatically copies the local file to the served web-media repository, stages it as an interactive media card with lightbox full-resolution zoom and download options.
2. **Discord (Piscord)**: Automatically uploads the file as a native Discord attachment in the channel.
3. The marker itself (`[[image: ...]]`) is automatically stripped from the visible text so your message looks clean.

---

## ❌ Common Mistakes to NEVER Make

| Incorrect Action | Why It Fails | Correct Action |
| :--- | :--- | :--- |
| **`read {"path": "/tmp/..."}` only** | `read` only loads image pixels into the AI's internal vision brain for AI analysis. **It DOES NOT send the image to the user.** | Always emit `[[image: /path/to/img.png]]` in your final reply prose. |
| **`![alt](/tmp/img.png)`** | Remote mobile/desktop browsers cannot reach server `/tmp` disk paths. It gets downgraded to broken text. | Use `[[image: /tmp/img.png]]`. |
| **Saying "It's displayed above" without emitting marker** | The user cannot see what only the AI saw via `read`. | Include the `[[image: ...]]` marker in your reply. |

---

## 📋 Common Scenarios & Workflows

### 1. Browser Screenshot (`browser screenshot` / `browser screenshot --full`)
When the user asks "給我看截圖", "截圖給我", "圖片傳給我", or when you capture a webpage:

```text
1. Execute tool: browser screenshot
2. Tool returns: Screenshot saved to /tmp/pi-nodriver-shot-abcdef12/screenshot.png
3. In your response to the user, output:
   這是當前網頁的截圖畫面：
   [[image: /tmp/pi-nodriver-shot-abcdef12/screenshot.png]]
```

### 2. Python / Matplotlib / Chart Generation
When you generate data visualization plots or diagrams:

```python
# Save chart to /tmp or local path
import matplotlib.pyplot as plt
plt.figure()
# ... plot data ...
plt.savefig('/tmp/stock_analysis.png', bbox_inches='tight')
```
In your response:
```text
分析圖表已生成：
[[image: /tmp/stock_analysis.png]]
```

### 3. File Downloads / PDFs / Audio
When a tool downloads a file or creates an export:
```text
下載完成的檔案如下：
[[file: /home/chihmin/.pi/agent/nodriver-downloads/manual.pdf]]
```

---

## 🎯 Quick Reference Cheat Sheet

* **Image (PNG, JPG, GIF, WebP)**: `[[image: /path/to/file.png]]`
* **General File (PDF, ZIP, CSV, TXT)**: `[[file: /path/to/file.pdf]]`
* **Video (MP4, WebM)**: `[[video: /path/to/file.mp4]]`
