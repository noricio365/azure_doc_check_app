# Azure Doc Check App

## 概要
契約書や規約文書を読み込み、OCRとAIを用いて要約や注意点を抽出するアプリです。

## 使用技術
- Python
- Streamlit
- Azure Document Intelligence
- Azure OpenAI

## 機能
- 文書読み込み
- OCRによるテキスト抽出
- 要約
- 注意点抽出

## 実行方法
1. ライブラリをインストール
pip install -r requirements.txt
2. .envファイルを作成し、Azureキーを設定
3. アプリ起動
streamlit run azure_doc_check_app.py

## デモ
①ドキュメントをアップ
![demo](images/step1.png)

②テキストの読み込み
![demo](images/step2.png)

③AIが分析中…
![demo](images/step3.png)

④要約と分析結果
![demo](images/step4.png)