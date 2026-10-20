---
name: nlp-patterns
description: "When to activate: NLP, text classification, NER, spaCy, NLTK, sentence-transformers, embeddings, text similarity, tokenization"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: ml-ai
  language: python
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# NLP Patterns

## spaCy Pipeline

```python
import spacy

nlp = spacy.load("en_core_web_lg")

# Add custom component
@spacy.Language.component("custom_sentencizer")
def custom_sentencizer(doc):
    for token in doc[:-1]:
        if token.text in (".", "!", "?"):
            doc[token.i + 1].is_sent_start = True
    return doc

nlp.add_pipe("custom_sentencizer", before="parser")

doc = nlp("Apple is looking at buying U.K. startup for $1 billion.")
for ent in doc.ents:
    print(ent.text, ent.label_)          # Apple ORG, U.K. GPE, $1 billion MONEY

# Batch processing (efficient)
texts = ["doc1...", "doc2...", "doc3..."]
for doc in nlp.pipe(texts, batch_size=64, n_process=4):
    print([ent.text for ent in doc.ents])
```

## HuggingFace Text Classification

```python
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch

# Zero-shot (no fine-tuning)
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
result = classifier(
    "This is a great product!",
    candidate_labels=["positive", "negative", "neutral"],
)
print(result["labels"][0], result["scores"][0])

# Fine-tuned classification
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=3)

def tokenize(texts, max_length=128):
    return tokenizer(texts, padding=True, truncation=True,
                     max_length=max_length, return_tensors="pt")

inputs = tokenize(["Great product!", "Terrible experience."])
with torch.no_grad():
    logits = model(**inputs).logits
probs = logits.softmax(dim=-1)
```

## Named Entity Recognition Fine-tuning

```python
from transformers import AutoModelForTokenClassification, TrainingArguments, Trainer
from datasets import Dataset

label2id = {"O": 0, "B-PER": 1, "I-PER": 2, "B-ORG": 3, "I-ORG": 4}
id2label = {v: k for k, v in label2id.items()}

model = AutoModelForTokenClassification.from_pretrained(
    "bert-base-cased", num_labels=len(label2id), id2label=id2label, label2id=label2id
)

training_args = TrainingArguments(
    output_dir="ner-model",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=64,
    warmup_ratio=0.1,
    weight_decay=0.01,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
)
trainer = Trainer(model=model, args=training_args, train_dataset=train_ds, eval_dataset=val_ds)
trainer.train()
```

## Sentence Embeddings & Similarity

```python
from sentence_transformers import SentenceTransformer, util
import torch

model = SentenceTransformer("all-MiniLM-L6-v2")  # 384-dim, fast

sentences = ["The cat sat on the mat.", "A feline rested on a rug.", "Dogs love to play fetch."]
embeddings = model.encode(sentences, convert_to_tensor=True, batch_size=64, show_progress_bar=True)

# Cosine similarity matrix
cos_sim = util.cos_sim(embeddings, embeddings)
print(cos_sim)

# Semantic search
query = model.encode("cat resting", convert_to_tensor=True)
hits = util.semantic_search(query, embeddings, top_k=2)[0]
for hit in hits:
    print(sentences[hit["corpus_id"]], f"score={hit['score']:.3f}")
```

## Text Preprocessing

```python
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

def preprocess(text: str) -> str:
    text = text.lower()
    text = re.sub(r"http\S+", "", text)          # remove URLs
    text = re.sub(r"[^a-z\s]", "", text)         # keep letters only
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(t) for t in tokens if t not in stop_words and len(t) > 2]
    return " ".join(tokens)
```

## Key Patterns

- Prefer `model.pipe()` over `model()` in a loop — batch processing is 5-10x faster
- For semantic similarity use cosine on L2-normalized embeddings, not dot product
- `distilbert` is 40% smaller, 60% faster than BERT with 97% of performance
- For production NER: spaCy with `en_core_web_trf` (transformer) beats most custom models
- Always check OOV handling: spaCy lg has vectors; sm does not
