---
name: supply-chain-compliance
category: cicd
description: "Supply Chain 컴플라이언스 가이드 — EU Cyber Resilience Act, SBOM 자동화, VEX, 중앙 저장소 아키텍처 Use when working with cicd 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Supply Chain 컴플라이언스 가이드

EU Cyber Resilience Act, SBOM 자동화, VEX, 중앙 저장소 아키텍처

## SBOM 자동화 & EU CRA 컴플라이언스

### EU Cyber Resilience Act (CRA) 요구사항

```
EU CRA 컴플라이언스 타임라인:
    |
    2024 ------> CRA 최종 승인
    |
    2025 ------> 전환 기간 시작
    |
    2026-2027 -> 의무화 시작
    |
    요구사항:
        +-- SBOM 제공 의무
        +-- 취약점 공개 의무 (24시간 내)
        +-- 보안 업데이트 제공 (5년+)
        +-- CE 마킹 요구
```

### SBOM 포맷 비교 상세

| 항목 | SPDX 3.0 | CycloneDX 1.6 |
|------|----------|---------------|
| **표준화** | ISO/IEC 5962:2021 | OWASP 표준 |
| **주요 용도** | 라이선스 컴플라이언스 | 보안/취약점 관리 |
| **VEX 지원** | 제한적 | 네이티브 |
| **Attestation** | 별도 | 내장 |
| **EU CRA** | 인정 | 인정 |
| **도구 생태계** | 넓음 | 보안 특화 |

### Syft SBOM 생성 자동화

```yaml
# .github/workflows/sbom-pipeline.yaml
name: SBOM Generation Pipeline

on:
  push:
    branches: [main]
  release:
    types: [published]

env:
  IMAGE: ghcr.io/${{ github.repository }}

jobs:
  build-and-sbom:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      packages: write
      id-token: write
      security-events: write

    steps:
      - uses: actions/checkout@v4

      - name: Build Image
        id: build
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: ${{ env.IMAGE }}:${{ github.sha }}

      # SPDX SBOM (라이선스 컴플라이언스)
      - name: Generate SPDX SBOM
        run: |
          syft packages ${{ env.IMAGE }}:${{ github.sha }} \
            -o spdx-json=sbom-spdx.json \
            --source-name="${{ github.repository }}" \
            --source-version="${{ github.sha }}"

      # CycloneDX SBOM (보안 분석)
      - name: Generate CycloneDX SBOM
        run: |
          syft packages ${{ env.IMAGE }}:${{ github.sha }} \
            -o cyclonedx-json=sbom-cyclonedx.json

      # SBOM 서명
      - name: Sign SBOM
        run: |
          cosign sign-blob --yes \
            --output-signature sbom-spdx.json.sig \
            --output-certificate sbom-spdx.json.crt \
            sbom-spdx.json

      # SBOM을 이미지에 첨부
      - name: Attach SBOM to Image
        run: |
          cosign attach sbom \
            --sbom sbom-spdx.json \
            ${{ env.IMAGE }}@${{ steps.build.outputs.digest }}

      # 취약점 스캔 (SBOM 기반)
      - name: Vulnerability Scan
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'sbom'
          scan-ref: 'sbom-cyclonedx.json'
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'

      # GitHub Security에 결과 업로드
      - name: Upload to Security Tab
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: 'trivy-results.sarif'

      # SBOM 아티팩트 저장
      - name: Upload SBOM Artifacts
        uses: actions/upload-artifact@v4
        with:
          name: sbom-${{ github.sha }}
          path: |
            sbom-spdx.json
            sbom-spdx.json.sig
            sbom-cyclonedx.json
          retention-days: 90

      # 릴리즈에 SBOM 첨부
      - name: Attach to Release
        if: github.event_name == 'release'
        uses: softprops/action-gh-release@v1
        with:
          files: |
            sbom-spdx.json
            sbom-cyclonedx.json
```

### SBOM 중앙 저장소

```yaml
# SBOM 저장소 구성
apiVersion: v1
kind: ConfigMap
metadata:
  name: sbom-config
  namespace: security
data:
  config.yaml: |
    storage:
      type: s3
      bucket: company-sbom-repository
      region: ap-northeast-2
      prefix: sboms/

    retention:
      days: 365  # EU CRA 요구사항

    indexing:
      # 빠른 검색을 위한 인덱싱
      fields:
        - name
        - version
        - purl
        - license
        - vulnerabilities

    notifications:
      # 새 취약점 발견 시 알림
      onVulnerability:
        slack: "#security-alerts"
        severity: ["critical", "high"]
```

### VEX (Vulnerability Exploitability eXchange)

```json
// vex-statement.json
{
  "@context": "https://openvex.dev/ns/v0.2.0",
  "@id": "https://example.com/vex/2024/001",
  "author": "security@example.com",
  "timestamp": "2024-01-15T10:00:00Z",
  "version": 1,
  "statements": [
    {
      "vulnerability": {
        "@id": "https://nvd.nist.gov/vuln/detail/CVE-2024-1234"
      },
      "products": [
        {
          "@id": "pkg:docker/myorg/myapp@1.0.0"
        }
      ],
      "status": "not_affected",
      "justification": "vulnerable_code_not_present",
      "statement": "이 취약점은 OpenSSL 3.0에 영향을 주지만, 우리 이미지는 1.1.1을 사용합니다."
    },
    {
      "vulnerability": {
        "@id": "https://nvd.nist.gov/vuln/detail/CVE-2024-5678"
      },
      "products": [
        {
          "@id": "pkg:docker/myorg/myapp@1.0.0"
        }
      ],
      "status": "fixed",
      "statement": "버전 1.0.1에서 수정됨"
    }
  ]
}
```

### SBOM 검증 정책

```yaml
# Kyverno SBOM 검증 정책
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-valid-sbom
spec:
  validationFailureAction: Enforce
  background: true
  rules:
    - name: check-sbom-exists
      match:
        any:
          - resources:
              kinds:
                - Pod
      verifyImages:
        - imageReferences:
            - "ghcr.io/myorg/*"
          attestations:
            - type: https://spdx.dev/Document
              attestors:
                - entries:
                    - keyless:
                        subject: "https://github.com/myorg/*"
                        issuer: "https://token.actions.githubusercontent.com"
              conditions:
                - all:
                    # SBOM이 최근 30일 이내 생성
                    - key: "{{ creationInfo.created }}"
                      operator: NotEquals
                      value: ""

    - name: check-critical-vulnerabilities
      match:
        any:
          - resources:
              kinds:
                - Pod
      verifyImages:
        - imageReferences:
            - "ghcr.io/myorg/*"
          attestations:
            - type: https://cosign.sigstore.dev/attestation/vuln/v1
              conditions:
                - all:
                    # Critical 취약점 없음
                    - key: "{{ scanner.result.criticalCount }}"
                      operator: Equals
                      value: 0
```

### 자동 SBOM 갱신 파이프라인

```yaml
# .github/workflows/sbom-refresh.yaml
name: SBOM Refresh

on:
  schedule:
    - cron: '0 0 * * *'  # 매일 자정
  workflow_dispatch:

jobs:
  refresh-sbom:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        image:
          - myorg/app-a:latest
          - myorg/app-b:latest
          - myorg/app-c:latest

    steps:
      - name: Generate Fresh SBOM
        run: |
          syft packages ${{ matrix.image }} \
            -o spdx-json=sbom.json

      - name: Scan for New Vulnerabilities
        run: |
          grype sbom:sbom.json \
            --output json \
            --file vulns.json

      - name: Check for Changes
        id: diff
        run: |
          # 이전 SBOM과 비교
          aws s3 cp s3://sbom-repo/${{ matrix.image }}/latest.json previous.json || true
          if ! diff -q sbom.json previous.json > /dev/null 2>&1; then
            echo "changed=true" >> $GITHUB_OUTPUT
          fi

      - name: Upload and Notify
        if: steps.diff.outputs.changed == 'true'
        run: |
          # 새 SBOM 업로드
          aws s3 cp sbom.json s3://sbom-repo/${{ matrix.image }}/latest.json

          # 슬랙 알림
          curl -X POST $SLACK_WEBHOOK \
            -H 'Content-type: application/json' \
            -d "{\"text\": \"SBOM updated for ${{ matrix.image }}\"}"
```

---

## SBOM 자동화 체크리스트

### 생성
- [ ] CI/CD에 Syft 통합
- [ ] SPDX + CycloneDX 양쪽 생성
- [ ] SBOM 서명 (Cosign)
- [ ] 이미지에 SBOM 첨부

### 저장
- [ ] 중앙 SBOM 저장소 구축
- [ ] 보존 기간 설정 (1년+)
- [ ] 버전별 SBOM 관리
- [ ] 검색 인덱싱

### 검증
- [ ] Kubernetes Admission 정책
- [ ] 취약점 스캔 연동
- [ ] VEX 문서 관리

### 컴플라이언스
- [ ] EU CRA 요구사항 검토
- [ ] 취약점 공개 프로세스
- [ ] 고객 SBOM 제공 절차

## Sources

- [DevSecOps Trends 2026](https://www.practical-devsecops.com/devsecops-trends-2026/)
- [Chainguard SLSA Guide](https://edu.chainguard.dev/compliance/slsa/what-is-slsa/)
- [EU Cyber Resilience Act](https://digital-strategy.ec.europa.eu/en/policies/cyber-resilience-act)
- [SBOM Guide](https://devdiligent.com/blog/future-open-source-security-devsecops-sbom-2026/)
- [OpenVEX](https://openvex.dev/)

## 참조 스킬

- `/supply-chain-security` - SLSA/Sigstore 기본 (SBOM 생성, 서명, Kubernetes 정책)
- `/k8s-security` - Kubernetes 보안
