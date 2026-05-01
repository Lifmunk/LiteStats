import sys
import os
from unittest.mock import MagicMock

# Mock fastapi, httpx and dotenv before importing from api.index
mock_fastapi = MagicMock()
sys.modules["fastapi"] = mock_fastapi
sys.modules["fastapi.responses"] = MagicMock()
sys.modules["httpx"] = MagicMock()
sys.modules["dotenv"] = MagicMock()

# Add the project root to sys.path to import from api
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.index import generate_stats_svg, generate_languages_svg, get_colors

def test_stats_svg():
    stats = {
        "name": "Test User",
        "login": "testuser",
        "stars": 100,
        "commits": 500,
        "prs": 50,
        "issues": 20,
        "contributed_to": 10,
        "total_repos": 15
    }
    c = get_colors("dark", None, None, None)
    svg = generate_stats_svg(stats, c, False, [])
    assert "Test User's GitHub Stats" in svg
    assert "Total Stars: <tspan class=\"bold\">100</tspan>" in svg
    print("test_stats_svg passed")

def test_languages_svg_compact():
    languages = [
        {"name": "Python", "color": "#3572A5", "percent": 60.5},
        {"name": "JavaScript", "color": "#f1e05a", "percent": 30.0},
        {"name": "HTML", "color": "#e34c26", "percent": 9.5}
    ]
    c = get_colors("dark", None, None, None)
    svg = generate_languages_svg("Test User", languages, c, False, "compact")
    assert "Test User's Top Languages" in svg
    assert "Python 60.5%" in svg
    assert "fill=\"#3572A5\"" in svg
    print("test_languages_svg_compact passed")

def test_languages_svg_bar():
    languages = [
        {"name": "Python", "color": "#3572A5", "percent": 60.5},
        {"name": "JavaScript", "color": "#f1e05a", "percent": 30.0}
    ]
    c = get_colors("light", "ff0000", "00ff00", "0000ff")
    svg = generate_languages_svg("Test User", languages, c, True, "bar")
    try:
        assert 'fill="none"' in svg  # transparent
        assert 'fill: #0000ff' in svg # header color (in CSS)
        assert "Python" in svg
        assert "60.5%" in svg
        print("test_languages_svg_bar passed")
    except AssertionError as e:
        print("test_languages_svg_bar failed")
        print(f"SVG Output snippet: {svg[:500]}")
        raise e

if __name__ == "__main__":
    try:
        test_stats_svg()
        test_languages_svg_compact()
        test_languages_svg_bar()
        print("All tests passed!")
    except AssertionError as e:
        print(f"Test failed: {e}")
        sys.exit(1)
