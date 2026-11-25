# Nightscout Platform — Main Codex Skill (Entry Point)

- `nightscout-platform-api-map/SKILL.md` (таблица: модуль → endpoints → jobs → DB)

---

## 1) Главные правила (не ломать старое)

1) **Один PR = одна цель.**  
   Большая фича = несколько PR.

2) **По умолчанию только additive изменения.**  
   API: добавлять поля/эндпойнты.  
   DB: новые таблицы/колонки (nullable/с дефолтами).  

3) **Ничего не удалять в первом PR.**  
   Сначала добавить параллельно.  
   Потом переключить.  
   Потом удалить (отдельно).

4) **Feature flags обязательны для новых модулей.**  
   По умолчанию OFF.  
   Включает ADMIN через UI Studio / DefaultConfig.

5) **Идемпотентность обязательна:**
   - Mobile/Lifestyle write: `Idempotency-Key`  
   - Telegram actions: стабильный idempotencyKey (tg:<chatId>:<messageId>:<action>)  
   - Wallet ledger: уникальный idempotencyKey

6) **Секреты не логировать.**  
   Не печатать `.env`, токены, `API_SECRET`, `initData`.

---

## 2) Source of Truth = сервер (обязательно)

Все проверки, smoke, и анализ логов делаются на сервере по SSH:

`ssh -p 40242 -i ~/.ssh/root_blast root@178.212.236.2`

Минимальный цикл:
- обновить код (git)
- `docker compose up -d --build`
- проверить `api /health`
- посмотреть логи `api` и `worker`

---

## 3) Где что живёт (очень коротко)

- Frontend: `apps/frontend` (panel.* и /tg/*)
- API: `apps/api`
- Worker: `apps/worker`
- Telegram bot: `apps/bot`
- Shared: `packages/shared`
- Prisma: `apps/api/prisma/schema.prisma`
- Compose: `infra/docker-compose.yml`

---

## 4) Smoke тесты (после рискованных изменений)

Минимум:
- Create MANAGED instance (RUNNING)
- AI chat session (job проходит steps)
- Meals photo estimate + confirm (carbs в Nightscout + лог в Postgres)
- Report 24h
- Doctor PDF
- Telegram bot: report/pdf/meal/ai
- /tg: автологин на любой странице
- DIARY_ONLY: diary write + health upload (если трогали lifestyle)

---

## 5) Обязательное правило обновления карты

Если меняешь endpoints/jobs/модели — обнови:
`nightscout-platform-api-map/SKILL.md`
