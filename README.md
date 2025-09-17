# 미연시 게임 엔진

이 저장소는 간단한 텍스트 기반 미연시(미소녀 연애 시뮬레이션) 게임을 만들고 실행할 수 있는 파이썬 엔진을 제공합니다. JSON 형식으로 작성된 시나리오 파일을 로드하여 분기형 스토리를 진행할 수 있습니다.

## 설치 및 실행 방법

1. 의존성 설치

   ```bash
   pip install -r requirements.txt  # pytest를 사용한 테스트 실행을 원할 경우
   ```

2. 샘플 스토리 실행

   ```bash
   python -m meva.cli stories/sample_story.json
   ```

## 스토리 파일 구조

스토리 JSON 파일은 다음과 같은 구조를 가집니다.

```json
{
  "title": "게임 제목",
  "opening_scene": "첫번째로 시작할 씬 ID",
  "characters": [
    {"name": "캐릭터 이름", "description": "설명"}
  ],
  "scenes": [
    {
      "id": "씬 ID",
      "description": "씬 설명",
      "dialogues": [
        {"speaker": "말하는 사람", "text": "대사"}
      ],
      "choices": [
        {"text": "선택지 설명", "next_scene": "다음에 이동할 씬 ID"}
      ],
      "next_scene": "선택지가 없을 때 이동할 다음 씬 ID (혹은 null)"
    }
  ]
}
```

`choices`가 비어 있고 `next_scene`가 `null`이면 해당 씬에서 스토리가 종료됩니다.

## 테스트 실행

```bash
pytest
```

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.