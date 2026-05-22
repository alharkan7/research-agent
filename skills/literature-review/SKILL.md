---
name: literature-review
description: >
  Search academic databases and return papers. Produces a reference list by
  default. Generates CSV matrix, BibTeX, annotated bibliography, and gap
  analysis only when explicitly requested.
triggers:
  - full literature review
  - annotated bibliography
  - literature matrix
  - research gap analysis
  - systematic review
---

# Literature Review Skill

## Overview

This skill searches academic sources and returns papers. The **default output is a formatted reference list in chat**. Extended outputs (CSV matrix, BibTeX file, gap analysis, annotated bibliography) are only generated when the user explicitly asks for them.

---

## What to do based on what the user asked

| User request | Steps to run |
|---|---|
| "Find N papers on X" | Steps 1–2 only. Return list in chat. Optionally save `.bib` if user said "save" or "references". |
| "Find papers and save references" | Steps 1–2, then save BibTeX. Show file path. |
| "Full literature review on X" | All steps 1–7. |
| "Annotated bibliography" | Steps 1–2, then Step 7. |
| "Research gap analysis" | Steps 1–2, then Step 6. |
| "Literature matrix / CSV" | Steps 1–3. |

---

## Step 1 — Understand the Search Request

Clarify (infer from context, don't ask unless ambiguous):
1. **Topic / keywords** — extract from user message
2. **Number of papers** — default: whatever user asked for (or 10 if unspecified)
3. **Date range** — default: last 5 years unless specified
4. **Language** — default: English only

---

## Step 2 — Search Sources

Run searches using the Python script:

```python
import subprocess
result = subprocess.run(
    ["python3", "/workspace/scripts/search_papers.py",
     "--query", "<TOPIC>",
     "--limit", "<N>",
     "--years", "5"],
    capture_output=True, text=True
)
print(result.stdout)
```

**Source priority order:**
1. **Semantic Scholar** (best coverage, free API) — uses `SEMANTIC_SCHOLAR_API_KEY` from `/workspace/.env`
2. **OpenAlex** (open scholarly graph) — uses `OPENALEX_EMAIL`
3. **CrossRef** (DOI metadata) — uses `CROSSREF_MAILTO`
4. **arXiv** (preprints)
5. **PubMed** (medical/biological, via `NCBI_API_KEY`)

**Fallback** if APIs are unavailable: use `google_search` tool:
```
site:semanticscholar.org "your topic"
site:scholar.google.com "your topic"
```

---

## Step 3 — Format and Return Results (always do this)

Present results inline in chat using this format:

```
1. Author(s) (Year). Title. *Journal*, Volume(Issue), pages. https://doi.org/...
2. ...
```

If saving references was requested, write a BibTeX file to `/workspace/output/references/references.bib` and report the path.

---

## Step 4 — Collect & Deduplicate (only for full review or matrix)

Only run this step if the user asked for a literature matrix or systematic review.

- Deduplicate by DOI (primary) then by title similarity
- Collect: Title, Authors, Year, Journal/Venue, DOI, URL, Abstract, Citation count
- Store in `/workspace/output/references/literature_matrix.csv`

CSV columns:
```
ID, Authors, Year, Title, Journal, DOI, URL, Abstract, Keywords, CitationCount, Notes, Included
```

---

## Step 5 — Generate BibTeX (only if requested)

Only run this step if user asked to "save references", "export BibTeX", or similar.

```python
result = subprocess.run(
    ["python3", "/workspace/scripts/export_bibtex.py",
     "--input", "/workspace/output/references/literature_matrix.csv",
     "--output", "/workspace/output/references/references.bib"],
    capture_output=True, text=True
)
```

---

## Step 6 — Research Gap Analysis (only if requested)

Only run this step if user asked for a gap analysis.

```markdown
## Research Gap Analysis

### What Has Been Studied
[2-3 sentence summary]

### Identified Gaps
1. **[Gap label]**: [Description + supporting papers]
2. ...

### Implications
[How gaps justify the proposed research]
```

Save to `/workspace/output/references/gap_analysis.md`.

---

## Step 7 — Annotated Bibliography (only if requested)

Only run this step if user asked for an annotated bibliography.

For each paper:
```markdown
## Author(s) (Year)
**Title**: ...
**Source**: Journal, Volume, Pages
**DOI**: https://doi.org/...

**Summary**: [2-3 sentences]
**Methods**: [Methodology]
**Key Findings**: [Main results]
**Relevance**: [How it relates to the topic]
```

Save to `/workspace/output/references/annotated_bibliography.md`.

---

## Error Handling

- Semantic Scholar 429 (rate limit): wait 2 seconds, retry up to 3 times
- DOI resolution fails: use title-based search as fallback
- Fewer papers found than requested: report the count and suggest broader keywords
