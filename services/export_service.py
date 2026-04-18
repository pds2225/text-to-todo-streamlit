"""
ParseResult를 다운로드 가능한 형식으로 변환.
"""
from __future__ import annotations
import json
import csv
import io

from schemas.result_schema import ParseResult


def to_txt(result: ParseResult) -> str:
    """TXT 형식 문자열 반환."""
    deadline_str = result.deadline or "미정"
    if result.deadline and result.deadline_time:
        deadline_str = f"{result.deadline} {result.deadline_time}"

    lines = [
        f"제목: {result.title}",
        f"리스트: {result.target_list}",
        f"기한: {deadline_str}",
        f"할일: {result.task_summary}",
        f"카테고리: {result.category}",
        f"기관명: {result.organization or ''}",
        f"메모: {result.memo}",
    ]

    if result.urls:
        lines.append("\n[참고 URL]")
        for url in result.urls:
            lines.append(f"  {url}")

    if result.checklist:
        lines.append("\n[서브태스크 (Google Tasks 하위 항목)]")
        for item in result.checklist:
            lines.append(f"  ☐ {item}")

    return "\n".join(lines)


def to_json(result: ParseResult) -> str:
    """JSON 형식 문자열 반환."""
    return json.dumps(result.to_dict(), ensure_ascii=False, indent=2)


def to_csv(result: ParseResult) -> str:
    """CSV 형식 문자열 반환 (단일 행)."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "제목", "리스트", "기한", "시간", "할일", "카테고리",
        "기관명", "메모", "이메일", "전화", "URL", "서브태스크"
    ])
    writer.writerow([
        result.title,
        result.target_list,
        result.deadline or "",
        result.deadline_time or "",
        result.task_summary,
        result.category,
        result.organization or "",
        result.memo,
        ";".join(result.emails),
        ";".join(result.phones),
        ";".join(result.urls),
        ";".join(result.checklist),
    ])
    return output.getvalue()
