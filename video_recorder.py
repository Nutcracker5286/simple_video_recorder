import numpy as np
import cv2 as cv

# 캠 열기
video=cv.VideoCapture(0)

# 캠 열림 여부 확인
if not video.isOpened():
    print('웹캠 열기 실페')
    exit()

codec=[ "XVID", "MJPG", "DIVX", "H264"]
print('코덱을 선택하시오')
print('1번XVID,  2번 MJPG, 3번 DIVX, 4번 H264')
codec_idx=input()
codec_idx=int(codec_idx)-1
fourcc=cv.VideoWriter_fourcc(*codec[codec_idx])
mode=False
frame_total = int(video.get(cv.CAP_PROP_FRAME_COUNT))
frame_shift = 10
speed_table = [1/10, 1/8, 1/4, 1/2, 1, 2, 3, 4, 5, 8, 10]
speed_index = 4
fps = video.get(cv.CAP_PROP_FPS)
wait_msec = int(1 / fps * 1000)
target=cv.VideoWriter()
recording=False

while True:
    # 웹캠으로부터 이미지 얻기
    valid, img =video.read()
    if not valid:
        break
    
    #이미지 보여주기
    frame = int(video.get(cv.CAP_PROP_POS_FRAMES))
    info = f'Frame: {frame}/{frame_total}, Speed: x{speed_table[speed_index]:.2g}'
    cv.putText(img, info, (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))
    if recording:
        cv.putText(img, 'recording', (30, 50), cv.FONT_HERSHEY_DUPLEX, 0.5, (0,0, 255))
        target.write(img)
    else:
        cv.putText(img, 'not recording', (30, 50), cv.FONT_HERSHEY_DUPLEX, 0.5, (0,0, 255))
    cv.imshow('Video Player', img)

    if not target.isOpened() and recording:
        h,w,*_=img.shape
        is_color = (img.ndim > 2) and (img.shape[2] > 1)
        cv.destroyAllWindows()
        
        target.open('output.avi', cv.VideoWriter_fourcc(*codec[codec_idx]), fps, (w, h), is_color)
        target.write(img)

    # Process the key event
    key = cv.waitKey(max(int(wait_msec / speed_table[speed_index]), 1))
    if key == ord('q'):       
        key = cv.waitKey()
    if key == ord(' '):
        recording=not recording
    if key == 27: # ESC
        break
    elif key == ord('\t'):
        speed_index = 4
    elif key == ord('>') or key == ord('.'):
        speed_index = min(speed_index + 1, len(speed_table) - 1)
    elif key == ord('<') or key == ord(','):
        speed_index = max(speed_index - 1, 0)
    elif key == ord(']') or key == ord('}'):
        video.set(cv.CAP_PROP_POS_FRAMES, frame + frame_shift)
    elif key == ord('[') or key == ord('{'):
        video.set(cv.CAP_PROP_POS_FRAMES, max(frame - frame_shift, 0))
    elif key == ord('[') or key == ord('{'):
        video.set(cv.CAP_PROP_POS_FRAMES, max(frame - frame_shift, 0))