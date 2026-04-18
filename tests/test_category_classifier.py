"""테스트: parser/category_classifier.py — TASK-201"""
import pytest
from parser.category_classifier import classify


def test_classify_supplement_request():
    assert classify("보완서류를 제출해주세요") == "보완요청"


def test_classify_submit_request():
    assert classify("서류를 제출해주시기 바랍니다") == "제출요청"


def test_classify_payment_request():
    assert classify("납부 기한을 확인하세요") == "납부요청"


def test_classify_visit():
    assert classify("방문하여 접수해주세요") == "방문/예약"


def test_classify_general_default():
    assert classify("안녕하세요. 알림 드립니다.") == "일반안내"


def test_empty_string_returns_default():
    assert classify("") == "일반안내"


def test_priority_supplement_over_submit():
    # 보완요청이 제출요청보다 우선순위 높음
    result = classify("보완서류를 제출해주세요")
    assert result == "보완요청", f"got: {result}"
