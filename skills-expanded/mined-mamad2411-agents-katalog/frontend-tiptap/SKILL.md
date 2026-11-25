---
name: frontend-tiptap
description: Use when building a rich-text editor with TipTap — schemas, extensions, collaboration, custom marks/nodes, content serialization, React integration.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: domain
  languages: [react, typescript]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-18"
  related: [react, typescript, ts-zod, frontend-tailwind, frontend-react-hook-form, frontend-msw, ux-wcag-a11y]
---

# TipTap

**Iron Law: JSON is the source of truth, never HTML. Store `editor.getJSON()`; render through `generateHTML()` or the editor itself. HTML round-trips lose unknown marks, can carry XSS, and serialize whatever the browser felt like emitting. JSON matches the schema exactly.**

**Versions:** Current `TipTap 2.10` (`@tiptap/react`, `@tiptap/starter-kit`) · No LTS series — _2.x is stable; the v3 beta exists but breaks extension APIs and isn't shipped. Always pin `@tiptap/_`packages to the same minor — mixing`2.10`and`2.8` cores produces silent schema mismatches.\*

## Mental model: ProseMirror schema

TipTap is a thin React wrapper over ProseMirror. Everything is a **schema** of:

| Concept       | What it is                                              | Examples                                                   |
| ------------- | ------------------------------------------------------- | ---------------------------------------------------------- |
| **Node**      | A block or inline element with its own boundary         | `paragraph`, `heading`, `bulletList`, `image`, `codeBlock` |
| **Mark**      | Inline formatting _applied to_ text inside a node       | `bold`, `italic`, `link`, `code`, `strike`                 |
| **Extension** | A plugin that registers nodes/marks/keymaps/input rules | `StarterKit` bundles 15+                                   |

A node can be `block` or `inline`, and either `atom` (no children — like `image`) or composite (`paragraph` holds text). Marks can't span across block boundaries by definition.

## StarterKit baseline

```tsx
import { useEditor, EditorContent } from "@tiptap/react";
import StarterKit from "@tiptap/starter-kit";

const editor = useEditor({
  extensions: [
    StarterKit.configure({
      heading: { levels: [1, 2, 3] },
      codeBlock: false, // disable in favor of CodeBlockLowlight below
    }),
  ],
  content: initialJSON, // ProseMirror JSON, not HTML
  onUpdate: ({ editor }) => onChange(editor.getJSON()),
});
```

StarterKit includes: `document`, `paragraph`, `text`, `heading`, `bold`, `italic`, `strike`, `code`, `codeBlock`, `bulletList`, `orderedList`, `listItem`, `blockquote`, `horizontalRule`, `hardBreak`, `history`, `dropcursor`, `gapcursor`. Disable individually via `.configure({ thing: false })` when you replace one.

## Common extensions

| Extension         | Package                                                | Use                                              |
| ----------------- | ------------------------------------------------------ | ------------------------------------------------ |
| Link              | `@tiptap/extension-link`                               | `<a>` with `openOnClick` + `protocols` allowlist |
| Image             | `@tiptap/extension-image`                              | inline images; pair with upload pipeline (below) |
| Table             | `@tiptap/extension-table` + `-row`, `-cell`, `-header` | resizable tables; heavy — load lazily            |
| CodeBlockLowlight | `@tiptap/extension-code-block-lowlight`                | syntax highlighting via `lowlight`               |
| Placeholder       | `@tiptap/extension-placeholder`                        | "Write something…" empty-state hint              |
| CharacterCount    | `@tiptap/extension-character-count`                    | limits + word counts                             |
| Mention           | `@tiptap/extension-mention`                            | `@user` chips; requires a suggestion renderer    |

## React integration

```tsx
function Editor({ value, onChange }: { value: JSONContent; onChange: (j: JSONContent) => void }) {
  const editor = useEditor({
    extensions: [StarterKit],
    content: value,
    onUpdate: ({ editor }) => onChange(editor.getJSON()),
  });
  return <EditorContent editor={editor} />;
}
```

**Controlled-ish pattern.** TipTap is internally controlled; React just feeds initial content and listens to updates. **Do not** call `editor.commands.setContent(value)` on every render — that nukes selection and history. Only call it when the document genuinely changes from outside (e.g., loading a new doc id):

```tsx
useEffect(() => {
  if (editor && docId !== prevDocId.current) {
    editor.commands.setContent(value, false); // false = don't emit update
    prevDocId.current = docId;
  }
}, [editor, docId, value]);
```

## Custom mark or node

```ts
// extensions/highlight.ts — a custom mark
import { Mark, mergeAttributes } from "@tiptap/core";

export const Highlight = Mark.create({
  name: "highlight",
  parseHTML() {
    return [{ tag: "mark" }];
  },
  renderHTML({ HTMLAttributes }) {
    return ["mark", mergeAttributes(HTMLAttributes, { class: "bg-yellow-200" }), 0];
  },
  addCommands() {
    return {
      toggleHighlight:
        () =>
        ({ commands }) =>
          commands.toggleMark(this.name),
    };
  },
});
```

Nodes get the same shape (`Node.create({...})`) with extra `group: "block"`, `content: "inline*"`, `atom: true|false`. Register in the `extensions` array of `useEditor`.

## Collaboration (Yjs + y-prosemirror)

```ts
import * as Y from "yjs";
import { WebsocketProvider } from "y-websocket";
import Collaboration from "@tiptap/extension-collaboration";
import CollaborationCursor from "@tiptap/extension-collaboration-cursor";

const ydoc = new Y.Doc();
const provider = new WebsocketProvider("wss://yjs.example.com", roomId, ydoc);

const editor = useEditor({
  extensions: [
    StarterKit.configure({ history: false }), // Yjs owns history now
    Collaboration.configure({ document: ydoc }),
    CollaborationCursor.configure({
      provider,
      user: { name: currentUser.name, color: currentUser.color },
    }),
  ],
});
```

Critical: disable `StarterKit.history` — Yjs has its own undo stack; running both produces undo chaos. The Yjs `Y.XmlFragment` _is_ the document; `getJSON()` still works for persistence, but the live source of truth is `ydoc`.

## Sanitization (input and output)

| Boundary                     | Risk                                              | Treatment                                                                                                                                 |
| ---------------------------- | ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Paste from clipboard         | `<script>`, inline event handlers, hostile styles | TipTap's parser drops unknown nodes/marks by schema. Add `transformPastedHTML` to strip `<script>`, `onerror=`, etc., as belt-and-braces. |
| Loading saved content        | JSON tampered server-side                         | Validate with zod against your schema shape (`Skill(ts-zod)`) before passing to `setContent`.                                             |
| Rendering output server-side | Stored JSON → HTML → page                         | Use `generateHTML(json, extensions)` + DOMPurify. Never inject raw `editor.getHTML()` into the DOM without DOMPurify wrapping it first.   |

## Serialization formats

| Format                    | Use                          | Caveat                                                          |
| ------------------------- | ---------------------------- | --------------------------------------------------------------- |
| JSON (`editor.getJSON()`) | Storage, diff, validation    | Schema-versioned — coordinate migrations when extensions change |
| HTML (`editor.getHTML()`) | Email export, print          | Lossy on round-trip; sanitize before render                     |
| Markdown                  | Display in non-rich contexts | Use `tiptap-markdown` (community) — official support is limited |

**Pick JSON for storage. Period.** Convert to HTML or Markdown at render time.

## Image upload pipeline

```ts
editor.setOptions({
  editorProps: {
    handlePaste(view, event) {
      const file = event.clipboardData?.files[0];
      if (!file || !file.type.startsWith("image/")) return false;
      event.preventDefault();
      uploadImage(file).then((url) => {
        editor.chain().focus().setImage({ src: url, alt: file.name }).run();
      });
      return true;
    },
  },
});
```

Upload via `Skill(frontend-msw)`-mocked endpoint in tests. **Don't** stuff base64 data URIs into the document — JSON balloons, every save re-uploads, mobile chokes.

## Anti-patterns

- **HTML as source of truth.** Round-trip through HTML loses unknown marks and invites XSS. JSON only.
- **Calling `setContent` on every render.** Resets selection + undo. Only call when the document id changes.
- **Both Yjs and StarterKit history enabled.** Undo behaves like a slot machine.
- **Injecting `editor.getHTML()` into the DOM unsanitized** (server-side or via raw-HTML React props). Always run DOMPurify over editor HTML before render. XSS via paste otherwise.
- **Mixing TipTap minor versions.** `@tiptap/core@2.10` + `@tiptap/extension-link@2.8` → silent schema mismatch. Pin all `@tiptap/*` together.
- **Forgetting `editor.destroy()`** when not using `useEditor` (which handles it). Memory leak.
- **Inline-styling everything via marks.** Marks are formatting categories, not arbitrary styles. Use a `Style` mark with a controlled vocabulary, not a free-form attribute bag.
- **Conditional extensions per render.** Extensions are registered once on mount. Toggle behavior via commands, not by mutating the array.

## Red flags

| Thought                                              | Reality                                                                                         |
| ---------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| "I'll store HTML, it's easier"                       | Wait until you need to add a feature that needs to inspect structure. Now you regex-parse HTML. |
| "Just inject the editor HTML straight into the page" | XSS via paste — a user pastes `<img onerror>` from somewhere. Run DOMPurify on every render.    |
| "Yjs + StarterKit history together for robustness"   | Two undo stacks fight; undo skips, redo doubles. Pick one.                                      |
| "I'll write my own schema from scratch"              | StarterKit covers 90%. Start there, replace pieces.                                             |
| "Base64 images in the doc"                           | Document grows 1.5× per image (base64 overhead). Upload to object storage, store the URL.       |

## Hand-off

For React rules and the controlled/uncontrolled distinction: `Skill(react)`. For validating loaded JSON shape: `Skill(ts-zod)`. For forms that contain a TipTap editor field: `Skill(frontend-react-hook-form)`. For mocking upload endpoints in tests: `Skill(frontend-msw)`. For toolbar a11y (ARIA toolbar, focus management): `Skill(ux-wcag-a11y)`.
