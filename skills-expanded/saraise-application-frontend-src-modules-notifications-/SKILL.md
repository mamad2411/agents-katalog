# Notifications Module - Cursor Rules
# These rules are automatically applied when editing files in this directory

# =============================================================================
# MODULE OVERVIEW
# =============================================================================
#
# This module manages in-app notifications and user preferences.
# Core module - part of foundation.

# =============================================================================
# CRITICAL: Read contracts.ts FIRST
# =============================================================================
#
# Before modifying any file in this module, you MUST read:
#   frontend/src/modules/notifications/contracts.ts
#
# Types: Notification, NotificationPreference
# Endpoints: NOTIFICATIONS (LIST, DETAIL, MARK_READ, MARK_ALL_READ, UNREAD_COUNT)
#            PREFERENCES (GET, UPDATE)

# =============================================================================
# TYPE IMPORTS
# =============================================================================
#
# ✅ CORRECT: Import types from contracts.ts
#   import { Notification, NotificationPreference, ENDPOINTS } from './contracts';
#
# ❌ FORBIDDEN: Import directly from @/types/api in pages/components
# ❌ FORBIDDEN: Define ad-hoc types in page files

# =============================================================================
# ENDPOINT USAGE
# =============================================================================
#
# ✅ CORRECT: Use ENDPOINTS constant
#   apiClient.get<Notification[]>(ENDPOINTS.NOTIFICATIONS.LIST);
#   apiClient.patch(ENDPOINTS.NOTIFICATIONS.MARK_READ(id), {});
#
# ❌ FORBIDDEN: Hardcode URL strings

# =============================================================================
# VALIDATION CHECKPOINTS
# =============================================================================
#
# After editing any TypeScript file in this module:
# 1. Run: npx tsc --noEmit src/modules/notifications/{file}.tsx
# 2. Run: npx eslint src/modules/notifications/{file}.tsx --max-warnings 0
# 3. Fix ALL errors before proceeding
