import pandas as pd
import matplotlib.pyplot as plt
import platform

# 한글 폰트 설정 (macOS용)
if platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'AppleGothic'

# CSV 파일 불러오기
df = pd.read_csv("../daejeon_2020_waste.csv")

# 분석할 구 선택
target_gu = "대덕구"

# 해당 구만 필터링
gu_df = df[df['city_gn_gu_nm'] == target_gu].copy()

# 월별 평균 배출량 계산
monthly_avg = gu_df.groupby('mt')['dscamt'].mean()

# 그래프 그리기
plt.figure(figsize=(10, 5))
plt.plot(monthly_avg.index, monthly_avg.values, marker='o', color='orange')
plt.title(f"{target_gu} 월별 쓰레기 배출량 평균")
plt.xlabel("월")
plt.ylabel("평균 배출량 (g)")
plt.grid(True)
plt.tight_layout()

# 그래프 저장
plt.savefig("../output/avg_daedeok.png", dpi=300, bbox_inches='tight')

# 화면에도 출력
plt.show()