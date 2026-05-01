# 📊 LiteStats: Minimal GitHub Stats for your Profile

LiteStats is a modern, lightweight, and minimal tool to display your GitHub statistics on your profile README. Built with Python and FastAPI, it focuses on simplicity and speed, providing exactly what you need without any bloat.

Inspired by the amazing [github-readme-stats](https://github.com/anuraghazra/github-readme-stats).

## ✨ Features

- **Minimalistic Design**: Clean and modern SVG output.
- **Fast & Light**: Built with Python and FastAPI for high performance.
- **Theme Support**: Simple Dark and Light themes.
- **Easy Deployment**: One-click deployment to Vercel.
- **GraphQL Powered**: Efficiently fetches data using GitHub's GraphQL API.

## 🚀 Quick Start

To use LiteStats on your profile, simply add the following to your `README.md`:

```markdown
![GitHub Stats](https://your-vercel-domain.vercel.app/?username=yourusername&theme=dark)
```

### Parameters

- `username`: Your GitHub username (Required)
- `theme`: `dark` (default) or `light`

## 🛠️ How to Host & Setup

### 1. Create a GitHub Personal Access Token (PAT)

You need a token to fetch your stats from GitHub's API.

1. Go to [GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)](https://github.com/settings/tokens).
2. Click **Generate new token**.
3. Select the `repo` and `user` scopes (or just `public_repo` if you only care about public stats).
4. Copy the generated token. **Keep it safe!**

### 2. Deploy to Vercel

1. Fork this repository.
2. Go to [Vercel](https://vercel.com/) and create a new project.
3. Import your forked repository.
4. In the **Environment Variables** section, add:
   - `GITHUB_TOKEN`: Paste your Personal Access Token here.
5. Click **Deploy**.

Once deployed, Vercel will give you a domain. Use that domain in your README link as shown in the [Quick Start](#-quick-start) section.

## 🎨 Themes

### Dark Theme (Default)
`?theme=dark`

### Light Theme
`?theme=light`

## 🤝 Inspiration

This project was inspired by [anuraghazra/github-readme-stats](https://github.com/anuraghazra/github-readme-stats). While that project is amazing and feature-rich, LiteStats aims to provide a simpler, Python-based alternative for those who want a more minimal approach.

## 📄 License

MIT License. See `LICENSE` for more details.
