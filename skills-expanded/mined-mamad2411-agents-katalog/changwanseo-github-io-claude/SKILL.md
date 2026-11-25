# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Mobile wedding invitation (모바일 청첩장) for Changwan & Sumin, hosted on GitHub Pages at `Changwanseo.github.io`.

## Deployment

Push to `main` branch. GitHub Pages automatically deploys. No build step required.

## Architecture

- `index.html` — Single-page mobile wedding invitation (main site entry point)
- `wedding_invitation_1.png` — Hero illustration (couple drawing with "welcome to our new beginning")
- `wedding_invitation_2.png` — Map/directions image (from 낙성대역 to 호암교수회관)
- `README.md` — Repository description

## Key Details

- **Wedding**: 2026년 11월 21일 토요일 오후 3시
- **Venue**: 서울대학교 호암교수회관
- **Design**: Warm minimal style matching hand-drawn invitation art. Off-white (#faf8f4) background, serif fonts (Gowun Batang, Nanum Myeongjo), gold accent (#c9b99a).
- **Mobile-first**: Max-width 480px, scroll-based fade-in animations.
- **Fonts**: Loaded from Google Fonts (Gowun Batang, Nanum Myeongjo).
- No build tools, package managers, or dependencies.
