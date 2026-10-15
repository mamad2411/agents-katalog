---
name: angular-jest
description: "ALWAYS use when testing Angular applications with Jest, configuring Jest, or migrating from Jasmine/Karma to Jest."
metadata:
  version: 21.0.0
  generated_by: oguzhancart
  generated_at: 2026-02-19
---

# Angular + Jest

**Version:** Jest 29.x (2025)
**Tags:** Jest, Testing, Unit Tests

**References:** [Jest](https://jestjs.io/) • [jest-preset-angular](https://github.com/thymikee/jest-preset-angular)

## Best Practices

- Install Jest

```bash
npm install --save-dev jest @types/jest jest-preset-angular
```

- Configure Jest

```js
// jest.config.js
module.exports = {
  preset: 'jest-preset-angular',
  setupFilesAfterEnv: ['<rootDir>/setup-jest.ts'],
  testPathIgnorePatterns: ['<rootDir>/node_modules/'],
};
```

- Write test

```ts
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MyComponent } from './my.component';

describe('MyComponent', () => {
  let component: MyComponent;
  let fixture: ComponentFixture<MyComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MyComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(MyComponent);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
```
