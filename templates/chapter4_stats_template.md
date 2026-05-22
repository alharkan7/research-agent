# Chapter 4: Results and Discussion

**Study Title:** [Full Study Title]
**Author:** [Name]
**Date:** [Month Year]

---

> **Instructions for the agent:** Fill in each `[PLACEHOLDER]` based on the statistical results from `/workspace/output/exports/statistical_results.xlsx` and the descriptive statistics from `/workspace/output/exports/descriptive_statistics.xlsx`. Use APA 7 formatting throughout. Tables should be numbered sequentially (Table 1, Table 2, etc.). Figures should reference files in `/workspace/output/charts/`.

---

## 4.1 Introduction to the Chapter

This chapter presents the findings of the study in response to the following research questions:

1. [RQ1]?
2. [RQ2]?
3. [RQ3]?

The results are organized to address each research question systematically. Statistical analyses were conducted using Python (scipy, pingouin, statsmodels). The significance level was set at α = .05 for all inferential tests.

---

## 4.2 Descriptive Statistics

Table 4.1 presents the descriptive statistics for all continuous variables in this study.

**Table 4.1**
*Descriptive Statistics for Study Variables (N = [n])*

| Variable | n | M | SD | Median | Min | Max | Skewness | Kurtosis |
|---|---|---|---|---|---|---|---|---|
| [Variable 1] | [n] | [M] | [SD] | [Mdn] | [min] | [max] | [skew] | [kurt] |
| [Variable 2] | [n] | [M] | [SD] | [Mdn] | [min] | [max] | [skew] | [kurt] |
| [Variable 3] | [n] | [M] | [SD] | [Mdn] | [min] | [max] | [skew] | [kurt] |

*Note.* M = mean; SD = standard deviation; Mdn = median.

**Narrative:** The descriptive statistics presented in Table 4.1 indicate that [Variable 1] had a mean of *M* = [value] (*SD* = [value]), with scores ranging from [min] to [max]. [Variable 2] showed a mean of *M* = [value] (*SD* = [value]). The distribution of [Variable 1] was [approximately normal/positively skewed/negatively skewed] (skewness = [value]).

---

## 4.3 Assumption Testing

Prior to conducting inferential analyses, assumptions were tested as follows.

### 4.3.1 Normality

The Shapiro-Wilk test (for n < 50) / Kolmogorov-Smirnov test (for n ≥ 50) was conducted to assess the normality of the distributions. Results indicated that [Variable 1] was [normally distributed / not normally distributed], *W* = [value], *p* = [value]. [Variable 2] was [normally distributed / not normally distributed], *W* = [value], *p* = [value].

[If non-normal:] Given the violation of normality assumptions, non-parametric equivalents were used for [Variable X].

### 4.3.2 Homogeneity of Variance *(if applicable)*

Levene's test for equality of variances was conducted prior to the independent samples t-test. Results indicated that the assumption of homogeneity of variance was [met / violated], *F*([df1], [df2]) = [value], *p* = [value].

---

## 4.4 Research Question 1: [State RQ1]

### Findings

**[Test used, e.g., Pearson Correlation / Independent t-test / One-way ANOVA / Simple Linear Regression]**

**[Example: Correlation]**

A Pearson product-moment correlation was conducted to examine the relationship between [Variable X] and [Variable Y]. Results indicated a [positive/negative/no] statistically [significant/non-significant] correlation, *r*([df]) = [value], *p* = [value], 95% CI [[lower], [upper]]. This represents a [small/medium/large] effect size based on Cohen's (1988) guidelines (*r* < .10 = small, .10–.30 = medium, > .30 = large). Figure 4.1 illustrates the scatter plot of this relationship.

*(Insert Figure 4.1 here)*

**Figure 4.1**
*Scatter Plot of [Variable X] and [Variable Y] (r = [value], p = [value])*

**[Example: Independent t-test]**

An independent samples t-test was conducted to compare [Variable] between [Group 1] and [Group 2]. [Group 1] (*M* = [value], *SD* = [value]) scored significantly [higher/lower/the same] than [Group 2] (*M* = [value], *SD* = [value]), *t*([df]) = [value], *p* = [value], Cohen's *d* = [value]. This represents a [small/medium/large] effect. Figure 4.X presents the group means.

**[Example: ANOVA]**

A one-way analysis of variance (ANOVA) was conducted to compare [Variable] across [k] groups. Results revealed a statistically significant difference among groups, *F*([df1], [df2]) = [value], *p* = [value], η² = [value], indicating a [small/medium/large] effect. Post hoc analyses using the Tukey HSD test revealed that [Group A] (*M* = [value]) differed significantly from [Group B] (*M* = [value]), *p* = [value], but not from [Group C], *p* = [value].

**Table 4.2**
*ANOVA Summary Table*

| Source | SS | df | MS | F | p | η² |
|---|---|---|---|---|---|---|
| Between Groups | | | | | | |
| Within Groups | | | | | | |
| Total | | | | | | |

**[Example: Linear Regression]**

A simple linear regression was performed to predict [Dependent Variable] from [Predictor Variable]. The model was statistically significant, *F*([df1], [df2]) = [value], *p* = [value], *R*² = [value], indicating that [Predictor] explained [%]% of the variance in [DV]. The regression equation was: Ŷ = [intercept] + [slope]([Predictor]), *b* = [value], *SE* = [value], *t*([df]) = [value], *p* = [value].

**Table 4.3**
*Regression Coefficients for [DV] Predicted by [IV]*

| Predictor | b | SE | β | t | p | 95% CI |
|---|---|---|---|---|---|---|
| (Constant) | | | — | | | |
| [Predictor 1] | | | | | | [LL, UL] |
| [Predictor 2] | | | | | | [LL, UL] |

*Note.* b = unstandardized coefficient; SE = standard error; β = standardized coefficient. *R*² = [value].

**Summary for RQ1:**
In summary, the results [support/do not support] [Hypothesis 1 or expectation]. [One-sentence plain-language summary of key finding].

---

## 4.5 Research Question 2: [State RQ2]

*(Repeat the structure from 4.4 for RQ2)*

---

## 4.6 Research Question 3: [State RQ3]

*(Repeat the structure from 4.4 for RQ3)*

---

## 4.7 Correlation Matrix (if multiple variables)

Table 4.X presents the intercorrelations among all study variables.

**Table 4.X**
*Pearson Correlations Among Study Variables*

| Variable | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| 1. [Variable 1] | — | | | |
| 2. [Variable 2] | [r] | — | | |
| 3. [Variable 3] | [r] | [r] | — | |
| 4. [Variable 4] | [r] | [r] | [r] | — |

*Note.* Values marked with * are significant at p < .05 (two-tailed); ** p < .01; *** p < .001.

---

## 4.8 Summary of Findings

Table 4.X summarizes the results for all research questions.

**Table 4.X**
*Summary of Inferential Statistical Results*

| Research Question | Test Used | Test Statistic | df | p-value | Effect Size | Decision |
|---|---|---|---|---|---|---|
| RQ1: [brief] | [test] | [stat] = [value] | [df] | [p] | [ES type] = [value] | [Supported/Not Supported] |
| RQ2: [brief] | [test] | [stat] = [value] | [df] | [p] | [ES type] = [value] | [Supported/Not Supported] |
| RQ3: [brief] | [test] | [stat] = [value] | [df] | [p] | [ES type] = [value] | [Supported/Not Supported] |

Overall, [X out of Y] research questions yielded statistically significant results at α = .05. The following chapter discusses these findings in relation to the existing literature.
