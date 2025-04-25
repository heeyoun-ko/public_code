import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt

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

# .mat 파일 불러오기
file_path = '/Users/koheeyoun/Desktop/im_document/Lab/grating2AFC S11.mat'
mat_data = sio.loadmat(file_path)

# 반응시간과 신뢰도 데이터 추출
rt_data = mat_data['data']['responseRT'][0][0].flatten()
confidence_data = mat_data['data']['rating'][0][0].flatten()

# 각 신뢰도 수준별 반응시간 분리
rt_by_confidence = [rt_data[confidence_data == i] for i in range(1, 5)]

# 각 신뢰도 수준별 중앙값 계산
medians = [np.median(rt) for rt in rt_by_confidence]

# 흑백 그래프 그리기
plt.figure(figsize=(8, 6))
bars = plt.bar(['1', '2', '3', '4'], 
               medians,
               color='white',
               edgecolor='black',
               linewidth=1)

# 그래프 꾸미기
plt.title('Median Reaction Time by Confidence Level', fontsize=12)
plt.ylabel('Reaction Time (ms)', fontsize=10)
plt.xlabel('Confidence Level', fontsize=10)

# y축 범위 설정
plt.ylim(0, max(medians) * 1.2)

# 격자 추가
plt.grid(True, alpha=0.3, linestyle='--')

# 중앙값 표시
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.2f}',
             ha='center', va='bottom')

plt.box(True)
plt.tight_layout()
plt.show()

# 데이터 확인을 위한 출력
print("\n=== Summary Statistics ===")
for i in range(1, 5):
    print(f"\nConfidence Level {i}:")
    print(f"N = {len(rt_by_confidence[i-1])}")
    print(f"Median RT = {medians[i-1]:.2f} ms")

'''

=== Summary Statistics ===

Confidence Level 1:
N = 300
Median RT = 0.77 ms

Confidence Level 2:
N = 218
Median RT = 0.74 ms

Confidence Level 3:
N = 363
Median RT = 0.71 ms

Confidence Level 4:
N = 106
Median RT = 0.71 ms    
    
    
'''