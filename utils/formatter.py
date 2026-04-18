from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from schemas.result_schema import ParseResult


def format_checklist_text(checklist: list[str]) -> str:
    """체크리스트를 텍스트 형식으로 변환."""
    return "\n".join(f"- {item}" for item in checklist)


def format_result_summary(result: ParseResult) -> str:
    """결과 요약 한 줄 텍스트 (히스토리 목록 표시용)."""
    parts = []
    if result.title:
        parts.append(result.title)
    if result.deadline:
        parts.append(f"기한: {result.deadline}")
    if result.organization:
        parts.append(result.organization)
    return " | ".join(parts) if parts else "(제목 없음)"


def truncate(text: str, max_len: int = 20) -> str:
    """텍스트를 최대 길이로 자르고 ... 추가."""
    return text if len(text) <= max_len else text[:max_len] + "..."
