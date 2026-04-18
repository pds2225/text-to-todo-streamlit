"""
샘플 텍스트 제공 서비스.
samples/ 디렉토리의 .txt 파일을 로드한다.
"""
from __future__ import annotations
from pathlib import Path

_SAMPLES_DIR = Path(__file__).parent.parent / "samples"

# TODO: TASK-702 — 아래 함수를 구현할 것


def get_samples() -> dict[str, str]:
    """샘플 이름 → 텍스트 매핑 반환.

    Returns:
        {'샘플명': '텍스트 내용', ...}
        파일이 없으면 {}.

    구현 요건:
        - _SAMPLES_DIR의 *.txt 파일을 모두 로드
        - 파일명(확장자 제외)을 키로 사용
        - 읽기 실패한 파일은 건너뜀
    """
    # TODO: 구현
    samples: dict[str, str] = {}
    for path in sorted(_SAMPLES_DIR.glob("*.txt")):
        try:
            samples[path.stem] = path.read_text(encoding="utf-8")
        except OSError:
            pass
    return samples
