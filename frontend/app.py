import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="🤖 Exact Instructions Challenge",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Exact Instructions Challenge")
st.caption("Josh Darnit의 그 유명한 챌린지 — 아빠(컴퓨터)는 글자 그대로만 따릅니다.")

st.divider()

# 세션 초기화
if "steps" not in st.session_state:
    st.session_state.steps = []
if "step_count" not in st.session_state:
    st.session_state.step_count = 1

# 목표 설정
st.subheader("🎯 오늘의 미션")
mission = st.text_input("무엇을 만들거나 할 건가요?", placeholder="예: 땅콩버터 샌드위치 만들기")

st.divider()

# 지시 입력
st.subheader(f"📝 {st.session_state.step_count}단계 지시를 입력하세요")
instruction = st.text_input(
    "지시문",
    placeholder="예: 빵을 집어",
    key=f"input_{st.session_state.step_count}"
)

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("🚀 컴퓨터에게 전달!", use_container_width=True):
        if instruction.strip():
            with st.spinner("컴퓨터가 처리 중..."):
                response = requests.post(f"{API_URL}/interpret", json={
                    "instruction": instruction,
                    "step_number": st.session_state.step_count
                })
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.steps.append(data)
                    st.session_state.step_count += 1
                    st.rerun()
                else:
                    st.error("API 오류 발생!")
        else:
            st.warning("지시문을 입력하세요!")

with col2:
    if st.button("🔄 처음부터 다시", use_container_width=True):
        st.session_state.steps = []
        st.session_state.step_count = 1
        st.rerun()

st.divider()

# 결과 히스토리
if st.session_state.steps:
    st.subheader("📜 지시 & 반응 기록")
    for step in reversed(st.session_state.steps):
        with st.container():
            st.markdown(f"**{step['step_number']}단계** 👤 나: _{step['original']}_")
            st.error(f"🤖 컴퓨터: {step['literal_response']}")
            st.write("")