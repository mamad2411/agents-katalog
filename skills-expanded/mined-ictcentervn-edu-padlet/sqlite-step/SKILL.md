---
name: sqlite-step
description: "교육용 Padlet 클론 Step 2: SQLite DB로 전환하는 코드 및 교안 가이드. Step 1 Notion 코드에서 db.js만 교체하여 SQLite로 마이그레이션. SQL 입문, 파일 DB 개념 학습. SQLite 전환, Step 2 코드 작성, SQL 입문 교안이 필요하면 이 스킬을 사용할 것."
---

# SQLite Step — Step 2 구현 가이드

교육용 Padlet 클론의 두 번째 단계: **파일 하나가 곧 데이터베이스**인 SQLite 도입.

## 이 단계의 핵심 메시지

> "Notion에서 데이터를 저장하던 걸 기억하나요? 이번엔 같은 일을 내 컴퓨터 파일로 해봅시다."

Step 1과 비교하며 배우는 것이 핵심이다.
`server.js`는 **그대로**, `db.js`만 바꾸는 것으로 전환 완료.

## 이 단계의 학습 목표

- DB = 데이터를 저장하는 파일/시스템이라는 개념 체화
- SQL 기본 문법 4가지: `CREATE TABLE`, `SELECT`, `INSERT`, `DELETE`
- ORM 없이 직접 SQL 작성 경험 (이후 Prisma/ORM의 편리함 이해 기반)
- 서버를 껐다 켜도 데이터가 유지되는 이유 이해

## 기술 스택

```
브라우저 (HTML/CSS/JS)  ← Step 1과 동일
    ↕ fetch()
localhost:3000 (Express.js)  ← Step 1과 동일
    ↕ better-sqlite3
padlet.db (파일 하나)  ← NEW: Notion 대신 로컬 파일
```

**변경 사항:**
- `db.js` 교체 (Notion SDK → better-sqlite3)
- `.env` 변경 (Notion 키 제거, DB 파일 경로 추가)
- `padlet.db` 파일 자동 생성

**유지 사항:**
- `server.js` — 변경 없음
- `public/` 디렉토리 전체 — 변경 없음
- `package.json` — 패키지 추가만

**사용 패키지 추가:**
- `better-sqlite3` — 동기식 SQLite (교육용으로 async/await 없이 단순)

## db.js (SQLite 버전) 표준 구현

**동일한 함수 시그니처**를 유지해야 server.js가 수정 없이 동작한다:

```javascript
// SQLite db.js — Step 1의 db.js를 이것으로 교체하세요
const Database = require('better-sqlite3');
const path = require('path');

// padlet.db 파일을 프로젝트 폴더에 생성 (없으면 자동 생성)
const db = new Database(path.join(__dirname, 'padlet.db'));

module.exports = {
  // 테이블이 없으면 만들기 (서버 시작 시 한 번 실행)
  initialize: async () => {
    db.exec(`
      CREATE TABLE IF NOT EXISTS cards (
        id        TEXT PRIMARY KEY,
        title     TEXT NOT NULL,
        content   TEXT DEFAULT '',
        color     TEXT DEFAULT 'yellow',
        board_id  TEXT DEFAULT 'default',
        created_at TEXT DEFAULT (datetime('now'))
      );
      CREATE TABLE IF NOT EXISTS boards (
        id   TEXT PRIMARY KEY,
        name TEXT NOT NULL
      );
      INSERT OR IGNORE INTO boards (id, name) VALUES ('default', '우리 반 보드');
    `);
    console.log('✅ SQLite DB 초기화 완료 (padlet.db)');
  },

  // 카드 목록 조회
  getCards: async (boardId = 'default') => {
    const stmt = boardId === 'all'
      ? db.prepare('SELECT * FROM cards ORDER BY created_at DESC')
      : db.prepare('SELECT * FROM cards WHERE board_id = ? ORDER BY created_at DESC');
    return boardId === 'all' ? stmt.all() : stmt.all(boardId);
  },

  // 카드 생성
  createCard: async ({ title, content = '', color = 'yellow', boardId = 'default' }) => {
    const id = Date.now().toString(); // 간단한 ID 생성
    db.prepare(
      'INSERT INTO cards (id, title, content, color, board_id) VALUES (?, ?, ?, ?, ?)'
    ).run(id, title, content, color, boardId);
    return { id, title, content, color, boardId };
  },

  // 카드 수정
  updateCard: async (id, { title, content, color }) => {
    const updates = [];
    const values = [];
    if (title !== undefined)   { updates.push('title = ?');   values.push(title); }
    if (content !== undefined) { updates.push('content = ?'); values.push(content); }
    if (color !== undefined)   { updates.push('color = ?');   values.push(color); }
    values.push(id);
    db.prepare(`UPDATE cards SET ${updates.join(', ')} WHERE id = ?`).run(...values);
    return db.prepare('SELECT * FROM cards WHERE id = ?').get(id);
  },

  // 카드 삭제
  deleteCard: async (id) => {
    db.prepare('DELETE FROM cards WHERE id = ?').run(id);
    return { success: true };
  },

  // 보드 목록
  getBoards: async () => db.prepare('SELECT * FROM boards').all(),
  createBoard: async ({ name }) => {
    const id = name.toLowerCase().replace(/\s/g, '-');
    db.prepare('INSERT OR IGNORE INTO boards (id, name) VALUES (?, ?)').run(id, name);
    return { id, name };
  },
};
```

## .env.example (Step 2용)

```
# SQLite DB 파일 경로 (기본값: 프로젝트 폴더의 padlet.db)
# 보통 변경할 필요 없음
DB_PATH=./padlet.db
```

## 전환 방법 (학생 실습 시나리오)

code-builder가 생성하는 마이그레이션 가이드에 포함할 내용:

```
Step 1 → Step 2 전환 체크리스트

□ step2-sqlite/ 폴더 생성
□ step1-notion/server.js   → step2-sqlite/server.js  (복사, 수정 없음)
□ step1-notion/public/     → step2-sqlite/public/     (복사, 수정 없음)
□ 새 db.js 작성 (SQLite 버전)
□ 새 package.json 작성 (better-sqlite3 추가)
□ .env.example 업데이트

확인: node server.js 실행 → padlet.db 파일 생성됨?
```

## 교육 포인트: SQL 비교 표

curriculum-writer가 교안에 포함할 Notion ↔ SQL 비교:

| Notion 행위 | SQL 동작 | SQL 문법 |
|------------|---------|---------|
| 새 행 추가 | 레코드 삽입 | `INSERT INTO cards ...` |
| 행 내용 보기 | 레코드 조회 | `SELECT * FROM cards` |
| 행 삭제 | 레코드 삭제 | `DELETE FROM cards WHERE id = ?` |
| 열 = 컬럼 | 필드 = 컬럼 | `title TEXT, content TEXT` |
| 표 = 데이터베이스 | 테이블 | `CREATE TABLE cards (...)` |

## SQLite 직접 확인하기 (선택 심화)

학생들이 파일을 직접 볼 수 있도록:

```bash
# 터미널에서 SQLite 데이터 직접 확인
npx better-sqlite3-cli padlet.db
# 또는 VS Code 확장: SQLite Viewer 설치 후 padlet.db 클릭
```

VS Code에서 SQLite Viewer 확장 설치하면 Excel처럼 데이터 확인 가능.
이것이 핵심 교육 포인트: "우리 앱의 데이터가 이 파일에 있어요!"

## 테스트 시나리오

1. `npm install` → `node server.js` 실행
2. `padlet.db` 파일 생성됨 확인
3. 카드 추가 → VS Code SQLite Viewer에서 새 행 확인
4. 카드 삭제 → 행 사라짐 확인
5. `node server.js` 종료 후 재시작 → 카드 데이터 유지됨 확인
   (Notion과 달리 서버가 꺼져도 데이터 유지 → "왜?" 토론)
