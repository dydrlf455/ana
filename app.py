import streamlit as st
import pandas as pd
import plotly.express as px
import json
import google.generativeai as genai

st.set_page_config(page_title="생기부 종단 궤적 진단", layout="wide")
st.title("📈 5개 대학 기준 생기부 성장 궤적 진단")

# 1. 입력부 설정
career_goal = st.text_input(
    "🎯 희망 진로 및 진학 학과", 
    placeholder="예: 약학과, 제약공학과",
    help="AI가 학생의 진로역량(전공 적합성)을 평가하는 기준점이 됩니다."
)

tabs = st.tabs(["1학년", "2학년", "3학년"])
record_data = {}

for i, tab in enumerate(tabs):
    grade = f"{i+1}학년"
    with tab:
        st.subheader(f"{grade} 기록 입력")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            auto_act = st.text_area(f"{grade} 자율활동", key=f"auto_{i}", height=150, placeholder="자율활동 내용 입력")
        with col2:
            club_act = st.text_area(f"{grade} 동아리활동", key=f"club_{i}", height=150, placeholder="동아리활동 내용 입력")
        with col3:
            career_act = st.text_area(f"{grade} 진로활동", key=f"career_{i}", height=150, placeholder="진로활동 내용 입력")
            
        st.markdown(f"**{grade} 교과 세특**")
        st.caption("💡 표의 맨 아랫줄을 클릭하여 과목명과 세특 내용을 붙여넣으세요.")
        
        df_subject = pd.DataFrame([{"과목명": "", "세특 내용": ""}])
        subject_data = st.data_editor(df_subject, num_rows="dynamic", key=f"subject_{i}", use_container_width=True)
        
        record_data[grade] = {
            "자율활동": auto_act, 
            "동아리활동": club_act, 
            "진로활동": career_act, 
            "교과세특": subject_data
        }

# 2. 분석 버튼 및 AI API 호출
if st.button("AI 사정관 종단 분석 시작", type="primary"):
    with st.spinner("학생의 데이터를 바탕으로 5개 대학 기준 분석을 진행 중입니다... (약 10~20초 소요)"):
        try:
            # API 키 설정 (Streamlit Secrets에서 불러오기)
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            
            # JSON 형태로만 답변하도록 모델 설정
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash-latest",
                generation_config={"response_mime_type": "application/json"}
            )
            
            # 학생 데이터 텍스트 취합
            input_text = f"희망 진로: {career_goal}\n\n"
            for grade, data in record_data.items():
                input_text += f"[{grade}]\n"
                input_text += f"- 자율활동: {data['자율활동']}\n"
                input_text += f"- 동아리활동: {data['동아리활동']}\n"
                input_text += f"- 진로활동: {data['진로활동']}\n"
                
                subject_str = ""
                for _, row in data['교과세특'].iterrows():
                    if row['과목명'] and row['세특 내용']:
                        subject_str += f"  * {row['과목명']}: {row['세특 내용']}\n"
                input_text += f"- 교과세특:\n{subject_str}\n\n"

            # 베테랑 입학사정관 프롬프트 (5개 대학 공통 평가요소 기준)
            system_prompt = """
            당신은 건국대, 경희대, 연세대, 중앙대, 한국외대가 공동 연구한 'NEW 학생부종합전형 공통 평가요소'를 엄격하게 적용하는 베테랑 입학사정관입니다.
            제공된 학생부 텍스트를 분석하여 다음 JSON 형식으로만 정확히 응답하세요. (입력되지 않은 학년의 점수는 모두 0으로 처리하세요.)

            {
              "story_trajectory": "1학년부터 현재까지의 관심사 심화 과정 및 학생의 핵심 강점을 종합하여 2~3문장으로 요약 (예: 1학년 때 ~한 관심이 2학년 때 ~로 심화됨)",
              "flow_1": "1학년 기록에서 도출된 주요 관심사 요약 (약 20자)",
              "flow_2": "2학년 기록에서 도출된 심화 관심사 요약 (기록이 없으면 1학년 기반 추천 목표)",
              "flow_3": "3학년 기록 기반 목표 또는 진학을 위한 최종 추천 목표 (약 20자)",
              "growth_scores": {
                "1학년": {"학업역량": 0~100, "진로역량": 0~100, "공동체역량": 0~100},
                "2학년": {"학업역량": 0~100, "진로역량": 0~100, "공동체역량": 0~100},
                "3학년": {"학업역량": 0~100, "진로역량": 0~100, "공동체역량": 0~100}
              },
              "sub_items": [
                {"역량": "학업역량", "항목": "탐구력", "진단": "🟢 우수 | 🟡 보통 | 🔴 부족 중 택1", "코멘트": "학생 기록에 기반한 구체적 근거 1문장"},
                {"역량": "학업역량", "항목": "학업태도", "진단": "🟢 우수 | 🟡 보통 | 🔴 부족 중 택1", "코멘트": "학생 기록에 기반한 구체적 근거 1문장"},
                {"역량": "진로역량", "항목": "진로탐색활동", "진단": "🟢 우수 | 🟡 보통 | 🔴 부족 중 택1", "코멘트": "학생 기록에 기반한 구체적 근거 1문장"},
                {"역량": "공동체역량", "항목": "협업과소통능력", "진단": "🟢 우수 | 🟡 보통 | 🔴 부족 중 택1", "코멘트": "학생 기록에 기반한 구체적 근거 1문장"},
                {"역량": "공동체역량", "항목": "리더십", "진단": "🟢 우수 | 🟡 보통 | 🔴 부족 중 택1", "코멘트": "학생 기록에 기반한 구체적 근거 1문장"}
              ],
              "action_plan": "현재 기록의 약점을 보완하고, 개념 기반의 '질문 중심 심화 탐구'를 다음 학기에 어떻게 전개할지에 대한 구체적이고 뼈 때리는 조언 (3~4문장)"
            }
            """
            
            # API 호출
            response = model.generate_content(system_prompt + "\n\n[학생 데이터]\n" + input_text)
            result = json.loads(response.text)
            
        except Exception as e:
            st.error("API 호출 중 에러가 발생했습니다. 입력창에 텍스트가 충분한지, 혹은 API 키가 정확히 설정되었는지 확인해주세요.")
            st.write(f"상세 에러: {e}")
            st.stop()

        # 3. 결과 화면 렌더링
        st.divider()
        st.header("📊 입학사정관 종단 궤적 리포트")
        
        st.subheader("🎯 관심사 심화 스토리라인")
        st.info(result["story_trajectory"])
        
        col_a, col_b, col_c, col_d, col_e = st.columns([2, 1, 2, 1, 2])
        col_a.success(f"🌱 1학년\n\n{result['flow_1']}")
        col_b.markdown("## ➡️")
        col_c.warning(f"🌿 2학년\n\n{result['flow_2']}")
        col_d.markdown("## ➡️")
        col_e.error(f"🌳 3학년 (목표)\n\n{result['flow_3']}")
        
        st.divider()

        col1, col2 = st.columns([3, 2])
        with col1:
            st.subheader("📈 3대 역량 학년별 성장 궤적")
            df_growth = pd.DataFrame(result["growth_scores"]).T.reset_index().rename(columns={"index": "학년"})
            # 점수가 0인 학년(미입력)은 그래프에서 제외
            df_growth = df_growth[(df_growth["학업역량"] > 0) | (df_growth["진로역량"] > 0) | (df_growth["공동체역량"] > 0)]
            df_melted = df_growth.melt(id_vars="학년", var_name="역량", value_name="점수")
            
            fig = px.line(df_melted, x="학년", y="점수", color="역량", markers=True, range_y=[0, 100])
            fig.update_traces(textposition="bottom right", marker=dict(size=10))
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.subheader("🚦 5대 대학 세부 항목 진단")
            df_sub = pd.DataFrame(result["sub_items"])
            st.dataframe(df_sub, hide_index=True, use_container_width=True)

        st.divider()
        st.subheader("💡 입학사정관의 Action Plan")
        st.write(result["action_plan"])
        
        st.divider()
        col_print1, col_print2 = st.columns([4, 1])
        with col_print1:
            st.caption("※ 단축키 `Ctrl + P` (Mac은 `Cmd + P`)를 누르시면 현재 리포트를 PDF로 저장하거나 인쇄할 수 있습니다.")
        with col_print2:
            st.components.v1.html(
                """
                
                    🖨️ 리포트 인쇄/저장
                
                """, height=50
            )
