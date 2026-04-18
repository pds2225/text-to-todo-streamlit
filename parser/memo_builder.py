"""
메모 문자열 조합 모듈.
"""
from __future__ import annotations
from typing import Optional


def build_memo(
    organization: Optional[str],
    emails: list[str],
    phones: list[str],
    conditions: list[str],
    submit_method: Optional[str],
) -> str:
    """메모 문자열을 조합. 없는 필드는 생략."""
    parts: list[str] = []

    if organization:
        parts.append(organization)
    if submit_method:
        parts.append(f"{submit_method} 제출")
    if emails:
        parts.extend(emails[:2])
    if phones:
        parts.extend(phones[:2])

    memo = " / ".join(parts)

    if conditions:
        memo += "\n조건: " + " · ".join(conditions)

    return memo[:200]
