# Slack 개인 비서 봇

이 프로젝트는 Slack에서 멘션을 통해 사용자와 상호작용하는 개인 비서 봇입니다. Anthropic API와 Google Calendar API 기능(이벤트 생성, 삭제, 조회 등)을 통합하여 자연어 명령에 따라 캘린더 이벤트를 처리할 수 있습니다.

## 주요 기능

- **Slack 이벤트 핸들링:** Slack Bolt를 사용하여 Slack 내 멘션 이벤트를 처리합니다.
- **자연어 처리:** Anthropic API를 이용해 사용자의 요청을 이해하고, 필요에 따라 도구 호출(tool call)을 실행합니다.
- **캘린더 연동:** Google Calendar API와 연동하여 다음 기능을 수행합니다.
  - 이벤트 생성 (`create_event`)
  - 이벤트 조회 (`check_event`)
  - 이벤트 삭제 (`delete_event`)
- **문맥 검색:** ABC 컴퍼니 관련 질문에 대해 적절한 문맥 정보를 반환합니다. (`retrieve_context`)

## 파일 구조

프로젝트는 기능별로 모듈을 분리하여 유지보수와 확장성을 높였습니다.

project/ ├── main.py # Slack 봇 시작 및 Socket Mode Handler 설정 ├── slack_app.py # Slack 이벤트 핸들링 및 Anthropic API 연동 로직 ├── tool_processor.py # 도구 호출(툴) 처리 및 도구 목록 정의 ├── calendar_functions.py # Google Calendar 관련 기능 (이벤트 생성, 삭제, 조회) ├── utils.py # 추가 유틸리티 함수 (문맥 검색 등) └── README.md # 프로젝트 설명서 (이 파일)

bash

## 설치 및 설정

1. **레포지토리 클론:**

   ```bash
   git clone https://github.com/yourusername/yourproject.git
   cd yourproject
필요한 패키지 설치:

bash
pip install -r requirements.txt
requirements.txt 파일에는 anthropic, slack, slack_bolt 등의 필수 패키지가 포함되어야 합니다.

환경 변수 설정:

프로젝트 실행 전에 다음 환경 변수를 설정해야 합니다.

SLACK_BOT_TOKEN: Slack 봇 토큰
SLACK_APP_TOKEN: Slack 앱 토큰 (Socket Mode 사용 시)
ANTHROPIC_API_KEY: Anthropic API 키
Google Calendar API 설정 (필요 시):

calendar_functions.py 파일 내 이벤트 생성/삭제/조회 함수를 실제 Google Calendar API와 연동하도록 수정할 수 있습니다.

실행 방법
다음 명령어로 봇을 실행합니다.

bash
python main.py
실행 후 Slack 내에서 봇이 멘션되면, 사용자 요청을 받아 Anthropic API를 통해 처리하고 필요한 경우 캘린더 관련 작업을 수행합니다.

커스터마이징
툴 함수 수정:
calendar_functions.py 파일에서 Google Calendar API 연동 로직을 본인의 필요에 맞게 수정할 수 있습니다.

문맥 검색 기능:
utils.py 파일의 retrieve_context 함수를 ABC 컴퍼니 관련 정보를 반환하도록 변경하여 확장할 수 있습니다.

로깅 및 테스트:
각 모듈에서 로깅 기능을 강화하거나, 단위 테스트를 추가하여 안정성을 높일 수 있습니다.
