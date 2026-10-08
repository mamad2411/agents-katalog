# add-gateway-client

Toonkit-Ray-Head의 테스트 클라이언트를 참고하여 Global Gateway에 새 모델 클라이언트를 추가하는 skill입니다.

## 워크플로우

### Phase 1: 준비 및 모델 선택

1. **참조 테스트 파일 확인**
   - 사용자에게 추가할 모델명 질문
   - `Toonkit-Ray-Head/client/test_{model_name}.py` 파일 존재 여부 확인
   - 없으면 참조할 파일 경로 직접 입력받기

2. **참조 파일 분석**
   - 테스트 파일에서 다음 정보 추출:
     - 모델 파라미터 (prompt, image_path, lora_path 등)
     - 테스트 데이터 (TEST_PAIRS, TEST_CASES 등)
     - 기본값 (DEFAULT_* 상수들)

3. **기존 inputs 구조 파악**
   - `client/inputs/base.py` - BaseModelInput 클래스 확인
   - `client/inputs/__init__.py` - export 패턴 확인
   - 기존 모델 입력 파일 (sam2.py, inpaint.py 등) 참고

### Phase 2: 작업 계획 수립

4. **서버 스키마 MODEL_NAME 확인**
   - `src/toonkit_ml_global_gateway/model_schemas/` 에서 해당 모델 스키마 파일 확인
   - 없으면 submodule에서 복사:
     ```bash
     cp submodules/toonkit-ray-worker/src/kuberay_worker/schemas/*.py \
        src/toonkit_ml_global_gateway/model_schemas/
     ```
   - `MODEL_NAME` 값 확인:
     ```bash
     grep "MODEL_NAME" src/toonkit_ml_global_gateway/model_schemas/{model_name}.py
     ```
   - **사용자에게 `model_name()` 반환값 확인 필수** (서버 스키마와 일치해야 함)
     - 예: 파일명은 `fluxkleini2i.py`이지만 `MODEL_NAME = "flux_klein_i2i"`일 수 있음

5. **작업 계획 생성**
   - 수집한 정보를 바탕으로 구체적인 작업 계획 작성
   - 사용자에게 다음 사항 확인:
     - **API용 모델명 (`model_name()` 반환값)** - 서버 스키마 MODEL_NAME과 동일해야 함
     - Input 클래스명 확인 (예: `ZImageInput`, `FluxKleinI2IInput`)
     - 테스트 데이터 구성 방식 (단일 DUMMY vs 여러 페어)
     - 기본 bucket 설정
   - 계획 승인 받기

### Phase 3: 코드 작성

5. **Input 클래스 파일 생성**
   - `client/inputs/{model_name}.py` 파일 생성
   - 포함 내용:
     ```python
     @dataclass
     class {ModelName}Input(BaseModelInput):
         # 필드 정의 (참조 파일 기반)

         @classmethod
         def model_name(cls) -> str:
             return "{model_name}"

         def preprocess(self) -> None:
             # 입력 검증 로직

         def postprocess(self, result: dict) -> dict:
             result["_model"] = self.model_name()
             return result

     # DUMMY 테스트 데이터
     DUMMY_{MODEL_NAME} = {ModelName}Input(...)
     ```

6. **__init__.py 업데이트**
   - `client/inputs/__init__.py`에 새 모델 import/export 추가
   ```python
   from .{model_name} import (
       DUMMY_{MODEL_NAME},
       {ModelName}Input,
   )

   __all__ = [
       ...
       # {ModelName}
       "{ModelName}Input",
       "DUMMY_{MODEL_NAME}",
   ]
   ```

7. **test_infer.py 업데이트**
   - import 문에 새 모델 추가
   - 테스트 클래스 추가:
     ```python
     class Test{ModelName}:
         def test_{model_name}_async_mode(self, client):
             result = client.infer(DUMMY_{MODEL_NAME}, async_mode=True)
             assert "job_id" in result
             assert "status" in result

         def test_{model_name}_preprocess_validation(self):
             # 입력 검증 테스트
     ```
   - CLI 함수 추가: `run_{model_name}_tests()`
   - argparse choices에 모델명 추가
   - docstring에 사용 예시 추가

### Phase 4: 완료 확인

8. **변경 파일 목록 출력**
   ```
   client/inputs/{model_name}.py      (신규)
   client/inputs/__init__.py          (수정)
   client/test_infer.py               (수정)
   ```

9. **테스트 실행 안내**
   ```bash
   # pytest로 실행
   pytest test_infer.py -v -k {model_name}

   # CLI로 실행
   python test_infer.py --model {model_name}
   ```

10. **커밋 여부 질문** (선택적)

## 파일 구조

```
Toonkit-ML-Global-Gateway/
├── client/
│   ├── inputs/
│   │   ├── __init__.py           # export 추가
│   │   ├── base.py               # 참고: BaseModelInput
│   │   ├── sam2.py               # 참고: 기존 모델 패턴
│   │   └── {model_name}.py       # 신규: Input 클래스 + DUMMY 데이터
│   ├── test_infer.py             # 수정: 테스트 클래스 + CLI 함수 추가
│   └── gateway_client.py         # 참고: infer() 메서드 사용법

Toonkit-Ray-Head/                   # 참조용
├── client/
│   └── test_{model_name}.py       # 참고: 테스트 데이터 및 파라미터
```

## 사용 예시

```
/add-gateway-client
```

또는 모델명을 직접 지정:
```
/add-gateway-client zimage
/add-gateway-client fluxkleini2i
```

## 주의사항

- 모델 이름은 소문자 사용 (예: `zimage`, `fluxkleini2i`)
- Input 클래스명은 PascalCase + Input 접미사 (예: `ZImageInput`)
- DUMMY 데이터명은 대문자 + 언더스코어 (예: `DUMMY_ZIMAGE`)
- 참조 파일의 테스트 데이터 구조를 최대한 유지
- `_today()` 함수로 upload_path에 날짜 prefix 추가
- bucket 기본값은 `toonkit-dev-assets-bucket` 또는 `toonkit-prod-assets-bucket`

### 모델명 일치 확인 (중요!)

**클라이언트의 `model_name()`과 서버 스키마의 `MODEL_NAME`이 반드시 일치해야 합니다.**

1. **서버 스키마 위치**: `src/toonkit_ml_global_gateway/model_schemas/{model_name}.py`
2. **스키마 원본**: `submodules/toonkit-ray-worker/src/kuberay_worker/schemas/`

로컬에서 테스트하기 전에 submodule의 스키마를 복사해야 합니다:
```bash
cp submodules/toonkit-ray-worker/src/kuberay_worker/schemas/*.py \
   src/toonkit_ml_global_gateway/model_schemas/
```

**MODEL_NAME 확인 방법:**
```bash
grep "MODEL_NAME" src/toonkit_ml_global_gateway/model_schemas/{model_name}.py
```

클라이언트의 `model_name()` 반환값과 일치하지 않으면 `Unknown model` 에러가 발생합니다.

## Input 클래스 필수 구현 사항

1. **필드 정의**: 참조 파일의 파라미터를 dataclass 필드로 정의
2. **model_name()**: API 라우팅용 모델명 반환
3. **preprocess()**: 입력 검증 (빈 값, 음수 값 등 체크)
4. **postprocess()**: 응답에 `_model` 필드 추가

## 테스트 데이터 패턴

### 단일 DUMMY (간단한 경우)
```python
DUMMY_{MODEL_NAME} = {ModelName}Input(
    param1="value1",
    param2="value2",
    upload_path=f"temp_jjy/{_today()}-{model_name}_output.png",
)
```

### 여러 페어 (LoRA 등 여러 조합 테스트)
```python
DUMMY_{MODEL_NAME}_PAIR1 = {ModelName}Input(...)
DUMMY_{MODEL_NAME}_PAIR2 = {ModelName}Input(...)
DUMMY_{MODEL_NAME}_PAIR3 = {ModelName}Input(...)

{MODEL_NAME}_TEST_PAIRS = [
    ("pair1", DUMMY_{MODEL_NAME}_PAIR1),
    ("pair2", DUMMY_{MODEL_NAME}_PAIR2),
    ("pair3", DUMMY_{MODEL_NAME}_PAIR3),
]

# pytest parametrize용
@pytest.mark.parametrize("name,input_data", {MODEL_NAME}_TEST_PAIRS)
def test_{model_name}_pairs(self, client, name, input_data):
    ...
```
