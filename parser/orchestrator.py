"""
파싱 파이프라인 조율자.
외부에서는 parse() 만 호출한다.
"""
from __future__ import annotations

from datetime import date
from typing import Optional

from schemas.result_schema import ParseResult
from parser import text_cleaner
from parser import contact_parser
from parser import category_classifier
from parser import organization_parser
from parser import date_parser
from parser import checklist_parser
from parser import title_builder
from parser import memo_builder


def parse(raw_text: str, base_date: date) -> ParseResult:
    """원문 텍스트를 받아 ParseResult를 반환하는 메인 진입점."""
    result = ParseResult(raw_text=raw_text, base_date=str(base_date))

    if not raw_text or not raw_text.strip():
        return result

    # 1. 텍스트 정제
    cleaned = text_cleaner.clean(raw_text)
    result.parse_logs.append("[text_cleaner] 정제 완료")

    # 2. 연락처 추출
    result.emails = contact_parser.extract_emails(cleaned)
    result.phones = contact_parser.extract_phones(cleaned)
    if result.emails:
        result.parse_logs.append(f"[contact_parser] 이메일 {len(result.emails)}개 추출")
    if result.phones:
        result.parse_logs.append(f"[contact_parser] 전화번호 {len(result.phones)}개 추출")

    # 3. 카테고리 분류
    result.category = category_classifier.classify(cleaned)
    result.parse_logs.append(f"[category_classifier] → {result.category}")

    # 4. 기관명 추출
    result.organization = organization_parser.extract_organization(cleaned)
    if result.organization:
        result.parse_logs.append(f"[organization_parser] → {result.organization}")

    # 5. 날짜 파싱
    result.deadline = date_parser.extract_deadline(cleaned, base_date)
    result.parse_logs.extend(date_parser.get_parse_log())

    # 6. 체크리스트 추출
    result.checklist = checklist_parser.extract_checklist(cleaned)
    if result.checklist:
        result.parse_logs.append(f"[checklist_parser] {len(result.checklist)}개 항목 추출")

    # 7. 제출 방법 감지 (title/memo 공용)
    submit_method: Optional[str] = title_builder._detect_submit_method(cleaned)

    # 8. 제목 생성
    result.title = title_builder.build_title(cleaned, result.category, result.organization)
    result.parse_logs.append(f"[title_builder] → {result.title}")

    # 9. 메모 조합
    result.memo = memo_builder.build_memo(
        result.organization,
        result.emails,
        result.phones,
        conditions=[],
        submit_method=submit_method,
    )

    # 10. 할일 요약 생성
    result.task_summary = _build_task_summary(result.category, submit_method)
    result.parse_logs.append(f"[orchestrator] task_summary → {result.task_summary}")

    return result


def _build_task_summary(category: str, submit_method: Optional[str]) -> str:
    """카테고리 기반 행동형 1문장 요약 생성."""
    if submit_method:
        method_str = f"{submit_method}로"
    else:
        # 제출 계열인데 방법 미감지 시 기본값
        method_str = "지정된 방법으로"

    templates: dict[str, str] = {
        "보완요청": f"보완서류를 준비하여 {method_str} 제출",
        "제출요청": f"서류를 준비하여 {method_str} 제출",
        "납부요청": "기한 내 해당 금액 납부",
        "방문/예약": "지정 일정에 방문하여 절차 진행",
        "일반안내": "내용 확인 후 필요한 조치 취하기",
    }
    return templates.get(category, "내용 확인 후 필요한 조치 취하기")
