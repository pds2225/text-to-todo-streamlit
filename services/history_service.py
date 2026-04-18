"""
세션 내 파싱 히스토리 관리.
디스크/DB 저장 없이 st.session_state만 사용.
"""
from __future__ import annotations
from typing import Any

from schemas.result_schema import ParseResult
from utils.constants import HISTORY_MAX_SIZE

# TODO: TASK-603 — 아래 함수들을 구현할 것

_HISTORY_KEY = "history"


def add_to_history(session_state: Any, result: ParseResult) -> None:
    """결과를 히스토리 앞에 추가. 최대 HISTORY_MAX_SIZE 개 유지.

    TODO: 구현
    """
    if _HISTORY_KEY not in session_state:
        session_state[_HISTORY_KEY] = []
    session_state[_HISTORY_KEY].insert(0, result)
    session_state[_HISTORY_KEY] = session_state[_HISTORY_KEY][:HISTORY_MAX_SIZE]


def get_history(session_state: Any) -> list[ParseResult]:
    """히스토리 목록 반환. 없으면 []."""
    return session_state.get(_HISTORY_KEY, [])


def clear_history(session_state: Any) -> None:
    """히스토리 초기화."""
    session_state[_HISTORY_KEY] = []
