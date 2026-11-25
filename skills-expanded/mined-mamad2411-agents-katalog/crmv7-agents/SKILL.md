# AGENTS.md — платформа «Свистоплясово»

Монорепозиторий связывает SEO-first public site, CMS, CRM и NestJS/PostgreSQL backend. Активна Phase 4: CMS, public delivery, media, intake, analytics и SEO expansion.

## Authority

- Backend/CRM владеет operational facts: статусы, availability/capacity, цены, брони, оплаты, права и concurrency.
- CMS владеет editorial content, SEO, media, composition и publication.
- Public site читает только published public API/projections, не обращается к БД/internal API, не публикует draft/internal/PII и не подтверждает бронь.
- Один бизнес-факт не имеет двух authority; границы проходят через typed contracts, audit/outbox, notifications и cache invalidation.

Приоритет при конфликте: явная задача пользователя → актуальное решение в `DECISIONS.md` → рабочая спецификация контура → код как свидетельство реализованного состояния. История решений и исходные ТЗ доступны через Git; они не переопределяют текущие правила.

## Контекстный бюджет

1. Определить контур.
2. Историю Git открывать только для конкретного пробела.

## Маршруты

| Задача | Основной контекст |
|---|---|
| Scope / запуск / стек | нужный раздел `README.md`; версии и команды — `package.json` нужного workspace |
| CRM UI | `apps/crm/AGENTS.md`, затем текущие page/components/tests |
| CMS UI | `apps/admin/AGENTS.md`, затем нужный раздел `07-phase-4-cms/CMS-UX-SPEC.md` |
| Backend/domain/PostgreSQL | `04-domain-backend/domain-model.md`, затем один профильный backend-документ |
| API/auth/concurrency | `04-domain-backend/api-auth-concurrency.md` |
| Live/notifications | `04-domain-backend/live-notifications.md` |
| Public UI/sections/booking | `packages/site-ui/AGENTS.md`, затем текущий consumer |
| Managed public page | `apps/site/src/managed/AGENTS.md` |
| Offering/pricing/CRM↔CMS | только нужный раздел `07-phase-4-cms/OFFERING-CATALOG-ARCHITECTURE.md` |
| CMS/publication/media/delivery | `07-phase-4-cms/README.md`, затем один документ из его индекса |
| Public intake/integration | `07-phase-4-cms/PLATFORM-ARCHITECTURE.md` + релевантные contracts/code |
| SEO/site structure/content | один из `07-phase-4-cms/SEO-STRATEGY.md` / `07-phase-4-cms/SITE-STRUCTURE.md`; live-выводы только по source evidence |
| Analytics/я.Метрика | `07-phase-4-cms/ANALYTICS.md` |
| Tests/security/release | `06-quality-process/testing-security.md` |

Текущий статус и следующий инкремент находятся только в `07-phase-4-cms/README.md`. `07-phase-4-cms/IMPLEMENTATION-ROADMAP.md` открывать точечно при изменении порядка или проверке acceptance gate.

## Реализация

- Не откатывать чужие dirty changes; использовать shared contracts/design systems/repository boundaries без второй authority.
- Для затронутых границ проверять `authority → contract/API → consumer → audit/notification/cache`.
- Public frontend сохраняет Astro-first HTML, crawlability, metadata/accessibility и минимальную hydration; fixtures только в явном dev/test mode.
- Проверки пропорциональны риску; UI включает desktop/mobile, overflow, keyboard и ключевые states.

## Короткий рабочий цикл

- До реализации определить наблюдаемый результат и минимальную проверку. Для runtime/UI-задачи сначала воспроизвести проблему в целевой среде: процесс, URL, API/БД, auth и данные. Не выводить состояние приложения только из кода или старого лога.
- Если среда недоступна, сразу зафиксировать ограничение; продолжать независимую работу, но не считать live-приёмку выполненной.
- После выполнения acceptance завершать задачу. Полный набор проверок нужен по затронутым границам или release gate, а не после каждой локальной правки; команды и выбор проверок — в `06-quality-process/testing-security.md`.

## Делегирование
- Git-операции записи выполняет только main.

## Документация без накопления истории
- Task plan — во встроенном plan; текущий статус/следующий шаг — только Phase 4 README; roadmap — оставшийся scope/order/gate. Закрытые задачи из плана удалять.
- `DECISIONS.md` содержит только действующий нетривиальный выбор и причину. Исправлять заменённое решение, сохраняя ID; не дописывать противоречащую историю и описание уже видимого кода.
- В той же задаче обновлять основной документ, если код изменил архитектуру, authority, API/контракт, основной UX flow, запуск или ограничения. Удалять старое утверждение, не оставлять его рядом с новым. При переносе контура обновлять маршрут в `AGENTS.md`/README и ссылки.
- Приёмка включает проверку затронутой документации против итогового кода. Если расхождение обнаружено в scope задачи, исправить до коммита; если за его пределами — явно сообщить, не объявлять всю документацию актуальной. Локальная правка без изменения документированного контракта не требует нового текста.
- У каждой темы один основной документ. Новая spec нужна только для отдельного контракта, который не помещается в существующий раздел; не создавать отдельные inventory/status/handoff/summary файлы задачи.
- История реализации, команды и результаты проверок — итог задачи и Git. Постоянные сессионные logs и дублирующий implementation journal не вести. Незакрытое требование переносить в основной план/spec до удаления временного материала.
- После каждого завершённого изменения по запросу пользователя main создаёт отдельный git-коммит с понятным сообщением после интеграции и необходимых проверок.
