import pandas as pd
import requests
import time


def get_coords_kakao(address, api_key):
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {api_key}"}
    params = {"query": address}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        return None, None

    result = response.json()
    if result['documents']:
        x = result['documents'][0]['x']  # 경도
        y = result['documents'][0]['y']  # 위도
        return float(x), float(y)
    else:
        return None, None


# ✅ 1. 엑셀 파일에서 주소 읽기
df = pd.read_excel('./data/Daejeon_population_2020.xlsx')

# ✅ 2. Kakao API Key 입력
api_key = ''

# ✅ 3. '행정구역' 컬럼에서 주소 추출 → 위경도 변환
longitudes = []
latitudes = []

for i, row in df.iterrows():
    address = row['행정구역']
    lon, lat = get_coords_kakao(address, api_key)
    longitudes.append(lon)
    latitudes.append(lat)

    print(f"{i + 1}/{len(df)} - {address} → {lon}, {lat}")
    time.sleep(0.2)  # 너무 빨리 호출하면 API에서 차단될 수 있어, 0.2초 대기

# ✅ 4. 결과 저장
df['경도'] = longitudes
df['위도'] = latitudes

# ✅ 5. 새 엑셀로 저장
df.to_excel('./output/Daejeon_population_with_coords.xlsx', index=False)