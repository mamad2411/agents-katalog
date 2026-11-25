# gpt-image 스킬을 공유 외부 스킬로 편입

## 상태

채택 (2026-08)

## 맥락

[GENEXIS-AI/gpt-image-skill](https://github.com/GENEXIS-AI/gpt-image-skill)은
ChatGPT 구독(`codex login` = ChatGPT)으로 이미지를 생성·편집하는 스킬이다.
Claude Code와 Codex 양쪽에서 같은 `gpt-image/` 디렉토리를 쓰며, 실제 생성은
로컬 Codex CLI를 중첩 실행(`codex exec --ephemeral --ignore-user-config`)해
내장 `$imagegen`을 호출한다. Images API·`OPENAI_API_KEY`는 코드 레벨에서 차단된다.

저장소가 제공하는 `bootstrap` 설치기는 다음 이유로 이 하네스에 그대로 쓸 수 없다:

- Claude 링크 대상이 `os.homedir()/.claude`로 고정되어 `CLAUDE_CONFIG_DIR`을
  무시한다 → 업무 계정(`~/.claude-upstage`)에는 설치되지 않는다
- Codex CLI·Node.js를 자동 설치하는 경로가 포함되어 있다(하네스는 런타임
  설치를 사용자에게 맡긴다)
- 설치 상태가 `setup.sh`/`check.sh` 밖에 남아 다른 머신에서 재현되지 않는다

## 결정

`shared/skills.json`에 선언된 **공유 외부 스킬** 메커니즘을 도입하고
gpt-image를 첫 항목으로 등록한다 (`shared/lib/shared-skills.sh`):

- 저장소를 `${XDG_DATA_HOME:-~/.local/share}/<repo>`에 영구 클론하고, 이후에는
  로컬 변경이 없을 때만 `--ff-only`로 갱신한다
- 심링크로 노출한다: `~/.agents/skills/<name>` (Codex 네이티브 경로이자
  `$CODEX_SKILLS_DIR/<name>` 링크의 소스), `~/.claude/skills/<name>`,
  `~/.claude-upstage/skills/<name>`
- 저장소의 `bootstrap`/`install-codex`/`login`은 사용하지 않는다. 로그인 상태와
  Node 버전은 사용자 책임이며, `setup.sh`/`check.sh`는 Node < `node_min`(22)일 때
  경고만 낸다
- 다른 사용자와 공유하는 호스트(예: Slurm 로그인 노드)에서도 시스템 Node를
  건드리지 않는다. nvm 등 사용자 레벨 Node로 요구 버전을 맞춘다

## 검토한 대안

- **`codex/external-skills.json`으로 설치**: 그 경로는 스킬 디렉토리를 Codex
  skills 폴더에 *복사*한다. gpt-image는 스크립트가 클론 루트를 기준으로 자기
  위치를 계산하고 git ff 갱신을 전제로 하므로 심링크가 필요하다. 또한 Claude
  쪽 링크를 만들지 못한다. 기각.
- **저장소의 원클릭 설치 프롬프트(`bootstrap --target all --yes`) 사용**:
  위 맥락의 세 가지 문제. 기각. 단 `doctor --json`은 진단용으로 계속 유용하다.
- **`claude/skills/`에 벤더링**: 36KB 문서 + 2K줄 스크립트를 복사해 두면 업스트림
  갱신을 놓치고, Codex 쪽 대응물을 별도로 관리해야 한다. 기각.

## 결과

- `./setup.sh` 한 번으로 세 위치에 링크가 생기고 `./check.sh`가 검증한다.
  gpt-image 관련 상태 파일은 `~/.local/share/gpt-image-skill` 하나뿐이다.
- 세션 context 영향은 스킬 목록의 description 한 줄뿐이다. 본문·참조 문서는
  `/gpt-image` 호출 시에만 로드되고, hooks/settings/MCP는 건드리지 않는다.
- 생성 시 중첩 Codex는 `--ignore-user-config`로 뜨므로 하네스의
  `config.toml`/hooks/MCP는 그 프로세스에 적용되지 않는다(이미지 생성 전용,
  `--sandbox workspace-write`, 승인 없음). 이는 의도된 업스트림 동작이다.
- 결과물은 `<작업 디렉토리>/generated-images/*.png`에 저장되며 ChatGPT 구독
  사용량을 소모한다(업스트림 안내: 일반 턴 대비 3–5배).
- Codex `openai.yaml`에 `allow_implicit_invocation: true`가 있어 Codex에서는
  이미지 요청 시 `$gpt-image` 없이도 발동할 수 있다.
