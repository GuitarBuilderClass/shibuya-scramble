import cv2
import os
from datetime import datetime
from time import time

VIDEO_PATH = "../data/mov/test.mp4"  # 画像に分割する対象の動画パス
CAPTURE_PER_SECONDS = 60  # 29.73FPSをベースとして、何秒に1枚の画像を保存するか


os.makedirs("../data/pics", exist_ok=True)
base_path = os.path.join("../data/pics", "test.mp4")
basename = os.path.splitext(base_path)[0]

# CV2で動画をキャプチャする
cap = cv2.VideoCapture(VIDEO_PATH)

# 動画のFPSを取得し、thresholdフレームに1回キャプチャするための値を取得する
read_fps = cap.get(cv2.CAP_PROP_FPS)
threshold = read_fps * CAPTURE_PER_SECONDS

frame_counter = 0
n = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("frame", frame)

    # frame_counterがthresholdの値を超えるか、nが0のとき(冒頭を記録するため)は画像をキャプチャーする
    if threshold <= frame_counter or n == 0:
        tmp_filename = "{}_{}.jpg".format(basename, str(n).zfill(4))
        cv2.imwrite(tmp_filename, frame)
        n += 1
        frame_counter = 0
        print(datetime.fromtimestamp(time()).strftime("[%H:%M:%S.%f]"), tmp_filename)

    frame_counter += 1

    # qキーを押したら処理から抜ける
    key = cv2.waitKey(20) & 0xFF
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
