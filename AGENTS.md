# AGENTS.md — text-to-todo-streamlit

## 프로젝트 개요

비정형 텍스트(문자, 카카오톡, 웹공지, 이메일 본문)를 붙여넣으면
**제목, 기한, 할일 요약, 체크리스트, 메모, 연락처**를 자동 추출하는
규칙 기반 Streamlit MVP.

- LLM 의존 없이 regex + 규칙 기반으로 동작
- 외부 API, DB, OCR 없음
- 단일 Streamlit 페이지

---

## 에이전트 역할 구분

### Claude Code — 구조 설계 담당
- 폴더 구조 설계 및 유지
- 파일 역할 및 함수 시그니처 정의
- 문서 작성 (AGENTS.md, TASKS.md, SCHEMA.md 등)
- 구조 리뷰 및 리팩터링 제안
- **구현 로직 최소화 — 뼈대/명세 중심**

### Codex — 구현 담당
- 이 파일(AGENTS.md), TASKS.md, SCHEMA.md를 **반드시 먼저** 읽고 따른다
- TASKS.md에 지정된 Task만 구현한다
- 완료 후 관련 테스트를 작성한다
- 구현 완료 시 변경 파일 목록 + 실행 방법을 요약한다

---

## 폴더 구조

```
text-to-todo-streamlit/
├─ app.py                     # Streamlit 메인 앱 (UI 전용, 파싱 로직 포함 금지)
├─ requirements.txt
├─ AGENTS.md                  # 이 파일
├─ TASKS.md                   # Task 목록 및 완료 기준
├─ SCHEMA.md                  # 데이터 스키마 정의
├─ PROJECT_STRUCTURE.md       # 파일별 역할 상세 설명
├─ TEST_PLAN.md                # 테스트 전략 및 케이스
├─ parser/
│  ├─ __init__.py
│  ├─ orchestrator.py         # 전체 파싱 흐름 조율 (각 모듈 호출)
│  ├─ text_cleaner.py         # 원문 정제 (메타텍스트 제거, 공백 정리)
│  ├─ title_builder.py        # 실행형 제목 생성
│  ├─ date_parser.py          # 날짜 표현 → YYYY-MM-DD
│  ├─ checklist_parser.py     # 목록 항목 추출 및 분리
│  ├─ contact_parser.py       # 이메일/전화번호 추출
│  ├─ category_classifier.py  # 텍스트 카테고리 분류
│  ├─ memo_builder.py         # 메모 문자열 조합
│  └─ organization_parser.py  # 기관명 추출
├─ schemas/
│  └─ result_schema.py        # ParseResult dataclass 정의
├─ services/
│  ├─ export_service.py       # TXT/JSON/CSV 다운로드 생성
│  ├─ history_service.py      # 세션 내 히스토리 관리
│  └─ sample_service.py       # 샘플 텍스트 제공
├─ utils/
│  ├─ regex_patterns.py       # 공통 정규식 상수
│  ├─ formatter.py            # 출력 포맷 헬퍼
│  └─ constants.py            # 전역 상수 (카테고리 목록 등)
├─ tests/
│  ├─ test_text_cleaner.py
│  ├─ test_contact_parser.py
│  ├─ test_date_parser.py
│  ├─ test_checklist_parser.py
│  ├─ test_title_builder.py
│  ├─ test_category_classifier.py
│  └─ test_orchestrator.py
└─ samples/
   └─ sample_01_youth_rent.txt
```

---

## 핵심 함수 시그니처

> 함수명과 인자를 임의로 변경하지 말 것. 변경 필요 시 AGENTS.md를 먼저 수정한다.

### parser/orchestrator.py
```python
def parse(raw_text: str, base_date: date) -> ParseResult:
    """원문 텍스트를 받아 ParseResult를 반환하는 메인 진입점."""
```

### parser/text_cleaner.py
```python
def clean(raw_text: str) -> str:
    """메타텍스트 제거, 공백 정리, 줄바꿈 정규화."""
```

### parser/date_parser.py
```python
def extract_deadline(text: str, base_date: date) -> Optional[str]:
    """날짜 표현 추출 → YYYY-MM-DD 또는 None."""

def get_parse_log() -> list[str]:
    """마지막 파싱에서 적용된 룰 로그 반환."""
```

### parser/checklist_parser.py
```python
def extract_checklist(text: str) -> list[str]:
    """목록 항목 추출, 분리, 중복 제거."""
```

### parser/contact_parser.py
```python
def extract_emails(text: str) -> list[str]:
    """이메일 주소 추출."""

def extract_phones(text: str) -> list[str]:
    """전화번호 추출 (하이픈/공백 형식 포함)."""
```

### parser/category_classifier.py
```python
def classify(text: str) -> str:
    """반환값: '제출요청' | '보완요청' | '납부요청' | '방문/예약' | '일반안내'"""
```

### parser/organization_parser.py
```python
def extract_organization(text: str) -> Optional[str]:
    """기관명 추출 또는 None."""
```

### parser/title_builder.py
```python
def build_title(text: str, category: str, organization: Optional[str]) -> str:
    """실행형 제목 생성."""
```

### parser/memo_builder.py
```python
def build_memo(
    organization: Optional[str],
    emails: list[str],
    phones: list[str],
    conditions: list[str],
    submit_method: Optional[str],
) -> str:
    """메모 문자열 조합."""
```

### services/export_service.py
```python
def to_txt(result: ParseResult) -> str:
    """TXT 형식 문자열 반환."""

def to_json(result: ParseResult) -> str:
    """JSON 형식 문자열 반환."""

def to_csv(result: ParseResult) -> str:
    """CSV 형식 문자열 반환."""
```

### services/history_service.py
```python
def add_to_history(session_state: Any, result: ParseResult) -> None:
def get_history(session_state: Any) -> list[ParseResult]:
def clear_history(session_state: Any) -> None:
```

---

## 데이터 스키마 요약

> 전체 정의는 SCHEMA.md 참조

| 필드 | 타입 | 설명 |
|------|------|------|
| title | str | 실행형 제목 |
| deadline | Optional[str] | YYYY-MM-DD 또는 None |
| task_summary | str | 행동형 1문장 요약 |
| category | str | 제출요청 / 보완요청 / 납부요청 / 방문·예약 / 일반안내 |
| organization | Optional[str] | 기관명 |
| memo | str | 이메일/전화/조건 조합 메모 |
| emails | list[str] | 추출된 이메일 목록 |
| phones | list[str] | 추출된 전화번호 목록 |
| checklist | list[str] | 체크리스트 항목 |
| raw_text | str | 원문 (변경 없음) |
| base_date | str | 기준일 YYYY-MM-DD |
| parse_logs | list[str] | 디버그용 파싱 로그 |

---

## 제약 및 금지사항

| 항목 | 허용 | 금지 |
|------|------|------|
| LLM 사용 | 향후 확장 고려 설계만 가능 | MVP에서 실제 호출 금지 |
| 외부 API | — | 금지 |
| DB (SQLite 포함) | — | 금지 |
| OCR | — | 금지 |
| Google 연동 | — | 금지 |
| 폴더 구조 변경 | Claude Code 승인 후 가능 | Codex 임의 변경 금지 |
| 함수명 변경 | Claude Code 승인 후 가능 | Codex 임의 변경 금지 |
| requirements 추가 | 꼭 필요한 경우만 | 불필요한 패키지 추가 금지 |

---

## Codex 작업 시작 체크리스트

1. [ ] AGENTS.md 확인
2. [ ] TASKS.md에서 현재 Task 확인
3. [ ] SCHEMA.md에서 ParseResult 구조 확인
4. [ ] 지정된 함수 시그니처 유지 확인
5. [ ] 구현 → 테스트 작성 → 요약 순서로 진행
