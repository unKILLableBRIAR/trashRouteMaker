import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform
import os

# 한글 폰트 설정 (macOS)
if platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

# output 폴더 생성
os.makedirs("output", exist_ok=True)

# 1. 쓰레기 데이터 불러오기
df = pd.read_csv("daejeon_2020_waste.csv")
donggu = df[df['city_gn_gu_nm'] == '동구'].copy()

# 날짜 열 생성
donggu['ds'] = pd.to_datetime({
    'year': donggu['year'],
    'month': donggu['mt'],
    'day': donggu['dt']
})

# 예측 대상 열 생성 (kg 단위) + 결측 제거
donggu = donggu.dropna(subset=['dscamt'])
donggu['y'] = donggu['dscamt'] / 1000
donggu['month'] = donggu['ds'].dt.month

# 2. 강수일수 데이터 불러오기
rain_df = pd.read_excel("rain.xlsx", skiprows=5, nrows=1)
rain_values = rain_df.iloc[0, 1:13]  # 1월~12월
rain_data = pd.DataFrame({
    'month': list(range(1, 13)),
    'rain_days': rain_values.values
})

# 3. 폭염일수 데이터 불러오기
hot_df = pd.read_excel("hot.xlsx", skiprows=4, nrows=5)
hot_values = hot_df.iloc[2, 1:13].astype(float)
hot_data = pd.DataFrame({
    'month': list(range(1, 13)),
    'hot_days': hot_values.values
})

# 4. 눈일수 데이터 불러오기
snow_df = pd.read_excel("snow.xlsx", skiprows=4, nrows=5)
snow_values = snow_df.iloc[2, 1:13].astype(float)
snow_data = pd.DataFrame({
    'month': list(range(1, 13)),
    'snow_days': snow_values.values
})

# 날씨 데이터 병합
donggu = pd.merge(donggu, rain_data, on='month', how='left')
donggu = pd.merge(donggu, hot_data, on='month', how='left')
donggu = pd.merge(donggu, snow_data, on='month', how='left')

# 5. Prophet 모델 학습 (외부 변수 포함)
model = Prophet()
model.add_regressor('rain_days')
model.add_regressor('hot_days')
model.add_regressor('snow_days')
model.fit(donggu[['ds', 'y', 'rain_days', 'hot_days', 'snow_days']])

# 6. 미래 데이터프레임 생성
future = model.make_future_dataframe(periods=30)
future['month'] = future['ds'].dt.month
future = pd.merge(future, rain_data, on='month', how='left')
future = pd.merge(future, hot_data, on='month', how='left')
future = pd.merge(future, snow_data, on='month', how='left')

# 7. 예측
forecast = model.predict(future)

# 8. 시각화
fig1 = model.plot(forecast)
plt.title("동구 쓰레기 배출량 예측 (날씨 반영)")
plt.xlabel("날짜")
plt.ylabel("배출량 (kg)")
plt.tight_layout()
plt.grid(True)
plt.show()

fig2 = model.plot_components(forecast)
plt.tight_layout()
plt.show()

# 9. 이미지 저장
fig1.savefig("output/predict_plot_weather_donggu.png", dpi=300, bbox_inches='tight')
fig2.savefig("output/components_plot_weather_donggu.png", dpi=300, bbox_inches='tight')

