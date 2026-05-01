# LiteStats

A minimal, lightweight tool for displaying GitHub statistics on your profile README. Built with Python and FastAPI, it generates dynamic SVG images showing your GitHub stats.

Inspired by [github-readme-stats](https://github.com/anuraghazra/github-readme-stats).

## Features

- **Minimal Design** — Clean SVG output without the bloat
- **Fast & Light** — Python + FastAPI for high performance
- **Theme Support** — Dark and light themes with custom colors
- **Two Views** — Stats overview and language breakdown
- **Easy Deployment** — One-click deploy to Vercel
- **GraphQL Powered** — Efficient data fetching from GitHub

## Quick Start

Add this to your `README.md`:

```markdown
![GitHub Stats](https://your-domain.vercel.app/?username=yourusername)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `username` | string | *required* | GitHub username |
| `type` | string | `stats` | `stats` or `languages` |
| `theme` | string | `dark` | `dark` or `light` |
| `chart` | string | `compact` | `compact` or `bar` (for languages) |
| `transparent` | bool | `false` | Transparent background |
| `bg_color` | string | theme default | Custom background color (hex, no `#`) |
| `text_color` | string | theme default | Custom text color (hex, no `#`) |
| `title_color` | string | theme default | Custom title color (hex, no `#`) |
| `hide` | string | `""` | Comma-separated stats to hide |

## Usage Examples

**Stats view (dark theme):**
```
https://your-domain.vercel.app/?username=yourusername
```

**Stats view (light theme):**
```
https://your-domain.vercel.app/?username=yourusername&theme=light
```

**Top languages (compact chart):**
```
https://your-domain.vercel.app/?username=yourusername&type=languages
```

**Top languages (bar chart):**
```
https://your-domain.vercel.app/?username=yourusername&type=languages&chart=bar
```

**Custom colors:**
```
https://your-domain.vercel.app/?username=yourusername&bg_color=0d1117&text_color=c9d1d9&title_color=58a6ff
```

**Transparent background:**
```
https://your-domain.vercel.app/?username=yourusername&transparent=true
```

**Hide specific stats:**
```
https://your-domain.vercel.app/?username=yourusername&hide=stars,issues
```

## Themes

### Dark (Default)
- Background: `#0d1117`
- Text: `#c9d1d9`
- Title: `#58a6ff`

`?theme=dark`

### Light
- Background: `#ffffff`
- Text: `#24292f`
- Title: `#0969da`

`?theme=light`

## Local Development

**Prerequisites:** Python 3.x, GitHub Personal Access Token

```bash
# Clone the repository
git clone https://github.com/yourusername/Lite-stats.git
cd Lite-stats

# Install dependencies
pip install -r requirements.txt

# Set your GitHub token
export GITHUB_TOKEN="your_github_token"

# Run the server
python api/index.py
```

Server starts at `http://localhost:8000`

## Deploy to Vercel

1. Fork this repository
2. Go to [Vercel](https://vercel.com/) and create a new project
3. Import your forked repository
4. Add environment variable: `GITHUB_TOKEN` = your GitHub PAT
5. Click **Deploy**

Vercel will provide a domain — use it in your README as shown in [Quick Start](#quick-start).

## Tech Stack

- **Python 3.x**
- **FastAPI** — Web framework
- **Uvicorn** — ASGI server
- **httpx** — Async HTTP client
- **Vercel** — Serverless deployment

## Project Structure

```
Lite-stats/
├── api/
│   └── index.py          # Main application & API endpoints
├── tests/
│   └── test_svg.py       # Unit tests
├── templates/            # Reserved for future use
├── requirements.txt      # Python dependencies
├── vercel.json          # Vercel configuration
└── LICENSE              # MIT License
```

## Stats Shown

The stats view displays:
- Total Stars
- Total Commits
- Pull Requests
- Issues
- Repositories Contributed To
- Total Repositories

The languages view shows your top programming languages with percentage breakdowns.

## Running Tests

```bash
pytest tests/
```

## License

MIT License — see [LICENSE](LICENSE) for details.
