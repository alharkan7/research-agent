---
name: statistical-analysis
description: >
  Perform statistical analysis on user data. Returns results inline by default.
  Generates Excel tables, diagnostic plots, and Chapter 4 draft only when
  explicitly requested.
triggers:
  - analyze data
  - run stats
  - t-test
  - ANOVA
  - correlation
  - regression
  - descriptive statistics
  - significance test
  - statistical analysis
  - Chapter 4
  - results section stats
---

# Statistical Analysis Skill

## What to do based on what the user asked

| User request | Steps to run |
|---|---|
| "Analyze my data / run stats on X" | Steps 1–4. Show results inline in chat. |
| "Save the results as Excel" | Steps 1–4, then Step 5. |
| "Write a Chapter 4 / Results section" | Steps 1–5, then Step 6. |
| "Just run a t-test / correlation / [specific test]" | Step 1 (load), then only that test from Step 4. Show result inline. |
| "Descriptive stats for my data" | Steps 1–2 only. Show inline. |

**Default behavior: show results inline in chat. Only create files when explicitly asked.**

---

## Supported Tests

| Test | When to Use | Python Function |
|---|---|---|
| Descriptive statistics | Always — run first | `pandas.DataFrame.describe()` |
| Shapiro-Wilk normality | n < 50 | `scipy.stats.shapiro()` |
| Kolmogorov-Smirnov | n ≥ 50 | `scipy.stats.kstest()` |
| Independent t-test | 2 groups, continuous DV | `pingouin.ttest()` |
| Paired t-test | Pre/post, matched pairs | `pingouin.ttest(paired=True)` |
| One-way ANOVA | 3+ groups, continuous DV | `pingouin.anova()` |
| Repeated measures ANOVA | Within-subjects design | `pingouin.rm_anova()` |
| Pearson correlation | Linear relationship, normal | `pingouin.corr(method='pearson')` |
| Spearman correlation | Non-parametric / ordinal | `pingouin.corr(method='spearman')` |
| Linear regression | Predict continuous outcome | `statsmodels.formula.api.ols()` |
| Multiple regression | Multiple predictors | `statsmodels.formula.api.ols()` |
| Chi-square | Categorical variables | `scipy.stats.chi2_contingency()` |
| Mann-Whitney U | Non-parametric 2-group | `scipy.stats.mannwhitneyu()` |
| Kruskal-Wallis | Non-parametric 3+ groups | `scipy.stats.kruskal()` |
| Post-hoc (Tukey HSD) | After significant ANOVA | `pingouin.pairwise_tukey()` |

---

## Step 1 — Load and Inspect Data

```python
import pandas as pd
import numpy as np

df = pd.read_csv("/workspace/data/<filename>")  # or read_excel()
print(df.shape)
print(df.dtypes)
print(df.head())
print(df.isnull().sum())
```

Report: n, columns, data types, missing values. Ask how to handle missing data if any.

---

## Step 2 — Descriptive Statistics

```python
desc = df.describe().T
desc['median'] = df.median()
desc['skewness'] = df.skew()
desc['kurtosis'] = df.kurtosis()
print(desc[['count', 'mean', 'std', 'min', '50%', 'max', 'skewness', 'kurtosis']])
```

**APA format:** "The mean score for [Variable] was *M* = [value], *SD* = [value] (n = [n])."

---

## Step 3 — Normality Testing (run before inferential tests)

```python
from scipy import stats

for col in numeric_columns:
    if len(df[col].dropna()) < 50:
        stat, p = stats.shapiro(df[col].dropna())
        test_name = "Shapiro-Wilk"
    else:
        stat, p = stats.kstest(df[col].dropna(), 'norm')
        test_name = "Kolmogorov-Smirnov"
    normal = "normal" if p > 0.05 else "non-normal"
    print(f"{col}: {test_name} W={stat:.3f}, p={p:.3f} → {normal}")
```

If p > .05 → use parametric; if p ≤ .05 → use non-parametric equivalents.

---

## Step 4 — Inferential Tests

### Correlation
```python
import pingouin as pg
corr = pg.corr(df['var1'], df['var2'], method='pearson')
r = corr['r'].values[0]
p = corr['p-val'].values[0]
ci95 = corr['CI95%'].values[0]
print(f"r({n-2}) = {r:.2f}, p = {p:.3f}, 95% CI [{ci95[0]:.2f}, {ci95[1]:.2f}]")
```

### Independent t-test
```python
ttest = pg.ttest(group1, group2)
t = ttest['T'].values[0]; df_val = ttest['dof'].values[0]
p = ttest['p-val'].values[0]; d = ttest['cohen-d'].values[0]
print(f"t({df_val:.0f}) = {t:.2f}, p = {p:.3f}, d = {d:.2f}")
```

### Linear Regression
```python
import statsmodels.formula.api as smf
model = smf.ols('dependent_var ~ predictor1 + predictor2', data=df).fit()
print(f"R² = {model.rsquared:.3f}, F({model.df_model:.0f}, {model.df_resid:.0f}) = {model.fvalue:.2f}, p = {model.f_pvalue:.3f}")
```

---

## Step 5 — Save Results as Excel (only if requested)

```python
with pd.ExcelWriter("/workspace/output/exports/statistical_results.xlsx") as writer:
    desc.to_excel(writer, sheet_name="Descriptive Stats")
    corr_matrix.to_excel(writer, sheet_name="Correlations")
print("Saved: /workspace/output/exports/statistical_results.xlsx")
```

---

## Step 6 — Generate Chapter 4 Draft (only if requested)

```python
import subprocess
result = subprocess.run(
    ["python3", "/workspace/scripts/stats_report.py",
     "--results", "/workspace/output/exports/statistical_results.xlsx",
     "--output", "/workspace/output/reports/chapter4_results.md"],
    capture_output=True, text=True
)
```

The output follows the `/workspace/templates/chapter4_stats_template.md` structure.

---

## APA 7 Statistical Reporting Cheatsheet

| Statistic | APA Format |
|---|---|
| t-test | *t*(df) = value, *p* = .xxx, *d* = value |
| ANOVA | *F*(df1, df2) = value, *p* = .xxx, η² = value |
| Correlation | *r*(df) = value, *p* = .xxx |
| Regression | *R*² = .xxx, *F*(df1, df2) = value, *p* = .xxx |
| Chi-square | χ²(df, *N* = n) = value, *p* = .xxx, φ = value |
| Mean/SD | *M* = value, *SD* = value |

- Report exact p-values; exception: p < .001
- Always report effect sizes alongside significance
