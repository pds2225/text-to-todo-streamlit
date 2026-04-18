"""
텍스트 카테고리 분류 모듈.
키워드 기반 규칙으로 분류하며 LLM을 사용하지 않는다.
"""
from __future__ import annotations
from utils.constants import CATEGORY_KEYWORDS, DEFAULT_CATEGORY


def classify(text: str) -> str:
    """텍스트를 카테고리로 분류.

    Returns:
        '보완요청' | '제출요청' | '납부요청' | '방문/예약' | '일반안내'
    """
    if not text:
        return DEFAULT_CATEGORY

    for category, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return category

    return DEFAULT_CATEGORY
