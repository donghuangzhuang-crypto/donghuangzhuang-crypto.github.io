"""Render the two static portfolio pages from the same project index."""
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECTS = json.loads((ROOT / "projects.json").read_text(encoding="utf-8"))
CATEGORIES = {
    "creative": ("内容与视频", "Content & video"),
    "marketing": ("创作者与出海", "Creators & commerce"),
    "research": ("市场与投研", "Market research"),
    "systems": ("学习与个人", "Learning & personal"),
}
STATUSES = {
    "local": ("本机工具", "Local tool"),
    "personal": ("个人工作台", "Personal workspace"),
    "prototype": ("交互原型", "Interactive prototype"),
    "website": ("作品集网站", "Portfolio website"),
}
LINKS = {
    "repo": ("GitHub 仓库", "GitHub repository"),
    "archive": ("早期原型", "Earlier prototype"),
    "upstream": ("上游项目", "Upstream"),
}


def card(project, lang):
    label = escape(project["name"][lang])
    summary = escape(project["summary"][lang])
    tags = "".join(f'<li>{escape(tag)}</li>' for tag in project["tags"])
    links = "".join(
        f'<a href="{escape(project[k], quote=True)}">{wording[lang]} <span aria-hidden="true">↗</span></a>'
        for k, wording in LINKS.items() if k in project
    )
    footer = f'\n      <div class="card-links">{links}</div>' if links else ""
    return f'''<article class="project" id="{project["id"]}" data-category="{project["category"]}">
      <span class="status">{STATUSES[project["status"]][lang]}</span>
      <h3>{label}</h3>
      <p>{summary}</p>
      <ul>{tags}</ul>{footer}
    </article>'''


def render(lang):
    zh = lang == 0
    locale = "zh-CN" if zh else "en"
    name = "东煌 DH" if zh else "Donghuang · DH"
    title = "我是个 AI Builder" if zh else "I’m an AI Builder"
    intro = ("我把内容创作、学习和投研中的重复工作，做成可以反复使用的工具。"
             if zh else "I build reusable tools for content creation, learning, and market research.")
    nav = "项目" if zh else "Projects"
    heading = "项目与工具" if zh else "Projects and tools"
    note = ("本机工具、产品原型和个人工作台。" if zh else "Local tools, product prototypes, and personal workspaces.")
    switch = '<a href="en/index.html" lang="en">English</a>' if zh else '<a href="../index.html" lang="zh-CN">简体中文</a>'
    relative = "./" if zh else "../"
    all_text = "全部" if zh else "All"
    filters = f'<button type="button" data-filter="all" aria-pressed="true">{all_text}</button>'
    filters += "".join(
        f'<button type="button" data-filter="{key}" aria-pressed="false">{words[lang]}</button>'
        for key, words in CATEGORIES.items()
    )
    sections = "\n".join(
        f'''<section class="category" data-group="{key}" aria-labelledby="label-{key}">
      <h2 id="label-{key}">{words[lang]}</h2>
      <div class="project-grid">{"".join(card(p, lang) for p in PROJECTS if p["category"] == key)}</div>
    </section>'''
        for key, words in CATEGORIES.items()
    )
    count = f"{len(PROJECTS)} 个项目" if zh else f"{len(PROJECTS)} projects"
    return f'''<!doctype html>
<html lang="{locale}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(intro, quote=True)}">
  <link rel="alternate" hreflang="{'en' if zh else 'zh-CN'}" href="{'en/index.html' if zh else '../index.html'}">
  <title>{name} · {'个人官网' if zh else 'Portfolio'}</title>
  <link rel="stylesheet" href="{relative}style.css">
  <script src="{relative}filters.js" defer></script>
</head>
<body>
  <header class="header wrap">
    <a class="brand" href="#top">{name}</a>
    <nav aria-label="{'站点导航' if zh else 'Site navigation'}">
      <a href="#projects">{nav}</a>
      <a href="https://github.com/donghuangzhuang-crypto">GitHub <span aria-hidden="true">↗</span></a>
      {switch}
    </nav>
  </header>
  <main id="top" class="wrap">
    <section class="hero" aria-labelledby="intro">
      <h1 id="intro">{title}</h1>
      <p>{intro}</p>
      <a href="#projects" class="primary">{'查看项目' if zh else 'Explore projects'} <span aria-hidden="true">↓</span></a>
    </section>
    <div id="projects" class="directory">
      <div class="directory-heading">
        <div><h2>{heading}</h2><p>{note}</p></div>
        <p class="count" id="project-count" aria-live="polite">{count}</p>
      </div>
      <div class="filters" aria-label="{'筛选项目类别' if zh else 'Filter projects by category'}" hidden>{filters}</div>
      {sections}
    </div>
  </main>
  <footer class="footer wrap"><span>{name}</span><a href="#top">{'返回顶部' if zh else 'Back to top'} <span aria-hidden="true">↑</span></a></footer>
</body>
</html>
'''


if __name__ == "__main__":
    assert len(PROJECTS) == len({project["id"] for project in PROJECTS})
    for project in PROJECTS:
        assert project["category"] in CATEGORIES and project["status"] in STATUSES
    (ROOT / "en").mkdir(exist_ok=True)
    (ROOT / "index.html").write_text(render(0), encoding="utf-8")
    (ROOT / "en/index.html").write_text(render(1), encoding="utf-8")
