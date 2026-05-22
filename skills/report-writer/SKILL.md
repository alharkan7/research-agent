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

## What to do based on what the user asked

| User request | What to do |
|---|---|
| "Write a [section]" (intro, discussion, etc.) | Write that section inline in chat. Save only if asked. |
| "Write a full paper / full report" | Use the full IMRaD structure. Load template. Save to reports/. |
| "Outline my paper" | Generate outline inline. |
| "Edit this document" | Read the file, make changes, save with `_v2` suffix. |
| "Write an abstract" | Write it inline. |
| "Write a research proposal" | Use the proposal template. Save to reports/. |

**Default: write inline in chat. Only create files when writing a full document or when user asks to save.**

---

## Document Templates Available

Check `/workspace/templates/` before writing full documents:

| Template | Use for |
|---|---|
| `report_template.md` | Full research paper |
| `research_proposal.md` | Research proposal |
| `chapter4_stats_template.md` | Results/Chapter 4 |

Load a template only when writing a full document:
```python
with open("/workspace/templates/report_template.md") as f:
    template = f.read()
print(template)
```

---

## IMRaD Structure (for full papers)

```
Abstract (150–250 words)
Keywords: [5–7 keywords]

1. Introduction
   1.1 Background
   1.2 Problem Statement
   1.3 Research Questions/Objectives
   1.4 Significance
   1.5 Scope and Limitations

2. Literature Review
   2.1 [Thematic Section 1]
   2.2 [Thematic Section 2]
   2.3 Research Gap

3. Methodology
   3.1 Research Design
   3.2 Sample
   3.3 Instruments
   3.4 Data Collection
   3.5 Data Analysis

4. Results
   4.1 Descriptive Statistics
   4.2 [Test 1 Results]
   4.3 [Test 2 Results]

5. Discussion
   5.1 Interpretation
   5.2 Comparison with Literature
   5.3 Implications

6. Conclusion
   6.1 Summary
   6.2 Recommendations
   6.3 Future Research

References
Appendices
```

---

## Section Writing Guidelines

**Introduction**: Broad → narrow funnel. Cite 3–5 papers for context. End with clear research question(s).

**Literature Review**: Organize thematically, not chronologically. Each paragraph = one idea + multiple citations. End with gap statement.
- Synthesis phrases: "Several studies have found..." / "While [A] argues X, [B] contends Y..."

**Methodology**: Past tense. Enough detail to replicate. Justify choices.

**Results**: Past tense, objective. Present tables/figures before narrating. Never interpret here.

**Discussion**: Compare each finding to literature: "This finding aligns with / contradicts / extends..." State limitations.

**Conclusion**: Summary → implications → recommendations → future research. No new information.

---

## Citation Formatting (APA 7)

```
(Smith, 2023)                   # Parenthetical
Smith (2023) found that...      # Narrative
(Smith & Jones, 2022)
(Smith et al., 2021)            # 3+ authors
"Exact text" (Smith, 2023, p. 45)
(Smith, 2023; Jones, 2022)      # Multiple citations
```

**Heading levels:**
```
# Level 1: Centered, Bold, Title Case
## Level 2: Left-aligned, Bold, Title Case
### Level 3: Left-aligned, Bold Italic, Title Case
```

**Numbers**: Spell out one–nine; numerals for 10+. Always numerals for statistics.

---

## Saving Files

When saving a full document:
```python
output_path = "/workspace/output/reports/paper_draft.md"
with open(output_path, 'w') as f:
    f.write(draft_content)
print(f"Saved: {output_path}")
```

When editing: save with `_v2` suffix, never overwrite the original.

---

## Editing Mode

When asked to edit an existing document:
1. Read the file from the path the user specifies (or `/workspace/output/reports/`)
2. Make the requested changes (grammar, tone, citations, restructuring)
3. Save with `_v2` suffix
4. Report: what was changed and why

Common edits: simplify long sentences, fix subject-verb agreement, replace casual language, check citation consistency.
