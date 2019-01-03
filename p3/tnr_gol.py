import pyxel
from time import sleep
from lib.game_of_life import GameOfLife
from lib.Tenorion import Tenorion


gol=GameOfLife()

class App:
    def __init__(self):
        pyxel.init(180,180)
        pyxel.mouse(False)

        self.tnr = Tenorion() # tenorion initialize
        self.init_tenorion()
        self.tnr.play()

        pyxel.run(self.update, self.draw )


    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            self.reset_tenorion()
            pyxel.quit()

        elif pyxel.btnp(pyxel.KEY_R):
            gol.reset()
            self.reset_tenorion()
            self.tnr.play()

        

    def draw(self):
        pyxel.cls(0)

        #次世代セルを計算
        matrix=gol.calc_state()
        
        #表示情報の取得( 1を黒, 0を白で表示)
        img=gol.create_matrix_img(matrix)

        # 表示をアップデート
        self.draw_pyxel_matrix(img)
        sleep(2)
        

    def draw_pyxel_matrix(self,img):
        tnr=self.tnr
        midi_lists=[]
        layer=4

        scale=0 
        if img.sum()>0:
            scale= int(img.sum()/255%7)

        tnr.common_param_change(2,0,scale) #scale変更

        for y, values in enumerate(img):
            for x, val in enumerate(values):
                if val==255:
                    pyxel.rect(x*10+10 ,y*10+10,x*10+10+10 ,y*10+10+10,col=0)
                    midi_lists.append(tnr.led_hold_on_off(on_off=False,x=x,y=y,layer=layer,is_play=False))                

                elif val==0:
                    pyxel.rect(x*10+10 ,y*10+10,x*10+10+10 ,y*10+10+10,col=7)
                    midi_lists.append(tnr.led_hold_on_off(on_off=True,x=x,y=y,layer=layer,is_play=False))                

        tnr.current_layer_change(layer=layer)
        tnr.execute_midi_lists(midi_lists)

    
    def init_tenorion(self):
        tnr=self.tnr
        tnr.remote_on(is_intialize=True)   
        tnr.clear_all_block_and_layer()
        tnr.current_block_change(0)
        tnr.current_layer_change(0)

        for layer in range(6):
            tnr.layer_parameter_change(2,0,3,layer) #speed
            tnr.layer_parameter_change(6,0,0,layer) #animation_type
            tnr.layer_parameter_change(7,0,1,layer) #animation_size
            tnr.layer_parameter_change(8,0,0,layer) #animation_direction        

        tnr.common_param_change(2,0,0) #scale
        tnr.common_param_change(4,0,2) #scroll speed
        tnr.common_param_change(7,0,0) #loop_timing
        tnr.common_param_change(3,0,64)#key default


    def reset_tenorion(self):
        tnr=self.tnr
        tnr.clear_all_block()
        tnr.pause()
        tnr.clear_all_block_and_layer()



if __name__=='__main__':
    App()