from __future__ import annotations

import base64
from dataclasses import dataclass
from pathlib import Path

import streamlit as st


@dataclass(frozen=True)
class CellVariant:
    key: str
    title: str
    description: str
    asset_path: Path


ROOT_DIR = Path(__file__).resolve().parent
ASSETS_DIR = ROOT_DIR / "assets"

VARIANTS = [
    CellVariant(
        key="catl",
        title="CATL inspired",
        description="Dark housing with orange accent lines.",
        asset_path=ASSETS_DIR / "prismatic-cell-catl.svg",
    ),
    CellVariant(
        key="byd",
        title="BYD inspired",
        description="Cool blue palette with crisp highlights.",
        asset_path=ASSETS_DIR / "prismatic-cell-byd.svg",
    ),
    CellVariant(
        key="sdi",
        title="SDI inspired",
        description="Neutral industrial tones with balanced contrast.",
        asset_path=ASSETS_DIR / "prismatic-cell-sdi.svg",
    ),
]


def svg_to_data_uri(path: Path) -> str:
    svg_content = path.read_text(encoding="utf-8")
    encoded = base64.b64encode(svg_content.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded}"


def ensure_assets_exist() -> None:
    missing = [variant.asset_path.name for variant in VARIANTS if not variant.asset_path.exists()]
    if missing:
        missing_list = ", ".join(missing)
        raise FileNotFoundError(f"Missing SVG assets: {missing_list}")


def render_header() -> None:
    st.markdown(
        """
        <div class="hero">
          <p class="eyebrow">Prismatic battery cell renders</p>
          <h1>3D-styled visuals for 500mm x 100mm x 20mm cells</h1>
          <p class="subtitle">
            Terminal layouts match left and right side placements, with visual cues inspired by CATL,
            BYD, and SDI product photography.
          </p>
          <div class="badges">
            <span>CATL</span>
            <span>BYD</span>
            <span>SDI</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_card(variant: CellVariant) -> None:
    data_uri = svg_to_data_uri(variant.asset_path)
    st.markdown(
        f"""
        <div class="card">
          <div class="card-header">
            <h2>{variant.title}</h2>
            <p>{variant.description}</p>
          </div>
          <img src="{data_uri}" alt="{variant.title} prismatic cell render" />
          <ul>
            <li>500mm x 100mm x 20mm</li>
            <li>Terminals on left and right sides</li>
          </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    st.set_page_config(page_title="Prismatic Battery Cell Renders", layout="wide")
    ensure_assets_exist()

    st.markdown(
        """
        <style>
          body {
            color: #0f172a;
            background: #eef1f6;
          }
          .hero {
            background: #0f172a;
            color: #f8fafc;
            padding: 40px 48px;
            border-radius: 24px;
            margin-bottom: 32px;
          }
          .hero h1 {
            font-size: 32px;
            margin: 12px 0 12px;
          }
          .eyebrow {
            text-transform: uppercase;
            letter-spacing: 0.18em;
            font-size: 12px;
            color: #a5b4fc;
            margin: 0;
          }
          .subtitle {
            font-size: 15px;
            line-height: 1.6;
            color: #d8e2ff;
            margin: 0 0 16px;
          }
          .badges {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
          }
          .badges span {
            background: rgba(148, 163, 184, 0.22);
            border: 1px solid rgba(148, 163, 184, 0.4);
            padding: 6px 14px;
            border-radius: 999px;
            font-size: 12px;
          }
          .card {
            background: #ffffff;
            border-radius: 18px;
            padding: 20px;
            box-shadow: 0 16px 32px rgba(15, 23, 42, 0.08);
            display: flex;
            flex-direction: column;
            gap: 16px;
            height: 100%;
          }
          .card img {
            width: 100%;
            height: auto;
          }
          .card-header h2 {
            margin: 0 0 6px;
            font-size: 20px;
          }
          .card-header p {
            margin: 0;
            color: #4b5563;
            font-size: 14px;
          }
          .card ul {
            margin: 0;
            padding-left: 18px;
            color: #4b5563;
            font-size: 14px;
            display: grid;
            gap: 6px;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )

    render_header()
    columns = st.columns(len(VARIANTS))
    for column, variant in zip(columns, VARIANTS):
        with column:
            render_card(variant)

    st.markdown(
        "Generated SVGs live in `assets/`. Update them with `python3 scripts/generate_prismatic_cells.py`."
    )


if __name__ == "__main__":
    main()
