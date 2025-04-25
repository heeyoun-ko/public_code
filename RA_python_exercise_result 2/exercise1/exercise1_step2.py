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
from scipy import stats

# .mat 파일 불러오기
file_path = '/Users/koheeyoun/Desktop/im_document/Lab/grating2AFC S11.mat'
mat_data = sio.loadmat(file_path)

# 반응시간 데이터 추출
rt_data = mat_data['data']['responseRT'][0][0].flatten()

# 데이터 반으로 나누기
first_half = rt_data[:len(rt_data)//2]
second_half = rt_data[len(rt_data)//2:]

# t-검정 실시
t_stat, p_value = stats.ttest_ind(first_half, second_half)

print("\n=== T-test Results ===")
print(f"t-statistic: {t_stat:.3f}")
print(f"p-value: {p_value:.3f}")
print(f"Significance: {'Significant (p < 0.05)' if p_value < 0.05 else 'Not significant (p > 0.05)'}")

'''
=== T-test Results ===
t-statistic: 3.071
p-value: 0.002
Significance: Significant (p < 0.05)
'''