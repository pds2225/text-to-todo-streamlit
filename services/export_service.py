"""
ParseResult를 다운로드 가능한 형식으로 변환.
파일 직접 저장 금지 — Streamlit download_button에서 처리.
"""
from __future__ import annotations
import json
import csv
import io

from schemas.result_schema import ParseResult

# TODO: TASK-602 — 아래 함수들을 구현할 것


def to_txt(result: ParseResult) -> str:
    """TXT 형식 문자열 반환.

    형식:
        제목: ...
        기한: ...
        할일: ...
        카테고리: ...
        기관명: ...
        메모: ...
        체크리스트:
        - 항목1
        - 항목2
    """
    # TODO: 구현
    lines = [
        f"제목: {result.title}",
        f"기한: {result.deadline or '미정'}",
        f"할일: {result.task_summary}",
        f"카테고리: {result.category}",
        f"기관명: {result.organization or ''}",
        f"메모: {result.memo}",
        "",
        "체크리스트:",
    ]
    for item in result.checklist:
        lines.append(f"- {item}")
    return "\n".join(lines)


def to_json(result: ParseResult) -> str:
    """JSON 형식 문자열 반환."""
    # TODO: 구현
    return json.dumps(result.to_dict(), ensure_ascii=False, indent=2)


def to_csv(result: ParseResult) -> str:
    """CSV 형식 문자열 반환 (단일 행, 체크리스트는 세미콜론 구분).

    TODO: 구현
    """
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "제목", "기한", "할일", "카테고리", "기관명", "메모",
        "이메일", "전화", "체크리스트"
    ])
    writer.writerow([
        result.title,
        result.deadline or "",
        result.task_summary,
        result.category,
        result.organization or "",
        result.memo,
        ";".join(result.emails),
        ";".join(result.phones),
        ";".join(result.checklist),
    ])
    return output.getvalue()
