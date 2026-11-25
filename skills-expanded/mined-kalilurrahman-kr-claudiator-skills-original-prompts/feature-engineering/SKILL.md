---
name: feature-engineering
description: Design ML features with encoding, scaling, selection, and extraction. Outputs feature pipelines, importance analysis, and validation strategies.
argument-hint: [data type, model type, target variable]
allowed-tools: Read, Write, Bash
---

# Feature Engineering for Machine Learning

Design effective features for ML models. Not raw data — encoding, scaling, feature extraction, selection, and validation pipelines that improve model performance.

## Process

1. **Analyze data types.** Numeric, categorical, text, datetime, geospatial.
2. **Handle missing values.** Imputation strategies, missing indicators.
3. **Encode categoricals.** One-hot, label, target, ordinal encoding.
4. **Scale numerics.** StandardScaler, MinMaxScaler, RobustScaler.
5. **Create features.** Interactions, polynomials, aggregations, domain-specific.
6. **Select features.** Correlation, mutual information, model-based selection.
7. **Validate pipeline.** Train/test split, cross-validation, leakage prevention.

## Output Format

### Feature Engineering: [ML Task]

**Task:** Customer churn prediction  
**Features:** 45 (15 raw + 30 engineered)  
**Encoding:** One-hot for categoricals  
**Scaling:** StandardScaler for numerics  
**Selection:** Random Forest importances (top 25)

---

## Feature Types

### Numeric Features
```python
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

# Original numeric features
df['age']
df['income']
df['credit_score']

# Scaling strategies
scaler = StandardScaler()  # Mean=0, std=1 (assumes normal distribution)
df['age_scaled'] = scaler.fit_transform(df[['age']])

scaler = MinMaxScaler()  # Scale to [0, 1]
df['income_scaled'] = scaler.fit_transform(df[['income']])

scaler = RobustScaler()  # Median, IQR (robust to outliers)
df['credit_score_robust'] = scaler.fit_transform(df[['credit_score']])
```

### Categorical Features
```python
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

# Label encoding (ordinal)
le = LabelEncoder()
df['education_encoded'] = le.fit_transform(df['education'])
# High School=0, Bachelor=1, Master=2, PhD=3

# One-hot encoding (nominal)
df_encoded = pd.get_dummies(df, columns=['city'], prefix='city')
# city_SF, city_NYC, city_LA (binary columns)

# Frequency encoding
df['city_freq'] = df['city'].map(df['city'].value_counts())

# Target encoding
target_means = df.groupby('city')['churn'].mean()
df['city_target_enc'] = df['city'].map(target_means)
```

---

## Missing Value Handling

```python
from sklearn.impute import SimpleImputer, KNNImputer

# Simple strategies
imputer = SimpleImputer(strategy='mean')  # or 'median', 'most_frequent'
df['age_imputed'] = imputer.fit_transform(df[['age']])

# Create missing indicator
df['age_missing'] = df['age'].isna().astype(int)

# KNN imputation
imputer = KNNImputer(n_neighbors=5)
df[['age', 'income']] = imputer.fit_transform(df[['age', 'income']])

# Domain-specific imputation
df['last_purchase_days'] = df['last_purchase_date'].fillna(
    df['last_purchase_date'].max()  # Fill with "never purchased"
).apply(lambda x: (pd.Timestamp.now() - x).days)
```

---

## Feature Creation

### Datetime Features
```python
df['signup_date'] = pd.to_datetime(df['signup_date'])

# Extract components
df['signup_year'] = df['signup_date'].dt.year
df['signup_month'] = df['signup_date'].dt.month
df['signup_day_of_week'] = df['signup_date'].dt.dayofweek
df['signup_is_weekend'] = df['signup_day_of_week'].isin([5, 6]).astype(int)

# Time since
df['days_since_signup'] = (pd.Timestamp.now() - df['signup_date']).dt.days

# Cyclical encoding (month, hour)
df['month_sin'] = np.sin(2 * np.pi * df['signup_month'] / 12)
df['month_cos'] = np.cos(2 * np.pi * df['signup_month'] / 12)
```

### Aggregation Features
```python
# Customer-level aggregations
customer_agg = df.groupby('customer_id').agg({
    'purchase_amount': ['sum', 'mean', 'std', 'count'],
    'last_purchase_date': 'max'
}).reset_index()

customer_agg.columns = ['_'.join(col).strip('_') for col in customer_agg.columns]

# customer_id, purchase_amount_sum, purchase_amount_mean, purchase_amount_std, etc.
```

### Interaction Features
```python
# Multiplication
df['income_x_age'] = df['income'] * df['age']

# Ratio
df['debt_to_income'] = df['total_debt'] / (df['income'] + 1)  # +1 to avoid division by zero

# Polynomial features
from sklearn.preprocessing import PolynomialFeatures

poly = PolynomialFeatures(degree=2, include_bias=False)
poly_features = poly.fit_transform(df[['age', 'income']])
# age, income, age^2, age*income, income^2
```

### Domain-Specific Features
```python
# E-commerce: RFM features
df['recency'] = (pd.Timestamp.now() - df['last_purchase_date']).dt.days
df['frequency'] = df.groupby('customer_id')['order_id'].transform('count')
df['monetary'] = df.groupby('customer_id')['total_amount'].transform('sum')

# Finance: Credit risk
df['debt_to_income_ratio'] = df['total_debt'] / df['annual_income']
df['credit_utilization'] = df['credit_balance'] / df['credit_limit']
df['payment_to_income_ratio'] = df['monthly_payment'] / df['monthly_income']

# Time series: Lag features
df['sales_lag_1'] = df.groupby('product_id')['sales'].shift(1)
df['sales_lag_7'] = df.groupby('product_id')['sales'].shift(7)
df['sales_rolling_mean_7'] = df.groupby('product_id')['sales'].rolling(7).mean().values
```

---

## Text Features

```python
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

# Bag of words
vectorizer = CountVectorizer(max_features=100)
bow_features = vectorizer.fit_transform(df['review_text'])

# TF-IDF
tfidf = TfidfVectorizer(max_features=100, ngram_range=(1, 2))
tfidf_features = tfidf.fit_transform(df['review_text'])

# Length features
df['review_length'] = df['review_text'].str.len()
df['review_word_count'] = df['review_text'].str.split().str.len()

# Sentiment (using library)
from textblob import TextBlob
df['sentiment'] = df['review_text'].apply(lambda x: TextBlob(x).sentiment.polarity)
```

---

## Feature Selection

### Correlation-Based
```python
# Remove highly correlated features
corr_matrix = df.corr().abs()
upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))

to_drop = [column for column in upper.columns if any(upper[column] > 0.95)]
df_reduced = df.drop(columns=to_drop)
```

### Variance Threshold
```python
from sklearn.feature_selection import VarianceThreshold

# Remove low-variance features
selector = VarianceThreshold(threshold=0.01)
df_selected = selector.fit_transform(df)
```

### Univariate Selection
```python
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif

# Select top K features by F-score
selector = SelectKBest(score_func=f_classif, k=20)
X_selected = selector.fit_transform(X, y)

selected_features = X.columns[selector.get_support()]

# Mutual information
selector = SelectKBest(score_func=mutual_info_classif, k=20)
X_selected = selector.fit_transform(X, y)
```

### Model-Based Selection
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel

# Train model to get feature importances
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Select features above importance threshold
selector = SelectFromModel(rf, threshold='median')
X_selected = selector.fit_transform(X_train, y_train)

# Get feature importances
importances = pd.DataFrame({
    'feature': X.columns,
    'importance': rf.feature_importances_
}).sort_values('importance', ascending=False)
```

---

## Complete Pipeline

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

# Define feature types
numeric_features = ['age', 'income', 'credit_score']
categorical_features = ['city', 'education', 'occupation']

# Numeric pipeline
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# Categorical pipeline
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Combine pipelines
preprocessor = ColumnTransformer(transformers=[
    ('num', numeric_transformer, numeric_features),
    ('cat', categorical_transformer, categorical_features)
])

# Full ML pipeline
from sklearn.ensemble import RandomForestClassifier

pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier())
])

# Fit and predict
pipeline.fit(X_train, y_train)
predictions = pipeline.predict(X_test)
```

---

## Advanced Techniques

### Feature Hashing
```python
from sklearn.feature_extraction import FeatureHasher

# For high-cardinality categoricals
hasher = FeatureHasher(n_features=10, input_type='string')
hashed = hasher.transform(df['user_id'])
```

### Binning/Discretization
```python
# Equal-width bins
df['age_bin'] = pd.cut(df['age'], bins=5, labels=['Very Young', 'Young', 'Middle', 'Senior', 'Very Senior'])

# Quantile bins
df['income_quartile'] = pd.qcut(df['income'], q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'])

# Custom bins
bins = [0, 25, 50, 75, 100]
labels = ['Low', 'Medium', 'High', 'Very High']
df['score_category'] = pd.cut(df['score'], bins=bins, labels=labels)
```

### Embedding Features
```python
from sklearn.decomposition import PCA

# Dimensionality reduction
pca = PCA(n_components=10)
principal_components = pca.fit_transform(X_high_dim)

# Explained variance
print(f"Explained variance: {pca.explained_variance_ratio_.sum():.2%}")
```

---

## Feature Store Pattern

```python
class FeatureStore:
    """Centralized feature computation and storage"""
    
    def __init__(self, db_connection):
        self.db = db_connection
    
    def compute_customer_features(self, customer_id, as_of_date):
        """Compute features as of specific date (point-in-time)"""
        
        # Historical purchases before as_of_date
        purchases = self.db.query("""
            SELECT * FROM purchases
            WHERE customer_id = %s AND purchase_date < %s
        """, [customer_id, as_of_date])
        
        features = {
            'total_purchases': len(purchases),
            'total_spent': purchases['amount'].sum(),
            'avg_purchase_value': purchases['amount'].mean(),
            'days_since_last_purchase': (as_of_date - purchases['purchase_date'].max()).days,
            'favorite_category': purchases['category'].mode()[0]
        }
        
        return features
    
    def get_features(self, customer_ids, as_of_date):
        """Batch feature retrieval"""
        return [
            self.compute_customer_features(cid, as_of_date)
            for cid in customer_ids
        ]
```

---

## Validation & Monitoring

### Check for Data Leakage
```python
# Target leakage: feature computed using future info
df['future_purchases'] = df.groupby('customer_id')['purchase_amount'].shift(-1)  # WRONG!

# Correct: only use past data
df['past_avg_purchase'] = df.groupby('customer_id')['purchase_amount'].expanding().mean()

# Train/test contamination
from sklearn.model_selection import TimeSeriesSplit

tscv = TimeSeriesSplit(n_splits=5)
for train_idx, test_idx in tscv.split(X):
    X_train, X_test = X[train_idx], X[test_idx]
    # Fit scaler only on train, transform both
```

### Feature Distribution Monitoring
```python
def monitor_feature_drift(train_df, prod_df, feature):
    """Detect if production data distribution differs from training"""
    from scipy.stats import ks_2samp
    
    statistic, pvalue = ks_2samp(train_df[feature], prod_df[feature])
    
    if pvalue < 0.05:
        print(f"ALERT: {feature} distribution has changed (p={pvalue:.4f})")
    
    return pvalue
```

## Rules

- Always split data BEFORE feature engineering — prevent data leakage from test to train.
- Fit scalers/encoders on training set only, transform both train and test — avoid leakage.
- Handle missing values explicitly — missing can be informative, don't drop blindly.
- Create features from domain knowledge — interactions, ratios, aggregations specific to problem.
- Remove highly correlated features (>0.95) — reduce multicollinearity.
- Use pipelines for reproducibility — ensures same transformations in production.
- Feature selection after all transformations — select from engineered features, not raw.
- Validate features don't use future information — especially in time series (no shift(-1)).
- Monitor feature distributions in production — drift detection prevents model degradation.
- Document feature definitions — critical for reproducibility and debugging.
