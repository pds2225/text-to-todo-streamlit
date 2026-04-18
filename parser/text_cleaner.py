"""
원문 텍스트 정제 모듈.
의미 있는 텍스트는 보존하고, 메타텍스트/노이즈만 제거한다.
"""
from __future__ import annotations
import re
from utils.constants import META_TEXT_PATTERNS


def clean(raw_text: str) -> str:
    """메타텍스트 제거, 공백 정리, 줄바꿈 정규화."""
    if not raw_text:
        return ""

    text = raw_text

    # [Web발신] 등 메타텍스트 제거
    for pattern in META_TEXT_PATTERNS:
        text = re.sub(pattern, "", text)

    # 마크다운 굵게 (**text**) 제거
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    # 마크다운 헤더 (#, ## 등) 제거
    text = re.sub(r"(?m)^#{1,6}\s*", "", text)

    # 줄별 앞뒤 공백 제거
    lines = [line.strip() for line in text.split("\n")]
    text = "\n".join(lines)

    # 연속 3줄 이상 빈 줄 → 2줄로 압축
    text = re.sub(r"\n{3,}", "\n\n", text)

    # 연속 공백/탭 → 단일 공백
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()
