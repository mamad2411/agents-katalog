---
name: angular-schematics
description: "ALWAYS use when working with Angular Schematics, custom generators, code generation, or building CLI tools in Angular."
metadata:
  version: 21.0.0
  generated_by: oguzhancart
  generated_at: 2026-02-19
---

# Angular Schematics

**Version:** Angular 21 (2025)
**Tags:** Schematics, Generators, CLI, Code Generation

**References:** [Schematics Guide](https://angular.io/guide/schematics) • [@schematics/angular](https://github.com/angular/angular/tree/main/packages/schematics/angular)

## Best Practices

- Create schematic

```bash
npm install -g @angular-devkit/schematics-cli
schematics schematics .:my-schematic
```

- Create rule

```ts
import { Rule, SchematicContext, Tree } from '@angular-devkit/schematics';

export function myScheme(options: any): Rule {
  return (tree: Tree, context: SchematicContext) => {
    tree.create(options.path + '/file.ts', 'content');
    return tree;
  };
}
```

- Use templates

```ts
import { apply, url, template } from '@angular-devkit/schematics';

export function myScheme(options: any): Rule {
  const templateSource = apply(url('./files'), [
    template({ ...options }),
    move(options.path)
  ]);
  return chain([mergeWith(templateSource)]);
}
```
