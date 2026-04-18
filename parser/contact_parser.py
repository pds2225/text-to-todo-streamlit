"""
이메일 및 전화번호 추출 모듈.
"""
from __future__ import annotations
import re
from utils.regex_patterns import EMAIL_PATTERN, PHONE_PATTERN


def extract_emails(text: str) -> list[str]:
    """이메일 주소를 추출하여 중복 제거 후 반환."""
    if not text:
        return []
    found = EMAIL_PATTERN.findall(text)
    seen: list[str] = []
    for item in found:
        if item not in seen:
            seen.append(item)
    return seen


def extract_phones(text: str) -> list[str]:
    """전화번호를 추출하여 하이픈 포함 형식으로 정규화 후 반환."""
    if not text:
        return []
    seen: list[str] = []
    for m in PHONE_PATTERN.finditer(text):
        area, mid, last = m.group(1), m.group(2), m.group(3)
        normalized = f"{area}-{mid}-{last}"
        if normalized not in seen:
            seen.append(normalized)
    return seen
