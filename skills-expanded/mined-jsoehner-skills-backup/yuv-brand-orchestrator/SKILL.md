---

name: "yuv-brand-orchestrator"

description: "Orchestrates all YUV.AI branded content, including presentation decks, design system assets, pilot planning, and viral video creation."

version: 1

created: "2026-07-31"

updated: "2026-07-31"

---

## When to Use

Use for any request involving YUV.AI branded output, including presentations (decks), design system assets, brand strategy, or viral video creation.



## Procedure

1. Identify the requested YUV.AI output medium: Presentation Deck, Web/App UI, Pilot/Strategic Plan, or Viral Video.

2. For Presentation Decks: Use `yuv-decks` to scaffold the 4-act narrative arc (Boarding, Ascent, Cruise, Descent) and apply the `yuv-design-system` brand tokens.

3. For Web/App UI: Apply the `yuv-design-system` NEON mode (pink/cyan/white) and ensure all components are accessible.

4. For Pilot/Strategic Plans: Use `yuv-pilot` to orchestrate multi-medium content across channels and handle strategic brand positioning.

5. For Viral Videos: Use `yuv-viral-video` to transform selfie or screen-share footage into high-paced, captioned shorts with liquid-glass cards and GSAP motion.

6. Synthesize all components into a unified brand experience, ensuring consistent typography (Anton/Inter) and color usage across all artifacts.



## Pitfalls

- Do not use the 'Warm Editorial' palette for web-facing apps; use 'NEON' for web and 'DECKS' for slides.

- Ensure all video content follows the 'liquid-glass' and 'liquid-blob' aesthetic constraints.

- Always verify that the 'Fly High' tagline and phoenix mark are present in all presentation decks.



## Verification

1. The final output follows the YUV.AI brand guidelines (typography, color, motifs).

2. Presentation decks follow the 4-act narrative structure.

3. Viral videos include both 9:16 and 16:9 versions with correct captioning.


## Memory Sync

After completing key technical findings, architectural decisions, code refactorings, or risk assessments, you **MUST** trigger the local memory capture.

1. Save the final summary or artifact as a Markdown file in the project directory.
2. Invoke the capture script:
   ```bash
   python3 ~/memory_system/capture_knowledge.py <file_path>
   ```
3. This ensures that new learnings, policies, and technical snippets are automatically routed to the correct local storage (OKF or ChromaDB).
