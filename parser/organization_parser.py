"""
기관명 추출 모듈.
"""
from __future__ import annotations
import re
from typing import Optional
from utils.constants import ORGANIZATION_SUFFIXES


def extract_organization(text: str) -> Optional[str]:
    """기관명을 추출. 추출 불가 시 None 반환."""
    if not text:
        return None

    # 우선순위 1: '안녕하십니까 XX입니다' 발신자 서명 패턴
    greeting = re.search(r"안녕하십니까\s+(.{2,20}?)입니다", text)
    if greeting:
        candidate = greeting.group(1).strip()
        # 너무 긴 경우 suffix로 자르기
        for suffix in ORGANIZATION_SUFFIXES:
            if suffix in candidate:
                idx = candidate.index(suffix) + len(suffix)
                return candidate[:idx]
        return candidate

    # 우선순위 2: suffix 기반 기관명 패턴 (한글 1~10자 + suffix)
    for suffix in ORGANIZATION_SUFFIXES:
        pattern = re.compile(r"[가-힣]{1,10}" + re.escape(suffix))
        m = pattern.search(text)
        if m:
            return m.group(0)

    return None
