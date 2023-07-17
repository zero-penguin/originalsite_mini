from PIL import Image, ImageDraw
import random
import datetime
import os

color_start = (0, 0, 0)  # 内側の色（青）
color_end = (0, 0, 255)  # 外側の色（黒）

def create_colorful_circle(color_start,color_end):
    width = 800
    height = 800
    radius = 400
    color_num = 40
    color = (color_num, color_num, color_num)  # 初期の色
    width = height = radius * 2


    # 画像オブジェクトを作成
    image = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # 円の中心座標
    cx = width // 2
    cy = height // 2

    # 円の内側から徐々に青から黒になるように描画
    for r in range(radius, 0, -1):
        # 円の色を計算
        ratio = r / radius  # 内側からの比率
        red = int(color_start[0] * ratio + color_end[0] * (1 - ratio))
        green = int(color_start[1] * ratio + color_end[1] * (1 - ratio))
        blue = int(color_start[2] * ratio + color_end[2] * (1 - ratio))
        color = (red, green, blue)

        # 円を描画
        draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=color)

    return image

def create_pattern():

    color_start = (0, 0, 255)  # 内側の色（青）
    color_end = (0, 0, 0)  # 外側の色（黒）
    width = 800
    height = 800
    sentiment = random.uniform(0, 300)
    random_count = random.randint(80, 100)
    start = 0
    midlle = 0.5

    # 画像オブジェクトを作成
    image = create_colorful_circle(color_start,color_end)
    draw = ImageDraw.Draw(image)

    # ランダムな模様を追加
    for _ in range(random_count):
        cx1 = random.gauss(start, 0.2) * width
        cy1 = random.gauss(start, 0.2) * height
        radius = random.weibullvariate(0.1, 3)

        sentiment = random.uniform(0, 300)

        if sentiment >200:
            color = (245,245,255)
        elif sentiment < 100:
            color =  (255, 245, 245)
        else:
            color =  (245, 255, 245)

        draw.ellipse([(cx1 - radius, cy1 - radius), (cx1 + radius, cy1 + radius)], fill=color)

        for _ in range(random_count):
            cx = random.gauss(midlle, 0.2) * width
            cy = random.gauss(midlle, 0.2) * height
            radius = random.weibullvariate(0.1, 3)

            sentiment = random.uniform(0, 300)

            if sentiment >200:
                color = (245,245,255)
            elif sentiment < 100:
                color =  (255, 245, 245)
            else:
                color =  (245, 255, 245)

            draw.ellipse([(cx - radius, cy - radius), (cx + radius, cy + radius)], fill=color)

    return image

def createimg():

    image = create_pattern()
    # 一時的なファイルパスを作成して画像を保存
    now = datetime.datetime.now() 
    directory = "create/createimg"  # 保存先ディレクトリのパスを指定
    filename = f"create_image_{now.strftime('%Y%m%d%H%M%S')}.png"
    file_path = os.path.join(directory, filename)
    image.save(file_path)
