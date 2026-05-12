#!/usr/bin/env python3
"""Wiki/*.md → docs/posts/*.html 변환 스크립트
새 글 추가 후: python3 build.py && git add . && git commit -m '글 업데이트' && git push
"""
import re, json
from pathlib import Path

WIKI_DIR  = Path('Obsidian/Wiki')
POSTS_DIR = Path('docs/posts')
DOCS_DIR  = Path('docs')

POST_HTML = '''\
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | 지식 블로그</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../style.css">
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
</head>
<body>
<nav>
  <a href="../index.html" class="brand">지식 블로그</a>
  <div class="links">
    <a href="../index.html">홈</a>
    <a href="../about.html">About</a>
  </div>
</nav>
<div class="container">
  <a href="../index.html" class="back">← 목록으로</a>
  <div class="post-content">
    <h1>{title}</h1>
    <div class="post-meta">{date}</div>
    <div class="post-body" id="post-body"></div>
  </div>
</div>
<footer>© 2026 지식 블로그</footer>
<script>
  document.getElementById('post-body').innerHTML = marked.parse({body_json});
</script>
</body>
</html>'''

def parse_frontmatter(text):
    m = re.match(r'^---\r?\n(.*?)\r?\n---\r?\n(.*)', text, re.DOTALL)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).split('\n'):
        if ':' in line:
            k, *v = line.split(':')
            meta[k.strip()] = ':'.join(v).strip()
    return meta, m.group(2)

POSTS_DIR.mkdir(parents=True, exist_ok=True)
posts = []

for md_file in sorted(WIKI_DIR.glob('*.md')):
    text  = md_file.read_text(encoding='utf-8')
    meta, body = parse_frontmatter(text)
    slug    = md_file.stem
    title   = meta.get('title', slug)
    date    = meta.get('date', '')
    excerpt = next((l.strip() for l in body.split('\n') if l.strip() and not l.startswith('#')), '')[:100]

    posts.append({'slug': slug, 'title': title, 'date': date, 'excerpt': excerpt})

    html = POST_HTML.format(title=title, date=date, body_json=json.dumps(body))
    (POSTS_DIR / f'{slug}.html').write_text(html, encoding='utf-8')
    print(f'  ✓ {slug}.html')

(DOCS_DIR / 'posts.json').write_text(
    json.dumps(posts, ensure_ascii=False, indent=2), encoding='utf-8')

print(f'\n완료: {len(posts)}개 글 → docs/posts/ + docs/posts.json')
