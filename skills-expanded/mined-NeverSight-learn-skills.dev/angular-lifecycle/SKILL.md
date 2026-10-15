---
name: angular-lifecycle
description: "ALWAYS use when working with Angular Lifecycle Hooks, ngOnInit, ngOnChanges, ngAfterViewInit, or component lifecycle in Angular."
metadata:
  version: 21.0.0
  generated_by: oguzhancart
  generated_at: 2026-02-19
---

# Angular Lifecycle Hooks

**Version:** Angular 21 (2025)
**Tags:** Lifecycle, Hooks, ngOnInit, ngOnChanges

**References:** [Lifecycle Hooks](https://angular.io/guide/lifecycle-hooks) • [API](https://angular.io/api/core)

## Best Practices

- Use OnInit for initialization

```ts
import { OnInit } from '@angular/core';

@Component({})
export class MyComponent implements OnInit {
  ngOnInit() {
    // Initialize data, call services
    this.loadData();
  }
}
```

- Use OnDestroy for cleanup

```ts
import { OnDestroy } from '@angular/core';

@Component({})
export class MyComponent implements OnDestroy {
  private destroy$ = new Subject<void>();
  
  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

- Use OnChanges for input changes

```ts
import { OnChanges, SimpleChanges } from '@angular/core';

@Component({})
export class MyComponent implements OnChanges {
  @Input() data: any;
  
  ngOnChanges(changes: SimpleChanges) {
    if (changes['data']) {
      console.log('Data changed:', this.data);
    }
  }
}
```

- Use AfterViewInit for DOM manipulation

```ts
import { AfterViewInit, ViewChild, ElementRef } from '@angular/core';

@Component({})
export class MyComponent implements AfterViewInit {
  @ViewChild('el') el!: ElementRef;
  
  ngAfterViewInit() {
    this.el.nativeElement.focus();
  }
}
```

- Use AfterContentInit for projected content

```ts
import { AfterContentInit, ContentChild } from '@angular/core';

@Component({})
export class MyComponent implements AfterContentInit {
  @ContentChild('header') header!: ElementRef;
  
  ngAfterContentInit() {
    // Access projected content
  }
}
```

- Use DoCheck for custom change detection

```ts
import { DoCheck } from '@angular/core';

@Component({})
export class MyComponent implements DoCheck {
  ngDoCheck() {
    // Custom change detection
  }
}
```

- Use OnPush with lifecycle

```ts
@Component({
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class MyComponent {
  @Input() data: any;
  
  ngOnChanges(changes: SimpleChanges) {
    // OnPush needs explicit change detection trigger
  }
}
```

- Use constructor vs ngOnInit

```ts
// Constructor - for dependency injection only
constructor(private service: MyService) {}

// ngOnInit - for initialization logic
ngOnInit() {
  this.data = this.service.getData();
}
```
