# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Sprite Service is a microservice-based application for automating game sprite processing:
- **AI Background Removal**: BiRefNet (Full) for high-quality edge-preserving background removal
- **Smart Splitting**: OpenCV to detect and separate multiple sprites from a single image
- **Grid Splitting**: Auto-detect or manual grid-based splitting for sprite sheets
- **Multi-Size Generation**: Outputs in Large (256x256), Medium (128x128), Small (64x64)
- **Text-to-Sprite (Planned)**: Google Nano Banana Pro API for text-to-image generation with auto-processing

**Security Architecture**: Backend-for-Frontend (BFF) pattern - Python API is isolated in Docker network, accessible only through Nuxt 3 frontend proxy. Port 8000 is NOT exposed; all requests go through port 3000.

## Commands

### Container Management
```bash
# Start all services
podman-compose up -d --build    # or docker-compose

# View logs
podman-compose logs -f [api|worker|frontend]

# Scale workers
podman-compose up -d --scale worker=3
```

### Testing
```bash
python3 api_test_script.py    # Full pipeline test: upload -> process -> download
```

### Frontend Development
```bash
cd frontend && npm install && npm run dev
```

## Architecture

```
Browser :3000 → Nuxt 3 Frontend → [Docker Network] → FastAPI :8000 → Celery → Redis
                     ↓                                    ↓
              /server/api/*                        /app/data (shared volume)
```

| Service | Directory | Purpose |
|---------|-----------|---------|
| api | `/api/` | FastAPI - receives requests, dispatches Celery tasks |
| worker | `/worker/` | Celery - AI processing (BiRefNet + OpenCV) |
| frontend | `/frontend/` | Nuxt 3 - UI + server-side API proxy |

### Key Files
- `api/main.py` - Endpoints: `/process`, `/process/grid`, `/status/{id}`, `/download/{id}`, `/generate`
- `worker/sprite_processor.py` - `IntegratedSpriteProcessor` class (core AI logic)
- `frontend/server/api/` - Nuxt server routes proxying to internal API

### Data Flow
1. Upload via frontend → proxy to API → Celery task dispatched
2. Worker: `remove_background()` → `split_sprites()` → `resize_sprites()`
3. Result ZIP saved to shared volume → user downloads via frontend proxy

## Android App

Android 前端應用程式，位於 `android_app/` 目錄。

**Tech Stack**: Kotlin, Jetpack Compose, MVVM + Clean Architecture, Hilt, Retrofit, Room

**專案狀態**: ✅ 開發環境已設定完成，可直接開發

### 快速開始
```bash
cd android_app

# 建置 Debug APK
./gradlew assembleDebug

# 安裝到裝置
./gradlew installDebug

# APK 輸出: app/build/outputs/apk/debug/app-debug.apk
```

### 專案結構
```
android_app/
├── app/src/main/java/com/spriteservice/
│   ├── di/           # Hilt DI modules
│   ├── data/         # API, Repository, Room
│   ├── domain/       # Models, UseCases
│   └── ui/           # Compose screens
├── build.gradle.kts
└── SETUP.md          # 詳細設定指南
```

### 功能模組
- **認證**: Firebase Auth (Email/Password, Google Sign-In)
- **Sprite 處理**: 上傳圖片、狀態追蹤、下載結果
- **訂閱管理**: Google Play Billing

### 訂閱方案
| 方案 | 每日限制 | 功能 |
|------|----------|------|
| Free | 3 次 | 有浮水印 |
| Basic | 30 次 | 無浮水印 |
| Pro | 無限 | 批次處理、API 存取 |

### 待完成 (Backend Extensions)
- Auth Service (Firebase Admin SDK)
- Subscription Service (Google Play Billing verification)
- API Gateway (rate limiting by subscription tier)

See Serena memory `android_app_plan.md` for full details.

## Planned: Text-to-Sprite Feature

Integrate Google Nano Banana Pro API for complete text-to-sprite workflow:

**Models**:
| Model | ID | Use Case |
|-------|-----|----------|
| Nano Banana | `gemini-2.5-flash-image` | Fast generation, high volume |
| Nano Banana Pro | `gemini-3-pro-image-preview` | Professional quality, 4K, advanced reasoning |

**Workflow**: Text prompt → AI image generation → (optional) iterative editing → auto background removal → sprite splitting → multi-size output

**New Endpoints (Planned)**:
- `POST /generate` - Text-to-image generation
- `POST /generate/edit` - Image editing with instructions
- `POST /generate/process` - Confirm and enter sprite processing pipeline

**New Dependencies**: `google-genai>=1.0.0`

**Environment Variable**: `GOOGLE_AI_API_KEY`

See Serena memory `text_to_sprite_plan.md` for full implementation details.

## Code Conventions

**Python**: `snake_case` functions, `PascalCase` classes, `UPPER_SNAKE_CASE` constants, `_prefix` for private methods

**TypeScript**: Nuxt conventions for server routes (`process.post.ts`, `[id].get.ts`)

**Comments**: Bilingual (English + Traditional Chinese)

**Type hints**: Prefer adding for new code (currently minimal in codebase)

## Environment Notes

- **Podman/Docker RAM**: Requires 8GB+ (set via `podman machine set --memory 8192`)
- Worker uses full `BiRefNet` model for best quality background removal
- First startup downloads AI models (~2GB)
- Access web UI at http://localhost:3000 (NOT port 8000)
