"""
날짜 표현 파싱 모듈.
실패 시 None을 반환하며, 절대 예외를 발생시키지 않는다.
"""
from __future__ import annotations
import re
from datetime import date, timedelta
from typing import Optional

from utils.regex_patterns import (
    DATE_ABSOLUTE_PATTERN,
    DATE_MONTH_DAY_PATTERN,
    DATE_SLASH_MONTH_DAY_PATTERN,
    DATE_RELATIVE_DAYS_PATTERN,
    DATE_WEEKDAY_PATTERN,
    WEEKDAY_MAP,
)

_last_parse_logs: list[str] = []


def extract_deadline(text: str, base_date: date) -> Optional[str]:
    """날짜 표현을 추출하여 YYYY-MM-DD 형식으로 반환."""
    global _last_parse_logs
    _last_parse_logs = []

    if not text:
        return None

    try:
        # Rule 1: 완전 절대일자 — 2026.04.17 / 2026-04-17
        m = DATE_ABSOLUTE_PATTERN.search(text)
        if m:
            y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
            result = date(y, mo, d)
            _last_parse_logs.append(f"[date_parser] 룰1 완전 절대일자 → {result}")
            return str(result)

        # Rule 2: 월일 한글 표현 — 4월 17일(금)까지
        m = DATE_MONTH_DAY_PATTERN.search(text)
        if m:
            mo, d = int(m.group(1)), int(m.group(2))
            y = base_date.year
            try:
                result = date(y, mo, d)
                # 기준일보다 과거면 내년으로 추론
                if result < base_date:
                    result = date(y + 1, mo, d)
                _last_parse_logs.append(f"[date_parser] 룰2 월일 표현 (base_date 연도={y}) → {result}")
                return str(result)
            except ValueError:
                pass

        # Rule 3: 슬래시 월일 — 04/17
        m = DATE_SLASH_MONTH_DAY_PATTERN.search(text)
        if m:
            mo, d = int(m.group(1)), int(m.group(2))
            try:
                result = date(base_date.year, mo, d)
                _last_parse_logs.append(f"[date_parser] 룰3 슬래시 월일 → {result}")
                return str(result)
            except ValueError:
                pass

        # Rule 4: 수신 후 N일 이내
        m = DATE_RELATIVE_DAYS_PATTERN.search(text)
        if m:
            days = int(m.group(1))
            result = base_date + timedelta(days=days)
            _last_parse_logs.append(f"[date_parser] 룰4 수신 후 {days}일 → {result}")
            return str(result)

        # Rule 5: 이번 주 X요일
        m = DATE_WEEKDAY_PATTERN.search(text)
        if m:
            target_wd = WEEKDAY_MAP[m.group(1)]
            current_wd = base_date.weekday()
            days_ahead = (target_wd - current_wd) % 7
            if days_ahead == 0:
                days_ahead = 7
            result = base_date + timedelta(days=days_ahead)
            _last_parse_logs.append(f"[date_parser] 룰5 이번 주 {m.group(1)}요일 → {result}")
            return str(result)

        # Rule 6: '오늘'
        if "오늘" in text:
            _last_parse_logs.append(f"[date_parser] 룰6 '오늘' → {base_date}")
            return str(base_date)

    except Exception as e:
        _last_parse_logs.append(f"[date_parser] 파싱 실패 (예외 무시): {e}")

    _last_parse_logs.append("[date_parser] 날짜 표현 없음 → None")
    return None


def get_parse_log() -> list[str]:
    """마지막 extract_deadline() 호출에서 적용된 룰 로그 반환."""
    return list(_last_parse_logs)
