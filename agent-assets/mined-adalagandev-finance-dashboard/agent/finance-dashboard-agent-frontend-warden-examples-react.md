# Frontend Rules — React/JSX Examples

**Framework basis:** React 18 + Vite, plain JavaScript (no TypeScript), function
components + Hooks only. Styling is one `styles.css` file driven by `:root` CSS
custom properties (BEM-ish class names). The rules in `frontend-warden.md` are
framework-agnostic; these examples are the React instantiation, showing this
repo's concrete stack and conventions (`api.js` seam, prop-drilling from
`App.jsx`, heavy teaching comments, stable `id`s).

**Repo touchstones:** `frontend/src/api.js` (the only fetch site),
`frontend/src/App.jsx` (owns all shared state), `components/StudentForm.jsx`
(controlled form), `components/Modal.jsx` (portal + Escape), `styles.css`
(`:root` tokens). Match their comment density.

## Rule 1 — `api.js` is the only backend seam
Violation:
```jsx
// inside StudentList.jsx — a component reaching for the network
function StudentList() {
  async function remove(id) {
    await fetch(`http://localhost:5000/api/students/${id}`, { method: "DELETE" });
  }
}
```
Correct:
```js
// api.js — add the function here, the ONE place that knows URLs/HTTP
export async function deleteStudent(id) {
  const response = await fetch(`${BASE_URL}/students/${id}`, { method: "DELETE" });
  if (!response.ok) {
    const data = await response.json();
    throw new Error(data.error || "Failed to delete student.");
  }
  return response.json();
}
// App.jsx calls deleteStudent() in a handler and passes it down as a prop.
```

## Rule 2 — State updates are immutable
Violation:
```jsx
function handleAddStudent(created) {
  students.push(created);   // mutation — React sees the same array ref, no re-render
  setStudents(students);
}
```
Correct:
```jsx
// build a NEW array; updater form reads the freshest previous value
setStudents((previous) => [created, ...previous]);
// swapping one record, immutably:
setStudents((previous) =>
  previous.map((s) => (s.id === updated.id ? updated : s))
);
```

## Rule 3 — The owner holds shared state; children are presentational
Violation:
```jsx
// StudentList.jsx keeps its own copy of the list and refetches it
function StudentList() {
  const [students, setStudents] = useState([]);
  useEffect(() => { getStudents().then(setStudents); }, []); // drifts from App's copy
}
```
Correct:
```jsx
// App.jsx owns it; StudentList just renders props + calls callbacks
<StudentList students={students} onEdit={setEditingStudent} />

function StudentList({ students, onEdit }) {   // dumb + presentational
  return students.map((s) => <StudentRow key={s.id} student={s} onEdit={onEdit} />);
}
```

## Rule 4 — Controlled inputs only
Violation:
```jsx
<input id="email" defaultValue={form.email} ref={emailRef} />   // DOM is the source of truth
// ...later: const value = emailRef.current.value;
```
Correct:
```jsx
<input
  id="email" name="email"
  value={form.email}          // value comes FROM state
  onChange={handleChange}     // every keystroke writes back
  required
/>
// reset by setting state back to the blank constant: setForm(EMPTY_FORM)
```

## Rule 5 — Hooks at the top level, complete dependency arrays
Violation:
```jsx
function Panel({ open }) {
  if (open) {
    const [count, setCount] = useState(0);   // hook inside a condition — illegal
  }
  useEffect(() => { load(id); }, []);        // reads `id` but omits it
}
```
Correct:
```jsx
function Panel({ open, id }) {
  const [count, setCount] = useState(0);     // top level, unconditional
  useEffect(() => { load(id); }, [id]);      // every read value is a dependency
  if (!open) return null;                    // branch AFTER the hooks
}
```

## Rule 6 — Effects synchronize with the outside world; derive the rest
Violation:
```jsx
const [students, setStudents] = useState([]);
const [count, setCount] = useState(0);
useEffect(() => { setCount(students.length); }, [students]); // derived state synced by effect
```
Correct:
```jsx
const [students, setStudents] = useState([]);
const count = students.length;               // derive during render — no effect, no drift
// useEffect is reserved for real outside-world work:
useEffect(() => { refreshStudents(); }, []); // data load on mount
```

## Rule 7 — Render from state, never imperative DOM
Violation:
```jsx
function showError(msg) {
  document.getElementById("status-message").innerHTML = msg;  // hand-editing the DOM
}
```
Correct:
```jsx
{message && <p className="message" id="status-message">{message}</p>}
// setMessage(error.message) triggers the re-render; React owns the DOM
```

## Rule 8 — Stable, descriptive `id` on every element
Violation:
```jsx
<tr>                                  {/* no id */}
  <td>{student.firstName}</td>
  <button onClick={() => onEdit(student)}>Edit</button>   {/* no id */}
</tr>
```
Correct:
```jsx
<tr id={`student-row-${student.id}`}>
  <td id={`student-firstName-${student.id}`}>{student.firstName}</td>
  <button id={`student-edit-btn-${student.id}`} onClick={() => onEdit(student)}>
    Edit
  </button>
</tr>
```

## Rule 9 — List items get stable, unique keys
Violation:
```jsx
{students.map((student, i) => <StudentRow key={i} student={student} />)}  // index key
```
Correct:
```jsx
{students.map((student) => <StudentRow key={student.id} student={student} />)}
```

## Rule 10 — Theme through CSS tokens
Violation:
```jsx
<button style={{ background: "#8c7cf0", color: "#fff" }}>Save</button>  // hardcoded color
```
Correct:
```jsx
<button className="btn btn--primary" id="edit-save-btn">Save</button>
/* styles.css — colors resolve from :root tokens */
.btn--primary { background: var(--accent); color: var(--text); }
```

## Rule 11 — Match the teaching-comment density
Violation:
```jsx
export default function WaitlistList({ waitlist }) {
  return waitlist.map((w) => <li key={w.email}>{w.name}</li>);   // zero explanation
}
```
Correct:
```jsx
// WaitlistList.jsx — a read-only, presentational list. It receives `waitlist`
// as a prop and renders it; it never fetches or mutates anything.
export default function WaitlistList({ waitlist }) {
  // .map() turns each data object into a <li>. `key` must be stable + unique so
  // React can match rows across re-renders — we use the email, not the index.
  return (
    <ul className="waitlist" id="waitlist-list">
      {waitlist.map((w) => (
        <li className="waitlist__row" id={`waitlist-row-${w.email}`} key={w.email}>
          {w.name}
        </li>
      ))}
    </ul>
  );
}
```

## Rule 12 — Overlays use portals, correctly
Violation:
```jsx
function Modal({ children }) {
  return <div className="modal__overlay">{children}</div>;  // no portal, no Esc, no stopPropagation
}
```
Correct:
```jsx
useEffect(() => {
  function onKey(e) { if (e.key === "Escape") onClose(); }
  document.addEventListener("keydown", onKey);
  return () => document.removeEventListener("keydown", onKey);  // cleanup on unmount
}, [onClose]);

return createPortal(
  <div className="modal__overlay" id="modal-overlay" onClick={onClose}>
    <div className="modal__dialog" role="dialog" aria-modal="true"
         onClick={(e) => e.stopPropagation()}>   {/* inner click must not close */}
      {children}
    </div>
  </div>,
  document.body
);
```

## Rule 13 — Uploads send `FormData` with NO `Content-Type`
Violation:
```js
const formData = new FormData();
formData.append("program", program);
await fetch(url, {
  method: "POST",
  headers: { "Content-Type": "multipart/form-data" },  // breaks the boundary
  body: formData,
});
```
Correct:
```js
const formData = new FormData();
formData.append("program", program);
for (const file of files) formData.append("forms", file);
// No headers: the browser sets Content-Type AND the multipart boundary itself.
const response = await fetch(`${BASE_URL}/students/${id}/program-change`, {
  method: "POST",
  body: formData,
});
```

## Rule 14 — Read the body once; surface the server's error
Violation:
```js
export async function createStudent(student) {
  const response = await fetch(`${BASE_URL}/students`, { method: "POST", /* ... */ });
  if (!response.ok) throw new Error("Failed.");   // discards the server's {"error": ...}
  return response.json();
}
```
Correct:
```js
export async function createStudent(student) {
  const response = await fetch(`${BASE_URL}/students`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(student),
  });
  const data = await response.json();               // read the body ONCE
  if (!response.ok) throw new Error(data.error || "Failed to create student.");
  return data;
}
// Component: try { await ... } catch (error) { setMessage(error.message); }
```

## Rule 15 — JSX must be valid JSX
Violation:
```jsx
<div class="form__row">                     {/* HTML attribute names */}
  <label for="email">Email</label>
</div>
<div>{firstEl}{secondEl}</div>              {/* extra wrapper div just to group */}
```
Correct:
```jsx
<div className="form__row" id="form-row-email">
  <label htmlFor="email" id="label-email">Email</label>
</div>
<>                                          {/* Fragment groups without a wrapper node */}
  {firstEl}
  {secondEl}
</>
```

## Rule 16 — Accessibility at the boundary
Violation:
```jsx
<input id="email" name="email" value={form.email} onChange={handleChange} />  {/* no label */}
<button onClick={onClose}>×</button>                                          {/* icon, no name */}
<button onClick={submit}>Save</button>                                        {/* no type */}
```
Correct:
```jsx
<label htmlFor="email" id="label-email">Email</label>
<input id="email" name="email" value={form.email} onChange={handleChange} required />

<button id="modal-close-btn" onClick={onClose} aria-label="Close">×</button>
<button type="button" id="edit-save-btn" className="btn btn--primary" onClick={submit}>
  Save
</button>
```
