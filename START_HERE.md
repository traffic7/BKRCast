# 🚀 BKRCast 학습 시작 가이드
# 🚀 BKRCast Learning Guide - Start Here

---

## 📖 환영합니다! Welcome!

이 문서는 BKRCast 프로젝트와 Emme Python API를 학습하기 위한 종합 문서 패키지의 시작점입니다.

This document is your starting point for learning the BKRCast project and Emme Python API comprehensive documentation package.

---

## 🗺️ 문서 구조 | Documentation Structure

### 1️⃣ **시작하기** | **Getting Started**
📄 [`DOCUMENTATION_INDEX.md`](DOCUMENTATION_INDEX.md) ⭐ **여기서 시작하세요! START HERE!**

전체 문서의 네비게이션 가이드입니다. 어떤 문서를 먼저 읽어야 할지, 각 문서의 내용과 수준을 설명합니다.

Complete navigation guide for all documentation. Explains which documents to read first and the content/level of each.

---

### 2️⃣ **상세 학습** | **Detailed Learning**

#### 한국어 사용자 (Korean Users)
📄 [`BKRCast_코드리뷰_활용가이드.md`](BKRCast_코드리뷰_활용가이드.md) ⭐⭐⭐
- **크기**: 32 KB, 1,170 줄
- **레벨**: 초급~고급 (포괄적)
- **내용**:
  - Emme Python API 완전 사용 설명서
  - 도로 수요분석 프로세스 상세 설명
  - 대중교통 수요분석 프로세스 상세 설명
  - EmmeProject 클래스 전체 메서드
  - 7가지 실행 가능한 코드 예제
  - 활용 방안 및 시나리오 분석

#### English Users
📄 [`EMME_PYTHON_GUIDE.md`](EMME_PYTHON_GUIDE.md) ⭐⭐
- **Size**: 11 KB, 370+ lines
- **Level**: Intermediate
- **Contents**:
  - Emme Python API core methods
  - Highway demand analysis workflow
  - Transit demand analysis workflow
  - Practical code examples
  - Use cases and applications

---

### 3️⃣ **빠른 참조** | **Quick Reference**
📄 [`QUICK_REFERENCE.md`](QUICK_REFERENCE.md) ⭐
- **크기 | Size**: 8 KB, 350+ 줄 | lines
- **레벨 | Level**: 빠른 참조 | Quick lookup
- **용도 | Use**: 코딩 중 참조용 | Reference while coding

**포함 내용 | Includes**:
- 자주 사용하는 코드 패턴
- Extra Attributes 참조표
- 성능지표 공식
- 문제 해결 팁

---

### 4️⃣ **실행 예제** | **Runnable Examples**
📁 [`examples/`](examples/) 디렉토리

#### 예제 1: 도로 네트워크 분석
📄 [`example_highway_analysis.py`](examples/example_highway_analysis.py)
```python
# 기능 | Features
- V/C ratio 계산
- VMT (Vehicle-Miles-Traveled) 계산
- 혼잡 링크 식별
- CSV 결과 내보내기

# 실행 | Run
python examples/example_highway_analysis.py
```

#### 예제 2: 대중교통 분석
📄 [`example_transit_analysis.py`](examples/example_transit_analysis.py)
```python
# 기능 | Features
- 승하차 분석
- 노선별 성능 지표
- 정류장별 통계
- 일일 집계

# 실행 | Run
python examples/example_transit_analysis.py
```

#### 예제 가이드
📄 [`examples/README.md`](examples/README.md)
- 예제 실행 방법
- 커스터마이징 가이드
- 출력 파일 설명
- 문제 해결

---

## 🎯 학습 경로 추천 | Recommended Learning Path

### 🌱 초보자 (Beginner)
```
1. 📖 DOCUMENTATION_INDEX.md 읽기
2. 📚 BKRCast_코드리뷰_활용가이드.md (한국어)
   또는 EMME_PYTHON_GUIDE.md (English)
3. 📝 QUICK_REFERENCE.md 북마크
4. 💻 example_highway_analysis.py 실행
5. 💻 example_transit_analysis.py 실행
6. 🔧 예제 수정 및 실험
```

### 🌿 중급자 (Intermediate)
```
1. 📝 QUICK_REFERENCE.md 복습
2. 💻 예제 실행 및 수정
3. 📖 특정 주제 상세 가이드 참조
4. 🔧 자신만의 분석 스크립트 작성
```

### 🌲 고급자 (Advanced)
```
1. 📝 QUICK_REFERENCE.md 참조
2. 💻 커스텀 지표 개발
3. 🔧 새로운 분석 모듈 개발
4. 📖 문서 개선 기여
```

---

## �� 빠른 시작 | Quick Start

### 최소 5분 빠른 시작
```python
# 1. 프로젝트 초기화
from scripts.EmmeProject import EmmeProject
project = EmmeProject('projects/LoadTripTables/LoadTripTables.emp')

# 2. 네트워크 가져오기
project.change_active_database('am')
network = project.current_scenario.get_network()

# 3. 링크 순회
for link in network.links():
    print(f"{link.i_node} → {link.j_node}: volume={link['@tveh']}")
```

더 많은 예제는 `QUICK_REFERENCE.md` 참조!

---

## 📊 다루는 주요 내용 | Main Topics Covered

### ✅ Emme Python API
- EmmeProject 클래스 사용법
- 네트워크 요소 접근 (links, nodes, transit lines)
- Extra Attributes 생성 및 활용
- Network Calculator 사용
- Matrix 작업 (생성, 변환, 내보내기)

### ✅ 도로 수요분석 | Highway Analysis
- 네트워크 가져오기
- VDF (Volume-Delay Function) 설정
- 다중 클래스 교통배정
- Skim 생성
- 성능지표 (VMT, VHT, V/C ratio)

### ✅ 대중교통 수요분석 | Transit Analysis
- 대중교통 네트워크 로드
- Extended Transit Assignment
- 승하차 계산
- 성능지표 (PMT, boardings, load factor)
- 노선 및 정류장 분석

---

## 📈 통계 | Statistics

```
📚 문서 파일:        4개 files
💻 예제 스크립트:    3개 scripts
📝 전체 라인:       2,200+ lines
📦 코드 예제:       20+ examples
🎯 다루는 주제:     30+ topics
💾 총 크기:         ~60 KB
```

---

## 🆘 도움이 필요하신가요? | Need Help?

### 문서 관련 | Documentation
1. `DOCUMENTATION_INDEX.md`에서 원하는 주제 찾기
2. 각 문서의 Troubleshooting 섹션 확인
3. 예제 스크립트의 주석 읽기

### 코드 관련 | Code
1. `QUICK_REFERENCE.md`에서 구문 확인
2. 예제 스크립트 실행 및 수정
3. 상세 가이드에서 설명 찾기

### 기타 지원 | Other Support
- **GitHub Issues**: 버그 리포트 및 기능 제안
- **BKRCast Wiki**: https://github.com/Bellevuewa/BKRCast/wiki
- **Contact**: City of Bellevue Transportation Department

---

## 🤝 기여하기 | Contributing

문서 개선, 번역, 새로운 예제 등 모든 기여를 환영합니다!

We welcome all contributions including documentation improvements, translations, and new examples!

1. Fork the repository
2. Make your changes
3. Submit a pull request
4. Describe your improvements

---

## 📞 연락처 | Contact

- **GitHub**: https://github.com/traffic7/BKRCast
- **Organization**: City of Bellevue Transportation Department
- **Project**: BKRCast Travel Demand Model

---

## ⚖️ 라이선스 | License

- **License**: Apache License 2.0
- **Copyright**: [2014] Puget Sound Regional Council

---

## 🎉 다음 단계 | Next Steps

### 지금 바로 시작하세요! | Start Now!

1. 🔍 **탐색**: [`DOCUMENTATION_INDEX.md`](DOCUMENTATION_INDEX.md) 읽기
2. 📖 **학습**: 언어에 맞는 상세 가이드 선택
3. 💻 **실습**: 예제 스크립트 실행
4. 🔧 **응용**: 자신의 프로젝트에 적용

---

**Created**: October 2024  
**Version**: 1.0  
**Status**: ✅ Complete

**Happy Learning! 즐거운 학습 되세요!** 🚀
