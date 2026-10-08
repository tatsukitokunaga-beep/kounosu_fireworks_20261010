# v52 QA — 真の最下部修正

## 構造変更
v51までは花火ギャラリーが `.app > main` の末尾にありました。
v52ではギャラリーを `.app` の外へ移し、body直下の最終通常フロー要素に変更しています。

DOM概略:

body
├─ fixed背景
├─ .app
│  ├─ main（通常コンテンツ）
│  └─ .bottomnav（fixed）
├─ #fireworkShowcase ← 最後に高さを持つ要素
├─ #celebration（fixed）
├─ #toast（fixed）
├─ scripts（display:none）
└─ #eventLockPop（fixed）

## スクロール終端
- documentの通常フローは `#fireworkShowcase` の下端で終了
- 花火より後ろのUIは fixed
- iOSのelastic overscroll中に gallery mode をOFFにしない
- 下端でさらに下方向へドラッグした場合は touchmove を preventDefault
- overshootした scrollY は requestAnimationFrame で花火下端へclamp

## 狙い
ブラウザのスクロールバーが示す文書終端と、花火ギャラリーの下端を同じ位置にすること。
