# 🛠️ Project Instructions for Cursor

This document gives **step-by-step instructions** for Cursor AI to create the full "Video → Flashcards & Questions" study platform using **Next.js 14**, **Supabase**, and **OpenAI**.

Use these instructions as a **starter `.cursor/instructions.md` file**.

---

# 📦 Project Overview

Build a web application where users can:

1. Upload a video or paste a YouTube link.
2. Extract audio → transcribe with Whisper.
3. Generate transcript segments.
4. Generate flashcards & questions using OpenAI.
5. Study with flashcards, quizzes, and exam modes.
6. Store all data in Supabase.

---

# 🧱 Tech Stack

* **Next.js 16 (App Router)**
* **TypeScript**
* **TailwindCSS**
* **Supabase** (Auth + Database + Storage)
* **OpenAI API** (Whisper + GPT)
* **shadcn/ui**
* **ffmpeg.wasm** for browser-side audio extraction (optional).

---

# 📁 Folder Structure

```
app/
  (auth)/
    login/
    signup/
    callback/
  dashboard/
    videos/
      [id]/
        page.tsx        # Main study interface
        flashcards/
        questions/
    library/
  api/
    upload/
    process/
    generate/
components/
library/
supabase/
utils/
```

---

# 🔒 Supabase Setup Steps

1. Create a new Supabase project.
2. Enable **Storage** bucket `videos` and `thumbnails`.
3. Create all tables from the SQL schema provided.
4. Enable RLS and apply policies.
5. Create `.env.local`:

```
NEXT_PUBLIC_SUPABASE_URL="your_url"
NEXT_PUBLIC_SUPABASE_ANON_KEY="your_key"
SUPABASE_SERVICE_ROLE_KEY="service_key"
OPENAI_API_KEY="your_openai_key"
```

---

# 🧩 Core Features to Implement

## 1. **Video Upload Flow**

* Use Supabase Storage for video files.
* For YouTube links, send URL to backend.
* Trigger `/api/process/transcribe` route.

### API Route: `/api/upload`

* Accept video file or link.
* Create video record.
* Upload file to storage.
* Return job ID.

---

## 2. **Transcription Pipeline (Server)**

### API Route: `/api/process/transcribe`

* Download video or extract audio.
* Use OpenAI Whisper API:

```ts
client.audio.transcriptions.create({
  file: videoBuffer,
  model: 'whisper-1'
})
```

* Store transcript in `video_segments` (auto-chunked).
* Update `videos.status = 'ready'`.

---

## 3. **Generate Flashcards**

### API Route: `/api/generate/flashcards`

* Input: transcript segments
* Use GPT-4o-mini or GPT-4.2
* Output 10–30 flashcards
* Store in `flashcards`.

---

## 4. **Generate Questions**

### Types:

* MCQ
* True/False
* Short Answer
* Fill in the blank

### API Route: `/api/generate/questions`

* Similar structure to flashcards
* Store in `questions`

---

## 5. **Study Mode UI**

### Flashcards UI

* Flip animation
* Spaced repetition buttons (Again, Hard, Good, Easy)
* Update flashcard SRS fields in Supabase

### Quiz Mode

* Timed or untimed
* On submit → show explanation

---

# 🎨 UI Requirements (Cursor Should Generate 100%)

* Use **shadcn/ui**
* Use **TailwindCSS**
* Use **Card**, **Button**, **Skeleton**, **Dialog**, **Tabs**, **Progress**
* Clean, minimal, modern layout

---

# 🤖 API Route Templates

## Example: Upload Route

```ts
export async function POST(req: Request) {
  const form = await req.formData();
  const file = form.get('file');

  // upload to Supabase storage
  // insert video into DB
  // return video ID
}
```

## Example: Generate Flashcards

```ts
const prompt = `Create flashcards from this transcript:
${transcript}
Format: JSON array of {front, back}`;

const response = await client.responses.create({...});
```

---

# 🔧 Util Functions Cursor Should Create

* `extractVideoAudio()`
* `segmentTranscript()`
* `generateFlashcards()`
* `generateQuestions()`
* `updateFlashcardSRS()`
* `getVideoWithSegments()`

---

# 📚 Pages Cursor Should Build

### `/dashboard/library`

* Shows all uploaded videos
* Grid of cards

### `/dashboard/videos/[id]`

Contains 3 columns:

1. Video Player
2. Transcript
3. AI Tools (Tabs)

Tabs:

* Flashcards
* Questions
* Notes
* Summary

### `/dashboard/videos/[id]/flashcards`

* Full-screen study mode

### `/dashboard/videos/[id]/quiz`

* 10–40 questions
* Timer
* Score report

---

# 🚀 Stretch Features

* Embeddings + semantic search
* Teacher mode with public quizzes
* Export flashcards to Anki

---

# ✔️ Cursor Final Goal

Cursor should generate a working **full-stack Next.js + Supabase AI study app** with:

* Video upload
* Transcription
* Flashcard generation
* Question generation
* Study mode
* Quiz mode
* Clean UI

---

# End of Instructions


