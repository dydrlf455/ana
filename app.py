import streamlit as st
import plotly.express as px
import pandas as pd
import json
import time

# 1. 페이지 기본 설정
st.set_page_config(page_title="생기부 입학사정관 진단", layout="wide")

st.title("📊 5개 대학 기준 생기부 핵심 역량 진단")
st.markdown("교과 세특, 창의적 체험활동, 행동특성 및 종합의견 텍스트를 붙여넣으세요.")

# 2. 텍스트 입력부 (복사-붙여넣기)
example_placeholder = """(예시) 
한국사: 1970년대 급격한 경제 성장과 산업화 과정을 조사하며 당시 노동 환경의 변화를 분석함. 
통합사회: 환경 오염 문제를 다루며 지속가능한 발전의 필요성을 발표함.
동아리활동: 역사 탐구 동아리에서 질문 중심 탐구 모형을 적용해 자료를 수집하고 토론을 주도함."""

student_text = st.text_area("여기에 생기부 내용을 붙여넣으세요:", height=250, placeholder=example_placeholder)

# 3. 분석 버튼 및 결과 출력부
if st.button("AI 사정관 분석 시작", type="primary"):
    if len(student_text) < 20:
        st.warning("분석할 텍스트가 너무 짧습니다. 충분한 내용을 붙여넣어 주세요.")
    else:
        with st.spinner("5개 대학 평가 기준을 적용하여 분석 중입니다..."):
            
            # TODO: 실제 LLM(OpenAI/Gemini) API 호출이 들어갈 자리입니다.
            # 지금은 UI 테스트를 위해 API 응답을 받았다고 가정(Simulation)합니다.
            time.sleep(1.5) # 분석하는 척 지연 시간
            
            # 가상의 AI 분석 결과 JSON
            mock_result = {
                "overall_summary": "지적 호기심을 바탕으로 깊이 있게 탐구한 '탐구력' 강점이 돋보이나, 융합적 사고를 보여주는 기록이 보완되면 더 좋은 평가를 받을 수 있습니다.",
                "radar_chart_data": {"학업역량": 85, "진로역량": 75, "공동체역량": 90},
                "action_plan": {
                    "weakness_fix": "다음 학기에는 단순 조사를 넘어, 두 가지 이상의 교과(예: 역사와 사회) 개념을 연결하는 프로젝트를 시도해 보세요.",
                    "deep_inquiry_question": "1970년대 급격한 산업화가 초래한 노동 환경 문제가 현대 사회의 플랫폼 노동 문제와 어떤 구조적 공통점을 가질까?"
                }
            }

        # --- 여기서부터 원페이지 대시보드 렌더링 ---
        st.divider()
        
        # [상단] 레이더 차트 및 종합 코멘트
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("🎯 3대 역량 밸런스")
            df = pd.DataFrame(dict(
                점수=list(mock_result["radar_chart_data"].values()),
                역량=list(mock_result["radar_chart_data"].keys())
            ))
            fig = px.line_polar(df, r='점수', theta='역량', line_close=True, range_r=[0, 100])
            fig.update_traces(fill='toself', marker=dict(size=8))
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.subheader("💡 입학사정관 종합 코멘트")
            st.info(mock_result["overall_summary"])
            
            st.subheader("🔍 강점 및 보완점 요약")
            st.success("🟢 우수: 질문 중심 탐구 모형을 적용한 주도적 자료 수집 (탐구력)")
            st.warning("🟡 보통: 전공(계열) 관련 심화 교과 이수 노력 (진로역량)")
        
        st.divider()
        
        # [하단] 행동 설계 및 심화 탐구 (Action Plan)
        st.subheader("🚀 다음 학기를 위한 Action Plan")
        
        st.markdown("**1. 약점 보완 가이드**")
        st.write(mock_result["action_plan"]["weakness_fix"])
        
        st.markdown("**2. 질문 중심 심화 탐구 제안**")
        st.error(f"**추천 질문:** {mock_result['action_plan']['deep_inquiry_question']}")
