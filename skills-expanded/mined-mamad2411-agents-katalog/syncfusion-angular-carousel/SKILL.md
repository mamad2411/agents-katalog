---
name: syncfusion-angular-carousel
description: Learn how to implement the Syncfusion Angular Carousel component for displaying slides with images and content. This comprehensive skill includes complete API documentation with all 30 properties, 5 methods, 2 events, and working code examples. Use when creating image galleries, product showcases, featured content sliders, news rotators, or implementing carousel navigation with animations.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Navigation Components"
---

# Implementing Syncfusion Angular Carousel Component

## When to Use This Skill

Use the Syncfusion Angular Carousel component when you need to:

- **Display multiple items sequentially** – Show images, products, or content in slide show format
- **Create image galleries** – Build responsive photo galleries with automatic or manual navigation
- **Feature rotating content** – Display featured articles, product highlights, or promotional banners
- **Implement scroll-like navigation** – Provide next/previous controls for content browsing
- **Add animations and transitions** – Create visually appealing slide effects with fade or slide animations
- **Support touch interactions** – Enable swipe gestures for mobile and touch devices
- **Display progress indicators** – Show users their position within carousel (dots, fractions, progress bars)
- **Handle slide change events** – Execute custom logic when slides transition

## Component Overview

The Syncfusion Angular Carousel component allows users to display images with content, links, and other media in a slide show format. It provides:

- **Multiple indicator types** – Default dots, dynamic markers, fractions, progress bars
- **Built-in animations** – None, Slide, Fade, and custom animation support
- **Navigation controls** – Previous/next buttons with visibility options (Visible, Hidden, VisibleOnHover)
- **Touch support** – Swipe gestures for mobile and desktop navigation
- **Auto-play functionality** – Automatic slide transitions with configurable intervals
- **Keyboard accessibility** – Arrow key navigation and WAI-ARIA compliance
- **Template support** – Custom item rendering, button templates, indicator customization
- **Event handling** – Pre/post slide transition events (slideChanging, slideChanged) for custom logic
- **Persistence** – Save/restore carousel state across page reloads
- **RTL support** – Right-to-left layout for Arabic, Hebrew, and other RTL languages

---

## Quick Start Example

Basic carousel with automatic slide transitions:

```typescript
import { Component } from "@angular/core";
import { CarouselModule } from "@syncfusion/ej2-angular-navigations";

@Component({
  selector: "app-carousel",
  standalone: true,
  imports: [CarouselModule],
  template: `
    <div class="carousel-container">
      <ejs-carousel [autoPlay]="true" [animationEffect]="'Slide'">
        <e-carousel-items>
          <e-carousel-item>
            <ng-template #template>
              <figure class="img-container">
                <img src="https://ej2.syncfusion.com/products/images/carousel/cardinal.png" alt="Slide 1" />
                <figcaption>Cardinal</figcaption>
              </figure>
            </ng-template>
          </e-carousel-item>
          <e-carousel-item>
            <ng-template #template>
              <figure class="img-container">
                <img src="https://ej2.syncfusion.com/products/images/carousel/hunei.png" alt="Slide 2" />
                <figcaption>Kingfisher</figcaption>
              </figure>
            </ng-template>
          </e-carousel-item>
          <e-carousel-item>
            <ng-template #template>
              <figure class="img-container">
                <img src="https://ej2.syncfusion.com/products/images/carousel/costa-rica.png" alt="Slide 3" />
                <figcaption>Keel-billed Toucan</figcaption>
              </figure>
            </ng-template>
          </e-carousel-item>
        </e-carousel-items>
      </ejs-carousel>
    </div>
  `,
  styles: [`
    .carousel-container {
      height: 400px;
      margin: 20px 0;
    }
  `]
})
export class CarouselComponent {}
```

**Key result:** Carousel automatically transitions between slides every 5000ms with slide animation.

---

## Component Properties

### 30 Total Properties Organized by Category

#### 1. Core Animation Properties

**animationEffect**
- **Type:** `'None' | 'Slide' | 'Fade' | 'Custom'`
- **Default:** `'Slide'`
- **Description:** Specifies animation effect when transitioning between slides.

```typescript
// Fade animation
<ejs-carousel [animationEffect]="'Fade'">
  <!-- Smooth fade in/out between slides -->
</ejs-carousel>

// No animation
<ejs-carousel [animationEffect]="'None'">
  <!-- Instant slide transition -->
</ejs-carousel>

// Custom CSS animation
<ejs-carousel [animationEffect]="'Custom'" [cssClass]="'custom-animation'">
  <!-- Define custom animation in CSS -->
</ejs-carousel>
```

#### 2. Auto-Play Properties

**autoPlay**
- **Type:** `boolean`
- **Default:** `true`
- **Description:** Enables automatic sliding through carousel items at intervals.

```typescript
<ejs-carousel [autoPlay]="true" [interval]="3000">
  <!-- Auto transitions every 3 seconds -->
</ejs-carousel>
```

**interval**
- **Type:** `number`
- **Default:** `5000` (milliseconds)
- **Description:** Time between automatic slide transitions (milliseconds). Only applies when autoPlay is true.

```typescript
<ejs-carousel [autoPlay]="true" [interval]="2000">
  <!-- 2 second interval between slides -->
</ejs-carousel>
```

**pauseOnHover**
- **Type:** `boolean`
- **Default:** `true`
- **Description:** Pauses auto-play when mouse hovers over carousel.

```typescript
<ejs-carousel [autoPlay]="true" [pauseOnHover]="false">
  <!-- Continue auto-play even on hover -->
</ejs-carousel>
```

#### 3. Navigation Properties

**buttonsVisibility**
- **Type:** `'Visible' | 'Hidden' | 'VisibleOnHover'`
- **Default:** `'Visible'`
- **Description:** Controls visibility of previous/next navigation buttons.

```typescript
// Always visible
<ejs-carousel [buttonsVisibility]="'Visible'">
  <!-- Buttons always shown -->
</ejs-carousel>

// Only on hover
<ejs-carousel [buttonsVisibility]="'VisibleOnHover'">
  <!-- Buttons appear on mouse hover -->
</ejs-carousel>

// Never visible
<ejs-carousel [buttonsVisibility]="'Hidden'">
  <!-- Use indicators or swipe instead -->
</ejs-carousel>
```

**previousButtonTemplate**
- **Type:** `string | object`
- **Default:** `null`
- **Description:** Custom template for previous navigation button.

```typescript
<ejs-carousel [previousButtonTemplate]="'#prevBtnTemplate'">
  <ng-template #prevBtnTemplate>
    <button class="custom-prev"><i class="icon-left"></i> Back</button>
  </ng-template>
  <e-carousel-items><!-- Items --></e-carousel-items>
</ejs-carousel>
```

**nextButtonTemplate**
- **Type:** `string | object`
- **Default:** `null`
- **Description:** Custom template for next navigation button.

```typescript
<ejs-carousel [nextButtonTemplate]="'#nextBtnTemplate'">
  <ng-template #nextBtnTemplate>
    <button class="custom-next">Next <i class="icon-right"></i></button>
  </ng-template>
  <e-carousel-items><!-- Items --></e-carousel-items>
</ejs-carousel>
```

**loop**
- **Type:** `boolean`
- **Default:** `true`
- **Description:** Enables infinite looping - cycles back to first slide after last.

```typescript
<ejs-carousel [loop]="true">
  <!-- Last slide -> First slide -->
</ejs-carousel>

<ejs-carousel [loop]="false">
  <!-- Last slide -> Navigation stops -->
</ejs-carousel>
```

**selectedIndex**
- **Type:** `number`
- **Default:** `0`
- **Description:** Initial slide index to display (0-based).

```typescript
<ejs-carousel [selectedIndex]="2">
  <!-- Start on third slide (index 2) -->
</ejs-carousel>
```

#### 4. Indicator Properties

**showIndicators**
- **Type:** `boolean`
- **Default:** `true`
- **Description:** Shows or hides position indicators.

```typescript
<ejs-carousel [showIndicators]="true">
  <!-- Indicators visible -->
</ejs-carousel>

<ejs-carousel [showIndicators]="false">
  <!-- No indicators shown -->
</ejs-carousel>
```

**indicatorsType**
- **Type:** `'Default' | 'Dynamic' | 'Fraction' | 'Progress'`
- **Default:** `'Default'`
- **Description:** Style of indicators displayed.

```typescript
// Dot indicators
<ejs-carousel [indicatorsType]="'Default'">
  <!-- Shows: ● ● ● ● ● -->
</ejs-carousel>

// Numeric format
<ejs-carousel [indicatorsType]="'Fraction'">
  <!-- Shows: 1 / 5 -->
</ejs-carousel>

// Progress bar
<ejs-carousel [indicatorsType]="'Progress'">
  <!-- Visual progress bar -->
</ejs-carousel>

// Animated
<ejs-carousel [indicatorsType]="'Dynamic'">
  <!-- Animated indicator effect -->
</ejs-carousel>
```

**indicatorsTemplate**
- **Type:** `string | object`
- **Default:** `null`
- **Description:** Custom template for indicators (e.g., thumbnail previews).

```typescript
<ejs-carousel [indicatorsTemplate]="'#indicatorTemplate'" [showIndicators]="true">
  <ng-template #indicatorTemplate let-data let-index="index">
    <img [src]="items[index]?.thumbnail" class="thumb" />
  </ng-template>
  <e-carousel-items><!-- Items --></e-carousel-items>
</ejs-carousel>
```

**showPlayButton**
- **Type:** `boolean`
- **Default:** `true`
- **Description:** Shows or hides play button to resume auto-play.

```typescript
<ejs-carousel [autoPlay]="false" [showPlayButton]="true">
  <!-- Users can click play to resume auto-play -->
</ejs-carousel>

<ejs-carousel [showPlayButton]="false">
  <!-- No play button visible -->
</ejs-carousel>
```

**playButtonTemplate**
- **Type:** `string | object`
- **Default:** `null`
- **Description:** Custom template for play button.

```typescript
<ejs-carousel [playButtonTemplate]="'#playBtnTemplate'">
  <ng-template #playBtnTemplate>
    <button class="play-btn">▶ Resume</button>
  </ng-template>
  <e-carousel-items><!-- Items --></e-carousel-items>
</ejs-carousel>
```

#### 5. Data and Item Properties

**dataSource**
- **Type:** `any[]`
- **Default:** `null`
- **Description:** Array of data for dynamic carousel items (use with itemTemplate).

```typescript
// Component
export class CarouselComponent {
  public slides = [
    { id: 1, image: 'img1.jpg', title: 'Slide 1' },
    { id: 2, image: 'img2.jpg', title: 'Slide 2' },
    { id: 3, image: 'img3.jpg', title: 'Slide 3' }
  ];
}

// Template
<ejs-carousel [dataSource]="slides">
  <ng-template #itemTemplate let-item>
    <figure>
      <img [src]="item.image" [alt]="item.title" />
      <figcaption>{{item.title}}</figcaption>
    </figure>
  </ng-template>
</ejs-carousel>
```

**itemTemplate**
- **Type:** `string | object`
- **Default:** `null`
- **Description:** Template for rendering each carousel item from dataSource.

```typescript
<ejs-carousel [dataSource]="products">
  <ng-template #itemTemplate let-product>
    <div class="product-card">
      <img [src]="product.image" />
      <h3>{{product.name}}</h3>
      <p>${{product.price}}</p>
    </div>
  </ng-template>
</ejs-carousel>
```

**items**
- **Type:** `CarouselItem[]`
- **Default:** `[]`
- **Description:** Array of carousel items (use with e-carousel-item directive for static content).

```typescript
<ejs-carousel>
  <e-carousel-items>
    <e-carousel-item>
      <ng-template #template><img src="image1.jpg" /></ng-template>
    </e-carousel-item>
    <e-carousel-item>
      <ng-template #template><img src="image2.jpg" /></ng-template>
    </e-carousel-item>
  </e-carousel-items>
</ejs-carousel>
```

**cssClass**
- **Type:** `string`
- **Default:** `''`
- **Description:** CSS class(es) for carousel container styling.

```typescript
<ejs-carousel [cssClass]="'dark-theme full-width'">
  <!-- Apply custom styles via CSS classes -->
</ejs-carousel>
```

#### 6. Interaction Properties

**enableTouchSwipe**
- **Type:** `boolean`
- **Default:** `true`
- **Description:** Enables swiping on touch devices to navigate slides.

```typescript
<ejs-carousel [enableTouchSwipe]="true">
  <!-- Touch swipe enabled -->
</ejs-carousel>

<ejs-carousel [enableTouchSwipe]="false">
  <!-- Touch swipe disabled -->
</ejs-carousel>
```

**swipeMode**
- **Type:** `'Touch' | 'Mouse' | 'Touch|Mouse'`
- **Default:** `'Touch|Mouse'`
- **Description:** Which interaction types enable swiping.

```typescript
// Both touch and mouse
<ejs-carousel [swipeMode]="'Touch|Mouse'" [enableTouchSwipe]="true">
  <!-- Both interactions work -->
</ejs-carousel>

// Touch only
<ejs-carousel [swipeMode]="'Touch'" [enableTouchSwipe]="true">
  <!-- Only touch gestures work -->
</ejs-carousel>

// Mouse only
<ejs-carousel [swipeMode]="'Mouse'" [enableTouchSwipe]="true">
  <!-- Only mouse drag works -->
</ejs-carousel>
```

**allowKeyboardInteraction**
- **Type:** `boolean`
- **Default:** `true`
- **Description:** Allows arrow keys to navigate carousel.

```typescript
<ejs-carousel [allowKeyboardInteraction]="true">
  <!-- Arrow keys navigate slides -->
</ejs-carousel>

<ejs-carousel [allowKeyboardInteraction]="false">
  <!-- Arrow keys disabled -->
</ejs-carousel>
```

#### 7. Dimension Properties

**height**
- **Type:** `string | number`
- **Default:** `'100%'`
- **Description:** Carousel container height (px, %, em, etc.).

```typescript
// Fixed height
<ejs-carousel [height]="400">
  <!-- 400px height -->
</ejs-carousel>

// Percentage
<ejs-carousel [height]="'100%'">
  <!-- Full parent height -->
</ejs-carousel>
```

**width**
- **Type:** `string | number`
- **Default:** `'100%'`
- **Description:** Carousel container width (px, %, em, etc.).

```typescript
// Fixed width
<ejs-carousel [width]="800">
  <!-- 800px width -->
</ejs-carousel>

// Full width
<ejs-carousel [width]="'100%'">
  <!-- Full parent width -->
</ejs-carousel>
```

**partialVisible**
- **Type:** `boolean`
- **Default:** `false`
- **Description:** Shows partial slides on sides for context.

```typescript
<ejs-carousel [partialVisible]="true">
  <!-- Shows portion of adjacent slides -->
</ejs-carousel>

<ejs-carousel [partialVisible]="false">
  <!-- Only current slide fully visible -->
</ejs-carousel>
```

#### 8. Localization and Persistence

**locale**
- **Type:** `string`
- **Default:** `''` (uses browser locale)
- **Description:** Locale/language for carousel (affects aria-labels, accessibility text).

```typescript
<ejs-carousel [locale]="'de-DE'">
  <!-- German localization -->
</ejs-carousel>

<ejs-carousel [locale]="'fr-FR'">
  <!-- French localization -->
</ejs-carousel>
```

**enablePersistence**
- **Type:** `boolean`
- **Default:** `false`
- **Description:** Saves carousel state to localStorage (restores on page reload).

```typescript
<ejs-carousel [enablePersistence]="true">
  <!-- Current slide position saved and restored -->
</ejs-carousel>
```

#### 9. Accessibility Properties

**enableRtl**
- **Type:** `boolean`
- **Default:** `false`
- **Description:** Enables right-to-left layout for RTL languages.

```typescript
<ejs-carousel [enableRtl]="true">
  <!-- RTL layout for Arabic, Hebrew, etc. -->
</ejs-carousel>
```

**htmlAttributes**
- **Type:** `Record<string, any>`
- **Default:** `null`
- **Description:** Additional HTML attributes for carousel root element.

```typescript
<ejs-carousel [htmlAttributes]="{ 'data-type': 'hero', 'aria-label': 'Hero Carousel' }">
  <!-- Custom attributes applied -->
</ejs-carousel>
```

---

## Component Methods

### 5 Total Methods

#### 1. next()
- **Signature:** `next(): void`
- **Description:** Navigate to next slide programmatically.

```typescript
import { Component, ViewChild } from "@angular/core";
import { CarouselComponent } from "@syncfusion/ej2-angular-navigations";

@Component({
  selector: "app-carousel-nav",
  template: `
    <button (click)="goNext()">Next</button>
    <ejs-carousel #carousel>
      <e-carousel-items>
        <e-carousel-item><ng-template #template><img src="img1.jpg" /></ng-template></e-carousel-item>
        <e-carousel-item><ng-template #template><img src="img2.jpg" /></ng-template></e-carousel-item>
      </e-carousel-items>
    </ejs-carousel>
  `
})
export class CarouselNavComponent {
  @ViewChild("carousel") carousel!: CarouselComponent;

  goNext() {
    this.carousel.next();
  }
}
```

#### 2. prev()
- **Signature:** `prev(): void`
- **Description:** Navigate to previous slide programmatically.

```typescript
export class CarouselNavComponent {
  @ViewChild("carousel") carousel!: CarouselComponent;

  goPrev() {
    this.carousel.prev();
  }
}
```

#### 3. play()
- **Signature:** `play(): void`
- **Description:** Resume automatic slide transitions.

```typescript
import { Component, ViewChild } from "@angular/core";
import { CarouselComponent } from "@syncfusion/ej2-angular-navigations";

@Component({
  selector: "app-carousel-controls",
  template: `
    <button (click)="playSlides()">Play</button>
    <button (click)="pauseSlides()">Pause</button>
    <ejs-carousel #carousel [autoPlay]="false">
      <e-carousel-items>
        <e-carousel-item><ng-template #template><img src="img1.jpg" /></ng-template></e-carousel-item>
        <e-carousel-item><ng-template #template><img src="img2.jpg" /></ng-template></e-carousel-item>
      </e-carousel-items>
    </ejs-carousel>
  `
})
export class CarouselControlsComponent {
  @ViewChild("carousel") carousel!: CarouselComponent;

  playSlides() {
    this.carousel.play();
  }

  pauseSlides() {
    this.carousel.pause();
  }
}
```

#### 4. pause()
- **Signature:** `pause(): void`
- **Description:** Pause automatic slide transitions.

```typescript
export class CarouselControlsComponent {
  @ViewChild("carousel") carousel!: CarouselComponent;

  pauseSlides() {
    this.carousel.pause();
  }
}
```

#### 5. destroy()
- **Signature:** `destroy(): void`
- **Description:** Destroy carousel component and release resources. Call before component removal.

```typescript
import { Component, ViewChild, OnDestroy } from "@angular/core";
import { CarouselComponent } from "@syncfusion/ej2-angular-navigations";

@Component({
  selector: "app-carousel-cleanup",
  template: `
    <ejs-carousel #carousel>
      <e-carousel-items>
        <e-carousel-item><ng-template #template><img src="img1.jpg" /></ng-template></e-carousel-item>
      </e-carousel-items>
    </ejs-carousel>
  `
})
export class CarouselCleanupComponent implements OnDestroy {
  @ViewChild("carousel") carousel!: CarouselComponent;

  ngOnDestroy() {
    // Cleanup when component destroyed
    this.carousel.destroy();
  }
}
```

---

## Component Events

### 2 Total Events

#### 1. slideChanging
- **Event Args:** `SlideChangingEventArgs`
- **Description:** Triggered before slide transition (can be prevented).
- **Key Use:** Validate or cancel slide changes

**Event Arguments:**
- `cancel: boolean` – Set true to prevent transition
- `currentIndex: number` – Current slide index
- `currentSlide: HTMLElement` – Current slide DOM element
- `nextIndex: number` – Next slide index to display
- `nextSlide: HTMLElement` – Next slide DOM element
- `isSwiped: boolean` – Whether triggered by swipe
- `slideDirection: 'Next' | 'Previous'` – Direction of change
- `name: string` – Event name ('slideChanging')

```typescript
import { Component, ViewChild } from "@angular/core";
import { CarouselComponent, SlideChangingEventArgs } from "@syncfusion/ej2-angular-navigations";

@Component({
  selector: "app-carousel-event",
  template: `
    <div class="status">Cannot navigate to slide 2</div>
    <ejs-carousel #carousel (slideChanging)="onSlideChanging($event)">
      <e-carousel-items>
        <e-carousel-item><ng-template #template><img src="img1.jpg" /><p>Slide 1</p></ng-template></e-carousel-item>
        <e-carousel-item><ng-template #template><img src="img2.jpg" /><p>Slide 2 - BLOCKED</p></ng-template></e-carousel-item>
        <e-carousel-item><ng-template #template><img src="img3.jpg" /><p>Slide 3</p></ng-template></e-carousel-item>
      </e-carousel-items>
    </ejs-carousel>
  `
})
export class CarouselEventComponent {
  onSlideChanging(args: SlideChangingEventArgs) {
    console.log(`Transitioning from ${args.currentIndex} to ${args.nextIndex}`);
    
    // Prevent navigating to slide 2
    if (args.nextIndex === 1) {
      args.cancel = true;
      alert("Slide 2 is blocked");
    }
  }
}
```

#### 2. slideChanged
- **Event Args:** `SlideChangedEventArgs`
- **Description:** Triggered after slide transition completes.
- **Key Use:** Track slide changes, update UI, log analytics

**Event Arguments:**
- `currentIndex: number` – Current slide index
- `currentSlide: HTMLElement` – Current slide DOM element
- `previousIndex: number` – Previous slide index
- `previousSlide: HTMLElement` – Previous slide DOM element
- `isSwiped: boolean` – Whether triggered by swipe
- `slideDirection: 'Next' | 'Previous'` – Direction of change
- `name: string` – Event name ('slideChanged')

```typescript
import { Component, ViewChild } from "@angular/core";
import { CarouselComponent, SlideChangedEventArgs } from "@syncfusion/ej2-angular-navigations";

@Component({
  selector: "app-carousel-tracking",
  template: `
    <div class="slide-counter">Slide {{currentSlide}} of {{totalSlides}}</div>
    <ejs-carousel #carousel (slideChanged)="onSlideChanged($event)">
      <e-carousel-items>
        <e-carousel-item><ng-template #template><img src="img1.jpg" /></ng-template></e-carousel-item>
        <e-carousel-item><ng-template #template><img src="img2.jpg" /></ng-template></e-carousel-item>
        <e-carousel-item><ng-template #template><img src="img3.jpg" /></ng-template></e-carousel-item>
      </e-carousel-items>
    </ejs-carousel>
  `
})
export class CarouselTrackingComponent {
  currentSlide = 1;
  totalSlides = 3;

  onSlideChanged(args: SlideChangedEventArgs) {
    this.currentSlide = args.currentIndex + 1;
    console.log(`Now on slide ${args.currentIndex}`);
    console.log(`Direction: ${args.slideDirection}`);
    console.log(`Swiped: ${args.isSwiped}`);
  }
}
```

---

## Default Values Reference

Complete table of default values for all 30 properties:

| Property | Default | Type |
|----------|---------|------|
| allowKeyboardInteraction | true | boolean |
| animationEffect | 'Slide' | string |
| autoPlay | true | boolean |
| buttonsVisibility | 'Visible' | string |
| cssClass | '' | string |
| dataSource | null | any[] |
| enablePersistence | false | boolean |
| enableRtl | false | boolean |
| enableTouchSwipe | true | boolean |
| height | '100%' | string/number |
| htmlAttributes | null | Record |
| indicatorsTemplate | null | string/object |
| indicatorsType | 'Default' | string |
| interval | 5000 | number (ms) |
| itemTemplate | null | string/object |
| items | [] | CarouselItem[] |
| locale | '' | string |
| loop | true | boolean |
| nextButtonTemplate | null | string/object |
| partialVisible | false | boolean |
| pauseOnHover | true | boolean |
| playButtonTemplate | null | string/object |
| previousButtonTemplate | null | string/object |
| selectedIndex | 0 | number |
| showIndicators | true | boolean |
| showPlayButton | true | boolean |
| swipeMode | 'Touch\|Mouse' | string |
| width | '100%' | string/number |

---

## Common Patterns and Use Cases

### Pattern 1: Data-Bound Carousel with Dynamic Content

**When to use:** Loading carousel items from an API or dynamic data source.

```typescript
import { Component, OnInit } from "@angular/core";
import { HttpClient } from "@angular/common/http";

@Component({
  selector: "app-data-carousel",
  template: `
    <ejs-carousel [dataSource]="items" [selectedIndex]="0">
      <ng-template #itemTemplate let-item>
        <figure class="img-container">
          <img [src]="item.image" [alt]="item.title" />
          <figcaption>{{item.title}}</figcaption>
        </figure>
      </ng-template>
    </ejs-carousel>
  `
})
export class DataCarouselComponent implements OnInit {
  items: any[] = [];

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.http.get<any>('/api/carousel-items')
      .subscribe(data => this.items = data);
  }
}
```

### Pattern 2: Manual Navigation with Buttons

**When to use:** Users control slide transitions with custom buttons instead of auto-play.

```typescript
import { Component, ViewChild } from "@angular/core";
import { CarouselComponent } from "@syncfusion/ej2-angular-navigations";

@Component({
  selector: "app-manual-nav",
  template: `
    <div class="carousel-controls">
      <button (click)="prevSlide()" class="control-btn">← Previous</button>
      <span class="slide-counter">{{currentSlide}} / {{totalSlides}}</span>
      <button (click)="nextSlide()" class="control-btn">Next →</button>
    </div>
    <ejs-carousel 
      #carousel 
      [autoPlay]="false" 
      [buttonsVisibility]="'Hidden'"
      (slideChanged)="onSlideChanged($event)"
    >
      <e-carousel-items>
        <e-carousel-item *ngFor="let item of items">
          <ng-template #template>
            <img [src]="item.image" />
          </ng-template>
        </e-carousel-item>
      </e-carousel-items>
    </ejs-carousel>
  `
})
export class ManualNavCarouselComponent {
  @ViewChild("carousel") carousel!: CarouselComponent;
  
  items = [
    { image: 'image1.jpg' },
    { image: 'image2.jpg' },
    { image: 'image3.jpg' }
  ];
  
  currentSlide = 1;
  totalSlides = this.items.length;

  prevSlide() { this.carousel.prev(); }
  nextSlide() { this.carousel.next(); }

  onSlideChanged(event: any) {
    this.currentSlide = event.currentIndex + 1;
  }
}
```

### Pattern 3: Event-Driven Carousel with Custom Handlers

**When to use:** Execute custom logic on slide transitions, track analytics, or prevent certain actions.

```typescript
import { Component, ViewChild } from "@angular/core";
import { CarouselComponent, SlideChangingEventArgs, SlideChangedEventArgs } from "@syncfusion/ej2-angular-navigations";

@Component({
  selector: "app-event-carousel",
  template: `
    <div class="carousel-stats">
      <p>Total Views: {{viewCount}}</p>
      <p>Current: {{lastViewedSlide}}</p>
    </div>
    <ejs-carousel 
      #carousel 
      (slideChanging)="onSlideChanging($event)"
      (slideChanged)="onSlideChanged($event)"
    >
      <e-carousel-items>
        <e-carousel-item *ngFor="let item of slides">
          <ng-template #template>
            <img [src]="item.image" />
            <h3>{{item.title}}</h3>
          </ng-template>
        </e-carousel-item>
      </e-carousel-items>
    </ejs-carousel>
  `
})
export class EventCarouselComponent {
  @ViewChild("carousel") carousel!: CarouselComponent;

  slides = [
    { title: 'Slide 1', image: 'image1.jpg' },
    { title: 'Slide 2', image: 'image2.jpg' },
    { title: 'Slide 3', image: 'image3.jpg' }
  ];

  viewCount = 0;
  lastViewedSlide = '';

  onSlideChanging(args: SlideChangingEventArgs) {
    // Example: Prevent returning to first slide
    if (args.previousIndex === 1 && args.nextIndex === 0) {
      console.log("Blocking return to first slide");
      // args.cancel = true; // Uncomment to prevent
    }
  }

  onSlideChanged(args: SlideChangedEventArgs) {
    this.viewCount++;
    this.lastViewedSlide = this.slides[args.currentIndex].title;
    
    // Log analytics
    console.log(`Viewed slide ${args.currentIndex} via ${args.slideDirection}`);
  }
}
```

---

## Implementation Guides

For detailed implementation on specific topics, see:

- **[Getting Started](references/getting-started.md)** – Installation, setup, CSS imports, basic configuration
- **[Item Population & Data](references/item-templates-and-content.md)** – dataSource, templates, data binding, navigation
- **[Navigation & Indicators](references/navigation-and-indicators.md)** – Button controls, indicator types, customization
- **[Animations & Transitions](references/animations-and-transitions.md)** – Animation effects, auto-play, event handling
- **[Styling & Appearance](references/styling-and-appearance.md)** – CSS customization, themes, WebP, responsive

---

## Next Steps

1. **Choose your data approach:** Use items binding for static content, dataSource for dynamic data
2. **Select navigation style:** Buttons, indicators, or both
3. **Decide on animations:** None, Slide (default), Fade, or custom CSS effects
4. **Configure auto-play:** Set interval and pause behavior
5. **Handle events:** Listen to slideChanging and slideChanged for custom logic
6. **Style your carousel:** Apply CSS classes and responsive design
7. **Test interactions:** Verify touch/keyboard navigation and event handling

See reference files for detailed implementation examples and best practices.
