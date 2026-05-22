---
name: export
description: >
  Export research documents to DOCX (Word), PPTX (PowerPoint), LaTeX (.tex),
  XLSX (Excel), and BibTeX (.bib). Uses Pandoc, python-docx, python-pptx,
  and openpyxl.
triggers:
  - export
  - convert to
  - download as
  - save as Word
  - save as DOCX
  - save as PowerPoint
  - save as PPTX
  - save as LaTeX
  - save as Excel
  - save as XLSX
  - export BibTeX
  - export references
  - generate .bib
---

# Export Skill

## Overview

Converts research documents and data into final publication-ready formats.
All exports go to `/workspace/output/exports/`.

Supported formats:

| Format | Tool | Best for |
|---|---|---|
| `.docx` (Word) | Pandoc | Final report submission |
| `.pptx` (PowerPoint) | python-pptx | Presentation export |
| `.tex` (LaTeX) | Pandoc | Journal submission |
| `.xlsx` (Excel) | openpyxl | Data tables, statistics |
| `.bib` (BibTeX) | python | Mendeley/Zotero import |

---

## Step-by-Step: DOCX Export

### Using Pandoc (Markdown → DOCX)

```bash
# Ensure Pandoc is available
pandoc --version || apt-get install -y pandoc

# Basic conversion
pandoc /workspace/output/reports/paper_draft.md \
    -o /workspace/output/exports/paper_final.docx \
    --reference-doc=/workspace/templates/apa_reference.docx \
    --citeproc \
    --bibliography=/workspace/output/references/references.bib \
    --csl=/workspace/citation-styles/apa7.csl \
    -f markdown -t docx

echo "DOCX exported: /workspace/output/exports/paper_final.docx"
```

**Key Pandoc flags:**
- `--reference-doc` → applies Word styles (APA formatting)
- `--citeproc` → processes `[@CitationKey]` citations automatically
- `--bibliography` → the `.bib` file for references
- `--csl` → citation style (APA, IEEE, Harvard, etc.)

### Inline citation syntax in Markdown for Pandoc
```markdown
# Use square bracket syntax in .md files:
[@Smith2023]                    → (Smith, 2023)
[@Smith2023; @Jones2022]        → (Smith, 2023; Jones, 2022)
@Smith2023 found that...        → Smith (2023) found that...
[@Smith2023, p. 45]             → (Smith, 2023, p. 45)
```

---

## Step-by-Step: PPTX Export

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
import os

output_path = "/workspace/output/exports/presentation.pptx"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

prs = Presentation()

# Set slide dimensions (widescreen 16:9)
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)

# --- Title Slide ---
slide_layout = prs.slide_layouts[0]  # Title slide
slide = prs.slides.add_slide(slide_layout)
title = slide.shapes.title
subtitle = slide.placeholders[1]
title.text = "[Paper Title]"
subtitle.text = "[Author Name]\n[Institution]\n[Year]"

# --- Content Slide ---
slide_layout = prs.slide_layouts[1]  # Title + content
slide = prs.slides.add_slide(slide_layout)
slide.shapes.title.text = "Slide Title"
body = slide.placeholders[1]
tf = body.text_frame
tf.text = "• Key point 1"
tf.add_paragraph().text = "• Key point 2"
tf.add_paragraph().text = "• Key point 3"

# --- Add image slide ---
def add_image_slide(prs, title_text, image_path, caption=""):
    slide = prs.slides.add_slide(prs.slide_layouts[5])  # blank
    # Title
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(12), Inches(0.8))
    txBox.text_frame.text = title_text
    txBox.text_frame.paragraphs[0].runs[0].font.size = Pt(24)
    txBox.text_frame.paragraphs[0].runs[0].font.bold = True
    # Image
    if os.path.exists(image_path):
        slide.shapes.add_picture(image_path, Inches(1.5), Inches(1.2), Inches(10), Inches(5))
    # Caption
    if caption:
        cap = slide.shapes.add_textbox(Inches(1.5), Inches(6.5), Inches(10), Inches(0.6))
        cap.text_frame.text = caption
        cap.text_frame.paragraphs[0].font.size = Pt(10)
    return slide

# Add a chart slide
add_image_slide(prs, "Figure 1. [Chart Title]", 
                "/workspace/output/charts/figure_1_barplot.png",
                "Note. [Caption text]")

prs.save(output_path)
print(f"PPTX saved: {output_path}")
```

---

## Step-by-Step: LaTeX Export

```bash
# Markdown → LaTeX (for journal submission)
pandoc /workspace/output/reports/paper_draft.md \
    -o /workspace/output/exports/paper.tex \
    --citeproc \
    --bibliography=/workspace/output/references/references.bib \
    --csl=/workspace/citation-styles/apa7.csl \
    -f markdown -t latex \
    --standalone \
    --template=default

echo "LaTeX exported: /workspace/output/exports/paper.tex"
```

For journal-specific templates (e.g., Elsevier, IEEE):
```bash
# If a journal .cls file is in /workspace/templates/latex/:
pandoc /workspace/output/reports/paper_draft.md \
    --template=/workspace/templates/latex/elsarticle.tex \
    -o /workspace/output/exports/paper_journal.tex \
    -f markdown -t latex
```

Also copy the `.bib` file alongside the `.tex`:
```bash
cp /workspace/output/references/references.bib /workspace/output/exports/
echo "BibTeX file copied alongside LaTeX."
```

---

## Step-by-Step: XLSX Export

### Statistics Tables to Excel
```python
import pandas as pd
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows
import os

output_path = "/workspace/output/exports/results_tables.xlsx"

with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    # Sheet 1: Descriptive Statistics
    desc_df.to_excel(writer, sheet_name="Descriptive Statistics", index=True)
    
    # Sheet 2: Correlation Matrix
    corr_df.to_excel(writer, sheet_name="Correlations", index=True)
    
    # Sheet 3: Inferential Results
    results_df.to_excel(writer, sheet_name="Statistical Tests", index=False)

# Apply APA-style formatting
wb = openpyxl.load_workbook(output_path)
for sheet_name in wb.sheetnames:
    ws = wb[sheet_name]
    # Header row: bold
    for cell in ws[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal='center')
    # Column widths
    for col in ws.columns:
        max_len = max(len(str(cell.value or "")) for cell in col)
        ws.column_dimensions[col[0].column_letter].width = min(max_len + 4, 30)
wb.save(output_path)
print(f"XLSX saved: {output_path}")
```

---

## Step-by-Step: BibTeX Export

```python
import subprocess
result = subprocess.run(
    ["python3", "/workspace/scripts/export_bibtex.py",
     "--input", "/workspace/output/references/literature_matrix.csv",
     "--output", "/workspace/output/exports/references.bib"],
    capture_output=True, text=True
)
print(result.stdout)
if result.returncode == 0:
    print("BibTeX exported: /workspace/output/exports/references.bib")
    print("This file can be imported directly into Mendeley or Zotero.")
```

**Mendeley import**: File → Import → BibTeX (.bib)
**Zotero import**: File → Import → BibTeX format

---

## Citation Style Selection

Pass `--csl` to Pandoc with one of these pre-installed styles:

| Style | File |
|---|---|
| APA 7th edition | `/workspace/citation-styles/apa7.csl` |
| IEEE | `/workspace/citation-styles/ieee.csl` |
| Harvard | `/workspace/citation-styles/harvard.csl` |
| Vancouver | `/workspace/citation-styles/vancouver.csl` |
| Chicago (Author-Date) | `/workspace/citation-styles/chicago-author-date.csl` |
| MLA 9 | `/workspace/citation-styles/mla9.csl` |

---

## Export Summary

After all exports, print a summary:
```
✅ Exports completed:
   📄 DOCX:   /workspace/output/exports/paper_final.docx
   📊 PPTX:   /workspace/output/exports/presentation.pptx
   📐 LaTeX:  /workspace/output/exports/paper.tex
   📈 XLSX:   /workspace/output/exports/results_tables.xlsx
   📚 BibTeX: /workspace/output/exports/references.bib
```
