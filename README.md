# Cognito — AI Decision Style Analyzer

Cognito is a Django-based cognitive science project that analyzes human decision-making behavior using machine learning.

## Concept
The system models decision-making using behavioral signals:
- response time
- hesitation patterns
- consistency across questions

These are mapped to cognitive styles:
- Impulsive (fast, intuitive)
- Analytical (slow, deliberate)
- Balanced

## ML Approach
- Synthetic behavioral dataset (with noise + overlap)
- Feature engineering (timing + hesitation metrics)
- Random Forest classifier
- Confidence-based prediction

## Features
- Interactive quiz UI
- Real-time behavioral tracking
- ML-based prediction
- Confidence score
- Response time visualization
- Admin dashboard for data inspection

## Tech Stack
- Django
- Python
- Scikit-learn
- Chart.js
- SQLite

## Future Improvements
- Real user dataset collection
- Model retraining
- Advanced explainability
- Personalized feedback

## Run Locally

```bash
pip install -r requirements.txt
python manage.py runserver
