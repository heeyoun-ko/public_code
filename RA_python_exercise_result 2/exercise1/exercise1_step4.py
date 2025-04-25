"""
이 코드는 원래 Python 2용으로 작성된 MATLAB(.mat) 파일을 Python 3에 맞게 변환하여 사용합니다.
원본 데이터 구조:
- Python 2: mat_data['data']['responseRT']
- Python 3: mat_data['data']['responseRT'][0][0].flatten()

변환 과정:
1. .mat 파일을 Python 3 호환 형식으로 변환
2. 데이터 구조를 [0][0].flatten() 형식으로 수정
3. 필요한 경우 tolist()를 사용하여 Python 리스트로 변환

원본 데이터 출처: /Users/koheeyoun/Desktop/im_document/Lab/grating2AFC S11.mat
"""

import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# .mat 파일 불러오기
file_path = '/Users/koheeyoun/Desktop/im_document/Lab/grating2AFC S11.mat'
mat_data = sio.loadmat(file_path)

# 데이터 추출
rating = mat_data['data']['rating'][0][0].flatten()
correct = mat_data['data']['correct'][0][0].flatten()
response = mat_data['data']['response'][0][0].flatten()  # 응답 데이터 추가

# 전체 데이터에서 target과 non-target 개수 계산
n_targets_total = np.sum(correct == 1)
n_nontargets_total = np.sum(correct == 0)

print(f"전체 데이터: target={n_targets_total}, non-target={n_nontargets_total}")

# 각 신뢰도 수준별 d' 계산
dprimes = []
epsilon = 0.0001  # 극단값 방지를 위한 보정값

for conf in range(1, 5):
    # 해당 신뢰도 수준의 시행만 선택
    conf_trials = rating == conf
    
    # 해당 신뢰도 수준에서의 target과 non-target 개수 계산
    n_targets_conf = np.sum((correct == 1) & conf_trials)
    n_nontargets_conf = np.sum((correct == 0) & conf_trials)
    
    # 해당 신뢰도 수준에서의 hit와 false alarm 계산
    # hit: target에 대해 'Yes' 응답
    hits = np.sum((correct == 1) & conf_trials & (response == 1))
    # false alarm: non-target에 대해 'Yes' 응답
    false_alarms = np.sum((correct == 0) & conf_trials & (response == 1))
    
    print(f"\n신뢰도 수준 {conf}:")
    print(f"target={n_targets_conf}, non-target={n_nontargets_conf}")
    print(f"hits={hits}, false_alarms={false_alarms}")
    
    # rate 계산 (0이나 1 방지용 극단값 보정 추가)
    if n_targets_conf > 0:
        hit_rate = hits / n_targets_conf
    else:
        hit_rate = epsilon
        
    if n_nontargets_conf > 0:
        false_alarm_rate = false_alarms / n_nontargets_conf
    else:
        false_alarm_rate = epsilon
    
    # 확률 보정
    hit_rate = min(max(hit_rate, epsilon), 1 - epsilon)
    false_alarm_rate = min(max(false_alarm_rate, epsilon), 1 - epsilon)
    
    print(f"hit_rate={hit_rate:.4f}, false_alarm_rate={false_alarm_rate:.4f}")
    
    # d' 계산
    dprime = norm.ppf(hit_rate) - norm.ppf(false_alarm_rate)
    dprimes.append(dprime)
    
    print(f"d'={dprime:.4f}")

# 그래프 그리기
plt.figure(figsize=(8, 6))
bars = plt.bar(['1', '2', '3', '4'], 
               dprimes,
               color='white',
               edgecolor='black',
               linewidth=1)

# 그래프 꾸미기
plt.title("d' by Confidence Level", fontsize=12)
plt.ylabel("d'", fontsize=10)
plt.xlabel('Confidence Level', fontsize=10)

# y축 범위 설정 (음수 값도 표시할 수 있도록)
min_dprime = min(dprimes)
max_dprime = max(dprimes)
y_range = max_dprime - min_dprime
if y_range == 0:
    plt.ylim(-1, 1)  # d'가 모두 같을 경우 기본 범위 설정
else:
    plt.ylim(min_dprime - 0.2 * y_range, max_dprime + 0.2 * y_range)

# 격자 추가
plt.grid(True, alpha=0.3, linestyle='--')

# d' 값 표시
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.2f}',
             ha='center', va='bottom')

plt.box(True)
plt.tight_layout()
plt.show()

# 결과 출력
print("\n=== d' by Confidence Level ===")
for i in range(1, 5):
    print(f"\nConfidence Level {i}:")
    print(f"N = {np.sum(rating == i)}")
    print(f"d' = {dprimes[i-1]:.2f}")
