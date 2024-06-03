# XAI BiciMAD age-cohort prediction | Project Overview
- This tool is designed to estimate the age range of BiciMAD users based on trip generation data for Year 2019, while also revealing the key determinants. This functionality is particularly valuable as this specific information has not been available since July 2021.
- The target audience for this tool are micromobility service companies and relevant institutions for refining their promotional strategies for Bike Sharing Systems in Madrid.
- Due to the significant data imbalance across categories, it was evaluated the potential advantages of using oversampling techniques like SMOTE. This consideration was made with an awareness of the possible impact on model explainability variance.

## Dataset Description

![image](https://github.com/jdecampo/xai_age_cohort_prediction_bss/blob/main/reports/assets/model_selected_features.png)


## Project Reference(s):
- Data Sources:
1. [BiciMAD BSS hourly trips.](https://opendata.emtmadrid.es/Datos-estaticos/Datos-generales-(1))
2. [BiciMAD Station hourly status.](https://opendata.emtmadrid.es/Datos-estaticos/Datos-generales-(1))
3. [Meteorological daily data for Madrid.](https://datos.madrid.es/portal/site/egob)
4. [Working calendar for Autonomous-Community of Madrid.](https://datos.madrid.es/portal/site/egob)

- Snippets of code, derived from existing solutions, have been annotated and included as inline comments.

Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── reports            <- Generated analysis as HTML, PDF, PNG, etc.
    │   ├── assets         <- Generated assets as PNG, for project overview.
    │   └── figures        <- Generated graphics and figures to be used in reporting.
    │
    └── src                <- Source code for use in this project.
        ├── 00_data           <- Scripts to download or generate data
        │   ├── processed      <- The final merged data sets for modeling.
        │   └── raw            <- The original data dump with required data cleaning steps.
        │
        ├── 10_eda            <- Scripts to create Exploratory Data Analysis results.
        │       
        ├── 20_features       <- Scripts to turn raw data into features for modeling
        │   └── feature_creation_full_dataset.ipynb
        │
        └──  30_baseline_models <- Scripts to train baseline models and then use trained models to make
            │                 predictions.
            └── baseline_models_2019_age-group_3_4_5.ipynb

## EDA

## Methodology Pipeline:

## Model Performance:

## XAI: 

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
