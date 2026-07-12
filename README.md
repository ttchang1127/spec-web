# 監造 web（案件級生產工具）

施工規範知識庫的 **client-side 靜態網頁**（方案 A）。案件檔全程在瀏覽器內處理，不上傳。

## 檔案
- `index.html` — v0.3，兩用：**試驗查核**（應辦組數＋漏編）＋**監造計畫產生**（第五/七章草稿，下載 .doc）
- `spec_data.js` — 規則燃料（`window.SPEC_DATA`），由知識庫編譯（含試驗庫、工項停留點、查核紅線、標單別名）

## 更新規則資料（KB 改動後）
```bash
cd "施工規範Obsidian"
python3 99_資料治理/spec_kb_export.py                    # → 99_資料治理/spec_data.json
python3 -c "import json;d=json.load(open('99_資料治理/spec_data.json',encoding='utf-8'));open('../監造web/spec_data.js','w',encoding='utf-8').write('window.SPEC_DATA='+json.dumps(d,ensure_ascii=False)+';')"
```

## 本機執行
```bash
cd 監造web
python3 -m http.server 8731
# 瀏覽器開 http://localhost:8731/index.html
```
（xlsx 上傳需連網載 SheetJS；離線可用「內建範例」或「貼上標單」。）

## 現況（v0.2，已對真實標單實測）
- **主匹配用編碼→章碼**（詳細表「編碼(備註)」前5碼，錨定；別名 fuzzy 為備援）。
- **章碼家族**：03310→03050（結構混凝土）、02336→02331（路基整理）等（工項卡 frontmatter `章碼別名`）。
- **數量→組數**：自動去千分位逗號；體積/面積制算組數，批/車/料源制標註。
- **漏編 diff**：讀資源統計表「材料試驗費」明細（含「試驗」之資源名），以應辦試驗核心詞（壓實度/含油/篩分…）比對 → 已編列（綠）/⚠漏編（紅）。
- 統計：標單章碼／對到工項／未建工項／疑似漏編／編列試驗數；未建章碼併成一張清單（覆蓋缺口）。

> ℹ **範例檔**：`sample.xls`（航空城復原工程空白標單）為**公開招標文件**（政府電子採購網），刻意納入作 demo，供「載入範例標單」按鈕使用。
> ⚠ **未來真實案件**的標單/設計圖仍受 `.gitignore` 保護（`*.xls`/`*.xlsx`/`*.pdf` 預設排除），**勿 commit**。

## 待辦（後續 Phase）
- 漏編/不足 diff（需標單含「材料試驗費」細項比對）。
- 監造計畫 .docx 產生（九章樣板 × 案件資料，docxtemplater）。
- PDF 標單解析（pdf.js）、設計圖輔助。
- 部署 GitHub Pages（比照 bridge_kb）。
