// 本機預覽用靜態伺服器（純內建模組，免安裝）
//   node _serve.js        → http://localhost:8770
//   PORT=9000 node _serve.js
// 註：等同 `python3 -m http.server`，但固定以本檔所在目錄為根，
//     避免 python 版本在部分環境對 --directory 取 cwd 失敗。
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = __dirname;
const PORT = process.env.PORT || 8770;
const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.js':   'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.css':  'text/css; charset=utf-8',
  '.xls':  'application/vnd.ms-excel',
  '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
};
http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split('?')[0]);
  if (p === '/') p = '/index.html';
  const f = path.join(ROOT, p);
  if (!f.startsWith(ROOT)) { res.writeHead(403); return res.end('forbidden'); }
  fs.readFile(f, (e, d) => {
    if (e) { res.writeHead(404); return res.end('not found'); }
    res.writeHead(200, { 'Content-Type': MIME[path.extname(f)] || 'application/octet-stream' });
    res.end(d);
  });
}).listen(PORT, () => console.log(`spec-web on http://localhost:${PORT}`));
