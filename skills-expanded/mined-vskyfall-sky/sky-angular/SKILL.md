---
name: sky-angular
description: >-
  Modern Angular (17+): standalone bileşenler, sinyaller (signal, computed, effect, input/output
  sinyalleri), yeni kontrol akışı (@if, @for, @defer), bağımlılık enjeksiyonu (inject), servisler,
  HttpClient ve interceptor'lar, router (lazy loading, guard'lar, resolver'lar), reactive forms ve
  typed forms, RxJS ile sinyal birlikteliği, SSR ve hydration, zoneless, test ve performans.
  Angular projesinde kullan.
disable-model-invocation: true
---

# Sky · Angular

## Bileşen (standalone + sinyaller)

```ts
@Component({
  selector: "app-bookings",
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [BookingRowComponent],
  template: `
    @if (loading()) { <app-skeleton /> }
    @else {
      @for (b of filtered(); track b.id) { <app-booking-row [booking]="b" (cancel)="cancel(b.id)" /> }
      @empty { <p>Henüz randevu yok</p> }
    }
    @defer (on viewport) { <app-stats [orgId]="orgId()" /> } @placeholder { <div class="h-40"></div> }
  `,
})
export class BookingsComponent {
  orgId = input.required<string>();
  selected = output<string>();
  private api = inject(BookingApi);
  query = signal("");
  bookings = signal<Booking[]>([]);
  loading = signal(true);
  filtered = computed(() => this.bookings().filter((b) => b.clientName.includes(this.query())));
  constructor() {
    effect(() => { this.loading.set(true); this.api.list(this.orgId()).subscribe((r) => { this.bookings.set(r); this.loading.set(false); }); });
  }
  cancel(id: string) { this.api.cancel(id).subscribe(() => this.bookings.update((l) => l.filter((x) => x.id !== id))); }
}
```
- Yeni projede NgModule yok (standalone), `OnPush` varsayılan düşünce, sinyaller + `@if/@for` (track zorunlu).
- `resource()` / `httpResource()` (yeni sürümlerde) async veriyi sinyal olarak; RxJS gerektiğinde `toSignal`/`toObservable`.
- `@defer` ile görünüm bazlı tembel yükleme — bundle'ı küçültür.

## Servisler ve HTTP

`@Injectable({ providedIn: "root" })` servisler, `inject()` fonksiyonu; `provideHttpClient(withInterceptors([authInterceptor]))` — fonksiyonel interceptor ile token ve hata yönetimi.

## Router

`provideRouter(routes, withComponentInputBinding())` (route parametreleri input olarak), `loadComponent` ile lazy, fonksiyonel guard'lar (`canActivate: [() => inject(Auth).isLoggedIn() || inject(Router).parseUrl("/login")]`) — yetki asıl sunucuda.

## Formlar

Typed reactive forms (`FormBuilder.nonNullable.group({...})`), `Validators` + özel doğrulayıcılar, hata mesajları `sky-forms` kurallarına göre; signal forms (yeni API) sürüm desteğine göre.

## SSR ve performans

`@angular/ssr` + hydration (incremental hydration `@defer` ile), zoneless change detection (`provideZonelessChangeDetection()` — sürüme göre), `NgOptimizedImage` (`ngSrc`), bundle bütçeleri `angular.json`'da.

## Test ve araçlar

Angular CLI (`ng generate`, `ng update` ile sürüm yükseltme — bkz. `sky-upgrades`), Vitest/Jest veya Karma, Testing Library Angular, Playwright; ESLint `angular-eslint`.
