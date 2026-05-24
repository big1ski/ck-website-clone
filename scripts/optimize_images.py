#!/usr/bin/env python3
"""
Phase 1 image optimization.

Reads every JPG/JPEG/PNG under assets/photos, assets/gallery, assets/projects
and writes AVIF + WebP + JPG variants at 400w, 800w, 1600w into
assets/optimized/<same-subdir>/.

Logos under assets/logos/ are NOT processed (already small).

Does not modify any source file.
"""

import argparse
import os
import sys
from pathlib import Path

from PIL import Image
import pillow_avif  # noqa: F401  (registers the AVIF plugin)

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIRS = ["assets/photos", "assets/gallery", "assets/projects"]
OUT_DIR = REPO_ROOT / "assets" / "optimized"
WIDTHS = [400, 800, 1600]
JPG_QUALITY = 82
WEBP_QUALITY = 80
AVIF_QUALITY = 60  # AVIF q=60 ≈ WebP q=80 in perceptual quality
SUPPORTED = {".jpg", ".jpeg", ".png"}


def variants_for(src: Path):
    """Return list of (out_path, width, format) tuples this source produces."""
    rel = src.relative_to(REPO_ROOT)
    stem = src.stem
    out_subdir = OUT_DIR / rel.parent.relative_to("assets")
    result = []
    for w in WIDTHS:
        for fmt, ext in [("avif", ".avif"), ("webp", ".webp"), ("jpg", ".jpg")]:
            result.append((out_subdir / f"{stem}-{w}{ext}", w, fmt))
    return result


def process(src: Path, dry_run: bool):
    """Generate variants for one source image. Returns total bytes written (estimated for dry run)."""
    try:
        im = Image.open(src)
        im.load()
    except Exception as e:
        print(f"  SKIP (cannot open): {src} — {e}", file=sys.stderr)
        return 0

    # Strip EXIF orientation by applying it
    from PIL import ImageOps
    im = ImageOps.exif_transpose(im)
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGB")

    native_w, native_h = im.size
    total_written = 0

    for out_path, target_w, fmt in variants_for(src):
        if target_w > native_w:
            # Don't upscale; cap at native width and rename
            target_w_actual = native_w
            out_path = out_path.parent / f"{src.stem}-{native_w}{out_path.suffix}"
        else:
            target_w_actual = target_w

        target_h = round(native_h * (target_w_actual / native_w))

        if dry_run:
            # Rough estimate
            est = (target_w_actual * target_h) // 8
            total_written += est
            continue

        out_path.parent.mkdir(parents=True, exist_ok=True)
        resized = im.resize((target_w_actual, target_h), Image.LANCZOS)

        try:
            if fmt == "jpg":
                resized.convert("RGB").save(out_path, "JPEG", quality=JPG_QUALITY, optimize=True, progressive=True)
            elif fmt == "webp":
                resized.save(out_path, "WEBP", quality=WEBP_QUALITY, method=6)
            elif fmt == "avif":
                resized.save(out_path, "AVIF", quality=AVIF_QUALITY)
            total_written += out_path.stat().st_size
        except Exception as e:
            print(f"  FAIL: {out_path} — {e}", file=sys.stderr)

    return total_written


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Scan and estimate, do not write files")
    args = parser.parse_args()

    sources = []
    for d in SRC_DIRS:
        p = REPO_ROOT / d
        if not p.exists():
            print(f"WARN: {p} does not exist, skipping", file=sys.stderr)
            continue
        for f in sorted(p.rglob("*")):
            if f.is_file() and f.suffix.lower() in SUPPORTED:
                sources.append(f)

    if not sources:
        print("No source images found.")
        return 1

    src_total = sum(s.stat().st_size for s in sources)
    print(f"Found {len(sources)} source images, {src_total / 1024 / 1024:.1f} MB total")
    print(f"Will produce {len(sources) * len(WIDTHS) * 3} variants ({len(WIDTHS)} widths × 3 formats per source)")
    print(f"Output directory: {OUT_DIR}")
    if args.dry_run:
        print("\n[DRY RUN] No files will be written.\n")

    out_total = 0
    for i, src in enumerate(sources, 1):
        rel = src.relative_to(REPO_ROOT)
        print(f"[{i:3d}/{len(sources)}] {rel}")
        out_total += process(src, args.dry_run)

    print()
    print(f"Source total:   {src_total / 1024 / 1024:7.1f} MB")
    if args.dry_run:
        print(f"Estimated out:  {out_total / 1024 / 1024:7.1f} MB (rough estimate)")
        print("\nRe-run without --dry-run to actually generate the variants.")
    else:
        print(f"Output total:   {out_total / 1024 / 1024:7.1f} MB")
        print(f"Reduction:      {(1 - out_total / src_total) * 100:5.1f}% smaller (but we ship only ONE variant per visitor)")
        print(f"Single-variant savings will be much larger.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
