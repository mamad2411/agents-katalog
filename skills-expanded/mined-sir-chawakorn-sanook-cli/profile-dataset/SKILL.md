---
name: profile-dataset
description: Profiles a dataset to surface summary statistics, distributions, missing-value matrix, correlations, outliers, and data-quality issues with severity ratings.
when_to_use: ได้ dataset ใหม่/ไม่รู้จัก แล้วอยากเข้าใจมันก่อนเริ่มทำงาน — summary stats, เช็ก missing/outlier, ดู distribution/correlation, หรือขอ data-quality report ที่ระบุ severity + วิธีแก้
---

## When to Use

ใช้เมื่อได้ dataset (CSV/Parquet/JSON/DB table/DataFrame) ที่ **ยังไม่เข้าใจ** แล้วต้อง EDA (exploratory data analysis) ก่อนทำงานต่อ:
- อยาก summary stats + dtype + cardinality + null rate ต่อ column
- เช็ก missing values, outliers, distribution, correlation
- ขอ data-quality report ที่ flag ปัญหา + ระบุ severity (high/med/low) + วิธีแก้

**Read-only เสมอ — ห้าม mutate source.** skill นี้แค่ inspect ไม่ transform.

แยกจาก skill ใกล้เคียง:
- **wrangle** = แก้/transform ข้อมูล (clean, reshape). profile แค่ "ดู" ไม่แตะ → ถ้าโจทย์คือ "clean/fix/แปลง" ใช้ wrangle.
- **validate-data-quality** = เช็กตาม rule/contract ที่กำหนดไว้ (pass/fail vs schema). profile เป็น ad-hoc EDA ที่ยัง **ไม่มี rule** → ใช้ profile เพื่อ "ค้นพบ" ปัญหา แล้วค่อยเขียน rule ให้ validate.

## Steps

1. **เปิดด้วย sample ก่อน full pass.** อ่าน `nrows≈1000` (หรือ `LIMIT 1000`) ก่อน เพื่อ infer schema + จับ dtype/encoding/delimiter ผิดแต่เนิ่นๆ ก่อน load ทั้งไฟล์. ระบุ **shape (rows × cols)** + ขนาดไฟล์/memory. ถ้าใหญ่กว่า RAM → ใช้ chunked read (`chunksize`) หรือ columnar engine (Polars/DuckDB/PyArrow) อย่า `pd.read_csv` ทั้งก้อน.

2. **ทำ per-column profile (loop ทุก column).** สำหรับแต่ละ column เก็บ: `dtype` (จริง ไม่ใช่ที่ pandas เดา), `non_null / null_count / null_pct`, `n_unique` (cardinality), และ sample 3–5 ค่า. จาก cardinality classify ชนิด:
   - `n_unique == 1` → **constant** (flag, ดู step 5)
   - `n_unique == n_rows` → candidate **ID/key** (ห้ามเอาไปทำ stats/correlation)
   - low cardinality (เช่น `< 50` หรือ `< 5%` ของ rows) → **categorical**
   - numeric dtype + high cardinality → **numeric**
   - parse ได้เป็น date → **datetime** (ลอง parse แม้ dtype เป็น object)

3. **Numeric columns → distribution + outliers + correlation.**
   - stats: `count, mean, std, min, p25, p50, p75, max, skew`. **skew สูง** (|skew| > 1) = แจกแจงเบ้ → บอกว่า mean ไม่ representative, ควรใช้ median.
   - outliers: **IQR rule** (นอก `[Q1 − 1.5·IQR, Q3 + 1.5·IQR]`) เป็น default; z-score (`|z| > 3`) ใช้เฉพาะเมื่อใกล้ normal เท่านั้น. รายงาน **count + %** ของ outlier ต่อ column ไม่ใช่ทุกแถว.
   - histogram: ใช้ bin หยาบ (เช่น 10 bins) สรุปรูปร่าง (unimodal/bimodal/uniform/skewed) เป็นข้อความ ไม่ต้อง dump ทุก bin.
   - correlation: คำนวณเฉพาะคู่ numeric. ใช้ **Spearman** ถ้า skew/มี outlier (robust กว่า Pearson). รายงานเฉพาะคู่ `|r| > 0.7` (strong) อย่า dump matrix เต็ม. เตือนถ้าเจอ `|r| ≈ 1.0` = อาจเป็น column ซ้ำ/leakage.

4. **Categorical columns → top values + rare levels.** รายงาน top 5–10 value พร้อม count + %. flag:
   - **rare levels** (level ที่ count น้อยมาก เช่น `< 1%` รวมกันเป็น long tail) → เสี่ยง noise/typo variant
   - **near-duplicate levels** จาก case/whitespace/encoding (`"USA"` vs `"usa "` vs `"U.S.A"`) → normalize ก่อนนับจริง
   - high-cardinality categorical (เช่น free-text) → อย่าทำ one-hot, flag ว่าควร bucket/embed

5. **Missing-data matrix + pattern detection.** ไม่ใช่แค่ % รวม — ดู **pattern**:
   - rank column ตาม null_pct (สูงสุดก่อน)
   - **co-missingness**: column ไหนหายด้วยกันเสมอ (correlation ของ null-mask) → บอกว่า missing เป็น structural (เช่น มาจาก join/optional section) ไม่ใช่ random
   - **MNAR signal**: null กระจุกในบาง segment/ช่วงเวลา → missing not at random, การ drop/impute จะ bias
   - เตือน **disguised missing**: `0`, `-1`, `999`, `"N/A"`, `"null"`, `""`, epoch `1970-01-01` ที่จริงคือ missing แต่ไม่ถูกนับเป็น NaN

6. **รวบ data-quality issues — แต่ละอันมี severity + fix.** เช็กอย่างน้อย:

   | Issue | severity ทั่วไป | recommended fix |
   |---|---|---|
   | Constant column (1 ค่า) | low | drop — ไม่มี information |
   | Duplicate rows (full-row) | high | dedupe; ถ้าตั้งใจซ้ำ ต้องมี key/timestamp อธิบาย |
   | Duplicate on key column | high | สืบ source; เลือก row ที่ถูก (latest/non-null) |
   | High null % (เช่น > 50%) | high/med | drop column หรือ impute + เพิ่ม missing-flag |
   | Disguised missing (sentinel) | high | convert เป็น NaN ก่อน analysis ใดๆ |
   | Suspicious range (อายุ < 0 / > 120, price ≤ 0, lat นอก ±90) | high | กฎ domain; clip/flag/drop |
   | Mixed types ใน column เดียว | high | parse/cast ให้ consistent; หา row ที่ทำพัง |
   | Skewed/outlier-heavy numeric | med | บอก downstream ว่าต้อง transform (log/winsorize) |
   | Rare/typo categorical levels | med | normalize + map synonyms |
   | Near-perfect correlation / leakage | med | drop redundant; ถ้าจะ model ระวัง target leakage |
   | Datetime ที่ parse ไม่ได้/อนาคต | med | ตรวจ format/timezone; flag future dates |

   จัด **high ก่อน** — high = ผิดแล้ว analysis ต่อจากนี้พังหมด (dup, sentinel, suspicious range, mixed type).

7. **Emit summary ที่อ่านได้ ไม่ใช่ raw dump.** Output เป็น report สั้น signal สูง:
   - **Overview**: shape, memory, จำนวน column แยกตาม type, จำนวน issue แยก severity
   - **Per-column table**: name · type · null% · cardinality · note สั้น (เฉพาะที่มีอะไรน่าสนใจ)
   - **Issues** เรียงตาม severity: `[HIGH] <column>: <อาการ> → <fix>`
   - **Top correlations** (ถ้ามี), **distribution highlights** (เฉพาะที่เบ้/bimodal)
   - **Next steps**: 2–4 action ที่ควรทำก่อนใช้ data นี้

   อย่า paste `df.describe()` ดิบ หรือ correlation matrix เต็ม หรือ histogram array — สรุปเป็นคำ.

## Common Errors

- **`df.describe()` แล้วจบ.** มันให้แค่ numeric column, ข้าม categorical/datetime/null-pattern ทั้งหมด — ซึ่งคือที่ที่ปัญหาคุณภาพข้อมูลซ่อนอยู่จริง. ต้องทำครบ step 2–6.
- **เชื่อ dtype ที่ pandas infer.** column ตัวเลขที่มี `""`/`"N/A"` ปนจะกลายเป็น `object` ทั้ง column; ID เลขล้วนกลายเป็น `int` แล้วโดนเอาไปทำ mean (ไร้ความหมาย). cast/parse เอง อย่าเชื่อ inference.
- **disguised missing ไม่ถูกนับ.** `0`/`-1`/`999`/`"unknown"` ทำให้ null_pct ดูสวยแต่ mean/min/max เพี้ยน. scan sentinel ก่อนคำนวณ stats (step 5).
- **z-score outlier บนข้อมูลเบ้.** z-score สมมติ normal — บน distribution เบ้/มี outlier มันพังเพราะ mean/std โดน outlier ดึงเอง. ใช้ IQR เป็น default.
- **Pearson บนข้อมูลมี outlier.** outlier เดียวสร้าง correlation ปลอมได้. ใช้ Spearman เมื่อไม่ normal.
- **average ของ ID/key column.** mean ของ `user_id`/`order_id` ไม่มีความหมาย. exclude high-cardinality unique column ออกจาก numeric stats (step 2 classify ก่อน).
- **โหลดไฟล์ใหญ่ทั้งก้อนจน OOM.** sample + chunk/columnar engine ก่อน (step 1). ถ้า dataset มาจาก DB → ทำ profiling ด้วย SQL aggregate (`COUNT, COUNT(DISTINCT), MIN, MAX, AVG`) อย่า pull ทั้ง table มา client.
- **mutate source.** sort/fillna/dropna/cast บน DataFrame ต้นฉบับแล้วเขียนกลับ. ทำงานบน copy เท่านั้น; ห้าม write ทับไฟล์/table เดิม.
- **dump ทุกอย่างใส่หน้าจอ.** correlation matrix 50×50, histogram ทุก column, value_counts เต็ม = noise. สรุปเฉพาะที่ผิดปกติ.
- **datetime ไม่ดู timezone/future.** mixed tz หรือ date ในอนาคต/epoch 1970 มักเป็น bug ที่ describe มองไม่เห็น.

## Verify

ถือว่าเสร็จเมื่อครบ:
- [ ] รายงาน **shape + memory + จำนวน column แยก type** ครบ
- [ ] **ทุก column** มี dtype + null% + cardinality (ไม่ข้าม column ไหน)
- [ ] numeric มี distribution + outlier (IQR) + correlation (เฉพาะคู่ strong); categorical มี top values + rare/typo flag
- [ ] missing-data **pattern** (ไม่ใช่แค่ % รวม) + scan disguised-missing แล้ว
- [ ] ทุก quality issue มี **severity + recommended fix**, เรียง high ก่อน
- [ ] output เป็น summary อ่านได้ + next steps — **ไม่มี raw dump**
- [ ] source ไม่ถูกแก้ (ทำบน copy / read-only query) — ยืนยันได้ว่า dataset เดิมไม่เปลี่ยน
