import streamlit as st
import google.generativeai as genai

# 1. 設定頁面
st.set_page_config(page_title="藥師文案產生器 v2026", page_icon="💊")
st.title("💊 藥局社群文案神隊友 (2.5版)")
st.caption("使用最新 Gemini 2.5 AI，輸入主題與重點，幫你生成吸睛文案！")

# 2. 側邊欄輸入 API Key
api_key = st.sidebar.text_input("請輸入你的 Google Gemini API Key", type="password")

# 3. 輸入區
col1, col2 = st.columns(2)
with col1:
    topic = st.text_input("💡 主題", placeholder="例如：過年大吃大喝消化不良")
with col2:
    product = st.text_input("🛍️ 產品/成分", placeholder="例如：益生菌、酵素")

content_points = st.text_area("📝 重點關鍵字", height=150,
                              placeholder="例如：\n1. 脹氣很不舒服\n2. 飯後可以散步\n3. 補充好菌幫助消化")

tone = st.select_slider("🎨 文案語氣", options=["專業嚴肅", "親切像鄰居", "幽默風趣"], value="親切像鄰居")

# 4. 生成按鈕
if st.button("✨ 啟動 2.5 Flash 生成文案！"):
    if not api_key:
        st.error("請在左側輸入 API Key 喔！")
    elif not topic:
        st.warning("請至少輸入主題！")
    else:
        # 設定 API
        genai.configure(api_key=api_key)
        
        # ★★★ 關鍵修改：使用你清單中的 gemini-2.5-flash ★★★
        model = genai.GenerativeModel('gemini-2.5-flash')

        prompt = f"""
        你是一位台灣的專業藥師，經營社區藥局。請撰寫一篇社群貼文。

        【輸入資訊】
        - 主題：{topic}
        - 重點：{content_points}
        - 產品：{product}
        - 語氣：{tone}

        【法規與撰寫規則】
        1. 遵守台灣藥事法，不宣稱療效，僅作營養補給或輔助建議。
        2. 結構：[吸睛標題] -> [情境共鳴] -> [藥師衛教] -> [軟性置入] -> [Take Home Message]。
        3. 多使用 Emoji，分段清晰，適合手機閱讀。
        """

        with st.spinner("Gemini 2.5 正在高速運轉中..."):
            try:
                response = model.generate_content(prompt)
                st.markdown("### 🎉 生成結果：")
                st.markdown("---")
                st.markdown(response.text)
                st.success("成功！這可是用最新模型寫出來的文案喔！")
            except Exception as e:
                st.error(f"發生錯誤：{e}")
