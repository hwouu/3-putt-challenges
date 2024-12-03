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
- 제한된 환경에서의 임베디드 소프트웨어 개발 경험을 축적.
- 간단한 물리 기반 게임의 설계와 구현.
- 라즈베리파이와 센서를 활용한 SPI 통신 구현.

---

## 🔑 주요 기능

- **게임 플레이:**
  - 공의 방향과 파워를 설정하여 가능한 3번 내에 공을 홀컵에 넣는 도전.
  - 현실감 있는 물리 엔진으로 경계 반사와 마찰 효과를 시뮬레이션.
  - 다양한 난이도의 스코어링 시스템(홀인원, 버디, 파 등) 제공.

- **플랫폼 지원:**
  - **Mac** 환경: Pygame을 활용한 키보드 입력.
  - **Raspberry Pi** 환경: 조이스틱 입력 및 SPI 통신 기반 디스플레이 지원.

- **게임 상태 관리:**
  - 조준, 파워 충전, 샷, 골퍼 이동, 일시 정지 상태 간 전환.

- **UI:**
  - 직관적인 게임 인터페이스와 점수 표시.

---

## ⚙️ 설치 및 실행

### 1. 요구 사항
- Python 3.8 이상
- **필수 라이브러리:**
  - `pygame`
  - `Pillow`
  - `spidev` (라즈베리파이 환경)

### 2. 설치

1. **레포지토리 클론**
    ```bash
    git clone https://github.com/your-username/3-putt-challenges.git
    cd 3-putt-challenges
    ```

2. **의존성 설치**
    ```bash
    pip install -r requirements.txt
    ```

3. **환경 설정**
    - Mac:
      ```bash
      export PLATFORM=mac
      ```
    - Raspberry Pi:
      ```bash
      export PLATFORM=rpi
      ```

### 3. 실행

```bash
python src/main.py
```

---

## 🗂 디렉토리 구조

```
src/
├── assets                # 게임 이미지 및 리소스
├── config                # 환경 설정 파일
├── core                  # 게임 및 물리 엔진 구현
├── main.py               # 메인 실행 파일
├── objects               # 게임 오브젝트 클래스 (공, 골퍼, 홀컵)
├── platforms             # 플랫폼별 입력 및 디스플레이 처리
└── screens               # 게임 및 시작 화면 로직
```

---

## 🛠 사용된 기술

- **언어 및 라이브러리:**
  - Python, Pygame, Pillow
- **플랫폼:**
  - Mac, Raspberry Pi
- **임베디드 통신:**
  - SPI(Serial Peripheral Interface)

---

## 🖋️ 기여 방법

1. 이 레포지토리를 포크하세요.
2. 새로운 브랜치를 생성하세요.
    ```bash
    git checkout -b feature/new-feature
    ```
3. 수정 사항을 커밋하고 브랜치에 푸시하세요.
    ```bash
    git commit -m "Add new feature"
    git push origin feature/new-feature
    ```
4. PR(Pull Request)을 제출하세요.

---

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](./LICENSE) 파일을 참조하세요.

---

**즐거운 플레이 되세요!**  
**3-Putt Challenges 팀 드림**

--- 
