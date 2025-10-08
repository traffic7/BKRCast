# BKRCast 코드 리뷰 및 활용 가이드

## 📋 목차
1. [프로젝트 개요](#프로젝트-개요)
2. [Emme Python API 사용법](#emme-python-api-사용법)
3. [도로 수요분석 프로세스](#도로-수요분석-프로세스)
4. [대중교통 수요분석 프로세스](#대중교통-수요분석-프로세스)
5. [주요 클래스 및 함수 설명](#주요-클래스-및-함수-설명)
6. [실행 예제 및 활용 방안](#실행-예제-및-활용-방안)

---

## 프로젝트 개요

**BKRCast**는 Bellevue, Kirkland, Redmond 지역의 교통 수요 예측 모델입니다.

### 주요 특징
- **Emme Python API**를 활용한 교통 네트워크 모델링
- **Daysim** 활동 기반 수요 모델과 통합
- 도로 및 대중교통 수요분석
- 시간대별(TOD) 교통 배정
- 반복 수렴(Feedback Loop) 프로세스

### 핵심 구성요소
```
BKRCast/
├── scripts/
│   ├── EmmeProject.py          # Emme API 래퍼 클래스
│   ├── skimming/
│   │   └── SkimsAndPaths.py   # 스킴 및 경로 계산
│   ├── modeller/
│   │   └── Assignment/         # 배정 모듈
│   └── summarize/              # 결과 요약
├── emme_configuration.py       # Emme 설정
├── input_configuration.py      # 입력 설정
└── run_bkrcast.py             # 메인 실행 스크립트
```

---

## Emme Python API 사용법

### 1. EmmeProject 클래스 초기화

`EmmeProject` 클래스는 Emme API의 핵심 래퍼입니다.

```python
from EmmeProject import EmmeProject

# Emme 프로젝트 초기화
my_project = EmmeProject('projects/LoadTripTables/LoadTripTables.emp')

# 주요 속성
# my_project.bank        - Emme 데이터뱅크
# my_project.tod         - 시간대 (am, md, pm, ni)
# my_project.current_scenario - 현재 시나리오
# my_project.m           - Modeller 객체
```

### 2. 네트워크 데이터 가져오기 및 설정

```python
# 네트워크 가져오기
network = my_project.current_scenario.get_network()

# 네트워크 요소 접근
for link in network.links():
    print(f"Link {link.i_node} -> {link.j_node}: length={link.length}")

for node in network.nodes():
    print(f"Node {node.id}: x={node.x}, y={node.y}")

# 대중교통 노선
for line in network.transit_lines():
    print(f"Transit Line {line.id}: {line.description}")
```

### 3. Extra Attributes 생성 및 사용

Extra Attributes는 네트워크 요소에 사용자 정의 데이터를 저장합니다.

```python
# Link extra attribute 생성
my_project.create_extra_attribute(
    type='LINK',
    name='@volume',
    description='교통량',
    overwrite=True,
    default_value=0
)

# Node extra attribute 생성
my_project.create_extra_attribute(
    type='NODE',
    name='@boarding',
    description='승차인원',
    overwrite=True
)

# Transit segment extra attribute
my_project.create_extra_attribute(
    type='TRANSIT_SEGMENT',
    name='@tboard',
    description='구간 승차',
    overwrite=True
)
```

### 4. 네트워크 계산 (Network Calculator)

```python
# Link 계산 - 차량 환산계수 적용
my_project.network_calculator(
    "link_calculation",
    result='@mveh',
    expression='@metrk/1.5'  # 중형트럭을 승용차 환산
)

# 총 교통량 계산
expression = '@svtl1 + @svtl2 + @svtl3 + @lttrk + @mveh + @hveh + @bveh'
my_project.network_calculator(
    "link_calculation",
    result='@tveh',
    expression=expression
)
```

### 5. Matrix 작업

```python
# Matrix 생성
my_project.create_matrix(
    matrix_name='sov_am',
    matrix_description='AM SOV trips',
    matrix_type='FULL'
)

# Numpy 배열을 Emme Matrix로 변환
import numpy as np
numpy_matrix = np.array([[0, 100, 200], [150, 0, 250], [300, 350, 0]])

my_project.matrix_to_emme(
    numpy_matrix=numpy_matrix,
    mfname='sov_am',
    description='AM SOV trips',
    matrix_type='FULL'
)

# Emme Matrix를 Numpy 배열로 변환
matrix_data = my_project.emmeMatrix_to_numpyMatrix(
    matrix_name='sov_am',
    np_data_type='float32',
    multiplier=1.0
)
```

---

## 도로 수요분석 프로세스

### 1. 전체 프로세스 개요

```
네트워크 가져오기
    ↓
VDF (Volume-Delay Functions) 설정
    ↓
Trip Table 로드
    ↓
교통배정 (Traffic Assignment)
    ↓
Skim 생성 (Travel Time, Distance, Cost)
    ↓
수렴 확인 및 반복
```

### 2. 네트워크 가져오기 (Network Import)

`scripts/network/network_importer.py`

```python
def import_network(my_project, base_inputs):
    # Mode 처리
    my_project.process_modes(os.path.join(base_inputs, 'modes.txt'))
    
    # 도로 네트워크 가져오기
    my_project.process_base_network(
        os.path.join(base_inputs, f'{tod}_roadway.in')
    )
    
    # 회전제한 가져오기
    my_project.process_turn(
        os.path.join(base_inputs, f'{tod}_turns.in')
    )
    
    # Extra attributes 생성
    for attr in extra_attributes:
        my_project.create_extra_attribute(
            type=attr['type'],
            name=attr['name'],
            description=attr['description'],
            overwrite=attr['overwrite']
        )
        
        # 외부 파일에서 속성값 가져오기
        if 'file_name' in attr:
            my_project.import_attribute_values(
                file_path=attr['file_name'],
                revert_on_error=False
            )
```

### 3. VDF (Volume-Delay Function) 설정

```python
def setup_vdf(my_project):
    """
    BPR (Bureau of Public Roads) 함수 설정
    time = free_flow_time * (1 + alpha * (volume/capacity)^beta)
    """
    my_project.delete_all_functions()
    
    # VDF 함수 파일 처리
    my_project.process_function_file('inputs/skim_params/vdfs.txt')
    
    # 예시: fd1 = free_flow_time * (1 + 0.15 * (volau/ul2)^4)
```

### 4. 교통배정 (Traffic Assignment)

#### SOLA 배정 (User Equilibrium)

```python
def run_sola_assignment(my_project, max_iterations=50):
    """
    Stochastic User Equilibrium Assignment
    """
    NAMESPACE = "inro.emme.traffic_assignment.sola_traffic_assignment"
    sola = my_project.m.tool(NAMESPACE)
    
    spec = {
        "type": "SOLA_TRAFFIC_ASSIGNMENT",
        "classes": [
            {
                "mode": "c",  # car mode
                "demand": "mfSOV",  # SOV demand matrix
                "generalized_cost": {
                    "link_costs": "length",
                    "perception_factor": 1.0
                },
                "results": {
                    "link_volumes": "@svol",
                    "od_travel_times": {
                        "shortest_paths": "mfSOVtime"
                    }
                }
            }
        ],
        "stopping_criteria": {
            "max_iterations": max_iterations,
            "relative_gap": 0.0001,
            "best_relative_gap": 0.01,
            "normalized_gap": 0.01
        },
        "performance_settings": {
            "number_of_processors": 4
        }
    }
    
    sola(spec)
```

#### Multi-Class 배정

```python
def run_multiclass_assignment(my_project):
    """
    여러 차량 클래스를 동시에 배정
    - SOV (Single Occupancy Vehicle)
    - HOV2 (High Occupancy Vehicle 2+)
    - HOV3 (High Occupancy Vehicle 3+)
    - Trucks (경트럭, 중트럭, 대형트럭)
    """
    classes = [
        # SOV - 일반 차로
        {
            "mode": "s",
            "demand": "mfSOV",
            "results": {"link_volumes": "@svol"}
        },
        # HOV2 - HOV 차로 가능
        {
            "mode": "h",
            "demand": "mfHOV2",
            "results": {"link_volumes": "@hvol2"}
        },
        # HOV3 - HOV 차로 가능
        {
            "mode": "h",
            "demand": "mfHOV3",
            "results": {"link_volumes": "@hvol3"}
        },
        # 경트럭
        {
            "mode": "c",
            "demand": "mfLTruck",
            "results": {"link_volumes": "@lttrk"}
        },
        # 중형트럭
        {
            "mode": "c",
            "demand": "mfMTruck",
            "results": {"link_volumes": "@metrk"}
        },
        # 대형트럭
        {
            "mode": "c",
            "demand": "mfHTruck",
            "results": {"link_volumes": "@hvtrk"}
        }
    ]
```

### 5. Skim 생성

```python
def create_skims(my_project):
    """
    통행 저항 매트릭스 생성
    - Travel Time (분)
    - Distance (마일)
    - Cost (센트)
    """
    # Travel Time Skim
    my_project.network_calculator(
        "link_calculation",
        result='@timau',
        expression='timau'  # 링크 통행시간
    )
    
    # Distance Skim
    spec = {
        "type": "MATRIX_RESULTS",
        "results": {
            "od_values": "mfDistance"
        },
        "analyzed_demand": None,
        "constraint": None,
        "path_to_od_composition": {
            "considered_paths": "ALL",
            "multiply_path_proportions_by": {
                "analyzed_demand": False,
                "path_value": True
            }
        },
        "path_value": "length"  # 링크 길이 합산
    }
```

### 6. 교통량 계산 및 요약

```python
def calculate_total_vehicles(my_project):
    """
    차량 환산계수 적용하여 총 교통량 계산
    PCE (Passenger Car Equivalent)
    """
    # 중형트럭: PCE = 1.5
    my_project.network_calculator(
        "link_calculation",
        result='@mveh',
        expression='@metrk/1.5'
    )
    
    # 대형트럭: PCE = 2.0
    my_project.network_calculator(
        "link_calculation",
        result='@hveh',
        expression='@hvtrk/2.0'
    )
    
    # 버스: PCE = 2.0
    my_project.network_calculator(
        "link_calculation",
        result='@bveh',
        expression='@trnv3/2.0'
    )
    
    # 총 교통량 계산
    expression = '@svol + @hvol2 + @hvol3 + @lttrk + @mveh + @hveh + @bveh'
    my_project.network_calculator(
        "link_calculation",
        result='@tveh',
        expression=expression
    )
```

### 7. HOT Lane 통행료 적용

```python
def apply_hot_lane_tolls(my_project, tod='am'):
    """
    HOT Lane 동적 통행료 적용
    """
    from emme_configuration import HOT_rate_dict
    
    # I-405 HOT Lane 요금
    # @tolllane: 1=I405 북측 Leaving BEL, 2=북측 Going BEL
    #            3=I405 남측 Leaving BEL, 4=남측 Going BEL
    
    for lane_id, rate in HOT_rate_dict[tod].items():
        # HOV 통행료
        my_project.network_calculator(
            "link_calculation",
            result='@htoll',
            expression=f'@tolllane={lane_id} * length * {rate}',
            selections_by_link=f'@tolllane={lane_id}'
        )
        
        # LOV 통행료 (일반차량)
        my_project.network_calculator(
            "link_calculation",
            result='@ltoll',
            expression=f'@tolllane={lane_id} * length * {rate}',
            selections_by_link=f'@tolllane={lane_id}'
        )
```

---

## 대중교통 수요분석 프로세스

### 1. 전체 프로세스 개요

```
대중교통 네트워크 로드
    ↓
Transit Node Attributes 설정
    ↓
대중교통 배정 (Transit Assignment)
    ↓
승하차 계산
    ↓
Transit Skim 생성
    ↓
성능 지표 요약
```

### 2. 대중교통 네트워크 로드

```python
def load_transit_network(my_project, base_inputs, tod):
    """
    대중교통 네트워크 및 차량 정보 로드
    """
    # 대중교통 차량 정보
    my_project.process_vehicles(
        os.path.join(base_inputs, 'vehicles.txt')
    )
    
    # 대중교통 노선 정보
    my_project.process_transit(
        os.path.join(base_inputs, f'{tod}_transit.in')
    )
    
    # 배차간격(Headway) 설정
    headway_df = pd.read_csv('inputs/sc_headways.csv')
    
    for line_id, headway in headway_df.items():
        line = network.transit_line(line_id)
        if line:
            line.headway = headway
```

### 3. Transit Node Attributes 설정

```python
def setup_transit_node_attributes(my_project):
    """
    대중교통 정류장별 특성 설정
    - 대기시간 인지계수
    - 차내시간 인지계수
    - 배차간격 계수
    """
    transit_node_attrs = {
        '@wait_time': {
            'description': '대기시간 인지계수',
            'default': 1.0
        },
        '@in_vehicle_time': {
            'description': '차내시간 인지계수',
            'default': 1.0
        },
        '@headway_fraction': {
            'description': '배차간격 계수',
            'default': 0.5  # 평균 대기시간 = headway * 0.5
        }
    }
    
    for attr_name, attr_info in transit_node_attrs.items():
        my_project.create_extra_attribute(
            type='NODE',
            name=attr_name,
            description=attr_info['description'],
            overwrite=True,
            default_value=attr_info['default']
        )
    
    # 특정 노선에 대한 특수 설정
    # 예: Light Rail은 정시성이 높아 대기시간 인지가 낮음
    network = my_project.current_scenario.get_network()
    for node in network.nodes():
        # Light Rail 역
        if node['@station_type'] == 'LRT':
            node['@wait_time'] = 0.8
            node['@in_vehicle_time'] = 0.9
```

### 4. Extended Transit Assignment

```python
def run_transit_assignment(my_project, class_name='trnst'):
    """
    확장 대중교통 배정
    
    class_name 옵션:
    - 'trnst': 일반 버스
    - 'commuter_rail': 통근열차
    - 'litrat': 경전철
    - 'ferry': 페리
    """
    NAMESPACE = "inro.emme.transit_assignment.extended_transit_assignment"
    assign_transit = my_project.m.tool(NAMESPACE)
    
    spec = {
        "type": "EXTENDED_TRANSIT_ASSIGNMENT",
        "modes": ["b", "r", "p", "f", "l"],  # bus, rail, premium, ferry, light rail
        "demand": "mfTransit",
        
        # 일반화비용 구성요소
        "waiting_time": {
            "headway_fraction": "@headway_fraction",
            "effective_headways": "hdw",
            "spread_factor": 1,
            "perception_factor": "@wait_time"
        },
        "boarding_time": {
            "at_nodes": None,
            "on_lines": {
                "penalty": 0,
                "perception_factor": 1
            }
        },
        "boarding_cost": {
            "at_nodes": {
                "penalty": 0,
                "perception_factor": 1
            },
            "on_lines": None
        },
        "in_vehicle_time": {
            "perception_factor": "@in_vehicle_time"
        },
        "in_vehicle_cost": {
            "penalty": 0,
            "perception_factor": 1
        },
        "aux_transit_time": {
            "perception_factor": 1
        },
        
        # 결과 저장
        "flow_distribution_at_origins": {
            "by_time_to_destination": "BEST_CONNECTOR",
        },
        "flow_distribution_between_lines": {
            "consider_total_impedance": True
        },
        "connector_to_connector_path_prohibition": None,
        
        # 성능 설정
        "od_results": {
            "transit_volumes": None,
            "transit_times": "mfTransitTime",
            "total_impedance": "mfTransitImpedance"
        },
        "strategy_analysis": {
            "sub_path_combination_operator": "+",
            "sub_strategy_combination_operator": "average",
            "selected_demand_and_transit_volumes": {
                "sub_strategies_to_retain": "ALL",
                "selection_threshold": {
                    "lower": 0,
                    "upper": 999999
                }
            }
        }
    }
    
    assign_transit(spec, add_volumes=False, class_name=class_name)
```

### 5. 승하차 계산 (Boarding/Alighting)

```python
def calculate_boarding_alighting(my_project):
    """
    Transit Segment별 승하차 인원 계산
    """
    # Transit Segment Extra Attributes 생성
    segment_attrs = {
        '@tboard': '총 승차',
        '@iboard': '최초 승차',
        '@trsboard': '환승 승차',
        '@talight': '총 하차',
        '@finalight': '최종 하차',
        '@transalight': '환승 하차'
    }
    
    for attr_name, desc in segment_attrs.items():
        my_project.create_extra_attribute(
            type='TRANSIT_SEGMENT',
            name=attr_name,
            description=desc,
            overwrite=True
        )
    
    # Network Results Tool 사용
    NAMESPACE = "inro.emme.transit_assignment.extended.network_results"
    network_results = my_project.m.tool(NAMESPACE)
    
    spec = {
        "on_segments": {
            "total_boardings": "@tboard",
            "initial_boardings": "@iboard",
            "transfer_boardings": "@trsboard",
            "total_alightings": "@talight",
            "final_alightings": "@finalight",
            "transfer_alightings": "@transalight"
        }
    }
    
    # 각 대중교통 클래스별로 적용
    for class_name in ['trnst', 'commuter_rail', 'ferry', 'litrat']:
        network_results(spec, class_name=class_name)
    
    # Node 레벨 집계
    network = my_project.current_scenario.get_network()
    for node in network.nodes():
        segments = node.outgoing_segments(True)
        if segments:
            for segment in segments:
                node['@tboard_nde'] += segment['@tboard']
                node['@talight_nde'] += segment['@talight']
```

### 6. Transit Summary 및 성능지표

```python
def transit_summary(my_project, node_attr_study_area='@ndmma'):
    """
    대중교통 성능지표 요약
    
    반환값:
    - df_transit_line: 노선별 통계
    - df_transit_node: 정류장별 통계
    - df_transit_segment: 구간별 통계
    """
    network = my_project.current_scenario.get_network()
    tod = my_project.tod
    
    # 1. 노선별 통계
    transit_line_data = []
    for line in network.transit_lines():
        transit_line_data.append({
            'line_id': int(line.id),
            'route_code': line.id,
            'mode': str(line.mode),
            'description': line.description,
            'boardings': line['@board'],
            'time': line['@timtr'],
            'tod': tod
        })
    
    df_transit_line = pd.DataFrame(transit_line_data)
    
    # 2. 정류장별 통계
    transit_node_data = []
    for node in network.nodes():
        transit_node_data.append({
            'node_id': int(node.id),
            'node_subarea': node[node_attr_study_area],
            'total_boarding': node['@tboard_nde'],
            'initial_boarding': node['@tiboard_nde'],
            'transfer_boarding': node['@trsboard_nde'],
            'total_alighting': node['@talight_nde'],
            'final_alighting': node['@finalight_nde'],
            'transfer_alighting': node['@trsalight_nde'],
            'tod': tod
        })
    
    df_transit_node = pd.DataFrame(transit_node_data)
    
    # 3. 구간별 통계
    transit_segment_data = []
    for tseg in network.transit_segments():
        # 버스 차량 환산
        bus_vehs = 60 / tseg.line.headway * hwy_tod[tod]
        
        transit_segment_data.append({
            'i_node': int(tseg.i_node.id),
            'j_node': int(tseg.j_node.id),
            'line_id': int(tseg.line.id),
            'segment_volume': tseg.transit_volume,
            'segment_boarding': tseg['@tboard'],
            'segment_alighting': tseg['@talight'],
            'length': tseg.link.length,
            'transit_travel_time': tseg.transit_time,
            'bus_vehicles': bus_vehs,
            'boarding_ok': int(tseg.allow_boardings),
            'alighting_ok': int(tseg.allow_alightings),
            'tod': tod
        })
    
    df_transit_segment = pd.DataFrame(transit_segment_data)
    
    # PMT (Person-Miles-Traveled) 계산
    df_transit_segment['PMT'] = \
        df_transit_segment['segment_volume'] * df_transit_segment['length']
    
    # VHD (Vehicle-Hours-Delay) 계산
    df_transit_segment['VHD'] = \
        df_transit_segment['bus_vehicles'] * \
        (df_transit_segment['transit_travel_time'] - 
         df_transit_segment['length'] / df_transit_segment['ul2'] * 60) / 60
    
    return df_transit_line, df_transit_node, df_transit_segment
```

### 7. 특수 노선 분석

```python
def analyze_special_transit_routes():
    """
    주요 노선 승하차 분석
    - Eastlink (경전철)
    - ST Express (급행버스)
    - B Line (BRT)
    """
    # emme_configuration.py에 정의된 특수 노선
    special_routes = {
        6025: 'Eastlink EB',
        6026: 'Eastlink WB',
        6039: 'ST3_to_issaquah_WB',
        6040: 'ST3_to_issaquah_EB',
        7040: 'ST560 NB',
        7041: 'ST560 SB',
        4019: 'B Line EB',
        4020: 'B Line WB'
    }
    
    # OD Table 생성
    for route_id, route_name in special_routes.items():
        line = network.transit_line(str(route_id))
        if line:
            # 노선별 OD 테이블 생성
            create_transit_line_od_table(line, route_name)
```

---

## 주요 클래스 및 함수 설명

### EmmeProject 클래스 주요 메서드

#### 1. 네트워크 관련

```python
class EmmeProject:
    def process_base_network(self, basenet_file):
        """도로 네트워크 가져오기"""
        
    def process_transit(self, transit_file):
        """대중교통 노선 가져오기"""
        
    def process_turn(self, turn_file):
        """회전제한 가져오기"""
        
    def process_shape(self, linkshape_file):
        """링크 형상 가져오기"""
```

#### 2. 속성 관련

```python
    def create_extra_attribute(self, type, name, description, overwrite, default_value=0):
        """
        Extra Attribute 생성
        
        type: 'NODE', 'LINK', 'TURN', 'TRANSIT_LINE', 'TRANSIT_SEGMENT'
        name: '@'로 시작하는 속성명 (예: '@volume')
        """
        
    def import_attribute_values(self, file_path, revert_on_error):
        """외부 파일에서 속성값 가져오기"""
        
    def network_calculator(self, type, **kwargs):
        """네트워크 계산기 - 속성값 계산 및 설정"""
```

#### 3. Matrix 관련

```python
    def create_matrix(self, matrix_name, matrix_description, matrix_type):
        """
        Matrix 생성
        
        matrix_type: 'FULL', 'ORIGIN', 'DESTINATION', 'SCALAR'
        """
        
    def matrix_to_emme(self, numpy_matrix, mfname, description, matrix_type):
        """Numpy 배열을 Emme Matrix로 변환"""
        
    def emmeMatrix_to_numpyMatrix(self, matrix_name, np_data_type, multiplier):
        """Emme Matrix를 Numpy 배열로 변환"""
        
    def matrix_calculator(self, **kwargs):
        """Matrix 계산기"""
        
    def export_omx_matrices(self, output_mat_file):
        """OMX 형식으로 Matrix 내보내기"""
```

#### 4. 배정 관련

```python
    def calculate_transit_alighting_by_segment(self, spec=None):
        """대중교통 구간별 승하차 계산"""
        
    def transit_summary(self, node_attr_study_area='@ndmma'):
        """대중교통 성능지표 요약"""
        
    def calc_total_vehicles(self):
        """총 교통량 계산 (PCE 적용)"""
```

#### 5. 데이터뱅크 관리

```python
    def change_active_database(self, database_name):
        """활성 데이터뱅크 변경"""
        
    def set_primary_scenario(self, scen_id):
        """기본 시나리오 설정"""
        
    def create_scenario(self, scenario_number, scenario_title='test'):
        """새 시나리오 생성"""
```

---

## 실행 예제 및 활용 방안

### 예제 1: 기본 교통 배정

```python
import sys
import os
sys.path.append(os.getcwd())
from scripts.EmmeProject import EmmeProject

# 1. 프로젝트 초기화
my_project = EmmeProject('projects/LoadTripTables/LoadTripTables.emp')

# 2. 데이터뱅크 선택 (AM 시간대)
my_project.change_active_database('am')

# 3. SOV 배정 실행
from scripts.skimming.SkimsAndPaths import run_sola_assignment
run_sola_assignment(my_project, max_iterations=50)

# 4. 결과 확인
network = my_project.current_scenario.get_network()
total_vmt = 0
for link in network.links():
    total_vmt += link['@svol'] * link.length

print(f"Total VMT: {total_vmt:,.0f} miles")
```

### 예제 2: 대중교통 승하차 분석

```python
from scripts.EmmeProject import EmmeProject
import pandas as pd

# 프로젝트 초기화
my_project = EmmeProject('projects/LoadTripTables/LoadTripTables.emp')

# 모든 시간대에 대해 분석
tod_list = ['am', 'md', 'pm', 'ni']
all_transit_data = []

for tod in tod_list:
    my_project.change_active_database(tod)
    
    # Transit summary 생성
    df_line, df_node, df_segment = my_project.transit_summary()
    
    all_transit_data.append(df_node)

# 통합 데이터프레임
df_daily = pd.concat(all_transit_data, ignore_index=True)

# 일일 승차인원 집계
daily_boarding = df_daily.groupby('node_id')['total_boarding'].sum()

# 상위 10개 정류장
top_10_stops = daily_boarding.nlargest(10)
print("Top 10 Transit Stops by Daily Boardings:")
print(top_10_stops)
```

### 예제 3: 링크별 V/C Ratio 계산

```python
from scripts.EmmeProject import EmmeProject

my_project = EmmeProject('projects/LoadTripTables/LoadTripTables.emp')

# V/C ratio 계산
my_project.network_calculator(
    "link_calculation",
    result='@vc_ratio',
    expression='@tveh / ul2'  # volume / capacity
)

# 혼잡 링크 추출
network = my_project.current_scenario.get_network()
congested_links = []

for link in network.links():
    if link['@vc_ratio'] > 1.0:  # V/C > 1.0
        congested_links.append({
            'i_node': link.i_node.id,
            'j_node': link.j_node.id,
            'volume': link['@tveh'],
            'capacity': link['ul2'],
            'vc_ratio': link['@vc_ratio']
        })

df_congested = pd.DataFrame(congested_links)
df_congested.to_csv('outputs/congested_links.csv', index=False)
```

### 예제 4: HOT Lane 수익 분석

```python
from scripts.EmmeProject import EmmeProject
from emme_configuration import HOT_rate_dict

my_project = EmmeProject('projects/LoadTripTables/LoadTripTables.emp')
my_project.change_active_database('am')

network = my_project.current_scenario.get_network()

total_revenue = 0
hot_lane_data = []

for link in network.links():
    if link['@tolllane'] > 0:  # HOT Lane
        # SOV 통행료 수입
        sov_revenue = link['@svol'] * link['@stoll'] / 100  # cent to dollar
        
        # HOV 통행료 수입 (할인 적용)
        hov_revenue = (link['@hvol2'] + link['@hvol3']) * link['@htoll'] / 100
        
        link_revenue = sov_revenue + hov_revenue
        total_revenue += link_revenue
        
        hot_lane_data.append({
            'i_node': link.i_node.id,
            'j_node': link.j_node.id,
            'toll_lane_id': link['@tolllane'],
            'sov_volume': link['@svol'],
            'hov_volume': link['@hvol2'] + link['@hvol3'],
            'revenue': link_revenue
        })

print(f"Total AM HOT Lane Revenue: ${total_revenue:,.2f}")

df_hot = pd.DataFrame(hot_lane_data)
df_hot.to_csv('outputs/hot_lane_revenue.csv', index=False)
```

### 예제 5: Skim Matrix를 HDF5로 저장

```python
from scripts.EmmeProject import EmmeProject
import h5py
import numpy as np

my_project = EmmeProject('projects/LoadTripTables/LoadTripTables.emp')
my_project.change_active_database('am')

# Emme Matrix 가져오기
time_matrix = my_project.emmeMatrix_to_numpyMatrix(
    matrix_name='mfSOVtime',
    np_data_type='float32',
    multiplier=1.0
)

distance_matrix = my_project.emmeMatrix_to_numpyMatrix(
    matrix_name='mfDistance',
    np_data_type='float32',
    multiplier=1.0
)

# HDF5 파일로 저장
with h5py.File('outputs/skims/am_skims.h5', 'w') as hf:
    hf.create_dataset('time', data=time_matrix)
    hf.create_dataset('distance', data=distance_matrix)
    
print("Skims saved to HDF5 file")
```

### 예제 6: 커스텀 Extra Attribute 생성 및 활용

```python
from scripts.EmmeProject import EmmeProject

my_project = EmmeProject('projects/LoadTripTables/LoadTripTables.emp')

# 1. Extra Attribute 생성
my_project.create_extra_attribute(
    type='LINK',
    name='@arterial',
    description='간선도로 플래그',
    overwrite=True,
    default_value=0
)

# 2. 네트워크 계산기로 값 설정
# Functional class가 2 또는 3인 링크를 간선도로로 표시
my_project.network_calculator(
    "link_calculation",
    result='@arterial',
    expression='1',
    selections_by_link='@class=2,3'
)

# 3. 간선도로만 집계
network = my_project.current_scenario.get_network()
arterial_vmt = 0

for link in network.links():
    if link['@arterial'] == 1:
        arterial_vmt += link['@tveh'] * link.length

print(f"Arterial VMT: {arterial_vmt:,.0f} miles")
```

### 예제 7: 시나리오 비교

```python
from scripts.EmmeProject import EmmeProject
import pandas as pd

my_project = EmmeProject('projects/LoadTripTables/LoadTripTables.emp')

# 베이스 시나리오
my_project.set_primary_scenario(1002)
network_base = my_project.current_scenario.get_network()

# 대안 시나리오
my_project.set_primary_scenario(1003)
network_alt = my_project.current_scenario.get_network()

# 링크별 비교
comparison_data = []

for link_base in network_base.links():
    link_key = (link_base.i_node.id, link_base.j_node.id)
    link_alt = network_alt.link(*link_key)
    
    if link_alt:
        volume_diff = link_alt['@tveh'] - link_base['@tveh']
        
        if abs(volume_diff) > 100:  # 차이가 100대 이상인 경우만
            comparison_data.append({
                'i_node': link_base.i_node.id,
                'j_node': link_base.j_node.id,
                'base_volume': link_base['@tveh'],
                'alt_volume': link_alt['@tveh'],
                'difference': volume_diff,
                'pct_change': (volume_diff / link_base['@tveh'] * 100) 
                              if link_base['@tveh'] > 0 else 0
            })

df_comparison = pd.DataFrame(comparison_data)
df_comparison.to_csv('outputs/scenario_comparison.csv', index=False)
```

---

## 활용 방안 요약

### 1. 교통 영향 분석 (Traffic Impact Analysis)
- 개발 프로젝트의 통행 발생량 예측
- 주변 도로망 영향 분석
- 신호체계 개선안 평가

### 2. 대중교통 계획
- 새로운 버스 노선 계획
- 배차간격 최적화
- BRT 시스템 평가

### 3. 도로 개선 사업 평가
- 차로 추가 효과 분석
- HOV/HOT Lane 도입 평가
- 교차로 개선 효과

### 4. 정책 시나리오 분석
- VMT 감축 정책 평가
- 통행료 정책 시뮬레이션
- 교통수요관리(TDM) 효과

### 5. 성능 모니터링
- V/C Ratio 분석
- LOS (Level of Service) 평가
- 혼잡 병목구간 식별

---

## 추가 학습 자료

### Emme 공식 문서
- [Emme Python API Reference](https://www.inrosoftware.com/en/products/emme/)
- Modeller Tool 개발 가이드

### BKRCast 관련
- [BKRCast Wiki](https://github.com/Bellevuewa/BKRCast/wiki)
- 모델 검보정 문서

### 교통 수요 예측 이론
- 4단계 수요예측 모델
- Activity-Based Model (Daysim)
- 교통배정 이론 (User Equilibrium)

---

## 문의 및 기여

이 가이드는 BKRCast 프로젝트의 코드를 학습하고 활용하기 위한 참고 자료입니다.

**주요 연락처:**
- GitHub Repository: https://github.com/traffic7/BKRCast
- City of Bellevue Transportation Department

**기여 방법:**
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

---

*문서 작성일: 2024*
*BKRCast Version: Latest*
