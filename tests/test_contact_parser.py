"""테스트: parser/contact_parser.py — TASK-102"""
import pytest
from parser.contact_parser import extract_emails, extract_phones


def test_extract_single_email():
    result = extract_emails("문의: naru0219@mapo.go.kr")
    assert "naru0219@mapo.go.kr" in result, f"got: {result}"


def test_extract_multiple_emails():
    result = extract_emails("a@b.com 그리고 c@d.org")
    assert len(result) == 2, f"got: {result}"


def test_no_duplicate_emails():
    result = extract_emails("naru0219@mapo.go.kr naru0219@mapo.go.kr")
    assert len(result) == 1, f"got: {result}"


def test_no_email_returns_empty():
    assert extract_emails("연락처 없음") == []


def test_extract_mobile_phone():
    result = extract_phones("010-1234-5678")
    assert len(result) == 1, f"got: {result}"
    assert "010" in result[0], f"got: {result}"


def test_extract_landline_phone():
    result = extract_phones("02-123-4567")
    assert len(result) == 1, f"got: {result}"


def test_no_phone_returns_empty():
    assert extract_phones("전화번호 없음") == []


def test_no_duplicate_phones():
    result = extract_phones("010-1234-5678 010-1234-5678")
    assert len(result) == 1, f"got: {result}"
