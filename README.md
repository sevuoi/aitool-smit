# 내 블로그

**라이브 URL:** https://sevuoi.github.io/aitool-smit/

## 구조
- `Obsidian/` — 콘텐츠 (Obsidian Vault로 열기)
  - `Raw/` — 생각 그대로 메모
  - `Wiki/` — 정리된 블로그 글 (.md)
  - `Master_Index.md` — 목차 + 기획
- `index.html` — 홈 (포스트 카드 목록)
- `post.html` — 글 상세
- `about.html` — 소개 페이지

## 글 업데이트 방법
`Obsidian/Wiki/` 에서 .md 파일 수정 후:
```
git add . && git commit -m "글 업데이트" && git push
```
