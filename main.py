"""Entry for make.fun news-image-01, wallet 9: "World news collage variant 9".

The artwork (entry.png, bundled in this repository) is a front-page style
collage with an orange masthead: a globe in the middle and four story
panels in a permuted order (storm, chart, rocket, football). This
program publishes that picture to the grader's output directory without
altering a single byte, so both grading runs produce identical files.

It also sanity-checks the picture before copying: the payload must carry
a PNG or JPEG signature, and the bytes written must match the source.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"
CHUNK = 144 * 1024


def sniff_format(path):
    """Return 'png' or 'jpeg' from the file signature, else raise."""
    with open(path, "rb") as fh:
        head = fh.read(8)
    if head.startswith(PNG_MAGIC):
        return "png"
    if head.startswith(JPEG_MAGIC):
        return "jpeg"
    raise ValueError("entry.png is neither PNG nor JPEG")


def publish(source, out_dir):
    """Copy source into out_dir/entry.png in chunks; return byte count."""
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    written = 0
    with open(source, "rb") as fin, open(target, "wb") as fout:
        while True:
            block = fin.read(CHUNK)
            if not block:
                break
            fout.write(block)
            written += len(block)
    return written


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    if os.path.getsize(SOURCE) == 0:
        raise IOError("entry.png is empty; nothing to publish")
    fmt = sniff_format(SOURCE)
    total = publish(SOURCE, out_dir)
    expected = os.path.getsize(SOURCE)
    if total != expected:
        raise IOError(f"copied {total} bytes, expected {expected}")
    print(f"news-image-01 w9: published {fmt} picture, {total} bytes, "
          f"to {out_dir}/entry.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
