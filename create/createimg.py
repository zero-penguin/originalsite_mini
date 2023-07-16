from PIL import Image, ImageDraw
import random
import datetime
import os
from textblob import TextBlob

def create_pattern(sentiment):
    width = 500
    height = 500

    # 画像オブジェクトを作成
    image = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # 感情に基づいて模様を描画
    if sentiment > 0.5:
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    elif sentiment < -0.5:
        color = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))
    else:
        color = (random.randint(100, 200), random.randint(100, 200), random.randint(100, 200))

    draw.rectangle([(0, 0), (width, height)], fill=color)

    # ランダムな模様を追加
    for _ in range(50):
        shape = random.choice(["rectangle", "ellipse"])
        x0 = random.randint(0, width-50)
        y0 = random.randint(0, height-50)
        x1 = x0 + random.randint(10, 50)
        y1 = y0 + random.randint(10, 50)

        if sentiment > 0.5:
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        elif sentiment < -0.5:
            color = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))
        else:
            color = (random.randint(100, 200), random.randint(100, 200), random.randint(100, 200))

        if shape == "rectangle":
            draw.rectangle([(x0, y0), (x1, y1)], fill=color)
        elif shape == "ellipse":
            draw.ellipse([(x0, y0), (x1, y1)], fill=color)

    return image

def createimg(body):
    # テキストの感情分析
    sentiment = TextBlob(body).sentiment.polarity

    # 感情に基づいて模様を生成
    image = create_pattern(sentiment)

    # 一時的なファイルパスを作成して画像を保存
    now = datetime.datetime.now()
    directory = "create/createimg"  # 保存先ディレクトリのパスを指定
    filename = f"create_image_{now.strftime('%Y%m%d%H%M%S')}.png"
    file_path = os.path.join(directory, filename)
    image.save(file_path)
