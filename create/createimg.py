from PIL import Image, ImageDraw
import random
import datetime
import os
from asari.api import Sonar

color_start = (0, 0, 0)  # 内側の色　初期値
color_end = (0, 0, 0)  # 外側の色　初期値

def create_colorful_circle(color_start,color_end):
    width = 1000
    height = 1000
    radius = 400
    color_num = 0
    color = (color_num, color_num, color_num)  # 初期の色
    width = height = radius * 2

    # 画像オブジェクトを作成
    image = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # 円の中心座標
    cx = width // 2
    cy = height // 2

    # 円の内側から徐々に変化するように描画
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

def create_pattern(positive_confidence, negative_confidence):

    # 乱数をポジネガのどちらかに依存させる
    diffusion_point_1 = abs(positive_confidence - negative_confidence)
    diffusion_point_2 = positive_confidence + negative_confidence / 2
 
    # 受け取った夢日記の内容に応じて水晶の色を変化
    colorelement_end = 10 * negative_confidence 
    color_start = (random.randint(0,255), random.randint(0,255), random.randint(0,255))  # 内側の色（青）
    color_end = (colorelement_end, colorelement_end, colorelement_end)  # 外側の色（黒）
    width = 800
    height = 800
    sentiment = random.uniform(0, 300)
    # 三乗の値が入ります↓
    random_count = random.randint(8, 15)
    
    positive = positive_confidence
    negative = negative_confidence

    middle_x = 0
    middle_y = 0

    if negative > 0.75:
        middle_x = random.randint(3, 7) / 10
        middle_y = 1 - random.randint(3, 7) / 10
    elif 0.75 > negative > 0.50:
        middle_x = 1 - random.randint(3, 7) / 10
        middle_y = random.randint(3, 7) / 10
    elif 0.50 > negative > 0.25:
        middle_x = 1 - random.randint(3, 7) / 10
        middle_y = 1 - random.randint(3, 7) / 10
    else:
        middle_x = random.randint(3, 7) / 10
        middle_y = random.randint(3, 7) / 10

    star_min_1 = 3

    star_min_2 = 1

    star_min_3 = 0.4

    star_min_4 = 0.1

    # 画像オブジェクトを作成
    image = create_colorful_circle(color_start,color_end)
    draw = ImageDraw.Draw(image)

    if positive > 0.5:
        R_color = random.randint(0,255)
        else_color_1 = min(R_color + colorelement_end, 255)
        else_color_2 = max(R_color - colorelement_end, 0)
        color_start = (R_color, else_color_1, else_color_2)
    elif negative > 0.5:
        G_color = random.randint(0,255)
        else_color_1 = min(G_color + colorelement_end, 255)
        else_color_2 = max(G_color - colorelement_end, 0)
        color_start = (else_color_2, G_color, else_color_1)
    else:
        B_color = random.randint(0,255)
        else_color_1 = min(B_color + colorelement_end, 255)
        else_color_2 = max(B_color - colorelement_end, 0)
        color_start = (else_color_1, else_color_2, B_color)

    # ランダムな模様を追加
    for _ in range(random_count):
        cx1 = random.gauss(diffusion_point_1, diffusion_point_2) * width
        cy1 = random.gauss(diffusion_point_1, diffusion_point_2) * height
        radius = random.weibullvariate(star_min_1, 7)

        sentiment = random.uniform(0, 300)

        if sentiment >200:
            color = (190,190,255)
        elif sentiment < 100:
            color =  (255, 190, 190)
        else:
            color =  (190, 255, 190)

        draw.ellipse([(cx1 - radius, cy1 - radius), (cx1 + radius, cy1 + radius)], fill=color)

        for _ in range(random_count):
            cx2 = random.gauss(diffusion_point_2, diffusion_point_1) * width
            cy2 = random.gauss(diffusion_point_2, diffusion_point_1) * height
            radius = random.weibullvariate(star_min_2, 5)

            sentiment = random.uniform(0, 300)

            if sentiment >200:
                color = (210,210,255)
            elif sentiment < 100:
                color =  (255, 210, 210)
            else:
                color =  (210, 255, 210)

            draw.ellipse([(cx2 - radius, cy2 - radius), (cx2 + radius, cy2 + radius)], fill=color)

            for _ in range(random_count):
                weight = random.randint(int(-negative * 1000), int(positive * 1000))
                weight = weight/100
                cx3 = random.gauss(middle_x, 0.2) * width
                cy3 = random.gauss(middle_y, 0.2) * height
                radius = random.weibullvariate(star_min_3, 1)

                sentiment = random.uniform(0, 300)

                if sentiment >200:
                    color = (225,225,255)
                elif sentiment < 100:
                    color =  (255, 225, 225)
                else:
                    color =  (225, 255, 225)

                draw.ellipse([(cx3 - radius + weight, cy3 - radius + weight), (cx3 + radius + weight, cy3 + radius + weight)], fill=color)

                for _ in range(random_count):
                    weight = random.randint(int(-negative * 1000), int(positive * 1000))
                    weight = weight/100
                    cx4 = random.gauss(middle_x, 0.1) * width
                    cy4 = random.gauss(middle_y, 0.1) * height
                    radius = random.weibullvariate(star_min_4, 0.5)

                    sentiment = random.uniform(0, 300)

                    if sentiment >200:
                        color = (225,225,255)
                    elif sentiment < 100:
                        color =  (255, 225, 225)
                    else:
                        color =  (225, 255, 225)

                    draw.ellipse([(cx4 - radius + weight, cy4 - radius + weight), (cx4 + radius + weight, cy4 + radius + weight)], fill=color)

    return image

def createimg(body):

    # asari言語処理によるスコアの計算
    sonar = Sonar()
    positive_confidence = next(item["confidence"] for item in sonar.ping(text=body)["classes"] if item["class_name"] == "positive")
    negative_confidence = next(item["confidence"] for item in sonar.ping(text=body)["classes"] if item["class_name"] == "negative")
    image = create_pattern(positive_confidence, negative_confidence)
    # 一時的なファイルパスを作成して画像を保存
    now = datetime.datetime.now() 
    directory = "create/createimg"  # 保存先ディレクトリのパスを指定
    filename = f"create_image_{now.strftime('%Y%m%d%H%M%S')}.png"
    file_path = os.path.join(directory, filename)
    image.save(file_path)
