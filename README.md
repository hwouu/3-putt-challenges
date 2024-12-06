
# 🏌️‍♂️ 3-Putt Challenges

**3-Putt Challenges**는 간단하고 직관적인 골프 미니게임으로, 플레이어가 방향과 힘을 설정하여 골프공을 홀컵에 넣는 재미를 제공합니다. Python과 라즈베리파이를 활용하여 개발되었으며, 물리 엔진과 멀티 플랫폼 지원을 통해 다양한 환경에서 실행 가능합니다.

---
## 📖 목차
1. [프로젝트 소개](#-프로젝트-소개)
2. [주요 기능](#-주요-기능)
3. [설치 및 실행](#-설치-및-실행)
4. [디렉토리 구조](#-디렉토리-구조)
5. [사용된 기술](#-사용된-기술)
6. [기여 방법](#️-기여-방법)
7. [라이선스](#️-라이선스)

---
## 🌟 프로젝트 소개
**3-Putt Challenges**는 골프의 전략적 요소를 물리 엔진과 간단한 인터페이스를 통해 구현한 게임입니다.  
특히, 플랫폼 간 호환성을 고려하여 Mac과 라즈베리파이 환경 모두에서 실행 가능하며, 사용자 입력은 키보드와 조이스틱을 지원합니다.

### 🎯 목표
- 제한된 환경에서의 임베디드 소프트웨어 개발 경험을 축적
- 간단한 물리 기반 게임의 설계와 구현
- 라즈베리파이와 센서를 활용한 SPI 통신 구현

---
## 🔑 주요 기능
- **게임 플레이:**
  - 3개의 서로 다른 코스 구현 (기본, 장애물, 폭탄)
  - 공의 방향과 파워를 설정하여 가능한 3번 내에 공을 홀컵에 넣는 도전
  - 현실감 있는 물리 엔진으로 경계 반사와 마찰 효과를 시뮬레이션
  - 다양한 난이도의 스코어링 시스템(홀인원, 버디, 파 등) 제공
- **장애물 시스템:**
  - 움직이는 펜스: 충돌 시 1타 페널티
  - 폭탄: 충돌 시 2타 페널티
- **플랫폼 지원:**
  - **Mac** 환경: 
    - Pygame을 활용한 키보드 입력
    - 방향키: 방향 조절
    - 스페이스바(A): 파워 충전/샷
    - 리턴(B): 일시정지/재시작
  - **Raspberry Pi** 환경: 
    - 조이스틱 입력 및 SPI 통신 기반 디스플레이 지원
    - 조이스틱: 방향 조절
    - A 버튼: 파워 충전/샷
    - B 버튼: 일시정지/재시작
- **게임 상태 관리:**
  - 조준(AIMING): 방향 설정
  - 파워 충전(CHARGING): 샷 파워 조절
  - 샷(SHOOTING): 공의 이동
  - 골퍼 이동(MOVING_GOLFER): 다음 샷 준비
  - 점수 표시(SHOWING_SCORE): 홀 완료 후 점수 표시
  - 코스 전환(COURSE_TRANSITION): 다음 코스로 이동
  - 일시 정지(PAUSED): 게임 일시 정지
  - 스코어카드(SHOW_SCORECARD): 최종 점수 확인
- **UI/UX:**
  - 직관적인 게임 인터페이스
  - 실시간 파워 게이지
  - 조준선 표시
  - 스코어카드 시스템

---
## ⚙️ 설치 및 실행
### 1. 요구 사항
- Python 3.8 이상
- **필수 라이브러리:**
  - `pygame`
  - `Pillow`
  - `adafruit-circuitpython-rgb-display` (라즈베리파이 환경)
  - `adafruit-blinka` (라즈베리파이 환경)

### 2. 설치
1. **레포지토리 클론**
    ```bash
    git clone https://github.com/your-username/3-putt-challenges.git
    cd 3-putt-challenges
    ```

2. **가상환경 설정**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux/Mac
    # or
    .\venv\Scripts\activate  # Windows
    ```

3. **의존성 설치**
    ```bash
    pip install -r requirements.txt
    ```

4. **라즈베리파이 추가 설정**
    ```bash
    # GPIO 및 SPI 권한 설정
    sudo usermod -a -G gpio,spi $USER
    
    # SPI 인터페이스 활성화
    sudo raspi-config  # Interfacing Options -> SPI -> Yes
    ```

### 3. 실행
```bash
# Mac 환경
PYTHONPATH=/path/to/project PLATFORM=mac python3 src/main.py

# 라즈베리파이 환경
PYTHONPATH=/path/to/project PLATFORM=rpi python3 src/main.py
```

---
## 🗂 디렉토리 구조
```
src/
├── assets/             # 게임 이미지 및 리소스
│   └── images/
│       ├── course/    # 코스 배경
│       ├── objects/   # 게임 오브젝트 이미지
│       ├── player/    # 플레이어 이미지
│       ├── scores/    # 점수 관련 이미지
│       └── ui/        # UI 요소
├── config/            # 환경 설정 파일
├── core/              # 핵심 게임 로직
│   ├── game_engine.py
│   └── physics_engine.py
├── models/            # 데이터 모델
├── objects/           # 게임 오브젝트
│   └── obstacles/     # 장애물 구현
├── platforms/         # 플랫폼별 구현
│   ├── display/      # 화면 출력 처리
│   └── input/        # 입력 처리
├── screens/           # 게임 화면
└── utils/            # 유틸리티 기능
```

---
## 🛠 사용된 기술
- **언어 및 프레임워크:**
  - Python 3.11
  - Pygame 2.5.2
  - Pillow (Python Imaging Library)
- **하드웨어 플랫폼:**
  - Mac OS
  - Raspberry Pi
- **하드웨어 통신:**
  - SPI(Serial Peripheral Interface)
  - GPIO
- **디스플레이:**
  - ST7789 LCD Driver
- **코드 구조:**
  - 객체지향 설계
  - 상태 패턴
  - 추상 팩토리 패턴

---
## 🖋️ 기여 방법
1. 이 레포지토리를 포크하세요
2. 새로운 브랜치를 생성하세요
    ```bash
    git checkout -b feature/new-feature
    ```
3. 수정 사항을 커밋하고 브랜치에 푸시하세요
    ```bash
    git commit -m "Add new feature"
    git push origin feature/new-feature
    ```
4. PR(Pull Request)을 제출하세요

---
## 📝 라이선스
이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](./LICENSE) 파일을 참조하세요.

---
