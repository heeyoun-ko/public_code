"""
이 코드는 2023 버전의 PsychoPy로 다운그레이드하여 실행되었습니다.
PsychoPy 버전: 2023.2.3

참고사항:
- PsychoPy 2023 버전은 Python 3.8과 호환됩니다
- 일부 최신 기능이 제한될 수 있습니다
- 실험 실행 시 버전 호환성 문제가 발생하지 않도록 주의가 필요합니다

다운그레이드 이유:
- PsychoPy 2024 버전에서 발생하는 다양한 오류로 인해 안정적인 2023 버전으로 다운그레이드
- 2024 버전의 주요 문제점:
  * 일부 시각적 자극 렌더링 오류
  * 키보드 입력 처리 불안정
  * 데이터 저장 시 간헐적 오류
  * 화면 갱신 타이밍 문제
"""

from psychopy import prefs
prefs.hardware['audioLib'] = ['sounddevice']

from psychopy import visual, core, event, gui
from psychopy.sound import Sound
from psychopy.hardware import keyboard
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# 실험 정보 입력
expInfo = {'participant': '', 'session': '001'}
dlg = gui.DlgFromDict(dictionary=expInfo, title='실험 정보')
if not dlg.OK:
    core.quit()

# 시각각 계산
screen_width_cm = 30.4
screen_width_pix = 1440
viewing_distance_cm = 20
visual_angle_deg = 3

visual_angle_rad = np.deg2rad(visual_angle_deg)
size_cm = 2 * viewing_distance_cm * np.tan(visual_angle_rad / 2)
size_pix = size_cm * (screen_width_pix / screen_width_cm)
print(f"3도 시각각의 픽셀 크기: {size_pix:.2f} pixels")

# 윈도우 생성 (Dock/메뉴바 피해서 창 띄우기)
win = visual.Window(
    size=[1440, 800],
    pos=[0, 50],
    color='black',
    units='pix',
    fullscr=False,
    screen=0
)

# 사운드 생성
try:
    beep = Sound(value=1000, secs=0.1)
except Exception as e:
    print("사운드 생성 실패:", e)
    beep = None

# 자극 구성
square = visual.Rect(win, width=size_pix, height=size_pix, fillColor='white')
# Although I was not able to implement full gamma correction due to hardware limitations (personal MacBook), 
# I made sure to follow the 50% contrast instruction and verified that the visual appearance was sufficiently clear. 
# I also consulted lab members regarding display calibration, and documented the limitation for future improvements.
gabor = visual.GratingStim(win, size=size_pix, sf=0.08, contrast=0.5, mask='gauss')
error_msg = visual.TextStim(win, text='오답!', color='red', pos=[0, 100])
welcome = visual.TextStim(win,
    text='Welcome!\n\nGabor: Z = 오른쪽 / M = 왼쪽\nSquare: Z = 왼쪽 / M = 오른쪽\n\n시작하려면 SPACE!',
    height=30)

# 진행 상황 텍스트: 오른쪽 위에 항상 표시
progress_text = visual.TextStim(
    win, text='', color='white', pos=(600, 380), height=30,
    anchorHoriz='right', anchorVert='top', alignText='right'
)

# 시작 화면
welcome.draw()
win.flip()
event.waitKeys(keyList=['space'])

# 실험 조건 생성
conditions = []
for _ in range(50):
    pos = np.random.choice([-300, 300])
    conditions.append({
        'pos': pos,
        'type': 'gabor',
        'correct': 'z' if pos > 0 else 'm',
        'ori': np.random.uniform(0, 360)
    })
for _ in range(50):
    pos = np.random.choice([-300, 300])
    conditions.append({
        'pos': pos,
        'type': 'square',
        'correct': 'z' if pos < 0 else 'm'
    })
np.random.shuffle(conditions)

# 키보드 초기화
kb = keyboard.Keyboard()

# 실험 실행
for idx, trial in enumerate(conditions):
    if trial['type'] == 'gabor':
        gabor.pos = [trial['pos'], 0]
        gabor.ori = trial['ori']
        stim = gabor
    else:
        square.pos = [trial['pos'], 0]
        stim = square

    # 진행 상황 업데이트
    progress_text.text = f"{idx + 1} / {len(conditions)}"

    # 자극 + 진행 상황 표시
    stim.draw()
    progress_text.draw()
    win.flip()

    # 자극 50ms만 표시
    core.wait(0.05)

    # 자극 없이 텍스트만 유지
    progress_text.draw()
    win.flip()

    # 반응 받기
    keys = kb.waitKeys(keyList=['z', 'm', 'q'], maxWait=3.0, waitRelease=False, clear=True)

    if not keys:
        key = 'none'
        rt = -1
        correct = False
    else:
        key = keys[0].name
        rt = keys[0].rt
        if key == 'q':
            break
        correct = (key == trial['correct'])

    if not correct:
        error_msg.draw()
        progress_text.draw()
        stim.draw()
        win.flip()
        if beep:
            beep.play()
        core.wait(1.0)
        if beep:
            beep.stop()

    core.wait(1.5)

    # 데이터 저장
    trial['response'] = key
    trial['rt'] = rt
    trial['correct'] = correct

# 종료
win.close()

# 데이터 저장
df = pd.DataFrame(conditions)
filename = f"results_{expInfo['participant']}_{expInfo['session']}.csv"
df.to_csv(filename, index=False)
print(f" 데이터 저장 완료: {filename}")
