---

## name: computational-linguistics
description: >
  Computational linguistics expert for NLP, linguistic analysis, and language technology.
  Use this skill whenever the user needs: building linguistically-aware NLP systems,
  implementing syntactic and semantic analysis, processing multilingual text, creating
  language models with linguistic structure, working with corpora and linguistic
  resources, or any task involving the computational treatment of natural language.
  This skill combines formal linguistics with machine learning approaches to create
  robust, interpretable language technology.
license: MIT
compatibility: opencode
metadata:
  audience: machine-learning-engineers
  category: artificial-intelligence

# Computational Linguistics

Covers: **Morphological Analysis · Syntactic Parsing · Semantic Representation · Pragmatics · Corpus Linguistics · Statistical Models · Deep Learning for Language · Multilingual Processing**

-----

## Linguistic Analysis Levels

Computational linguistics operates across multiple levels of linguistic analysis:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Discourse Level                               │
│         (context, coherence, discourse relations)                │
├─────────────────────────────────────────────────────────────────┤
│                     Semantics Level                              │
│     (meaning, logical form, thematic roles, word senses)        │
├─────────────────────────────────────────────────────────────────┤
│                    Pragmatics Level                              │
│        (intent, context, speech acts, presupposition)           │
├─────────────────────────────────────────────────────────────────┤
│                     Syntax Level                                 │
│         (grammar, phrase structure, dependency)                 │
├─────────────────────────────────────────────────────────────────┤
│                   Morphology Level                               │
│        (word formation, inflections, compounding)             │
├─────────────────────────────────────────────────────────────────┤
│              Phonology/Orthography Level                         │
│           (sounds, phonemes, written form, tokens)             │
└─────────────────────────────────────────────────────────────────┘
```

Each level requires different computational approaches and contributes to complete language understanding.

-----

## Morphological Analysis

### Finite-State Morphology

Finite-state transducers (FSTs) provide efficient morphological analysis:

```python
# Conceptual FST for English noun plurals
class FSTMorphology:
    def __init__(self):
        # Rewrite rules for plural formation
        self.rules = [
            # Regular: cat -> cats
            ('+V', '+PL', 's'),
            # es after s, x, z, ch, sh: box -> boxes
            ('+Sfx', 's|x|z|ch|sh', 'es'),
            # y -> ies: city -> cities
            ('y', '[b-gilm-npr-t]y', 'ies'),
            # Irregular forms
            ('man', 'man', 'men'),
            ('foot', 'foot', 'feet'),
            ('tooth', 'tooth', 'teeth'),
        ]
    
    def analyze(self, word):
        """Analyze word into stem + morphological features"""
        for suffix, stem, plural in self.irregular:
            if word == plural:
                return {'stem': stem, 'number': 'plural'}
        
        # Apply regular rules
        for rule in self.rules:
            if word.endswith(rule[2]):
                stem = word[:-len(rule[2])]
                return {'stem': stem, 'number': 'plural'}
        
        return {'stem': word, 'number': 'singular'}

    def generate(self, stem, features):
        """Generate word from stem + features"""
        # Apply morphological rules
        return stem + 's'
```

### Word Segmentation

```python
# Maximum matching (forward) for Chinese word segmentation
def max_match_forward(text, dictionary):
    """Forward maximum matching segmentation"""
    results = []
    i = 0
    while i < len(text):
        matched = False
        for j in range(min(len(text), i + 10), i, -1):
            word = text[i:j]
            if word in dictionary:
                results.append(word)
                i = j
                matched = True
                break
        if not matched:
            results.append(text[i])
            i += 1
    return results

# BPE (Byte Pair Encoding) for subword tokenization
class BPE:
    def __init__(self, vocab_size=10000):
        self.vocab_size = vocab_size
        self.vocab = {}
        self.merges = []
    
    def get_stats(self, text):
        """Get frequency counts of adjacent pairs"""
        pairs = {}
        for i in range(len(text) - 1):
            pair = (text[i], text[i+1])
            pairs[pair] = pairs.get(pair, 0) + 1
        return pairs
    
    def merge_vocab(self, pair):
        """Merge most frequent pair"""
        # Implementation of BPE merge operation
        pass
```

-----

## Syntactic Analysis

### Context-Free Grammars

```python
# CFG definition for simple English
grammar = {
    'S': [['NP', 'VP']],
    'NP': [['Det', 'N'], ['NP', 'PP'], ['Det', 'Adj', 'N']],
    'VP': [['V'], ['V', 'NP'], ['VP', 'PP']],
    'PP': [['P', 'NP']],
    'Det': ['the', 'a', 'an'],
    'N': ['cat', 'dog', 'bird', 'fish'],
    'V': ['chases', 'eats', 'sees'],
    'P': ['in', 'on', 'with', 'by'],
    'Adj': ['fast', 'lazy', 'blue']
}

# CKY Parser
def cky_parse(sentence, grammar):
    """Cocke-Kasami-Younger bottom-up parsing"""
    n = len(sentence)
    table = [[set() for _ in range(n)] for _ in range(n)]
    back = [[None for _ in range(n)] for _ in range(n)]
    
    # Initialize diagonal with terminal productions
    for i, word in enumerate(sentence):
        for lhs, rhss in grammar.items():
            for rhs in rhss:
                if len(rhs) == 1 and rhs[0] == word:
                    table[i][i].add(lhs)
                    back[i][i] = (lhs, [word])
    
    # Fill table for longer spans
    for length in range(2, n + 1):
        for start in range(n - length + 1):
            end = start + length - 1
            for mid in range(start, end):
                for i, lhs in enumerate(grammar):
                    for j, rhs in enumerate(grammar[lhs]):
                        if len(rhs) == 2:
                            B, C = rhs
                            if B in table[start][mid] and C in table[mid+1][end]:
                                table[start][end].add(lhs)
                                back[start][end] = (lhs, (mid, B, C))
    
    return table, back
```

### Dependency Parsing

```python
# Using spaCy for dependency parsing
import spacy

nlp = spacy.load("en_core_web_sm")

def analyze_dependencies(sentence):
    """Analyze sentence structure using dependency parsing"""
    doc = nlp(sentence)
    
    results = {
        'tokens': [],
        'dependencies': [],
        'nouns': [],
        'verbs': [],
        'root': None
    }
    
    for token in doc:
        results['tokens'].append({
            'text': token.text,
            'pos': token.pos_,
            'dep': token.dep_,
            'head': token.head.text,
            'lemma': token.lemma_,
            'tag': token.tag_
        })
        
        if token.dep_ == 'ROOT':
            results['root'] = token.text
        
        if token.pos_ == 'NOUN':
            results['nouns'].append(token.text)
        elif token.pos_ == 'VERB':
            results['verbs'].append(token.text)
    
    return results

# Universal Dependencies POS tags
ud_pos_tags = {
    'NOUN': 'Noun - person, place, thing, idea',
    'VERB': 'Verb - action, state, occurrence',
    'ADJ': 'Adjective - describes noun',
    'ADV': 'Adverb - describes verb/adjective',
    'PRON': 'Pronoun - replaces noun',
    'DET': 'Determiner - specifies noun',
    'PREP': 'Preposition - spatial/temporal relation',
    'CONJ': 'Conjunction - connects elements',
    'NUM': 'Numeral - number',
    'PUNCT': 'Punctuation'
}
```

### Constituency vs. Dependency

| Aspect | Constituency | Dependency |
|--------|--------------|------------|
| **Structure** | Phrase structure tree | Directed graph |
| **Units** | Phrases | Words |
| **History** | Chomsky (1950s) | Tesnière (1959) |
| **Modern use** | Statistical parsers | Neural parsers |
| **Strengths** | Cross-linguistic | Efficient, direct |
| **Tools** | Stanford Parser, Berkeley | spaCy, UDPipe |

-----

## Semantic Representation

### Formal Semantics

```python
# Lambda calculus semantics for simple sentences
class LambdaCalculus:
    def __init__(self):
        self.variables = {}
    
    def parse(self, expr):
        """Parse lambda expression"""
        if isinstance(expr, str):
            # Handle variables and constants
            return expr
        elif expr[0] == 'lambda':
            var, body = expr[1], expr[2]
            return lambda x: self.substitute(body, var, x)
        elif isinstance(expr, list):
            # Function application
            func = self.parse(expr[0])
            arg = self.parse(expr[1])
            return func(arg)
    
    def substitute(self, expr, var, value):
        """Substitute variable with value"""
        if expr == var:
            return value
        elif isinstance(expr, list):
            return [self.substitute(e, var, value) for e in expr]
        return expr

# Example: "Every dog barks"
# Every = λP.λQ.∀x.(P(x) → Q(x))
# dog = λx.dog(x)
# barks = λx.barks(x)
# (Every dog) barks = λQ.∀x.(dog(x) → Q(x)) (barks) = ∀x.(dog(x) → barks(x))
```

### Semantic Role Labeling

```python
# PropBank-style semantic roles
propbank_roles = {
    'ARG0': 'Agent - doer of the action',
    'ARG1': 'Patient - undergoer of the action',
    'ARG2': 'Instrument, beneficiary, or location',
    'ARG3': 'Start point or extent',
    'ARG4': 'End point',
    'ARGM-LOC': 'Location',
    'ARGM-TMP': 'Time',
    'ARGM-MNR': 'Manner',
    'ARGM-CAU': 'Cause',
    'ARGM-PNC': 'Purpose'
}

# FrameNet-style frames
framenet_frames = {
    'Destroying': {
        'core_roles': ['Destroyer', 'Patient', 'Instrument'],
        'examples': ['The fire destroyed the building']
    },
    'Motion': {
        'core_roles': ['Theme', 'Source', 'Goal', 'Path'],
        'examples': ['The bird flew from the tree to the roof']
    },
    'Communication': {
        'core_roles': ['Speaker', 'Message', 'Addressee'],
        'examples': ['She told him the story']
    }
}
```

### Word Senses and Embeddings

```python
# Word sense disambiguation using embeddings
def disambiguate_sense(word, context, wordnet):
    """Disambiguate word sense using context"""
    # Get all senses of word
    senses = wordnet.senses(word)
    
    if not senses:
        return None
    
    # Get context embeddings
    context_vec = get_embedding(context)
    
    # Score each sense
    best_sense = None
    best_score = -float('inf')
    
    for sense in senses:
        # Get definition embedding
        def_vec = get_embedding(sense.definition)
        
        # Calculate similarity
        score = cosine_similarity(context_vec, def_vec)
        
        if score > best_score:
            best_score = score
            best_sense = sense
    
    return best_sense
```

-----

## Corpus Linguistics

### Corpus Query and Statistics

```python
# Concordance generation
def concordance(query, corpus, window=5):
    """Generate KWIC (Key Word In Context) concordance"""
    results = []
    for i, sent in enumerate(corpus):
        tokens = sent['tokens']
        for j, token in enumerate(tokens):
            if token.lower() == query.lower():
                # Extract context
                start = max(0, j - window)
                end = min(len(tokens), j + window + 1)
                
                left = ' '.join(tokens[start:j])
                center = tokens[j]
                right = ' '.join(tokens[j+1:end])
                
                results.append({
                    'left': left,
                    'center': center,
                    'right': right,
                    'sentence_id': i
                })
    
    return results

# Frequency analysis
def frequency_analysis(text):
    """Calculate frequency statistics"""
    tokens = tokenize(text)
    freq = {}
    for token in tokens:
        freq[token] = freq.get(token, 0) + 1
    
    # Sort by frequency
    sorted_freq = sorted(freq.items(), key=lambda x: -x[1])
    
    return {
        'types': len(freq),
        'tokens': len(tokens),
        'ttr': len(freq) / len(tokens),  # Type-token ratio
        'hapax': sum(1 for f in freq.values() if f == 1),
        'top_100': sorted_freq[:100]
    }
```

### N-gram Analysis

```python
def ngrams(text, n):
    """Extract n-grams from text"""
    tokens = tokenize(text)
    return [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

def ngram_probability(ngram, ngram_counts, context_counts):
    """Calculate n-gram probability using MLE"""
    n = len(ngram)
    context = ngram[:n-1]
    
    if context not in context_counts:
        return 0
    
    count_ngram = ngram_counts.get(ngram, 0)
    count_context = context_counts[context]
    
    return count_ngram / count_context if count_context > 0 else 0

def smoothed_probability(ngram, ngram_counts, context_counts, vocab_size, alpha=0.1):
    """Add-k smoothing"""
    n = len(ngram)
    context = ngram[:n-1]
    
    count_ngram = ngram_counts.get(ngram, 0)
    count_context = context_counts.get(context, 0)
    
    return (count_ngram + alpha) / (count_context + alpha * vocab_size)
```

-----

## Statistical and Neural Models

### Hidden Markov Models for POS Tagging

```python
class HMM:
    def __init__(self):
        self.transition_probs = {}  # P(tag_i | tag_{i-1})
        self.emission_probs = {}    # P(word | tag)
        self.tag_probs = {}         # P(tag)
        self.vocab = set()
        self.tags = set()
    
    def train(self, tagged_sentences):
        """Train HMM on tagged corpus"""
        # Count transitions and emissions
        for sent in tagged_sentences:
            prev_tag = None
            for word, tag in sent:
                self.tags.add(tag)
                self.vocab.add(word)
                
                # Emission
                if tag not in self.emission_probs:
                    self.emission_probs[tag] = {}
                self.emission_probs[tag][word] = \
                    self.emission_probs[tag].get(word, 0) + 1
                
                # Transition
                if prev_tag:
                    if prev_tag not in self.transition_probs:
                        self.transition_probs[prev_tag] = {}
                    self.transition_probs[prev_tag][tag] = \
                        self.transition_probs[prev_tag].get(tag, 0) + 1
                
                # Initial probability
                self.tag_probs[tag] = self.tag_probs.get(tag, 0) + 1
                prev_tag = tag
        
        # Convert to probabilities
        self._normalize()
    
    def _normalize(self):
        """Convert counts to probabilities"""
        # Normalize transitions
        for prev in self.transition_probs:
            total = sum(self.transition_probs[prev].values())
            for tag in self.transition_probs[prev]:
                self.transition_probs[prev][tag] /= total
        
        # Normalize emissions
        for tag in self.emission_probs:
            total = sum(self.emission_probs[tag].values())
            for word in self.emission_probs[tag]:
                self.emission_probs[tag][word] /= total
        
        # Normalize tag probs
        total = sum(self.tag_probs.values())
        for tag in self.tag_probs:
            self.tag_probs[tag] /= total
    
    def viterbi(self, sentence):
        """Viterbi algorithm for decoding"""
        V = [{}]
        path = {}
        
        # Initialize
        for tag in self.tags:
            V[0][tag] = self.tag_probs.get(tag, 0) * \
                        self.emission_probs.get(tag, {}).get(sentence[0], 1e-10)
            path[tag] = [tag]
        
        # Forward pass
        for t in range(1, len(sentence)):
            V.append({})
            new_path = {}
            
            for curr_tag in self.tags:
                (prob, prev_tag) = max(
                    (V[t-1][prev_tag] * 
                     self.transition_probs.get(prev_tag, {}).get(curr_tag, 0) *
                     self.emission_probs.get(curr_tag, {}).get(sentence[t], 1e-10),
                     prev_tag)
                    for prev_tag in self.tags
                )
                V[t][curr_tag] = prob
                new_path[curr_tag] = path[prev_tag] + [curr_tag]
            
            path = new_path
        
        # Backtrack
        best_tag = max(V[-1], key=V[-1].get)
        return path[best_tag]
```

### Transformer Architecture

```python
# Simplified transformer attention mechanism
class SelfAttention:
    def __init__(self, d_model, num_heads):
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        self.W_q = Linear(d_model, d_model)
        self.W_k = Linear(d_model, d_model)
        self.W_v = Linear(d_model, d_model)
        self.W_o = Linear(d_model, d_model)
    
    def split_heads(self, x):
        """Split into multiple heads"""
        batch_size = x.size(0)
        x = x.view(batch_size, -1, self.num_heads, self.d_k)
        return x.permute(0, 2, 1, 3)
    
    def forward(self, x, mask=None):
        # Linear projections
        Q = self.split_heads(self.W_q(x))
        K = self.split_heads(self.W_k(x))
        V = self.split_heads(self.W_v(x))
        
        # Scaled dot-product attention
        scores = torch.matmul(Q, K.transpose(-2, -1)) / np.sqrt(self.d_k)
        
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
        
        attention = F.softmax(scores, dim=-1)
        context = torch.matmul(attention, V)
        
        # Concatenate heads
        context = context.permute(0, 2, 1, 3).contiguous()
        context = context.view(context.size(0), -1, self.d_model)
        
        return self.W_o(context)
```

-----

## Linguistic Resources

### Major Resources

| Resource | Description | URL |
|----------|-------------|-----|
| **WordNet** | Lexical database with synsets | wordnet.princeton.edu |
| **Universal Dependencies** | Cross-linguistic syntactic annotations | universaldependencies.org |
| **Penn Treebank** | English syntactic annotations | nlp.cornell.edu/data |
| **BabelNet** | Multilingual encyclopedic dictionary | babekn.net |
| **FrameNet** | Semantic frame database | framenet.icsi.berkeley.edu |
| **VerbNet** | Verb classification | verbnet.ldc.upenn.edu |
| **COMBO** | Unified verb resource | combostates.com |
| **Wikipedia** | Knowledge base | wikipedia.org |

### Processing Multilingual Text

```python
# Language detection using character n-grams
def detect_language(text, lang_profiles):
    """Detect language using n-gram profiles"""
    # Extract character trigrams
    trigrams = {}
    for i in range(len(text) - 2):
        trigram = text[i:i+3].lower()
        trigrams[trigram] = trigrams.get(trigram, 0) + 1
    
    # Normalize
    total = sum(trigrams.values())
    for t in trigrams:
        trigrams[t] /= total
    
    # Compare with profiles
    scores = {}
    for lang, profile in lang_profiles.items():
        score = 0
        for t, freq in trigrams.items():
            profile_freq = profile.get(t, 0)
            score += freq * np.log(freq / (profile_freq + 1e-10) + 1e-10)
        scores[lang] = score
    
    return min(scores, key=scores.get)
```

-----

## Common Errors to Avoid

- **Ignoring tokenization**: Different languages require different tokenization strategies
- **Over-reliance on English**: Many NLP techniques don't generalize across languages
- **Neglecting morphology**: Especially for morphologically rich languages
- **Using word embeddings alone**: Contextual embeddings (BERT, etc.) are more powerful
- **Ignoring discourse**: Sentences in context mean more than isolated sentences
- **Not handling ambiguity**: Natural language is inherently ambiguous
- **Assuming standard POS tags**: Different annotation schemes exist
- **Ignoring Named Entities**: NER is crucial for information extraction
- **Not evaluating on real data**: Synthetic test data often doesn't reflect reality
- **Confusing syntax and semantics**: They are related but distinct levels of analysis
