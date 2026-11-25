---
name: portfolio-architecture
description: "Understand current Portfolio boundaries before changing cross-layer architecture."
---

# portfolio-architecture

Read [verified architecture](../../brain/architecture.md) for current behavior and separately marked target design. Keep that file as the fact authority instead of duplicating a stack map here.

Next.js owns UI/rendering and BFF transport; FastAPI owns backend business/AI logic; Supabase persistence uses migrations and explicit access policies when introduced. Choose contracts before independent implementation. Record significant accepted changes in decisions and update verified facts after implementation.
