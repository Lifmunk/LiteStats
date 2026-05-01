# LiteStats

A minimal, fast, and clean way to display your GitHub stats directly in your README.

Built with Python + FastAPI, LiteStats generates dynamic SVGs that stay lightweight while still looking good.

Inspired by [github-readme-stats](https://github.com/anuraghazra/github-readme-stats), but focused on simplicity and performance.

🌐 **Live Demo:** https://lite-stats.vercel.app/

---

## ✨ Features

- Minimal SVG design — no unnecessary clutter  
- Fast & lightweight — powered by FastAPI + async requests  
- Theme support — dark, light, and custom colors  
- Two views — overall stats + top languages  
- Easy deploy — works seamlessly with Vercel  
- GraphQL-based — efficient GitHub data fetching  

---

## 🚀 Quick Start (Using Hosted Version)

You can start using LiteStats immediately — no setup required.

Add this to your `README.md`:

```markdown
![GitHub Stats](https://lite-stats.vercel.app/?username=yourusername)
```

---

## ⚙️ Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `username` | string | required | Your GitHub username |
| `type` | string | `stats` | `stats` or `languages` |
| `theme` | string | `dark` | `dark` or `light` |
| `chart` | string | `compact` | `compact` or `bar` (languages only) |
| `transparent` | bool | `false` | Transparent background |
| `bg_color` | string | theme default | Background color (hex, no `#`) |
| `text_color` | string | theme default | Text color (hex, no `#`) |
| `title_color` | string | theme default | Title color (hex, no `#`) |
| `hide` | string | `""` | Comma-separated stats to hide |

---

## 📌 Examples

### Default stats
```
https://lite-stats.vercel.app/?username=yourusername
```

### Light theme
```
https://lite-stats.vercel.app/?username=yourusername&theme=light
```

### Top languages
```
https://lite-stats.vercel.app/?username=yourusername&type=languages
```

### Bar chart (languages)
```
https://lite-stats.vercel.app/?username=yourusername&type=languages&chart=bar
```

### Custom colors
```
https://lite-stats.vercel.app/?username=yourusername&bg_color=0d1117&text_color=c9d1d9&title_color=58a6ff
```

### Transparent background
```
https://lite-stats.vercel.app/?username=yourusername&transparent=true
```

### Hide stats
```
https://lite-stats.vercel.app/?username=yourusername&hide=stars,issues
```

---

## 🎨 Themes

### Dark (default)
- Background: `#0d1117`
- Text: `#c9d1d9`
- Title: `#58a6ff`
- Query param: `?theme=dark`

### Light
- Background: `#ffffff`
- Text: `#24292f`
- Title: `#0969da`
- Query param: `?theme=light`

---

## 🧑‍💻 Deploy Your Own (Vercel)

If you want your own instance (recommended for better rate limits and control):

1. Fork this repository
2. Go to https://vercel.com
3. Click **New Project** → Import your fork
4. Add environment variable:
   ```
   GITHUB_TOKEN=your_github_token
   ```
5. Click **Deploy**

After deployment, you'll get a URL like:
```
https://your-project.vercel.app
```

---

## 🔗 Using Your Own Deployment

Replace the base URL with your deployed domain:

```markdown
![GitHub Stats](https://your-project.vercel.app/?username=yourusername)
```

Example:
```
https://your-project.vercel.app/?username=yourusername&type=languages&theme=light
```

---

## 🧪 Local Development

### Prerequisites
- Python 3.x
- GitHub Personal Access Token

### Setup
```bash
git clone https://github.com/yourusername/Lite-stats.git
cd Lite-stats
pip install -r requirements.txt
export GITHUB_TOKEN="your_github_token"
python api/index.py
```

Server will run at:
```
http://localhost:8000
```

---

## 🧾 Stats Included

### Stats View
- Total Stars
- Total Commits
- Pull Requests
- Issues
- Repositories Contributed To
- Total Repositories

### Languages View
- Top programming languages
- Percentage distribution
- Compact or bar chart view

---

## 🧱 Project Structure

```
Lite-stats/
├── api/
│   └── index.py
├── tests/
│   └── test_svg.py
├── templates/
├── requirements.txt
├── vercel.json
└── LICENSE
```

---

## 🧪 Running Tests

```bash
pytest tests/
```

---

## 📄 License

MIT License — see LICENSE
