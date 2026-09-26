import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. 기본 설정
st.set_page_config(page_title="생기부 종단 궤적 진단", layout="wide")
st.title("📈 5개 대학 기준 생기부 성장 궤적 진단")

# 2. 진로/진학 목표 설정 (최상단 고정)
career_goal = st.text_input("🎯 희망 진로 및 진학 학과", placeholder="예: 역사교육과, 사회학과")

# 3. 학년별 입력부 (모듈형 탭 구조)
tabs = st.tabs(["1학년", "2학년", "3학년"])

# 데이터 저장을 위한 딕셔너리 구조
record_data = {}

for i, tab in enumerate(tabs):
    grade = f"{i+1}학년"
    with tab:
        st.subheader(f"{grade} 기록 입력")
        
        col1, col2 = st.columns(2)
        with col1:
            auto_act = st.text_area(f"{grade} 자율활동", key=f"auto_{i}", height=150, placeholder="자율활동 특기사항을 붙여넣으세요")
        with col2:
            career_act = st.text_area(f"{grade} 진로활동", key=f"career_{i}", height=150, placeholder="진로활동 특기사항을 붙여넣으세요")
            
        st.markdown(f"**{grade} 교과 세특**")
        st.caption("표의 맨 아랫줄을 클릭하여 과목명과 세특 내용을 붙여넣으세요. 입력 칸은 이수한 만큼 무한정 늘어납니다.")
        
        # 동적 행 추가가 가능한 엑셀형 UI
        df_subject = pd.DataFrame([{"과목명": "", "세특 내용": ""}])
        subject_data = st.data_editor(df_subject, num_rows="dynamic", key=f"subject_{i}", use_container_width=True)
        
        # 입력된 데이터 갈무리
        record_data[grade] = {
            "자율활동": auto_act,
            "진로활동": career_act,
            "교과세특": subject_data
        }

# 4. 분석 버튼 및 결과 출력
if st.button("AI 사정관 종단 분석 시작", type="primary"):
    with st.spinner("입력된 학년별 데이터를 바탕으로 우상향 스토리를 진단하고 있습니다..."):
        
        # TODO: 실제 LLM API 호출로 교체할 부분 (프롬프트에 "입력되지 않은 학년/항목은 무시하고 평가" 지시 포함)
        # UI 구성을 위한 가상 분석 결과 (Mock Data)
        mock_analysis = {
            "story_trajectory": f"1학년 공통 한국사에서 보인 '사회 변화'에 대한 넓은 관심이, 2학년 사회문화와 진로활동을 거치며 '{career_goal if career_goal else '특정 시대의 노동 인권'}'과 같은 구체적인 주제로 성공적으로 심화되었습니다.",
            "growth_scores": {
                "1학년": {"학업역량": 65, "진로역량": 50, "공동체역량": 70},
                "2학년": {"학업역량": 80, "진로역량": 75, "공동체역량": 75},
                "3학년": {"학업역량": 85, "진로역량": 90, "공동체역량": 80}
            },
            "action_plan": "진로역량과 학업역량이 꾸준히 우상향하고 있습니다. 다음 학기에는 이 주제를 바탕으로 타 교과(예: 문학, 윤리 등)와 연계하는 융합적 탐구 기록을 남기면 완벽합니다."
        }

    st.divider()
    
    # --- 결과 화면: 세로토닌 스토리텔링 ---
    st.header("📊 입학사정관 종단 궤적 리포트")
    
    # 관심사의 심화 궤적 시각화 (텍스트 흐름도)
    st.subheader("🎯 관심사 심화 스토리라인")
    st.info(mock_analysis["story_trajectory"])
    
    # 텍스트 화살표 흐름도 UI
    col_a, col_b, col_c, col_d, col_e = st.columns([2, 1, 2, 1, 2])
    col_a.success("🌱 1학년\n\n사회 변화 전반에 대한 호기심")
    col_b.markdown("
