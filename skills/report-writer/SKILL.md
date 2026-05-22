---
name: report-writer
description: >
  Draft, outline, edit, and format academic reports, research papers, and
  dissertation chapters. Applies APA 7 formatting, inserts citations, and
  uses workspace templates.
triggers:
  - write report
  - draft chapter
  - outline
  - edit document
  - format paper
  - write introduction
  - write literature review section
  - write methods section
  - write discussion
  - write conclusion
  - write abstract
  - research proposal
---

# Report Writer Skill

## Overview

This skill produces structured academic writing using templates from `/workspace/templates/`. It supports full paper drafts, individual chapters, abstracts, and proposals. All writing follows APA 7th edition conventions by default.

---

## Document Types Supported

| Document | Template | Output |
|---|---|---|
| Full research paper | `report_template.md` | `reports/paper_draft.md` |
| Research proposal | `research_proposal.md` | `reports/proposal.md` |
| Chapter 4 (Results) | `chapter4_stats_template.md` | `reports/chapter4_results.md` |
| Literature review section | Generate from matrix | `reports/literature_review.md` |
| Abstract | Inline generation | appended to draft |
| Presentation script | Inline generation | `slides/speaker_notes.md` |

---

## Step-by-Step Instructions

### Step 1 — Load the Appropriate Template

```python
import os

template_dir = "/workspace/templates/"

# Load template based on task
template_map = {
    "full_paper": "report_template.md",
    "proposal": "research_proposal.md",
    "chapter4": "chapter4_stats_template.md",
}

with open(os.path.join(template_dir, template_map["full_paper"])) as f:
    template = f.read()
print(template)
```

Read the template structure before writing. Fill in each section systematically.

### Step 2 — Check Available Resources

Before writing, check what's available in `/workspace/`:
```bash
ls /workspace/output/references/       # literature_matrix.csv, references.bib
ls /workspace/output/exports/          # statistical_results.xlsx, descriptive_statistics.xlsx
ls /workspace/output/charts/           # figures
ls /workspace/data/                    # raw data files
```

### Step 3 — Structure the Document

**IMRaD Structure (empirical papers)**:

```
Title: [Full paper title]
Author: [Name(s)]
Running head: [Short title]

Abstract (150-250 words)
Keywords: [5-7 keywords]

1. Introduction
   1.1 Background
   1.2 Problem Statement
   1.3 Research Questions/Objectives
   1.4 Significance of Study
   1.5 Scope and Limitations
   1.6 Definition of Terms

2. Literature Review
   2.1 [Thematic Section 1]
   2.2 [Thematic Section 2]
   2.3 Research Gap

3. Methodology
   3.1 Research Design
   3.2 Population and Sample
   3.3 Instruments
   3.4 Data Collection Procedure
   3.5 Data Analysis

4. Results
   4.1 Descriptive Statistics
   4.2 [Test 1 Results]
   4.3 [Test 2 Results]

5. Discussion
   5.1 Interpretation of Findings
   5.2 Comparison with Previous Studies
   5.3 Implications

6. Conclusion
   6.1 Summary
   6.2 Recommendations
   6.3 Future Research

References
Appendices
```

### Step 4 — Writing Guidelines

**Introduction**:
- Start broad → narrow funnel approach
- Cite 3-5 key papers establishing context
- State problem clearly: "Despite X, little is known about Y"
- End with explicit research question(s) or objective(s)

**Literature Review**:
- Organize thematically, not chronologically
- Each paragraph = one idea supported by multiple citations
- Use synthesis phrases: "Several studies have found..." / "While [A] argues X, [B] contends Y..."
- End with gap statement linking to your research

**Methodology**:
- Past tense for what was done
- Enough detail to replicate
- Justify choices: "A quantitative approach was adopted because..."

**Results** (use `statistical-analysis` skill output):
- Past tense, objective language
- Present tables/figures before narrating them
- Never interpret in Results section — only report

**Discussion**:
- Present tense for general statements, past tense for your results
- Compare each finding to literature: "This finding aligns with / contradicts / extends..."
- State limitations honestly

**Conclusion**:
- Summarize findings → implications → recommendations → future research
- Do not introduce new information

### Step 5 — Citation Insertion (APA 7)

**In-text citation patterns**:
```
# Parenthetical: (Author, Year)
(Smith, 2023)
(Smith & Jones, 2022)
(Smith et al., 2021)   # 3+ authors

# Narrative: Author (Year)
Smith (2023) found that...
Smith and Jones (2022) argued...
Smith et al. (2021) demonstrated...

# Direct quote: (Author, Year, p. X)
"Exact text" (Smith, 2023, p. 45)

# Two citations: (Smith, 2023; Jones, 2022)
```

**Reference list** is generated automatically from `/workspace/output/references/references.bib` using the export skill.

### Step 6 — APA Formatting Rules

**Headings**:
```
# Level 1: Centered, Bold, Title Case
## Level 2: Left-aligned, Bold, Title Case
### Level 3: Left-aligned, Bold Italic, Title Case
#### Level 4: Indented, Bold, Title Case, ends with period.
##### Level 5: Indented, Bold Italic, Title Case, ends with period.
```

**Numbers**: Spell out one through nine; use numerals for 10+. Exception: always use numerals for statistics, measurements, ages.

**Tables and Figures**: 
- Tables: `Table 1`, `Table 2` — above the table
- Figures: `Figure 1`, `Figure 2` — below the figure

### Step 7 — Save Draft

```python
output_path = "/workspace/output/reports/paper_draft.md"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w') as f:
    f.write(draft_content)
print(f"Draft saved to {output_path}")
```

---

## Editing Mode

When asked to **edit** an existing document:
1. Read the file from `/workspace/output/reports/` or user-specified path
2. Identify requested changes (grammar, flow, citations, restructuring)
3. Track changes conceptually — note before/after for significant revisions
4. Save edited version with `_v2` suffix (never overwrite original)

**Common edits**:
- Grammar and clarity: simplify long sentences, fix subject-verb agreement
- Academic tone: replace casual language with formal equivalents
- Citation checking: ensure all in-text citations have corresponding references
- Consistency: tense, heading levels, number formatting
