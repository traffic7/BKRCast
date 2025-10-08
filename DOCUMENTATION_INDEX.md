# BKRCast Documentation Index
# BKRCast 문서 색인

This guide helps you navigate the comprehensive BKRCast documentation package.
이 가이드는 포괄적인 BKRCast 문서 패키지를 탐색하는 데 도움을 줍니다.

---

## 📚 Documentation Files | 문서 파일

### 1. 한국어 상세 가이드 (Korean Comprehensive Guide)
**File**: [`BKRCast_코드리뷰_활용가이드.md`](BKRCast_코드리뷰_활용가이드.md)
- **Size**: 1,170+ lines
- **Language**: 한국어 (Korean)
- **Level**: Comprehensive / 상세

**내용:**
- ✅ 프로젝트 개요 및 구조
- ✅ Emme Python API 완전 사용 설명서
- ✅ 도로 수요분석 프로세스 (네트워크 가져오기, VDF, 배정, 스킴)
- ✅ 대중교통 수요분석 프로세스 (노선, 승하차, 성능지표)
- ✅ EmmeProject 클래스 상세 설명
- ✅ 7가지 실행 예제 코드
- ✅ 활용 방안 및 시나리오 분석

**추천 대상:**
- 한국어 사용자
- 상세한 설명이 필요한 초보자
- BKRCast 전체 이해가 필요한 사용자

---

### 2. English Summary Guide
**File**: [`EMME_PYTHON_GUIDE.md`](EMME_PYTHON_GUIDE.md)
- **Size**: 370+ lines
- **Language**: English
- **Level**: Intermediate

**Contents:**
- ✅ Project overview
- ✅ Emme Python API core methods
- ✅ Highway demand analysis process flow
- ✅ Transit demand analysis process flow
- ✅ Practical code examples
- ✅ Use cases and applications

**Recommended for:**
- English speakers
- Users familiar with travel demand modeling
- Quick reference needs

---

### 3. Quick Reference Cheat Sheet
**File**: [`QUICK_REFERENCE.md`](QUICK_REFERENCE.md)
- **Size**: 350+ lines
- **Language**: English with code examples
- **Level**: Quick reference

**Contents:**
- ✅ Quick start code snippets
- ✅ Common operations
- ✅ Extra attributes reference
- ✅ Performance metrics formulas
- ✅ Troubleshooting tips

**Recommended for:**
- Experienced users needing quick lookup
- Reference during coding
- Copy-paste code patterns

---

### 4. Example Scripts Guide
**File**: [`examples/README.md`](examples/README.md)
- **Size**: 150+ lines
- **Language**: English
- **Level**: Practical

**Contents:**
- ✅ How to run example scripts
- ✅ Customization guide
- ✅ Output file descriptions
- ✅ Troubleshooting
- ✅ Learning path

**Recommended for:**
- Hands-on learners
- Users wanting to run actual code
- Customization needs

---

## 💻 Example Scripts | 예제 스크립트

### 1. Highway Analysis
**File**: [`examples/example_highway_analysis.py`](examples/example_highway_analysis.py)

**기능 (Features):**
```python
- Load Emme project and network
- Calculate V/C ratio
- Calculate VMT (Vehicle-Miles-Traveled)
- Identify congested links
- Export results to CSV
```

**실행 방법 (How to run):**
```bash
python examples/example_highway_analysis.py
```

---

### 2. Transit Analysis
**File**: [`examples/example_transit_analysis.py`](examples/example_transit_analysis.py)

**기능 (Features):**
```python
- Analyze transit boardings/alightings
- Route-level performance metrics
- Stop-level analysis
- Daily aggregation across time periods
- Export transit results
```

**실행 방법 (How to run):**
```bash
python examples/example_transit_analysis.py
```

---

## 🎯 Learning Path | 학습 경로

### For Beginners | 초보자용
1. 📖 Read: `BKRCast_코드리뷰_활용가이드.md` (Korean) or `EMME_PYTHON_GUIDE.md` (English)
2. 📝 Study: `QUICK_REFERENCE.md` for syntax
3. 💻 Run: `examples/example_highway_analysis.py`
4. 💻 Run: `examples/example_transit_analysis.py`
5. 🔧 Modify: Customize examples for your needs

### For Intermediate Users | 중급 사용자용
1. 📝 Review: `QUICK_REFERENCE.md`
2. 💻 Run and modify example scripts
3. 📖 Reference: Detailed guide for specific topics
4. 🔧 Create: Your own analysis scripts

### For Advanced Users | 고급 사용자용
1. 📝 Quick lookup: `QUICK_REFERENCE.md`
2. 💻 Extend: Example scripts with custom metrics
3. 🔧 Develop: New analysis modules
4. 📖 Contribute: Improve documentation

---

## 🔑 Key Topics Covered | 주요 다루는 주제

### Emme Python API
- ✅ EmmeProject class initialization
- ✅ Network access (links, nodes, transit lines)
- ✅ Extra attributes creation and manipulation
- ✅ Network calculator
- ✅ Matrix operations (create, import, export)

### Highway Analysis | 도로 분석
- ✅ Network import
- ✅ VDF (Volume-Delay Function) setup
- ✅ Multi-class traffic assignment
- ✅ Skim generation
- ✅ Performance metrics (VMT, VHT, V/C ratio)
- ✅ HOT lane analysis

### Transit Analysis | 대중교통 분석
- ✅ Transit network loading
- ✅ Node attributes setup
- ✅ Extended transit assignment
- ✅ Boarding/alighting calculation
- ✅ Performance metrics (PMT, boardings, load factor)
- ✅ Route and stop analysis

---

## 📊 Output Files | 출력 파일

### From Documentation
- Detailed explanations
- Code examples
- Conceptual understanding

### From Example Scripts
- `outputs/examples/highway_analysis_{tod}.csv` - Link-level highway data
- `outputs/examples/congested_links_{tod}.csv` - Congested links only
- `outputs/examples/transit_routes_{tod}.csv` - Route performance
- `outputs/examples/transit_stops_{tod}.csv` - Stop boardings/alightings
- `outputs/examples/transit_segments_{tod}.csv` - Segment-level data
- `outputs/examples/daily_route_boardings.csv` - Daily route totals
- `outputs/examples/daily_stop_boardings.csv` - Daily stop totals

---

## 🔍 Finding Information | 정보 찾기

### Need to understand concepts?
→ Read `BKRCast_코드리뷰_활용가이드.md` (Korean) or `EMME_PYTHON_GUIDE.md` (English)

### Need quick syntax?
→ Check `QUICK_REFERENCE.md`

### Need working code?
→ Run scripts in `examples/`

### Need to customize?
→ Modify example scripts and refer to guides

### Need help with errors?
→ See Troubleshooting sections in any guide

---

## 📞 Support | 지원

### Documentation Issues
- Create GitHub issue with specific document reference
- Suggest improvements via pull request

### Code Questions
- Review example scripts first
- Check troubleshooting sections
- Refer to Emme Python API documentation

### Model Questions
- BKRCast Wiki: https://github.com/Bellevuewa/BKRCast/wiki
- Contact: City of Bellevue Transportation Department

---

## 🎓 Additional Resources | 추가 자료

### Official Documentation
- [Emme Python API Reference](https://www.inrosoftware.com/en/products/emme/)
- [BKRCast GitHub Wiki](https://github.com/Bellevuewa/BKRCast/wiki)

### Theory and Methods
- Four-step travel demand modeling
- Activity-based models (Daysim)
- Traffic assignment algorithms (User Equilibrium, SOLA)
- Transit assignment methods

---

## 📝 Document Status | 문서 상태

- ✅ **Complete**: Core documentation
- ✅ **Complete**: Example scripts
- ✅ **Complete**: Quick reference
- ✅ **Tested**: Example code patterns
- 📅 **Updated**: October 2024

---

## 🤝 Contributing | 기여하기

We welcome contributions to improve this documentation:

1. **Bug fixes**: Correct errors in examples or explanations
2. **New examples**: Add useful analysis scripts
3. **Translations**: Help translate between Korean and English
4. **Improvements**: Enhance clarity or add missing topics

**How to contribute:**
1. Fork the repository
2. Make your changes
3. Submit a pull request
4. Describe your improvements

---

## 📄 License | 라이선스

This documentation is part of the BKRCast project.
- **License**: Apache License 2.0
- **Copyright**: [2014] Puget Sound Regional Council
- **Maintained by**: City of Bellevue Transportation Department

---

*Last updated: October 2024*
*Documentation version: 1.0*
