"""
Google Tasks 리스트 추천 모듈 — 개선1.
사용자의 실제 Tasks 패턴(업무/업무장기/개인/짬짬이)을 기반으로 분류.
"""
from __future__ import annotations
from utils.constants import LIST_KEYWORDS


def recommend_list(
    text: str,
    category: str,
    urls: list[str],
    checklist: list[str],
) -> str:
    """어느 Google Tasks 리스트에 넣을지 추천.

    Returns:
        '업무' | '업무(장기)' | '개인' | '짬짬이'
    """
    if not text:
        return "업무"

    # 우선순위: 개인 → 업무(장기) → 짬짬이 → 업무(기본값)
    for list_name in ["개인", "업무(장기)", "짬짬이"]:
        for kw in LIST_KEYWORDS.get(list_name, []):
            if kw in text:
                return list_name

    # URL만 있고 체크리스트/서류 없는 짧은 텍스트 → 짬짬이
    cleaned_len = len(text.replace(" ", "").replace("\n", ""))
    if urls and not checklist and cleaned_len < 80:
        return "짬짬이"

    return "업무"
