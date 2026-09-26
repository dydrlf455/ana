import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="생기부 종단 궤적 진단", layout="wide")
st.title("📈 5개 대학 기준 생기부 성장 궤적 진단")

career_goal = st.text_input(
    "🎯 희망 진로 및 진학 학과", 
    placeholder="예: 약학과, 제약공학과",
    help="AI가 학생의 진로역량(전공 적합성)을 평가하는 기준점이 됩니다. 구체적일수록 좋습니다."
)

tabs = st.tabs(["1학년", "2학년", "3학년"])
record_data = {}

for i, tab in enumerate(tabs):
    grade = f"{i+1}학년"
    with tab:
        st.subheader(f"{grade} 기록 입력")
        
        # 자율, 동아리, 진로를 3단으로 배치
        col1, col2, col3 = st.columns(3)
        with col1:
            auto_act = st.text_area(
                f"{grade} 자율활동", 
                key=f"auto_{i}", height=150, 
                placeholder="자율활동 내용 입력",
                help="학급 특색 활동, 프로젝트, 반장 등의 리더십 경험을 자세히 적어주세요."
            )
        with col2:
            club_act = st.text_area(
                f"{grade} 동아리활동", 
                key=f"club_{i}", height=150, 
                placeholder="동아리활동 내용 입력",
                help="동아리에서 주도적으로 진행한 탐구, 실험, 혹은 협력 프로젝트를 적어주세요."
            )
        with col3:
            career_act = st.text_area(
                f"{grade} 진로활동", 
                key=f"career_{i}", height=150, 
                placeholder="진로활동 내용 입력",
                help="진로 탐색 보고서, 진로 캠프 등 전공과 관련된 심화 탐구 내용을 적어주세요."
            )
            
        st.markdown(f"**{grade} 교과 세특**")
        st.caption("💡 표의 맨 아랫줄을 클릭하여 과목명과 세특 내용을 붙여넣으세요.")
        
        df_subject = pd.DataFrame([{"과목명": "", "세특 내용": ""}])
        subject_data = st.data_editor(df_subject, num_rows="dynamic", key=f"subject_{i}", use_container_width=True)
        
        # 동아리활동 데이터 저장 추가
        record_data[grade] = {
            "자율활동": auto_act, 
            "동아리활동": club_act, 
            "진로활동": career_act, 
            "교과세특": subject_data
        }

if st.button("AI 사정관 종단 분석 시작", type="primary"):
    with st.spinner("학생의 데이터를 바탕으로 5개 대학 기준 분석을 진행 중입니다..."):
        
        # (기존 Mock Data 영역 유지)
        mock_analysis = {
            "story_trajectory": f"1학년 진로 캠프에서 체득한 '중심원리(Central Dogma)'에 대한 이해가, 학급 특색 활동과 동아리를 거치며 '{career_goal if career_goal else '제약학'}'과 관련된 공중보건 문제로 훌륭하게 심화되었습니다.",
            "growth_scores": {
                "1학년": {"학업역량": 65, "진로역량": 70, "공동체역량": 80},
                "2학년": {"학업역량": 85, "진로역량": 90, "공동체역량": 85},
                "3학년": {"학업역량": 0, "진로역량": 0, "공동체역량": 0} 
            },
            "sub_items": [
                {"역량": "학업역량", "항목": "탐구력", "진단": "🟢 우수", "코멘트": "GLP-1 호르몬 기전을 도식화하고 국정 감사 자료를 근거로 활용한 점이 탁월함."},
                {"역량": "학업역량", "항목": "학업태도", "진단": "🟢 우수", "코멘트": "질문에 즉답하지 못한 것을 부끄러워하지 않고 재탐구하여 설명하는 태도."},
                {"역량": "진로역량", "항목": "진로탐색경험", "진단": "🟢 우수", "코멘트": "독성학 등 구체적인 커리큘럼까지 탐색하며 로드맵을 그림."},
                {"역량": "공동체역량", "항목": "리더십", "진단": "🟡 보통", "코멘트": "소극적인 학생들을 독려한 경험이 있으나, 구체적인 갈등 해결 사례가 보완되면 좋음."}
            ],
            "action_plan": "진로에 대한 비전과 생명과학적 탐구력이 매우 우수합니다. 다음 학기에는 '약물의 유통 모니터링 시스템'에 관한 아이디어를 사회(혹은 정보) 교과와 연계하여 정책적, 윤리적 관점에서 다뤄보길 권장합니다."
        }

    st.divider()
    st.header("📊 입학사정관 종단 궤적 리포트")
    
    st.subheader("🎯 관심사 심화 스토리라인")
    st.info(mock_analysis["story_trajectory"])
    
    col_a, col_b, col_c, col_d, col_e = st.columns([2, 1, 2, 1, 2])
    col_a.success("🌱 1학년\n\n중심원리(Central Dogma) 등 분자생물학적 기초 확립")
    col_b.markdown("## ➡️")
    col_c.warning("🌿 2학년\n\nGLP-1 작용 기전 탐구 및 공중보건 문제로의 시각 확장")
    col_d.markdown("## ➡️")
    col_e.error(f"🌳 3학년 (목표)\n\n{career_goal if career_goal else '약학'} 분야의 다각적 융합 탐구 (정책, 윤리 등)")
    
    st.divider()

    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("📈 3대 역량 학년별 성장 궤적")
        df_growth = pd.DataFrame(mock_analysis["growth_scores"]).T.reset_index().rename(columns={"index": "학년"})
        df_growth = df_growth[(df_growth["학업역량"] > 0) | (df_growth["진로역량"] > 0) | (df_growth["공동체역량"] > 0)]
        df_melted = df_growth.melt(id_vars="학년", var_name="역량", value_name="점수")
        
        fig = px.line(df_melted, x="학년", y="점수", color="역량", markers=True, range_y=[0, 100])
        fig.update_traces(textposition="bottom right", marker=dict(size=10))
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.subheader("🚦 5대 대학 세부 항목 진단")
        df_sub = pd.DataFrame(mock_analysis["sub_items"])
        st.dataframe(df_sub, hide_index=True, use_container_width=True)

    st.divider()
    st.subheader("💡 입학사정관의 Action Plan")
    st.write(mock_analysis["action_plan"])
    
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
