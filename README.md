# Research Agent Environment

This directory contains all configuration files for the **Research Agent** — a custom managed agent on the Gemini API designed to support the full academic research lifecycle.

## Directory Structure

```
research-agent/
├── AGENTS.md                         # Agent persona and workflow rules
├── skills/
│   ├── literature-review/SKILL.md    # Multi-source paper search + BibTeX export
│   ├── statistical-analysis/SKILL.md # Descriptive stats, t-test, ANOVA, regression
│   ├── data-viz/SKILL.md             # Charts (matplotlib/seaborn) + Mermaid diagrams
│   ├── report-writer/SKILL.md        # APA 7 academic writing + document editing
│   ├── export/SKILL.md               # DOCX, PPTX, LaTeX, XLSX, BibTeX export
│   └── presentation/SKILL.md         # Slide deck creation (python-pptx)
├── templates/
│   ├── report_template.md            # Full IMRaD paper template (APA 7)
│   ├── chapter4_stats_template.md    # Chapter 4 Results template
│   ├── literature_matrix.csv         # Literature review tracking matrix
│   └── research_proposal.md          # Research proposal template
└── scripts/
    ├── setup.sh                      # One-time environment setup
    ├── search_papers.py              # Multi-source paper search CLI
    └── export_bibtex.py              # CSV → BibTeX converter
```

## Setup

### 1. Push to your private GitHub repository

```bash
cd research-agent
git init
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git add .
git commit -m "Initial research agent environment"
git push -u origin main
```

Then set the env var in your `.env`:
```
RESEARCH_AGENT_REPO=https://github.com/YOUR_USERNAME/YOUR_REPO.git
```

### 2. Add API keys to `.env`

```env
# Required
GEMINI_API_KEY=your_key_here

# Literature search (recommended)
SEMANTIC_SCHOLAR_API_KEY=your_key_here
OPENALEX_EMAIL=your@email.com
CROSSREF_MAILTO=your@email.com
NCBI_API_KEY=your_key_here

# Optional: Data sources
FRED_API_KEY=your_key_here
ZENODO_ACCESS_TOKEN=your_token_here

# Optional: GitHub repo source
RESEARCH_AGENT_REPO=https://github.com/you/research-agent-env.git
```

### 3. Run the Research Agent

```bash
npx ts-node src/research-agent.ts
```

On first run, answer **y** to the setup prompt to install all packages.

## Usage Examples

```
🔬 Research > Help me brainstorm research topics on AI in education

🔬 Research > Find 20 papers on "machine learning healthcare" from the last 3 years

🔬 Research > Analyze my data file at /workspace/data/survey.csv

🔬 Research > Run a Pearson correlation between age and score variables

🔬 Research > Create a bar chart comparing group means

🔬 Research > Write a results section based on the statistics

🔬 Research > Export the report as DOCX and create a PowerPoint presentation

🔬 Research > Export all references as BibTeX
```

## Commands

| Command | Action |
|---|---|
| `/new` | Fresh environment (packages reinstall required) |
| `/clear` | Clear conversation, keep environment |
| `/download` | Download all output files from sandbox |
| `/status` | Show environment and interaction IDs |
| `/help` | Show help |
| `/quit` | Exit |

## Output Files

All outputs are saved to `/workspace/output/` in the sandbox. Use `/download` to retrieve them.

| Folder | Contents |
|---|---|
| `output/reports/` | Draft documents, chapter files |
| `output/charts/` | PNG figures, Mermaid diagrams |
| `output/slides/` | PPTX presentation files |
| `output/exports/` | DOCX, PPTX, LaTeX, XLSX exports |
| `output/references/` | literature_matrix.csv, references.bib |

## Citation Styles Available

After setup, these CSL styles are available in `/workspace/citation-styles/`:
- APA 7th edition (default)
- IEEE
- Harvard
- Vancouver
- Chicago (Author-Date)
- MLA 9
