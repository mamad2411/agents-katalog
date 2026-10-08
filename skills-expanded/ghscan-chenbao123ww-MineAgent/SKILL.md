You are generating skill-annotated Minecraft VQA training data.

You receive:
  1. A video of a Minecraft agent (one video frame = one trajectory step, 0-indexed).
  2. A step-by-step trajectory log: step index, action, equipped item, position, events.
  3. A "skill_context" block with two sections retrieved via RAG:

     SUCCESS SKILLS — what to do:
       [skill_id] Name
         Description   : what the skill achieves
         Preconditions : what must be true BEFORE applying this skill
         Sub-tasks     : ordered execution steps
         Key actions   : concrete button/camera patterns

     AVOIDANCE SKILLS — what NOT to do:
       [skill_id] Name
         Description   : what mistake to avoid and why it hurts performance
         Preconditions : when this mistake is likely to occur
         Common mistakes    : suboptimal behaviours that have occurred
         Corrective actions : what to do instead

YOUR TASK:
  Watch the video and read the trajectory log together.
  Select the steps that most deserve skill-based chain-of-thought annotation.
  Aim for roughly 15–25% of total steps. Prioritise:
    • The moment skill preconditions first become satisfied
    • Phase transitions (searching → approaching → attacking → post-event)
    • Steps immediately before/after a significant event (kill, mine, craft, reward)
    • Steps where the agent appears to be making or about to make a known avoidable mistake
    • Periodic coverage (~every 30 steps) when nothing notable is happening

For each selected step generate:
  "obs"  : ONE sentence — perceptual facts visible in that video frame +
            the single most relevant game-state fact from the log.
  "think": 2–3 sentences structured EXACTLY as:
             (a) Precondition check: which success or avoidance preconditions are now met
             (b) [skill_id] + which sub-task is currently active
                 OR which avoidance mistake is at risk right now
             (c) Immediate next action and why
                 (cite key_action_patterns for success skills,
                  corrective_actions for avoidance skills)

  When citing an avoidance skill, sentence (b) must clearly name the mistake at risk
  and sentence (c) must state the corrective action
  (e.g. "[avoid_unequipped_armor] Armor is in inventory but not equipped —
   equip chestplate now before engaging combat.").

OUTPUT: a JSON array and NOTHING else (no markdown, no prose):
[
  {"step": <int>, "obs": "...", "think": "...", "skill_ids": ["skill_id"]},
  ...
]
Sorted by step ascending.
