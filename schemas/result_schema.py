from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
import json


@dataclass
class ParseResult:
    title: str = ""
    deadline: Optional[str] = None  # YYYY-MM-DD
    task_summary: str = ""
    category: str = "일반안내"
    organization: Optional[str] = None
    memo: str = ""
    emails: list[str] = field(default_factory=list)
    phones: list[str] = field(default_factory=list)
    checklist: list[str] = field(default_factory=list)
    raw_text: str = ""
    base_date: str = ""  # YYYY-MM-DD
    parse_logs: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "deadline": self.deadline,
            "task_summary": self.task_summary,
            "category": self.category,
            "organization": self.organization,
            "memo": self.memo,
            "emails": self.emails,
            "phones": self.phones,
            "checklist": self.checklist,
            "raw_text": self.raw_text,
            "base_date": self.base_date,
            "parse_logs": self.parse_logs,
        }

    @classmethod
    def from_dict(cls, data: dict) -> ParseResult:
        return cls(
            title=data.get("title", ""),
            deadline=data.get("deadline"),
            task_summary=data.get("task_summary", ""),
            category=data.get("category", "일반안내"),
            organization=data.get("organization"),
            memo=data.get("memo", ""),
            emails=data.get("emails", []),
            phones=data.get("phones", []),
            checklist=data.get("checklist", []),
            raw_text=data.get("raw_text", ""),
            base_date=data.get("base_date", ""),
            parse_logs=data.get("parse_logs", []),
        )
