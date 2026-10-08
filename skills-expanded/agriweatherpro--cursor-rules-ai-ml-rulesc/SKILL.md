---
description: AI/ML Implementation Standards for AgriWeather Pro
globs: 
alwaysApply: true
---
---
globs: **/*.{py,ipynb,js}
---
# AI/ML Implementation

<rule>
name: ai_ml_implementation
description: Standards for AI/ML components in AgriWeather Pro
filters:
  - type: file_extension
    pattern: "\\.(py|ipynb|js)$"
  - type: content
    pattern: "model|prediction|ML|AI|train|tensorflow|pytorch|scikit"

actions:
  - type: suggest
    message: |
      # AI/ML Implementation Guidelines for AgriWeather Pro
      
      ## Model Development Standards
      
      1. **Weather Prediction Models**:
         - Use ensemble methods combining multiple weather sources
         - Implement transfer learning from pre-trained climate models
         - Calibrate predictions to local conditions using historical data
      
      2. **Crop Yield Prediction**:
         - Feature engineering should include:
           * Accumulated GDD (Growing Degree Days)
           * Precipitation distribution throughout growing season
           * Extreme weather event frequency
           * Soil moisture levels
         - Use time-series analysis for seasonal patterns
      
      3. **Model Training Template**:
         ```python
         def train_weather_crop_model(weather_features, yield_data, model_config):
             """
             Train a model that correlates weather patterns with crop yields
             
             Args:
                 weather_features: DataFrame of weather variables
                 yield_data: Historical yield information
                 model_config: Configuration parameters
                 
             Returns:
                 Trained model and performance metrics
             """
             # Preprocess
             X_train, X_test, y_train, y_test = preprocess_agri_data(
                 weather_features, 
                 yield_data, 
                 test_size=0.2
             )
             
             # Initialize model (prefer XGBoost or Random Forest for tabular data)
             model = initialize_model(model_config)
             
             # Train with cross-validation
             cv_results = cross_validate(
                 model, 
                 X_train, 
                 y_train, 
                 cv=5, 
                 scoring=['r2', 'neg_mean_absolute_error']
             )
             
             # Final training
             model.fit(X_train, y_train)
             
             # Evaluate
             metrics = evaluate_model(model, X_test, y_test)
             
             # Log results
             log_training_results(metrics, model_config)
             
             return model, metrics
         ```
      
      4. **Model Deployment**:
         - Version all models with clear changelog
         - Implement A/B testing for new prediction algorithms
         - Set up monitoring for model drift
         - Use lightweight models for edge computing on farm equipment

metadata:
  priority: high
  version: 1.0
</rule>