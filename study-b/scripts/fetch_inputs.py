"""Fetch and rebuild the Study B inputs from the public HBCP release.

Downloads two files from the Human Behaviour-Change Project's Info-extract
repository (Apache 2.0), pinned to one commit, then rebuilds exactly what
Study B imported into QualFrame:

  data/texts/<paper>.txt     plain text of the 95 presence-cohort papers
  data/reference_table.csv   724 expert annotation rows (Document, Code, Quotation, Note)

Every download and output is checked against a SHA-256 hash, so a successful
run reproduces the study inputs byte for byte. Nothing is sent anywhere.

Usage:
    python study-b/scripts/fetch_inputs.py            # writes to study-b/data/
    python study-b/scripts/fetch_inputs.py --out DIR
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import sys
import urllib.request
import zipfile
from pathlib import Path

COMMIT = "4a016d6c491e8f231723b2075ee57b93a7b84efa"
BASE = f"https://raw.githubusercontent.com/HumanBehaviourChangeProject/Info-extract/{COMMIT}/"
SOURCES = {
    "corpus": (BASE + "HBCP-Corpus.zip",
               "0ee1d5aee7932e4eb01cbeb8d940c1b27739901f86b80e1ea3841220506e3c56"),
    "annotations": (BASE + "core/src/main/resources/data/jsons/Smoking_AllAnnotations_01Apr19.json",
                    "481caf55e09367d9b818d6fe4e5c99c829b4a611aa9934cdd4927aed2df524de"),
}
HERE = Path(__file__).resolve().parent
STUDY_B = HERE.parent
EXPECTED = json.loads((HERE / "expected_sha256.json").read_text(encoding="utf-8"))

# Two Burke (1994) annotations point to a different report (ICRF 1993). They are
# kept and flagged so they can be left out in a sensitivity analysis.
BURKE_CROSS_REPORT = {"32637256:code:7", "32637256:code:8"}
BCT_NAME = re.compile(r"^(\d+\.\d+)(?:\.\s*|\s+)(.+)$")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def download(url: str, expected: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "qualframe-studies/1.0 (academic replication)"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        body = resp.read()
    if sha256(body) != expected:
        sys.exit(f"Checksum mismatch for {url}; the source may have changed.")
    return body


def walk(attrs, parent=""):
    for a in attrs:
        yield a, parent
        yield from walk(a.get("Attributes", {}).get("AttributesList", []), a["AttributeName"])


def bct_codes(annotations: dict) -> dict:
    """Map HBCP attribute IDs to BCT numbers for the leaf techniques."""
    root = next(a for s in annotations["CodeSets"] if s["SetName"] == "Intervention"
                for a in s["Attributes"]["AttributesList"] if a["AttributeName"] == "BCTs")
    codes = {}
    for a, _ in walk(root["Attributes"]["AttributesList"]):
        m = BCT_NAME.match(a["AttributeName"])
        if m:
            codes[a["AttributeId"]] = m[1]
    return codes


def paper_text(paper: dict) -> str:
    """Join text blocks and flattened table cells, as in the original preparation."""
    parts = []
    for block in paper["content"]:
        if block["type"] == "TEXT":
            parts.append(block.get("text", ""))
        else:
            parts.append("\n".join(
                " | ".join(c.get("rowHeaders", []) + c.get("columnHeaders", []) + [c.get("value", "")])
                for c in block.get("cells", [])))
    return "\n\n".join(parts)


def quotation(raw: str) -> str:
    """Take the highlighted span between HBCP's [¬s] and [¬e] markers."""
    if not raw:
        return ""
    m = re.search(r"\[¬s\](.*?)\[¬e\]", raw, re.S)
    if not m or raw.count("[¬s]") != 1 or raw.count("[¬e]") != 1:
        sys.exit("Unexpected highlight markers in the annotation source.")
    return "\n".join(line.removeprefix('"').removesuffix('"') for line in m[1].split("\n"))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path, default=STUDY_B / "data")
    args = ap.parse_args()

    with open(STUDY_B / "cohorts.csv", encoding="utf-8") as f:
        presence = {r["paper_id"] for r in csv.DictReader(f) if r["in_presence_cohort"] == "yes"}

    print("Downloading the HBCP corpus and annotations ...")
    corpus = zipfile.ZipFile(io.BytesIO(download(*SOURCES["corpus"])))
    annotations = json.loads(download(*SOURCES["annotations"]).decode("utf-8-sig"))
    codes = bct_codes(annotations)
    refs = {r["ShortTitle"]: r for r in annotations["References"]}

    members = [n for n in corpus.namelist()
               if "/OA-HBCP-Corpus/" in n and n.endswith(".json") and "__MACOSX" not in n]
    members.sort(key=str.lower)  # the original preparation ran on Windows, which sorts paths case-insensitively

    text_dir = args.out / "texts"
    text_dir.mkdir(parents=True, exist_ok=True)
    rows, written = [], 0
    for name in members:
        paper = json.loads(corpus.read(name).decode("utf-8"))
        doc = paper["shortTitle"]
        if doc in presence:
            path = text_dir / f"{doc}.txt"
            with open(path, "w", encoding="utf-8", newline="\r\n") as f:
                f.write(paper_text(paper))
            written += 1
        ref = refs[doc]
        for ci, code in enumerate(ref["Codes"]):
            if code["AttributeId"] not in codes:
                continue
            ann_id = f"{ref['ItemId']}:code:{ci}"
            details = code.get("ItemAttributeFullTextDetails", [])
            for idx, quote in enumerate([quotation(d.get("Text", "")) for d in details] or [""]):
                note = f"annotation_id={ann_id}; detail_index={idx}"
                if ann_id in BURKE_CROSS_REPORT:
                    note = "BURKE cross-report (ICRF 1993); " + note
                if not details:
                    note += "; no quotation detail recorded (presence only)"
                rows.append({"Document": doc, "Code": codes[code["AttributeId"]], "Quotation": quote, "Note": note})

    buf = io.StringIO(newline="")
    w = csv.DictWriter(buf, fieldnames=["Document", "Code", "Quotation", "Note"], lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    ref_path = args.out / "reference_table.csv"
    ref_path.write_text("﻿" + buf.getvalue(), encoding="utf-8", newline="")

    problems = [doc for doc, h in EXPECTED["texts"].items()
                if not (text_dir / f"{doc}.txt").exists() or sha256((text_dir / f"{doc}.txt").read_bytes()) != h]
    if sha256(ref_path.read_bytes()) != EXPECTED["reference_table.csv"]:
        problems.append("reference_table.csv")
    print(f"Wrote {written} texts and {len(rows)} reference rows to {args.out}")
    if problems:
        sys.exit(f"{len(problems)} output(s) differ from the study inputs: {problems[:5]}")
    print("All outputs match the Study B inputs.")


if __name__ == "__main__":
    main()
