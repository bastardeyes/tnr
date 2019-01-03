import numpy as np
import pandas as pd

import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

import pygame
from pygame.locals import *

import sys
from pygame.locals import QUIT


class TextConvert:
    def __init__(self):
        pass

    def convert_txt_to_bmp(self,text="",size=16):
        text_len = len(text)
        image = Image.new('1', (text_len*size, size))
        font  = ImageFont.truetype("./font/misaki_gothic.ttf", size, encoding='unic')
        draw  = ImageDraw.Draw(image)
        draw.text((0,1), text, font=font, fill=255)

        return image #bmpと同じデータ

    def convert_char_to_bmp(self,char="",size=16):
        image = Image.new('1', (size, size))
        font  = ImageFont.truetype("./font/misaki_gothic.ttf", size, encoding='unic')
        print(char)
        draw  = ImageDraw.Draw(image)
        draw.text((0,1), char, font=font, fill=255)

        #image.show()
        return image #bmpと同じデータ

    def convert_bmp_to_bit_array(self,bmp_image):
        # pilIN = PIL.Image.open("./img/font.bmp").convert("1") #ファイル使う場合はこれ
        pilIN = bmp_image.convert("1")
        bit_array = np.asarray(pilIN,np.bool8) #読み込みモードとしてbool8
        return bit_array

    def convert_bmp_to_panel(self,bmp_image,size=16):
        pilIN = bmp_image.convert("1")
        bit_array = np.asarray(pilIN,np.bool8) #読み込みモードとしてbool8

        df=pd.DataFrame(bit_array)

        df_columns=[]
        for i in range(len(bit_array[0])):
            df_columns.append(i)

        layer_list=[0,1,2,3,4,5,6] #score_mode = 1 to 7
        block_list=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]

        layer_cnt=0
        block_cnt=0
        num=0

        dict_df={}

        for i in df_columns:
            layer=layer_list[layer_cnt]
            block=block_list[block_cnt]

            key="df"+"{0:03d}".format(i)

            if i==0 or i % 2 == 0:
                #dfを1列ずつずらして取得
                dict_df[key]=df.iloc[:, df_columns[i:(i+size)]]

                col_name=df_columns[0:len(df_columns[i:(i+size)])]
                dict_df[key].columns=col_name

                dict_df[key]["block"]=block
                dict_df[key]["layer"]=layer
                dict_df[key]["no"]=num

            num=num+1
            layer_cnt=layer_cnt+1

            if layer_cnt ==7:
                layer_cnt=0
                block_cnt=block_cnt+1

            if block_cnt==16:
                block_cnt=0

        pf = pd.Panel(dict_df).fillna(False)

        return pf
