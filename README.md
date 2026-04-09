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
![demo](https://github.com/user-attachments/assets/74cf9ec8-6a9c-476f-9a1f-a26889d164a3)

②テキストの読み込み
![demo](https://github.com/user-attachments/assets/f9d8cf41-08f5-46d1-ae49-d13dfd8d6c8f)

③AIが分析中…
![demo](https://github.com/user-attachments/assets/e156934f-f797-42ff-b58a-156ef606e726)

④要約と分析結果
![demo](https://github.com/user-attachments/assets/dbeea1a6-403e-4b3c-a994-3ef629ffa7b7)
