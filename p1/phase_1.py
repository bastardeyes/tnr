import numpy as np
import pandas as pd

import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
import pygame
import pygame.midi

from pygame.locals import *

import sys
from pygame.locals import QUIT

from lib.Tenorion import Tenorion
from lib.TextConvert import TextConvert
import tkinter as tk
from tkinter import messagebox,font

from time import sleep



class Tkinter_app(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.create_widgets()

    def create_widgets(self):
        my_font =font.Font(root,family="Helvetica",size=40,weight="bold")
        self.input_box=tk.Entry(width=20,font=my_font)
        self.input_box.grid(row=0,column=0,columnspan=4, padx=5, pady=30,sticky=(tk.N, tk.S, tk.E, tk.W))#

        self.clear_btn=tk.Button(width=5, fg='#696969',font=my_font,relief="raised"     ) #
        self.clear_btn["borderwidth"]=5
        self.clear_btn["text"]="クリア"
        self.clear_btn["command"]=self.clear_input_value
        self.clear_btn.grid(row=1,column=1,padx=5, pady=10,sticky=(tk.N, tk.S, tk.E, tk.W))#,sticky=(tk.N, tk.S, tk.E, tk.W)

        self.exec_btn=tk.Button(width=5,fg="#ff6347",font=my_font)
        self.exec_btn["text"]="実行"
        self.exec_btn["command"]=self.execute_input_value
        self.exec_btn.grid(row=1,column=2,padx=5, pady=10,sticky=(tk.N, tk.S, tk.E, tk.W))#,sticky=(tk.N, tk.S, tk.E, tk.W)

    def clear_input_value(self):
        self.input_box.delete(0, tk.END)

    def execute_input_value(self):
        try:
            exec_button=self.exec_btn
            #exec_button.fg="#dddddd"
            msg = self.input_box.get()
            if len(msg)>0:
                pray_tenorion(msg)
                self.input_box.delete(0, tk.END)


        except Exception as e:
            messagebox.showinfo("ERROR!!",e)

def pray_tenorion(text):

    try:
        #print(text)
        txt_cnv= TextConvert()

        bmp_image = txt_cnv.convert_txt_to_bmp(text=text,size=8)

        # pandasのpanel。16桁のデータ+block+layer。
        pf=txt_cnv.convert_bmp_to_panel(bmp_image)

        # tnr初期化
        tnr = Tenorion()

        tnr.play()

        append_row=3

        for i in range(len(pf)):

            df =pf.ix[i]

            midi_lists= []

            layer=df.layer[0]
            block=df.block[0]

            tnr.current_block_change(block=block)

            for row in df.itertuples(name=None):
                y=row[0]+append_row
                for x, on_off in enumerate(row[1:-3]):
                    midi_lists.append(tnr.led_hold_on_off(on_off=on_off,x=x,y=y,layer=layer,is_play=False))

            tnr.current_layer_change(layer=layer)
            tnr.execute_midi_lists(midi_lists)
            sleep(1.25)

        del pf

        tnr.clear_all_block()

        tnr.pause()
        tnr.clear_all_block_and_layer()

    except Exception as e:
        print(e)
        tnr.pause()
        tnr.remote_off()



if __name__=='__main__':

    root = tk.Tk()
    root.title("電光掲示板")
    root.geometry("630x400")
    root.config(bg="#f5f5f5")

    app=Tkinter_app(master=root)
    app.grid(column=0, row=1)
    app.mainloop()
