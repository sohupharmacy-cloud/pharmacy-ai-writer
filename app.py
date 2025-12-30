import streamlit as st
import google.generativeai as genai

# 1. 設定頁面標題與風格
st.set_page_config(page_title="藥師文案產生器", page_icon="💊")
st.title("💊 藥局社群文案神隊友")
st.caption("輸入主題與重點，AI 幫你生成符合法規的吸睛文案！")

# 2. 側邊欄：輸入 API Key (保護你的帳號安全)
api_key = st.sidebar.text_input("請輸入你的 Google Gemini API Key", type="password")

# 3. App 的主要輸入區
col1, col2 = st.columns(2)
with col1:
    topic = st.text_input("💡 這次的主題是？", placeholder="例如：換季過敏、冬季血管保養")
with col2:
    product = st.text_input("🛍️ 想推廣的產品 (或成分)", placeholder="例如：益生菌、魚油 (AI 會幫你軟性置入)")

content_points = st.text_area("📝 請輸入大約內容 / 重點關鍵字", height=150,
                              placeholder="例如：\n1. 早上起床打噴嚏\n2. 溫差大血管收縮\n3. 建議洋蔥式穿法\n4. 多吃抗氧化食物")

tone = st.select_slider("🎨 選擇文案語氣", options=["專業嚴肅", "親切像鄰居", "幽默風趣"], value="親切像鄰居")

# 4. 按鈕觸發 AI 生成
if st.button("✨ 幫我產出文案！"):
    if not api_key:
        st.error("請先在側邊欄輸入 API Key 喔！")
    elif not topic or not content_points:
        st.warning("主題和內容重點不能留白喔～")
    else:
        # 設定 Gemini API
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        # 5. 【核心秘密】給 AI 的指令 (Prompt) - 包含法規防護
        prompt = f"""
        你是一位台灣的專業藥師，經營社區藥局。請幫我撰寫一篇 Facebook/Instagram 社群貼文。

        【輸入資訊】
        - 主題：{topic}
        - 重點內容：{content_points}
        - 欲推廣產品/成分：{product}
        - 語氣：{tone}

        【撰寫規則與法規限制 (非常重要)】
        1. **法規紅線**：嚴格遵守台灣藥事法與化妝品衛生安全管理法。
           - 若產品非藥品，**絕對不能**宣稱「治療」、「改善」、「預防」特定疾病。
           - 產品僅能作為「營養補給」、「健康維持」、「保養輔助」或「舒緩」。
           - 不要將產品名稱與療效直接畫上等號。
        2. **結構**：
           - [吸睛標題]：用 emoji 和痛點吸引注意。
           - [情境共鳴]：描述客人常見困擾。
           - [藥師衛教]：解釋原理 (專業知識)。
           - [軟性置入]：根據輸入的產品，建議適合的族群或保養方式 (不要硬推銷)。
           - [Take Home Message]：一句話總結知識點。
        3. **格式**：分段清楚，適當使用 emoji，適合手機閱讀。
        """

        with st.spinner("藥師大腦運轉中...正在撰寫文案..."):
            try:
                response = model.generate_content(prompt)
                st.markdown("### 🎉 你的貼文草稿：")
                st.markdown("---")
                st.markdown(response.text)
                st.success("生成完成！請記得人工檢查一遍再發布喔！")
            except Exception as e:
                st.error(f"發生錯誤：{e}")
