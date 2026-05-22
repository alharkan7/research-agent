#!/usr/bin/env python3
"""
search_papers.py — Multi-source academic paper search
Searches Semantic Scholar, OpenAlex, CrossRef, and arXiv.
Outputs results as a literature matrix CSV.

Usage:
    python3 search_papers.py --query "machine learning" --limit 20 --years 5
    python3 search_papers.py --query "climate change" --limit 30 --output /workspace/output/references/literature_matrix.csv
"""

import argparse
import csv
import json
import os
import sys
import time
from datetime import datetime, timedelta
from typing import Optional

import requests

# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────
SS_API_KEY = os.environ.get("SEMANTIC_SCHOLAR_API_KEY", "")
OPENALEX_EMAIL = os.environ.get("OPENALEX_EMAIL", "research@example.com")
CROSSREF_MAILTO = os.environ.get("CROSSREF_MAILTO", "research@example.com")
NCBI_API_KEY = os.environ.get("NCBI_API_KEY", "")

OUTPUT_DIR = "/workspace/output/references"
DEFAULT_OUTPUT = os.path.join(OUTPUT_DIR, "literature_matrix.csv")

CSV_FIELDS = [
    "ID", "Authors", "Year", "Title", "Journal", "Volume", "Issue",
    "Pages", "DOI", "URL", "Abstract", "Keywords", "CitationCount",
    "Notes", "Included", "Relevance_Score", "Source"
]


# ─────────────────────────────────────────────
# Source: Semantic Scholar
# ─────────────────────────────────────────────
def search_semantic_scholar(query: str, limit: int = 20, year_from: Optional[int] = None) -> list:
    print(f"  → Searching Semantic Scholar for: '{query}'")
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    headers = {}
    if SS_API_KEY:
        headers["x-api-key"] = SS_API_KEY

    year_filter = f"{year_from}-" if year_from else ""
    params = {
        "query": query,
        "limit": min(limit, 100),
        "fields": "title,authors,year,journal,externalIds,abstract,citationCount,publicationTypes,venue",
        "year": year_filter if year_filter else None,
    }
    params = {k: v for k, v in params.items() if v is not None}

    results = []
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        papers = data.get("data", [])
        for paper in papers:
            authors = "; ".join(a.get("name", "") for a in paper.get("authors", []))
            doi = paper.get("externalIds", {}).get("DOI", "")
            results.append({
                "Title": paper.get("title", ""),
                "Authors": authors,
                "Year": paper.get("year", ""),
                "Journal": paper.get("venue", "") or paper.get("journal", {}).get("name", "") if paper.get("journal") else paper.get("venue", ""),
                "DOI": doi,
                "URL": f"https://doi.org/{doi}" if doi else "",
                "Abstract": (paper.get("abstract", "") or "")[:500],
                "CitationCount": paper.get("citationCount", 0),
                "Source": "Semantic Scholar",
            })
        print(f"    Found {len(results)} papers from Semantic Scholar")
    except Exception as e:
        print(f"    ⚠️  Semantic Scholar error: {e}")
    return results


# ─────────────────────────────────────────────
# Source: OpenAlex
# ─────────────────────────────────────────────
def search_openalex(query: str, limit: int = 20, year_from: Optional[int] = None) -> list:
    print(f"  → Searching OpenAlex for: '{query}'")
    url = "https://api.openalex.org/works"
    filter_str = f"title_and_abstract.search:{query}"
    if year_from:
        filter_str += f",publication_year:>{year_from - 1}"

    params = {
        "filter": filter_str,
        "per-page": min(limit, 200),
        "sort": "cited_by_count:desc",
        "mailto": OPENALEX_EMAIL,
    }
    results = []
    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        works = data.get("results", [])
        for work in works:
            authors = "; ".join(
                a.get("author", {}).get("display_name", "") for a in work.get("authorships", [])[:6]
            )
            doi = work.get("doi", "")
            if doi and doi.startswith("https://doi.org/"):
                doi_clean = doi.replace("https://doi.org/", "")
            else:
                doi_clean = doi or ""

            primary_loc = work.get("primary_location") or {}
            source = primary_loc.get("source") or {}
            journal = source.get("display_name", "")

            abstract = ""
            abst_inv = work.get("abstract_inverted_index")
            if abst_inv:
                # Reconstruct abstract from inverted index
                try:
                    positions = {word: pos for word, positions in abst_inv.items() for pos in positions}
                    abstract = " ".join(w for w, _ in sorted(positions.items(), key=lambda x: x[1]))
                    abstract = abstract[:500]
                except Exception:
                    pass

            results.append({
                "Title": work.get("title", ""),
                "Authors": authors,
                "Year": work.get("publication_year", ""),
                "Journal": journal,
                "DOI": doi_clean,
                "URL": doi if doi else work.get("id", ""),
                "Abstract": abstract,
                "CitationCount": work.get("cited_by_count", 0),
                "Source": "OpenAlex",
            })
        print(f"    Found {len(results)} papers from OpenAlex")
    except Exception as e:
        print(f"    ⚠️  OpenAlex error: {e}")
    return results


# ─────────────────────────────────────────────
# Source: CrossRef
# ─────────────────────────────────────────────
def search_crossref(query: str, limit: int = 20, year_from: Optional[int] = None) -> list:
    print(f"  → Searching CrossRef for: '{query}'")
    url = "https://api.crossref.org/works"
    params = {
        "query": query,
        "rows": min(limit, 100),
        "mailto": CROSSREF_MAILTO,
        "sort": "relevance",
    }
    if year_from:
        params["filter"] = f"from-pub-date:{year_from}"

    results = []
    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        items = data.get("message", {}).get("items", [])
        for item in items:
            authors_list = item.get("author", [])
            authors = "; ".join(
                f"{a.get('family', '')}, {a.get('given', '')}" for a in authors_list[:6]
            )
            doi = item.get("DOI", "")
            pub_date = item.get("published", {}).get("date-parts", [[""]])[0]
            year = pub_date[0] if pub_date else ""
            journal = ""
            container = item.get("container-title", [])
            if container:
                journal = container[0]

            results.append({
                "Title": item.get("title", [""])[0] if item.get("title") else "",
                "Authors": authors,
                "Year": year,
                "Journal": journal,
                "Volume": item.get("volume", ""),
                "Issue": item.get("issue", ""),
                "Pages": item.get("page", ""),
                "DOI": doi,
                "URL": f"https://doi.org/{doi}" if doi else "",
                "Abstract": (item.get("abstract", "") or "")[:500],
                "CitationCount": item.get("is-referenced-by-count", 0),
                "Source": "CrossRef",
            })
        print(f"    Found {len(results)} papers from CrossRef")
    except Exception as e:
        print(f"    ⚠️  CrossRef error: {e}")
    return results


# ─────────────────────────────────────────────
# Source: arXiv
# ─────────────────────────────────────────────
def search_arxiv(query: str, limit: int = 10) -> list:
    print(f"  → Searching arXiv for: '{query}'")
    url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": min(limit, 50),
        "sortBy": "relevance",
    }
    results = []
    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        import xml.etree.ElementTree as ET
        root = ET.fromstring(resp.content)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        entries = root.findall("atom:entry", ns)
        for entry in entries:
            title = entry.find("atom:title", ns)
            title_text = title.text.strip().replace("\n", " ") if title is not None else ""
            abstract = entry.find("atom:summary", ns)
            abstract_text = abstract.text.strip()[:500] if abstract is not None else ""
            published = entry.find("atom:published", ns)
            year = published.text[:4] if published is not None else ""
            arxiv_id = entry.find("atom:id", ns)
            url_text = arxiv_id.text if arxiv_id is not None else ""
            authors_els = entry.findall("atom:author", ns)
            authors = "; ".join(
                a.find("atom:name", ns).text for a in authors_els[:6]
                if a.find("atom:name", ns) is not None
            )
            results.append({
                "Title": title_text,
                "Authors": authors,
                "Year": year,
                "Journal": "arXiv (preprint)",
                "DOI": "",
                "URL": url_text,
                "Abstract": abstract_text,
                "CitationCount": 0,
                "Source": "arXiv",
            })
        print(f"    Found {len(results)} papers from arXiv")
    except Exception as e:
        print(f"    ⚠️  arXiv error: {e}")
    return results


# ─────────────────────────────────────────────
# Deduplication
# ─────────────────────────────────────────────
def deduplicate(papers: list) -> list:
    seen_dois = set()
    seen_titles = set()
    unique = []
    for p in papers:
        doi = (p.get("DOI") or "").strip().lower()
        title = (p.get("Title") or "").strip().lower()[:60]
        if doi and doi in seen_dois:
            continue
        if title and title in seen_titles:
            continue
        if doi:
            seen_dois.add(doi)
        if title:
            seen_titles.add(title)
        unique.append(p)
    return unique


# ─────────────────────────────────────────────
# Save to CSV
# ─────────────────────────────────────────────
def save_to_csv(papers: list, output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for i, paper in enumerate(papers, 1):
            row = {field: "" for field in CSV_FIELDS}
            row.update(paper)
            row["ID"] = i
            row["Included"] = "YES"
            row["Relevance_Score"] = "Medium"
            writer.writerow(row)
    print(f"\n✅ Saved {len(papers)} papers to: {output_path}")


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Multi-source academic paper search")
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument("--limit", type=int, default=20, help="Max papers to retrieve (default: 20)")
    parser.add_argument("--years", type=int, default=5, help="Papers from last N years (default: 5)")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Output CSV path")
    parser.add_argument("--sources", default="ss,openalex,crossref,arxiv",
                        help="Comma-separated sources to use: ss,openalex,crossref,arxiv")
    args = parser.parse_args()

    year_from = datetime.now().year - args.years
    sources = [s.strip().lower() for s in args.sources.split(",")]
    per_source = max(args.limit // len(sources), 5)

    print(f"\n🔍 Searching for: '{args.query}'")
    print(f"   Date range: {year_from}–present | Max results: {args.limit}")
    print(f"   Sources: {', '.join(sources)}\n")

    all_papers = []
    if "ss" in sources:
        all_papers.extend(search_semantic_scholar(args.query, per_source, year_from))
        time.sleep(1)
    if "openalex" in sources:
        all_papers.extend(search_openalex(args.query, per_source, year_from))
        time.sleep(1)
    if "crossref" in sources:
        all_papers.extend(search_crossref(args.query, per_source, year_from))
        time.sleep(1)
    if "arxiv" in sources:
        all_papers.extend(search_arxiv(args.query, min(per_source, 15)))

    print(f"\n📚 Total before dedup: {len(all_papers)}")
    unique_papers = deduplicate(all_papers)
    print(f"📚 After deduplication: {len(unique_papers)}")

    # Sort by citation count descending
    unique_papers.sort(key=lambda x: int(x.get("CitationCount", 0) or 0), reverse=True)

    # Trim to limit
    final_papers = unique_papers[:args.limit]
    save_to_csv(final_papers, args.output)


if __name__ == "__main__":
    main()
