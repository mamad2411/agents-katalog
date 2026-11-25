---
title: Manifest and first skill
order: 1
issue: 45
github:
  state: closed
  pr: null
  merged_at: null
  synced_at: '2026-09-21T00:10:47.258Z'
---

# Manifest and first skill

Make the repository a plugin and prove it loads: the manifest that names it, one skill
carried across, and the test that will police the other seven when they arrive. Nothing here
is interesting except that it works — a manifest in the wrong directory produces a plugin
that silently contributes nothing, and the only way to find out is to load it.

`write-spec` is the witness because it is the smallest of the eight and because it names a
path from the repository it came from, which is the exact coupling every other skill also
has.

**Files**

- Create: `.claude-plugin/plugin.json`
- Create: `skills/write-spec/SKILL.md`
- Create: `tests/plugin.test.ts`
- Modify: `tsconfig.json` — include `hooks` and `tests`

**Interfaces**

- Consumes: nothing.
- Produces: the plugin namespace `ccgh`, so every skill answers as `/ccgh:<name>`; and `tests/plugin.test.ts`, which tasks 2 to 6 extend rather than replace.

- [ ] **Write the failing test**

`tests/plugin.test.ts`:

```ts
import { describe, expect, it } from "bun:test";
import { readdir, readFile } from "node:fs/promises";
import { join } from "node:path";

const root = new URL("..", import.meta.url).pathname;

const manifest = async (): Promise<Record<string, unknown>> =>
  JSON.parse(await readFile(join(root, ".claude-plugin/plugin.json"), "utf8"));

const skills = async (): Promise<string[]> => (await readdir(join(root, "skills"))).sort();

describe("the manifest", () => {
  it("names the plugin after the command, because the name prefixes every skill", async () => {
    expect((await manifest()).name).toBe("ccgh");
  });

  it("carries a description and a version", async () => {
    const parsed = await manifest();

    expect(typeof parsed.description).toBe("string");
    expect(parsed.version).toMatch(/^\d+\.\d+\.\d+$/);
  });
});

describe("every skill", () => {
  it("is a directory holding a SKILL.md", async () => {
    for (const name of await skills()) {
      const body = await readFile(join(root, "skills", name, "SKILL.md"), "utf8");

      expect(body.startsWith("---\n"), name).toBe(true);
    }
  });

  it("declares a name matching its directory, and a description", async () => {
    for (const name of await skills()) {
      const body = await readFile(join(root, "skills", name, "SKILL.md"), "utf8");

      expect(body, name).toContain(`name: ${name}`);
      expect(body.match(/^description: \S.*$/m), name).not.toBeNull();
    }
  });

  it("names no command and no path from the repository this came from", async () => {
    for (const name of await skills()) {
      const body = await readFile(join(root, "skills", name, "SKILL.md"), "utf8");

      expect(body, name).not.toContain("pnpm --filter");
      expect(body, name).not.toContain("src/content");
    }
  });
});
```

The last assertion is the one that matters. It fails for every skill still carrying its
origin, and it is what makes task 2 a mechanical job with a verdict rather than a reading
exercise.

- [ ] **Run it to verify it fails**

```bash
bun test tests/plugin.test.ts
```

- [ ] **Write the implementation**

`.claude-plugin/plugin.json`:

```json
{
  "name": "ccgh",
  "description": "A development lifecycle for a repository: specifications and tasks written as content, promoted through human gates, mirrored to GitHub issues.",
  "version": "0.1.0",
  "homepage": "https://github.com/Hova25/ccgh-bridge"
}
```

`skills/write-spec/SKILL.md` carries the origin's text with two changes: it names no path,
and it names `ccgh validate`. Where it said *write to
`<one repository's content directory>/<domain>/iterations/<…>/spec.md`*, it says to write to
the `spec.md` that `ccgh scaffold iteration` reported. The scaffold prints the file it wrote;
a skill that repeats the path is a second place for the convention to be wrong.

`tsconfig.json` gains `hooks` and `tests` in `include`, so `bun run typecheck` covers them
from here on.

- [ ] **Run the tests to verify they pass**

```bash
bun run verify
```

Then load the plugin and use it, which is the only way to know the manifest is in the right
place:

```bash
claude --plugin-dir .
```

In that session, `/ccgh:write-spec` answers and `/help` lists it under the `ccgh` namespace.
A skill that does not appear means the directory is inside `.claude-plugin/` rather than
beside it.

- [ ] **Commit**
