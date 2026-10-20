# @ladamczyk/qoq-utils — Agent Context

Shared utility library used internally across all `@ladamczyk/qoq-*` packages. Can also be used directly in consumer projects.

## Exports

### `objectMergeRight(first, ...args)` — deprecated

**Deprecated: to reduce unnecessary complexity this will be removed in next major version.** No
consumer left in this monorepo.

Deep-merges objects with right-side precedence. Setting a key to `undefined` in a right-side object removes that key from the result. Does not mutate inputs — uses `structuredClone` where possible.

```ts
import { objectMergeRight } from '@ladamczyk/qoq-utils';

const result = objectMergeRight(base, override, furtherOverride);
```

### `executeCommand(command, args?, stdio?, captureOutput?)`

Promisified `child_process.spawn`. Returns `EExitCode` (0/1/2) by default, or the captured stdout string when `captureOutput` is `true`.

```ts
import { executeCommand, EExitCode } from '@ladamczyk/qoq-utils';

const code = await executeCommand('eslint', ['--fix', 'src']);
const output = await executeCommand('npm', ['outdated', '--json'], 'pipe', true);
```

### Package helpers

```ts
import { getPackageInfo, isPackageInstalled, getPackageJson } from '@ladamczyk/qoq-utils';

isPackageInstalled('typescript'); // boolean
getPackageInfo('typescript'); // { name, version, rootPath, packageJsonPath, packageJson }
getPackageJson(); // PackageJson | null — reads cwd package.json
getPackageJson('/some/path'); // reads from specific path
```

`getPackageInfo` throws if the package is not installed.

### Path helpers

```ts
import { getRelativePath, resolveCwdPath, resolveCwdRelativePath } from '@ladamczyk/qoq-utils';

resolveCwdPath('/src/index.ts'); // absolute: process.cwd() + /src/index.ts
getRelativePath('/abs/path/to/file'); // strips process.cwd(), returns ./relative/path
resolveCwdRelativePath('/src'); // combines both: relative path resolved from cwd
```
