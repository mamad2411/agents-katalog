---
name: sole-search
description: '운영 중인 소상공인(가게·점포·자영업자)을 위한 지원사업 조사 스킬. 소상공인24·기업마당 공고를 전수 수집하고 가게 프로필(업종·지역·업력·직원수·매출)로 자격을 판정해 "오늘 신청할 것"부터 보고한다. 보조금·바우처, 정책자금(대출·보증), 교육·컨설팅 전 범위. 사용자가 "우리 가게 지원사업", "소상공인 지원금", "정책자금 알아봐줘", "가게 시설개선 지원", "사장님 지원 뭐 있어", "소상공인24 조사", "폐업/재기 지원" 등을 요청하면 이 스킬을 사용한다. 재조사("새로 나온 거 있나", "지난번 이후 뭐 올라왔나")는 diff 모드로 사용. 반대로 "우리 아이템", "창업지원", "예비창업", "K-Startup", "TIPS", "R&D 과제", "입주공간", "액셀러레이팅" 등 아이템·프로젝트 기반 창업지원 탐색은 이 스킬이 아니라 ir-search를 사용한다. 신호가 섞이면(예: "온라인 셀러 지원금") 어느 쪽인지 한 번 묻는다. 사용자 신분보다 요청 목적이 우선이다 — 가게 사장이라도 신규 기술 아이템 R&D를 찾으면 ir-search. 한국 전용.'
---

# sole-search — 소상공인 지원사업 조사

> **스크립트 위치**: `${CLAUDE_PLUGIN_ROOT}/skills/sole-search/scripts/` (단독 스킬 설치 시 스킬 디렉토리 자체). 미정의 시 폴백: `~/.claude/skills/sole-search/scripts/`. 아래 명령의 경로 변수를 환경에 맞게 치환해 실행한다.

이 스킬은 "룰베이스 수집 + LLM 판정" 구조다. 스크립트는 공고를 기계적으로 수집만 하고,
선별·자격 판정·보고서는 에이전트(너)가 한다.

세 가지 원칙 (위반 금지):

1. **조용한 누락 금지** — 커버하지 못한 소스·읽지 못한 첨부는 보고서에 명시한다. 모든 보고서에 coverage_manifest가 있어야 한다.
2. **추정 금지** — 공고 원문에 없는 것은 '불명'. 첨부를 읽지 못했으면 `확인됨` 판정 금지.
3. **허위신청 유도 금지** — "변형하면 가능" 식 프레이밍을 쓰지 않는다. 실제 등록업종·영업내용이 뒷받침되는 것만 후보다.

## 0단계 — 프로필

**먼저 현재 작업 폴더에서 `sole-profile.md`를 찾는다.** 있으면 본문 요약을 보여주고
"바뀐 것 있나요?" **한 번만** 묻고 1단계로 간다.

없으면 쉬운 말로, 관공서 용어 없이, **한 번에** 묻는다 (이미 대화·폴더에서 파악된 항목은 제외):

1. 무슨 장사/사업을 하세요? (예: 치킨집, 네일샵, 스마트스토어)
2. 개인사업자세요, 법인이세요? 지금 정상 영업 중이세요?
3. 가게는 어느 동네예요? (시·군·구까지. 사업자등록상 주소가 다르면 둘 다)
4. 사업자 등록은 언제 하셨어요? (년·월)
5. 직원은 몇 명이에요? (4대보험 가입 기준과, 가족·알바 포함 인원을 구분해서)
6. 혹시 소상공인확인서(중소기업현황정보시스템 발급) 있으세요? 유효기간은?
7. (확인서 없으면) 작년 매출이 대략 어느 정도예요? — 3천만 미만 / 3천만~1억 / 1억~5억 / 5억~10억 / 10억~30억 / 30억 이상
8. 대표님 나이대와 성별은? (건너뛰어도 됨)
9. 지금 제일 필요한 건? (복수) — 안 갚는 돈 / 빌리는 돈 / 가게 시설 / 온라인 판매 / 홍보 / 배우기 / 정리·재기

확정되면 `sole-profile.md`로 저장한다. **YAML 프론트매터는 원자 필드**로 쓴다:

```markdown
---
schema_version: 1
type: sole-search-profile
entity_type: individual | corporation
business_status: active | suspended | closing | closed
closure_date: YYYY-MM            # closed일 때만
industry_text: <사용자 표현 그대로>
industry_code_candidates:
  - {code: <KSIC>, label: <업종명>, confidence: high|medium|low}
registration_date: YYYY-MM
regular_employee_count: <N>      # 4대보험 기준
headcount: <N>                   # 가족·알바 포함
employee_count_as_of: YYYY-MM-DD
sbiz_certificate: none | valid | expired
sbiz_certificate_valid_until: YYYY-MM-DD
sales_band: lt_30m | 30m_100m | 100m_500m | 500m_1b | 1b_3b | gte_3b
sales_period: <YYYY 연간>
sales_basis: statutory_average | recent_year_proxy
sales_vs_industry_threshold: below | near | above | unknown
threshold_industry_code: <KSIC>
sales_threshold_as_of: YYYY-MM-DD
province: <시/도>
district: <시/군/구>
hq_district: <본점, 다를 때만>
owner_age_band: 20s|30s|40s|50s|60s_plus|unspecified
owner_gender: female | male | unspecified
needs: [grant, loan, facility, online_sales, marketing, education, recovery]
last_survey_at: YYYY-MM-DD
last_survey_dir: <보고서 폴더>
survey_sources: [sbiz24, sbiz24_combine, bizinfo, fanfandaero]  # 서울이면 + seoulshinbo, API 키 등록 시 + gov24
---
# sole-search 프로필
<사람이 읽는 한 줄 요약>
```

**소상공인 법적 판정 우선순위**: ① 유효한 소상공인확인서 → 확정 ② 법령상 기준기간
평균매출액(statutory_average) 근거가 있으면 상시근로자 기준(업종별 5인/10인 미만)과
평균매출액 기준을 함께 판정 ③ **최근 1년 근사치(recent_year_proxy)만 있으면 below라도
법적 지위는 '확인 필요'** — 이전 연도 매출 때문에 법령상 평균이 기준을 넘을 수 있다.

**개인정보 최소화**: 세금 체납·대출액·신용점수는 묻지 않는다. 정책자금 후보가 나온 뒤
"이 요건 해당되세요?"로만 확인하고, 답을 프로필에 저장하지 않는다. 출생연월도 저장하지 않는다.

## 0.5단계 — 조사 범위 명시 선택

실제 수집 전에 범위 계획기를 실행해 사용자 선택과 커버리지 한계를 고정한다. 계획기는
Python 표준 라이브러리만 사용하고 **네트워크·LLM을 호출하지 않으므로 모델 토큰은 0**이다.

```bash
# 빠른 확인: 소상공인24만
python3 "${CLAUDE_PLUGIN_ROOT}/skills/sole-search/scripts/scope_plan.py" \
    --preset quick -o scope-plan.json

# 특정 출처 하나만
python3 "${CLAUDE_PLUGIN_ROOT}/skills/sole-search/scripts/scope_plan.py" \
    --preset focused --source sbiz24 -o scope-plan.json

# 프로필 기반 권장 범위
python3 "${CLAUDE_PLUGIN_ROOT}/skills/sole-search/scripts/scope_plan.py" \
    --preset recommended --need loan --need online_sales \
    --province 서울 -o scope-plan.json

# 사용자가 고른 출처만. 자동 어댑터가 없는 출처는 manual_only로 남는다.
python3 "${CLAUDE_PLUGIN_ROOT}/skills/sole-search/scripts/scope_plan.py" \
    --preset custom --source sbiz24 --source work24 -o scope-plan.json
```

- `quick`: 소상공인24 하나만 빠르게 본다.
- `focused`: `--source`로 지정한 정확히 한 출처만 본다.
- `recommended`: 업종·필요·지역·보유 credential에 맞는 등록 출처를 추천한다.
- `all_registered`: 현재 저장소에 검증된 자동 어댑터 또는 명시된 수동 계약이 있는 출처를
  전부 계획한다. 후보 출처를 자동으로 승격하지 않는다.
- `all_known`: 등록 출처와 프로필 확장 후보를 모두 계획하되 후보는 `manual_only`로
  유지한다. 자동 수집 전체가 아니다.
- `custom`: 사용자가 지정한 출처만 계획한다. 후보 출처는 선택돼도 수동 확인이다.

`scope-plan.json`의 모든 출처 상태(`selected / omitted_by_user / not_applicable`,
`ready / manual_only / unavailable_credential`)와 요청 수·시간 추정을 먼저 보여준다.
보고서에는 `scope_fingerprint`와 "선택 범위 기준" 커버리지를 기록한다. 재조사는 직전과
fingerprint가 같을 때만 GONE·UNCHANGED 승계를 허용한다. fingerprint가 다르면 출처 제외를
GONE으로 오판하지 말고 범위 변경으로 표시해 전체 재판정한다. 후보·수동 출처 목록과 등록
조건은 `references/sources.md`를 따른다.

## 재조사 (diff 모드)

프로필의 `last_survey_dir`가 있으면 전수 재검토 대신 증분 조사:

1. **직전과 같은 소스 구성으로** 1단계 크롤링을 그대로 실행 (새 보고서 폴더에)
2. 비교:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/sole-search/scripts/diff_surveys.py" \
       <직전_폴더> <새_폴더> --out new_items.jsonl \
       --old-profile <직전_폴더>/profile-snapshot.md --new-profile sole-profile.md \
       --incremental-sources fanfandaero,seoulshinbo
   ```
   `--incremental-sources`에는 `--since` 컷오프로 수집한 소스를 넣는다 — 그 소스는
   이전 레코드 부재가 소멸이 아니므로 GONE을 계산하지 않는다
3. 검토·상세검증은 `new_items.jsonl`(NEW+CHANGED+NEEDS_REHASH)만. GONE은 **별도 파일
   `gone_new_items.jsonl`**에 기록된다(기회 소멸 알림 재료 — 검토 대상과 섞지 않는다).
   UNCHANGED는 직전 판정 승계. 단 **프로필 fingerprint가 바뀌었다는 WARNING이 나오면 전체 재판정**
4. **NEEDS_REHASH** = 직전 조사에 content_hash가 있었는데 새 목록엔 아직 없음. 목록 필드만으로
   같아 보여도 본문·첨부가 바뀌었을 수 있으니 **상세 재수집(`detail --merge-into`) 후 해시를
   채우고 재비교**한다 — 그때 같으면 승계, 다르면 변경 처리. **hash_version이 다른 경우**(해시
   산식 v1↔v2)는 값 비교가 불가능하므로 1회 CHANGED로 분류된다 — 상세 재검증하면 이번
   조사부터 양쪽 v2로 수렴한다
5. **정책자금(loan) 전체와 직전 `확인됨` 항목은 diff 결과와 무관하게 접수상태를 재확인**
6. 보고서: 신규 / 변경(마감·조건 — changed_fields 표기) / 소멸된 확인됨 항목(기회 소멸 알림) / 승계 요약.
   WARNING(미갱신 소스)은 coverage_manifest에 "미갱신" 명시

## 1단계 — 수집

```bash
mkdir -p survey-$(date +%Y%m%d)/details && cd survey-$(date +%Y%m%d)

# 소상공인24: 소진공 공고 + 통합조회(지자체·유관기관 포함) — 필수
python3 "${CLAUDE_PLUGIN_ROOT}/skills/sole-search/scripts/sbiz_crawl.py" list all -o sbiz24.jsonl

# 기업마당: 모집중 전체 전 페이지 (~96p, 2~3분) — 필수
python3 "${CLAUDE_PLUGIN_ROOT}/skills/sole-search/scripts/sources_crawl.py" list -o bizinfo.jsonl

# 판판대로: 온라인판로 사업목록 + 세부·수시 모집공고 게시판 — 권장
#   (--since: 첫 조사는 1년 전, 재조사는 직전 조사일)
python3 "${CLAUDE_PLUGIN_ROOT}/skills/sole-search/scripts/region_crawl.py" list fanfan \
    -o fanfandaero.jsonl --since <YYYY-MM-DD>

# 서울신보: 프로필 province가 서울일 때만 — 권장 (서울시 사업 공고 원출처)
python3 "${CLAUDE_PLUGIN_ROOT}/skills/sole-search/scripts/region_crawl.py" list seoulshinbo \
    -o seoulshinbo.jsonl --since <YYYY-MM-DD>

# 보조금24: 선택 소스 (API 키 등록 시에만 — 상시 수혜 제도 커버)
python3 "${CLAUDE_PLUGIN_ROOT}/skills/sole-search/scripts/gov24_crawl.py" list \
    -o gov24.jsonl --filter-target 소상공인

# 프로필 스냅샷 (필수, 수집 직후) — 다음 diff의 --old-profile 재료
cp ../sole-profile.md profile-snapshot.md
```

게시판형 소스(판판대로 공지·서울신보)는 접수기간이 목록에 없어 status가 `불명`으로
수집된다 — 선별에서 제목·게시일로 1차 거르고, candidate는 상세에서 접수 여부를 확인한다.
`--since` 컷오프를 쓴 조사는 coverage_manifest에 컷오프 날짜를 명시한다 (전수 아님을 표기).

**보조금24는 선택 소스**: 종료 코드 4(미활성)면 coverage_manifest에
`미활성(선택 소스, API 키 미등록)`으로 기록하고 보고서 한계에 활성화 방법
(data.go.kr 15113968 활용신청 → `DATA_GO_KR_API_KEY` 또는 `~/.config/sole-search/api_key`)을
한 줄 안내한다. 활성 시 상시 제도는 보고서에 **"상시 혜택(보조금24)" 별도 섹션**으로
다룬다 — 마감 기준 정렬인 "오늘 신청할 것"과 섞지 않는다. 키를 프로필·보고서 폴더에
저장하지 않는다.

stderr의 `TOTAL/COLLECTED/DUPLICATES`·`PAGES/CRAWLED`를 기록한다 — coverage_manifest 재료다.
종료 코드 2는 부분 수집(partial)이다. **소스별 계약·수동확인 절차는 `references/sources.md`**,
지역신보·지자체 포털은 `references/region-registry.md` 참조.

**중복 제거**: ① `(발행기관, 공고번호)` ② 정규화 canonical URL — 특히 sbiz24_combine의
`PBLN_*` ID는 bizinfo의 pblancId와 같은 공고다 ③ 제목+기관+접수기간 전부 일치.
애매하면 삭제하지 말고 묶어서 "동일 사업 추정 N건"으로 표기.

## 1.5단계 — 전수 선별 (screening)

100% 수집해도 일부만 읽으면 전수조사가 아니다:

- 수집된 **모든** 레코드를 배치(예: 100건씩)로 나눠 빠짐없이 읽는다. 제목 키워드로 자동 제외 금지
- 각 레코드에 `screening: candidate | excluded | needs_detail` + 제외 사유를 붙여 `screening.jsonl`로 저장
- 프로필의 needs·업종·지역과 명백히 무관해도 "excluded + 사유"로 기록하고 넘어간다 (조용히 버리지 않는다)
- 중단되면 어디까지 검토했는지 기록하고 coverage를 partial로 보고
- **모델 분기(비용 최적화)**: 선별은 거친 1차 통과라 서브에이전트를 **저비용 모델**(Claude Code면
  `model: haiku`)로 돌려도 된다 — 실수는 2단계 판정에서 걸러진다. 단 방향이 중요하다:
  **애매하면 excluded가 아니라 `candidate`/`needs_detail`로** (과소 선별은 2단계가 못 되살린다).
  2단계 자격 판정은 원문·첨부 해석이 필요하므로 세션 기본 모델을 유지한다

## 2단계 — 자격 판정

candidate와 needs_detail 레코드는 상세 원문을 확인한다:

```bash
# 소상공인24 상세+첨부 (첨부 자동 다운로드 + 목록 jsonl에 content_hash 병합)
python3 "${CLAUDE_PLUGIN_ROOT}/skills/sole-search/scripts/sbiz_crawl.py" detail <pbancSn> \
    --download-dir details -o details/<pbancSn>.json --merge-into sbiz24.jsonl
# 기업마당 상세 (본문 해시 v2·첨부 링크를 목록에 병합 — 레코드에 hash_version: 2)
#   --download-dir details 를 붙이면 첨부까지 다운로드·추출하고, 전부 성공 시
#   해시 v3(본문+정렬된 첨부 sha256, hash_version: 3)를 스탬프한다 — v2↔v3 전환은
#   diff가 1회 CHANGED로 흡수. 첨부 일부가 실패·생략되면 본문만의 v2 해시를 유지하고
#   attachments_complete: false + exit 2로 첨부 미검증을 표현한다
python3 "${CLAUDE_PLUGIN_ROOT}/skills/sole-search/scripts/sources_crawl.py" detail "<URL>" \
    -o details --merge-into bizinfo.jsonl
# 판판대로·서울신보 상세 (canonical_url로 소스 자동 판별, 소스별 jsonl에 병합)
#   --download-dir details 를 붙이면 첨부까지 다운로드·추출한다 (bizinfo와 동일 계약:
#   전부 성공 시 hash v3, 일부 실패·생략 시 본문 v2 유지 + attachments_complete: false
#   + exit 2). 서울신보는 연속 다운로드 시 서버가 http 리다이렉트로 막는 경우가 있다 —
#   blocked_redirect로 남으면 재실행하거나 수동 확인
python3 "${CLAUDE_PLUGIN_ROOT}/skills/sole-search/scripts/region_crawl.py" detail \
    "<canonical_url>" -o details --merge-into <해당소스>.jsonl [--download-dir details]
# 첨부 텍스트 추출 (HWP는 hwp5txt→PrvText 미리보기 폴백 — 부분 추출/실패 후보는 '확인 필요')
python3 "${CLAUDE_PLUGIN_ROOT}/skills/sole-search/scripts/attach_extract.py" \
    details/<파일> -o details/<파일>.txt
```

**sbiz24_combine 레코드의 상세 분기** (계약: references/sources.md §1):
- ID가 `PBLN_*` → 기업마당 공고 — `sources_crawl.py detail <bizinfo URL>`로 검증
- 비PBLN·비대출(`raw.pbancGubun`이 A(공단)/D(지방정부)) → `sbiz_crawl.py detail <sn>
  --source sbiz24_combine --merge-into sbiz24.jsonl` — pbanc 상세 API를 공유한다
  (2026-07-23 실호출 검증). **--merge-into 필수**: 목록 레코드의 pbancGubun 게이트 +
  상세 응답 sn·제목 대조를 통과해야 병합한다(불일치 시 exit 2, 조용한 오독 금지)
- `raw.pbancGubun`이 C(대출상품)·미지 코드·부재(구버전 목록) → 별도 네임스페이스/계약
  미확인이라 exit 2로 거부(fail-closed) — canonical_url로 수동 확인.
  bizType=`대출상품` 문자열도 보조 검사로 거부된다

판정 상태 5단계:

| 상태 | 의미 |
|---|---|
| `확인됨` | 공고 원문(첨부 포함)에서 모든 필수 신청자격 충족 확인 |
| `조건부` | 구체 요건 충족 시 가능 (예: 교육 이수 후) — 요건 명시 |
| `확인 필요` | 프로필 또는 원문 부족 — 부족한 항목 명시 |
| `신청 불가` | 필수요건 불충족 — 근거 문구 인용 |
| `사업전환 후보` | 실제 사업전환 전제 — 별도 섹션, 기본 비표시 |

검증 축: 업종 제한(제외 업종), 업력(공고 기준일로 산정), 상시근로자 수, 매출액 기준,
소재지(본점/사업장 구분), 기수혜 제외, 영업상태.

규칙:
- **판정 상태는 위 5개 중 정확히 하나** — '정보성', '조건부/확인 필요' 같은 비표준·복합 상태 금지.
  직접 신청 대상이 아닌 통합·메타 공고는 선별 단계에서 `excluded`(사유: 메타 공고, 세부공고로 신청) 처리
- **접수 마감이 확정된 후보는 상세검증을 생략할 수 있다** — 단 보고서에 건수·대표 목록·
  "차기 재조사 우선확인 대상"을 명시한다 (조용한 생략 금지)
- **첨부를 읽지 못한 후보(`attachments_complete: false` 포함)는 `확인됨` 금지** → `확인 필요` + "첨부 미확인(사유)".
  HWP의 PrvText 미리보기 추출(`extract_reason: hwp_preview_only`)은 **부분 추출**이라 여기에 해당한다
- **status가 `불명`인 레코드는 접수 여부부터 상세에서 확인** — 크롤러는 낙관 추정하지 않는다
- 크롤러 종료 코드 3(MANUAL)은 차단 신호다 — 재시도하지 말고 해당 소스를 manual로 기록
- 각 판정에 근거 출처(문서·문구)를 기록
- `확인됨` = 공고상 신청자격 확인일 뿐, 선정·대출심사 통과 예측이 아님 — 보고서에 명시
- 연락처는 `contacts: [{kind: phone|email|url, value}]`, 없으면 "연락처 미기재"
- 유형은 `primary_type`(grant|loan|advisory) + tags. loan에는 한도·금리(기준일)·기간·
  거치·상환방식·보증기관을 채우고, 회차 접수상태는 sources.md의 수동확인 절차를 따른다

## 3단계 — 보고서

`survey-YYYYMMDD/report.md`. 사장님이 읽는 문서 — 관공서 용어에 괄호 해설. 구조:

1. **오늘 신청할 것** — 전 유형 통합 `확인됨` 목록. 정렬: 마감 D-day 오름차순 →
   예산소진 시까지("서두르세요") → 상시 → 회차예정(예정일). 각 항목: 제목, 한 줄 요약,
   금액/혜택, 마감, 신청 방법·링크, 연락처. `확인됨` 목록 **뒤에** 남은 조건이 1개뿐인
   `조건부`를 별도 하위 목록(🔶 "조건 1개만 채우면 됨")으로 붙일 수 있다 — 확인됨과
   섞지 말고, 각 항목 첫 줄에 남은 조건을 명시하며, 정렬 규칙은 동일 적용
2. **coverage_manifest** — 소스별 `collection_status`와 `screening_status`
   (`success|partial|failed|manual`), collected/screened/candidate/detail_verified 카운트.
   **카운트는 소스별로 기재 — "(합산)" 뭉개기 금지**. 중복 제거 시 어느 소스에 귀속했는지
   설명해 수집→선별 합계가 재검산 가능해야 한다. partial·manual·미갱신은 사유 명시.
   **partial인 소스를 "전수 수집 완료"로 표현 금지**. 미커버 영역(미등록 지자체 포털 등) 한계 고지
3. **유형별 상세** — 💰 받는 돈 / 🏦 빌리는 돈 / 🎓 배우고 돕기 순, 각 유형 안에서 판정 상태순.
   🏦에는 "갚아야 하는 돈입니다" 문구 + 한도·금리(기준일)·기간·취급기관 필수
4. **사업전환 후보** — 해당 시에만. 그 외 부가 정보(공통 준비물, 마감 후보 목록 등)는
   번호 없는 "비고"로 붙인다

**보고서 자가 점검** — 작성 직후 아래를 전부 확인하고, 어긋난 항목은 고친 뒤 완료 선언:

- 판정 상태에 5개 enum 외 값·복합 표기 없음 (항목당 정확히 하나)
- "오늘 신청할 것"에서 확인됨/🔶조건부가 구분돼 있고 정렬 규칙(D-day 오름차순 → 예산소진 → 상시 → 회차예정) 준수
- coverage_manifest 카운트가 소스별로 채워져 있고 수집→선별 합계가 재검산됨
- 첨부 미추출 항목 전부가 상세 표에 `확인 필요`로 존재 (coverage 언급과 상세 표 판정 일치)
- `확인 필요` 판정에 "실무상 문제 가능성 낮음" 류의 추정 보완 문구 없음 — 부족한 항목과 확인 방법만 적는다
- 사장님용 본문에 내부 식별자(idx, candidate, needs_detail 등) 노출 최소화 — 감사 정보는 산출 파일에 있다

완료 후 프로필의 `last_survey_at`·`last_survey_dir`를 갱신하고, **갱신된 현재
`sole-profile.md`를 조사 폴더에 `profile-snapshot.md`로 복사(cp)한다** (필수 —
다음 diff의 `--old-profile` 재료, 1단계에서 만든 스냅샷을 덮어써 최종본으로 남긴다).

## 중단선

403·CAPTCHA·로그인 요구를 만나면 우회(TLS 지문 변경, 내부 API 반복 재시도)하지 않는다.
해당 소스를 manual로 전환하고 sources.md의 수동확인 절차를 보고서에 첨부한다.
