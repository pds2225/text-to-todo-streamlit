"""테스트: parser/orchestrator.py — TASK-503"""
import pytest
from datetime import date
from parser.orchestrator import parse

SAMPLE_TEXT = """[Web발신]
[청년월세 신청서류 보완요청]

안녕하십니까 합정동주민센터입니다.
신청하신 청년월세 보완서류 관련하여 연락드렸습니다.
4월 17일(금)까지 아래 서류를 메일로 보내주시기 바랍니다.

보완서류
-부 기준, 모 기준의 가족관계증명서(상세)-주민등록번호 뒷자리 공개(총 2장)
-통장사본
-부모님 거주지 자가 아닐 경우, 부모님 거주지 임대차계약서

naru0219@mapo.go.kr"""

BASE = date(2026, 4, 15)


def test_parse_returns_parse_result():
    from schemas.result_schema import ParseResult
    result = parse(SAMPLE_TEXT, BASE)
    assert isinstance(result, ParseResult)


def test_parse_preserves_raw_text():
    result = parse(SAMPLE_TEXT, BASE)
    assert result.raw_text == SAMPLE_TEXT


def test_parse_extracts_email():
    result = parse(SAMPLE_TEXT, BASE)
    assert "naru0219@mapo.go.kr" in result.emails, f"got: {result.emails}"


def test_parse_extracts_deadline():
    result = parse(SAMPLE_TEXT, BASE)
    assert result.deadline == "2026-04-17", f"got: {result.deadline}"


def test_parse_classifies_category():
    result = parse(SAMPLE_TEXT, BASE)
    assert result.category == "보완요청", f"got: {result.category}"


def test_parse_extracts_organization():
    result = parse(SAMPLE_TEXT, BASE)
    assert result.organization == "합정동주민센터", f"got: {result.organization}"


def test_parse_extracts_checklist():
    result = parse(SAMPLE_TEXT, BASE)
    assert len(result.checklist) >= 3, f"got: {result.checklist}"


def test_parse_empty_string_no_exception():
    result = parse("", BASE)
    assert result is not None


def test_parse_no_date_text():
    result = parse("안녕하세요. 연락드립니다.", BASE)
    assert result.deadline is None
