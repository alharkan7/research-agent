---
name: presentation
description: >
  Create academic and professional slide presentations from research content.
  Outputs PPTX (PowerPoint) files with figures, charts, and structured slides.
  Uses python-pptx and optionally reveal-md for HTML slides.
triggers:
  - create slides
  - make presentation
  - slide deck
  - PowerPoint
  - present findings
  - create a presentation from
  - slides for my research
  - conference presentation
  - thesis defense slides
---

# Presentation Skill

## Overview

Creates structured slide decks from research content. Reads from:
- Report draft: `/workspace/output/reports/`
- Charts: `/workspace/output/charts/`
- Statistics: `/workspace/output/exports/statistical_results.xlsx`

Output: PPTX (primary) or HTML/Reveal.js (optional)

---

## What to do based on what the user asked

| User request | What to do |
|---|---|
| "Create slides for my research" | Ask: how many slides? what type? Then build. |
| "Make a [N]-slide summary" | Build exactly N slides on the key points. |
| "Conference presentation" | Use the 12–15 slide structure below. |
| "Thesis defense slides" | Use the 25–35 slide structure. |
| "Turn this into slides" | Extract key points from provided content, build slides. |
| "Add a slide about X" | Add just that slide to an existing deck. |

**Default: ask clarifying questions if the scope is ambiguous. Don't build a full deck if the user only asked for a few slides.**

---

## Presentation Types

| Type | Slides | Style |
|---|---|---|
| Conference paper | 12–15 | Dense, academic |
| Thesis defense | 25–35 | Comprehensive |
| Research summary | 8–10 | Executive-friendly |
| Progress report | 10–15 | Updates focused |

---

## Step-by-Step: Build Presentation

### Step 1 — Plan the Slide Structure

For a **conference paper** (15 slides):
```
1.  Title slide
2.  Outline / Agenda
3.  Introduction & Background
4.  Problem Statement & Research Questions
5.  Literature Review (key themes, gap)
6.  Conceptual Framework (diagram)
7.  Methodology
8.  Results 1 — Descriptive Statistics
9.  Results 2 — [Test 1] (chart)
10. Results 3 — [Test 2] (chart)
11. Discussion — Key Findings
12. Discussion — Comparison with Literature
13. Conclusion & Contributions
14. Limitations & Future Research
15. Thank You / Q&A
```

For a **thesis defense** (30 slides), expand each section with more depth.

### Step 2 — Extract Content from Report

```python
# Read the draft report
with open("/workspace/output/reports/paper_draft.md") as f:
    report = f.read()

# List available charts
import os
charts = os.listdir("/workspace/output/charts/")
print("Available charts:", charts)
```

### Step 3 — Build the PPTX

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import os

prs = Presentation()
prs.slide_width = Inches(13.33)   # 16:9 widescreen
prs.slide_height = Inches(7.5)

# === COLOR SCHEME (academic professional) ===
COLORS = {
    "primary": RGBColor(0x1A, 0x3A, 0x6B),    # Deep navy
    "accent": RGBColor(0x2E, 0x86, 0xAB),       # Steel blue
    "light": RGBColor(0xF0, 0xF4, 0xF8),        # Light gray
    "text": RGBColor(0x2C, 0x2C, 0x2C),         # Near black
    "white": RGBColor(0xFF, 0xFF, 0xFF),
    "highlight": RGBColor(0xF7, 0x7F, 0x00),    # Orange accent
}

# === HELPER FUNCTIONS ===
def add_slide(prs, layout_idx=5):
    """Add a blank slide."""
    return prs.slides.add_slide(prs.slide_layouts[layout_idx])

def add_header_bar(slide, prs, color=None):
    """Add a colored header bar."""
    color = color or COLORS["primary"]
    bar = slide.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.RECTANGLE
        Inches(0), Inches(0), prs.slide_width, Inches(1.2)
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = color
    bar.line.fill.background()
    return bar

def add_title_text(slide, text, left=Inches(0.5), top=Inches(0.1), 
                   width=Inches(12), height=Inches(1.0),
                   size=Pt(28), bold=True, color=None):
    """Add title text box."""
    color = color or COLORS["white"]
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.runs[0].font.size = size
    p.runs[0].font.bold = bold
    p.runs[0].font.color.rgb = color
    return txBox

def add_body_text(slide, lines, left=Inches(0.5), top=Inches(1.4),
                  width=Inches(12.3), height=Inches(5.5), size=Pt(18)):
    """Add bulleted body text."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = line
        p.runs[0].font.size = size
        p.runs[0].font.color.rgb = COLORS["text"]
        p.space_before = Pt(6)
    return txBox

def add_image(slide, image_path, left, top, width, height):
    """Add image if it exists."""
    if os.path.exists(image_path):
        return slide.shapes.add_picture(image_path, left, top, width, height)
    else:
        # Placeholder box
        box = slide.shapes.add_textbox(left, top, width, height)
        box.text_frame.text = f"[Image: {os.path.basename(image_path)}]"
        return box

# ============================================================
# SLIDE 1: TITLE SLIDE
# ============================================================
slide = add_slide(prs)
# Background
bg = slide.shapes.add_shape(1, Inches(0), Inches(0), prs.slide_width, prs.slide_height)
bg.fill.solid()
bg.fill.fore_color.rgb = COLORS["primary"]
bg.line.fill.background()

# Title
add_title_text(slide, "[Paper Title Goes Here]",
               top=Inches(2.0), height=Inches(1.8), size=Pt(36))

# Subtitle
add_title_text(slide, "[Author Name] | [Institution] | [Conference/Year]",
               top=Inches(4.2), size=Pt(20), bold=False,
               color=RGBColor(0xBB, 0xCC, 0xDD))

# ============================================================
# SLIDE 2: OUTLINE
# ============================================================
slide = add_slide(prs)
add_header_bar(slide, prs)
add_title_text(slide, "Outline")
add_body_text(slide, [
    "01 · Introduction & Background",
    "02 · Research Problem & Questions",
    "03 · Literature Review",
    "04 · Methodology",
    "05 · Results & Findings",
    "06 · Discussion",
    "07 · Conclusion",
])

# ============================================================
# SLIDE 3: INTRODUCTION
# ============================================================
slide = add_slide(prs)
add_header_bar(slide, prs)
add_title_text(slide, "Introduction")
add_body_text(slide, [
    "▸ [Background context — 1 sentence]",
    "▸ [The problem being addressed]",
    "▸ [Why it matters / significance]",
    "▸ [What this study does]",
])

# ============================================================
# SLIDE 4: RESEARCH QUESTIONS
# ============================================================
slide = add_slide(prs)
add_header_bar(slide, prs)
add_title_text(slide, "Research Questions")
add_body_text(slide, [
    "RQ1: [First research question?]",
    "",
    "RQ2: [Second research question?]",
    "",
    "RQ3: [Third research question?]",
], size=Pt(20))

# ============================================================
# SLIDE: CONCEPTUAL FRAMEWORK (diagram)
# ============================================================
slide = add_slide(prs)
add_header_bar(slide, prs)
add_title_text(slide, "Conceptual Framework")
add_image(slide, "/workspace/output/charts/diagram_conceptual_framework.png",
          Inches(1.5), Inches(1.3), Inches(10), Inches(5.5))

# ============================================================
# SLIDE: RESULTS — with chart
# ============================================================
def add_results_slide(prs, title, chart_path, finding_text, figure_caption):
    slide = add_slide(prs)
    add_header_bar(slide, prs)
    add_title_text(slide, title)
    
    # Chart (left side)
    add_image(slide, chart_path,
              Inches(0.3), Inches(1.3), Inches(8.0), Inches(5.2))
    
    # Key finding callout (right side)
    txBox = slide.shapes.add_textbox(Inches(8.5), Inches(1.5), Inches(4.5), Inches(3.5))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Key Finding"
    p.runs[0].font.size = Pt(14)
    p.runs[0].font.bold = True
    p.runs[0].font.color.rgb = COLORS["accent"]
    
    p2 = tf.add_paragraph()
    p2.text = finding_text
    p2.runs[0].font.size = Pt(16)
    p2.runs[0].font.color.rgb = COLORS["text"]
    p2.space_before = Pt(8)
    
    # Figure caption
    cap = slide.shapes.add_textbox(Inches(0.3), Inches(6.7), Inches(7.8), Inches(0.6))
    cap.text_frame.text = figure_caption
    cap.text_frame.paragraphs[0].font.size = Pt(9)
    cap.text_frame.paragraphs[0].font.color.rgb = RGBColor(0x66, 0x66, 0x66)
    
    return slide

# Add results slides for each chart
add_results_slide(prs,
    "Results: [First Analysis]",
    "/workspace/output/charts/figure_1_barplot.png",
    "[Key statistical finding stated plainly, e.g., Group A scored significantly higher (p < .05)]",
    "Figure 1. [Chart caption]"
)

# ============================================================
# SLIDE: CONCLUSION
# ============================================================
slide = add_slide(prs)
add_header_bar(slide, prs)
add_title_text(slide, "Conclusion")
add_body_text(slide, [
    "✓ [Finding 1 — one sentence]",
    "✓ [Finding 2 — one sentence]",
    "✓ [Finding 3 — one sentence]",
    "",
    "Contributions:",
    "  • [Theoretical contribution]",
    "  • [Practical contribution]",
])

# ============================================================
# SLIDE: THANK YOU
# ============================================================
slide = add_slide(prs)
bg = slide.shapes.add_shape(1, Inches(0), Inches(0), prs.slide_width, prs.slide_height)
bg.fill.solid()
bg.fill.fore_color.rgb = COLORS["primary"]
bg.line.fill.background()
add_title_text(slide, "Thank You", top=Inches(2.5), size=Pt(40))
add_title_text(slide, "Questions & Discussion", top=Inches(3.8), size=Pt(24),
               bold=False, color=RGBColor(0xBB, 0xCC, 0xDD))
add_title_text(slide, "[author.email@university.edu]", top=Inches(5.0),
               size=Pt(16), bold=False, color=RGBColor(0x99, 0xAA, 0xBB))

# ============================================================
# SAVE
# ============================================================
os.makedirs("/workspace/output/slides", exist_ok=True)
output_path = "/workspace/output/slides/presentation.pptx"
prs.save(output_path)
print(f"Presentation saved: {output_path}")
print(f"Total slides: {len(prs.slides)}")
```

---

## Output Files

| File | Location |
|---|---|
| PowerPoint | `/workspace/output/slides/presentation.pptx` |
| Speaker notes (optional) | `/workspace/output/slides/speaker_notes.md` |

After creating, report: total slide count, slides that need user content filled in, and which chart files were embedded vs. missing.
