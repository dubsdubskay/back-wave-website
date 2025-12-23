import re
import sys
from pathlib import Path

#====================================================================================
# Executable script to generate or update a Table of Contents (TOC)
# in a Markdown file based on its headings.
#====================================================================================
# Must be in folder of python script to run:
# then map to your markdown file:
# Example:
#       - terminal is at "hangar_queens" folder
#       - generate_toc.py is in "markdowns" folder (1 level below)
#       - the markdown file is in Cheatsheets folder (2 levels below)
# $ python markdowns/generate_toc.py markdowns/concept.md
#
# $ python markdowns/generate_toc.py markdowns/Cheatsheet/terminal_codes_latex.md
#====================================================================================

FENCE_RE = re.compile(r"^(```|~~~)")

def fence_mask(lines):
    """
    Return a list[bool] same length as lines where True means the line is
    inside a fenced code block (``` or ~~~).
    """
    mask = []
    in_fence = False
    fence_token = None  # track which fence started (``` or ~~~)
    for line in lines:
        m = FENCE_RE.match(line.strip())
        if m:
            token = m.group(1)
            if not in_fence:
                in_fence = True
                fence_token = token
            else:
                # only close if same token type
                if token == fence_token:
                    in_fence = False
                    fence_token = None
        mask.append(in_fence)
    return mask

def slugify(header_text: str) -> str:
    """
    Convert header text to a GitHub-style anchor.
    Rules:
    - lowercase
    - remove anything that's not a letter/number/space/hyphen
    - collapse spaces to hyphens
    - collapse multiple hyphens
    """
    text = header_text.strip().lower()

    # remove characters that aren't alphanum, space, or hyphen
    text = re.sub(r"[^a-z0-9\s-]", "", text)

    # spaces -> hyphens
    text = re.sub(r"\s+", "-", text)

    # collapse multiple hyphens
    text = re.sub(r"-{2,}", "-", text)

    return text

def extract_headings(md_lines):
    """
    Return a list of (level, text) for headings like
    '## My Section', '### Another Section'
       - We ignore level 1 (# ...) in the TOC by default unless you want it..
       - Skips headings inside fenced code blocks and HTML comments.
    """
    in_fence = fence_mask(md_lines)
    headings = []
    header_pattern = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
    for i, line in enumerate(md_lines):
        if in_fence[i]:
            continue
        m = header_pattern.match(line)
        if m:
            hashes, title = m.groups()
            # skip headings that are code fences or commented out
            if not title.startswith("<!--"):
                headings.append((len(hashes), title))
    return headings

def build_toc(headings, include_h1=False, toc_title="## Table of Contents"):
    """
    Build a markdown TOC. Indent deeper levels.
    include_h1=False means we skip level-1 headings in the TOC.
    """
    toc_lines = [toc_title]

    for level, title in headings:
        if level == 1 and not include_h1:
            continue

        anchor = slugify(title)

        # indent with 2 spaces per depth beyond level 2
        # so:
        # ## Heading (level 2) -> no indent
        # ### Subheading (level 3) -> 2 spaces
        # #### Sub-sub (level 4) -> 4 spaces
        indent = "  " * (level - 2 if level >= 2 else 0)

        toc_lines.append(f"{indent}- [{title}](#{anchor})")

    toc_lines.append("")  # trailing newline
    return "\n".join(toc_lines)

def insert_or_replace_toc(md_text, toc_block, toc_heading="## Table of Contents"):
    """
    If a TOC section already exists (starts with '## Table of Contents'
    and goes until the next heading of same or higher level), replace it.
    Otherwise insert right after the first top-level heading (# ...) if found,
    else at the very top.
    """

    lines = md_text.splitlines()
    in_fence = fence_mask(lines)

    # 1) Find an existing TOC heading outside fences
    toc_start_idx = None
    heading_text = toc_heading.lstrip("# ").strip()
    toc_re = re.compile(rf"^##\s+{re.escape(heading_text)}\s*$", flags=re.IGNORECASE)

    for i, line in enumerate(lines):
        if in_fence[i]:
            continue
        if toc_re.match(line):
            toc_start_idx = i
            break

    if toc_start_idx is not None:
        # Find where TOC ends: next H1 or H2 outside fences
        toc_end_idx = len(lines)
        for j in range(toc_start_idx + 1, len(lines)):
            if in_fence[j]:
                continue
            if re.match(r"^#{1,2}\s+", lines[j]):
                toc_end_idx = j
                break
        new_lines = lines[:toc_start_idx] + toc_block.splitlines() + lines[toc_end_idx:]
        return "\n".join(new_lines) + "\n"

    # 2) Insert after first H1 (# ...) outside fences
    first_h1_idx = None
    for i, line in enumerate(lines):
        if in_fence[i]:
            continue
        if re.match(r"^#\s+", line):
            first_h1_idx = i
            break

    if first_h1_idx is not None:
        insert_at = first_h1_idx + 1
        while insert_at < len(lines) and lines[insert_at].strip() == "":
            insert_at += 1
        new_lines = lines[:insert_at] + ["", toc_block, ""] + lines[insert_at:]
        return "\n".join(new_lines) + "\n"

    # 3) Fallback: prepend
    return toc_block + "\n\n" + md_text


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_toc.py your_file.md")
        sys.exit(1)

    md_path = Path(sys.argv[1])
    if not md_path.exists():
        print(f"Error: {md_path} not found")
        sys.exit(1)

    md_text = md_path.read_text(encoding="utf-8")
    lines = md_text.splitlines()

    headings = extract_headings(lines)
    toc_block = build_toc(headings, include_h1=False)

    new_md = insert_or_replace_toc(md_text, toc_block)

    # overwrite the same file (you can change this to write to a new file)
    md_path.write_text(new_md, encoding="utf-8")
    print(f"TOC updated in {md_path}")

if __name__ == "__main__":
    main()

