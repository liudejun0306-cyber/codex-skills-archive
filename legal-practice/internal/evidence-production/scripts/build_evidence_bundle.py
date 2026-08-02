#!/usr/bin/env python3
"""Build numbered exhibit PDFs, a merged bundle, and a page map from JSON."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageOps
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas

OFFICE = {".docx", ".doc", ".xlsx", ".xls", ".pptx", ".ppt", ".odt", ".ods", ".odp"}
IMAGES = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"}


def safe_name(value: str) -> str:
    value = re.sub(r"[\\/:*?\"<>|\r\n]+", "_", value).strip(" ._")
    return value[:80] or "未命名证据"


def parse_pages(spec: str | None, total: int) -> list[int]:
    if not spec:
        return list(range(total))
    result: list[int] = []
    for part in str(spec).replace(" ", "").split(","):
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            start, end = int(a), int(b)
            if start > end:
                raise ValueError(f"页码范围倒置：{part}")
            result.extend(range(start - 1, end))
        else:
            result.append(int(part) - 1)
    if not result or min(result) < 0 or max(result) >= total:
        raise ValueError(f"页码越界：{spec}，文件共 {total} 页")
    if len(set(result)) != len(result):
        raise ValueError(f"页码重复：{spec}")
    return result


def image_to_pdf(source: Path, target: Path) -> None:
    frames = []
    with Image.open(source) as img:
        for n in range(getattr(img, "n_frames", 1)):
            img.seek(n)
            frame = ImageOps.exif_transpose(img.copy()).convert("RGB")
            frames.append(frame)
    if not frames:
        raise ValueError(f"图片无可用帧：{source}")
    frames[0].save(target, "PDF", save_all=True, append_images=frames[1:], resolution=150)


def convert_office(source: Path, work: Path) -> Path:
    soffice = shutil.which("soffice")
    if not soffice:
        raise RuntimeError("找不到 soffice，无法转换 Office 文件")
    token = hashlib.sha256(str(source).encode("utf-8")).hexdigest()[:12]
    outdir = work / f"office_{token}"
    profile = work / f"lo_profile_{token}"
    outdir.mkdir(parents=True, exist_ok=True)
    profile.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        [soffice, f"-env:UserInstallation={profile.as_uri()}", "--headless",
         "--convert-to", "pdf", "--outdir", str(outdir), str(source)],
        capture_output=True, text=True, timeout=180,
    )
    target = outdir / f"{source.stem}.pdf"
    if proc.returncode or not target.exists():
        raise RuntimeError(f"Office 转换失败：{source}\n{proc.stdout}\n{proc.stderr}")
    return target


def to_pdf(source: Path, work: Path) -> Path:
    ext = source.suffix.lower()
    if ext == ".pdf":
        return source
    if ext in IMAGES:
        target = work / f"{source.stem}_{abs(hash(source))}.pdf"
        image_to_pdf(source, target)
        return target
    if ext in OFFICE:
        return convert_office(source, work)
    raise ValueError(f"不支持转换为 PDF 的格式：{source}")


def add_page_number(page, number: int):
    width = float(page.mediabox.width)
    height = float(page.mediabox.height)
    stream = io.BytesIO()
    c = canvas.Canvas(stream, pagesize=(width, height))
    c.setFont("Helvetica", 9)
    c.drawCentredString(width / 2, 18, str(number))
    c.save()
    stream.seek(0)
    overlay = PdfReader(stream).pages[0]
    page.merge_page(overlay)
    return page


def resolve_source(plan_dir: Path, raw: str) -> Path:
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = plan_dir / path
    path = path.resolve()
    if not path.is_file():
        raise FileNotFoundError(f"源文件不存在：{path}")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="生成单项证据 PDF、证据册和页码映射")
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--stamp-pages", action="store_true")
    args = parser.parse_args()

    plan_path = args.plan.resolve()
    plan = json.loads(plan_path.read_text(encoding="utf-8-sig"))
    exhibits = [x for x in plan.get("exhibits", []) if not x.get("exclude", False)]
    if not exhibits:
        raise ValueError("组卷计划中没有可提交的证据")
    numbers = [int(x["number"]) for x in exhibits]
    if any(n <= 0 for n in numbers) or len(set(numbers)) != len(numbers):
        raise ValueError("证据编号必须为不重复的正整数")
    exhibits.sort(key=lambda x: int(x["number"]))
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    bundle = PdfWriter()
    page_map = []
    current_page = 1
    with tempfile.TemporaryDirectory(prefix="evidence-build-") as tmp:
        work = Path(tmp)
        for exhibit in exhibits:
            number = int(exhibit["number"])
            name = str(exhibit.get("name", "")).strip()
            sources = exhibit.get("sources") or []
            if not name or not sources:
                raise ValueError(f"证据 {number} 缺少名称或来源文件")
            writer = PdfWriter()
            source_refs = []
            for item in sources:
                source = resolve_source(plan_path.parent, item["path"])
                pdf = to_pdf(source, work)
                reader = PdfReader(str(pdf))
                if reader.is_encrypted:
                    raise ValueError(f"PDF 已加密：{source}")
                selected = parse_pages(item.get("pages"), len(reader.pages))
                for idx in selected:
                    writer.add_page(reader.pages[idx])
                source_refs.append(f"{source}:{item.get('pages') or '全部'}")
            filename = f"证据{number:02d}_{safe_name(name)}.pdf"
            exhibit_path = output / filename
            with exhibit_path.open("wb") as f:
                writer.write(f)

            reader = PdfReader(str(exhibit_path))
            start = current_page
            for page in reader.pages:
                if args.stamp_pages:
                    page = add_page_number(page, current_page)
                bundle.add_page(page)
                current_page += 1
            end = current_page - 1
            page_map.append({
                "证据编号": number,
                "证据名称": name,
                "单项文件": filename,
                "起始页": start,
                "结束页": end,
                "页码": f"第{start}-{end}页" if start != end else f"第{start}页",
                "来源文件及选页": " | ".join(source_refs),
            })

    bundle_name = safe_name(Path(plan.get("bundle_name", "证据册.pdf")).stem) + ".pdf"
    with (output / bundle_name).open("wb") as f:
        bundle.write(f)
    with (output / "证据页码映射.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(page_map[0]))
        writer.writeheader()
        writer.writerows(page_map)
    print(f"已生成 {len(page_map)} 项证据，共 {current_page - 1} 页：{output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
