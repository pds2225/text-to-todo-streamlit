"""
실행형 제목 생성 모듈.
"""
from __future__ import annotations
import re
from typing import Optional

from utils.regex_patterns import BRACKET_TITLE_PATTERN
from utils.constants import SUBMIT_METHODS

_CATEGORY_NOISE = ["보완요청", "제출요청", "납부요청", "방문/예약", "방문예약", "일반안내"]

_ACTION_MAP = {
    "보완요청": "서류보완",
    "제출요청": "서류제출",
    "납부요청": "납부처리",
    "방문/예약": "방문예약",
    "일반안내": "확인필요",
}

_SUBMIT_ACTION = {
    "이메일": "메일발송",
    "팩스": "팩스발송",
    "방문": "방문접수",
    "우편": "우편발송",
    "온라인": "온라인제출",
}


def build_title(text: str, category: str, organization: Optional[str]) -> str:
    """실행형 제목을 생성."""
    if not text:
        return _fallback(category, organization)

    # 대괄호 제목 우선 추출
    matches = BRACKET_TITLE_PATTERN.findall(text)
    if matches:
        bracket = matches[0]
        # 카테고리 노이즈 키워드 제거
        for noise in _CATEGORY_NOISE:
            bracket = bracket.replace(noise, "").strip()
        bracket = bracket.strip("[] ")

        submit = _detect_submit_method(text)
        if submit and submit in _SUBMIT_ACTION:
            return f"{bracket} {_SUBMIT_ACTION[submit]}"
        return bracket if bracket else _fallback(category, organization)

    return _fallback(category, organization)


def _fallback(category: str, organization: Optional[str]) -> str:
    action = _ACTION_MAP.get(category, "확인필요")
    if organization:
        return f"{organization} {action}"
    return action


def _detect_submit_method(text: str) -> Optional[str]:
    """텍스트에서 제출 방법을 감지."""
    for method, keywords in SUBMIT_METHODS.items():
        for kw in keywords:
            if kw in text:
                return method
    return None
