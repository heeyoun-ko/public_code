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
from trials2counts import trials2counts
from type2_SDT_SSE import type2_SDT_SSE

# .mat 파일 불러오기
file_path = '/Users/koheeyoun/Desktop/im_document/Lab/grating2AFC S11.mat'
mat_data = sio.loadmat(file_path)

# 데이터 추출
stim = mat_data['data']['stimID'][0][0].flatten()  # stimulus (0 or 1)
resp = mat_data['data']['response'][0][0].flatten()  # response (0 or 1)
rating = mat_data['data']['rating'][0][0].flatten()  # confidence rating (1-4)

# 데이터 반으로 나누기
half_point = len(stim) // 2
first_half = {
    'stim': stim[:half_point],
    'resp': resp[:half_point],
    'rating': rating[:half_point]
}
second_half = {
    'stim': stim[half_point:],
    'resp': resp[half_point:],
    'rating': rating[half_point:]
}

# 각 반부에 대해 meta-d' 계산
results = []
for half in [first_half, second_half]:
    # trials2counts를 사용하여 반응 횟수 계산
    nR_S1, nR_S2 = trials2counts(
        half['stim'].tolist(),
        half['resp'].tolist(),
        half['rating'].tolist(),
        nRatings=4,
        padCells=True
    )
    
    # type2_SDT_SSE를 사용하여 meta-d' 계산
    fit = type2_SDT_SSE(nR_S1, nR_S2)
    results.append(fit)

# 결과 플로팅
plt.figure(figsize=(8, 6))
bars = plt.bar(['First Half', 'Second Half'], 
               [results[0]['meta_d_a'], results[1]['meta_d_a']],
               color='white',
               edgecolor='black',
               linewidth=1)

# 그래프 꾸미기
plt.title("Meta-d' by Experimental Half", fontsize=12)
plt.ylabel("Meta-d'", fontsize=10)
plt.xlabel('Experimental Half', fontsize=10)

# y축 범위 설정
plt.ylim(0, max(results[0]['meta_d_a'], results[1]['meta_d_a']) * 1.2)

# 격자 추가
plt.grid(True, alpha=0.3, linestyle='--')

# 값 표시
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.2f}',
             ha='center', va='bottom')

plt.box(True)
plt.tight_layout()
plt.show()

# 결과 출력
print("\n=== Meta-d' Analysis ===")
print(f"First Half Meta-d': {results[0]['meta_d_a']:.3f}")
print(f"Second Half Meta-d': {results[1]['meta_d_a']:.3f}")
print("\nM-ratio (meta-d'/d'):")
print(f"First Half: {results[0]['M_ratio']:.3f}")
print(f"Second Half: {results[1]['M_ratio']:.3f}")
