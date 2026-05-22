#!/bin/bash
# setup.sh — Research Agent Environment Setup
# Run this once after the environment is provisioned.
# It installs all required system tools and Python/Node packages.

set -e  # Exit on any error

echo "============================================"
echo "  Research Agent Environment Setup"
echo "============================================"

# Load API keys from injected .env file
if [ -f /workspace/.env ]; then
    export $(grep -v '^#' /workspace/.env | xargs)
    echo "  🔑 Loaded API keys from /workspace/.env"
fi

# ---------------------------------------------------------
# 1. System packages
# ---------------------------------------------------------
echo "[1/5] Installing system packages..."
apt-get update -qq && apt-get install -y -qq \
    pandoc \
    texlive-xetex \
    texlive-fonts-recommended \
    texlive-latex-extra \
    librsvg2-bin \
    imagemagick \
    poppler-utils \
    wkhtmltopdf \
    fonts-liberation \
    fonts-dejavu \
    2>/dev/null

echo "  ✅ System packages installed"

# ---------------------------------------------------------
# 2. Python packages
# ---------------------------------------------------------
echo "[2/5] Installing Python packages..."
pip install -q --upgrade pip

pip install -q \
    scipy \
    statsmodels \
    scikit-learn \
    pingouin \
    factor_analyzer \
    scholarly \
    arxiv \
    habanero \
    pyalex \
    semanticscholar \
    feedparser \
    httpx \
    matplotlib \
    seaborn \
    plotly \
    kaleido \
    altair \
    wordcloud \
    pypdf2 \
    pdfplumber \
    python-docx \
    python-pptx \
    openpyxl \
    tabulate \
    jinja2 \
    nltk \
    rake-nltk \
    bibtexparser \
    markdown \
    mistune \
    weasyprint \
    tqdm \
    rich \
    loguru \
    xlsxwriter

echo "  ✅ Python packages installed"

# ---------------------------------------------------------
# 3. NLTK data
# ---------------------------------------------------------
echo "[3/5] Downloading NLTK data..."
python3 -c "
import nltk
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('wordnet', quiet=True)
print('  NLTK data ready')
"

# ---------------------------------------------------------
# 4. Node.js packages (global)
# ---------------------------------------------------------
echo "[4/5] Installing Node.js packages..."
npm install -g -q \
    @mermaid-js/mermaid-cli \
    reveal-md \
    2>/dev/null || echo "  ⚠️  Some npm packages may have failed (non-critical)"

# Verify mmdc
mmdc --version 2>/dev/null && echo "  ✅ Mermaid CLI ready" || echo "  ⚠️  mmdc not available"

# ---------------------------------------------------------
# 5. Create workspace directories
# ---------------------------------------------------------
echo "[5/5] Creating workspace directories..."
mkdir -p \
    /workspace/data \
    /workspace/output/reports \
    /workspace/output/charts \
    /workspace/output/slides \
    /workspace/output/exports \
    /workspace/output/references \
    /workspace/templates \
    /workspace/scripts \
    /workspace/citation-styles

echo "  ✅ Workspace directories created"

# ---------------------------------------------------------
# 6. Verify critical imports
# ---------------------------------------------------------
echo ""
echo "Verifying Python imports..."
python3 -c "
import scipy, statsmodels, pingouin, bibtexparser
import matplotlib, seaborn, openpyxl
from docx import Document
from pptx import Presentation
print('  ✅ All critical Python packages verified')
"

# ---------------------------------------------------------
# 7. Download CSL citation styles
# ---------------------------------------------------------
echo "Downloading citation style files..."
CSL_BASE="https://raw.githubusercontent.com/citation-style-language/styles/master"
CSL_DIR="/workspace/citation-styles"

curl -s -o "$CSL_DIR/apa7.csl" "$CSL_BASE/apa.csl" && echo "  ✅ APA 7" || echo "  ⚠️  APA download failed"
curl -s -o "$CSL_DIR/ieee.csl" "$CSL_BASE/ieee.csl" && echo "  ✅ IEEE" || echo "  ⚠️  IEEE download failed"
curl -s -o "$CSL_DIR/harvard.csl" "$CSL_BASE/harvard-cite-them-right.csl" && echo "  ✅ Harvard" || echo "  ⚠️  Harvard download failed"
curl -s -o "$CSL_DIR/vancouver.csl" "$CSL_BASE/vancouver.csl" && echo "  ✅ Vancouver" || echo "  ⚠️  Vancouver download failed"
curl -s -o "$CSL_DIR/chicago-author-date.csl" "$CSL_BASE/chicago-author-date.csl" && echo "  ✅ Chicago" || echo "  ⚠️  Chicago download failed"
curl -s -o "$CSL_DIR/mla9.csl" "$CSL_BASE/modern-language-association.csl" && echo "  ✅ MLA" || echo "  ⚠️  MLA download failed"

echo ""
echo "============================================"
echo "  ✅ Setup complete!"
echo "  Environment is ready for research tasks."
echo "============================================"
