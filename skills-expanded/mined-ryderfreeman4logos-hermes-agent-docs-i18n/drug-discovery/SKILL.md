---
name: drug-discovery
description: "Drug discovery: ChEMBL search, drug-likeness, interactions."
platforms: [linux, macos, windows]
version: 1.0.0
author: bennytimz
license: MIT
metadata:
  hermes:
    tags: [science, chemistry, pharmacology, research, health]
prerequisites:
  commands: [curl, python]
---

# 药物发现与制药研究

您是一位经验丰富的制药科学家和药物化学家，精通药物发现、化学生物学以及临床药理学领域。您可以将此技能应用于各类制药/化学研究任务中。

## 核心工作流程

### 1 — 生物活性化合物检索（ChEMBL）

通过靶点、活性或分子名称，在全球最大的开放生物活性数据库ChEMBL中检索相关化合物。无需API密钥即可使用。

```bash
# Search compounds by target name (e.g. "EGFR", "COX-2", "ACE")
TARGET="$1"
ENCODED=$(python -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$TARGET")
curl -s "https://www.ebi.ac.uk/chembl/api/data/target/search?q=${ENCODED}&format=json" \
  | python -c "
import json,sys
data=json.load(sys.stdin)
targets=data.get('targets',[])[:5]
for t in targets:
    print(f\"ChEMBL ID : {t.get('target_chembl_id')}\")
    print(f\"Name      : {t.get('pref_name')}\")
    print(f\"Type      : {t.get('target_type')}\")
    print()
"
```

```bash
# Get bioactivity data for a ChEMBL target ID
TARGET_ID="$1"   # e.g. CHEMBL203
curl -s "https://www.ebi.ac.uk/chembl/api/data/activity?target_chembl_id=${TARGET_ID}&pchembl_value__gte=6&limit=10&format=json" \
  | python -c "
import json,sys
data=json.load(sys.stdin)
acts=data.get('activities',[])
print(f'Found {len(acts)} activities (pChEMBL >= 6):')
for a in acts:
    print(f\"  Molecule: {a.get('molecule_chembl_id')}  |  {a.get('standard_type')}: {a.get('standard_value')} {a.get('standard_units')}  |  pChEMBL: {a.get('pchembl_value')}\")
"
```

```bash
# Look up a specific molecule by ChEMBL ID
MOL_ID="$1"   # e.g. CHEMBL25 (aspirin)
curl -s "https://www.ebi.ac.uk/chembl/api/data/molecule/${MOL_ID}?format=json" \
  | python -c "
import json,sys
m=json.load(sys.stdin)
props=m.get('molecule_properties',{}) or {}
print(f\"Name       : {m.get('pref_name','N/A')}\")
print(f\"SMILES     : {m.get('molecule_structures',{}).get('canonical_smiles','N/A') if m.get('molecule_structures') else 'N/A'}\")
print(f\"MW         : {props.get('full_mwt','N/A')} Da\")
print(f\"LogP       : {props.get('alogp','N/A')}\")
print(f\"HBD        : {props.get('hbd','N/A')}\")
print(f\"HBA        : {props.get('hba','N/A')}\")
print(f\"TPSA       : {props.get('psa','N/A')} Å²\")
print(f\"Ro5 violations: {props.get('num_ro5_violations','N/A')}\")
print(f\"QED        : {props.get('qed_weighted','N/A')}\")
"
```

### 2 — 药物相似度计算（Lipinski Ro5 + Veber）

无需安装 RDKit，即可利用 PubChem 的免费属性 API，根据既定的口服生物利用度标准对任意分子进行评估。

```bash
COMPOUND="$1"
ENCODED=$(python -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$COMPOUND")
curl -s "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/${ENCODED}/property/MolecularWeight,XLogP,HBondDonorCount,HBondAcceptorCount,RotatableBondCount,TPSA,InChIKey/JSON" \
  | python -c "
import json,sys
data=json.load(sys.stdin)
props=data['PropertyTable']['Properties'][0]
mw   = float(props.get('MolecularWeight', 0))
logp = float(props.get('XLogP', 0))
hbd  = int(props.get('HBondDonorCount', 0))
hba  = int(props.get('HBondAcceptorCount', 0))
rot  = int(props.get('RotatableBondCount', 0))
tpsa = float(props.get('TPSA', 0))
print('=== Lipinski Rule of Five (Ro5) ===')
print(f'  MW   {mw:.1f} Da    {\"✓\" if mw<=500 else \"✗ VIOLATION (>500)\"}')
print(f'  LogP {logp:.2f}       {\"✓\" if logp<=5 else \"✗ VIOLATION (>5)\"}')
print(f'  HBD  {hbd}           {\"✓\" if hbd<=5 else \"✗ VIOLATION (>5)\"}')
print(f'  HBA  {hba}           {\"✓\" if hba<=10 else \"✗ VIOLATION (>10)\"}')
viol = sum([mw>500, logp>5, hbd>5, hba>10])
print(f'  Violations: {viol}/4  {\"→ Likely orally bioavailable\" if viol<=1 else \"→ Poor oral bioavailability predicted\"}')
print()
print('=== Veber Oral Bioavailability Rules ===')
print(f'  TPSA         {tpsa:.1f} Å²   {\"✓\" if tpsa<=140 else \"✗ VIOLATION (>140)\"}')
print(f'  Rot. bonds   {rot}           {\"✓\" if rot<=10 else \"✗ VIOLATION (>10)\"}')
print(f'  Both rules met: {\"Yes → good oral absorption predicted\" if tpsa<=140 and rot<=10 else \"No → reduced oral absorption\"}')
"
```

### 3 — 药物相互作用与安全性查询（OpenFDA）

```bash
DRUG="$1"
ENCODED=$(python -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$DRUG")
curl -s "https://api.fda.gov/drug/label.json?search=drug_interactions:\"${ENCODED}\"&limit=3" \
  | python -c "
import json,sys
data=json.load(sys.stdin)
results=data.get('results',[])
if not results:
    print('No interaction data found in FDA labels.')
    sys.exit()
for r in results[:2]:
    brand=r.get('openfda',{}).get('brand_name',['Unknown'])[0]
    generic=r.get('openfda',{}).get('generic_name',['Unknown'])[0]
    interactions=r.get('drug_interactions',['N/A'])[0]
    print(f'--- {brand} ({generic}) ---')
    print(interactions[:800])
    print()
"
```

```bash
DRUG="$1"
ENCODED=$(python -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$DRUG")
curl -s "https://api.fda.gov/drug/event.json?search=patient.drug.medicinalproduct:\"${ENCODED}\"&count=patient.reaction.reactionmeddrapt.exact&limit=10" \
  | python -c "
import json,sys
data=json.load(sys.stdin)
results=data.get('results',[])
if not results:
    print('No adverse event data found.')
    sys.exit()
print(f'Top adverse events reported:')
for r in results[:10]:
    print(f\"  {r['count']:>5}x  {r['term']}\")
"
```

### 4 — PubChem化合物检索

```bash
COMPOUND="$1"
ENCODED=$(python -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$COMPOUND")
CID=$(curl -s "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/${ENCODED}/cids/TXT" | head -1 | tr -d '[:space:]')
echo "PubChem CID: $CID"
curl -s "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/${CID}/property/IsomericSMILES,InChIKey,IUPACName/JSON" \
  | python -c "
import json,sys
p=json.load(sys.stdin)['PropertyTable']['Properties'][0]
print(f\"IUPAC Name : {p.get('IUPACName','N/A')}\")
print(f\"SMILES     : {p.get('IsomericSMILES','N/A')}\")
print(f\"InChIKey   : {p.get('InChIKey','N/A')}\")
"
```

### 5 — 目标与疾病相关文献（OpenTargets）

```bash
GENE="$1"
curl -s -X POST "https://api.platform.opentargets.org/api/v4/graphql" \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"{ search(queryString: \\\"${GENE}\\\", entityNames: [\\\"target\\\"], page: {index: 0, size: 1}) { hits { id score object { ... on Target { id approvedSymbol approvedName associatedDiseases(page: {index: 0, size: 5}) { count rows { score disease { id name } } } } } } } }\"}" \
  | python -c "
import json,sys
data=json.load(sys.stdin)
hits=data.get('data',{}).get('search',{}).get('hits',[])
if not hits:
    print('Target not found.')
    sys.exit()
obj=hits[0]['object']
print(f\"Target: {obj.get('approvedSymbol')} — {obj.get('approvedName')}\")
assoc=obj.get('associatedDiseases',{})
print(f\"Associated with {assoc.get('count',0)} diseases. Top associations:\")
for row in assoc.get('rows',[]):
    print(f\"  Score {row['score']:.3f}  |  {row['disease']['name']}\")
"
```

## 推理指南

在分析药物相似性或分子特性时，应始终遵循以下步骤：

1. **首先列出原始数值** — 分子量、LogP值、HBD值、HBA值、TPSA值以及旋转键数
2. **应用规则集** — 在适用情况下使用Ro5（Lipinski规则）、Veber规则及Ghose过滤器
3. **标记潜在风险点** — 代谢热点区域、hERG基因风险，以及可能影响中枢神经系统渗透的高TPSA值
4. **提出优化建议** — 如生物等效替代、前药策略或环结构截断等方案
5. **注明数据来源API** — ChEMBL、PubChem、OpenFDA或OpenTargets

针对ADMET相关问题，需系统地从吸收、分布、代谢、排泄和毒性五个方面进行分析。详细指导可参阅参考文档/ADMET_REFERENCE.md。

## 重要说明

- 所有API均为免费且公开可用，无需身份验证
- ChEMBL存在调用频率限制：批量请求之间需添加1秒的间隔
- FDA数据库中的数据仅反映已报告的不良事件，不必然代表因果关系
- 对于临床决策，始终建议咨询持证药剂师或医生

## 快速参考表

| 任务 | API | 接口地址 |
|------|-----|----------|
| 查找靶点 | ChEMBL | `/api/data/target/search?q=` |
| 获取生物活性数据 | ChEMBL | `/api/data/activity?target_chembl_id=` |
| 分子特性分析 | PubChem | `/rest/pug/compound/name/{name}/property/` |
| 药物相互作用查询 | OpenFDA | `/drug/label.json?search=drug_interactions:` |
| 不良事件查询 | OpenFDA | `/drug/event.json?search=...&count=reaction` |
| 基因与疾病关联查询 | OpenTargets | GraphQL POST `/api/v4/graphql` |
