# TASKS.md — text-to-todo-streamlit

## 상태 표기
- `[ ]` TODO
- `[~]` IN_PROGRESS
- `[x]` DONE

> Codex는 항상 AGENTS.md → TASKS.md → SCHEMA.md 순서로 읽은 뒤 작업을 시작한다.
> 완료된 Task는 `[x]`로 변경하고, 발견된 이슈는 하단 **미결 이슈** 표에 기록한다.

---

## Phase 1: 구조 설계 (Claude Code 담당)

| 상태 | Task ID | 내용 |
|------|---------|------|
| [x] | TASK-001 | 폴더 구조 및 스텁 파일 생성 |
| [x] | TASK-002 | AGENTS.md 작성 |
| [x] | TASK-003 | TASKS.md 작성 |
| [ ] | TASK-004 | SCHEMA.md 작성 |
| [ ] | TASK-005 | PROJECT_STRUCTURE.md 작성 |
| [ ] | TASK-006 | TEST_PLAN.md 작성 |
| [ ] | TASK-007 | 스텁 파일 생성 (app.py, parser/*.py, services/*.py, utils/*.py) |
| [ ] | TASK-008 | samples/sample_01_youth_rent.txt 작성 |

---

## Phase 2: 텍스트 정제 + 연락처 + 기본 UI (Codex 담당)

### TASK-101 — text_cleaner.py 구현
**파일:** `parser/text_cleaner.py`
**함수:** `clean(raw_text: str) -> str`

구현 요건:
- `[Web발신]`, `[SMS발신]`, `[MMS]` 등 메타텍스트 제거
- 연속 공백·줄바꿈 정규화 (3줄 이상 → 2줄)
- 불필요한 마크다운 기호 제거 (`**`, `##` 등)
- 앞뒤 공백 strip

테스트 파일: `tests/test_text_cleaner.py`

완료 기준:
- `[Web발신]` 포함 입력 → 제거된 텍스트 반환
- 연속 빈 줄 정규화 확인

---

### TASK-102 — contact_parser.py 구현
**파일:** `parser/contact_parser.py`
**함수:** `extract_emails`, `extract_phones`

구현 요건:
- 이메일: `user@domain.tld` 형식 (복수 추출 가능)
- 전화번호: `010-0000-0000`, `02-000-0000`, `0000-0000` 형식 지원
- 중복 제거

테스트 파일: `tests/test_contact_parser.py`

완료 기준:
- `naru0219@mapo.go.kr` 추출됨
- 전화번호 다양한 형식 파싱됨

---

### TASK-103 — app.py 기본 UI 구현
**파일:** `app.py`

구현 요건:
- 원문 입력 `st.text_area`
- 기준일 `st.date_input` (기본값: 오늘)
- 실행 버튼
- 결과 JSON 또는 주요 필드 표시 (제목, 이메일, 전화 최소)
- orchestrator.parse() 호출

완료 기준:
- `streamlit run app.py` 실행 가능
- 예시 입력 시 이메일 추출 확인

---

## Phase 3: 카테고리 + 기관명 + 할일 요약 (Codex 담당)

### TASK-201 — category_classifier.py 구현
**파일:** `parser/category_classifier.py`
**함수:** `classify(text: str) -> str`

카테고리 목록:
- `보완요청`: 보완서류, 추가서류, 미비서류
- `제출요청`: 제출, 신청서, 서류 제출
- `납부요청`: 납부, 고지서, 요금, 수납
- `방문/예약`: 방문, 예약, 내원, 방문 접수
- `일반안내`: 위에 해당 없을 때 기본값

테스트 파일: `tests/test_category_classifier.py`

완료 기준:
- 예시 입력 → `보완요청` 분류됨

---

### TASK-202 — organization_parser.py 구현
**파일:** `parser/organization_parser.py`
**함수:** `extract_organization(text: str) -> Optional[str]`

지원 패턴 (우선순위 순):
1. `XX동주민센터`, `XX구청`, `XX시청`
2. `XX병원`, `XX의원`, `XX센터`
3. `XX학교`, `XX대학교`
4. `XX공단`, `XX공사`, `XX재단`
5. 발신자 서명 라인 (`안녕하십니까 XX입니다`)

테스트: `tests/test_organization_parser.py` (신규 생성)

완료 기준:
- `합정동주민센터` 추출됨

---

### TASK-203 — task_summary 생성 로직 추가
**파일:** `parser/orchestrator.py`

카테고리별 task_summary 템플릿:
- `보완요청` / `제출요청`: `보완서류를 준비하여 {submit_method}로 제출`
- `납부요청`: `기한 내 해당 금액을 납부`
- `방문/예약`: `지정 일정에 방문하여 절차 진행`
- `일반안내`: 첫 문장 요약 또는 `내용을 확인하고 필요한 조치를 취할 것`

완료 기준:
- 예시 입력 → `보완서류를 준비하여 이메일로 제출` 생성됨

---

## Phase 4: 날짜 파서 (Codex 담당)

### TASK-301 — date_parser.py 구현
**파일:** `parser/date_parser.py`
**함수:** `extract_deadline(text, base_date) -> Optional[str]`, `get_parse_log() -> list[str]`

지원 날짜 형식 (우선순위 순):
1. `2026.04.17까지` — 완전 절대일자
2. `4월 17일(금)까지` — 월일 표현 (연도는 base_date 기준 추론)
3. `04/17까지` — 슬래시 형식
4. `문자 수신 후 14일 이내` — 상대일자 (base_date + N일)
5. `이번 주 금요일까지` — 요일 기반 상대일자
6. `N일 이내`, `N일 후` — 일수 기반 상대일자

내부 저장 형식: `YYYY-MM-DD`
불명확한 경우: `None` 반환 (앱이 죽으면 안 됨)
parse_logs: 어떤 룰이 적용됐는지 기록

테스트 파일: `tests/test_date_parser.py`

완료 기준:
- `base_date=2026-04-15` + `4월 17일(금)까지` → `2026-04-17`
- 절대일자/상대일자 테스트 케이스 각 3개 이상 통과
- 오인식 입력에서 None 반환, 앱 미종료

---

## Phase 5: 체크리스트 파서 (Codex 담당)

### TASK-401 — checklist_parser.py 구현
**파일:** `parser/checklist_parser.py`
**함수:** `extract_checklist(text: str) -> list[str]`

섹션 트리거 키워드: `보완서류`, `제출서류`, `준비물`, `필수서류`, `아래 서류`

지원 목록 기호:
- `-` 대시
- `•` 불릿
- `1.` `2.` 번호 목록

특수 처리:
- `부 기준, 모 기준의 가족관계증명서(상세)` → 2개 항목으로 분리
- 조건문 (`자가 아닐 경우`, `미해당 시 제외`) → 괄호 안 조건으로 보존
- 중복 항목 제거
- 빈 항목 제거

테스트 파일: `tests/test_checklist_parser.py`

완료 기준:
- 예시 입력에서 체크리스트 4개 항목 추출
- `부 기준`/`모 기준` 분리 확인
- 조건부 문구 보존 확인

---

## Phase 6: 제목 생성 + 메모 조립 (Codex 담당)

### TASK-501 — title_builder.py 구현
**파일:** `parser/title_builder.py`
**함수:** `build_title(text, category, organization) -> str`

우선순위:
1. 텍스트 내 `[대괄호 제목]` 존재 시 → 제목 추출 + 제출방법 조합
2. 없을 경우 → `{기관명} {카테고리키워드} {제출방법}` 조합
3. 최대 20자 권장 (초과 시 그대로 두되 로그 기록)

예시: `[청년월세 신청서류 보완요청]` + 이메일 제출 → `청년월세 신청서류 메일발송`

테스트: `tests/test_title_builder.py` (신규 생성)

---

### TASK-502 — memo_builder.py 구현
**파일:** `parser/memo_builder.py`
**함수:** `build_memo(organization, emails, phones, conditions, submit_method) -> str`

조합 형식:
```
{organization} / {submit_method} / {email} / {phone}
조건: {conditions}
```
- 없는 필드는 생략
- 메모 전체 100자 이내 권장

---

### TASK-503 — orchestrator.py 최종 연결
**파일:** `parser/orchestrator.py`

모든 모듈 호출 순서:
1. `text_cleaner.clean()`
2. `contact_parser.extract_emails()` / `extract_phones()`
3. `category_classifier.classify()`
4. `organization_parser.extract_organization()`
5. `date_parser.extract_deadline()`
6. `checklist_parser.extract_checklist()`
7. `title_builder.build_title()`
8. `memo_builder.build_memo()`
9. `task_summary` 생성
10. `ParseResult` 조립 후 반환

테스트: `tests/test_orchestrator.py`

완료 기준:
- 예시 입력 → ParseResult 모든 필드 채워짐
- 기대 출력과 80% 이상 일치

---

## Phase 7: 편집 UI + 다운로드 + 히스토리 (Codex 담당)

### TASK-601 — app.py 결과 편집 UI
**파일:** `app.py`

편집 가능 필드:
- 제목 (`st.text_input`)
- 기한 (`st.date_input`)
- 할일 요약 (`st.text_input`)
- 카테고리 (`st.selectbox`)
- 기관명 (`st.text_input`)
- 메모 (`st.text_area`)
- 체크리스트 (항목별 `st.text_input` + 삭제 버튼 + 추가 버튼)

원문 / 결과 비교: `st.columns(2)` 또는 expander 활용

완료 기준:
- 사용자가 결과 편집 후 다운로드 가능

---

### TASK-602 — export_service.py 구현
**파일:** `services/export_service.py`

출력 형식:
- TXT: 필드명: 값 형식, 체크리스트는 `- 항목` 형식
- JSON: `json.dumps(result.to_dict(), ensure_ascii=False, indent=2)`
- CSV: 단일 행, 체크리스트는 세미콜론 구분

`st.download_button`과 연동

완료 기준:
- 3가지 형식 모두 다운로드 가능
- 다운로드 파일 내용이 결과와 일치

---

### TASK-603 — history_service.py 구현
**파일:** `services/history_service.py`

요건:
- `st.session_state["history"]` 기반 (최대 10개)
- 히스토리 패널에서 이전 결과 선택 가능
- 선택 시 편집 폼에 결과 반영

완료 기준:
- 여러 번 파싱 후 히스토리에서 선택 가능

---

## Phase 8: 디버그 모드 + 샘플 (Codex 담당)

### TASK-701 — 디버그 모드
**파일:** `app.py`

요건:
- 사이드바 또는 하단 체크박스로 디버그 모드 ON/OFF
- 활성화 시 `parse_logs` expander로 표시
- 각 로그 항목: `[모듈명] 적용룰: {설명}` 형식

---

### TASK-702 — sample_service.py + 샘플 연동
**파일:** `services/sample_service.py`, `samples/sample_01_youth_rent.txt`

요건:
- `get_samples() -> dict[str, str]` (이름 → 텍스트)
- app.py에서 selectbox로 샘플 선택 → 텍스트에어리어 자동 채움

---

## Phase 9: 최종 리뷰 (Claude Code 담당)

| 상태 | Task ID | 내용 |
|------|---------|------|
| [ ] | TASK-801 | parser 책임 분리 검수 |
| [ ] | TASK-802 | app.py 비대화 여부 점검 |
| [ ] | TASK-803 | 테스트 커버리지 최소 타당성 점검 |
| [ ] | TASK-804 | MVP 배포 가능 / 보완 후 배포 판정 |
| [ ] | TASK-805 | 후속 고도화 목록 정리 (Google Tasks 연동 등) |

---

## 미결 이슈 / TODO

_(구현 중 발견된 이슈를 여기에 기록한다)_

| 번호 | 내용 | 파일 | 우선순위 | 등록일 |
|------|------|------|---------|--------|
|      |      |      |         |        |

---

## 예시 입력 / 기대 출력

### 입력 (base_date: 2026-04-15)
```
[Web발신]
[청년월세 신청서류 보완요청]

안녕하십니까 합정동주민센터입니다.
신청하신 청년월세 보완서류 관련하여 연락드렸습니다.
4월 17일(금)까지 아래 서류를 메일로 보내주시기 바랍니다.

보완서류
-부 기준, 모 기준의 가족관계증명서(상세)-주민등록번호 뒷자리 공개(총 2장)
-통장사본
-부모님 거주지 자가 아닐 경우, 부모님 거주지 임대차계약서

naru0219@mapo.go.kr
```

### 기대 출력
```
title:        청년월세 신청서류 메일발송
deadline:     2026-04-17
task_summary: 보완서류를 준비하여 이메일로 제출
category:     보완요청
organization: 합정동주민센터
memo:         합정동주민센터 / 메일 제출 / naru0219@mapo.go.kr
emails:       ["naru0219@mapo.go.kr"]
phones:       []
checklist:
  - 부 기준 가족관계증명서(상세, 주민등록번호 뒷자리 공개)
  - 모 기준 가족관계증명서(상세, 주민등록번호 뒷자리 공개)
  - 통장사본
  - 부모님 거주지 임대차계약서 (부모님 거주지가 자가 아닐 경우)
```
