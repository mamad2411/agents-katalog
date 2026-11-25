---
name: manage-workflows
description: ComfyUI 워크플로우 패키지를 관리할 때 사용한다 (새 워크플로우 등록, 기존 워크플로우 수정/조회/삭제).
allowed-tools: Read
---

# ComfyUI 워크플로우 패키지 관리

## 개요

`comfyui_workflow` 도구로 워크플로우 패키지를 CRUD한다. 각 패키지는 `workflow.json` + `params.json` + 선택적 `resolver.mjs`로 구성된다.

## LoRA를 포함한 패키지 설계

LoRA를 추가·변경할 때는 [이미지 생성 스킬](../generate-image/SKILL.md)의 「모델별 LoRA 치트시트 확인」 절차로 모델 호환성·권장 강도·트리거·기본 체인 중복을 확인한다. 참조 경로는 이 SKILL.md 기준이다. 단순 목록 조회나 LoRA와 무관한 패키지 수정에는 치트시트 조회가 필요 없다.

## Action별 사용법

### list — 패키지 목록 조회

```json
{ "action": "list" }
```

반환: 각 패키지의 name, description, 파라미터 요약, resolver 존재 여부

### get — 패키지 상세 조회

```json
{ "action": "get", "name": "portrait" }
```

반환: workflow.json 전체, params.json 전체, resolver.mjs 소스코드 (있으면)

### save — 패키지 생성/수정

```json
{
  "action": "save",
  "name": "my-workflow",
  "workflow": { "1": { "class_type": "...", "inputs": {...} }, ... },
  "params": {
    "description": "워크플로우 설명",
    "features": {
      "checkpoint_auto": true,
      "lora_injection": true,
      "lora_couple_branches": false,
      "seed_randomize": true,
      "trigger_tags": true
    },
    "params": {
      "prompt": { "node": "2", "field": "text", "type": "string", "required": true, "description": "생성 프롬프트" },
      "seed": { "node": "5", "field": "seed", "type": "number", "default": -1 }
    }
  }
}
```

- `name`: 영문, 숫자, 하이픈, 언더스코어만 허용
- `resolver`: 문자열이면 resolver.mjs로 저장, `null`이면 기존 resolver 삭제, 생략하면 기존 유지

### delete — 패키지 삭제

```json
{ "action": "delete", "name": "my-workflow" }
```

## 새 워크플로우 등록 가이드

사용자가 ComfyUI API format JSON을 제공하면:

1. JSON의 노드 구조를 분석하여 주요 입력 파라미터를 식별한다
2. `params.json`의 `params` 필드에 각 파라미터의 `node`, `field`, `type`, `required`, `default`, `description`을 매핑한다
3. `features` 플래그를 설정한다:
   - `checkpoint_auto`: CheckpointLoaderSimple 노드가 있으면 `true`
   - `lora_injection`: LoRA를 동적으로 주입/교체하려면 `true`
   - `lora_couple_branches`: Attention Couple 좌/우 분리 워크플로우면 `true`
   - `seed_randomize`: 시드 파라미터가 있으면 `true`
   - `trigger_tags`: LoRA 트리거 태그 자동 삽입이 필요하면 `true`
4. `save` action으로 저장한다
5. `comfyui_generate`에서 `workflow: "my-workflow"`로 사용한다

## params.json과 resolver의 역할 분리

- 단순히 하나의 파라미터를 하나의 node/field에 매핑하는 경우에는 `params.json`만 사용하라.
- 여러 노드를 동시에 수정해야 하거나, 파라미터 값에 따라 조건 분기가 필요할 때만 `resolver.mjs`를 작성하라.
- `params.json`에 정의된 파라미터 중 `node`/`field`가 없는 항목은 resolver가 직접 소비하는 제어 파라미터로 사용할 수 있다.
- resolver는 강력하지만 유지보수 비용이 높다. 기본 매핑으로 충분한 경우 resolver를 만들지 마라.

## resolver.mjs 작성 가이드

기본 리졸버(params.json의 node+field 매핑)로 충분하지 않을 때만 작성한다.

```javascript
export default function resolve(workflow, params, context) {
  // context.defaultResolve — 기본 매핑을 먼저 적용하고 싶을 때
  const patched = context.defaultResolve(workflow, params, context);

  // context.sessionDir — 세션 디렉토리 경로
  // context.config — comfyui-config.json 내용
  // context.models — { checkpoints: [...], loras: [...] }

  // 커스텀 로직...
  return patched;
}
```

resolver에서 에러가 발생하면 이미지 생성 자체가 실패한다 (폴백 없음).

## features 플래그 상세

| 플래그 | 설명 | 해당 런타임 변환 |
|--------|------|-----------------|
| `checkpoint_auto` | CheckpointLoaderSimple의 ckpt_name을 사용 가능한 모델로 자동 교체 | 체크포인트 없는 워크플로우(후처리 등)는 false |
| `lora_injection` | base LoRA 주입 + 동적 LoRA override/injection + 프루닝 | LoRA를 쓰지 않는 워크플로우는 false |
| `lora_couple_branches` | scene-couple용 좌/우 CLIP 브랜치 LoRA 주입 | Attention Couple 워크플로우에서만 true |
| `seed_randomize` | seed=-1이면 랜덤 값으로 교체 | 시드 파라미터가 없으면 false |
| `trigger_tags` | 활성 LoRA의 트리거 태그를 프롬프트에 삽입 | LoRA trigger 자동 삽입이 불필요하면 false |
