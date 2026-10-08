# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Sky Track is a React TypeScript flight tracking application built with Vite. It displays flight information in a list/detail view pattern with animated UI components and uses React Router for navigation.

## Development Commands

- `bun run dev` - Start development server with hot reload
- `bun run build` - Build for production (runs TypeScript check then Vite build)
- `bun run lint` - Run ESLint for code quality checks
- `bun run preview` - Preview production build locally

## Architecture & Tech Stack

**Core Technologies:**
- React 19 with TypeScript
- Vite for build tooling
- React Router v7 for navigation
- Tailwind CSS v4 with @tailwindcss/vite plugin

**Key Libraries:**
- `motion` (v12) - Animation library for UI interactions
- `lucide-react` - Icon components
- `class-variance-authority` + `clsx` + `tailwind-merge` - Component styling utilities
- `tw-animate-css` - Additional Tailwind animations

## Project Structure

**Components Architecture:**
- `src/components/Layout.tsx` - Root layout with React Router Outlet
- `src/components/flight-list/` - Flight list components and data
- `src/components/flight-details/` - Flight detail view components
- `src/components/animate-ui/` - Custom animated UI components and icons
- `src/screens/home/` - Main screen combining flight list and details

**Data Layer:**
- `src/types/flight.types.ts` - TypeScript interfaces for flight data
- `src/components/flight-list/fligths.data.ts` - Static flight data (FLIGHTS array)
- Flight data includes airline info, routes, aircraft details, and gradient colors

**Utilities:**
- `src/lib/utils.ts` - Shared utility functions
- `src/utils/cn.ts` - Tailwind class merging utility
- Path alias `@/` configured to resolve to `src/`

## Key Patterns

**Flight Data Structure:**
Each flight has airline, aircraft, route (speed/altitude), locations (from/to with timezone), and visual properties (logo, gradient colors).

**Styling Approach:**
Uses Tailwind CSS with custom gradients per flight, utility-first approach with component variance API for consistent styling patterns.

**Component Organization:**
Components are grouped by feature (flight-list, flight-details) with shared animate-ui components for reusable animated elements.

## Assets

Static assets in `public/` include airline logos (`/logos/`), aircraft images (`/planes/`), and country flags (`/flags/`) referenced in flight data.