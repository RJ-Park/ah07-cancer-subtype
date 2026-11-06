# AI 작업 지침

이 레포에서 코드를 작성하거나 수정하기 전에 반드시 `AI_RULES.md`를 읽고, 그 안의 규칙(데이터 누수 금지, 재현성, 레포 구조와 공통 함수, 협업 규칙)을 그대로 따르세요.

- 핵심: 학습하는 변환은 fold의 학습 부분에만 fit (sklearn Pipeline + `src/validation.py`의 `run_cv`), test는 형식 확인과 최종 추론에만, train과 test를 합치지 않기.
- 사용자의 담당 폴더(`notebooks/이니셜_역할/`)와 담당 src 파일만 수정하세요. 담당이 불분명하면 먼저 물어보세요.
- 팀 운영(역할, 일정): `docs/team_plan.md` / 시작 방법: `README.md`
