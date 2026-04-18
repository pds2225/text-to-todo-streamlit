"""테스트: parser/text_cleaner.py — TASK-101"""
import pytest
from parser.text_cleaner import clean


def test_removes_web_notification_tag():
    result = clean("[Web발신]\n안녕하세요")
    assert "[Web발신]" not in result, f"got: {result}"


def test_removes_sms_tag():
    result = clean("[SMS발신]\n내용")
    assert "[SMS발신]" not in result, f"got: {result}"


def test_collapses_multiple_blank_lines():
    result = clean("줄\n\n\n\n바꿈")
    assert "\n\n\n" not in result, f"got: {result}"


def test_strips_leading_trailing_whitespace():
    result = clean("  공백  ")
    assert result == result.strip(), f"got: {result!r}"


def test_removes_markdown_bold():
    result = clean("**마크다운**")
    assert "**" not in result, f"got: {result}"


def test_preserves_meaningful_text():
    text = "청년월세 신청서류 보완요청"
    result = clean(text)
    assert "청년월세" in result, f"got: {result}"


def test_empty_string_returns_empty():
    assert clean("") == ""
