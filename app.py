import streamlit as st
import google.generativeai as genai
from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime

# --- 設定頁面 ---
st.set_page_config(page_title="藥局文案神器Pro", page_icon="💊")
st.title("💊 藥局文案神器 Pro (自動存檔版)")

# --- 1. 處理 API Key (Gemini) ---
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Gemini API Key", type="password")

# --- 2. 處理 Google Docs 存檔函數 ---
# --- 修改後的存檔函式 (直接在目標資料夾建立) ---
def save_to_google_doc(title, content):
    try:
        # 1. 檢查憑證
        if "gcp_service_account" not in st.secrets:
            return "❌ 尚未設定 Google 憑證"
            
        creds = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']
        )
        
        # 建立服務
        docs_service = build('docs', 'v1', credentials=creds)
        drive_service = build('drive', 'v3', credentials=creds)
        folder_id = st.secrets["TARGET_FOLDER_ID"]

        # 2. 直接在「目標資料夾」內建立檔案 (這是改良的關鍵)
        file_metadata = {
            'name': f"{datetime.date.today()} - {title}",
            'mimeType': 'application/vnd.google-apps.document',
            'parents': [folder_id] # 直接指定父母是誰
        }
        
        # 使用 Drive API 建立檔案
        file = drive_service.files().create(body=file_metadata, fields='id').execute()
        doc_id = file.get('id')

        # 3. 寫入內容 (使用 Docs API)
        requests = [
            {'insertText': {'location': {'index': 1}, 'text': content}},
        ]
        docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()

        return f"✅ 成功！已直接存入資料夾，檔名：{file_metadata['name']}"

    except Exception as e:
        return f"⚠️ 存檔失敗: {str(e)}"

# --- 3. 介面輸入 ---
col1, col2 = st.columns(2)
with col1:
    topic = st.text_input("💡 主題", placeholder="例如：春節腸胃保養")
with col2:
    product = st.text_input("🛍️ 產品/成分", placeholder="例如：益生菌")
    
content_points = st.text_area("📝 重點內容", height=100)
tone = st.select_slider("🎨 語氣", options=["專業", "親切", "幽默"], value="親切")

# --- 4. 生成與存檔邏輯 ---
if st.button("✨ 生成並自動存檔"):
    if not api_key:
        st.error("缺 API Key")
    elif not topic:
        st.warning("請輸入主題")
    else:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
        你是一位台灣藥師。請撰寫一篇社群貼文。
        主題：{topic}
        重點：{content_points}
        產品：{product}
        語氣：{tone}
        規則：符合法規、無療效宣稱、親切、結構清晰。
        """
        
        with st.spinner("AI 寫作中..."):
            response = model.generate_content(prompt)
            final_text = response.text
            
            st.markdown("---")
            st.markdown(final_text) # 顯示在網頁上
            
            # 自動存檔
            with st.spinner("正在上傳 Google Drive..."):
                save_status = save_to_google_doc(topic, final_text)
                if "✅" in save_status:
                    st.success(save_status)
                else:
                    st.error(save_status)
