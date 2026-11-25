---
name: build-form-validation
description: Implements type-safe forms with React Hook Form + Zod (or server-action validation) — schemas, field arrays, multi-step flows, and accessible error handling; used when building or fixing forms.
when_to_use: When the user builds or fixes a form, mentions React Hook Form, Zod, form validation, multi-step/wizard forms, field arrays, or server-action input validation.
---

## When to Use

Use this skill when building or fixing a form in a React/Next.js codebase — anything touching `react-hook-form`, `zod`, `zodResolver`, field arrays, multi-step/wizard flows, or server-action input validation. This covers the **client form layer**: schema-driven validation, RHF wiring, accessible errors, and the client↔server-action contract.

Not this skill: pure REST/RPC contract or response-shape review (that is API design review). This skill stops at "the action received validated input and returned a typed result."

First, detect the stack before writing code:
- `grep -r "next" package.json` and check for an `app/` dir → App Router (server actions + `useActionState` available on React 19).
- Check installed versions: `react-hook-form` v7+, `zod` v3 vs v4 (error API differs), `@hookform/resolvers`.
- Look for an existing form in the repo and **match its pattern** (UI lib, resolver setup, error component) instead of inventing a new one.

## Steps

1. **One Zod schema = source of truth.** Write the schema once, derive the TS type with `z.infer`, and import the *same* schema on client and server. Never hand-write a parallel `interface`.
   ```ts
   // schema.ts — shared
   export const signupSchema = z.object({
     email: z.string().email(),
     password: z.string().min(8),
     confirm: z.string(),
   }).refine((d) => d.password === d.confirm, {
     message: "Passwords must match",
     path: ["confirm"], // attaches error to the field, not the form root
   });
   export type SignupInput = z.infer<typeof signupSchema>;
   ```
   For inputs that arrive as strings but mean numbers/dates, use `z.coerce.number()` / `z.coerce.date()` so form values and server `FormData` both parse.

2. **Wire React Hook Form with the resolver.** Use `zodResolver`, set `defaultValues` for *every* field (uncontrolled inputs need them or they switch controlled→uncontrolled mid-edit), and pick a sane `mode`.
   ```ts
   const form = useForm<SignupInput>({
     resolver: zodResolver(signupSchema),
     defaultValues: { email: "", password: "", confirm: "" },
     mode: "onTouched", // validate after blur, then re-validate onChange — best UX default
   });
   ```
   - Native inputs (`<input>`, `<select>`): use `{...form.register("email")}`.
   - Custom/headless components (Select, DatePicker, anything not exposing a ref): wrap in `<Controller name=... control={form.control} render={...} />`. Mixing `register` on a controlled component silently drops values.

3. **Field arrays + nested objects** use `useFieldArray`. Key the rows by `field.id` (RHF's stable id), **never by array index** — index keys corrupt state on remove/reorder.
   ```ts
   const { fields, append, remove } = useFieldArray({ control: form.control, name: "items" });
   // register nested path:
   {...form.register(`items.${index}.name`)}
   ```
   Read nested errors via `form.formState.errors.items?.[index]?.name`.

4. **Multi-step / wizard:** one sub-schema per step; validate only the current step's fields before advancing with `await form.trigger(["fieldA","fieldB"])`. Keep all steps in **one** `useForm` instance (do not remount per step or you lose state). Persist between steps with a single `useForm` + (optionally) `localStorage`/URL state; validate the *full* schema on final submit. Compose with `signupSchema.pick({...})` or `.partial()` per step so the final type stays one source of truth.

5. **Next.js server actions** — validate inside the action, **return** typed errors, do not `throw` for validation:
   ```ts
   "use server";
   export async function signup(_prev: State, formData: FormData): Promise<State> {
     const parsed = signupSchema.safeParse(Object.fromEntries(formData));
     if (!parsed.success) {
       return { ok: false, errors: parsed.error.flatten().fieldErrors };
     }
     // ...mutate DB...
     revalidatePath("/dashboard"); // or revalidateTag — refresh cache after mutation
     return { ok: true };
   }
   ```
   On the client (React 19): `const [state, action, pending] = useActionState(signup, { ok: false });`. Bind RHF to the action with `<form action={action}>` and `form.handleSubmit` for client-side pre-check, or surface `state.errors` back into RHF via `form.setError`. **Always** re-validate server-side — client validation is UX, not security.

6. **Accessible errors** on every field:
   - `aria-invalid={!!errors.email}` on the input.
   - `aria-describedby="email-error"` pointing at the error node; the error node has `id="email-error"` and `role="alert"` (or sits in an `aria-live="polite"` region) so SRs announce it.
   - Associate a real `<label htmlFor>`; placeholders are not labels.
   - On failed submit, **focus the first errored field**. RHF does this with `shouldFocusError: true` (default) for registered native inputs; for `Controller`/custom inputs, focus manually in the submit-error handler.

7. **Async validation** (e.g. "username taken"): debounce the check (~300–500ms), and validate server-side too. Either a Zod `.refine(async ...)` (requires `parseAsync`/`safeParseAsync` — `zodResolver` handles this) or `form.setError("username", { message })` after a fetch. Disable submit while `formState.isValidating || isSubmitting` to prevent races.

## Common Errors

- **`defaultValues` missing → "controlled to uncontrolled" warning** and lost values. Always seed every field, including arrays (`{ items: [] }`).
- **Field array keyed by index** → on `remove(2)` the wrong rows re-render / values shift. Key by `field.id`.
- **`Controller` value not updating** because the inner component fires a non-standard onChange — map it: `onChange={(v) => field.onChange(v)}`. Don't spread `register` onto a controlled component.
- **`refine`/`superRefine` error lands on form root, not the field** → user sees no inline message. Set `path: ["confirm"]`.
- **`z.coerce` forgotten for number/checkbox inputs** → `FormData` gives `"3"`/`"on"`, schema expects `number`/`boolean`, every submit fails validation silently.
- **Server action `throw` for invalid input** → blows up as an error boundary / 500 instead of inline errors. Use `safeParse` + return.
- **Forgot `revalidatePath`/`revalidateTag` after mutation** → UI shows stale cached data post-submit even though the DB changed.
- **Re-mounting `useForm` per wizard step** wipes earlier answers. One instance, conditionally render steps.
- **Trusting client validation only** — bypassable; the server action must re-`safeParse`.
- **Zod v3 vs v4 mismatch**: `.flatten()` and the error object shape changed across majors. Check the installed version before copying error-extraction code.
- **`mode: "onChange"` on a big form** → validates on every keystroke, janky + noisy errors before the user finishes typing. Prefer `onTouched` / `onBlur`.

## Verify

Run these before declaring done — show evidence, not just "fixed":

1. **Type check:** `npx tsc --noEmit` (or the project's typecheck script) passes — confirms `z.infer` and form generics line up.
2. **Lint:** project ESLint passes on touched files.
3. **Happy path:** submit valid data → action runs, success state shows, cache revalidates (data refreshes without a hard reload).
4. **Validation path:** submit each invalid field → inline error appears under the right field, submit is blocked, no 500/error boundary.
5. **A11y spot-check:** invalid field has `aria-invalid="true"` and `aria-describedby` resolving to a visible error node; first errored field receives focus on failed submit. Verify in the DOM/accessibility tree (e.g. devtools snapshot), not by eye alone.
6. **Field array / wizard** (if present): add → remove a middle row → values of remaining rows stay correct; advancing a step only validates that step; final submit validates the whole schema.
7. If a contract or behavior is testable, add/run a unit test on the schema (`safeParse` of good + bad payloads) so the validation can't silently regress.
