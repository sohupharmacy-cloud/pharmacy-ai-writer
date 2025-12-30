import streamlit as st
import google.generativeai as genai
import sys

st.title("👨‍⚕️ 藥師文案產生器 - 診斷模式")

# 1. 檢查工具版本
try:
    version = genai.__version__
except:
    version = "無法讀取版本"
st.write(f"目前 AI 工具版本: `{version}` (建議至少要 0.7.0 以上)")

# 2. 輸入 API Key
api_key = st.sidebar.text_input("請輸入 API Key", type="password")

if st.button("🔍 開始診斷"):
    if not api_key:
        st.error("請先輸入 API Key！")
    else:
        genai.configure(api_key=api_key)
        st.info("正在詢問 Google 大腦有哪些模型可用...")
        
        try:
            # 嘗試列出所有模型
            available_models = []
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    available_models.append(m.name)
            
            if available_models:
                st.success(f"🎉 連線成功！你的 API Key 可以使用以下 {len(available_models)} 個模型：")
                st.code("\n".join(available_models))
                st.markdown("### 👉 接下來怎麼做？")
                st.markdown("請把上面顯示的清單中，看起來像 `models/gemini-1.5-flash` 或 `models/gemini-pro` 的名字複製起來，告訴我你看到了什麼！")
            else:
                st.warning("連線成功，但沒有找到任何可用模型。這可能跟 API Key 的權限有關。")
                
        except Exception as e:
            st.error("❌ 連線失敗！診斷出的錯誤如下：")
            st.code(e)
            st.markdown("如果出現 `400` 或 `API_KEY_INVALID`，代表金鑰可能複製錯了，或是該 Google 帳號需要驗證。")
