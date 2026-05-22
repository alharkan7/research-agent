---
name: literature-review
description: >
  Search academic databases, collect papers, build reference lists, analyze
  literature, identify research gaps, and generate annotated bibliographies
  and BibTeX files.
triggers:
  - find papers
  - literature review
  - search for research
  - related work
  - research gap
  - annotated bibliography
  - references on
  - cite papers about
---

# Literature Review Skill

## Overview

This skill orchestrates multi-source academic literature search and analysis. It produces:
- Structured paper metadata lists
- Annotated bibliography (Markdown + DOCX)
- BibTeX `.bib` file (Mendeley/Zotero compatible)
- Literature review matrix (`/workspace/output/references/literature_matrix.csv`)
- Research gap analysis section

---

## Step-by-Step Instructions

### Step 1 — Understand the Search Request

Before searching, clarify:
1. **Topic / keywords** (extract if not stated)
2. **Date range** (default: last 5 years unless user specifies)
3. **Number of papers** (default: 20, max: 50 per run)
4. **Field/domain** (helps choose which APIs to prioritize)
5. **Language** (default: English only)

### Step 2 — Search Sources (use Python scripts)

Run searches in this priority order:

```python
# /workspace/scripts/search_papers.py handles multi-source search
# Usage:
import subprocess
result = subprocess.run(
    ["python3", "/workspace/scripts/search_papers.py",
     "--query", "<TOPIC>",
     "--limit", "20",
     "--years", "5"],
    capture_output=True, text=True
)
print(result.stdout)
```

**Source priority order:**
1. **Semantic Scholar** (best coverage, free API) — use `SEMANTIC_SCHOLAR_API_KEY` env var
2. **OpenAlex** (open scholarly graph) — use `OPENALEX_EMAIL` env var
3. **CrossRef** (DOI metadata) — use `CROSSREF_MAILTO` env var
4. **arXiv** (preprints, CS/Physics/Math/Econ)
5. **PubMed** (medical/biological, via `NCBI_API_KEY`)

**Fallback** if APIs unavailable: use `google_search` tool with site-specific queries:
```
site:scholar.google.com "your topic" filetype:pdf
site:semanticscholar.org "your topic"
```

### Step 3 — Collect & Deduplicate

- Deduplicate by DOI (primary) then by title similarity
- For each paper, collect: Title, Authors, Year, Journal/Venue, DOI, URL, Abstract, Citations count
- Store in `/workspace/output/references/literature_matrix.csv`

CSV columns:
```
ID, Authors, Year, Title, Journal, DOI, URL, Abstract, Keywords, CitationCount, Notes, Included
```

### Step 4 — Screen & Filter

- Remove papers where abstract does not mention key concepts
- Mark `Included` column as `YES` / `NO` / `MAYBE`
- Always retain at least the user's requested number as `YES`

### Step 5 — Generate BibTeX

```python
# Run the BibTeX export script
result = subprocess.run(
    ["python3", "/workspace/scripts/export_bibtex.py",
     "--input", "/workspace/output/references/literature_matrix.csv",
     "--output", "/workspace/output/references/references.bib"],
    capture_output=True, text=True
)
```

BibTeX entry format (APA-compatible):
```bibtex
@article{AuthorYear,
  author    = {Last, First and Last2, First2},
  title     = {Full Paper Title},
  journal   = {Journal Name},
  year      = {2023},
  volume    = {12},
  number    = {3},
  pages     = {100--115},
  doi       = {10.1234/example},
  url       = {https://doi.org/10.1234/example},
}
```

### Step 6 — Research Gap Analysis

After collecting papers, synthesize gaps using this structure:

```markdown
## Research Gap Analysis

### What Has Been Studied
[2-3 sentence summary of existing work]

### Identified Gaps
1. **[Gap 1 label]**: [Description + which papers support this gap]
2. **[Gap 2 label]**: [Description]
3. **[Gap 3 label]**: [Description]

### Implications for Current Research
[How the gaps justify the proposed research]
```

### Step 7 — Annotated Bibliography (optional, if requested)

For each included paper, generate:
```markdown
## [Author(s), Year]
**Title**: [Full title]
**Source**: [Journal/Conference, Volume, Pages]
**DOI**: [DOI link]

**Summary**: [2-3 sentence summary of contribution]
**Methods**: [Brief description of methodology used]
**Key Findings**: [Main results]
**Relevance**: [How it relates to the current research topic]
```

---

## Output Files

| File | Location | Format |
|---|---|---|
| Literature matrix | `/workspace/output/references/literature_matrix.csv` | CSV |
| BibTeX references | `/workspace/output/references/references.bib` | `.bib` |
| Gap analysis | `/workspace/output/references/gap_analysis.md` | Markdown |
| Annotated bibliography | `/workspace/output/references/annotated_bibliography.md` | Markdown |

---

## Error Handling

- If Semantic Scholar API returns 429 (rate limit): wait 2 seconds and retry, max 3 retries
- If DOI resolution fails: use title-based search as fallback
- If fewer papers found than requested: report how many were found and suggest broadening keywords
