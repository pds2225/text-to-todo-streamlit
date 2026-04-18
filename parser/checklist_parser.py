"""
체크리스트(서류 목록) 추출 모듈.
섹션 키워드 이후의 목록 항목만 추출한다.
"""
from __future__ import annotations
import re
from utils.constants import CHECKLIST_TRIGGER_KEYWORDS


def extract_checklist(text: str) -> list[str]:
    """서류/항목 목록을 추출. 없으면 []."""
    if not text:
        return []

    # 첫 번째 트리거 키워드 위치 탐색
    trigger_pos = -1
    for kw in CHECKLIST_TRIGGER_KEYWORDS:
        pos = text.find(kw)
        if pos != -1 and (trigger_pos == -1 or pos < trigger_pos):
            trigger_pos = pos

    if trigger_pos == -1:
        return []

    # 트리거 키워드 이후 줄부터 파싱
    after_trigger = text[trigger_pos:]
    lines = after_trigger.split("\n")[1:]  # 트리거 라인 자체는 건너뜀

    raw_items: list[str] = []
    for line in lines:
        line = line.strip()
        if not line:
            # 빈 줄이 연속되면 목록 끝
            if raw_items:
                break
            continue

        # 대시/불릿 패턴
        m = re.match(r"^[-•·]\s*(.+)$", line)
        if not m:
            # 번호 목록 패턴
            m = re.match(r"^\d+[.)]\s*(.+)$", line)

        if m:
            raw_items.append(m.group(1).strip())
        elif raw_items:
            # 목록이 시작된 후 비목록 라인이 나오면 종료
            break

    # 항목 분리/정제
    items: list[str] = []
    for raw in raw_items:
        items.extend(_split_item(raw))

    # 중복 제거 (순서 유지)
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        item = item.strip()
        if item and item not in seen:
            seen.add(item)
            result.append(item)

    return result


def _split_item(text: str) -> list[str]:
    """'부 기준, 모 기준의 X' 분리 및 조건문 처리."""
    # 패턴: "A 기준, B 기준의 나머지"
    m = re.match(r"^(.+?)\s*기준,\s*(.+?)\s*기준의\s+(.+)$", text)
    if m:
        prefix_a = m.group(1).strip()
        prefix_b = m.group(2).strip()
        suffix = m.group(3).strip()
        return [
            f"{prefix_a} 기준 {suffix}",
            f"{prefix_b} 기준 {suffix}",
        ]

    # 조건문: "조건, 실제항목" — '아닐 경우', '없는 경우', '미해당 시' 포함
    m = re.match(
        r"^(.+?(?:아닐\s*경우|없는\s*경우|미해당\s*시))[,\s]+(.+)$", text
    )
    if m:
        condition = m.group(1).strip().rstrip(",").strip()
        item = m.group(2).strip()
        return [f"{item} ({condition})"]

    return [text]
