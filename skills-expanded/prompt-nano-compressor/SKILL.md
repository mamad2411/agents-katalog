---
name: "prompt-nano-compressor"
description: "ULTRA prompt compression: keep 8-10% tokens ONLY. Invoke on messages[] right BEFORE sending to LLM (post-truncate)."
---

# Prompt Nano-Compressor — 90–92% Token Reduction
**Target ratio: 0.08–0.10 (8-10% original tokens).** Uses SVO triples + hash dedupe.

## 7 STEP ALGORITHM (DETERMINISTIC, NO LLM)
Run sequential. All steps in-memory Python only.

### 1. WHITESPACE & DEDUPE (savings ~8%)
- Remove leading/trailing blank lines.
- Collapse multiple spaces/tabs → 1 space.
- Remove duplicate lines (hash set). Order preserved.
- Delete comment lines (#, //, --, *) IF length >150 chars.

### 2. STOPWORD PRUNE AGGRESSIVE (savings ~22%)
Remove ALL words that appear in English/Indonesian stoplist (union 900 words).
STOPWORDS = {the,a,an,and,or,but,if,then,else,of,to,in,on,at,for,with,by,is,are,was,were,be,been,being,have,has,had,do,does,did,will,would,should,could,may,might,can,i,you,he,she,it,we,they,me,him,her,us,them,my,your,his,its,our,their,this,that,these,those,what,which,who,whom,whose,when,where,why,how,all,any,each,few,more,most,other,some,such,no,nor,not,only,own,same,so,than,too,very,just,because,as,until,while,about,into,through,during,before,after,above,below,up,down,out,off,over,under,again,further,once,here,there,dan,atau,tetapi,jika,maka,adalah,ialah,dari,ke,dalam,pada,untuk,dengan,oleh,seperti,juga,hanya,yang,ini,itukah,apakah,bagaimana,mengapa,kapan,di mana,siapa,semua,setiap,beberapa,lebih,banyak,sedikit,lain,beberapa,sudah,akan,perlu,bisa,dapat,mungkin,harus,pasti,sudah,masih,belum,sedang,sekarang,nanti,dulu,sebelum,sesudah,atas,bawah,keluar,masuk,lebih,kurang}
Exceptions: words inside ```code blocks``` are untouched.

### 3. SVO TRIPLE EXTRACTION (savings ~35%)
For every sentence, keep ONLY: (SUBJECT, VERB-lemma, OBJECT).
Drop: adjectives, adverbs, conjunctions, prepositional phrases < 5 chars, relative clauses.
Tool: POS tagger lightweight (NLTK averaged_perceptron_tagger). If unavailable → heuristic: keep nouns + verbs + numbers (3/4/5-grams).

### 4. NUMBER & SYMBOL SHORTHAND (savings ~5%)
- Replace `(example: e.g. for instance` → `∈`
- Replace `therefore so thus hence consequently` → `∴`
- Replace `approximately about ≈ ~` → `≈`
- Replace `= equals` → `=`
- Replace Unicode arrows → ASCII `->` (saves 2 bytes each).
- Long number: round to 2 sig figs. `123,456 → 1.2e5`.

### 5. WORD HASH REPEAT (savings ~10%)
- Every word >15 chars that appears >2x: replace with `#H12` where H=hash prefix (1st letter) + count.
- First occurrence stays. All subsequent use the #TAG.
- Example: "anthropomorphic cat. anthropomorphic dog." → "anthropomorphic cat. #A2 dog."

### 6. CONTEXT WINDOW CAP (savings ~8%)
Final compressed output absolute MAX:
- User messages history: ≤ 800 tokens (total).
- System prompt: ≤ 450 tokens.
- Tool outputs (post-strangler): ≤ 800 tokens.
- **TOTAL FINAL SEND**: ≤ 2500 tokens. ALWAYS.

### 7. CHECKSUM VALIDATION
Append `|CMP:` + first 8 chars of SHA256(raw prompt). So if quality issue: raw can reconstruct from cache via exact hash.

## VERIFICATION & FALLBACK
If len(compressed tokens)/len(original) > 0.15:
→ Re-run STEP 2 & 3 with stopword +200 domain specific words (top TF-IDF). Loop until ratio ≤0.12.

## CONSUMPTION NOTE
Compressor uses NO LLM. Runtime <60ms for 5000 tokens input. No API cost: 100% CPU local.
