from fastapi import FastAPI, Response, Query
from fastapi.responses import HTMLResponse
import httpx
import os
from typing import Optional

app = FastAPI()

GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

def get_query(username: str):
    return {
        "query": """
        query userInfo($login: String!) {
          user(login: $login) {
            name
            login
            contributionsCollection {
              totalCommitContributions
              restrictedContributionsCount
            }
            repositoriesContributedTo(first: 1, contributionTypes: [COMMIT, ISSUE, PULL_REQUEST, REPOSITORY]) {
              totalCount
            }
            pullRequests(first: 1) {
              totalCount
            }
            issues(first: 1) {
              totalCount
            }
            repositories(first: 100, ownerAffiliations: OWNER, orderBy: {direction: DESC, field: STARGAZERS}) {
              totalCount
              nodes {
                stargazers {
                  totalCount
                }
              }
            }
          }
        }
        """,
        "variables": {"login": username}
    }

def generate_svg(stats: dict, theme: str = "dark"):
    colors = {
        "dark": {
            "bg": "#0d1117",
            "text": "#c9d1d9",
            "header": "#58a6ff",
            "icon": "#8b949e"
        },
        "light": {
            "bg": "#ffffff",
            "text": "#24292f",
            "header": "#0969da",
            "icon": "#57606a"
        }
    }
    
    c = colors.get(theme, colors["dark"])
    
    svg = f"""
    <svg width="450" height="190" viewBox="0 0 450 190" fill="none" xmlns="http://www.w3.org/2000/svg">
        <style>
            .header {{ font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif; fill: {c['header']}; }}
            .stat {{ font: 400 14px 'Segoe UI', Ubuntu, Sans-Serif; fill: {c['text']}; }}
            .bold {{ font-weight: 700; }}
        </style>
        <rect x="0.5" y="0.5" width="449" height="189" rx="4.5" fill="{c['bg']}" stroke="#e4e2e2" stroke-opacity="0.2"/>
        
        <text x="25" y="35" class="header">{stats['name'] or stats['login']}'s GitHub Stats</text>
        
        <g transform="translate(25, 60)">
            <text x="0" y="0" class="stat">Total Stars: <tspan class="bold">{stats['stars']}</tspan></text>
            <text x="0" y="25" class="stat">Total Commits: <tspan class="bold">{stats['commits']}</tspan></text>
            <text x="0" y="50" class="stat">Total PRs: <tspan class="bold">{stats['prs']}</tspan></text>
            <text x="0" y="75" class="stat">Total Issues: <tspan class="bold">{stats['issues']}</tspan></text>
            <text x="0" y="100" class="stat">Contributed to: <tspan class="bold">{stats['contributed_to']}</tspan></text>
        </g>
    </svg>
    """
    return svg

@app.get("/")
async def get_stats(username: str, theme: str = "dark"):
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return Response(content="GITHUB_TOKEN not found", status_code=500)

    async with httpx.AsyncClient() as client:
        response = await client.post(
            GITHUB_GRAPHQL_URL,
            json=get_query(username),
            headers={"Authorization": f"bearer {token}"}
        )
        
        if response.status_code != 200:
            return Response(content="Error fetching data from GitHub", status_code=500)
        
        data = response.json()
        if "errors" in data:
            return Response(content=data["errors"][0]["message"], status_code=404)
            
        user = data["data"]["user"]
        
        stats = {
            "name": user["name"],
            "login": user["login"],
            "stars": sum(repo["stargazers"]["totalCount"] for repo in user["repositories"]["nodes"]),
            "commits": user["contributionsCollection"]["totalCommitContributions"] + user["contributionsCollection"]["restrictedContributionsCount"],
            "prs": user["pullRequests"]["totalCount"],
            "issues": user["issues"]["totalCount"],
            "contributed_to": user["repositoriesContributedTo"]["totalCount"]
        }
        
        svg_content = generate_svg(stats, theme)
        return Response(content=svg_content, media_type="image/svg+xml")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
