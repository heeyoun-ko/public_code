import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# CSV 파일 불러오기
df = pd.read_csv('results_0409_001.csv')

# 분석 및 시각화
plt.figure(figsize=(15, 6))

# 1. RT 비교
plt.subplot(1, 2, 1)
rt_data = [df[df['type'] == 'gabor']['rt'], df[df['type'] == 'square']['rt']]
plt.boxplot(rt_data, labels=['Gabor', 'Square'])
plt.title('Reaction Time by Stimulus Type')
plt.ylabel('Reaction Time (s)')
plt.xlabel('Stimulus Type')

# 2. Error Rate 비교
plt.subplot(1, 2, 2)
error_rates = 1 - df.groupby('type')['correct'].mean()
bars = plt.bar(['Gabor', 'Square'], error_rates, color='white', edgecolor='black')
plt.title('Error Rate by Stimulus Type')
plt.ylabel('Error Rate')
plt.xlabel('Stimulus Type')

# Error rate 값 표시
for i, rate in enumerate(error_rates):
    plt.text(i, rate, f'{rate:.3f}', ha='center', va='bottom')

plt.tight_layout()
plt.savefig('results_plot.png')
plt.close()

# 통계 요약 출력
print("\n🎯 통계 결과 요약")
print(f"- Gabor 평균 RT: {df[df['type'] == 'gabor']['rt'].mean():.3f}s")
print(f"- Square 평균 RT: {df[df['type'] == 'square']['rt'].mean():.3f}s")
print(f"- Gabor 오류율: {1 - df[df['type'] == 'gabor']['correct'].mean():.3f}")
print(f"- Square 오류율: {1 - df[df['type'] == 'square']['correct'].mean():.3f}")

# t-test 결과
gabor_rt = df[df['type'] == 'gabor']['rt']
square_rt = df[df['type'] == 'square']['rt']
t_stat, p_value = stats.ttest_ind(gabor_rt, square_rt)
print(f"- RT t-test p-value: {p_value:.3f}")

