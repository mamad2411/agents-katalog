---
alwaysApply: false
description: React code readability pass — apply after generating any React component
---

# React readability pass

After generating or modifying any React component, perform a dedicated readability
pass before considering the task complete. Do not combine this with implementation.
The sole job of this pass is to make the code easy to read at a glance — not to
change behaviour, not to refactor logic, not to add features.

---

## Principles

**Code is written for the next reader, not the machine.**
A component should read top to bottom like a short document. Someone who has never
seen this file should be able to understand what it does within thirty seconds.

**Names express intent, not implementation.**
A name should tell you what a thing *means* in the context of this component, not
what it technically is. `likesCount` over `likes`. `previousCommentsState` over
`prev`. `isLiked` over `liked`. If you have to read the surrounding lines to
understand a name, the name is wrong.

**Whitespace is punctuation.**
A blank line means "these two groups of things are unrelated." No blank line means
"these things belong together." Blank lines are not decorative — use them only where
the grouping boundary is real. Never use more than one blank line between groups.

**Handlers and helpers are different things. Name and group them accordingly.**
A handler responds to a user gesture and owns the try/catch, the toast, the
side-effect. A helper mutates state on behalf of a handler or a child component —
it is an imperative command, not an event response. They serve different purposes
and belong in separate groups.

**Abstraction is earned, not assumed.**
Do not extract a function because it is more than N lines. Extract it when the
extraction has a name that is more expressive than the code it replaces, and when
that name makes the call site read more clearly. Otherwise, leave it inline.

---

## Component template

Use this ordering for every component. Do not reorder sections.
Separate each section with exactly one blank line.

```tsx
// ─── 1. Props destructuring ───────────────────────────────────────────────────
// Destructure immediately. Never access props.x anywhere below this block.
// Name every destructured value for what it means in this component, not what
// the parent called it if those differ.

const {
  thumbnailUrl,
  username,
  id,
} = props.post;

// ─── 2. State ─────────────────────────────────────────────────────────────────
// All useState calls together. Name state variables for the thing they hold,
// not for their setter. Context that the component "lives on" goes here too —
// it is incoming data, same category as state.

const [likesCount, setLikesCount] = useState(Number(likes));
const [postComments, setPostComments] = useState(comments);
const [currentUser] = useContext(CurrentUserContext);

// ─── 3. Derived values ────────────────────────────────────────────────────────
// Values computed from state or props. useMemo if expensive, plain const if not.
// Never derive inside JSX — give the value a name here so the return stays clean.

const isPostOwner = currentUser?.username === username;
const hasComments = postComments.length > 0;

// ─── 4. Effects ───────────────────────────────────────────────────────────────
// useEffect calls. One blank line between each effect if there are multiple.
// If an effect needs a comment to explain why it exists, write the comment.

useEffect(() => {
  // reason this effect exists, if non-obvious
}, [dependency]);

// ─── 5. Handlers ──────────────────────────────────────────────────────────────
// Functions that respond directly to user gestures (clicks, submits, changes).
// Naming convention: onVerb + Noun + Action — e.g. onClickLikePost, onSubmitLoginForm.
// Handlers own the try/catch, the toast, and any async side-effect.
// One blank line between each handler.

const onClickDeletePost = async () => {
  try {
    const response = await deletePost(id);
    if (response) {
      toast.success("Post deleted!");
    }
  } catch (error) {
    console.error(error);
    toast.error("Failed to delete post. Please try again.");
  }
};

const onClickLikePost = async () => {
  const likePayload = {
    user_id: currentUser.userID,
    post_id: id,
  };
  try {
    const response = await likePost(likePayload);
    if (response) {
      const isLiked = response.liked;
      if (isLiked) {
        setLikesCount((previousLikesCount) => previousLikesCount + 1);
        toast.success("Post liked!");
      } else {
        setLikesCount((previousLikesCount) => previousLikesCount - 1);
        toast.success("Post like removed :(");
      }
    }
  } catch (error) {
    console.error(error);
    toast.error("Failed to like or remove like from post. Please try again.");
  }
};

// ─── 6. Helpers ───────────────────────────────────────────────────────────────
// Imperative state-mutation functions. Not event responses — these are commands
// called by handlers above or passed down to child components as props.
// Naming convention: verb + Noun — e.g. addCommentToPost, removeCommentFromPost.
// No try/catch here. No toasts. No side-effects. Pure state transitions only.

const addCommentToPost = (comment) => {
  setPostComments((previousCommentsState) => [...previousCommentsState, comment]);
};

const removeCommentFromPost = (commentId) => {
  setPostComments((previousCommentsState) =>
    previousCommentsState.filter((comment) => comment.id !== commentId)
  );
};

const addShowMoreCommentsToPost = (newComments) => {
  setPostComments(newComments);
};

// ─── 7. Return ────────────────────────────────────────────────────────────────
// One blank line before the return. JSX should be as flat as the design allows.
// No inline logic that needs a comment to understand — derive it in section 3.
// No anonymous functions in JSX — all handlers and helpers are named above.

return (
  <div className="post">
    ...
  </div>
);
```

---

## Naming reference

| Thing | Convention | Example |
|---|---|---|
| Event handler | `onVerb + Noun + Context` | `onClickLikePost`, `onSubmitLoginForm`, `onChangeSearchInput` |
| State helper / child prop | `verb + Noun` | `addCommentToPost`, `removeCommentFromPost`, `resetFormFields` |
| State variable | the thing it holds | `likesCount`, `postComments`, `isMenuOpen` |
| setState callback arg | `previous + StateName` | `previousLikesCount`, `previousCommentsState` |
| Boolean | reads as a question | `isLiked`, `hasComments`, `isPostOwner`, `canDelete` |
| Async response | `response` (always) | `const response = await likePost(payload)` |
| Extracted value from response | name what it means | `const isLiked = response.liked` |
| Payload / request body | `nounPayload` | `likePayload`, `commentPayload` |

---

## Before / after examples

### Variable names

```tsx
// Bad
const res = await fetch(url);
const data = await res.json();
const filtered = data.filter(x => x.active);
const [val, setVal] = useState(0);

// Good
const response = await fetch(userProfileUrl);
const userProfiles = await response.json();
const activeProfiles = userProfiles.filter((profile) => profile.isActive);
const [likesCount, setLikesCount] = useState(0);
```

### setState callback argument

```tsx
// Bad — "prev" tells you nothing about what the state is
setLikesCount((prev) => prev + 1);
setPostComments((prev) => [...prev, comment]);

// Good — the argument name matches the state variable name
setLikesCount((previousLikesCount) => previousLikesCount + 1);
setPostComments((previousCommentsState) => [...previousCommentsState, comment]);
```

### Handler vs helper distinction

```tsx
// Bad — a handler that does no error handling, and a "helper" that fires a toast
const likePost = async () => {
  await likePostApi(id); // no try/catch, no feedback
};

const updateComments = (comment) => {
  setPostComments([...postComments, comment]);
  toast.success("Comment added!"); // toast does not belong in a helper
};

// Good — handler owns the side-effect and feedback, helper is a pure state transition
const onClickLikePost = async () => {
  try {
    const response = await likePost(id);
    toast.success("Post liked!");
  } catch (error) {
    toast.error("Failed to like post. Please try again.");
  }
};

const addCommentToPost = (comment) => {
  setPostComments((previousCommentsState) => [...previousCommentsState, comment]);
};
```

### Whitespace grouping

```tsx
// Bad — no visual separation, everything runs together
const [isOpen, setIsOpen] = useState(false);
const title = props.title;
useEffect(() => { document.title = title; }, [title]);
const onClickOpen = () => setIsOpen(true);
const filteredItems = items.filter(i => i.active);

// Good — each group is visually distinct, reading order matches mental model
const { title, items } = props;

const [isOpen, setIsOpen] = useState(false);

const filteredItems = items.filter((item) => item.isActive);

useEffect(() => {
  document.title = title;
}, [title]);

const onClickOpen = () => setIsOpen(true);
```

---

## Readability pass checklist

Run through this after every component generation before marking the task done:

- [ ] Props are destructured at the top in a single block
- [ ] All state and context declarations are grouped together
- [ ] Derived values are named and computed before the return — none inside JSX
- [ ] Effects follow derived values
- [ ] Handlers are named `onVerb + Noun` and own their own try/catch and toasts
- [ ] Helpers are named `verb + Noun`, contain no toasts, no try/catch, no side-effects
- [ ] setState callbacks name the previous state argument (`previousXxx`)
- [ ] Booleans read as questions (`isX`, `hasX`, `canX`)
- [ ] One blank line between sections, no double blank lines
- [ ] No anonymous functions passed directly in JSX — all are named above
- [ ] No name requires reading surrounding code to understand
