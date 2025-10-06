💤 Sleep–Stress Analysis

[![Medium](https://img.shields.io/badge/Read_on-Medium-black?logo=medium)](https://medium.com/@danliontario/how-stress-and-lifestyle-predict-sleep-quality-and-disorders-a-data-driven-analysis-82301b82bb36)  
[![Portfolio](https://img.shields.io/badge/View-Portfolio-blue?logo=react)](https://dlport.web.app/)  


📖 Project Overview

Sleep quality is a critical marker of both mental and physical well-being.
This project investigates how stress, physical activity, and physiological variables (heart rate, age, sleep duration) influence sleep quality and the risk of sleep disorders such as insomnia and sleep apnea.

The goal was to quantify these relationships and build statistical models that explain both continuous outcomes (sleep quality) and categorical outcomes (type of sleep disorder).

🧪 Methods

- Tools: Python (Pandas, Statsmodels, Seaborn, Matplotlib)
- Models:OLS Regression (3 stages), Multinomial Logistic Regression (sleep disorder classification)
- Dataset: 374 adult records with 15 variables (age, stress, sleep duration, heart rate, physical activity, etc.)
- Outputs: Full model summaries, correlation heatmaps, and predicted probability visualizations.

📊 Key Findings

- Stress alone explained ≈81% of the variance in sleep quality — the strongest single predictor.
- Physical activity improves sleep but does not fully offset stress effects.
- Adding physiological factors (age, heart rate, duration) increased R² to 0.87, indicating strong overall model fit.

Sleep disorder prediction:
- High stress and low quality → greater odds of Insomnia.
- Elevated heart rate and older age → greater odds of Sleep Apnea.
- The extended multinomial model achieved a Pseudo R² ≈ 0.51, showing strong predictive capability.

🧩 Interpretation

- Stress emerges as the central determinant of poor sleep, but its impact is moderated by behavioral (activity) and physiological (age, heart rate) buffers.
- Together, these results illustrate how psychological pressure translates into biological strain and measurable sleep pathology.
