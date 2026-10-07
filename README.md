# こうのす花火大会 2026 — ふたりの花火ナイト

スマホ向けの静的Webアプリです。GitHub Pagesでそのまま公開できます。

## GitHub Pages公開
1. このフォルダの中身をGitHubリポジトリの `main` ブランチ直下へアップロード
2. GitHubの **Settings → Pages** を開く
3. **Source: GitHub Actions** を選択
4. `Actions` の `Deploy GitHub Pages` が完了すると公開URLが発行されます

## MAP仕様
- 初期表示：会場ガイドMAP（HTMLに画像埋め込み済みなので画像パス切れなし）
- 2本指ピンチ：拡大縮小
- 1本指：移動
- ダブルタップ：拡大
- `リアル地図`：Leaflet + OpenStreetMapを読み込み
- `◎`：スマホの位置情報を取得し現在地を表示
- `①`：おすすめ地点へ移動
- `🏮`：会場全体を表示
- `⛶`：全画面表示

位置情報はHTTPSが必要です。GitHub PagesはHTTPSなのでスマホ本番利用に適しています。

## 注意
会場ガイド画像上の位置は案内用の目安です。実際の現在地と徒歩導線は「リアル地図」またはGoogle Maps徒歩ナビを優先してください。
