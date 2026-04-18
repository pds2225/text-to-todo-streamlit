"""
text-to-todo-streamlit — Streamlit 메인 앱.
UI 전용: 파싱 로직을 직접 포함하지 않는다.
"""
from __future__ import annotations

import streamlit as st
from datetime import date

from parser.orchestrator import parse
from services import export_service, history_service, sample_service
from utils.constants import CATEGORIES
from utils.formatter import format_result_summary

# ── 페이지 설정 ──────────────────────────────────────────────
st.set_page_config(page_title="텍스트 → 할일", page_icon="📋", layout="wide")
st.title("📋 텍스트 → 할일 변환기")

# ── 사이드바 ─────────────────────────────────────────────────
with st.sidebar:
    st.header("설정")
    debug_mode = st.checkbox("디버그 모드", value=False)

    st.divider()
    st.subheader("샘플 불러오기")
    # TODO: TASK-702 — sample_service.get_samples() 연동
    samples = sample_service.get_samples()
    if samples:
        selected_sample = st.selectbox("샘플 선택", ["(직접 입력)"] + list(samples.keys()))
    else:
        selected_sample = "(직접 입력)"

    st.divider()
    if st.button("히스토리 초기화"):
        history_service.clear_history(st.session_state)

# ── 입력 영역 ─────────────────────────────────────────────────
col_input, col_result = st.columns(2)

with col_input:
    st.subheader("원문 입력")
    default_text = (
        samples.get(selected_sample, "")
        if selected_sample != "(직접 입력)"
        else ""
    )
    raw_text = st.text_area(
        "텍스트를 붙여넣으세요",
        value=default_text,
        height=300,
        placeholder="[Web발신]\n[청년월세 신청서류 보완요청]\n...",
    )
    base_date = st.date_input("기준일 (오늘)", value=date.today())
    run_btn = st.button("🔍 분석하기", type="primary", use_container_width=True)

# ── 파싱 실행 ─────────────────────────────────────────────────
if run_btn and raw_text.strip():
    with st.spinner("분석 중..."):
        result = parse(raw_text, base_date)
    history_service.add_to_history(st.session_state, result)
    st.session_state["current_result"] = result

# ── 결과 편집 영역 ────────────────────────────────────────────
with col_result:
    st.subheader("결과 편집")

    if "current_result" not in st.session_state:
        st.info("원문을 입력하고 '분석하기'를 클릭하세요.")
    else:
        r = st.session_state["current_result"]

        edited_title = st.text_input("제목", value=r.title)

        # 리스트 추천 (개선1)
        LIST_OPTIONS = ["업무", "업무(장기)", "개인", "짬짬이"]
        edited_target_list = st.selectbox(
            "📂 Google Tasks 리스트",
            LIST_OPTIONS,
            index=LIST_OPTIONS.index(r.target_list) if r.target_list in LIST_OPTIONS else 0,
        )

        # 기한 + 시간 (개선2)
        dl_c1, dl_c2 = st.columns(2)
        with dl_c1:
            edited_deadline = st.text_input("기한 (YYYY-MM-DD)", value=r.deadline or "")
        with dl_c2:
            edited_time = st.text_input("시간 (HH:MM)", value=r.deadline_time or "")

        edited_summary = st.text_input("할일 요약", value=r.task_summary)
        edited_category = st.selectbox(
            "카테고리", CATEGORIES,
            index=CATEGORIES.index(r.category) if r.category in CATEGORIES else 0
        )
        edited_org = st.text_input("기관명", value=r.organization or "")
        edited_memo = st.text_area("메모", value=r.memo, height=80)

        # URL 목록 (개선4)
        if r.urls:
            st.markdown("**🔗 URL**")
            for url in r.urls:
                st.caption(url)

        # 서브태스크 (개선3) — Google Tasks 하위 항목으로 매핑
        if r.checklist:
            st.markdown("**☑ 서브태스크** (Google Tasks 하위 항목)")
        for i, item in enumerate(r.checklist):
            st.text_input(f"서브태스크 {i+1}", value=item, key=f"chk_{i}")

        # ── 다운로드 버튼 ─────────────────────────────────────
        st.divider()
        dl_col1, dl_col2, dl_col3 = st.columns(3)
        with dl_col1:
            st.download_button(
                "📄 TXT",
                data=export_service.to_txt(r),
                file_name="result.txt",
                mime="text/plain",
            )
        with dl_col2:
            st.download_button(
                "📦 JSON",
                data=export_service.to_json(r),
                file_name="result.json",
                mime="application/json",
            )
        with dl_col3:
            st.download_button(
                "📊 CSV",
                data=export_service.to_csv(r),
                file_name="result.csv",
                mime="text/csv",
            )

        # ── 디버그 로그 ───────────────────────────────────────
        if debug_mode and r.parse_logs:
            with st.expander("🔧 파싱 로그"):
                for log in r.parse_logs:
                    st.text(log)

# ── 히스토리 ─────────────────────────────────────────────────
history = history_service.get_history(st.session_state)
if history:
    st.divider()
    st.subheader("최근 분석 히스토리")
    for i, h in enumerate(history):
        label = format_result_summary(h)
        if st.button(label, key=f"hist_{i}"):
            st.session_state["current_result"] = h
            st.rerun()
