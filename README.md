# Planning Permission Prediction — Socioeconomics & Access in Ireland

Using machine learning and SHAP explainability to investigate how socioeconomic conditions, access to public services, and infrastructure availability influence planning permission outcomes for one-off houses in Ireland.

## Overview

Ireland's [Project Ireland 2040](https://www.gov.ie/en/department-of-housing-local-government-and-heritage/publications/project-ireland-2040-national-planning-framework/) framework sets out national objectives to develop rural areas, maximise employment, and provide nationwide infrastructure. Yet planning permission approval rates are declining amid a record housing crisis. This project builds a diagnostic model to examine whether current planning authority decision-making aligns with these long-term policy goals.

By training a gradient boosting classifier on planning application data merged with 2022 Census data at the small area level, and extracting SHAP feature importance and interaction values, the project highlights where policy and practice diverge.

**This is a diagnostic tool for policy analysis — not a predictive system for determining future application outcomes.**

## Research Questions

1. Which factor — socioeconomic conditions, access to infrastructure, or access to public services — most significantly determines planning outcomes?
2. How do features across these categories interact to predict the likelihood of permission being granted?
3. Under what combinations of conditions are applications most likely to be rejected?

## Key Findings

- **Access to public services** is the most influential category, driven primarily by commute time — short commutes strongly predict approval, while 30–60+ minute commutes predict rejection
- **Low population density**, high personal vehicle use, and lower college education levels point to rural areas being most favoured for one-off housing approval
- Areas lacking **public water and sewerage** infrastructure face higher rejection rates, even in low-density regions — contradicting the government's stated goal of extending nationwide coverage
- The model uses **population density as a contextual moderator**: the same feature value (e.g. long commute, lack of sewerage) pushes predictions in opposite directions depending on urban vs rural setting
- Socioeconomic factors like employment rate and education ranked low in importance, suggesting limited demographic discrimination in planning decisions

## Methodology

1. **Data collection** — Irish planning application records (2012–present) merged with 8 Census 2022 datasets covering commuting, infrastructure, education, and employment at the small area level (~18,000 areas, ~300 residents each)
2. **Geocoding** — addresses converted to coordinates via the Photon API and spatially joined to Census small area boundaries; mismatched local authorities filtered out
3. **Baseline models** — logistic regression, random forest, XGBoost, and neural network trained with default parameters on an 80/20 stratified split
4. **Class imbalance handling** — 87% approval rate addressed via SMOTE, undersampling, oversampling, and class weighting; class-weighted XGBoost selected for best AUC + minority recall balance
5. **Hyperparameter tuning** — GridSearchCV to optimise learning rate, max depth, and other parameters
6. **Explainability** — SHAP importance values and pairwise interaction values computed to interpret model behaviour

## Final Model Performance

| Metric | Value |
|--------|-------|
| Accuracy | 0.670 |
| AUC | 0.675 |
| Recall (rejected) | 0.564 |
| F1 (rejected) | 0.306 |
| Recall (approved) | 0.685 |
| F1 (approved) | 0.783 |

## Features

| Access to Public Services | Access to Infrastructure | Socioeconomic Conditions |
|---------------------------|--------------------------|--------------------------|
| Commute via personal vehicle | Public water supply | Population density |
| Commute via public transport | Public sewerage system | Employment rate |
| Commute via walk/cycle | Central heating | No Leaving Cert qualification |
| Under 30 min commute | Renewable energy source | Third level education |
| 30–60 min commute | | |
| Over 60 min commute | | |

## Data Sources

- [Planning Application Sites](https://data.gov.ie/dataset/planning-application-sites1) — data.gov.ie
- [Census 2022 Small Area Data](https://www.geohive.ie/) — CSO via GeoHive (tables 6.5, 6.6, 6.7, 6.10, 8.1, 10.4, 11.1, 11.3)
- [CSO Small Area Boundaries](https://www.geohive.ie/datasets/7ff6cde006db4a98876c58de49f108b1_0/about) — 2022 ungeneralised geopackage
- [Photon Geocoding API](https://photon.komoot.io/) — OpenStreetMap-based geocoder

## Project Structure

```
├── data/                   # Source and processed datasets
├── code/                   # Jupyter notebooks and Python file for analysis and modelling
├── report/                 # Final technical report (PDF)
└── README.md
```

## Tech Stack

- Python, scikit-learn, XGBoost
- SHAP for model explainability
- GeoPandas for spatial joins
- Photon API for geocoding
- Matplotlib / Seaborn for visualisation

## Ethical Considerations

- All data publicly available under Creative Commons Attribution 4.0
- Personal identifiers (applicant names) removed; exact addresses replaced with Census small area codes in compliance with GDPR
- The merged dataset is not published to prevent misuse for real-world decision-making that could perpetuate historical biases

## License

MIT
