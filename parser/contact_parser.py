"""
이메일, 전화번호, URL 추출 모듈.
"""
from __future__ import annotations
from utils.regex_patterns import EMAIL_PATTERN, PHONE_PATTERN, URL_PATTERN


def extract_emails(text: str) -> list[str]:
    """이메일 주소를 추출하여 중복 제거 후 반환."""
    if not text:
        return []
    seen: list[str] = []
    for item in EMAIL_PATTERN.findall(text):
        if item not in seen:
            seen.append(item)
    return seen


def extract_phones(text: str) -> list[str]:
    """전화번호를 추출하여 하이픈 포함 형식으로 정규화 후 반환."""
    if not text:
        return []
    seen: list[str] = []
    for m in PHONE_PATTERN.finditer(text):
        normalized = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
        if normalized not in seen:
            seen.append(normalized)
    return seen


def extract_urls(text: str) -> list[str]:
    """URL을 추출하여 중복 제거 후 반환 — 개선4."""
    if not text:
        return []
    seen: list[str] = []
    for url in URL_PATTERN.findall(text):
        url = url.rstrip(".,;")  # 문장 부호 후처리
        if url not in seen:
            seen.append(url)
    return seen
