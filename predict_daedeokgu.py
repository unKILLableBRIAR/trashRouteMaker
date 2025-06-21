import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform

if platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'AppleGothic'


df = pd.read_csv("daejeon_2020_waste.csv")

daedeokgu = df[df['city_gn_gu_nm'] == '대덕구'].copy()

daedeokgu['ds'] = pd.to_datetime({
    'year': daedeokgu['year'],
    'month': daedeokgu['mt'],
    'day': daedeokgu['dt']
})

# 예측할 y값 만들기 (단위: kg) & 누락값 제거
daedeokgu = daedeokgu.dropna(subset=['dscamt'])  # NaN 제거
daedeokgu['y'] = daedeokgu['dscamt'] / 1000

model = Prophet()
model.fit(daedeokgu[['ds', 'y']])

# 30일 미래 데이터프레임 생성 및 예측
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

model.plot(forecast)
plt.title("대덕구 쓰레기 배출량 예측 (30일)")
plt.xlabel("날짜")
plt.ylabel("배출량 (kg)")
plt.tight_layout()
plt.grid(True)
plt.show()

model.plot_components(forecast)
plt.tight_layout()
plt.show()

# 7. 예측 그래프 저장
fig1 = model.plot(forecast)
fig1.savefig("output/predict_plot_daedeok.png", dpi=300, bbox_inches='tight')

# 8. 구성요소 그래프 저장
fig2 = model.plot_components(forecast)
fig2.savefig("output/components_plot_daedeok.png", dpi=300, bbox_inches='tight')
