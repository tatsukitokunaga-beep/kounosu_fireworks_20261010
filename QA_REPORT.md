# v51 最終余白修正 QA

## 原因
v50では最終ギャラリーに `height:100lvh` を強制していました。
iPhone Chrome / SafariではブラウザUIの状態と `lvh` が一致しないことがあり、
解説カードの後ろに「内容のないセクション高さ」が残る可能性がありました。

## v51修正
- `.firework-showcase` の `100lvh / 100vh / 100dvh` 強制固定を最終CSSで完全無効化
- ギャラリーの高さを実コンテンツ量で決定
- 花火空間だけ `clamp(430px, 58svh, 560px)` を確保
- 解説カード直下をセクション終端に変更
- セクション下padding / margin / borderを0
- html / body / main / app の下余白を0
- iPhoneの最下部 rubber-band を touchmove で抑止
- トラックパッド / wheelの下方向overscrollも抑止

## 構造確認
- footerは花火ギャラリーより前
- 花火ギャラリーは main の最後のflow要素
- その後にある下部ナビ・乾杯モーダルは fixed overlayで、通常flowの高さを持たない
