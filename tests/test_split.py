import pytest
import io
import pikepdf
from pathlib import Path
from pdfjin_split.core import split_pdf


def create_dummy_pdf(num_pages: int = 5) -> bytes:
    pdf = pikepdf.new()
    for _ in range(num_pages):
        pdf.add_blank_page(page_size=(300, 300))
    buf = io.BytesIO()
    pdf.save(buf)
    return buf.getvalue()


def test_split_ranges(tmp_path: Path):
    src = tmp_path / "test.pdf"
    src.write_bytes(create_dummy_pdf(6))

    out_files = split_pdf(src, ranges="1-2, 3-4, 5-6", output_dir=tmp_path)
    assert len(out_files) == 3
    for f in out_files:
        assert f.exists()
        with pikepdf.open(str(f)) as p:
            assert len(p.pages) == 2
