from PIL import Image, ImageDraw
import random
import datetime

def createimg():

    # 画像サイズと背景色を指定
    width = 500
    height = 500
    background_color = (255, 255, 255)  # RGB形式で指定

    # 画像オブジェクトを作成
    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # ランダムな図形を描画
    shape = random.choice(["rectangle", "ellipse"])  # 描画する図形をランダムに選択

    if shape == "rectangle":
        x1 = random.randint(0, width // 2)
        y1 = random.randint(0, height // 2)
        x2 = random.randint(width // 2, width)
        y2 = random.randint(height // 2, height)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        draw.rectangle([x1, y1, x2, y2], fill=color)

    elif shape == "ellipse":
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(x1, width)
        y2 = random.randint(y1, height)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        draw.ellipse([x1, y1, x2, y2], fill=color)

    # 画像を保存
    now = datetime.datetime.now()
    filename = f"random_image_{now.strftime('%Y%m%d%H%M')}.png"
    image.save(filename)
