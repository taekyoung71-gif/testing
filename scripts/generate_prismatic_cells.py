from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Colors:
    background: str
    front: str
    top: str
    side: str
    stroke: str
    terminal: str
    terminal_ring: str
    label: str
    accent: str


@dataclass(frozen=True)
class CellGeometry:
    x: int
    y: int
    width: int
    height: int
    depth_x: int
    depth_y: int
    terminal_length: int
    terminal_height: int
    terminal_corner_radius: int
    terminal_hole_radius: int
    terminal_hole_ring: int


CANVAS_WIDTH = 1400
CANVAS_HEIGHT = 700
GEOMETRY = CellGeometry(
    x=200,
    y=300,
    width=1100,
    height=220,
    depth_x=44,
    depth_y=-28,
    terminal_length=28,
    terminal_height=80,
    terminal_corner_radius=10,
    terminal_hole_radius=11,
    terminal_hole_ring=5,
)


VARIANTS: dict[str, Colors] = {
    "catl": Colors(
        background="#f6f7f9",
        front="#2d3136",
        top="#3a4046",
        side="#24282c",
        stroke="#1b1f22",
        terminal="#cfd3d8",
        terminal_ring="#8a9098",
        label="#f4f5f7",
        accent="#ff7a18",
    ),
    "byd": Colors(
        background="#f1f6ff",
        front="#e2ecff",
        top="#f3f7ff",
        side="#cddbf2",
        stroke="#9fb4d6",
        terminal="#c6ccd6",
        terminal_ring="#7f8aa0",
        label="#1d2a44",
        accent="#1270ff",
    ),
    "sdi": Colors(
        background="#f7f8fb",
        front="#d9dee6",
        top="#edf0f5",
        side="#c1c9d4",
        stroke="#8a95a5",
        terminal="#d4d7dd",
        terminal_ring="#7d8796",
        label="#1f2a38",
        accent="#6b7788",
    ),
}


OUTPUT_DIR = Path(__file__).resolve().parents[1] / "assets"


def points(*coords: tuple[int, int]) -> str:
    return " ".join(f"{x},{y}" for x, y in coords)


def build_svg(variant: str, colors: Colors) -> str:
    geo = GEOMETRY
    x = geo.x
    y = geo.y
    width = geo.width
    height = geo.height
    dx = geo.depth_x
    dy = geo.depth_y

    top_face = points((x, y), (x + width, y), (x + width + dx, y + dy), (x + dx, y + dy))
    right_face = points(
        (x + width, y),
        (x + width, y + height),
        (x + width + dx, y + height + dy),
        (x + width + dx, y + dy),
    )
    front_face = points((x, y), (x + width, y), (x + width, y + height), (x, y + height))

    terminal_y = y + (height - geo.terminal_height) // 2
    left_terminal_x = x - geo.terminal_length
    right_terminal_x = x + width
    terminal_center_y = terminal_y + geo.terminal_height // 2
    terminal_center_left_x = left_terminal_x + geo.terminal_length * 0.5
    terminal_center_right_x = right_terminal_x + geo.terminal_length * 0.5

    label_x = x + width * 0.5
    label_y = y + height * 0.55

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_WIDTH}" height="{CANVAS_HEIGHT}" viewBox="0 0 {CANVAS_WIDTH} {CANVAS_HEIGHT}">
  <rect width="100%" height="100%" fill="{colors.background}" />
  <g stroke="{colors.stroke}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round">
    <polygon points="{top_face}" fill="{colors.top}" />
    <polygon points="{right_face}" fill="{colors.side}" />
    <polygon points="{front_face}" fill="{colors.front}" />
    <line x1="{x}" y1="{y + height * 0.28}" x2="{x + width}" y2="{y + height * 0.28}" stroke="{colors.accent}" stroke-width="3" />
    <line x1="{x}" y1="{y + height * 0.72}" x2="{x + width}" y2="{y + height * 0.72}" stroke="{colors.accent}" stroke-width="3" />
  </g>
  <g stroke="{colors.stroke}" stroke-width="2">
    <rect x="{left_terminal_x}" y="{terminal_y}" width="{geo.terminal_length}" height="{geo.terminal_height}" rx="{geo.terminal_corner_radius}" ry="{geo.terminal_corner_radius}" fill="{colors.terminal}" />
    <circle cx="{terminal_center_left_x}" cy="{terminal_center_y}" r="{geo.terminal_hole_radius}" fill="{colors.terminal}" stroke="{colors.stroke}" />
    <circle cx="{terminal_center_left_x}" cy="{terminal_center_y}" r="{geo.terminal_hole_ring}" fill="{colors.terminal_ring}" stroke="{colors.stroke}" />

    <rect x="{right_terminal_x}" y="{terminal_y}" width="{geo.terminal_length}" height="{geo.terminal_height}" rx="{geo.terminal_corner_radius}" ry="{geo.terminal_corner_radius}" fill="{colors.terminal}" />
    <circle cx="{terminal_center_right_x}" cy="{terminal_center_y}" r="{geo.terminal_hole_radius}" fill="{colors.terminal}" stroke="{colors.stroke}" />
    <circle cx="{terminal_center_right_x}" cy="{terminal_center_y}" r="{geo.terminal_hole_ring}" fill="{colors.terminal_ring}" stroke="{colors.stroke}" />
  </g>
  <g font-family="Arial, Helvetica, sans-serif" text-anchor="middle">
    <text x="{label_x}" y="{label_y}" font-size="36" fill="{colors.label}" font-weight="700">{variant.upper()} PRISMATIC CELL</text>
    <text x="{label_x}" y="{label_y + 40}" font-size="22" fill="{colors.label}">500mm x 100mm x 20mm</text>
    <text x="{label_x}" y="{label_y + 72}" font-size="18" fill="{colors.label}">Terminals on left/right sides</text>
  </g>
</svg>
"""


def write_variant(variant: str, colors: Colors) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    svg_path = OUTPUT_DIR / f"prismatic-cell-{variant}.svg"
    svg_path.write_text(build_svg(variant, colors), encoding="utf-8")
    return svg_path


def main() -> None:
    for variant, colors in VARIANTS.items():
        svg_path = write_variant(variant, colors)
        print(f"Wrote {svg_path.relative_to(Path.cwd())}")


if __name__ == "__main__":
    main()
