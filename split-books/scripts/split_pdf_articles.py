#!/usr/bin/env python3
"""Split an article-style PDF into per-item PDFs using start and end markers."""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path

import pdfplumber
from pypdf import PdfReader, PdfWriter


ILLEGAL_FILENAME = re.compile(r'[\\/:*?"<>|]')
DEFAULT_START = r"摘\s*要|摘要|内容提要"
DEFAULT_END = r"[（(]\s*责任编辑\s*[:：]"


@dataclass
class Article:
    title: str
    start: int
    end: int
    method: str


def clean_text(text: str) -> str:
    text = re.sub(r"[\ufeff\u200b\u200e\u200f\u202a-\u202e\u00ad\u2060]", "", text)
    return re.sub(r"[ \t]+", " ", text).strip()


def compact(text: str) -> str:
    return re.sub(r"\s+", "", clean_text(text))


def safe_name(title: str) -> str:
    title = ILLEGAL_FILENAME.sub("_", title)
    title = re.sub(r"\s+", "", title).strip(" ._")
    return title[:180] or "未命名"


def looks_like_author(line: str) -> bool:
    value = compact(line).strip("*＊")
    if not value:
        return True
    stripped = line.strip(" *＊")
    if re.search(r"[\s　·]", stripped):
        return len(value) <= 16 and bool(re.match(r"^[\u4e00-\u9fff]{1,4}(?:[\s·　]+[\u4e00-\u9fff]{1,4}){0,4}$", stripped))
    return 2 <= len(value) <= 4 and bool(re.match(r"^[\u4e00-\u9fff]+$", value))


def clean_title(title: str, main_title_only: bool) -> str:
    title = clean_text(title)
    title = re.sub(r"^(?:特别策划|专题研究|案例聚焦|类案研究|域外案例|国外司法|高端论坛|新法新释|巡回法庭专栏|法官说法)[:：]?", "", title)
    title = re.sub(r"\s+", "", title)
    title = re.sub(r"[〔［\[]?\d+[〕］\]]?[*＊]?$", "", title)
    if main_title_only:
        title = re.split(r"——+|一一+|—|--+|－|–", title, maxsplit=1)[0]
    return title.strip(" ：:，,、。")


def extract_title(page_text: str, start_regex: re.Pattern[str], main_title_only: bool) -> str | None:
    lines = [clean_text(line) for line in page_text.splitlines()]
    marker_index = None
    for index, line in enumerate(lines[:24]):
        if start_regex.search(line):
            marker_index = index
            break
    if marker_index is None:
        return None

    parts: list[str] = []
    for line in reversed(lines[:marker_index]):
        if not line or line == "CMYK":
            continue
        if re.match(r"^(法律适用|Journal|CONTENTS|目录|\d{1,3})", compact(line), re.I):
            if parts:
                break
            continue
        if parts and (line.startswith("编辑提示") or len(compact(line)) > 45 or re.search(r"[。！？；]", line)):
            break
        if looks_like_author(line):
            if parts:
                break
            continue
        if re.search(r"[\u4e00-\u9fff]", line) and len(compact(line)) >= 4:
            parts.append(line)
    if not parts:
        return None
    title = clean_title("".join(reversed(parts)), main_title_only)
    if len(title) < 4 or not re.search(r"[\u4e00-\u9fffA-Za-z]", title):
        return None
    return title


def detect_starts(page_texts: list[str], start_regex: re.Pattern[str], main_title_only: bool) -> list[tuple[int, str]]:
    starts: list[tuple[int, str]] = []
    for index, text in enumerate(page_texts):
        if not start_regex.search(text[:3000]):
            continue
        title = extract_title(text, start_regex, main_title_only)
        if not title:
            continue
        if starts and index - starts[-1][0] < 2:
            continue
        starts.append((index, title))
    return starts


def build_articles(page_texts: list[str], starts: list[tuple[int, str]], end_regex: re.Pattern[str]) -> list[Article]:
    articles: list[Article] = []
    for idx, (start, title) in enumerate(starts):
        limit = starts[idx + 1][0] - 1 if idx + 1 < len(starts) else len(page_texts) - 1
        end_pages = [page for page in range(start, limit + 1) if end_regex.search(page_texts[page])]
        if end_pages:
            end = end_pages[-1]
        else:
            end = limit
        articles.append(Article(title, start, end, "start-marker"))
    return articles


def write_pdf(reader: PdfReader, article: Article, output_dir: Path) -> Path:
    path = output_dir / f"{safe_name(article.title)}.pdf"
    suffix = 2
    while path.exists():
        path = output_dir / f"{safe_name(article.title)}_{suffix}.pdf"
        suffix += 1
    writer = PdfWriter()
    for page in range(article.start, article.end + 1):
        writer.add_page(reader.pages[page])
    with path.open("wb") as file:
        writer.write(file)
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf")
    parser.add_argument("--output", required=True)
    parser.add_argument("--start-regex", default=DEFAULT_START)
    parser.add_argument("--end-regex", default=DEFAULT_END)
    parser.add_argument("--main-title-only", action="store_true")
    args = parser.parse_args()

    pdf_path = Path(args.pdf).resolve()
    output_dir = Path(args.output).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    start_regex = re.compile(args.start_regex)
    end_regex = re.compile(args.end_regex)

    with pdfplumber.open(str(pdf_path)) as pdf:
        page_texts = [page.extract_text() or "" for page in pdf.pages]

    starts = detect_starts(page_texts, start_regex, args.main_title_only)
    articles = build_articles(page_texts, starts, end_regex)
    reader = PdfReader(str(pdf_path))

    rows = []
    for article in articles:
        out = write_pdf(reader, article, output_dir)
        rows.append(
            {
                "source_pdf": str(pdf_path),
                "output_pdf": str(out),
                "title": article.title,
                "start_page": article.start + 1,
                "end_page": article.end + 1,
                "pages": article.end - article.start + 1,
                "method": article.method,
            }
        )

    report = output_dir / "split_report.csv"
    with report.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=["source_pdf", "output_pdf", "title", "start_page", "end_page", "pages", "method"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Split {len(rows)} items into {output_dir}")


if __name__ == "__main__":
    main()
