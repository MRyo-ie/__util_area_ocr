


import os
from PIL import Image
import pyautogui as gui
import pyocr
import pyocr.builders
import sys


def mean(a, b):
    return int((a+b)/2)


if __name__ == "__main__":
    # 事前準備
    tmp_img_path = 'res/screen_tmp.png'
    os.makedirs('res', exist_ok=True)


    # 座標の大きさにズレがあるっぽいので、0~1 の相対座標にしてみる。

    # 参考： https://boook24.com/?p=348
    print('中断するにはCrt+Cを入力してください。')
    
    points = []
    try:
        for i in range(2):
            x = input(f"{i+1}点目にマウスを移動 → Enterキー押してください。\n")
            points.append(gui.position())
            print(f"OK!\n座標：{points[i]}\n")

    except KeyboardInterrupt:
        print('\n終了')
        sys.exit()

    # 矩形 を計算する。
    x_min = min(points[0][0], points[1][0])
    y_min = min(points[0][1], points[1][1])

    # スクショ
    # 参考： https://qiita.com/eito_2/items/1974f3cfa1f4d101378d
    # スクリーンショット（全体）を取得する。
    img = gui.screenshot()

    # gui.position() の最大値
    screen_x, screen_y = gui.size()
    print(screen_x, screen_y)
    # gui.position()  と  gui.screenshot()  の縮尺の違いを吸収する。
    ratio_x = (img.width / screen_x)
    ratio_y = (img.height / screen_y)

    # スクリーンショットした画像は表示しきれないので画像リサイズ
    x = int(x_min * ratio_x) #+ mean(points[0][0], points[1][0])
    y = int(y_min * ratio_y) # + mean(points[0][1], points[1][1])
    w_adj = int(abs(points[0][0] - points[1][0]) * ratio_x)
    h_adj = int(abs(points[0][1] - points[1][1]) * ratio_y)

    # region = (left_x, top_y, width, height)
    print(f'(left_x, top_y, width, height) = ({x}, {y}, {w_adj}, {h_adj})')
    screenshot = gui.screenshot(region=(x, y, w_adj, h_adj))
    screenshot.save(tmp_img_path)

    # img = Image.open(tmp_img_path)
    # img.show()


    # Tesseract OCR
    # 参考：https://chusotsu-program.com/python-tesseract-pyocr/
    # 切り出した領域に OCRする。（Tesseract OCR）
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found")
        sys.exit(1)
    
    tool = tools[0]
    # print("Will use tool '%s'" % (tool.get_name()))

    txt = tool.image_to_string(
        Image.open(tmp_img_path),
        lang="jpn",
        builder = pyocr.builders.TextBuilder(tesseract_layout=6)
    )
    print(txt.replace(' ', ''))

    # ファイルに保存
    with open('res/ocr.txt', 'w') as f:
        f.write(txt)

