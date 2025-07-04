# 2025_CHALLKATHON_Nulls_BE
Null_s 팀

# ⏳ 인생 시계 (Life Clock)

> "내 인생 몇 % 살았지?"  
프로젝트 "인생 시계"는 사용자의 출생부터 기대 수명까지의 삶을 하나의 긴 타임라인(바 형태)으로 시각화하여, 인생의 흐름과 밀도를 직관적으로 보여주는 웹 기반 서비스입니다. 사용자는 자신의 과거 주요 이벤트를 타임라인에 직접 기록할 수 있으며, 앞으로의 계획이나 목표도 함께 추가할 수 있습니다. 이를 통해 지나온 시간을 되돌아보고, 남은 시간을 어떻게 채워나갈지 생각해보는 계기를 제공합니다. 삶이 답답하고 막막하게 느껴질 때, 또는 나의 삶에 대한 동기 부여가 필요할 때, 인생 시계는  데이터 기반 통찰을 통해 나 자신을 돌아보게 만드는 의미 있는 도구가 될 것입니다.

📌 주제 요약: "인생 시계 (Life Clock)"
사용자가 생년월일과 기대 수명을 입력하면,
현재 인생이 몇 % 진행됐는지 시각적으로 보여주는 웹 앱

---

## 👩‍💻 개발자 소개

| 이름 | 역할 | GitHub |
|------|------|--------|
| 곽현철 | 프론트엔드 개발, UI/UX 디자인 |  |
| 서정혁 | 백엔드 개발, DB 설계 |  |
| 서정훈 | 전체 기획, 기능 통합, 시각화 | |

## 🛠️ 사용 기술 스택

- **언어:** Python, JavaScript (Node.js)  
- **프레임워크:** FastAPI, Express  
- **데이터베이스:** SQLite3  
- **인증 방식:** JWT (토큰 발급 및 검증)  
- **기타 사용 기술:**  
  - `bcrypt` : 비밀번호 해싱  
  - `Pydantic` : 요청/응답 스키마 검증  
  - `CORS` : 교차 출처 리소스 공유 설정  
  - `dotenv` : 환경 변수 관리

---
## 📁파일 구조

루트 디렉터리 (2025_CHALLKATHON_Nulls_BE/)
- .gitignore — Git 추적 제외 설정
- README.md — 프로젝트 설명 문서
- database.py — SQLite 연결 및 테이블 초기화
- main.py — FastAPI 앱 실행 진입점
- requirements.txt — Python 의존성 목록
- user.db — SQLite 사용자 DB 파일 (개발용)

fastapi_api/ — 🐍 Python 기반 메인 백엔드
- app/__init__.py — FastAPI 앱 초기화
- app/core/security.py — JWT 발급, 비밀번호 해싱 등 보안 유틸리티
- app/models/user.py — 사용자 데이터베이스 모델
- app/routes/auth.py — 로그인 및 회원가입 라우트
- app/routes/ping.py — 서버 헬스 체크용 엔드포인트
- app/schemas/auth.py — 로그인 요청/응답용 Pydantic 스키마
- app/schemas/token.py — JWT 토큰 구조 정의

node_api/ — 🌐 Node.js 기반 퍼센트 계산 API
- app.js — Express 진입점
- routes/life.js — 생년월일 기반 인생 퍼센트 계산 API
- package.json, package-lock.json — Node 의존성 및 버전 정보


## 🔧 기능별 소개

---

### 🔐 1. 사용자 인증 & 로그인  
**관련 파일:** `auth.py`, `security.py`, `schemas/auth.py`, `token.py`

- 사용자는 이메일과 비밀번호로 로그인할 수 있습니다.  
- 로그인 요청 시 입력값을 검증한 후, 서버는 **JWT 토큰**을 발급합니다.  
- JWT는 이후 요청에서 사용자를 식별하고, 로그인 상태 유지를 돕습니다.  
- **주요 API:**  
  - `POST /auth/login` : 로그인  
  - `GET /auth/me` : 로그인된 사용자 정보 조회  
- 비밀번호는 `bcrypt`로 안전하게 해싱되어 저장되며, 로그인 시 해시 비교 방식으로 인증됩니다.

---

### 🧠 2. 생일 기반 인생 퍼센트 계산  
**관련 파일:** `node_api/routes/life.js`

- 사용자의 **생년월일**을 기준으로 오늘 날짜와의 차이를 계산해 나이를 구합니다.  
- 입력된 **기대 수명** 대비 현재까지 인생을 몇 퍼센트 살았는지 계산해 숫자로 반환합니다.  
- 프론트엔드에서는 이 값을 **바 차트** 또는 **도넛 그래프** 등으로 시각화합니다.  
- **주요 API:**  
  - `POST /life` : 생년월일과 기대 수명을 요청하면, 인생 퍼센트와 나이를 응답으로 제공합니다.

---

### 🩺 3. 서버 상태 확인  
**관련 파일:** `ping.py`

- FastAPI 서버가 정상적으로 동작 중인지 확인하는 **상태 확인용 엔드포인트**입니다.  
- `/ping`으로 요청을 보내면 `"pong"`이라는 단순한 응답이 돌아옵니다.  
- 프론트엔드나 배포 환경에서 서버 상태를 빠르게 체크하는 데 사용됩니다.

---

### 📄 4. 사용자 데이터 저장  
**관련 파일:** `models/user.py`, `database.py`, `user.db`

- 사용자 정보(email, 해싱된 비밀번호 등)는 **SQLite 기반 DB(user.db)**에 저장됩니다.  
- `models/user.py`는 SQLAlchemy를 이용해 테이블 구조를 정의합니다.  
- `database.py`는 SQLite와 연결하여 DB 초기화 및 쿼리 실행을 담당합니다.
