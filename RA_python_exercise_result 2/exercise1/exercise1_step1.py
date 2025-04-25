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

# .mat 파일 불러오기
file_path = '/Users/koheeyoun/Desktop/im_document/Lab/grating2AFC S11.mat'
mat_data = sio.loadmat(file_path)

# 반응시간 데이터 추출
rt_data = mat_data['data']['responseRT'][0][0].flatten()

# 데이터 반으로 나누기
first_half = rt_data[:len(rt_data)//2]
second_half = rt_data[len(rt_data)//2:]

# 평균 계산
mean_first = np.mean(first_half)
mean_second = np.mean(second_half)

# 표준오차 계산
sem_first = np.std(first_half) / np.sqrt(len(first_half))
sem_second = np.std(second_half) / np.sqrt(len(second_half))

# 흑백 그래프 그리기
plt.figure(figsize=(8, 6))
bars = plt.bar(['First Half', 'Second Half'], 
               [mean_first, mean_second],
               yerr=[sem_first, sem_second],
               capsize=5,
               color='white',
               edgecolor='black',
               linewidth=1)

# 그래프 꾸미기
plt.title('Reaction Time by Experimental Half', fontsize=12)
plt.ylabel('Reaction Time (ms)', fontsize=10)
plt.xlabel('Experimental Half', fontsize=10)

# y축 범위 설정
plt.ylim(0, max(mean_first, mean_second) * 1.2)

# 격자 추가
plt.grid(True, alpha=0.3, linestyle='--')

# 평균값 표시
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.2f}',
             ha='center', va='bottom')

# 테두리 추가
plt.box(True)

plt.tight_layout()
plt.show()

# 데이터 확인을 위한 출력
print("데이터 크기:", len(rt_data))
print("전반부 평균:", mean_first)
print("후반부 평균:", mean_second)
