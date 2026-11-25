---
name: bun-windows-copyfile-backend
description: Bun on Windows 에서 `bun install` 이 `Failed to link ... EUNKNOWN` 으로 실패할 때, `--backend=copyfile` 로 symlink 경로를 파일 복사로 우회한다.
category: cli
tags: [bun, windows, symlink, node_modules, install]
triggers:
  - "bun install windows"
  - "Failed to link EUNKNOWN"
  - "bun symlink error"
  - "bun windows node_modules"
source_project: lucida-ui
version: 1.0.0
---

# bun-windows-copyfile-backend

## Purpose
`bun install` 이 Windows 에서 `error: Failed to link <pkg>: EUNKNOWN` 로 실패할 때, 관리자 권한 없이 즉시 우회한다.

## When to Activate
- OS: Windows (10/11, Git Bash / PowerShell 환경)
- Bun 1.3.x 이상
- 에러: `Failed to link @xxx/yyy: EUNKNOWN` 반복

## 원인
Bun 은 기본적으로 node_modules 에 **symlink** 를 만든다. Windows 는 개발자 모드 또는 관리자 권한이 없으면 symlink 생성 실패 → link step EUNKNOWN.

## Fix
설치 명령에 `--backend=copyfile` 플래그를 추가:
```bash
bun install --backend=copyfile
```
symlink 대신 파일 복사로 node_modules 를 구성한다. 디스크 사용량이 약간 늘지만 Windows 에서 안정적이다.

## 영속화 옵션
1. `.bunfig.toml` 에 기록:
   ```toml
   [install]
   backend = "copyfile"
   ```
2. 또는 CI/개발 스크립트에 `bun install --backend=copyfile` 를 하드코딩.

## Verify
```bash
ls node_modules/<pkg>  # 실제 파일 (심볼릭 링크 아님) 인지 확인
```
PowerShell: `Get-Item node_modules\<pkg> | Select-Object LinkType`. `LinkType` 가 `$null` 이면 copy 성공.

## 참고
- Claude Code gstack skill 의 `browse` 바이너리 빌드 시에도 동일 이슈 재현됨.
- Node 호환 bundle 을 생성해야 하는 Windows 환경에서는 `scripts/build-node-server.sh` 같은 별도 후처리가 필요할 수 있다.
