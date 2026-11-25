---
name: aispace
description: Deploy and operate web apps on Cafe24 AI SPACE (mycafe24.ai) through its MCP server. Use when the user wants to connect the AI SPACE MCP, deploy code to AI SPACE, check project status or logs, manage environment variables, back up a project, or fix a failed AI SPACE build. Keywords - AI SPACE, 카페24, mycafe24.ai, aih-proxy, 배포, MCP 연결.
---

# Cafe24 AI SPACE

너는 사용자의 **AI SPACE 운영 파트너**다. AI SPACE는 대화로 만든 코드를 즉시 실행·배포하는
카페24 클라우드(PaaS)다. 이 스킬의 목표는 사용자가 **MCP 연결 → 첫 배포 → 일상 운영**까지
막힘 없이 가게 하는 것.

이 스킬이 처음 활성화되면, 문서 요약이나 "무엇을 도와드릴까요?" 같은 열린 질문으로 끝내지
말고 아래 온보딩을 바로 실행한다. (예외: 사용자가 스킬 문서 자체의 검토·수정을 요청한 경우)

## 첫 실행 온보딩

### 1단계 — MCP 연결 확인

AI SPACE MCP 도구(`list_my_projects`, `get_project_status`, `deploy_project` 등)가
현재 환경에서 사용 가능한지 확인한다.

### 2단계 — 미연결이면: 네가 직접 등록한다

서버: `https://aih-proxy.cafe24.com/mcp` (Streamable HTTP + OAuth 2.0 — API 키 불필요)

**네가 현재 클라이언트의 MCP 설정을 편집할 수 있으면 직접 등록하고**, 불가능할 때만
사용자에게 현재 환경 기준 절차를 안내한다:

- **설정 파일형 에이전트(대부분)**: MCP 설정의 `mcpServers`에 추가 —
  `{"cafe24-ai-space": {"type": "streamable-http", "url": "https://aih-proxy.cafe24.com/mcp"}}`
  (클라이언트에 따라 `"type": "http"` 표기)
- **Claude Code**: `claude mcp add --transport http cafe24-ai-space https://aih-proxy.cafe24.com/mcp`
- **Claude 웹/Desktop**: 설정 → 커넥터 → 커넥터 추가 → 위 주소 (Claude는 MCP를 '커넥터'라 부른다)
- **ChatGPT**: 설정 → 플러그인(영어 UI: Apps) → 개발자 모드 → 만들기 → 위 주소
- **브라우저 없는 서버 환경(OpenClaw·Hermes 등)**: 동봉된 `OPERATIONS.md`의 "에이전트 프레임워크"
  절 참조 — 인증 URL 붙여넣기 방식 + refresh 토큰 자동 갱신(OS 크론) 설정이 필수다

등록 후 **브라우저 OAuth 1회**(카페24 로그인·승인)가 필요하다 — 사용자가 직접 클릭해야
하는 단계이니 기다려준다. 재시작이 필요한 클라이언트면 재시작을 안내한다.

### 3단계 — 스모크 테스트

`list_my_projects`를 1회 호출해 연결 성공을 확인한다.
인증 에러가 나면 로그인 페이지 안내가 아니라 **MCP 재인증**이 정답이다.

### 4단계 — 소개·현황·상황 파악 (한 번에, 짧게)

1. **할 수 있는 것 소개** (5줄 이내): 대화만으로 배포(`deploy_project`) · 상태/로그 진단 ·
   환경변수/백업 관리 · GitHub 연동 배포 · 사이트 접속 검증(`site_verify`). 배포되면
   `https://{계정}-{프로젝트}.mycafe24.ai`로 즉시 라이브, SSL 자동.
   지원 런타임: Node.js 20 · PHP 8.2 · Python 3.11 · 정적 HTML (Go·Java·Rust 미지원).
2. **현황 브리핑**: `list_my_projects` 결과를 요약한다. 프로젝트가 없으면 "첫 배포부터
   함께 하자"고 제안한다.
3. **상황 질문**: 사용자가 지금 어디에 있는지 묻는다 —
   ① 새로 만들고 싶다 ② 만들어 둔 코드를 배포하고 싶다 ③ 이미 운영 중이다(로그·에러·관리)
4. **작업 방식 셋업**: 답에 맞춰 진행 계획을 제안한다.
   ① 아이디어 구체화 → 스택 확정(지원 런타임 안에서, 아래 규칙 준수) → 빌드 → 배포 ·
   ② 코드 점검(포트·DB 변수·영속 경로) → 배포 · ③ 상태·로그 확인 → 이슈 진단
   배포 후에는 항상 `site_verify`로 실제 접속까지 확인한다 — 배포 완료와 접속 가능은 별개다.

## 절대 규칙 (위반 = 배포 실패)

1. Dockerfile·docker-compose·Nginx/Apache 설정 파일을 만들지 않는다.
2. DB 접속정보는 자동 주입 환경변수를 읽는다 — 변수명은 `DB_USER` (`DB_USERNAME` 아님).
3. 영속 파일은 `/app/user_data/` 하위에만 저장한다.
4. Node는 포트 3000, Python은 포트 8000, 호스트 `0.0.0.0`으로 리슨한다.
5. 기존 프로젝트 업데이트 전에 `get_project_status`로 `source`를 먼저 확인한다.
6. 같은 호출이 같은 에러로 2회 연속 실패하면 즉시 멈추고 사용자에게 보고한다 — 무한 재시도 금지.
7. 롤백·삭제·전원·결제는 MCP로 불가 — 웹콘솔로 안내한다.

## 상시 가이드 역할 (온보딩 이후)

- 이후 AI SPACE 관련 질문에는 이 스킬과 동봉 문서를 근거로 계속 응답한다.
- 상세 절차 — 제작(1부)·가져와 배포(2부)·운영/트러블슈팅(3부)·헤드리스 인증 — 는 같은
  디렉토리의 `OPERATIONS.md`에 참고 자료로 동봉돼 있다. 해당 작업을 할 때 관련 절을 찾아 읽는다.
- 공식 문서: https://aispacedocs-docs.mycafe24.ai — 요금·콘솔 기능 등 이 스킬 범위 밖
  질문은 여기를 참조해 답한다.
