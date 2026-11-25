# Project Management Module - Cursor Rules
# These rules are automatically applied when editing files in this directory

# =============================================================================
# MODULE OVERVIEW
# =============================================================================
#
# This module manages Project Management functionality.
# Status: Scaffold - Phase 8 module (NOT FOR IMPLEMENTATION UNTIL PHASE 8)

# =============================================================================
# CRITICAL: Read contracts.ts FIRST
# =============================================================================
#
# Before modifying any file in this module, you MUST read:
#   frontend/src/modules/project_management/contracts.ts
#
# ⚠️ PHASE 8 MODULE - DO NOT IMPLEMENT YET
# This module is documented for Phase 8 implementation only.
# Framework must be complete (Phases 1-7) before implementation.

# =============================================================================
# TYPE IMPORTS
# =============================================================================
#
# ✅ CORRECT: Import types from contracts.ts
#   import { Entity, EntityCreate, ENDPOINTS } from './contracts';
#
# ❌ FORBIDDEN: Import directly from @/types/api in pages/components
# ❌ FORBIDDEN: Define ad-hoc types in page files

# =============================================================================
# ENDPOINT USAGE
# =============================================================================
#
# ✅ CORRECT: Use ENDPOINTS constant
#   apiClient.get<Entity[]>(ENDPOINTS.ENTITIES.LIST);
#
# ❌ FORBIDDEN: Hardcode URL strings

# =============================================================================
# VALIDATION CHECKPOINTS
# =============================================================================
#
# After editing any TypeScript file in this module:
# 1. Run: npx tsc --noEmit src/modules/project_management/{file}.tsx
# 2. Run: npx eslint src/modules/project_management/{file}.tsx --max-warnings 0
# 3. Fix ALL errors before proceeding
