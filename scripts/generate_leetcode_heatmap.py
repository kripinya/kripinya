"""
LeetCode Contribution Heatmap Generator

Fetches submission calendar data from LeetCode's public GraphQL API
and generates a clean SVG contribution grid (similar to GitHub's green grid).
Uses the portfolio color theme: #0a192f background, #64ffda accent.
"""

import json
import math
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timedelta, timezone

LEETCODE_USERNAME = os.environ.get("LEETCODE_USERNAME", "ananyakarn_kripinya")
OUTPUT_PATH = os.environ.get("OUTPUT_PATH", "assets/leetcode-heatmap.svg")

# Portfolio color theme
BG_COLOR = "#0a192f"
CELL_EMPTY = "#112240"
CELL_LEVEL_1 = "#1a3a4a"
CELL_LEVEL_2 = "#2a6a5a"
CELL_LEVEL_3 = "#3d9b7a"
CELL_LEVEL_4 = "#64ffda"
TEXT_COLOR = "#8892b0"
BORDER_COLOR = "#1e3a5f"

CELL_SIZE = 11
CELL_GAP = 3
CELL_RADIUS = 2
MONTH_LABEL_HEIGHT = 18
DAY_LABEL_WIDTH = 30
PADDING = 16

MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DAY_NAMES = ["Mon", "Wed", "Fri"]


def fetch_submission_calendar(username: str) -> dict:
    """Fetch submission calendar from LeetCode GraphQL API."""
    query = {
        "query": """
            query userProfileCalendar($username: String!) {
                matchedUser(username: $username) {
                    userCalendar {
                        submissionCalendar
                    }
                }
            }
        """,
        "variables": {"username": username}
    }

    data = json.dumps(query).encode("utf-8")
    req = urllib.request.Request(
        "https://leetcode.com/graphql",
        data=data,
        headers={
            "Content-Type": "application/json",
            "Referer": "https://leetcode.com",
            "User-Agent": "Mozilla/5.0 (compatible; LeetCodeHeatmapBot/1.0)"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}", file=sys.stderr)
        return {}
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}", file=sys.stderr)
        return {}

    try:
        calendar_str = result["data"]["matchedUser"]["userCalendar"]["submissionCalendar"]
        return json.loads(calendar_str)
    except (KeyError, TypeError, json.JSONDecodeError) as e:
        print(f"Failed to parse calendar data: {e}", file=sys.stderr)
        return {}


def get_color_for_count(count: int) -> str:
    """Map submission count to a color intensity level."""
    if count == 0:
        return CELL_EMPTY
    elif count <= 1:
        return CELL_LEVEL_1
    elif count <= 3:
        return CELL_LEVEL_2
    elif count <= 6:
        return CELL_LEVEL_3
    else:
        return CELL_LEVEL_4


def generate_heatmap_svg(calendar: dict) -> str:
    """Generate an SVG contribution grid from the submission calendar."""
    today = datetime.now(timezone.utc).date()
    # Show ~52 weeks (364 days) ending today
    num_weeks = 53
    total_days = num_weeks * 7

    # Find the Sunday that starts our grid
    # weekday(): Monday=0, Sunday=6
    days_since_sunday = (today.weekday() + 1) % 7
    end_date = today
    start_date = end_date - timedelta(days=total_days - 1)
    # Align start_date to a Sunday
    start_weekday = (start_date.weekday() + 1) % 7  # 0=Sunday
    if start_weekday != 0:
        start_date = start_date - timedelta(days=start_weekday)

    # Recalculate total days after alignment
    total_days = (end_date - start_date).days + 1
    num_weeks = math.ceil(total_days / 7)

    # Build the day-by-day data
    grid_data = []
    for i in range(total_days):
        day = start_date + timedelta(days=i)
        timestamp = str(int(datetime(day.year, day.month, day.day).timestamp()))
        count = calendar.get(timestamp, 0)
        grid_data.append({
            "date": day,
            "count": count,
            "col": i // 7,
            "row": i % 7
        })

    # Calculate SVG dimensions
    grid_width = num_weeks * (CELL_SIZE + CELL_GAP)
    svg_width = DAY_LABEL_WIDTH + grid_width + PADDING * 2
    svg_height = MONTH_LABEL_HEIGHT + 7 * (CELL_SIZE + CELL_GAP) + PADDING * 2 + 40  # extra for legend

    # Compute total submissions in the displayed period
    total_submissions = sum(d["count"] for d in grid_data)

    # Start building SVG
    svg_parts = []
    svg_parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" '
        f'viewBox="0 0 {svg_width} {svg_height}">'
    )

    # Background
    svg_parts.append(
        f'<rect width="{svg_width}" height="{svg_height}" rx="8" ry="8" '
        f'fill="{BG_COLOR}" stroke="{BORDER_COLOR}" stroke-width="1"/>'
    )

    # Style
    svg_parts.append(
        f'<style>'
        f'  text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; }}'
        f'  .month-label {{ font-size: 10px; fill: {TEXT_COLOR}; }}'
        f'  .day-label {{ font-size: 10px; fill: {TEXT_COLOR}; }}'
        f'  .legend-label {{ font-size: 10px; fill: {TEXT_COLOR}; }}'
        f'  .title-label {{ font-size: 11px; fill: {TEXT_COLOR}; font-weight: 600; }}'
        f'  .cell {{ stroke: {BG_COLOR}; stroke-width: 1; }}'
        f'</style>'
    )

    offset_x = PADDING + DAY_LABEL_WIDTH
    offset_y = PADDING + MONTH_LABEL_HEIGHT

    # Month labels
    current_month = -1
    for d in grid_data:
        if d["row"] == 0 and d["date"].month != current_month:
            current_month = d["date"].month
            x = offset_x + d["col"] * (CELL_SIZE + CELL_GAP)
            svg_parts.append(
                f'<text x="{x}" y="{PADDING + 10}" class="month-label">'
                f'{MONTH_NAMES[current_month - 1]}</text>'
            )

    # Day labels (Mon, Wed, Fri)
    for label, row in [("Mon", 1), ("Wed", 3), ("Fri", 5)]:
        y = offset_y + row * (CELL_SIZE + CELL_GAP) + CELL_SIZE - 2
        svg_parts.append(
            f'<text x="{PADDING}" y="{y}" class="day-label">{label}</text>'
        )

    # Grid cells
    for d in grid_data:
        if d["date"] > end_date:
            continue
        x = offset_x + d["col"] * (CELL_SIZE + CELL_GAP)
        y = offset_y + d["row"] * (CELL_SIZE + CELL_GAP)
        color = get_color_for_count(d["count"])
        tooltip = f'{d["date"].strftime("%b %d, %Y")}: {d["count"]} submission{"s" if d["count"] != 1 else ""}'
        svg_parts.append(
            f'<rect x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" '
            f'rx="{CELL_RADIUS}" ry="{CELL_RADIUS}" fill="{color}" class="cell">'
            f'<title>{tooltip}</title></rect>'
        )

    # Legend
    legend_y = offset_y + 7 * (CELL_SIZE + CELL_GAP) + 14
    legend_x_start = svg_width - PADDING - 5 * (CELL_SIZE + CELL_GAP) - 50

    svg_parts.append(
        f'<text x="{PADDING}" y="{legend_y + CELL_SIZE - 2}" class="title-label">'
        f'{total_submissions} submissions in the last year</text>'
    )

    svg_parts.append(
        f'<text x="{legend_x_start - 30}" y="{legend_y + CELL_SIZE - 2}" class="legend-label">Less</text>'
    )

    legend_colors = [CELL_EMPTY, CELL_LEVEL_1, CELL_LEVEL_2, CELL_LEVEL_3, CELL_LEVEL_4]
    for i, color in enumerate(legend_colors):
        x = legend_x_start + i * (CELL_SIZE + CELL_GAP)
        svg_parts.append(
            f'<rect x="{x}" y="{legend_y}" width="{CELL_SIZE}" height="{CELL_SIZE}" '
            f'rx="{CELL_RADIUS}" ry="{CELL_RADIUS}" fill="{color}" class="cell"/>'
        )

    more_x = legend_x_start + 5 * (CELL_SIZE + CELL_GAP) + 4
    svg_parts.append(
        f'<text x="{more_x}" y="{legend_y + CELL_SIZE - 2}" class="legend-label">More</text>'
    )

    svg_parts.append('</svg>')
    return "\n".join(svg_parts)


def main():
    print(f"Fetching LeetCode calendar for: {LEETCODE_USERNAME}")
    calendar = fetch_submission_calendar(LEETCODE_USERNAME)

    if not calendar:
        print("Warning: No calendar data received. Generating empty heatmap.", file=sys.stderr)

    print(f"Found {len(calendar)} days with submissions")

    svg_content = generate_heatmap_svg(calendar)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_PATH) or ".", exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"Heatmap SVG written to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
