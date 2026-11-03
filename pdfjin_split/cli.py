import sys
import argparse
from pathlib import Path
try:
    from .core import split_pdf
    from . import __version__
except (ImportError, ValueError):
    from pdfjin_split.core import split_pdf
    from pdfjin_split import __version__


def main():
    parser = argparse.ArgumentParser(
        prog="pdfjin-split",
        description="Split a PDF file into separate documents by page ranges.",
        epilog="Online web version available at https://pdfjin.com/pages/split-pdf.html",
    )
    parser.add_argument("input", metavar="INPUT_PDF", help="Path to the PDF file to split")
    parser.add_argument("-r", "--ranges", required=True, help="Page ranges (e.g. '1-3, 4, 5-10')")
    parser.add_argument("-o", "--output-dir", default=".", help="Directory to save split files (default: current directory)")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")

    args = parser.parse_args()

    try:
        files = split_pdf(args.input, ranges=args.ranges, output_dir=args.output_dir)
        print(f"✨ Successfully split into {len(files)} file(s):")
        for f in files:
            print(f"   -> {f}")
    except Exception as e:
        print(f"❌ Split failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
