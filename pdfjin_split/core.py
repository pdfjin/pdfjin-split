from pathlib import Path
from typing import List, Union, BinaryIO
import io
import pikepdf


def split_pdf(
    input_pdf: Union[str, Path, bytes, BinaryIO],
    ranges: str,
    output_dir: Union[str, Path] = None,
) -> List[Path]:
    """
    Split a PDF into multiple files based on comma-separated ranges.
    e.g. ranges="1-2, 3, 4-5"
    """
    if isinstance(input_pdf, (str, Path)):
        src = pikepdf.open(str(input_pdf))
    elif isinstance(input_pdf, bytes):
        src = pikepdf.open(io.BytesIO(input_pdf))
    else:
        src = pikepdf.open(input_pdf)

    out_folder = Path(output_dir) if output_dir else Path.cwd()
    out_folder.mkdir(parents=True, exist_ok=True)
    created_files = []

    with src:
        total_pages = len(src.pages)
        for part_idx, range_str in enumerate(ranges.split(",")):
            range_str = range_str.strip()
            if not range_str:
                continue
            parts = range_str.split("-")
            if len(parts) == 1:
                start = end = int(parts[0])
            else:
                start, end = map(int, parts[:2])

            start = max(1, start)
            end = min(total_pages, end)

            new_pdf = pikepdf.new()
            for i in range(start - 1, end):
                new_pdf.pages.append(src.pages[i])

            out_file = out_folder / f"split_part_{part_idx + 1}.pdf"
            new_pdf.save(str(out_file))
            created_files.append(out_file)

    return created_files
