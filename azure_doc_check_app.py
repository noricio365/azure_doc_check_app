import os
import json
from io import BytesIO

import streamlit as st
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from openai import AzureOpenAI

load_dotenv()

# ===== Azure settings =====
DOC_INTEL_ENDPOINT = os.getenv("DOCUMENTINTELLIGENCE_ENDPOINT")
DOC_INTEL_KEY = os.getenv("DOCUMENTINTELLIGENCE_KEY")

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21")

# ===== Clients =====
doc_client = DocumentIntelligenceClient(
    endpoint=DOC_INTEL_ENDPOINT,
    credential=AzureKeyCredential(DOC_INTEL_KEY)
)

aoai_client = AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION
)

st.set_page_config(page_title="Document Check Assistant", layout="wide")
st.title("📄 Document Check Assistant")
st.caption("Azure AI Document Intelligence + Azure OpenAI")

uploaded_file = st.file_uploader(
    "PDFまたは画像ファイルをアップロード",
    type=["pdf", "png", "jpg", "jpeg", "bmp", "tiff"]
)

def extract_text_from_document(file_bytes: bytes) -> str:
    poller = doc_client.begin_analyze_document(
        model_id="prebuilt-layout",
        body=BytesIO(file_bytes),
        content_type="application/octet-stream"
    )
    result = poller.result()

    lines = []
    if result.paragraphs:
        for p in result.paragraphs:
            if p.content:
                lines.append(p.content)

    # paragraphsが取れない場合の保険
    if not lines and result.pages:
        for page in result.pages:
            if page.lines:
                for line in page.lines:
                    lines.append(line.content)

    return "\n".join(lines).strip()

def analyze_with_openai(text: str) -> dict:
    prompt = f"""
あなたは業務文書チェック支援アシスタントです。
以下の文書テキストを読み、次のJSON形式だけで返してください。
必ず日本語で回答してください。

{{
  "summary": "3行以内の要約",
  "important_points": ["重要ポイント1", "重要ポイント2", "重要ポイント3"],
  "risks": ["注意点1", "注意点2"],
  "unknowns": ["不明点1", "不明点2"],
  "check_items": ["確認事項1", "確認事項2", "確認事項3"]
}}

文書テキスト:
\"\"\"
{text[:15000]}
\"\"\"
"""

    response = aoai_client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        messages=[
            {"role": "system", "content": "必ず有効なJSONのみを返してください。説明文、前置き、コードブロックは禁止です。必ず日本語で回答してください。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content
    print("AI raw output:", repr(content))

    content = (content or "").strip()
    content = content.replace("```json", "").replace("```", "").strip()

    if not content:
        return {
            "summary": "AIから結果を取得できませんでした。",
            "important_points": [],
            "risks": [],
            "unknowns": [],
            "check_items": []
        }

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "summary": "JSON変換に失敗しました。",
            "important_points": [],
            "risks": [content],
            "unknowns": [],
            "check_items": []
        }

if uploaded_file:
    file_bytes = uploaded_file.read()

    with st.spinner("文書を解析中..."):
        extracted_text = extract_text_from_document(file_bytes)

    st.subheader("抽出テキスト（プレビュー）")
    st.text_area("OCR / 解析結果", extracted_text, height=250)

    if extracted_text:
        with st.spinner("要点と注意点を整理中..."):
            result = analyze_with_openai(extracted_text)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("要約")
            st.write(result.get("summary", ""))

            st.subheader("重要ポイント")
            for item in result.get("important_points", []):
                st.markdown(f"- {item}")

            st.subheader("注意点")
            for item in result.get("risks", []):
                st.markdown(f"- {item}")

        with col2:
            st.subheader("不明点")
            for item in result.get("unknowns", []):
                st.markdown(f"- {item}")

            st.subheader("確認した方がよい事項")
            for item in result.get("check_items", []):
                st.markdown(f"- {item}")

        st.markdown("---")
        st.caption("※この結果は参考情報です。最終的な判断は専門家にご相談ください。")