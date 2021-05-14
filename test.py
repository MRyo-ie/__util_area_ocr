
import pyautogui as gui
import os

from PIL import Image


if __name__ == "__main__":
    tmp_img_path = 'res/screen_tmp.png'
    os.makedirs('res', exist_ok=True)

    screen_x,screen_y = gui.size()
    print(screen_x,screen_y)

    # スクショ
    # 参考： https://qiita.com/eito_2/items/1974f3cfa1f4d101378d
    # region = (center_x, center_y, width, height)
    screenshot = gui.screenshot()  # < Point(x=1679, y=1049)
    # screenshot = gui.screenshot(region = (0, 0, 1679, 1049))  # < Point(x=1679, y=1049)
    print(screenshot.width)
    screenshot.save(tmp_img_path)

    img = Image.open(tmp_img_path)
    img.show()

