# 自動テスト

Python + Playwright + Chromiumがある開発環境用です。スマホで実行する必要はありません。

```
python tests/test_final.py
python tests/test_extras.py
```

Chromiumのパスは環境に合わせて変更してください（この検証環境では /usr/bin/chromium）。
ネットワークを遮断し、YouTubeを模擬したプレーヤーでテストします。実音・実機の試験とは異なります。
`qa_results.json` が今回の実行結果です。
