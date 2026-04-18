"""테스트: parser/date_parser.py — TASK-301"""
import pytest
from datetime import date
from parser.date_parser import extract_deadline


BASE = date(2026, 4, 15)


def test_absolute_date_dot_format():
    result = extract_deadline("2026.04.17까지", BASE)
    assert result == "2026-04-17", f"got: {result}"


def test_absolute_date_dash_format():
    result = extract_deadline("2026-04-17까지", BASE)
    assert result == "2026-04-17", f"got: {result}"


def test_month_day_korean_format():
    result = extract_deadline("4월 17일(금)까지", BASE)
    assert result == "2026-04-17", f"got: {result}"


def test_slash_month_day_format():
    result = extract_deadline("04/17까지 제출", BASE)
    assert result == "2026-04-17", f"got: {result}"


def test_relative_days_after_receive():
    result = extract_deadline("문자 수신 후 14일 이내", BASE)
    assert result == "2026-04-29", f"got: {result}"


def test_this_week_friday():
    result = extract_deadline("이번 주 금요일까지", BASE)
    assert result == "2026-04-17", f"got: {result}"


def test_today_keyword():
    result = extract_deadline("오늘까지", BASE)
    assert result == "2026-04-15", f"got: {result}"


def test_no_date_returns_none():
    result = extract_deadline("날짜 없는 텍스트입니다.", BASE)
    assert result is None, f"got: {result}"


def test_empty_string_returns_none():
    result = extract_deadline("", BASE)
    assert result is None, f"got: {result}"


def test_phone_number_not_mistaken_as_date():
    result = extract_deadline("010-1234-5678", BASE)
    assert result is None, f"got: {result}"
