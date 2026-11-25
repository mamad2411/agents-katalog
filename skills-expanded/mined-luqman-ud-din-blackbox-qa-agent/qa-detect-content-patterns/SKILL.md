---
name: qa-detect-content-patterns
section: content
description: "Layer 1 of grammar/content 2-layer strategy. Deterministic Haiku probe. Catches: typos (60-word dict), pluralization, untranslated i18n keys, HTML entities, markdown literal, mojibake, lorem ipsum, TODO leaks, long sentences (>30 words), high reading level (Flesch-Kincaid >12), generic CTA copy, homophone candidates (flag for L2 judgment), suspicious-word misspelling candidates (flag for L2 dictionary check). Lang-scoped — skips non-English regions via lang attribute. Reads proper-noun whitelist from probe input."
model: haiku
applyOn: [laptop]
needsSetup: false
viewportSensitive: true
---
## Why this skill exists

Sonnet review (`qa-review-content`) is non-deterministic — same page produces slightly different findings between runs. That breaks regression tracking.

This skill is **Layer 1** of a two-layer strategy:

| Layer | Type | Catches | Determinism |
|-------|------|---------|-------------|
| **1 — this skill** | Haiku probe (regex + heuristic) | Pattern-detectable + candidate extraction | ✅ Deterministic same input → same output |
| **2 — `qa-review-content`** | Sonnet judgment | Confirms candidates + judges grammar/word-choice | ⚠️ Non-deterministic but scoped to long tail |

Layer 2 receives this layer's findings as context and is instructed to NOT re-flag confirmed patterns AND to confirm/dismiss candidate flags from this layer.

## What it catches — 18 issue types

| issueType | severity | What | Layer relationship |
|-----------|----------|------|--------------------|
| `commonTypo` | medium | 60-word dictionary of well-known typos (`teh`, `recieve`, `seperate`) | L1 final |
| `pluralAgreement` | low | "1 items", "0 days ago", "1 results found" | L1 final |
| `untranslatedKey` | high | Visible i18n keys: `{{user.email}}`, `common.button.save`, `__MSG_save__` | L1 final |
| `htmlEntityLiteral` | medium | `&amp;`, `&lt;`, `&nbsp;` rendered as text | L1 final |
| `markdownLiteral` | medium | `**bold**`, `[link](url)` rendered as text | L1 final |
| `encodingMojibake` | medium | UTF-8/Latin-1 corruption signatures | L1 final |
| `loremIpsum` | high | "Lorem ipsum / dolor sit amet" placeholder | L1 final |
| `todoLeak` | high | Developer markers (`TODO`, `FIXME`, `XXX`, `TBD`, `PLACEHOLDER`) visible | L1 final |
| `longSentence` | low | Sentence exceeds 30 words (readability) | L1 final |
| `highReadingLevel` | low | Flesch-Kincaid grade > 12 for body copy paragraphs | L1 final |
| `genericCTACopy` | medium | Button/link text matches blacklist (`Click here`, `Submit`, `More`, `Learn more`, `Read more`, etc.) | L1 final |
| `homophoneCandidate` | low | Sentence contains a homophone pair — Layer 2 grades correctness | L1 → L2 confirm |
| `candidateMisspelling` | low | 5+ char word not in stopword list, not proper noun, not technical token — Layer 2 confirms with real dictionary | L1 → L2 confirm |
| `doubledWord` | medium | Accidental word repetition ("the the", "is is", "and and") | L1 final |
| `spacingError` | low | Space before punctuation ("word ,") or multiple consecutive spaces | L1 final |
| `spellingLocaleMix` | low | Both UK and US spellings of the same word on the site (colour/color, organise/organize) | L1 final |
| `junkDataLeak` | high | Placeholder/test data in production (asdf, qwerty, foo bar, John Doe, test@test.com, 123 Main St) | L1 final |
| `brandInconsistency` | medium | Proper noun used with inconsistent casing vs the configured spelling (DoWeb vs Doweb vs DOWEB) | L1 final |

## Probe input schema

The orchestrator passes config-derived context into the probe via a wrapping `(ctx) => {...probe...}(ctx)` pattern:

```js
{
  properNouns: ["DoSuite", "Argus"],    // from automation.config.json → content.proper_nouns
  englishOnly: true,                     // from customize.toml → [content] english_only
  enableReadingLevel: true               // from customize.toml → [content] enable_reading_level
}
```

If `properNouns` is missing, the probe falls back to `[]` and Layer 2 handles brand recognition.

## Probe (browser_evaluate)

```js
((ctxCfg) => {
  const cfg = ctxCfg || {};
  const PROPER_NOUNS = new Set((cfg.properNouns || []).map(s => s.toLowerCase()));
  const ENGLISH_ONLY = cfg.englishOnly !== false;
  const ENABLE_READING_LEVEL = cfg.enableReadingLevel !== false;

  // ── Common-typo dictionary (60 words) ────────────────────────────────────
  const TYPOS = new Set([
    'teh','recieve','recieved','seperate','seperated','definately','occured','occuring',
    'untill','accross','adress','arguement','begining','beleive','calender','cemetary',
    'collegue','comming','concious','curiousity','dependant','desireable','dissapoint',
    'embarass','enviroment','existance','familar','febuary','foriegn','goverment',
    'grammer','happend','harrass','independant','knowlege','liason','libary','licence',
    'maintainance','millenium','noticable','occassion','occurance','peice','persistant',
    'possesion','prefered','priviledge','professer','pronounciation','publically',
    'reccomend','refered','responsability','similiar','succesful','suprise','tatoo',
    'tommorow','truely','wether','wierd'
  ]);

  // ── Top-300 most-common English stopwords (high-confidence "known good") ──
  // Words in this set are NEVER flagged as candidateMisspelling.
  const STOPWORDS = new Set([
    'about','above','after','again','against','all','also','although','always','among',
    'and','any','are','around','because','become','been','before','being','below','between',
    'both','came','can','come','could','course','did','does','done','during','each','either',
    'enough','even','ever','every','few','for','from','further','get','give','given','goes',
    'going','gone','got','had','has','have','having','here','him','his','how','however',
    'into','its','just','keep','kept','know','known','last','later','least','less','let',
    'like','likely','little','long','look','made','make','many','may','maybe','might','more',
    'most','must','need','never','new','next','nor','not','now','off','often','old','once',
    'one','only','onto','other','our','out','over','own','past','perhaps','place','put','quite',
    'rather','really','right','said','same','say','see','seen','set','several','she','should',
    'show','since','some','such','take','taken','than','that','the','their','them','then',
    'there','these','they','thing','this','those','though','through','time','too','under',
    'until','use','used','very','want','was','way','well','went','were','what','when','where',
    'which','while','who','whom','whose','why','will','with','within','without','would','yes',
    'yet','you','your','about','please','thank','thanks','welcome','hello','goodbye','sorry',
    'home','page','login','signup','register','account','profile','settings','dashboard',
    'search','submit','cancel','save','delete','edit','create','update','add','remove',
    'next','previous','back','close','open','select','choose','continue','finish','start',
    'help','support','contact','email','password','username','name','phone','address',
    'city','country','state','zip','postal','code','date','time','today','tomorrow','yesterday',
    'menu','user','users','admin','customer','customers','order','orders','product','products',
    'service','services','price','prices','total','subtotal','tax','discount','quantity',
    'item','items','cart','checkout','payment','shipping','billing','invoice','receipt',
    'success','error','warning','info','loading','please','required','optional','default',
    'available','unavailable','active','inactive','enabled','disabled','public','private',
    'yes','none','all','any','some','more','less','first','last','top','bottom','left','right',
    'company','team','project','task','tasks','status','priority','due','overdue','completed',
    'pending','draft','published','archived','deleted','recent','popular','featured','new',
    'view','views','viewing','viewer','viewed','show','showing','shown','hide','hidden',
    'send','sent','sending','sender','receive','received','receiver','message','messages',
    'notification','notifications','alert','alerts','reminder','reminders','update','updates',
    'history','log','logs','report','reports','export','import','download','upload',
    'file','files','folder','folders','document','documents','image','images','video','videos',
    'website','site','sites','app','application','applications','mobile','desktop','tablet',
    'browser','browsers','device','devices','platform','platforms','system','systems',
    'feature','features','option','options','preference','preferences','setting','help',
    'question','questions','answer','answers','request','requests','response','responses',
    'agree','accept','decline','allow','deny','grant','revoke','approve','reject','review',
    'reviews','rating','ratings','feedback','comment','comments','reply','replies','post',
    'posts','share','shares','like','likes','follow','follows','subscribe','subscriber'
  ]);

  // ── Generic CTA blacklist ────────────────────────────────────────────────
  const GENERIC_CTA = new Set([
    'click here','click','tap here','tap','here','more','read more','learn more',
    'see more','show more','view more','continue','next','submit','ok','okay',
    'go','start','begin','enter','done','finish','close','open','show','hide',
    'details','info','information','description','view','see','read','watch'
  ]);

  // ── Homophone pairs (flag candidates; L2 judges correctness) ─────────────
  const HOMOPHONE_RE = /\b(their|there|they['']?re|your|you['']?re|its|it['']?s|whose|who['']?s|to|too|two|then|than|affect|effect|accept|except|loose|lose|principal|principle|stationary|stationery|complement|compliment|farther|further|fewer|less)\b/gi;

  // ── DOM helpers ──────────────────────────────────────────────────────────
  const sel = el => {
    const id = el && el.id ? '#' + el.id : '';
    const cls = (el && el.className && typeof el.className === 'string')
      ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '';
    return ((el && el.tagName ? el.tagName.toLowerCase() : 'text') + id + cls).slice(0, 120);
  };
  const visible = el => {
    if (!el || el.nodeType !== 1) return true;
    const s = getComputedStyle(el);
    if (s.display === 'none' || s.visibility === 'hidden') return false;
    if (el.getAttribute && el.getAttribute('aria-hidden') === 'true') return false;
    return true;
  };
  const nearestLang = el => {
    let cur = el;
    while (cur && cur.nodeType === 1) {
      const l = cur.getAttribute && cur.getAttribute('lang');
      if (l) return l.toLowerCase().split('-')[0];
      cur = cur.parentElement;
    }
    return (document.documentElement.getAttribute('lang') || '').toLowerCase().split('-')[0] || null;
  };

  const SKIP_TAGS = new Set(['SCRIPT', 'STYLE', 'NOSCRIPT', 'NAV', 'FOOTER', 'IFRAME', 'TEMPLATE']);
  const MAX_FINDINGS = 50;
  const MAX_CANDIDATES_PER_CELL = 20;
  const out = [];
  const seen = new Set();
  let candidateMisspellingCount = 0;
  let homophoneCount = 0;

  const push = (finding) => {
    if (out.length >= MAX_FINDINGS) return;
    out.push(finding);
  };

  // ── Generic CTA scan (separate pass — element-level, not text-node) ──────
  const ctaSelectors = 'button, a[href], input[type="submit"], input[type="button"], [role="button"]';
  for (const el of document.querySelectorAll(ctaSelectors)) {
    if (!visible(el)) continue;
    if (ENGLISH_ONLY) {
      const lang = nearestLang(el);
      if (lang && lang !== 'en') continue;
    }
    const txt = ((el.textContent || el.value || '') + '').replace(/\s+/g, ' ').trim().toLowerCase();
    if (!txt || txt.length > 40) continue;
    if (GENERIC_CTA.has(txt)) {
      const ctx = sel(el);
      const key = `cta|${ctx}|${txt}`;
      if (seen.has(key)) continue;
      seen.add(key);
      push({
        issueType: 'genericCTACopy', severity: 'medium', selector: ctx,
        description: `Generic CTA copy "${txt}" — replace with action-specific verb (e.g., "Save changes", "View order")`,
        snippet: txt
      });
    }
  }

  // ── Walk text nodes for everything else ──────────────────────────────────
  const walk = (node) => {
    if (!node || out.length >= MAX_FINDINGS) return;
    if (node.nodeType === 1) {
      if (SKIP_TAGS.has(node.tagName)) return;
      if (!visible(node)) return;
    }
    if (node.nodeType === 3) {
      const text = (node.textContent || '');
      if (text.trim().length < 2) return;
      const parent = node.parentElement || document.body;
      const ctx = sel(parent);

      // Lang scoping — skip non-English text regions
      if (ENGLISH_ONLY) {
        const lang = nearestLang(parent);
        if (lang && lang !== 'en') return;
      }

      // ── 1. Common typo dictionary ─────────────────────────────────────────
      const words = text.match(/\b[a-zA-Z]+\b/g) || [];
      for (const w of words) {
        const lw = w.toLowerCase();
        if (!TYPOS.has(lw)) continue;
        const key = `typo|${ctx}|${lw}`;
        if (seen.has(key)) continue;
        seen.add(key);
        push({
          issueType: 'commonTypo', severity: 'medium', selector: ctx,
          description: `Misspelled word "${w}" — common dictionary typo`,
          snippet: w, position: text.trim().slice(0, 80)
        });
      }

      // ── 2. Pluralization: "1 items", "0 days ago", "1 results" ────────────
      const pluralRe = /\b([01])\s+([a-zA-Z]{3,})s\b/g;
      let pm;
      while ((pm = pluralRe.exec(text)) !== null) {
        const key = `plural|${ctx}|${pm[0]}`;
        if (seen.has(key)) continue;
        seen.add(key);
        push({
          issueType: 'pluralAgreement', severity: 'low', selector: ctx,
          description: `Plural agreement: "${pm[0]}" — should be "${pm[1]} ${pm[2]}"`,
          snippet: pm[0], suggestion: `${pm[1]} ${pm[2]}`
        });
      }

      // ── 3. Untranslated i18n keys ─────────────────────────────────────────
      const keyRe = /\{\{[\w.]+\}\}|\b[a-z][a-z0-9_]+\.[a-z][a-z0-9_]+\.[a-z][a-z0-9_]+\b|__MSG_\w+__/g;
      let km;
      while ((km = keyRe.exec(text)) !== null) {
        const dkey = `i18n|${ctx}|${km[0]}`;
        if (seen.has(dkey)) continue;
        seen.add(dkey);
        push({
          issueType: 'untranslatedKey', severity: 'high', selector: ctx,
          description: `Untranslated i18n key visible to users: "${km[0]}"`,
          snippet: km[0]
        });
      }

      // ── 4. HTML entities rendered as literal text ─────────────────────────
      const entRe = /&(?:amp|lt|gt|nbsp|quot|apos|copy|reg|trade|#\d+|#x[0-9a-fA-F]+);/g;
      let em;
      while ((em = entRe.exec(text)) !== null) {
        const dkey = `ent|${ctx}|${em[0]}`;
        if (seen.has(dkey)) continue;
        seen.add(dkey);
        push({
          issueType: 'htmlEntityLiteral', severity: 'medium', selector: ctx,
          description: `HTML entity "${em[0]}" rendered as literal text instead of decoded character`,
          snippet: em[0]
        });
      }

      // ── 5. Markdown rendered as literal text ──────────────────────────────
      const mdRe = /\*\*[^*\n]{1,80}\*\*|__[^_\n]{1,80}__|\[[^\]\n]{1,40}\]\([^)\n]{1,80}\)/g;
      let mdm;
      while ((mdm = mdRe.exec(text)) !== null) {
        const dkey = `md|${ctx}|${mdm[0]}`;
        if (seen.has(dkey)) continue;
        seen.add(dkey);
        push({
          issueType: 'markdownLiteral', severity: 'medium', selector: ctx,
          description: `Markdown syntax "${mdm[0].slice(0, 40)}" rendered as text instead of formatting`,
          snippet: mdm[0].slice(0, 80)
        });
      }

      // ── 6. Encoding mojibake ──────────────────────────────────────────────
      var MOJI_BIGRAMS = ["Ã©","Ã¨","Ã ","Ã«","Ã¯","Ã³","Ã¶","Ã¼","Ã±","Ã§","â€™","â€œ","â€¦","â€“","Â©","Â®","Â°","Â£","Â¥","Â§","â‚¬"];
      var hasMoji = false;
      for (var mi = 0; mi < MOJI_BIGRAMS.length; mi++) {
        if (text.indexOf(MOJI_BIGRAMS[mi]) !== -1) { hasMoji = true; break; }
      }
      if (hasMoji) {
        const dkey = `moji|${ctx}`;
        if (!seen.has(dkey)) {
          seen.add(dkey);
          push({
            issueType: 'encodingMojibake', severity: 'medium', selector: ctx,
            description: `UTF-8/Latin-1 encoding corruption in text`,
            snippet: text.trim().slice(0, 80)
          });
        }
      }

      // ── 7. Lorem ipsum placeholder ────────────────────────────────────────
      if (/\b(lorem\s+ipsum|dolor\s+sit\s+amet|consectetur\s+adipiscing)\b/i.test(text)) {
        const dkey = `lorem|${ctx}`;
        if (!seen.has(dkey)) {
          seen.add(dkey);
          push({
            issueType: 'loremIpsum', severity: 'high', selector: ctx,
            description: `Lorem ipsum placeholder text in production page`,
            snippet: text.trim().slice(0, 80)
          });
        }
      }

      // ── 8. Developer markers ──────────────────────────────────────────────
      const todoMatch = text.match(/\b(TODO|FIXME|XXX|TBD|PLACEHOLDER)\b/);
      if (todoMatch) {
        const dkey = `todo|${ctx}|${todoMatch[1]}`;
        if (!seen.has(dkey)) {
          seen.add(dkey);
          push({
            issueType: 'todoLeak', severity: 'high', selector: ctx,
            description: `Developer marker "${todoMatch[1]}" visible to users`,
            snippet: text.trim().slice(0, 80)
          });
        }
      }

      // ── 9. Long sentence (>30 words) — readability ────────────────────────
      // Split on . ! ? — count words per sentence.
      const sentences = text.match(/[^.!?]+[.!?]/g) || [];
      for (const s of sentences) {
        const trimmed = s.trim();
        if (trimmed.length < 50) continue;
        const wc = (trimmed.match(/\b[\w'']+\b/g) || []).length;
        if (wc > 30) {
          const dkey = `longsent|${ctx}|${trimmed.slice(0, 30)}`;
          if (seen.has(dkey)) continue;
          seen.add(dkey);
          push({
            issueType: 'longSentence', severity: 'low', selector: ctx,
            description: `Sentence has ${wc} words (>30) — split for readability`,
            snippet: trimmed.slice(0, 120)
          });
        }
      }

      // ── 10. Reading level (Flesch-Kincaid grade) ──────────────────────────
      if (ENABLE_READING_LEVEL && text.trim().length > 200) {
        const cleanText = text.trim();
        const sentenceCount = (cleanText.match(/[.!?]+/g) || []).length || 1;
        const wordList = cleanText.match(/\b[\w'']+\b/g) || [];
        const wordCount = wordList.length;
        if (wordCount > 30) {
          // Crude syllable estimate: vowel groups per word
          let syllables = 0;
          for (const w of wordList) {
            const groups = w.toLowerCase().match(/[aeiouy]+/g);
            syllables += groups ? Math.max(1, groups.length) : 1;
          }
          const fk = 0.39 * (wordCount / sentenceCount) + 11.8 * (syllables / wordCount) - 15.59;
          if (fk > 12) {
            const dkey = `fk|${ctx}`;
            if (!seen.has(dkey)) {
              seen.add(dkey);
              push({
                issueType: 'highReadingLevel', severity: 'low', selector: ctx,
                description: `Flesch-Kincaid grade ${fk.toFixed(1)} (>12, college-level) — simplify for general audience`,
                snippet: cleanText.slice(0, 100)
              });
            }
          }
        }
      }

      // ── 11. Homophone candidate (Layer 2 grades) ──────────────────────────
      if (homophoneCount < MAX_CANDIDATES_PER_CELL) {
        const matches = text.match(HOMOPHONE_RE);
        if (matches && matches.length > 0) {
          const dkey = `homo|${ctx}|${matches[0].toLowerCase()}`;
          if (!seen.has(dkey)) {
            seen.add(dkey);
            homophoneCount++;
            push({
              issueType: 'homophoneCandidate', severity: 'low', selector: ctx,
              description: `Possible homophone misuse near "${matches[0]}" — Layer 2 will grade`,
              snippet: text.trim().slice(0, 120),
              candidateWord: matches[0]
            });
          }
        }
      }

      // ── 12. Candidate misspelling (5+ chars, not stopword/proper-noun/typo)
      if (candidateMisspellingCount < MAX_CANDIDATES_PER_CELL) {
        for (const w of words) {
          if (w.length < 5) continue;
          if (/[A-Z].*[A-Z]/.test(w)) continue;                          // ALLCAPS / acronyms
          if (/^[A-Z][a-z]*[A-Z]/.test(w)) continue;                     // camelCase
          const lw = w.toLowerCase();
          if (STOPWORDS.has(lw)) continue;
          if (TYPOS.has(lw)) continue;                                   // already L1-final
          if (PROPER_NOUNS.has(lw)) continue;                            // brand whitelist
          // Skip standard English suffix derivations of stopwords
          const root = lw.replace(/(?:ing|ed|er|est|ly|s|es|tion|ment|ness|ity|ful|less|ous|ive|able|ible)$/, '');
          if (STOPWORDS.has(root)) continue;
          // Suspicious patterns: 3+ consonants in a row OR no vowel
          if (!/[aeiouy]/.test(lw)) {
            // truly suspicious — no vowel at all
          } else if (!/[bcdfghjklmnpqrstvwxz]{3,}/.test(lw)) {
            continue; // benign-looking — let L2 decide only if it wants extra recall
          }
          const dkey = `cand|${ctx}|${lw}`;
          if (seen.has(dkey)) continue;
          seen.add(dkey);
          candidateMisspellingCount++;
          push({
            issueType: 'candidateMisspelling', severity: 'low', selector: ctx,
            description: `Suspicious word "${w}" — Layer 2 will confirm against full dictionary`,
            snippet: w, position: text.trim().slice(0, 80),
            candidateWord: w
          });
          if (candidateMisspellingCount >= MAX_CANDIDATES_PER_CELL) break;
        }
      }
      return;
    }
    for (const c of node.childNodes || []) walk(c);
  };

  walk(document.body);

  // ── Full-page deterministic checks (gap-fill 2026-06-04) ─────────────────
  (() => {
    const bodyText = (document.body.innerText || '').replace(/ /g, ' ');
    const lc = bodyText.toLowerCase();

    // 14. Doubled words ("the the", "is is") — exclude legitimate repeats
    const DOUBLE_OK = new Set(['had','that','this','no','very','really','ha','blah','sing','beep']);
    const dblRe = /\b([a-z]{2,})\s+\1\b/gi;
    let dm; const dblSeen = new Set();
    while ((dm = dblRe.exec(bodyText)) !== null) {
      const w = dm[1].toLowerCase();
      if (DOUBLE_OK.has(w) || dblSeen.has(w)) continue;
      dblSeen.add(w);
      push({ issueType: 'doubledWord', severity: 'medium', selector: 'body',
        description: `Doubled word: "${dm[0]}" — likely an accidental repetition.`, snippet: dm[0] });
      if (dblSeen.size >= 5) break;
    }

    // 15. Spacing — space before punctuation (renders visibly) + run-on double spaces
    let sm = bodyText.match(/\w\s[,.;:!?](?:\s|$)/);
    if (sm) push({ issueType: 'spacingError', severity: 'low', selector: 'body',
      description: `Space before punctuation (e.g. "${sm[0].trim()}") — remove the space.`, snippet: sm[0].slice(0, 40) });
    let dsm = bodyText.match(/\S {2,}\S/);
    if (dsm) push({ issueType: 'spacingError', severity: 'low', selector: 'body',
      description: `Multiple consecutive spaces in visible text.`, snippet: dsm[0].slice(0, 40) });

    // 16. US/UK spelling mixed on the same site
    const UK_US = [['colour','color'],['favourite','favorite'],['organise','organize'],['organisation','organization'],['centre','center'],['catalogue','catalog'],['cancelled','canceled'],['behaviour','behavior'],['analyse','analyze'],['labour','labor'],['defence','defense'],['grey','gray'],['programme','program'],['enquiry','inquiry'],['licence','license']];
    for (const [uk, us] of UK_US) {
      if (new RegExp('\\b'+uk+'\\b','i').test(lc) && new RegExp('\\b'+us+'\\b','i').test(lc)) {
        push({ issueType: 'spellingLocaleMix', severity: 'low', selector: 'body',
          description: `Mixed UK/US spelling on the same site: "${uk}" and "${us}". Pick one locale and be consistent.`, snippet: uk+' / '+us });
        break;
      }
    }

    // 17. Junk / placeholder test-data leaked to production (lorem handled separately)
    const JUNK = [/\basdf+\b/i, /\bqwerty\b/i, /\bfoo\s*bar\b/i, /\btest\s+test\b/i, /\b(john|jane)\s+doe\b/i, /\b(test|example|sample|foo)@(test|example|sample|email)\.(com|test|org)\b/i, /\b123\s+main\s+st/i, /\bxxxx+\b/i];
    for (const re of JUNK) {
      const jm = bodyText.match(re);
      if (jm) { push({ issueType: 'junkDataLeak', severity: 'high', selector: 'body',
        description: `Placeholder/test data visible in production: "${jm[0]}".`, snippet: jm[0] }); break; }
    }

    // 19. trailingPeriodOnNumber — stat/metric numbers with a trailing period ("3.", "45.", "0.")
    // These look like sentence fragments. Common cause: a number formatter appending '.'
    // accidentally, or CMS content ending a number with a period.
    const statContainers = document.querySelectorAll('[class*="stat"],[class*="metric"],[class*="kpi"],[class*="count"],[class*="widget"],[class*="summary"],[class*="overview"],[class*="dashboard"]');
    let numPeriodFlagged = 0;
    const numPeriodSeen = new Set();
    for (const container of statContainers) {
      if (numPeriodFlagged >= 4) break;
      for (const el of container.querySelectorAll('span,p,div,h1,h2,h3,h4,h5,h6')) {
        if (numPeriodFlagged >= 4) break;
        const text = (el.innerText || '').trim();
        if (/^\d[\d,\s]*\.$/.test(text) && text.length <= 12) {
          const key = `numperiod|${text}`;
          if (numPeriodSeen.has(key)) continue;
          numPeriodSeen.add(key);
          numPeriodFlagged++;
          push({ issueType:'trailingPeriodOnNumber', severity:'low', selector:sel(el),
            description:`Stat number "${text}" has a trailing period — looks like an unfinished sentence. Remove the period or check your number formatter.`,
            snippet: text });
        }
      }
    }

    // 18. Brand / proper-noun casing consistency (DoWeb vs Doweb vs DOWEB)
    for (const brand of (cfg.properNouns || [])) {
      if (!brand || brand.length < 3) continue;
      const re = new RegExp('\\b' + brand.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\b', 'gi');
      const variants = new Set(); let bm;
      while ((bm = re.exec(bodyText)) !== null) { variants.add(bm[0]); if (variants.size > 6) break; }
      const wrong = [...variants].filter(v => v !== brand);
      if (wrong.length) push({ issueType: 'brandInconsistency', severity: 'medium', selector: 'body',
        description: `Brand "${brand}" appears with inconsistent casing: ${[...variants].join(', ')}. Use "${brand}" everywhere.`, snippet: wrong.join(', ').slice(0, 80) });
    }
  })();

  return out;
})
```

## Probe invocation

```
browser_evaluate(function = "(...probe code above wrapped in IIFE...)", arg = { properNouns: cfg.properNouns, englishOnly: cfg.englishOnly, enableReadingLevel: cfg.enableReadingLevel })
```

The orchestrator builds the `arg` object from:
- `automation.config.json → content.proper_nouns` (default `[appName]`)
- `customize.toml → [content] english_only` (default `true`)
- `customize.toml → [content] enable_reading_level` (default `true`)

## Issues

| issueType | severity | description format |
|---|---|---|
| commonTypo | medium | `Misspelled word '{word}' — common dictionary typo` |
| pluralAgreement | low | `Plural agreement: '1 items' — should be '1 item'` |
| untranslatedKey | high | `Untranslated i18n key visible to users: '{key}'` |
| htmlEntityLiteral | medium | `HTML entity '{entity}' rendered as literal text` |
| markdownLiteral | medium | `Markdown syntax '{md}' rendered as text` |
| encodingMojibake | medium | `UTF-8/Latin-1 encoding corruption in text` |
| loremIpsum | high | `Lorem ipsum placeholder text in production` |
| todoLeak | high | `Developer marker '{marker}' visible to users` |
| longSentence | low | `Sentence has {N} words (>30) — split for readability` |
| highReadingLevel | low | `Flesch-Kincaid grade {N} (>12) — simplify for general audience` |
| genericCTACopy | medium | `Generic CTA copy '{text}' — replace with action-specific verb` |
| homophoneCandidate | low | `Possible homophone misuse near '{word}' — Layer 2 will grade` |
| candidateMisspelling | low | `Suspicious word '{word}' — Layer 2 will confirm` |

## Notes

- **Read-only**: never mutates the DOM, never types or clicks
- **Bounded**: max 50 findings per cell; 20 candidate misspellings + 20 homophones max
- **Lang-scoped**: skips text inside `lang="ar"`, `lang="fr"`, etc. when `englishOnly=true`
- **Proper-noun aware**: brand names from config are never flagged as `candidateMisspelling`
- **Deduplication**: tracks `(issueType + selector + snippet)` to avoid same finding many times
- **Self-skip**: returns empty array on pages with no visible text content
- **Layer 2 contract**: `qa-review-content` (Sonnet) reads this skill's findings from the cell's findings buffer and:
  1. Does NOT re-flag any `L1 final` issueType match
  2. Confirms or dismisses every `candidateMisspelling` (real dictionary check)
  3. Grades every `homophoneCandidate` for context-correctness
