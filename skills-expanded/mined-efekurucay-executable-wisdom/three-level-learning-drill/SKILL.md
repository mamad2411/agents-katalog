---
name: three-level-learning-drill
description: Teach programming concepts by moving across three abstraction levels: high-level code or product behavior, runtime/intermediate representation, and low-level data/hardware effects. Use when asked to deeply understand code, frameworks, React, .NET, SQL, Vite, APIs, memory, performance, compiler/runtime behavior, or when the user says “anlamamı sağla”, “deep reasoning yap”, “neden böyle”, or “mantığını anlat”.
---

# Three-Level Learning Drill

## Purpose
Use this skill to help the user understand programming concepts by moving between abstraction levels instead of giving a flat explanation.

The goal is not to dump theory. The goal is to build the engineer’s ability to zoom in and out:

- What do I write?
- What does the runtime/framework/compiler actually do?
- What happens to data, memory, IO, or machine resources?

## Core philosophy

- Understanding comes from moving between levels.
- Do not stay only at the framework vocabulary level.
- Do not jump to hardware unless it clarifies the concept.
- Use tiny examples and traces.
- Prefer one concrete path over many abstract definitions.
- Teach the hidden layer under the tool.

## When to use this skill
Use this skill for requests like:

- “Bunu kısaca anlamamı sağla.”
- “Deep reasoning yap.”
- “Bu helper ne işe yarıyor?”
- “Bu .NET/React/Vite/MVC olayı ne?”
- “Bu SQL komutu ne yapar?”
- “Abstraction nedir?”
- “CSRF nedir?”
- “Bu kod runtime’da nasıl çalışıyor?”
- “Bunu yeni başlayan ama hızlı öğrenen biri gibi anlat.”

## The three levels

### Level 1 — Surface/API level
What the developer sees and writes:

- code syntax
- method/class/component/API name
- framework concept
- product behavior
- visible input/output

### Level 2 — Runtime/translation level
What the platform does with it:

- compiler/transpiler behavior
- MVC routing
- React render cycle
- HTTP request/response
- ORM query generation
- async state machine
- dependency injection
- middleware/filter pipeline
- SQL execution plan

### Level 3 — Data/resource level
What happens underneath:

- bytes/data shape
- object lifetime
- memory allocation
- cache/locality implications
- network round-trips
- database indexes/locks
- CPU work
- serialization/deserialization
- security boundary

Not every topic needs literal CPU details. Use the lowest useful level.

## Teaching process

### 1. Start with the shortest useful definition
Give one sentence that makes the concept usable immediately.

### 2. Build a concrete example
Use a tiny example from the user’s context when possible: C#, .NET MVC, React, TypeScript, SQL, auth, CMS, API routes, helpers, DTOs, query keys, etc.

### 3. Walk through the three levels
Explain:

- what the developer writes
- what the runtime/framework does
- what data/resource effect occurs

### 4. Show the “trap”
Every concept has a common misunderstanding. Name it.

Examples:

- Abstraction trap: assuming fewer visible lines means less total complexity.
- Big-O trap: ignoring memory locality and real data size.
- Helper trap: hiding behavior behind a nice name.
- Async trap: assuming async means faster CPU work.
- ORM trap: assuming a nice LINQ expression means a nice SQL query.
- React trap: assuming state change updates only what you visually changed.

### 5. Give one tiny drill
Give the user one small exercise or mental check that takes under five minutes.

## Output format

### Tek cümlelik anlam
One sentence.

### 3 seviye açıklama
| Seviye | Ne oluyor? |
|---|---|
| Yazdığın kod / API |  |
| Runtime / framework |  |
| Data / kaynak |  |

### Mini örnek
Use a compact code or flow example if useful.

### En sık yanlış anlama
Explain the trap.

### Pratik kontrol sorusu
Give one question the user can ask next time they see this concept.

### 5 dakikalık drill
Give a small action the user can do immediately.

## Style rules

- Turkish by default.
- Speak like a sharp mentor, not like documentation.
- Keep explanations compact but layered.
- Avoid long academic background unless the user asks.
- Use analogies only if they reveal the hidden layer.
- Prefer code/path traces over metaphors.

## Example

### Input
“PutVoid helper ne demek?”

### Output shape

### Tek cümlelik anlam
`putVoid`, PUT isteği atan ama response body beklemeyen küçük HTTP helper’dır.

### 3 seviye açıklama
| Seviye | Ne oluyor? |
|---|---|
| Yazdığın kod / API | `putVoid('/api/user/5', body)` çağırırsın; dönüş datası beklemezsin. |
| Runtime / framework | `fetch` PUT methoduyla çalışır, cookie/header ekler, status başarısızsa hata fırlatır. |
| Data / kaynak | JSON serialize edilir, network request gider, server body okumadan sadece status dönebilir. |

### En sık yanlış anlama
“Void” demek server hiçbir şey yapmıyor demek değildir; sadece client response body beklemiyor demektir.

### Pratik kontrol sorusu
Bu endpoint gerçekten body döndürmeyecek mi, yoksa dönen bilgiyi yanlışlıkla çöpe mi atıyorum?
