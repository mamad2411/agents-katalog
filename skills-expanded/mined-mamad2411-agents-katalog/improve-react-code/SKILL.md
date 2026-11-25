---
name: improve-react-code
description: Find composition and state-lifting refactor opportunities in a React codebase. Audits for boolean-prop bloat, monolith components with variant explosion, sibling clusters that should share lego-brick subcomponents, render-prop slots that can't reach outside the box, and state synced between siblings via useEffect. Use when the user wants to improve react code, audit react components, find react refactor opportunities, run a react composition review, or asks "improve react", "audit react", "react architecture review".
---

# Improve React Code

Find refactor opportunities in the React side of a codebase, focused on composition and lifted state.

React codebases drift toward monolithic components: every new variant adds another boolean prop, another render-prop slot, another optional field in a config array. Eventually the file is hard to peek inside — for humans and AI alike. The way out is composition — split variants into distinct components built from a small set of named subcomponents and a lifted state provider.

A 15-boolean monolith is worth fixing on its own, but the biggest wins come from clusters of similar siblings (e.g. `CreateUserForm` and `UpdateUserForm`) that could share the same extracted pieces. Lifting state and replacing prop bloat with JSX is where most friction relaxes.

## Glossary

- **Brick** — a small, named subcomponent reused across variants (`UserFormHeader`, `ModalFooter`, `Wizard.Step`).
- **Lifted provider** — the context `Provider` extracted into its own component that takes `children`, so siblings outside the visual box can read its state and actions.
- **Sibling cluster** — 2+ components in the same feature that share most of their structure but differ in variant logic (e.g. `CreateUserForm` and `UpdateUserForm`, or `ChannelDialog` and `ThreadDialog`).
- **State slot** — `state` / `actions` / `meta` exposed via context. Children read from it; the implementation (useState, store, custom hook) lives in the component that renders the provider.
- **Meta** — the slot for non-state values (e.g. an `inputRef`) that several siblings need access to. Avoids `useImperativeHandle` and ref drilling.

## Core principles

Audit findings should be framed in terms of these principles. Reference them by short name in the **Problem** field of each candidate.

1. **Boolean props that gate which subtree renders → split into distinct components.** `<UserForm isUpdate>` becomes `<CreateUserForm>` and `<UpdateUserForm>`, sharing a `UserFormProvider`, `UserFormFields`, `UserFormSubmit`.
2. **Compound components.** Build features as a Provider + named subcomponents (Header, Body, Footer, Submit, etc.) plus distinct action subcomponents.
3. **JSX over arrays-of-config for variant UI.** Replace `[{label, isSortable, divider, isMenu, items}]` with `<Table.Column>`, `<Table.Divider>`, `<Table.MenuColumn>`.
4. **"Common*" wrappers are JSX inside JSX**; they never take their own boolean variants.
5. **Don't render absent UI by toggling a boolean — just don't render it.** A dialog that has no dropzone simply omits `<Dialog.Dropzone>`. No `disableDropzone` prop.
6. **Avoid `renderX` slot props as the primary surface.** They don't survive when the slot needs to render outside the visual box (e.g. a Modal whose Forward button lives below the modal). Children-as-function — for sharing internal state with the caller — is a different, valid pattern.
7. **Provider exposes `{ state, actions, meta }`.** Implementation lives in the component that renders the provider. Children stay agnostic — they work whether state is ephemeral, persisted, or synced across devices. The `actions` and `meta` slots are open-ended bags — start small (`actions={{ update: setState }}`) and grow them as new operations show up (`{ update, submit }`). When state comes from a custom hook (e.g. `useSyncedDraft`, `useFormStore`), the hook's return shape must conform to the provider's interface.
8. **Lift state by extracting the provider.** `<WizardProvider>{children}</WizardProvider>` lets Next/Back buttons rendered as siblings of the wizard read context directly — no `onStepChange` callback or shared ref. In practice, this usually means moving the provider into its own file (`WizardProvider.tsx`) so it can wrap the visual `Wizard.tsx` *and* whatever sits next to it.
9. **Use `meta` for refs and non-state values** instead of `useImperativeHandle` or ref drilling.
10. **Don't sync sibling state via `useEffect`.** A `useEffect(() => onChange(state), [state])` whose only job is lifting state up is the `onFormStateDidChange` smell. Lift the provider instead.
11. **Don't fear context re-renders.** React Compiler memoizes consumers by the slice they actually read.

Plus, prop-API hygiene:

- **Don't use `React.FC`.** Type props with an interface on the function parameter.
- **Prop API decision flow:** lists → `items` + `renderItem`; variants without internal data → `children` (compound); variants needing internal data → children-as-function; simple ReactNode swap → slot prop; 3+ props describing the same element → single slot prop; simple variants → value prop (`variant="ghost"`).
- **File placement:** feature folder first; shared `components/` only when 2+ features use it.
- **Composition over rigid props.** Prefer `<Button>{icon}{label}</Button>` over `<Button icon label />`.

## Threshold — when NOT to flag

Refuse to flag a component for compound-component refactoring unless **at least one** is true:

- (a) ≥2 distinct callers shape it differently.
- (b) The same condition is checked in ≥2 JSX branches inside one component.
- (c) UI rendered outside the visual box needs the component's state/actions.
- (d) Variants need different state-management implementations (ephemeral vs synced, etc.).
- (e) **Strongest signal** — 2+ similar components **reimplement** the same internals instead of composing shared bricks. Distinct pages or variants are *not* the smell — `CreateUserPage` and `EditUserPage` existing as separate pages is correct, the same way Fernando's `ChannelComposer`, `ThreadComposer`, and `EditMessageComposer` are correctly separate. The smell is when each one carries its own copy of the form fields, the upload handler, the lifecycle, instead of composing shared `Header`, `Fields`, `Submit` pieces. Look for the *missing* shared brick, not the *existing* sibling.

Below that threshold, single booleans, single render-prop slots, and children-as-function are fine. Don't refactor for the sake of it.

## When duplication is the right call

DRY is a goal, not a rule. **Prefer duplication over the wrong abstraction**. Wrong abstractions accumulate conditionals over time as new requirements force them to flex; duplication stays honest and easy to delete. Leave repetition alone when:

- **Two callers + small block.** Rule of Three: asking *"haven't I written this before?"* twice is fine — on the third occurrence the pattern starts to scream. Two callers of a 5-line block is below threshold. Two callers of a 100-line form is not — substantial duplication earns extraction at two.
- **The duplicates might evolve independently.** Two forms in different domains (staff vs client, payments vs shipping) may look identical today and diverge as each domain grows. Forcing them through one shared API makes future divergence painful — the abstraction grows conditional flags to accommodate. Optimize for change.
- **The abstraction would leak its implementation.** A hook with 8 parameters, a brick with 5 render-prop slots, or a component with `hasX` / `disableY` flags is the abstraction failing. Two duplicated implementations are more readable than one over-parameterized one.
- **The repeated block is trivial.** A default `[]`, a `setState(false)` reset, a `className` concatenation — these don't earn names. Reading them in place beats jumping to another file.
- **The use cases haven't crystallized.** If you'd have to guess what callers will need, you'll guess wrong. Wait for the patterns to scream — not whisper.

When in doubt, leave the duplication. The audit should propose abstractions only when the patterns *scream*.

## Shape — provider vs custom hook

Once a finding passes the threshold, decide *what shape* the abstraction takes. Don't reach for a provider every time.

- **Shared state across siblings** → **lifted provider** with `{ state, actions, meta }`. Use this when multiple components need to read or update the same values (wizard step, selected appointment, draft form contents).
- **Shared lifecycle around a callback** → **custom hook**. Use this when each consumer owns its own state but repeats the same `saving / error / success / handleSave` boilerplate around a callback. `useSectionForm(saveFn, onSaved)` returning `{ saving, error, success, handleSave }` is the canonical shape.
- **One-shot imperative interactions** (confirm dialogs, toasts) → **imperative hook** like `useConfirm()` returning `{ confirm }` that owns its own open/saving lifecycle internally. The call site just `await`s it.

If the proposed solution is a hook, none of the compound-component principles (provider, frame, named subcomponents) apply — the hook *is* the abstraction.

## Process

### 1. Explore

Use the Agent tool with `subagent_type=Explore` to walk the React side of the codebase. Don't follow rigid heuristics — explore organically, but also:

- Scan for **name-stem clusters** (`*Form`, `*Modal`, `*Dialog`, `*Card`, `*List`, `*Wizard`, `*Sheet`, `*Drawer`, `*Panel`, `*Composer`).
- For each cluster, read the candidate components and judge structural similarity by eye. Two components share a "substructure" when they render a recognizable named region (header, body, footer, action row, input area, etc.) the same way. A cluster qualifies when ≥2 components share ≥3 substructures.
- Note components with high prop count (many booleans), `useEffect` whose only job is calling a parent setter, `useImperativeHandle` outside design-system primitives, and array-of-config UI with heterogeneous item shapes.
- **Trace prop-drilling depth.** Pick stateful props (state values, setters, callbacks owned higher up). Follow each one down the tree. If a prop is forwarded through ≥3 components that do not consume it themselves, that's threshold-(c) firing — the leaf component is reaching back to the root via the intermediate layers. "It works" is not an excuse: pass-through layers are exactly the smell. Cite the chain explicitly in the finding (e.g. `Page → DayView → StaffColumn → AppointmentBlock`).
- **Trace prop fan-out at a single level.** Beyond depth, count props passed to a single child component. If a parent passes ≥10 props (state, setters, callbacks combined) to one child, that's principle 8 firing — the child is a state-drop because the parent owns state the child should read from context. Common shape: wizard steps each receiving `step`, `selection`, `setSelection`, `loading`, `setLoading`, `data`, `setData`, `onNext`, `onBack`, `onSubmit`. Even with no depth-drilling, this is the lift-the-provider signal. Cite the prop count and the receiving component in the finding.

Apply the **threshold** before promoting any finding into the report.

### 2. Verify before promoting

For each candidate that passes the threshold, run three checks before adding it to the report. This filters out the most common failure modes: hallucinated extractions, premature abstractions, and misidentified state machines.

1. **Structural identity check.** Are the alleged duplicates actually structurally identical, or do they just *look* similar? Open both files. List the substructures (header, body, footer, validation, error handling). Compare 1:1. If the *same* JSX shape is rendered with different validators, different success paths, or different button arrangements, the duplication is shallower than it looks.

2. **Load-bearing divergence check.** Would the proposed abstraction force divergent cases through one API surface? If a brick proposed for "shared chrome" would force some consumers to use escape hatches because their footer, header, or action shape genuinely differs (one needs Save/Cancel, another needs Activate/Deactivate, another needs no buttons), the brick is too thin. Propose a richer API (slot, children, render-prop) — or downgrade the finding to "split the file" without proposing a chrome brick.

3. **State-machine vs boolean-bloat check.** A boolean or enum prop deciding which subtree renders is a smell *only when* the branches are variants of *the same thing*. If `mode === "draft"` shows an Edit button and `mode === "published"` shows an Unpublish button, those are semantically distinct operations on different states — that's a state machine, and the branching is correct. Don't flag.

**If any check fails, demote or drop.** Demote Critical → Medium → Bikeshedding when the underlying signal is real but the proposed shape is wrong. Drop entirely when the finding is a hallucination (the alleged duplicate doesn't exist) or a misidentified state machine. Note dropped findings briefly in the "What I left out" section so the user knows they were considered.

### 3. Present numbered candidates

Return a numbered list. Each candidate:

- **Files** — paths involved.
- **Problem** — which principle is being violated, in plain English. Reference the principle by short name.
- **Solution** — sketch the proposed compound API in flat-export style (`<UserFormProvider>`, `<UserFormFields>`, `<UserFormSubmit>`) — unless the codebase already uses dot-namespaced compound, in which case match that.
- **Reuse map** — which **existing** components would consume the extracted bricks. Cite real consumers only — don't speculate about hypothetical future use cases ("future bulk import," "could be used for X"). This is what makes a finding *Critical*.
- **Severity** — Critical / Medium / Bikeshedding (see below).
- **Benefits** — testability, fewer call-site shapes, AI navigability.

Do NOT propose detailed interfaces yet. Ask: *"Which of these would you like to explore?"*

> **No subsumption.** If a narrow finding (e.g. two duplicated staff forms) fits inside a broader one (e.g. a cross-feature lifecycle pattern), surface **both** as separate candidates. They have different right answers — the narrow one may need a provider extraction while the broader one needs a hook. Don't drop the smaller finding because the bigger one "covers it." A 100-line two-component duplication and a 10-call-site lifecycle hook are independent wins.

### 4. Grilling loop

Once the user picks a candidate, walk the design tree: what becomes a brick, what stays a one-off, where the provider sits, who lifts state, what `meta` carries, which siblings need access. Output a recommended interface (set of compound parts + provider shape) that the user can hand to Claude to implement.

## Detection signals, tiered

**Critical** — lead the report:

- Sibling clusters with shared bricks (threshold clause e).
- ≥3 boolean props gating JSX subtrees, used in ≥2 distinct shapes.
- State sync between siblings via `useEffect` (`onFormStateDidChange` smell).
- UI outside the visual box reaching back in via callbacks or shared refs.

**Medium**:

- Same condition checked in ≥2 JSX branches inside one component.
- `renderX` slot prop where the slot needs internal state and could live in context.
- Array-of-config UI with heterogeneous item shapes (`isMenu`, `divider`, `items`).
- `useImperativeHandle` for things that could live in context `meta`.
- File placement (feature-folder vs shared `components/`).

**Bikeshedding** — collapsed at the bottom of the report:

- `React.FC` usage.
- Lone components with 1–2 boolean props and a single call site.
- Render-prop slots that work fine and don't escape the box.
- 3+ props describing the same element with only 1 caller.

## Examples

Five canonical refactors. Use these as templates when sketching Solution shapes in the report.

### 1. Boolean-bloat → split into siblings sharing bricks

```tsx
// BEFORE
function UserForm({ isUpdate, hideWelcome, hideTerms, onSuccess }) {
  const user = isUpdate ? useUser() : null;
  return (
    <form>
      {!hideWelcome && <Welcome />}
      <Fields initialUser={user} />
      {!hideTerms && <Terms />}
      <button>{isUpdate ? "Save" : "Create"}</button>
    </form>
  );
}

// usage:
<UserForm isUpdate hideWelcome hideTerms onSuccess={...} />
<UserForm onSuccess={...} />
```

```tsx
// AFTER
function UserFormProvider({ initialUser, children }) {
  const [draft, setDraft] = useState(initialUser ?? emptyUser);
  return <Ctx.Provider value={{ draft, setDraft }}>{children}</Ctx.Provider>;
}
function UserFormFields() { /* reads ctx */ }
function UserFormSubmit({ children }) { /* reads ctx, posts */ }

function CreateUserForm() {
  return (
    <UserFormProvider>
      <Welcome />
      <UserFormFields />
      <Terms />
      <UserFormSubmit>Create</UserFormSubmit>
    </UserFormProvider>
  );
}

function UpdateUserForm() {
  const user = useUser();
  return (
    <UserFormProvider initialUser={user}>
      <UserFormFields />
      <UserFormSubmit>Save</UserFormSubmit>
    </UserFormProvider>
  );
}
```

### 2. Sibling state-sync via callback → lifted provider

```tsx
// BEFORE — Next/Back live outside the wizard, state is drilled
function Page() {
  const [step, setStep] = useState(0);
  return (
    <>
      <Wizard step={step} onStepChange={setStep} />
      <BackButton onClick={() => setStep((s) => s - 1)} />
      <NextButton onClick={() => setStep((s) => s + 1)} />
    </>
  );
}
```

```tsx
// AFTER — provider wraps Wizard *and* the buttons
function WizardProvider({ children }) {
  const [step, setStep] = useState(0);
  return <Ctx.Provider value={{ step, setStep }}>{children}</Ctx.Provider>;
}
function Wizard() { const { step } = useWizard(); /* renders step UI */ }
function BackButton() { const { setStep } = useWizard(); /* ... */ }
function NextButton() { const { setStep } = useWizard(); /* ... */ }

function Page() {
  return (
    <WizardProvider>
      <Wizard />
      <BackButton />
      <NextButton />
    </WizardProvider>
  );
}
```

### 3. Repeated lifecycle → custom hook (not a provider)

```tsx
// BEFORE — every section reimplements the same save lifecycle
function ProfileSection() {
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const handleSave = async () => {
    setSaving(true); setError(null);
    try { await saveProfile(); setSuccess(true); }
    catch (e) { setError(e); }
    finally { setSaving(false); }
  };
  return /* ... */;
}
// PreferencesSection, BookingSection — same 12 lines copy-pasted
```

```tsx
// AFTER — one hook, three call sites, each owns its own state
function useSectionForm(saveFn) {
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const handleSave = async () => {
    setSaving(true); setError(null);
    try { await saveFn(); setSuccess(true); }
    catch (e) { setError(e); }
    finally { setSaving(false); }
  };
  return { saving, error, success, handleSave };
}

function ProfileSection() {
  const { saving, error, handleSave } = useSectionForm(saveProfile);
  return /* ... */;
}
```

> Note: there is no shared state across sections — each call to `useSectionForm` gets its own. The shared thing is the *lifecycle shape*, not the values. That's why a hook fits, not a provider.

### 4. Per-caller confirm state → imperative `useConfirm()` hook

```tsx
// BEFORE — every consumer manages its own confirm dialog
function AppointmentCard() {
  const [pendingDelete, setPendingDelete] = useState(false);
  const [deleting, setDeleting] = useState(false);
  return (
    <>
      <button onClick={() => setPendingDelete(true)}>Delete</button>
      <ConfirmDialog
        open={pendingDelete}
        saving={deleting}
        onConfirm={async () => { setDeleting(true); await deleteAppt(); }}
        onCancel={() => setPendingDelete(false)}
      />
    </>
  );
}
```

```tsx
// AFTER — call site is one line; the hook owns the dialog
function AppointmentCard() {
  const { confirm } = useConfirm();
  return (
    <button
      onClick={async () => {
        if (await confirm({ title: "Delete?", message: "Cannot be undone." })) {
          await deleteAppt();
        }
      }}
    >
      Delete
    </button>
  );
}
```

### 5. `renderX` slot prop → compound subcomponent reading context

```tsx
// BEFORE — footer slot can't access modal's internal state
function Modal({ title, renderFooter, children }) {
  const [busy, setBusy] = useState(false);
  return (
    <Dialog>
      <header>{title}</header>
      <main>{children}</main>
      <footer>{renderFooter?.({ busy, setBusy })}</footer>
    </Dialog>
  );
}

<Modal
  title="Edit"
  renderFooter={({ busy, setBusy }) => (
    <button disabled={busy} onClick={() => { setBusy(true); save(); }}>Save</button>
  )}
>
  <Form />
</Modal>
```

```tsx
// AFTER — Modal.Footer is a real component reading modal context
function ModalProvider({ children }) {
  const [busy, setBusy] = useState(false);
  return <Ctx.Provider value={{ busy, setBusy }}>{children}</Ctx.Provider>;
}
function Modal({ children }) { /* renders Dialog shell */ }
function ModalHeader({ children }) { /* ... */ }
function ModalBody({ children }) { /* ... */ }
function ModalFooter({ children }) { /* ... */ }

<ModalProvider>
  <Modal>
    <ModalHeader>Edit</ModalHeader>
    <ModalBody><Form /></ModalBody>
    <ModalFooter>
      <SaveButton />  {/* reads { busy, setBusy } from context */}
    </ModalFooter>
  </Modal>
</ModalProvider>
```

> If the Save button needs to live *outside* the Modal box (e.g. in a sticky page footer), it still works — it just needs to be rendered inside `<ModalProvider>`. That's the lifted-provider payoff.

### 6. Hide-flags → just don't render the part

```tsx
// BEFORE — a single component with toggles for every variant
function Dialog({ title, hideHeader, hideTitle, disableDropzone, children }) {
  return (
    <Shell>
      {!hideHeader && (
        <header>{!hideTitle && <h2>{title}</h2>}</header>
      )}
      {!disableDropzone && <Dropzone />}
      <main>{children}</main>
    </Shell>
  );
}

<Dialog title="Edit" hideHeader disableDropzone>...</Dialog>
<Dialog title="Forward" hideTitle>...</Dialog>
```

```tsx
// AFTER — the absence of the part *is* the variant
function Dialog({ children }) { return <Shell>{children}</Shell>; }
function DialogHeader({ children }) { return <header>{children}</header>; }
function DialogTitle({ children }) { return <h2>{children}</h2>; }
function DialogDropzone() { /* ... */ }

// Edit dialog has no header and no dropzone — just don't render them
<Dialog>
  <main>...</main>
</Dialog>

// Forward dialog has a header but no title
<Dialog>
  <DialogHeader>...</DialogHeader>
  <DialogDropzone />
  <main>...</main>
</Dialog>
```

> No `hideX` / `disableX` props anywhere. The boolean is implicit in whether the JSX is present.

### 7. Array-of-config → JSX subcomponents

```tsx
// BEFORE — heterogeneous item shapes hidden behind a config array
<DataTable
  columns={[
    { key: "name", label: "Name", isSortable: true },
    { divider: true },
    { isMenu: true, items: [{ label: "Edit" }, { label: "Delete" }] },
  ]}
/>
```

```tsx
// AFTER — flat JSX, easy to escape into one-offs
<DataTable>
  <DataTable.Column field="name" sortable>Name</DataTable.Column>
  <DataTable.Divider />
  <DataTable.MenuColumn>
    <DataTable.MenuItem>Edit</DataTable.MenuItem>
    <DataTable.MenuItem>Delete</DataTable.MenuItem>
  </DataTable.MenuColumn>
</DataTable>
```

## Style for proposed solutions

Default to **flat separate exports**:

```tsx
<UserFormProvider>
  <UserFormFields />
  <UserFormSubmit />
</UserFormProvider>
```

If the codebase already uses dot-namespaced compound (`<UserForm.Fields>`), match that — respect existing convention. The underlying composition principles are identical either way.

## Skips (default)

- `*.test.tsx`, `*.spec.tsx`, `*.stories.tsx`.
- Generated/codegen output (`*.gen.*`, GraphQL types).
- `node_modules`, `dist`, `build`, `.next`, `out`.
- Design-system primitives by location (`components/ui/`, `design-system/`, `primitives/`) and tiny single-export leaf files.
- Files under 50 lines.

User-targeted paths (e.g. `improve-react-code path/to/file.tsx`) bypass every skip — explicit beats implicit.

## Notes

- **Agnostic to state-management library.** The provider's interface is `{ state, actions, meta }`; the implementation can be `useState`, Zustand, Redux, a sync hook, or anything else.
- **React Compiler** removes most context-perf objections — a consumer is memoized by the slice it reads.
