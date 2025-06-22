import requests
import pandas as pd

# 🔐 사용자 정보 입력 (보호 필수)
USRID = ""  # 네 ID
KEY = ""

# 🔎 API 호출 URL 구성
year = 2020
PID = "NTN003"

url = (
    f"http://www.recycling-info.or.kr/sds/JsonApi.do"
    f"?PID={PID}&YEAR={year}&USRID={USRID}&KEY={KEY}"
)

# 요청 보내기
resp = requests.get(url, headers={'User-Agent':'Mozilla/5.0'})
resp.raise_for_status()

# JSON 데이터 → DataFrame 변환
data = resp.json().get('list', [])

df_api = pd.DataFrame(data)

# 💾 구/월별 배출량 확인
print(df_api[['gunguName','mon','disQty']].head())