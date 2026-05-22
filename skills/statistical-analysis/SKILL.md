---
name: statistical-analysis
description: >
  Perform descriptive statistics, common inferential tests (t-test, ANOVA,
  correlation, regression), and generate APA-formatted results tables and
  Chapter 4 sections from user data files.
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

## Overview

This skill loads user data, runs appropriate statistical tests, and produces:
- APA 7th-edition formatted results narrative
- Summary statistics tables (saved as `.xlsx`)
- Chapter 4 (Results) section draft
- Diagnostic plots (normality, residuals, etc.)

---

## Supported Tests

| Test | When to Use | Python Function |
|---|---|---|
| Descriptive statistics | Always — run first | `pingouin.describe()` or `pandas.DataFrame.describe()` |
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

## Step-by-Step Instructions

### Step 1 — Load and Inspect Data

```python
import pandas as pd
import numpy as np

# Load the data file (CSV, XLSX, or JSON)
df = pd.read_csv("/workspace/data/<filename>")  # or read_excel()

# Basic inspection
print(df.shape)
print(df.dtypes)
print(df.head())
print(df.isnull().sum())
```

Report:
- Number of rows (n) and columns
- Data types of each variable
- Missing values per column
- Ask user how to handle missing data (listwise deletion, mean imputation, etc.)

### Step 2 — Descriptive Statistics

```python
import pingouin as pg

# For all numeric columns
desc = df.describe().T
desc['median'] = df.median()
desc['skewness'] = df.skew()
desc['kurtosis'] = df.kurtosis()

print(desc[['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max', 'skewness', 'kurtosis']])

# Save to Excel
desc.to_excel("/workspace/output/exports/descriptive_statistics.xlsx")
```

**APA reporting format:**
> "Descriptive statistics are presented in Table 1. The mean score for [Variable] was *M* = [value], *SD* = [value] (n = [n])."

### Step 3 — Normality Testing

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

Decide: if p > .05 → use parametric tests; if p ≤ .05 → use non-parametric equivalents.

### Step 4 — Inferential Tests

#### Correlation
```python
corr = pg.corr(df['var1'], df['var2'], method='pearson')
r = corr['r'].values[0]
p = corr['p-val'].values[0]
ci95 = corr['CI95%'].values[0]

# APA format:
print(f"r({n-2}) = {r:.2f}, p = {p:.3f}, 95% CI [{ci95[0]:.2f}, {ci95[1]:.2f}]")
```

#### Independent t-test
```python
ttest = pg.ttest(group1, group2)
t = ttest['T'].values[0]
df_val = ttest['dof'].values[0]
p = ttest['p-val'].values[0]
d = ttest['cohen-d'].values[0]

# APA format:
print(f"t({df_val:.0f}) = {t:.2f}, p = {p:.3f}, d = {d:.2f}")
```

#### Linear Regression
```python
import statsmodels.formula.api as smf

model = smf.ols('dependent_var ~ predictor1 + predictor2', data=df).fit()
print(model.summary())

# Extract key values:
r2 = model.rsquared
f_stat = model.fvalue
f_p = model.f_pvalue
print(f"R² = {r2:.3f}, F({model.df_model:.0f}, {model.df_resid:.0f}) = {f_stat:.2f}, p = {f_p:.3f}")
```

### Step 5 — Generate Results Tables (Excel)

```python
# Save all results to Excel with multiple sheets
with pd.ExcelWriter("/workspace/output/exports/statistical_results.xlsx") as writer:
    desc.to_excel(writer, sheet_name="Descriptive Stats")
    corr_matrix.to_excel(writer, sheet_name="Correlations")
    # Add other result sheets...
```

### Step 6 — Generate Chapter 4 Draft

```python
# Use the Chapter 4 template
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

**Notes:**
- Report exact p-values (not p < .05); exception: p < .001
- Use italics for statistical symbols in final Word doc
- Always report effect sizes alongside significance

---

## Output Files

| File | Location |
|---|---|
| Descriptive statistics | `/workspace/output/exports/descriptive_statistics.xlsx` |
| All statistical results | `/workspace/output/exports/statistical_results.xlsx` |
| Chapter 4 draft | `/workspace/output/reports/chapter4_results.md` |
| Diagnostic plots | `/workspace/output/charts/` |
