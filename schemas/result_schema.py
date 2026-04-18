from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
import json


@dataclass
class ParseResult:
    title: str = ""
    deadline: Optional[str] = None       # YYYY-MM-DD
    deadline_time: Optional[str] = None  # HH:MM (24h) — 개선2
    task_summary: str = ""
    category: str = "일반안내"
    target_list: str = "업무"            # 업무/업무(장기)/개인/짬짬이 — 개선1
    organization: Optional[str] = None
    memo: str = ""
    emails: list[str] = field(default_factory=list)
    phones: list[str] = field(default_factory=list)
    urls: list[str] = field(default_factory=list)    # 개선4
    checklist: list[str] = field(default_factory=list)  # Google Tasks 서브태스크 — 개선3
    raw_text: str = ""
    base_date: str = ""
    parse_logs: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "deadline": self.deadline,
            "deadline_time": self.deadline_time,
            "task_summary": self.task_summary,
            "category": self.category,
            "target_list": self.target_list,
            "organization": self.organization,
            "memo": self.memo,
            "emails": self.emails,
            "phones": self.phones,
            "urls": self.urls,
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
            deadline_time=data.get("deadline_time"),
            task_summary=data.get("task_summary", ""),
            category=data.get("category", "일반안내"),
            target_list=data.get("target_list", "업무"),
            organization=data.get("organization"),
            memo=data.get("memo", ""),
            emails=data.get("emails", []),
            phones=data.get("phones", []),
            urls=data.get("urls", []),
            checklist=data.get("checklist", []),
            raw_text=data.get("raw_text", ""),
            base_date=data.get("base_date", ""),
            parse_logs=data.get("parse_logs", []),
        )
