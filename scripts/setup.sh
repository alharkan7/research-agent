#!/bin/bash
# setup.sh — Research Agent Environment Setup
# Run this once after the environment is provisioned.
# It installs a lean core stack by default.
# Heavy extras are opt-in via env flags.

set -e  # Exit on any error

# Optional installation toggles (default = lean setup)
INSTALL_HEAVY_TOOLS=${INSTALL_HEAVY_TOOLS:-0}   # TeX/Image stack
INSTALL_NODE_TOOLS=${INSTALL_NODE_TOOLS:-0}     # Mermaid/reveal-md
INSTALL_NLP_EXTRAS=${INSTALL_NLP_EXTRAS:-0}     # nltk + corpora

echo "============================================"
echo "  Research Agent Environment Setup"
echo "============================================"

# Load API keys from injected .env file
if [ -f /workspace/.env ]; then
    export $(grep -v '^#' /workspace/.env | xargs)
    echo "  🔑 Loaded API keys from /workspace/.env"
fi

# ---------------------------------------------------------
# 1. System packages (lean baseline)
# ---------------------------------------------------------
echo "[1/5] Installing system packages..."
apt-get update -qq && apt-get install -y -qq \
    pandoc \
    poppler-utils \
    fonts-liberation \
    fonts-dejavu \
    2>/dev/null

echo "  ✅ System packages installed"

if [ "$INSTALL_HEAVY_TOOLS" = "1" ]; then
    echo "  ➕ Installing heavy system extras (TeX/image stack)..."
    apt-get install -y -qq \
        texlive-xetex \
        texlive-fonts-recommended \
        texlive-latex-extra \
        librsvg2-bin \
        imagemagick \
        wkhtmltopdf \
        2>/dev/null
    echo "  ✅ Heavy system extras installed"
else
    echo "  ⏭️  Skipping heavy system extras (set INSTALL_HEAVY_TOOLS=1 to enable)"
fi

# ---------------------------------------------------------
# 2. Python packages (lean core)
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
    pypdf2 \
    pdfplumber \
    python-docx \
    python-pptx \
    openpyxl \
    tabulate \
    jinja2 \
    bibtexparser \
    markdown \
    mistune \
    tqdm \
    rich \
    loguru \
    xlsxwriter

echo "  ✅ Python packages installed"

# ---------------------------------------------------------
# 3. Optional NLP extras (NLTK)
# ---------------------------------------------------------
if [ "$INSTALL_NLP_EXTRAS" = "1" ]; then
    echo "[3/5] Installing NLP extras and downloading NLTK data..."
    pip install -q nltk rake-nltk wordcloud weasyprint
    python3 -c "
import nltk
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('wordnet', quiet=True)
print('  NLTK data ready')
"
else
    echo "[3/5] Skipping NLP extras (set INSTALL_NLP_EXTRAS=1 to enable)"
fi

# ---------------------------------------------------------
# 4. Optional Node.js packages
# ---------------------------------------------------------
if [ "$INSTALL_NODE_TOOLS" = "1" ]; then
    echo "[4/5] Installing Node.js packages..."
    npm install -g -q \
        @mermaid-js/mermaid-cli \
        reveal-md \
        2>/dev/null || echo "  ⚠️  Some npm packages may have failed (non-critical)"

    # Verify mmdc
    mmdc --version 2>/dev/null && echo "  ✅ Mermaid CLI ready" || echo "  ⚠️  mmdc not available"
else
    echo "[4/5] Skipping Node.js global tools (set INSTALL_NODE_TOOLS=1 to enable)"
fi

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
echo "  Lean mode enabled by default."
echo "  Optional extras:"
echo "    INSTALL_HEAVY_TOOLS=1 bash /workspace/scripts/setup.sh"
echo "    INSTALL_NODE_TOOLS=1  bash /workspace/scripts/setup.sh"
echo "    INSTALL_NLP_EXTRAS=1  bash /workspace/scripts/setup.sh"
echo "  Environment is ready for research tasks."
echo "============================================"
