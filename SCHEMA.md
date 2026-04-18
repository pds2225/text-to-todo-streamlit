# SCHEMA.md — text-to-todo-streamlit

## ParseResult 데이터 스키마

> 전체 파싱 결과를 담는 핵심 데이터 구조.
> 정의 위치: `schemas/result_schema.py`

---

## 필드 정의

| 필드명 | 타입 | 기본값 | 설명 |
|--------|------|--------|------|
| `title` | `str` | `""` | 실행형 제목 (예: `청년월세 신청서류 메일발송`) |
| `deadline` | `Optional[str]` | `None` | 기한 (`YYYY-MM-DD` 형식 또는 None) |
| `task_summary` | `str` | `""` | 행동형 1문장 요약 (예: `보완서류를 준비하여 이메일로 제출`) |
| `category` | `str` | `"일반안내"` | 분류: `보완요청` / `제출요청` / `납부요청` / `방문/예약` / `일반안내` |
| `organization` | `Optional[str]` | `None` | 기관명 (예: `합정동주민센터`) |
| `memo` | `str` | `""` | 메모 (이메일, 전화, 제출방법, 조건 조합) |
| `emails` | `list[str]` | `[]` | 추출된 이메일 주소 목록 |
| `phones` | `list[str]` | `[]` | 추출된 전화번호 목록 |
| `checklist` | `list[str]` | `[]` | 체크리스트 항목 목록 |
| `raw_text` | `str` | `""` | 원문 텍스트 (변경 없음) |
| `base_date` | `str` | `""` | 기준일 (`YYYY-MM-DD`, 상대 날짜 계산 기준) |
| `parse_logs` | `list[str]` | `[]` | 디버그용 파싱 로그 (어떤 룰이 적용됐는지) |

---

## category 허용값

```python
CATEGORIES = ["보완요청", "제출요청", "납부요청", "방문/예약", "일반안내"]
```

| 값 | 의미 | 예시 키워드 |
|----|------|------------|
| `보완요청` | 서류 보완 요청 | 보완서류, 추가서류, 미비서류 |
| `제출요청` | 서류/신청서 제출 | 제출, 신청서, 서류 제출 |
| `납부요청` | 요금/금액 납부 | 납부, 고지서, 요금, 수납 |
| `방문/예약` | 방문 또는 예약 | 방문, 예약, 내원, 방문 접수 |
| `일반안내` | 그 외 기본값 | — |

---

## deadline 형식 규칙

- 저장 형식: `YYYY-MM-DD` (예: `2026-04-17`)
- 파싱 불가 또는 불명확 → `None` 반환
- 연도 불명확 시 `base_date`의 연도 사용
- 기준일보다 과거 날짜 → 다음 해로 추론 (예외: 명시적 연도가 있으면 그대로)

---

## parse_logs 형식

```
[text_cleaner] 메타텍스트 제거: [Web발신]
[date_parser] 룰 적용: 월일 표현 (base_date 연도 사용) → 2026-04-17
[checklist_parser] 섹션 감지: '보완서류' 키워드 → 4개 항목 추출
[category_classifier] 키워드 매칭: '보완서류' → 보완요청
```

---

## dataclass 정의 (schemas/result_schema.py 동일 내용)

```python
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class ParseResult:
    title: str = ""
    deadline: Optional[str] = None
    task_summary: str = ""
    category: str = "일반안내"
    organization: Optional[str] = None
    memo: str = ""
    emails: list[str] = field(default_factory=list)
    phones: list[str] = field(default_factory=list)
    checklist: list[str] = field(default_factory=list)
    raw_text: str = ""
    base_date: str = ""
    parse_logs: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        ...
```

---

## 예시 완성 결과

```json
{
  "title": "청년월세 신청서류 메일발송",
  "deadline": "2026-04-17",
  "task_summary": "보완서류를 준비하여 이메일로 제출",
  "category": "보완요청",
  "organization": "합정동주민센터",
  "memo": "합정동주민센터 / 메일 제출 / naru0219@mapo.go.kr",
  "emails": ["naru0219@mapo.go.kr"],
  "phones": [],
  "checklist": [
    "부 기준 가족관계증명서(상세, 주민등록번호 뒷자리 공개)",
    "모 기준 가족관계증명서(상세, 주민등록번호 뒷자리 공개)",
    "통장사본",
    "부모님 거주지 임대차계약서 (부모님 거주지가 자가 아닐 경우)"
  ],
  "raw_text": "...",
  "base_date": "2026-04-15",
  "parse_logs": [
    "[text_cleaner] 메타텍스트 제거: [Web발신]",
    "[date_parser] 룰 적용: 월일 표현 → 2026-04-17",
    "[checklist_parser] 섹션 감지: '보완서류' → 4개 항목",
    "[category_classifier] '보완서류' → 보완요청"
  ]
}
```
