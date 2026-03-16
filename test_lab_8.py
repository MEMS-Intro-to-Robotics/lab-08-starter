#!/usr/bin/env python3
"""
Autograding validation for Lab 8: Hardware Drone Flight & Analysis.
Run with: pytest test_lab_8.py -v
"""

import ast
import os
import warnings

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}
EXPECTED_IMPORTS = {"pandas", "numpy", "matplotlib", "scipy", "csv"}
README_STARTER_FINGERPRINT = "Update this README"


def _get_images(docs_dir="docs"):
    if not os.path.isdir(docs_dir):
        return []
    return [
        f for f in os.listdir(docs_dir)
        if os.path.splitext(f)[1].lower() in IMAGE_EXTENSIONS
    ]


def _get_imports(path):
    with open(path, "r", errors="replace") as f:
        source = f.read()
    tree = ast.parse(source, filename=path)
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            found.add(node.module.split(".")[0])
    return found


# ── Required files (hard fail) ──────────────────────────────


def test_readme_exists():
    assert os.path.isfile("README.md"), "README.md not found"


def test_readme_not_empty():
    assert os.path.getsize("README.md") > 0, "README.md is empty"


def test_readme_updated():
    with open("README.md", "r", errors="replace") as f:
        content = f.read()
    assert README_STARTER_FINGERPRINT not in content, (
        "README.md still contains the starter template text. "
        "Please update it with your name, NetID, and analysis instructions."
    )


def test_analysis_directory_exists():
    assert os.path.isdir("analysis"), "analysis/ directory not found"


def test_analysis_script_exists():
    path = os.path.join("analysis", "lab08_analysis.py")
    assert os.path.isfile(path), "analysis/lab08_analysis.py not found"


def test_analysis_script_not_empty():
    path = os.path.join("analysis", "lab08_analysis.py")
    assert os.path.getsize(path) > 0, "analysis/lab08_analysis.py is empty"


# ── Python syntax (hard fail) ───────────────────────────────


def test_analysis_script_syntax():
    path = os.path.join("analysis", "lab08_analysis.py")
    with open(path, "r", errors="replace") as f:
        source = f.read()
    ast.parse(source, filename=path)


# ── Analysis quality (warnings) ─────────────────────────────


def test_analysis_imports():
    path = os.path.join("analysis", "lab08_analysis.py")
    if not os.path.isfile(path):
        return
    found = _get_imports(path)
    relevant = found & EXPECTED_IMPORTS
    if relevant:
        print(f"Analysis script imports: {', '.join(sorted(relevant))}")
    else:
        warnings.warn(
            f"Analysis script does not import expected data libraries "
            f"({', '.join(sorted(EXPECTED_IMPORTS))}). "
            f"Found: {', '.join(sorted(found)) or 'none'}"
        )


# ── Optional docs (informational) ───────────────────────────


def test_optional_docs():
    if os.path.isdir("docs"):
        images = _get_images()
        if images:
            print(f"Found {len(images)} figure(s) in docs/:")
            for img in sorted(images):
                print(f"  - {img}")
        else:
            print("docs/ exists but contains no images (figures may be in PDF only)")
    else:
        print("docs/ not found (optional)")
