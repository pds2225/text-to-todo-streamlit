"""테스트: parser/checklist_parser.py — TASK-401"""
import pytest
from parser.checklist_parser import extract_checklist

SAMPLE = """보완서류
-부 기준, 모 기준의 가족관계증명서(상세)-주민등록번호 뒷자리 공개(총 2장)
-통장사본
-부모님 거주지 자가 아닐 경우, 부모님 거주지 임대차계약서"""


def test_extracts_minimum_three_items():
    result = extract_checklist(SAMPLE)
    assert len(result) >= 3, f"got {len(result)} items: {result}"


def test_splits_bu_mo_into_two_items():
    result = extract_checklist(SAMPLE)
    bu = any("부 기준" in item for item in result)
    mo = any("모 기준" in item for item in result)
    assert bu and mo, f"분리 안됨: {result}"


def test_condition_preserved_in_item():
    result = extract_checklist(SAMPLE)
    conditional = any("자가 아닐 경우" in item or "자가" in item for item in result)
    assert conditional, f"조건문 없음: {result}"


def test_no_duplicate_items():
    doubled = SAMPLE + "\n" + SAMPLE
    result = extract_checklist(doubled)
    assert len(result) == len(set(result)), f"중복 존재: {result}"


def test_no_trigger_keyword_returns_empty():
    result = extract_checklist("안녕하세요. 별다른 서류는 없습니다.")
    assert result == [], f"got: {result}"


def test_bullet_point_items():
    text = "준비물\n• 신분증\n• 도장"
    result = extract_checklist(text)
    assert len(result) >= 2, f"got: {result}"


def test_numbered_items():
    text = "제출서류\n1. 주민등록등본\n2. 통장사본"
    result = extract_checklist(text)
    assert len(result) >= 2, f"got: {result}"


def test_empty_string_returns_empty():
    assert extract_checklist("") == []
