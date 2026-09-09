#!/usr/bin/env python3
"""KB spec_data.json → 監造web/spec_data.js，並以內容雜湊蓋章到 index.html 的 script src。

為什麼要蓋章：index.html 與 spec_data.js 是兩個獨立檔案，瀏覽器/CDN 各自快取。
2026-09-09 實際踩到——使用者拿到新版 index.html 配舊版 spec_data.js，
「分項工程範本」鍵不存在，畫面只畫出表頭沒有任何列且不報錯。
把雜湊寫進 src 後，資料一變 URL 就變，舊快取不可能被命中。
"""
import hashlib, json, pathlib, re, sys

BASE = pathlib.Path(__file__).resolve().parent
SRC  = BASE.parent / "施工規範Obsidian" / "99_資料治理" / "spec_data.json"
JS   = BASE / "spec_data.js"
HTML = BASE / "index.html"

raw = SRC.read_text(encoding="utf-8")
JS.write_text("window.SPEC_DATA=" + raw + ";\n", encoding="utf-8")

h = hashlib.sha256(JS.read_bytes()).hexdigest()[:12]
html = HTML.read_text(encoding="utf-8")
new, n = re.subn(r'<script src="spec_data\.js(?:\?v=[0-9a-f]+)?"></script>',
                 f'<script src="spec_data.js?v={h}"></script>', html, count=1)
if n != 1:
    sys.exit("❌ 找不到 spec_data.js 的 script 標籤，未蓋章")
HTML.write_text(new, encoding="utf-8")

d = json.loads(raw)
c = d["meta"]["counts"]
print(f"✅ spec_data.js {JS.stat().st_size:,} bytes｜?v={h}")
print(f"   工項 {c['工項']}｜試驗庫 {c['試驗庫']}｜分項工程範本 {c.get('分項工程範本','—')}｜{d['meta']['generated']}")
