import re

EMAIL_PATTERN = re.compile(
    r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"
)

PHONE_PATTERN = re.compile(
    r"(0\d{1,2})[-\s]?(\d{3,4})[-\s]?(\d{4})"
)

# URL — 개선4
URL_PATTERN = re.compile(
    r"https?://[^\s\n\]）)>]+"
)

# 2026.04.17 / 2026-04-17 / 2026/04/17
DATE_ABSOLUTE_PATTERN = re.compile(
    r"(\d{4})[.\-/](\d{1,2})[.\-/](\d{1,2})"
)

# 2025년 12월 31일 / 2026년 4월 17일
DATE_YEAR_MONTH_DAY_PATTERN = re.compile(
    r"(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일"
)

# 4월 17일 / 4월17일(금) 등
DATE_MONTH_DAY_PATTERN = re.compile(
    r"(\d{1,2})월\s*(\d{1,2})일(?:\([월화수목금토일]\))?"
)

# 04/17 또는 4/17 — \b는 한글 앞에서 오작동하므로 digit lookaround 사용
DATE_SLASH_MONTH_DAY_PATTERN = re.compile(
    r"(?<!\d)(\d{1,2})/(\d{1,2})(?!\d)"
)

# N일 이내 / 수신 후 N일
DATE_RELATIVE_DAYS_PATTERN = re.compile(
    r"(?:수신|접수|발송|문자)\s*후?\s*(\d+)일\s*(?:이내|이전|안에)?"
)

# 이번 주 금요일 / 이번 주 월요일 등
DATE_WEEKDAY_PATTERN = re.compile(
    r"이번\s*주\s*([월화수목금토일])요일"
)

WEEKDAY_MAP: dict[str, int] = {
    "월": 0, "화": 1, "수": 2, "목": 3, "금": 4, "토": 5, "일": 6
}

# 시간 — 오전/오후 N시 M분, 오전/오후 N:MM — 개선2
TIME_AMPM_PATTERN = re.compile(
    r"(오전|오후)\s*(\d{1,2})(?:시|:)\s*(\d{2})?"
)

# 24시간 표기 HH:MM (단독)
TIME_24H_PATTERN = re.compile(
    r"(?<!\d)(\d{1,2}):(\d{2})(?!\d)"
)

# [대괄호 제목] 추출
BRACKET_TITLE_PATTERN = re.compile(r"\[([^\]]{2,40})\]")

# 목록 기호
LIST_DASH_PATTERN = re.compile(r"^\s*[-•·]\s*(.+)$", re.MULTILINE)
LIST_NUMBERED_PATTERN = re.compile(r"^\s*\d+[.)]\s*(.+)$", re.MULTILINE)
