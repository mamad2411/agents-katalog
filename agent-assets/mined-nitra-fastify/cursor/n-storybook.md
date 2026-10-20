---
description: Канонічний Storybook для Vue-компонентних бібліотек — скафолд, vitest/Stryker, гігієна залежностей, рецепти мокання
version: '1.0'
globs: ["package.json", "**/*.vue", ".storybook/**"]
alwaysApply: false
---

# Канон Storybook для Vue-компонентних бібліотек — хвиля 1

Джерело рішення: `docs/adr/канон-storybook-для-vue-компонентних-бібліотек.md`. Storybook впроваджувався вручну двічі в різних nitra-репо в одній сесії — обидва рази з тими самими невидимими заздалегідь проблемами (конфлікт `@vitejs/plugin-vue`/`quasar()`, недоступні внутрішні Quasar-іконки без `iconSet`+`iconMapFn`, ручне мокання мережі) і одним реальним merge-конфліктом між двома паралельними ручними реалізаціями тієї самої фічі. Це правило робить канонічний скафолд стандартом, а не одноразовим рішенням кожного агента.

**Хвильовий rollout:** `alwaysApply: false` — правило не гейтить CI, доки не ввімкнене явно в `.n-rules.json` консюмер-репо (`rules: ["storybook"]`). Хвиля 1 (це правило) покриває детекцію скоупу, канонічний скафолд `.storybook/`, vitest/Stryker-конфіг (Кластер 5), гігієну сторонніх залежностей (Кластер 6), рецепти мокання (docs-only, Кластер 3) і `--adopt`-режим rollout-у для вже впроваджених вручну пакетів (Кластер 8); **LLM-генерація args для stories — хвиля 2**, свідомо відкладена (ADR: ризик одночасного org-wide CI-блоку на необкатаному generation pipeline, на відміну від production-proven doc-files).

Усі concern-и хвилі 1 (`scope`/`scaffold`/`vitest-config`/`hygiene`) мають `lint`-поверхню в `concern.json` і виконуються під `npx @7n/rules lint storybook` — `scope`/`scaffold`/`vitest-config` раніше декларували лише `check: true` без `lint`-блоку і тому мовчки не підхоплювались unified lint-рушієм (`run-detectors.mjs` виконує лише concern-и з явним `lint` чи `policy` блоком); виправлено разом із введенням `adopt`-режиму.

## Скоуп

Тільки Vue-компонентні бібліотеки — пакет із `vue` у `peerDependencies` (маркер `isVueComponentLibraryPkg`, той самий що й у `vue.mdc`, не дублюється) і не менше **3** `.vue`-файлів. Поріг відсікає пакети з одним-двома допоміжними компонентами, для яких повний Storybook-скафолд — зайві накладні витрати. Пакети без розпізнаваного `vite.config.{js,ts,mjs}` (нестандартний build) пропускаються мовчки — автоматичний скафолд спирається на `viteConfigPath` пакета.

Опційно (вимкнено за замовчуванням) — app-проєкти (`vue` у `dependencies`, не бібліотека, + `src/pages/`). Детекція реалізована в `scope/main.mjs`, але не викликається доки в `.n-rules.json` не задано прапорець хвилі 2 — рішення розширювати скоуп на app-проєкти залишається відкритим питанням ADR.

**Opt-out:** окремий пакет можна виключити зі скоупу через `.n-rules.json` → `storybook.optOut: string[]` (root dir пакета, той самий формат що й у виводі workspace-роутингу — `.` для кореня, `packages/ui` тощо). Виняток — намір, не помилка: якщо в `optOut` вказано неіснуючий workspace-пакет, `scope`-концерн репортує це як застаріле налаштування.

Логіка детекції (поріг, opt-out, нестандартний build, app-проєкти) — у `scope/main.mjs`, не дублюється тут.

## Канонічний скафолд

Для кожного пакета в скоупі обов'язкові: `.storybook/main.js`, `.storybook/preview.js`, `package.json#scripts.storybook`. Канонічні шаблони — `scaffold/template/`.

Фіксовані рішення (деталі — ADR, Кластер 2):

- **Порядок Vite-плагінів фіксований**: `@vitejs/plugin-vue` **перед** `quasar()` — інакше Quasar-плагін не бачить SFC, уже скомпільований `plugin-vue`.
- **Layout-детекція**: `src/components/` присутній → stories-glob звужується до нього; пласка структура (`src/` без `components/`) — ширший glob по всьому `src/`.
- **`viteFinal`** зчитує `vite.config` самого пакета (той самий, що й для звичайного білду) і мерджить його плагіни в конфіг Storybook, **знімаючи** `vite-plugin-pages`/`vite-plugin-vue-layouts` — файлова маршрутизація належить додатку-споживачу, не ізольованому рендеру компонента.
- **`staticDirs`** покриває `.storybook/public` — статичний asset для msw service worker (`preview.js`).
- **`preview.js`**: повний `Quasar`-install (не тільки окремі компоненти) + `iconSet`+`iconMapFn`-комбо — без цієї пари внутрішні Quasar-компоненти (напр. стрілка `QSelect`) не резолвлять вбудовані іконки поза full CLI build. `msw-storybook-addon` ініціалізується з `onUnhandledRequest`-фільтром: **same-origin GET мовчки пропускається** (Vite HMR/asset-шум), решта — попередження (не білд-помилка — навмисно м'яко для хвилі 1).
- **`.storybook/mocks/gql-sse.js`**: єдиний канонічний хелпер `sseSubscription` для MSW-мокання Apollo-підписок через wire-протокол `graphql-sse` (`event: next\ndata: …`, distinct-connection mode) — переносити цю логіку в кожен пакет окремо заборонено, є одне джерело істини.
- **`package.json#scripts.storybook`** — уніфікований скрипт, однаковий для всіх пакетів у скоупі (значення — `scaffold/main.mjs`, не дублюється тут).

Перевірка присутності й ключових маркерів канону — `scaffold/main.mjs`; детерміноване відтворення відсутніх файлів із `scaffold/template/` — `scaffold/fix-scaffold.mjs` (fixability: `config` — канонічна форма одна, LLM у ланцюжку фіксу не потрібен).

## Vitest-конфіг і Stryker-ізоляція (Кластер 5)

Канонічний `test.projects` (`unit`+`storybook`, browser-mode лише chromium) і ізольований `vitest.stryker.config` (той самий unit-набір, без browser-mode — `@stryker-mutator/vitest-runner` крашиться на browser-mode `projects`) — `vitest-config/main.mjs` (перевірка, AST через `oxc-parser`) і `vitest-config/fix-vitest-config.mjs` (точкові insert-only правки наявного конфіга, fixability: `config`). Деталі канону, чому саме chromium і межі автофіксу — `vitest-config/vitest-config.mdc`, не дублюється тут.

## Гігієна сторонніх залежностей (Кластер 6)

`hygiene/main.mjs`: (1) undeclared third-party imports у `.vue`-файлах пакета — import стороннього пакета, якого немає в `dependencies`/`peerDependencies` (реальний кейс ADR — зламаний default-export `@vuepic/vue-datepicker` v14, silent breakage без цієї перевірки); (2) наявність `src/css/quasar.variables.{scss,sass}` без відповідного `quasar({ sassVariables: true })` у `.storybook/main.js` — глобальні Quasar SCSS-змінні пакета інакше не резолвляться в ізольованому Storybook-рендері. Docs-only детальний виклад не потрібен — концерн самодостатній, без окремого `.mdc`.

## Мокання (Кластер 3, docs-only)

Рецепти router/`@nitra/tfm`/Apollo-GraphQL(MSW)/Pinia/сторінкових stories — `mocking/mocking.mdc`. Свідомо без механічної перевірки (`concern.json` без `check`/`policy`/`lint`-блоку, як і решта чисто-документаційних concern-ів репозиторію) — кожен пакет мокає свій набір залежностей по-своєму, детермінований чек дав би або хибні спрацювання, або нульове покриття.

## Adopt-режим і скіл `n-storybook` (Кластер 8)

Скіл `npm/skills/storybook/` (`.cursor/skills/n-storybook/` після синку) — тонка обгортка запуску: звичайний режим — `npx @7n/rules lint storybook`; `--adopt` — окремий діагностичний JS-модуль `adopt/main.mjs` для пакетів, де ВЖЕ є ручний `.storybook/`, що не збігається з каноном. Adopt діагностує diff по секціях проти `template/` (main.js/preview.js/mocks/gql-sse.js/package.json#scripts.storybook/vitest test.projects/vitest.stryker.config) — статус `match`/`differ`/`missing` на секцію, **без сліпого перезапису** розбіжних файлів; автофікс (`--fix-missing`) генерує лише секції зі статусом `missing`. Circuit breaker: збій діагностики одного пакета деградує до `status: 'broken'` для нього, решта пакетів прогону обробляються далі. Викликається напряму (`bun node_modules/@7n/rules-lang-js/rules/storybook/adopt/main.mjs`), без окремого CLI-прапорця в ядрі `n-rules.js` — деталі й приклади звіту в `SKILL.md` скіла.

## Що свідомо поза хвилею 1

LLM-генерація `args` для stories з `defineProps`/`defineEmits`/slots (Кластер 4 ADR) — хвиля 2, свідомо відкладена. Governance-винятки в `n-npm-module.mdc`/`n-bun.mdc` (Кластер 7 — Storybook-devDeps у `npm/package.json`, canonical version pin, review-гейт лише для нових stories) — окремий трек, не в обсязі цього правила.

## Мокання зовнішніх залежностей у Storybook

Джерело рішень: `docs/adr/канон-storybook-для-vue-компонентних-бібліотек.md`, Кластер 3 і розділ «Розширення (2026-07-20): сторінки — route.params + Apollo subscription + Pinia» (прототип-верифікація на реальному кейсі `gt`). Це docs-only концерн — рецепти для агента, що впроваджує/підтримує Storybook у консюмер-репо; механічної перевірки немає (кожен пакет мокає свій набір залежностей по-своєму, детермінований чек дав би або хибні спрацювання, або нульове покриття).

### Router

Детекція: компонент використовує `useRoute`/`useRouter` (composition API з `vue-router`). Базовий рецепт — `createMemoryHistory()` з одним catch-all-маршрутом, без реальних params:

```js
import { createMemoryHistory, createRouter } from 'vue-router'

const router = createRouter({
  history: createMemoryHistory(),
  routes: [{ path: '/:pathMatch(.*)*', component: { render: () => null } }]
})
```

Для сторінок (хвиля 2, app-проєкти з `src/pages/`) — реальний параметризований маршрут замість catch-all, `router.push` перед mount і `await router.isReady()` у Storybook `loaders` (не в декораторі — `loaders` виконується per-story до рендеру, прибирає перший рендер без `route.params`):

```js
const router = createRouter({
  history: createMemoryHistory(),
  routes: [{ path: '/task/:id', component: TaskPage }]
})

export const pageLoader = ({ args }) => async () => {
  await router.push(`/task/${args.taskId}`)
  await router.isReady()
  return { router }
}
```

### `@nitra/tfm`

No-op. `@nitra/tfm` (`tf`/`lang`/`getTr`) не потребує мокання — компонент рендериться з реальним модулем, переклади вже статичні дані в самому файлі (`vue/tfm-translations.mdc`). Задокументуй це явно в story-файлі коментарем (`// @nitra/tfm — no-op, реальний модуль`), щоб наступний агент не витрачав час на пошук неіснуючого моку.

### Apollo/GraphQL — виключно MSW

**Рішення ADR-розширення:** мокання GraphQL (query/mutation/subscription) — тільки на мережевому рівні через `msw-storybook-addon`, **без** `resolve.alias`-підмін app-коду (`boot/apollo.js` чи еквівалент лишається повністю справжнім). Facilitator у сесії розширення рекомендував лінк-рівневий alias-мок (справжні хуки `@vue3-apollo/core` + фейковий termination `ApolloLink`), а після вибору MSW — гібрид MSW+alias для side-effect boot-модулів; обрано чистий MSW, бо app-код (включно з link-split http/sse) не розходиться з production-поведінкою, а мок-хендлери переносні в майбутні vitest/playwright.

Query/mutation — стандартний `graphql.query`/`graphql.mutation` handler, сценарії через `parameters.msw`:

```js
import { graphql, HttpResponse } from 'msw'

export const Default = {
  parameters: {
    msw: {
      handlers: [graphql.query('GetTask', () => HttpResponse.json({ data: { task: taskFixture } }))]
    }
  }
}
```

Підписки — `msw-storybook-addon` не має готового `graphql.subscription()`-хендлера; wire-протокол `graphql-sse` (`event: next\ndata: …`, distinct-connection mode) мокається вручну через канонічний хелпер `sseSubscription` з `.storybook/mocks/gql-sse.js` (генерується скафолдом, `scaffold/template/mocks/gql-sse.js` — не копіювати логіку в кожен пакет, одне джерело істини для протоколу):

```js
import { http, HttpResponse } from 'msw'
import { sseSubscription } from '../../.storybook/mocks/gql-sse.js'

export const Realtime = {
  parameters: {
    msw: {
      handlers: [
        http.post('/graphql/stream', () =>
          new HttpResponse(sseSubscription([{ data: { taskUpdated: frame1 } }, { data: { taskUpdated: frame2 } }]), {
            headers: { 'Content-Type': 'text/event-stream' }
          })
        )
      ]
    }
  }
}
```

### Pinia

Справжня `createPinia()` у page-декораторі — **без** `pinia-plugin-persistedstate` (`persist: true` у сторі стає no-op, читання/запис localStorage не потрібні в ізольованому рендері). Наповнення початкового стану — через `parameters.pinia.initialState`, не хардкод у декораторі:

```js
import { createPinia } from 'pinia'

export function pageDecorator({ route, pinia } = {}) {
  return (story, ctx) => {
    const app = createPinia()
    if (ctx.parameters.pinia?.initialState) {
      for (const [id, state] of Object.entries(ctx.parameters.pinia.initialState)) {
        app.state.value[id] = state
      }
    }
    // ...install router/pinia у app instance, повернути wrapped story
  }
}
```

**Не** `@pinia/testing` (`createTestingPinia`) — вона за замовчуванням підміняє actions заглушками, а сторінка в Storybook має жити зі справжньою бізнес-логікою стору, не з заглушкою.

### Патерн story для сторінки

- Одна фабрика-декоратор `pageDecorator({ route, pinia })` на весь повторюваний код (router + pinia + Quasar layout) — не дублювати в кожному story-файлі.
- **`QLayout`/`QPageContainer`-wrapper обов'язковий**: `q-page` кидає виняток без layout-предка. Quasar SFC-transform (auto-реєстрація компонентів через build-time трансформ) **не працює** в runtime-шаблонах декораторів — `QLayout`/`QPageContainer`/`QPage` реєструються явно (`app.component('QLayout', QLayout)` тощо), інакше рендер падає з незрозумілою помилкою про невідомий тег.
- Фікстури — окремим модулем `.storybook/fixtures/<page>.js`, не inline в story-файлі (переюз між `Default`/`Loading`/`Error`/`Realtime`).
- **Smoke-мінімум**: одна story «рендериться без помилок» на кожну сторінку — обов'язковий нижній рівень покриття, навіть без окремих stories для кожного стану.
- Окремі stories для `Loading`/`Error`/`Realtime` (сценарій з кількома SSE-кадрами через `sseSubscription`) — де застосовно, поверх smoke-мінімуму.

### Мережеві side-effect компоненти без моку

Компонент робить мережеві виклики (analytics-трекер, session-boot тощо), для яких мокання поки не покрите канонічним рецептом — постав у story коментар-маркер `// n-storybook: лише display-стан, мережеві side-effects без моку`, щоб було видно свідоме рішення, а не забутий пропуск.

## Vitest-конфіг Storybook-пакета: named projects `unit`+`storybook` та ізоляція Stryker

Джерело рішення: ADR `канон-storybook-для-vue-компонентних-бібліотек.md`, Кластер 5. Стосується лише пакетів у скоупі `storybook` (`scope/main.mjs#collectInScopeVuePackages`).

### Канон `test.projects`

Vue-компонентна бібліотека вже має `vitest.config.{mjs,js,ts}` за каноном `vue/testing.mdc` (`mergeConfig(viteConfig, defineConfig({ test: {...} }))` з `environment: 'happy-dom'`). Storybook-хвиля **дописує** до цього `test`-блоку named-project `unit`+`storybook` — існуючі поля (`include`, `environment`, `coverage`) лишаються без змін, `projects` — нова властивість поруч:

- `{ extends: true, test: { name: 'unit' } }` — успадковує решту `test`-опцій пакета як є.
- `storybook`-проєкт — **browser-mode, лише chromium** (`browser: { enabled: true, provider: 'playwright', instances: [{ browser: 'chromium' }] }`) і `include` на stories-glob пакета (та сама layout-детекція, що й `scaffold/main.mjs#detectStoriesGlob`, лише без префіксу `../` — vitest-конфіг лежить у корені пакета, а не в `.storybook/`).

Firefox/webkit свідомо не додаються — ADR і main.mdc хвилі 1 фіксують лише chromium; розширення на інші браузери — поза обсягом цього концерну.

### Чому окремий `vitest.stryker.config`

`@stryker-mutator/vitest-runner` крашиться, коли конфіг, який він завантажує, містить browser-mode `projects` (сам факт присутності `storybook`-проєкту в основному vitest-конфізі ламає mutation-прогін, незалежно від того, чи Stryker фактично торкається storybook-файлів). Тому концерн генерує **сусідній** ізольований `vitest.stryker.config.<ext>` — той самий `mergeConfig(viteConfig, defineConfig({ test: {...} }))`, але **без** `projects`/browser-mode: лише unit-набір (`include`, `happy-dom`, `coverage`), на якому mutation-testing працює штатно.

Концерн лише генерує/підтримує цей файл поруч з основним vitest-конфігом. Він **не** переналаштовує `stryker.config.mjs#vitest.configFile` пакета (це відповідальність `test/stryker_config`, який поки що не знає про Storybook-канон) — до появи такого зв'язку вказати `configFile: 'vitest.stryker.config.<ext>'` для пакетів у скоупі Storybook потрібно вручну.

### Що перевіряє й що виправляє концерн

Перевірка (`main.mjs`) — AST-аналіз (`oxc-parser`) наявного vitest-конфіга: знаходить `test`-блок (незалежно від того, чи він огорнутий у `defineConfig`/`mergeConfig`, чи це простий об'єкт), дивиться на `test.projects` і класифікує елементи за `name: 'unit'`/`name: 'storybook'`; для `storybook`-елемента перевіряє маркери `chromium`/`browser`/stories-glob текстовим пошуком. Стійка до форматування й порядку полів — не вимагає конкретного стилю запису, лише семантичну присутність маркерів.

Автофікс (`fix-vitest-config.mjs`, fixability `config`) виправляє й дописує **лише відсутнє**:

- Немає vitest-конфіга взагалі → створює повний файл з canonical `unit`+`storybook` projects.
- Є test-блок без `projects` → вставляє нову property `projects: [...]` з обома записами, не займаючи `include`/`environment`/`coverage`.
- Є `projects`, але без одного із записів → дописує відсутній запис у кінець масиву.
- Немає `vitest.stryker.config.*` → генерує з canonical baseline.

Як і в `test/stryker_config`, правка — точкові string-splice-и (insert-only) поверх існуючого тексту, а не переписаний AST-serializer, щоб не зачепити форматування й коментарі решти файлу; результат повторно парситься, і при невалідному виводі запис скасовується (fail-closed).

**Свідомо без автофіксу:** `test.projects` — не статичний масив (spread/змінна), test-блок не вдалось знайти структурно, або `storybook`-запис уже присутній, але без якогось із маркерів (chromium/browser/stories-glob) — надійно виправити частковий вручну написаний запис програмно ризиковано, тож це лишається порушенням для ручного review (той самий компроміс, що й marker-порушення в `scaffold`).
