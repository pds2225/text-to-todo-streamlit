"""
날짜/시간 표현 파싱 모듈.
실패 시 None을 반환하며, 절대 예외를 발생시키지 않는다.
"""
from __future__ import annotations
import re
from datetime import date, timedelta
from typing import Optional

from utils.regex_patterns import (
    DATE_ABSOLUTE_PATTERN,
    DATE_YEAR_MONTH_DAY_PATTERN,
    DATE_MONTH_DAY_PATTERN,
    DATE_SLASH_MONTH_DAY_PATTERN,
    DATE_RELATIVE_DAYS_PATTERN,
    DATE_WEEKDAY_PATTERN,
    TIME_AMPM_PATTERN,
    TIME_24H_PATTERN,
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
        # Rule 0: 연도 포함 한글 표현 — 2025년 12월 31일
        m = DATE_YEAR_MONTH_DAY_PATTERN.search(text)
        if m:
            y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
            result = date(y, mo, d)
            _last_parse_logs.append(f"[date_parser] 룰0 연도포함 한글 → {result}")
            return str(result)

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
                # 60일 넘게 과거인 경우만 내년으로 추론 (어제 받은 문자는 올해 유지)
                if result < base_date - timedelta(days=60):
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


def extract_time(text: str) -> Optional[str]:
    """시간 표현을 추출하여 HH:MM (24h) 형식으로 반환 — 개선2.

    지원 형식:
        오후 5:00  → 17:00
        오전 10시  → 10:00
        오후 2시 30분 → 14:30
    """
    if not text:
        return None
    try:
        m = TIME_AMPM_PATTERN.search(text)
        if m:
            ampm = m.group(1)
            hour = int(m.group(2))
            minute = int(m.group(3)) if m.group(3) else 0
            if ampm == "오후" and hour != 12:
                hour += 12
            elif ampm == "오전" and hour == 12:
                hour = 0
            return f"{hour:02d}:{minute:02d}"

        # 단독 24h 표기 (날짜 숫자와 겹치지 않도록 마지막에)
        m = TIME_24H_PATTERN.search(text)
        if m:
            h, mi = int(m.group(1)), int(m.group(2))
            if 0 <= h <= 23 and 0 <= mi <= 59:
                return f"{h:02d}:{mi:02d}"
    except Exception:
        pass
    return None


def get_parse_log() -> list[str]:
    """마지막 extract_deadline() 호출에서 적용된 룰 로그 반환."""
    return list(_last_parse_logs)
