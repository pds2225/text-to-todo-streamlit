"""테스트: parser/title_builder.py — TASK-501"""
import pytest
from parser.title_builder import build_title


def test_builds_title_from_bracket():
    text = "[청년월세 신청서류 보완요청]\n메일로 제출해주세요"
    result = build_title(text, "보완요청", "합정동주민센터")
    assert result, "제목이 빈 문자열"
    assert "청년월세" in result or "메일" in result, f"got: {result}"


def test_never_returns_empty_string():
    result = build_title("", "일반안내", None)
    assert result != "", f"got empty string"


def test_uses_category_when_no_bracket():
    result = build_title("서류를 제출해주세요", "제출요청", None)
    assert result, f"got: {result}"


def test_includes_org_when_no_bracket():
    result = build_title("방문 예약 바랍니다", "방문/예약", "구청")
    assert result, f"got: {result}"
