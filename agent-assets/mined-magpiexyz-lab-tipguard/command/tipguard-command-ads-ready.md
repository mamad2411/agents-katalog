---
description: "Verify PostHog tracking is correctly configured before paid ads launch. Run after /deploy, before manually creating a Google Ads campaign."
type: analysis-only
reads: []
stack_categories: []
requires_approval: false
references:
  - .claude/stacks/analytics/posthog.md
branch_prefix: ""
modifies_specs: false
---
Verify PH/DB/Vercel/Stripe setup is ads-ready. $ARGUMENTS

Phase selection and optional flags:
- `phase-1`: run base readiness checks for the Phase 1 demand screen
- `phase-2`: run base checks plus additional static fake-door configuration checks for the Phase 2 value screen
- no phase flag: ask which phase to check before initializing the lifecycle
- `--static-only`: skip Layer B (live smoke test) -- dev-iteration mode only
- `--url <URL>`: override Vercel auto-detect for Layer B target

## Lifecycle

1. Parse `$ARGUMENTS` for `phase-1`, `phase-2`, `--static-only`, and `--url <URL>` flags using a small bash block in this dispatcher:
   ```bash
   STATIC_ONLY=false
   PHASE=""
   DEPLOY_URL=""
   for arg in $ARGUMENTS; do
     case "$arg" in
       phase-1) PHASE="phase-1" ;;
       phase-2) PHASE="phase-2" ;;
       --static-only) STATIC_ONLY=true ;;
       --url) DEPLOY_URL_NEXT=1 ;;
       *) if [ "${DEPLOY_URL_NEXT:-}" = "1" ]; then DEPLOY_URL="$arg"; DEPLOY_URL_NEXT=0; fi ;;
     esac
   done
   ```
2. Resolve the phase. If step 1 left `PHASE` empty, ask the user via AskUserQuestion (never ExitPlanMode): "Which phase are you checking ads readiness for?" with two options: "Phase 1 -- demand screen (signup funnel; checks 1-13)" and "Phase 2 -- value screen (fake-door pay_intent; checks 1-13 + P2-a..P2-e)". Set `PHASE=phase-1` or `PHASE=phase-2` from the user's answer before continuing. AskUserQuestion is an established approval source in `.claude/patterns/prose-gates.json`. If the question cannot be asked in a non-interactive/headless run, STOP with: "Usage: pass `phase-1` or `phase-2` explicitly."
3. Run `bash .claude/scripts/lifecycle-init.sh ads-ready`.
4. Inject flags into the context via the canonical helper. State 1 always runs and short-circuits internally based on `static_only`; `skip_states` is intentionally not used here.
   ```bash
   if [ -z "$PHASE" ]; then
     echo "Usage: pass phase-1 or phase-2 explicitly" >&2
     exit 1
   fi
   PHASE_2=false
   if [ "$PHASE" = "phase-2" ]; then PHASE_2=true; fi
   PAYLOAD=$(python3 -c "
   import json
   print(json.dumps({
       'static_only': '$STATIC_ONLY' == 'true',
       'phase': '$PHASE',
       'phase_2': '$PHASE_2' == 'true',
       'deploy_url': '$DEPLOY_URL' or None,
   }))
   ")
   bash .claude/scripts/init-context.sh ads-ready "$PAYLOAD"
   ```
5. State execution loop:
   a. Run: `NEXT=$(bash .claude/scripts/lifecycle-next.sh ads-ready)`
   b. If NEXT is "FINALIZE" -> skill complete
   c. If NEXT does not start with "/" -> STOP with error (print NEXT for diagnosis)
   d. Read the state file at $NEXT and execute its ACTIONS section
   e. After ACTIONS complete, run the state's STATE TRACKING command
      (the `bash .claude/scripts/advance-state.sh` call in the state file)
   f. Return to step 5a

## Do NOT
- Modify any code files -- this skill is analysis-only
- Create branches or PRs
- Auto-fix detected issues -- operators or `/change` own the fix
