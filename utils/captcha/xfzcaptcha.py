import random
from PIL import Image, ImageDraw, ImageFont
import time
import os
import string


class Captcha(object):
    font_path = os.path.join(os.path.dirname(__file__), 'verdana.ttf')
    # 生成几位数的验证码
    number = 4
    # 生成验证码的宽度和高度
    size = (100, 40)
    # 背景颜色
    bgcolor = (0, 0, 0)
    # 随机字体颜色
    random.seed(int(time.time()))
    fontcolor = (random.randint(200, 255), random.randint(100, 255), random.randint(100, 255))
    # 验证码字体大小
    fontsize = 20
    # 随机干扰线颜色
    linecolor = (random.randint(0, 250), random.randint(0, 255), random.randint(0, 250))
    # 是否要加入干扰线
    draw_line = True
    # 是否要加入噪点
    draw_point = True
    # 加入干扰线的条数
    line_number = 3

    SOURCE = list(string.ascii_letters)  # string.ascii_letters生成包含a-z和A-Z的字符串
    for index in range(0, 10):
        SOURCE.append(str(index))

    # 生成验证码字符
    @classmethod
    def gene_text(cls):
        return ''.join(random.sample(cls.SOURCE, cls.number))  # 用join转化为字符串

    # 绘制干扰线
    @classmethod
    def __gene_line(cls, draw, width, height):
        begin = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([begin, end], fill=cls.linecolor)

    @classmethod
    def __gene_points(cls, draw, point_chance, width, height):
        chance = min(100, max(0, int(point_chance)))  # 大小限制在0-100
        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=(0, 0, 0))

    @classmethod
    def gene_code(cls):
        width, height = cls.size
        image = Image.new('RGBA', (width, height), cls.bgcolor)  # 创建画板
        font = ImageFont.truetype(cls.font_path, cls.fontsize)  # 验证码的字体及其大小
        draw = ImageDraw.Draw(image)  # 在image上 创建画笔
        text = cls.gene_text()
        font_width, font_height = font.getsize(text)
        draw.text(((width - font_width) / 2, (height - font_height) / 2), text,
                  font=font, fill=cls.fontcolor)
        if cls.draw_line:
            for x in range(0, cls.line_number):
                cls.__gene_line(draw, width, height)
        if cls.draw_point:
            cls.__gene_points(draw, 10, width, height)

        return text, image
