import sys
import struct

from lib.Tenorion import Tenorion
from lib.Pac import Pac
from lib.ADXL345 import ADXL345


from time import sleep
import time

if sys.version > '3':
   buffer = memoryview

RUNTIME=40.0
DEFAULT_SLEEP=1

def main():
    pray_tenorion_pac()    


def create_init_data(pac,tnr,layer):
    midi_lists= []

    init_led_state = pac.PARMANENT_LED_ON + pac.TO_RIGHT_LED_ON + pac.WALK_TYPE_1
    on_off=True
        
    for i in range(len(init_led_state)):            
        x = init_led_state[i][0]
        y = init_led_state[i][1]
        midi_lists.append(tnr.led_hold_on_off(on_off=on_off,x=x,y=y,layer=layer,is_play=False))
    
    return midi_lists

def create_direction_data(pac,tnr,layer,direction,on_off):
    midi_lists= []

    if direction=="right" and on_off==True:
        led_state = pac.TO_RIGHT_LED_ON 
    elif direction=="right" and on_off==False:
        led_state = pac.TO_RIGHT_LED_OFF
    elif direction=="left" and on_off==True:
        led_state = pac.TO_LEFT_LED_ON 
    elif direction=="left" and on_off==False:
        led_state = pac.TO_LEFT_LED_OFF
    elif direction=="up" and on_off==True:
        led_state = pac.TO_UP_LED_ON 
    elif direction=="up" and on_off==False:
        led_state = pac.TO_UP_LED_OFF
    elif direction=="down" and on_off==True:
        led_state = pac.TO_DOWN_LED_ON 
    elif direction=="down" and on_off==False:
        led_state = pac.TO_DOWN_LED_OFF
    else :
        return midi_lists

    for i in range(len(led_state)):            
        x = led_state[i][0]
        y = led_state[i][1]
        midi_lists.append(tnr.led_hold_on_off(on_off=on_off,x=x,y=y,layer=layer,is_play=False))    
    
    return midi_lists

def create_foot_data(pac,tnr,layer,foot_mode):
    midi_lists= []

    if foot_mode % 2 ==1 :
        on_off=True
    else :
        on_off=False

    for i in range(len(pac.WALK_TYPE_1)):            
        x = pac.WALK_TYPE_1[i][0]
        y = pac.WALK_TYPE_1[i][1]
        midi_lists.append(tnr.led_hold_on_off(on_off=on_off,x=x,y=y,layer=layer,is_play=False))
        
    for i in range(len(pac.WALK_TYPE_2)):            
        x = pac.WALK_TYPE_2[i][0]
        y = pac.WALK_TYPE_2[i][1]
        midi_lists.append(tnr.led_hold_on_off(on_off= not on_off,x=x,y=y,layer=layer,is_play=False))

    return midi_lists


def pray_tenorion_pac():
    sleep_time=DEFAULT_SLEEP

    try:
        #初期化
        pac = Pac()
        adxl345 = ADXL345()

        tnr = Tenorion()
        tnr.clear_all_block_and_layer() 

        
        layer = 3
        tnr.current_layer_change(layer=layer)
        tnr.common_param_change(2,0,8)#沖縄スケール
        tnr.common_param_change(3,0,64)#キーdefault


        # アイコンの初期データ作成
        midi_lists = create_init_data(pac,tnr,layer)
        
        tnr.execute_midi_lists(midi_lists)
        tnr.remote_on()
        tnr.play()
        sleep(sleep_time)

        foot_mode=0

        while (time.time()-adxl345.start_time) < RUNTIME:

            midi_lists = create_foot_data(pac,tnr,layer,foot_mode)

            (s, b) = adxl345.pi.i2c_read_i2c_block_data(adxl345.h, 0x32, 6)

            if s >= 0:
                (x, y, z) = struct.unpack('<3h', buffer(b))
                
                y +=180 # 本体は水平に持たないので、斜めに持つのに合わせて補正。

                if x<30 and x>-30 and y<30 and y>-30 :
                    sleep_time=DEFAULT_SLEEP
                    tnr.common_param_change(4,0,2)#速度普通
                    tnr.common_param_change(3,0,64)#キーdefault

                elif (abs(x) - abs(y)) > 0 :
                    tnr.common_param_change(3,0,64)#キーdefault

                    if x < 0:
                        #print("=>")
                        #sleep_time=3
                        sleep_time=0.5
                        midi_lists += create_direction_data(pac,tnr,layer,direction="right",on_off=True)
                        midi_lists += create_direction_data(pac,tnr,layer,direction="right",on_off=False)  
                        tnr.common_param_change(4,0,4)#速度遅い
                    else :
                        #print("<=")
                        #sleep_time=0.5
                        sleep_time=3

                        midi_lists += create_direction_data(pac,tnr,layer,direction="left",on_off=True)
                        midi_lists += create_direction_data(pac,tnr,layer,direction="left",on_off=False)
                        tnr.common_param_change(4,0,1)#速度速い
                else :
                    sleep_time=DEFAULT_SLEEP
                    tnr.common_param_change(4,0,2)#速度普通

                    if y<0:
                        #print("↓")
                        midi_lists += create_direction_data(pac,tnr,layer,direction="down",on_off=True)
                        midi_lists += create_direction_data(pac,tnr,layer,direction="down",on_off=False)                        
                        tnr.common_param_change(3,0,57)#キー 低い
                        
                    else :
                        #print("↑")
                        midi_lists += create_direction_data(pac,tnr,layer,direction="up",on_off=True)
                        midi_lists += create_direction_data(pac,tnr,layer,direction="up",on_off=False)
                        tnr.common_param_change(3,0,72)#キー高い
                        
                #print("{0} {1} {2}".format(x, y, z))
                adxl345.read += 1

            tnr.execute_midi_lists(midi_lists)
            sleep(sleep_time)
            foot_mode += 1  

        adxl345.pi.i2c_close(adxl345.h)
        adxl345.pi.stop()
 

        sleep(3)
        tnr.clear_all_block()

        tnr.pause()
        tnr.clear_all_block_and_layer()

        del tnr
        del pac
        
    except Exception as e:
        print(e)
        tnr.pause()
        #tnr.remote_off()
    
    

if __name__=='__main__':
    main()
