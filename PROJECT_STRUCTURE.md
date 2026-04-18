# PROJECT_STRUCTURE.md — text-to-todo-streamlit

## 파일별 역할 정의

> 각 파일의 단일 책임(Single Responsibility)을 명확히 한다.
> 이 범위를 벗어나는 코드는 해당 파일에 추가하지 않는다.

---

## 루트 파일

### app.py
**역할:** Streamlit UI 전용 진입점

**해야 할 것:**
- 사용자 입력 수집 (원문, 기준일)
- `orchestrator.parse()` 호출
- 결과 편집 UI 렌더링
- `export_service`, `history_service`, `sample_service` 호출

**하면 안 되는 것:**
- 직접 regex 실행 금지
- 파싱 로직 포함 금지
- 비즈니스 규칙 포함 금지

**의존:** `parser.orchestrator`, `services.*`, `schemas.result_schema`

---

### requirements.txt
**역할:** 최소 의존성 목록

포함 항목:
- `streamlit` — UI
- `pytest` — 테스트

포함하지 않는 것: LLM SDK, DB 드라이버, OCR 라이브러리

---

## parser/

### orchestrator.py
**역할:** 파싱 파이프라인 조율자

**해야 할 것:**
- `parse(raw_text, base_date) -> ParseResult` 한 함수만 외부 공개
- 각 parser 모듈을 순서에 맞게 호출
- ParseResult 조립 및 반환

**하면 안 되는 것:**
- 직접 regex 실행 금지
- UI 관련 코드 금지

**호출 순서:** `text_cleaner` → `contact_parser` → `category_classifier` → `organization_parser` → `date_parser` → `checklist_parser` → `title_builder` → `memo_builder`

---

### text_cleaner.py
**역할:** 원문 텍스트 정제

**해야 할 것:**
- `[Web발신]`, `[SMS발신]` 등 메타텍스트 제거
- 연속 공백/줄바꿈 정규화
- 마크다운 기호 제거

**하면 안 되는 것:**
- 의미 있는 텍스트 삭제 금지
- 파싱 로직 포함 금지

**입력:** raw str / **출력:** cleaned str

---

### date_parser.py
**역할:** 날짜 표현 → YYYY-MM-DD 변환

**해야 할 것:**
- 절대/상대 날짜 표현 인식
- `base_date` 기준 상대일 계산
- parse_logs에 적용 룰 기록
- 실패 시 None 반환 (예외 발생 금지)

**지원 형식:** 4월 17일(금)까지 / 2026.04.17 / 이번 주 금요일 / N일 이내

---

### checklist_parser.py
**역할:** 서류/항목 목록 추출

**해야 할 것:**
- 섹션 키워드(보완서류, 준비물 등) 이후 목록 감지
- `-`, `•`, `1.` 등 기호 처리
- 콤마로 연결된 복수 항목 분리
- 조건문을 항목 뒤 괄호로 보존

**하면 안 되는 것:**
- 섹션 외 본문의 일반 문장 목록화 금지

---

### contact_parser.py
**역할:** 이메일/전화번호 추출

**해야 할 것:**
- 복수 이메일 추출
- 복수 전화번호 추출 (다양한 형식)
- 중복 제거

**의존:** `utils.regex_patterns`

---

### category_classifier.py
**역할:** 텍스트 → 카테고리 분류

**해야 할 것:**
- 키워드 기반 분류
- 우선순위 순서 적용 (보완요청 > 제출요청 > 납부요청 > 방문/예약 > 일반안내)
- 기본값 `일반안내` 반환

**의존:** `utils.constants`

---

### organization_parser.py
**역할:** 기관명 추출

**해야 할 것:**
- 주민센터, 구청, 병원, 학교 등 패턴 매칭
- 발신자 서명 라인에서 추출
- 추출 불가 시 None 반환

---

### title_builder.py
**역할:** 실행형 제목 생성

**해야 할 것:**
- `[대괄호 제목]` 우선 추출
- 카테고리 + 제출방법 조합
- 20자 이내 권장

---

### memo_builder.py
**역할:** 메모 문자열 조합

**해야 할 것:**
- 기관명 / 이메일 / 전화 / 제출방법 / 조건문 조합
- 없는 필드 생략
- 100자 이내 권장

---

## schemas/

### result_schema.py
**역할:** ParseResult dataclass 단일 정의

**해야 할 것:**
- 모든 필드 기본값 포함
- `to_dict()` 메서드
- `from_dict()` 클래스 메서드 (선택)

**하면 안 되는 것:**
- 파싱 로직 포함 금지
- I/O 로직 포함 금지

---

## services/

### export_service.py
**역할:** ParseResult → 다운로드 파일 생성

**해야 할 것:**
- `to_txt(result) -> str`
- `to_json(result) -> str`
- `to_csv(result) -> str`

**하면 안 되는 것:**
- 파일 직접 저장 금지 (Streamlit download_button에서 처리)

---

### history_service.py
**역할:** 세션 내 파싱 히스토리 관리

**해야 할 것:**
- `st.session_state["history"]` 기반 최대 10개 유지
- add / get / clear 기능

**하면 안 되는 것:**
- 디스크/DB 저장 금지

---

### sample_service.py
**역할:** 샘플 텍스트 제공

**해야 할 것:**
- `get_samples() -> dict[str, str]` (이름 → 텍스트)
- `samples/` 디렉토리에서 로드

---

## utils/

### constants.py
**역할:** 전역 상수 저장소

포함: CATEGORIES, SUBMIT_METHODS, META_TEXT_PATTERNS

### regex_patterns.py
**역할:** 공통 정규식 패턴 상수

포함: EMAIL_PATTERN, PHONE_PATTERN, DATE_* 패턴, LIST_ITEM_PATTERN

### formatter.py
**역할:** 출력 포맷 헬퍼 함수

포함: `format_checklist_text`, `format_result_summary`

---

## tests/

각 테스트 파일은 대응하는 parser 모듈만 테스트한다.
테스트 간 의존성을 최소화하고, 외부 서비스 없이 실행 가능해야 한다.

---

## samples/

수동으로 만든 예시 원문 텍스트 파일. `sample_service.py`가 로드한다.
OCR 결과나 실제 메시지를 익명화한 버전을 저장한다.

---

## 의존성 흐름 요약

```
app.py
  └─ orchestrator.parse()
       ├─ text_cleaner.clean()
       ├─ contact_parser.extract_*()      ← utils.regex_patterns
       ├─ category_classifier.classify()  ← utils.constants
       ├─ organization_parser.extract_*()
       ├─ date_parser.extract_deadline()  ← utils.regex_patterns
       ├─ checklist_parser.extract_*()
       ├─ title_builder.build_title()
       └─ memo_builder.build_memo()
            └─ returns ParseResult        ← schemas.result_schema

app.py
  ├─ export_service.to_txt/json/csv()
  ├─ history_service.add/get/clear()
  └─ sample_service.get_samples()
```
