#!/usr/bin/env python3
"""
export_bibtex.py — Convert literature matrix CSV to BibTeX .bib file
Compatible with Mendeley, Zotero, LaTeX, and Pandoc.

Usage:
    python3 export_bibtex.py \
        --input /workspace/output/references/literature_matrix.csv \
        --output /workspace/output/references/references.bib \
        --filter YES
"""

import argparse
import csv
import os
import re
import sys
from unicodedata import normalize


# ─────────────────────────────────────────────
# Citation key generation
# ─────────────────────────────────────────────
def make_citation_key(authors: str, year: str, title: str) -> str:
    """Generate AuthorYear or AuthorYearKeyword style citation key."""
    # Get first author last name
    if authors:
        first_author = authors.split(";")[0].strip()
        # Handle "Last, First" format
        if "," in first_author:
            last_name = first_author.split(",")[0].strip()
        else:
            # Handle "First Last" format
            parts = first_author.split()
            last_name = parts[-1] if parts else "Unknown"
    else:
        last_name = "Unknown"

    # Clean the name
    last_name = normalize("NFKD", last_name).encode("ascii", "ignore").decode("ascii")
    last_name = re.sub(r"[^a-zA-Z]", "", last_name)
    last_name = last_name[:15]

    # Year
    year_clean = re.sub(r"[^0-9]", "", str(year))[:4]

    # Short title keyword (first significant word)
    stop_words = {"a", "an", "the", "of", "in", "on", "to", "for", "and", "or", "with", "is", "are"}
    title_words = [w for w in re.sub(r"[^a-zA-Z ]", "", title).lower().split() if w not in stop_words]
    keyword = title_words[0].capitalize() if title_words else ""

    return f"{last_name}{year_clean}{keyword}"


# ─────────────────────────────────────────────
# Entry type detection
# ─────────────────────────────────────────────
def detect_entry_type(journal: str, title: str) -> str:
    journal_lower = (journal or "").lower()
    title_lower = (title or "").lower()

    if "arxiv" in journal_lower or "preprint" in journal_lower:
        return "misc"  # preprint
    if "proceedings" in journal_lower or "conference" in journal_lower or "workshop" in journal_lower:
        return "inproceedings"
    if "thesis" in title_lower or "dissertation" in title_lower:
        return "phdthesis"
    if "report" in journal_lower or "technical" in journal_lower:
        return "techreport"
    if journal:
        return "article"
    return "misc"


# ─────────────────────────────────────────────
# Escape special LaTeX characters
# ─────────────────────────────────────────────
def latex_escape(text: str) -> str:
    if not text:
        return ""
    # Order matters — ampersand must be first
    replacements = [
        ("&", r"\&"),
        ("%", r"\%"),
        ("$", r"\$"),
        ("#", r"\#"),
        ("_", r"\_"),
        ("{", r"\{"),
        ("}", r"\}"),
        ("~", r"\textasciitilde{}"),
        ("^", r"\textasciicircum{}"),
        ("\\", r"\textbackslash{}"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text


# ─────────────────────────────────────────────
# Format authors for BibTeX
# ─────────────────────────────────────────────
def format_authors_bibtex(authors_str: str) -> str:
    """Convert 'Author A; Author B; Author C' to BibTeX 'Author A and Author B and Author C'."""
    if not authors_str:
        return ""
    authors = [a.strip() for a in authors_str.split(";") if a.strip()]
    return " and ".join(authors)


# ─────────────────────────────────────────────
# Generate single BibTeX entry
# ─────────────────────────────────────────────
def make_bibtex_entry(row: dict, cite_key: str) -> str:
    entry_type = detect_entry_type(row.get("Journal", ""), row.get("Title", ""))

    fields = []

    # Required fields
    if row.get("Authors"):
        fields.append(f"  author    = {{{format_authors_bibtex(row['Authors'])}}}")
    if row.get("Title"):
        fields.append(f"  title     = {{{latex_escape(row['Title'])}}}")
    if row.get("Year"):
        fields.append(f"  year      = {{{row['Year']}}}")

    # Journal/conference
    if entry_type == "article" and row.get("Journal"):
        fields.append(f"  journal   = {{{latex_escape(row['Journal'])}}}")
    elif entry_type == "inproceedings" and row.get("Journal"):
        fields.append(f"  booktitle = {{{latex_escape(row['Journal'])}}}")

    # Optional fields
    if row.get("Volume"):
        fields.append(f"  volume    = {{{row['Volume']}}}")
    if row.get("Issue"):
        fields.append(f"  number    = {{{row['Issue']}}}")
    if row.get("Pages"):
        fields.append(f"  pages     = {{{row['Pages'].replace('-', '--')}}}")
    if row.get("DOI"):
        fields.append(f"  doi       = {{{row['DOI']}}}")
    if row.get("URL"):
        fields.append(f"  url       = {{{row['URL']}}}")
    if row.get("Abstract"):
        abstract_clean = row["Abstract"].replace("\n", " ").replace("{", "(").replace("}", ")")
        fields.append(f"  abstract  = {{{abstract_clean[:400]}}}")
    if row.get("Keywords"):
        fields.append(f"  keywords  = {{{row['Keywords']}}}")

    fields_str = ",\n".join(fields)
    return f"@{entry_type}{{{cite_key},\n{fields_str}\n}}\n"


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Convert literature matrix CSV to BibTeX")
    parser.add_argument("--input", default="/workspace/output/references/literature_matrix.csv",
                        help="Input CSV file path")
    parser.add_argument("--output", default="/workspace/output/exports/references.bib",
                        help="Output .bib file path")
    parser.add_argument("--filter", default="YES",
                        help="Only include rows where Included == this value (default: YES, use ALL for everything)")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"❌ Input file not found: {args.input}")
        sys.exit(1)

    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    # Read CSV
    with open(args.input, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Filter
    if args.filter.upper() != "ALL":
        rows = [r for r in rows if r.get("Included", "").strip().upper() == args.filter.upper()]

    print(f"📥 Processing {len(rows)} papers from: {args.input}")

    # Generate entries with unique cite keys
    seen_keys = {}
    bib_entries = []
    header = (
        "% BibTeX references file\n"
        "% Generated by Research Agent\n"
        f"% Date: {__import__('datetime').datetime.now().strftime('%Y-%m-%d')}\n"
        "% Compatible with Mendeley, Zotero, LaTeX, and Pandoc\n\n"
    )

    for row in rows:
        base_key = make_citation_key(
            row.get("Authors", ""),
            row.get("Year", ""),
            row.get("Title", "")
        )
        # Handle duplicates
        if base_key in seen_keys:
            seen_keys[base_key] += 1
            cite_key = f"{base_key}{chr(96 + seen_keys[base_key])}"  # a, b, c...
        else:
            seen_keys[base_key] = 0
            cite_key = base_key

        entry = make_bibtex_entry(row, cite_key)
        bib_entries.append(entry)

    # Write .bib file
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(header)
        f.write("\n".join(bib_entries))

    print(f"✅ BibTeX file saved: {args.output}")
    print(f"   {len(bib_entries)} entries written")
    print(f"\n📌 Import instructions:")
    print(f"   Mendeley: File → Import → BibTeX (.bib)")
    print(f"   Zotero:   File → Import → BibTeX format")
    print(f"   LaTeX:    \\bibliography{{references}}")
    print(f"   Pandoc:   --bibliography={args.output}")


if __name__ == "__main__":
    main()
