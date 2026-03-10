# Report 1: Are Headtracking Measures an Indicator of Depressive Symptoms?

## Team Members

- Priyanshu Sharma [2024201046]
- Amarnath Kumar [2024202024]
- Prakhar Kesari [2024202023]

## Repository
- [Github-Repository](https://github.com/ps600779/360-Videos-VR-Project)

## 1. Introduction

This report analyzes whether head-tracking metrics from 360° VR videos are associated with depressive symptoms in college students. The project hypothesis (from the experiment brief) is that participants with higher depressive symptoms may show a stunted psychomotor response (e.g., lower movement speed and reduced variability), potentially linked to anhedonia and psychomotor slowing.

The analysis scope:-

- data organization and unit of analysis,
- visualization and summarization,
- inferential hypothesis testing,
- probability/distribution assumptions,
- sampling-based inference,
- multiple-comparison correction.

### Dataset overview

- Source file: `data/data.xlsx`
- Participants: **40**
- Videos per participant: **5** (`v1` to `v5`)
- Total video-level observations: **200**
- Headtracking source files: `data/headtracking-data/v1 ... v5/*.csv`

Participant-level psychological measures include:
- `score_phq` (PHQ-9 depressive symptoms),
- `score_gad` (GAD-7 anxiety symptoms),
- `score_stai_t`, `score_vrise`, and affect variables.

Headtracking files provided per-video summary rows with:
- circular average position (X, Y, Z),
- circular SD position (X, Y, Z),
- average rotation speed (X, Y, Z, total).

This report uses **rotation speed total** as the primary psychomotor speed measure and the average of circular SD across X/Y/Z as a movement-variability measure.

## 2. Methods

## 2.1 Data organization and preprocessing

Following slide guidance on data organization and unit of analysis:
- The primary inferential unit for depression analyses was **participant-level** (video means aggregated per participant).
- For video-type effects, the unit was **within-participant repeated observations** across five videos.

Processing steps:
1. Loaded `data.xlsx` and matched each participant’s `v1`–`v5` filename to corresponding headtracking CSV.
2. Extracted summary metrics from each CSV’s final line.
3. Built:
   - a long video-level table (`long_video_metrics.csv`),
   - a participant-level table (`participant_level_metrics.csv`).

## 2.2 Outlier identification and decision

As taught in data visualization/summarization slides, outliers were screened using the IQR rule (1.5 × IQR) on rotation speed total within each video.

- Outliers detected: **1** video-level point (in `v2`, value = 8.49).
- Decision: **Retained**.

Reasoning:
- It is a plausible behavioral value (not a data-entry artifact).
- Excluding a single valid low-response observation in a small sample (N=40) can bias effect estimates.
- Robustness is handled by reporting distributions and effect sizes, not only p-values.

## 2.3 Group partitioning for depression hypothesis

To create interpretable groups for the central hypothesis, participants were split using a standard PHQ-9 threshold:
- **Elevated depression**: PHQ-9 >= 10
- **Low depression**: PHQ-9 < 10

Group counts:
- Low depression: **32**
- Elevated depression: **8**

This preserves the hypothesis focus while remaining clinically interpretable.

## 2.4 Inferential strategy


1. **Descriptive statistics and visualization**
   - Histograms, box/strip plots, point plots with confidence intervals.

2. **Group hypothesis tests**
   - Independent-samples t-tests (Welch) for elevated vs low depression groups on:
     - mean rotation speed total,
     - mean circular SD.
   - Effect size: Cohen’s d.

3. **Associations with symptom scales**
   - Pearson correlation of PHQ and GAD with psychomotor metrics.

4. **Reconciling depression–anxiety covariance**
   - Multiple linear regression with both PHQ and GAD entered simultaneously to estimate unique contributions.

5. **Video-type psychomotor differences**
   <!-- - Repeated-measures ANOVA across five videos for rotation speed total. -->
   - Post-hoc paired t-tests with **Bonferroni correction**.

Alpha was 0.05 unless otherwise stated.

## 3. Results

### 3.1 Descriptive overview

PHQ/GAD covariance was substantial:
- $r = 0.579$, $p < .001$

This confirms the expected overlap between depression and anxiety symptom scores.

### 3.1.1 Correlation matrix (participant-level variables)

To summarize linear relationships across key psychological and headtracking variables, a Pearson correlation matrix was computed for:
- PHQ-9 (`score_phq`)
- GAD-7 (`score_gad`)
- STAI-T (`score_stai_t`)
- VRISE (`score_vrise`)
- mean rotation speed total (`rot_speed_avg_total`)
- mean circular SD (`circ_sd_mean`)

| Variable | PHQ-9 | GAD-7 | STAI-T | VRISE | Speed | Variability |
|---|---:|---:|---:|---:|---:|---:|
| PHQ-9 | 1.000 | 0.579 | 0.642 | -0.170 | -0.060 | 0.229 |
| GAD-7 | 0.579 | 1.000 | 0.697 | -0.040 | 0.048 | 0.410 |
| STAI-T | 0.642 | 0.697 | 1.000 | 0.022 | -0.012 | 0.224 |
| VRISE | -0.170 | -0.040 | 0.022 | 1.000 | 0.089 | -0.023 |
| Speed | -0.060 | 0.048 | -0.012 | 0.089 | 1.000 | -0.061 |
| Variability | 0.229 | 0.410 | 0.224 | -0.023 | -0.061 | 1.000 |

Interpretation:
- Symptom scales cluster together (PHQ, GAD, STAI-T are positively intercorrelated).
- Speed has near-zero correlations with symptom variables.
- Variability has its strongest positive relationship with anxiety (GAD), which supports the regression finding in Section 3.3.

![PHQ-9 score distribution across participants](analysis_outputs/figures/fig1_phq_distribution.png){width=50%}

![ Overall distribution of rotation speed across all video-level observations](analysis_outputs/figures/fig6_dataset_speed_distribution.png){width=60%}


### 3.2 Central hypothesis: depression and psychomotor response

#### A) Depression groups (PHQ-9 threshold)

**Mean rotation speed total**
- Elevated depression (n=8): 32.68
- Low depression (n=32): 32.31
- Welch t-test: $t = 0.13$, $p = .898$, $d = 0.05$

**Mean circular SD (variability)**
- Elevated depression: 32.35
- Low depression: 27.17
- Welch t-test: $t = 0.92$, $p = .381$, $d = 0.40$

Interpretation:
- No statistically significant group difference in psychomotor speed.
- Variability shows a small-to-moderate numeric increase in elevated depression, but not significant with current sample size.

![Rotation speed by depression group](analysis_outputs/figures/fig2_speed_by_depression_group.png){width=50%}

#### B) Continuous symptom associations

**PHQ correlations**
- PHQ vs speed: $r = -0.060$, $p = .712$
- PHQ vs variability: $r = 0.229$, $p = .155$

Interpretation:
- Depression severity does not show a reliable linear association with speed or variability in this sample.

![Symptom scores vs movement variability](analysis_outputs/figures/fig3_symptoms_vs_variability.png)

### 3.3 Reconciling depression vs anxiety overlap

Regression with both PHQ and GAD as predictors:

**Outcome: speed**
- PHQ: $\beta = -0.263$, $p = .512$
- GAD: $\beta = 0.266$, $p = .536$
- $R^2 = .014$

**Outcome: variability**
- PHQ: $\beta = -0.031$, $p = .945$
- GAD: $\beta = 1.088$, $p = .029$
- $R^2 = .168$

Interpretation:
- After accounting for shared variance, **anxiety (GAD)**—not depression—shows a significant unique association with movement variability.
- This is an important conceptual result given the known covariance between anxiety and depression.

### 3.4 Do different videos elicit different psychomotor responses?

Video-wise speed means:
- V1: 39.08
- V2: 32.75
- V3: 34.87
- V4: 24.17
- V5: 31.03

<!-- Repeated-measures ANOVA:
- $F(4,156) = 34.58$, $p < .001$ -->

Bonferroni-corrected pairwise results:
- Significant: V1>V2, V1>V3, V1>V4, V1>V5, V2>V4, V3>V4, V3>V5, V5>V4
- Non-significant after correction: V2 vs V3, V2 vs V5

Interpretation:
- Video context strongly changes head-movement speed.
- V4 (horror clip) produced the lowest speed on average, while V1 was highest.

Possible behavioral explanation (consistent with design/measurement framing from course):
- Different scene dynamics, emotional valence/arousal, attentional focus, and motor strategy demands likely drive distinct movement profiles.
- Psychomotor response in VR appears **stimulus-dependent**, not just trait-dependent.

![Video-wise rotation speed comparison](analysis_outputs/figures/fig4_video_speed_pointplot.png){width=50%}

## 4. Replication judgment and additional insights

### Replication of original claim (depression → stunted psychomotor response)

Based on this sample and current metrics:
- The core depression-specific effect is **not clearly replicated**.
- Directional evidence for slower movement in higher depression is weak to absent.

### Additional insights beyond the original central question

1. Anxiety appears more tightly related to movement variability than depression when both are modeled together.
2. Video content has a strong and robust effect on psychomotor behavior.
3. Any future depression-linked effect should model content/context explicitly (video type as a major source of variance).

## 5. Conclusion and next steps

### Conclusion

Using only BRSM-taught concepts and methods, this analysis shows:
- No significant depression-group difference in head-movement speed,
- No strong PHQ-only linear effect,
- Significant anxiety-linked increase in movement variability (when controlling overlap),
- Strong and reliable video-dependent differences in psychomotor response.

### Practical next steps for Report 2

1. Add preregistered primary outcome(s) and planned contrasts.
2. Model repeated measures more explicitly for both symptom and video effects.
3. Integrate valence/arousal/presence scores as predictors/moderators of movement metrics.
4. Report confidence intervals for all key effects and maintain correction for multiple testing.

## 6. Files generated for reproducibility

- Analysis script: `analysis_outputs/run_analysis.py`
- Output tables:
  - `analysis_outputs/group_tests.csv`
  - `analysis_outputs/correlations.csv`
   - `analysis_outputs/correlation_matrix.csv`
  - `analysis_outputs/regression_controls.csv`
  - `analysis_outputs/anova_speed.txt`
  - `analysis_outputs/pairwise_video_tests_bonferroni.csv`
- Figures:
  - `analysis_outputs/figures/fig1_phq_distribution.png`
  - `analysis_outputs/figures/fig2_speed_by_depression_group.png`
  - `analysis_outputs/figures/fig3_symptoms_vs_variability.png`
  - `analysis_outputs/figures/fig4_video_speed_pointplot.png`
   - `analysis_outputs/figures/fig5_correlation_matrix_heatmap.png`

## 7. Team Contributions

- **Priyanshu Sharma [2024201046]:** Led project coordination, cleaned and merged participant-level and headtracking data, and drafted the Introduction/Conclusion sections.
- **Amarnath Kumar [2024202024]:** Implemented descriptive and inferential analyses (group tests, post-hoc comparisons) and verified statistical outputs.
- **Prakhar Kesari [2024202023]:** Prepared visualizations (distribution, group, video-wise, and correlation matrix plots), compiled Results interpretation, and finalized formatting/references.

## 8. References

### Course materials (used for concepts and methods)

- BRSM_L1_DataVisualization_Summarization_S26.pdf
- BRSM_L2_DataVisualization_Summarization_S26.pdf
- Data Visualization and Summarization.pdf
- Hypothesis testing .pdf
- Multiple Comparisons.pdf
- Probability Distribution.pdf
- Sampling_and_estimating_quantities_Lec4.pdf

### Domain/measurement references from experiment brief

- What Do Head Scans Reveal About Depression? Insights from 360° Psychomotor Assessment. (2025)
- Development and validation of brief measures of positive and negative affect: the PANAS scales. (1988)
- Validation of the Virtual Reality Neuroscience Questionnaire: Maximum Duration of Immersive Virtual Reality Sessions Without the Presence of Pertinent Adverse Symptomatology. (2019)
- Mental Health, Suicidality, Health, and Social Indicators Among College Students Across Nine States in India. (2024)
- PHQ-9 (standardized clinical resource)
- A brief measure for assessing generalized anxiety disorder: the GAD-7. (2006)
- State-Trait Anxiety Inventory (STAI)
- Measuring Presence in Virtual Environments: A Presence Questionnaire. (1998)
- A Circumplex model of Affect (Russell, 1980)
- The Critical Relationship Between Anxiety and Depression. (2020)
