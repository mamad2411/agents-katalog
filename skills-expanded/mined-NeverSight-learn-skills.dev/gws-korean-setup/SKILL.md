---
name: gws-korean-setup
description: Google Workspace CLI(gws) 초기 설치 및 설정을 단계별로 안내합니다. npm 설치, gcloud CLI 설치, OAuth 인증, Claude Code 스킬 설치, 한국어 인코딩 설정까지 완료. 처음 gws를 사용하는 사용자를 위한 가이드.
argument-hint: "[--skip-gcloud] [--skip-skills]"
---

# Google Workspace CLI(gws) 설치 및 설정

gws CLI를 처음 설치하는 사용자를 위한 단계별 안내.
총 6단계로 진행되며, 각 단계가 끝날 때마다 정상 설치를 확인한다.

## 인수 처리

`$ARGUMENTS`에서 다음 플래그를 파싱한다:

- `--skip-gcloud` → Phase 2(gcloud 설치)를 건너뛴다
- `--skip-skills` → Phase 5(Claude Code 스킬 설치)를 건너뛴다

---

## Phase 1: gws CLI 설치

> gws는 npm 패키지로 배포된다. Node.js가 설치되어 있어야 한다.

### 1-1. 이미 설치되어 있는지 확인

```bash
which gws && gws --version
```

- Windows에서는 `where gws`로 확인한다.
- 버전이 출력되면 Phase 2로 바로 진행한다.

### 1-2. 설치

```bash
npm install -g @googleworkspace/cli
```

설치가 안 될 때:

| 증상 | 해결 |
|------|------|
| `npm: command not found` | Node.js가 없다. https://nodejs.org/ 에서 LTS 버전을 먼저 설치한다. |
| `EACCES: permission denied` | macOS/Linux: `sudo npm install -g @googleworkspace/cli`. Windows: 관리자 권한으로 터미널을 다시 열고 재시도. |

### 1-3. 설치 확인

```bash
gws --version
```

버전 번호가 출력되면 성공.

---

## Phase 2: gcloud CLI 설치

> `--skip-gcloud`이면 이 Phase를 건너뛴다.
>
> gcloud는 Google Cloud Platform(GCP) 프로젝트를 관리하는 도구다. gws의 OAuth 설정에서 GCP 프로젝트가 필요하므로 미리 설치해두면 편하다.

### 2-1. 이미 설치되어 있는지 확인

```bash
gcloud --version
```

- Windows에서는 `where gcloud`로 확인한다.
- 버전이 출력되면 2-5(초기 로그인)로 바로 진행한다.

### 2-2. OS 확인

`AskUserQuestion`으로 OS를 확인한다:

> gcloud CLI를 설치할게요. 사용 중인 OS를 알려주세요:
> 1. macOS Apple Silicon (M1/M2/M3/M4)
> 2. macOS Intel
> 3. Linux x86_64
> 4. Linux ARM
> 5. Windows

### 2-3. macOS / Linux 설치

OS에 맞는 URL로 다운로드한다:

| OS | 다운로드 URL |
|----|-------------|
| macOS Apple Silicon | `https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-darwin-arm.tar.gz` |
| macOS Intel | `https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-darwin-x86_64.tar.gz` |
| Linux x86_64 | `https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-x86_64.tar.gz` |
| Linux ARM | `https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-arm.tar.gz` |

```bash
# 다운로드
curl -O {위 테이블에서 선택한 URL}

# 압축 해제
tar -xzf google-cloud-cli-*.tar.gz

# 설치 (대화형 프롬프트가 나온다)
./google-cloud-sdk/install.sh
```

설치 스크립트가 질문하는 항목:
- **"Modify profile to update your $PATH?"** → `Y` 입력
- **쉘 프로파일 경로** → 그냥 Enter (기본값 수락)

설치 후 PATH를 현재 셸에 반영한다:

```bash
source ~/.zshrc   # zsh
source ~/.bashrc  # bash
```

### 2-4. Windows 설치

PowerShell에서 다음 두 명령어를 순서대로 실행한다:

```powershell
# 1. 설치 프로그램 다운로드
(New-Object Net.WebClient).DownloadFile("https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe", "$env:Temp\GoogleCloudSDKInstaller.exe")

# 2. 설치 프로그램 실행
& $env:Temp\GoogleCloudSDKInstaller.exe
```

설치 화면이 뜨면:
1. 기본 옵션으로 **Next** 클릭하며 진행
2. 마지막 화면에서 **"Run gcloud init" 체크를 해제** (Phase 3에서 별도 진행)
3. **Finish** 클릭

설치 후 PATH를 현재 셸에 반영한다:

```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
```

### 2-5. 설치 확인 및 초기 로그인

```bash
gcloud --version
```

버전이 나오면 초기 로그인을 한다:

```bash
gcloud auth login
```

브라우저가 열리면 Google 계정으로 로그인한다. 이 인증은 다음 단계(OAuth 설정)에서 GCP 프로젝트에 접근할 때 사용된다.

---

## Phase 3: OAuth 설정 (gws auth setup)

> 이 단계에서는 Google API를 사용할 수 있도록 OAuth 인증을 설정한다.
> 처음 하면 복잡해 보이지만, `gws auth setup` 명령이 대부분 자동으로 처리해준다.

실행 전에 사용자에게 전체 흐름을 미리 안내한다:

> 이제 OAuth 인증을 설정합니다. 총 5단계가 자동으로 진행됩니다:
> 1. GCP 프로젝트 선택 또는 새로 만들기
> 2. OAuth 동의 화면 구성 (앱 이름, 사용자 유형 설정)
> 3. Google API 활성화 (Gmail, Drive, Sheets, Docs 등)
> 4. OAuth 클라이언트 ID 생성
> 5. 인증 정보 파일 저장
>
> 대부분 자동이고, 몇 가지만 직접 선택하면 됩니다.

### 3-1. GCP 프로젝트 확인

`AskUserQuestion`으로 확인한다:

> 기존 GCP 프로젝트가 있으신가요?
> - **있다면** → 프로젝트 ID를 알려주세요 (예: `my-gws-project`)
> - **없거나 모르겠다면** → 새로 만들겠습니다 (Enter)

### 3-2. setup 실행

```bash
# 기존 프로젝트가 있는 경우
gws auth setup --project {PROJECT_ID} --login

# 새 프로젝트를 생성하는 경우
gws auth setup --login
```

### 3-3. 대화형 프롬프트 안내

명령 실행 중 브라우저에서 설정 화면이 열린다. 사용자에게 다음 순서로 안내한다:

1. **GCP 프로젝트**: 기존 프로젝트를 선택하거나 새 이름을 입력
2. **OAuth 동의 화면** — 브라우저에서 순서대로 입력:
   1. **앱 이름**: 자유롭게 짓는다 (예: "GWS CLI", "내 워크스페이스" 등 아무거나 괜찮음)
   2. **사용자 지원 이메일**: 현재 로그인한 Google 계정의 이메일을 선택
   3. **개발자 연락처 이메일**: 같은 이메일을 입력
   4. **대상** (User Type):
      - 회사/학교 Google Workspace 계정 → **내부(Internal)** 선택 (권장, 추가 설정 불필요)
      - 개인 Gmail(@gmail.com) → **외부(External)** 선택
   5. 만들기 클릭 → 나머지 항목은 기본값 그대로 **저장 후 계속** 클릭하며 끝까지 진행
   6. **외부(External)를 선택한 경우에만**: 테스트 사용자 등록이 필요하다
      - OAuth 동의 화면 → **대상** 탭 → **테스트 사용자** 섹션
      - **Add users** 클릭 → 로그인에 사용할 본인 Gmail 추가 → 저장
      - 이 단계를 빠뜨리면 Phase 4에서 **"액세스 차단됨: 승인 오류"** 가 발생한다
3. **API 활성화**: Gmail, Drive, Sheets, Docs, Calendar 등 — 자동으로 처리됨
4. **OAuth 클라이언트 ID**: Desktop app 타입으로 자동 생성됨
5. **client_secret.json 저장**: 화면에 클라이언트 ID와 시크릿이 표시되면 **JSON 다운로드** 버튼을 클릭하거나, 표시된 JSON을 복사한다

### 3-4. client_secret.json 저장

다운로드하거나 복사한 JSON을 `~/.config/gws/client_secret.json`에 저장한다:

```bash
# 디렉토리가 없으면 생성
mkdir -p ~/.config/gws

# 복사한 JSON을 붙여넣기 (Ctrl+V 후 Ctrl+D로 저장)
cat > ~/.config/gws/client_secret.json
```

Windows:
```powershell
mkdir -Force "$env:USERPROFILE\.config\gws"

# 메모장으로 열어서 JSON 붙여넣기 후 저장
notepad "$env:USERPROFILE\.config\gws\client_secret.json"
```

### 3-5. 설정 확인

```bash
ls -la ~/.config/gws/client_secret.json
```

파일이 보이면 성공.

---

## Phase 4: 로그인 (gws auth login)

> OAuth 설정이 끝났으니, 이제 실제로 Google 계정에 로그인한다.

### 4-1. 인증 범위 선택

`AskUserQuestion`으로 안내한다:

> 어떤 Google 서비스에 접근할지 선택해주세요:
> 1. **필요한 서비스만 (권장)** — Gmail, Drive, Sheets, Calendar, Docs
> 2. **읽기 전용** — 모든 서비스를 읽기만
> 3. **전체 권한** — 모든 서비스에 읽기/쓰기 (restricted_client 경고가 나올 수 있음)

선택에 따라 명령어를 **백그라운드로 실행**한다 (`run_in_background: true`).
인증 URL 대기 중 Claude가 멈추지 않도록 하기 위함이다.

```bash
# 1번 선택
gws auth login -s gmail,drive,sheets,calendar,docs

# 2번 선택
gws auth login --readonly

# 3번 선택
gws auth login --full
```

### 4-2. 브라우저에서 로그인

명령이 백그라운드에서 실행되면 사용자에게 안내한다:

> 인증 URL이 Bash 출력에 있습니다.
> **Ctrl+O** 를 눌러 출력을 펼친 뒤, URL을 복사해서 브라우저에 붙여넣기 해주세요.
> 브라우저에서 인증을 완료하면 알려주세요.

브라우저에서 인증 페이지가 열리면 다음 순서로 진행된다:

1. Google 계정을 선택한다
2. **"이 앱은 Google의 인증을 받지 않았습니다"** 라는 경고가 나온다 — **이것은 정상이다.** 개인용 OAuth 앱은 Google 심사를 받지 않으므로 항상 이 경고가 표시된다.
3. **"고급"** 을 클릭한다
4. **"(앱 이름)(으)로 이동 (안전하지 않음)"** 을 클릭한다
5. 요청된 권한을 확인하고 **"허용"** 을 클릭한다

### 4-3. 로그인 확인

사용자가 인증을 마쳤다고 하면 `gws auth status`로 확인한다:

```bash
gws auth status
```

인증된 계정과 스코프가 표시되면 성공.

### 4-4. 간단한 동작 테스트

```bash
# Gmail: 최근 메일 1건 조회
gws gmail users.messages list --userId me --maxResults 1

# Drive: 파일 1건 조회
gws drive files list --pageSize 1
```

결과가 나오면 gws가 정상 작동하는 것이다.

---

## Phase 5: Claude Code 스킬 설치

> `--skip-skills`이면 이 Phase를 건너뛴다.
>
> gws의 Claude Code 스킬을 설치하면 `/gws-gmail-send`, `/gws-drive` 같은 명령을 Claude Code에서 바로 쓸 수 있다.

```bash
npx skills add https://github.com/googleworkspace/cli
```

설치 후 Claude Code를 재시작하면 gws-* 스킬들이 `/` 메뉴에 나타난다.

---

## Phase 6: 한국어 인코딩 안내

> gws로 한국어 텍스트를 다룰 때 알아야 할 핵심 규칙을 안내한다.
> 자세한 내용은 `/gws-korean-encoding` 스킬에 정리되어 있다.

사용자에게 다음 핵심 사항을 안내한다:

### 꼭 알아야 할 3가지

1. **이메일 주소의 한글 이름** — RFC 2047 Base64 인코딩이 필요하다
   ```
   # "홍길동 <hong@example.com>" → 이렇게 인코딩
   =?UTF-8?B?7ZmN6ri464+Z?= <hong@example.com>
   ```
   ```bash
   # 인코딩 생성 방법
   echo -n "홍길동" | base64
   ```

2. **한글 파라미터는 큰따옴표로 감싸기**
   ```bash
   gws gmail users.messages send --userId me --subject "회의 안내"
   ```

3. **긴 한글 텍스트는 임시 파일 사용**
   ```bash
   echo "긴 본문..." > /tmp/body.txt
   gws gmail users.messages send --userId me --bodyFile /tmp/body.txt
   ```

> 한글이 깨지는 문제가 생기면 `/gws-korean-encoding` 스킬의 디버깅 체크리스트를 참조하세요.

---

## 완료 확인

모든 Phase가 끝나면 최종 점검을 한다:

```bash
gws --version
gcloud --version
gws auth status
ls ~/.config/gws/client_secret.json
```

사용자에게 결과를 요약 테이블로 보여준다:

| 항목 | 상태 | 비고 |
|------|------|------|
| gws CLI | ✅ / ❌ | 버전 |
| gcloud CLI | ✅ / ❌ / ⏭️ 스킵 | 버전 |
| OAuth 설정 | ✅ / ❌ | client_secret.json 존재 여부 |
| 인증 로그인 | ✅ / ❌ | 인증된 스코프 |
| Claude Code 스킬 | ✅ / ❌ / ⏭️ 스킵 | gws-* 스킬 수 |
| 한국어 인코딩 | ℹ️ 안내 완료 | — |

---

## 문제 해결

상세 트러블슈팅은 `references/troubleshooting.md`를 참조한다.

자주 발생하는 문제:

| 증상 | 해결 |
|------|------|
| `gws: command not found` | `npm config get prefix` → PATH에 `{prefix}/bin` 추가 |
| `gcloud: command not found` | 터미널을 새로 열거나 `source ~/.zshrc` |
| `restricted_client` 경고 | 정상. 테스트 사용자로 등록된 계정만 사용 가능 |
| `invalid_grant` | 토큰 만료. `gws auth login` 재실행 |
| `PERMISSION_DENIED` | `gws auth setup`으로 API 재활성화 후 `gws auth login` |
| Windows에서 명령 미인식 | PowerShell/CMD를 새로 열기. PATH 확인 |
