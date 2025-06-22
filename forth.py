import pandas as pd
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

# 데이터 불러오기
df = pd.read_excel('./data/Daejeon_population_with_coords.xlsx')

# 대덕구만 필터링
target_gu = '유성구'
gu_df = df[df['행정구역'].str.contains(target_gu)].reset_index(drop=True)

# 거리 행렬 계산 함수 (유클리디안 거리 사용)
def compute_euclidean_distance_matrix(locations):
    size = len(locations)
    matrix = {}
    for from_counter in range(size):
        matrix[from_counter] = {}
        for to_counter in range(size):
            if from_counter == to_counter:
                matrix[from_counter][to_counter] = 0
            else:
                dx = locations[from_counter][0] - locations[to_counter][0]
                dy = locations[from_counter][1] - locations[to_counter][1]
                matrix[from_counter][to_counter] = int(((dx**2 + dy**2)**0.5) * 1000)
    return matrix

# 경도, 위도 리스트 생성
locations = list(zip(gu_df['위도'], gu_df['경도']))

# 인구수를 가중치로 활용 (큰 값일수록 우선순위 높게)
weights = gu_df['2020년_총인구수'].tolist()

# 거리 행렬 생성
distance_matrix = compute_euclidean_distance_matrix(locations)

# 라우팅 모델 초기화
manager = pywrapcp.RoutingIndexManager(len(distance_matrix), 1, 0)
routing = pywrapcp.RoutingModel(manager)

# 거리 콜백 함수 등록
def distance_callback(from_index, to_index):
    from_node = manager.IndexToNode(from_index)
    to_node = manager.IndexToNode(to_index)
    # 거리에서 인구 수 가중치 반영 (멀리 가도 인구가 많으면 고려됨)
    weight_factor = (weights[to_node] + weights[from_node]) / 2
    return int(distance_matrix[from_node][to_node] / (weight_factor / 10000))

transit_callback_index = routing.RegisterTransitCallback(distance_callback)

# 거리 기준 최적화
routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

# 탐색 매개변수 설정
search_parameters = pywrapcp.DefaultRoutingSearchParameters()
search_parameters.first_solution_strategy = (
    routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

# 최적 경로 계산
solution = routing.SolveWithParameters(search_parameters)

# 결과 출력
if solution:
    print("📍 쓰레기 수거 최적 경로 (인구 가중치 고려):\n")
    index = routing.Start(0)
    route = []
    while not routing.IsEnd(index):
        node_index = manager.IndexToNode(index)
        route.append(node_index)
        index = solution.Value(routing.NextVar(index))
    route.append(manager.IndexToNode(index))  # 마지막 노드

    for i, idx in enumerate(route):
        name = gu_df.iloc[idx]['행정구역']
        lat = gu_df.iloc[idx]['위도']
        lon = gu_df.iloc[idx]['경도']
        pop = gu_df.iloc[idx]['2020년_총인구수']
        print(f"{i+1}. {name} (인구수: {pop}) - {lat:.6f}, {lon:.6f}")
else:
    print("❌ 경로를 찾을 수 없습니다.")