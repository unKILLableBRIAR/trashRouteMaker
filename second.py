import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import seaborn as sns
import platform
import os

# macOS 한글 폰트 설정
if platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'AppleGothic'

# CSV 파일 불러오기
df = pd.read_csv("./data/Population_waste.csv")

# 컬럼명 정리
df.columns = ['index', '구', '인구수', '배출량', '1인당_배출량_톤_일']

# 피어슨 상관계수 계산
corr, p = pearsonr(df['인구수'], df['배출량'])

# 산점도 + 회귀선 시각화
plt.figure(figsize=(8, 6))
sns.regplot(x='인구수', y='배출량', data=df, marker='o', color='forestgreen')

# 각 포인트에 구 이름 표시
for i in range(len(df)):
    plt.text(df['인구수'][i], df['배출량'][i] + 1, df['구'][i], fontsize=9)

# 그래프 제목에 상관계수 표시
plt.title(f"인구수 vs 쓰레기 배출량\n피어슨 상관계수: {corr:.3f}")
plt.xlabel("인구수")
plt.ylabel("쓰레기 배출량 (톤/일)")
plt.grid(True)
plt.tight_layout()


output_dir = "./output"
os.makedirs(output_dir, exist_ok=True)
plt.savefig(f"{output_dir}/population_vs_waste_with_labels.png", dpi=300, bbox_inches='tight')
plt.show()
