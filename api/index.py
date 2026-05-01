from fastapi import FastAPI, Response, Query
from fastapi.responses import HTMLResponse
import httpx
import os
from typing import Optional, List, Dict
from dotenv import load_dotenv

load_dotenv()

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
                languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
                  edges {
                    size
                    node {
                      name
                      color
                    }
                  }
                }
              }
            }
          }
        }
        """,
        "variables": {"login": username}
    }

def get_colors(theme: str, bg_color: Optional[str], text_color: Optional[str], title_color: Optional[str]):
    themes = {
        "dark": {
            "bg": "#0d1117",
            "text": "#c9d1d9",
            "header": "#58a6ff"
        },
        "light": {
            "bg": "#ffffff",
            "text": "#24292f",
            "header": "#0969da"
        }
    }
    c = themes.get(theme, themes["dark"]).copy()
    if bg_color: c["bg"] = f"#{bg_color}" if not bg_color.startswith("#") else bg_color
    if text_color: c["text"] = f"#{text_color}" if not text_color.startswith("#") else text_color
    if title_color: c["header"] = f"#{title_color}" if not title_color.startswith("#") else title_color
    return c

def generate_stats_svg(stats: dict, c: dict, transparent: bool, hide: List[str]):
    bg_attr = 'fill="none"' if transparent else f'fill="{c["bg"]}"'
    stroke_attr = 'stroke="none"' if transparent else 'stroke="#e4e2e2" stroke-opacity="0.2"'
    
    rows = [
        ("stars", f"Total Stars: {stats['stars']}"),
        ("commits", f"Total Commits: {stats['commits']}"),
        ("prs", f"Total PRs: {stats['prs']}"),
        ("issues", f"Total Issues: {stats['issues']}"),
        ("contributed", f"Contributed to: {stats['contributed_to']}"),
        ("repos", f"Total Repos: {stats['total_repos']}")
    ]
    
    visible_rows = [r[1] for r in rows if r[0] not in hide]
    height = 60 + (len(visible_rows) * 25) + 20
    
    stat_items = ""
    for i, text in enumerate(visible_rows):
        label, value = text.split(": ")
        stat_items += f'<text x="0" y="{i*25}" class="stat">{label}: <tspan class="bold">{value}</tspan></text>\n'

    svg = f"""
    <svg width="450" height="{height}" viewBox="0 0 450 {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
        <style>
            .header {{ font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif; fill: {c['header']}; }}
            .stat {{ font: 400 14px 'Segoe UI', Ubuntu, Sans-Serif; fill: {c['text']}; }}
            .bold {{ font-weight: 700; }}
        </style>
        <rect x="0.5" y="0.5" width="449" height="{height-1}" rx="4.5" {bg_attr} {stroke_attr}/>
        
        <text x="25" y="35" class="header">{stats['name'] or stats['login']}'s GitHub Stats</text>
        
        <g transform="translate(25, 65)">
            {stat_items}
        </g>
    </svg>
    """
    return svg

def generate_languages_svg(name: str, languages: List[dict], c: dict, transparent: bool, chart: str):
    bg_attr = 'fill="none"' if transparent else f'fill="{c["bg"]}"'
    stroke_attr = 'stroke="none"' if transparent else 'stroke="#e4e2e2" stroke-opacity="0.2"'
    
    if chart == "compact":
        height = 160
        bar_y = 65
        bar_height = 10
        total_width = 400
        
        bar_segments = ""
        current_x = 0
        legend_items = ""
        
        for i, lang in enumerate(languages[:6]):
            width = (lang['percent'] / 100) * total_width
            bar_segments += f'<rect x="{current_x}" y="0" width="{width}" height="{bar_height}" fill="{lang["color"] or "#8b949e"}" {"rx=\"2\"" if i==0 or i==len(languages[:6])-1 else ""}/>'
            
            row = i // 3
            col = i % 3
            legend_items += f"""
            <g transform="translate({col * 135}, {bar_y + 35 + (row * 25)})">
                <circle cx="5" cy="-5" r="5" fill="{lang["color"] or "#8b949e"}"/>
                <text x="15" y="0" class="stat">{lang['name']} {lang['percent']:.1f}%</text>
            </g>
            """
            current_x += width

        svg = f"""
        <svg width="450" height="{height}" viewBox="0 0 450 {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
            <style>
                .header {{ font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif; fill: {c['header']}; }}
                .stat {{ font: 400 14px 'Segoe UI', Ubuntu, Sans-Serif; fill: {c['text']}; }}
            </style>
            <rect x="0.5" y="0.5" width="449" height="{height-1}" rx="4.5" {bg_attr} {stroke_attr}/>
            <text x="25" y="35" class="header">{name}'s Top Languages</text>
            
            <g transform="translate(25, {bar_y})">
                <mask id="bar-mask"><rect width="{total_width}" height="{bar_height}" rx="5"/></mask>
                <g mask="url(#bar-mask)">{bar_segments}</g>
                {legend_items}
            </g>
        </svg>
        """
    else: # bar chart
        height = 60 + (len(languages[:5]) * 40) + 10
        items = ""
        for i, lang in enumerate(languages[:5]):
            y = i * 40
            items += f"""
            <g transform="translate(0, {y})">
                <text x="0" y="0" class="stat">{lang['name']}</text>
                <text x="400" y="0" class="stat" text-anchor="end">{lang['percent']:.1f}%</text>
                <rect x="0" y="8" width="400" height="8" rx="4" fill="{c['text']}" fill-opacity="0.1"/>
                <rect x="0" y="8" width="{lang['percent'] * 4}" height="8" rx="4" fill="{lang['color'] or "#8b949e"}"/>
            </g>
            """
        
        svg = f"""
        <svg width="450" height="{height}" viewBox="0 0 450 {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
            <style>
                .header {{ font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif; fill: {c['header']}; }}
                .stat {{ font: 400 14px 'Segoe UI', Ubuntu, Sans-Serif; fill: {c['text']}; }}
            </style>
            <rect x="0.5" y="0.5" width="449" height="{height-1}" rx="4.5" {bg_attr} {stroke_attr}/>
            <text x="25" y="35" class="header">{name}'s Top Languages</text>
            <g transform="translate(25, 70)">
                {items}
            </g>
        </svg>
        """
    return svg

@app.get("/")
async def get_stats(
    username: str, 
    type: str = "stats",
    theme: str = "dark", 
    transparent: bool = False,
    bg_color: Optional[str] = None,
    text_color: Optional[str] = None,
    title_color: Optional[str] = None,
    hide: str = "",
    chart: str = "compact"
):
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return Response(content="GITHUB_TOKEN not found", status_code=500)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                GITHUB_GRAPHQL_URL,
                json=get_query(username),
                headers={"Authorization": f"bearer {token}"}
            )
            
            if response.status_code != 200:
                return Response(content="Error fetching data from GitHub", status_code=500)
            
            data = response.json()
    except Exception as e:
        return Response(content=f"Request error: {str(e)}", status_code=500)
        
    if "errors" in data:
        return Response(content=data["errors"][0]["message"], status_code=404)
            
    user = data["data"]["user"]
    if not user:
        return Response(content="User not found", status_code=404)

    c = get_colors(theme, bg_color, text_color, title_color)
    hide_list = [h.strip() for h in hide.split(",") if h.strip()]
    
    if type == "languages":
        lang_stats = {}
        for repo in user["repositories"]["nodes"]:
            for edge in repo["languages"]["edges"]:
                name = edge["node"]["name"]
                color = edge["node"]["color"]
                size = edge["size"]
                if name in lang_stats:
                    lang_stats[name]["size"] += size
                else:
                    lang_stats[name] = {"name": name, "color": color, "size": size}
        
        total_size = sum(l["size"] for l in lang_stats.values())
        languages = sorted(lang_stats.values(), key=lambda x: x["size"], reverse=True)
        for l in languages:
            l["percent"] = (l["size"] / total_size * 100) if total_size > 0 else 0
        
        svg_content = generate_languages_svg(user["name"] or user["login"], languages, c, transparent, chart)
    else:
        stats = {
            "name": user["name"],
            "login": user["login"],
            "stars": sum(repo["stargazers"]["totalCount"] for repo in user["repositories"]["nodes"]),
            "commits": user["contributionsCollection"]["totalCommitContributions"] + user["contributionsCollection"]["restrictedContributionsCount"],
            "prs": user["pullRequests"]["totalCount"],
            "issues": user["issues"]["totalCount"],
            "contributed_to": user["repositoriesContributedTo"]["totalCount"],
            "total_repos": user["repositories"]["totalCount"]
        }
        svg_content = generate_stats_svg(stats, c, transparent, hide_list)
        
    return Response(content=svg_content, media_type="image/svg+xml")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
