#Подключаем подготовленные модули нашего проекта
from pygame import * #Подключаем модуль pygame
import os #Подключаем модуль os
#Подключаем модули нашего проекта
from constant import * #Подключаем модуль файл constant
from sprite import Sprite #Подключаем модуль файл sprite
from graphic_elements import Graphic_elements #Подключаем модуль файл graphic_elements
from text import Font #Подключаем модуль файл text
from sounds import * #Подключаем модуль файл sounds
init() #Инициализируем pygame
#Создаем спрайт и его настройки для создание графических елементов

sprite1 = Sprite(
                    name_image="1", #Имя картинки
                    sprite_x = dict_argument["BLOCK_SIZE"]*dict_argument["sprite_x"],
                    sprite_y = dict_argument["BLOCK_SIZE"]*dict_argument["sprite_y"],
                    sprite_speed = dict_argument["BLOCK_SIZE"]//5, #Скорость спрайта
                    sprite_width = dict_argument["BLOCK_SIZE"], #Ширина спрайта
                    sprite_height = dict_argument["BLOCK_SIZE"]*1.66, #Высота спрайта
                    sprite_gravity_power = SCREEN_H//40, #Сила гравитации спрайта
                    double_jump = dict_argument["DOUBLE_JUMP"], #Двойной прыжок
                    jump_boost = dict_argument["BLOCK_SIZE"]*1.1*3, #Сила прыжка 
                    index_layout = 0 #Индекс   0-стрелки 1 - WSDA
                )                    
#Создаем графические елементы
Circle_invible_block = Graphic_elements(0,0,sprite1.image_sprite.WIDTH,sprite1.image_sprite.HEIGHT,"image/Circle_invible_block.png",None)
Fon =  Graphic_elements(0,0,SCREEN_W,SCREEN_H,"image/backgroubd_room.bmp")
black_fon =  Graphic_elements(0,0,SCREEN_W,SCREEN_H,"image/lvl1.png")
load = Graphic_elements(SCREEN_W-SCREEN_W//10,SCREEN_H-SCREEN_H//10,SCREEN_W//10,SCREEN_H//10,"image/Загрузка/Загрузка0.png")
cloud = Graphic_elements(0,0,SCREEN_W*2,SCREEN_H//3.52,"image/cloud.bmp")
cloud2 = Graphic_elements(SCREEN_W*2,0,SCREEN_W*2,SCREEN_H//3.52,"image/cloud.bmp")
invisible_block_icon = Graphic_elements(SCREEN_W-SCREEN_W//10,SCREEN_H-SCREEN_H//10,SCREEN_W//10,SCREEN_H//10,"image/invisible_block_icon.png")
Rope_with_saw = Graphic_elements(SCREEN_W//2,SCREEN_H//15,int(dict_argument["BLOCK_SIZE"]*1.36),dict_argument["BLOCK_SIZE"]*10,"image/Rope_with_saw.png")
Hook = Graphic_elements(SCREEN_W//2,SCREEN_H//15,SCREEN_W//30,dict_argument["BLOCK_SIZE"]*10,"image/Hook.png")
button = Graphic_elements(0,0,dict_argument["BLOCK_SIZE"],dict_argument["BLOCK_SIZE"]//3.3846,"image/button.png")
achievement_img = Graphic_elements(SCREEN_W,SCREEN_H,SCREEN_W//15,SCREEN_W//15,None,"0")
Background_shooting = Graphic_elements(-SCREEN_W,-SCREEN_H,SCREEN_W*3,SCREEN_H*2,"image/Fon_shooting.png")
dimming = Graphic_elements(0,0,SCREEN_W,SCREEN_H,"image/black.png")
dimming.image_load()
dimming.IMG.set_alpha(round(dict_argument["screen_dimming_count"]))
aim = Graphic_elements(SCREEN_W//2-SCREEN_W//40,SCREEN_H//2-SCREEN_W//40,dict_argument["BLOCK_SIZE"],dict_argument["BLOCK_SIZE"],"image/aim.png")
#Обекты текста
text_transition_new_lvl = Font("font/pixel_font.ttf",SCREEN_W//22,"white",None,0,0,None)
text_select_complexity = Font("font/pixel_font.ttf",SCREEN_W//20,"white","Выберите уровень сложности:",SCREEN_W//20,SCREEN_W//20)
list_button_collid = [
    Font("font/pixel_font.ttf",SCREEN_W//20,"darkgrey",dict_languages_settings["7"][config["language"]],SCREEN_W//1.6,SCREEN_H-SCREEN_W//18),
    Font("font/pixel_font.ttf",SCREEN_W//20,"darkgrey",dict_languages_settings["8"][config["language"]],SCREEN_W//1.4,SCREEN_H-SCREEN_W//18)
]
list_emodji = [
    Graphic_elements(SCREEN_W//20,SCREEN_W//6,SCREEN_W//12,SCREEN_W//12,path="image/Green_emoji.png"),
    Graphic_elements(SCREEN_W//20,SCREEN_W//6 + SCREEN_W//8,SCREEN_W//12,SCREEN_W//12,path="image/Yellow_emoji.png"),
    Graphic_elements(SCREEN_W//20,SCREEN_W//6 + SCREEN_W//4,SCREEN_W//12,SCREEN_W//12,path="image/Red_emoji.png")                 
]   
list_text_emodji = [
    Font("font/pixel_font.ttf",SCREEN_W//20,"white","Легкая",list_emodji[0].X+SCREEN_W//10,list_emodji[0].Y+SCREEN_W//42),
    Font("font/pixel_font.ttf",SCREEN_W//20,"white","Средняя",list_emodji[1].X+SCREEN_W//10,list_emodji[1].Y+SCREEN_W//42),
    Font("font/pixel_font.ttf",SCREEN_W//20,"white","Сложная",list_emodji[2].X+SCREEN_W//10,list_emodji[2].Y+SCREEN_W//42),
]
img_music_player = Graphic_elements(SCREEN_W//50,SCREEN_H-SCREEN_W//25,SCREEN_W//8,SCREEN_W//32,"image/music.png") 
if dict_argument["flag_pause"]:
    img_music_player.path = "image/music_pause.png"
rect_music_left = Rect(img_music_player.X,img_music_player.Y,img_music_player.WIDTH//5,img_music_player.HEIGHT) 
rect_music_right = Rect(img_music_player.X+img_music_player.WIDTH-img_music_player.WIDTH//5,img_music_player.Y,img_music_player.WIDTH//5,img_music_player.HEIGHT) 
rect_music_pause = Rect(img_music_player.X+img_music_player.WIDTH//2.32,img_music_player.Y,img_music_player.WIDTH//7,img_music_player.HEIGHT) 
list_music_name = list()
for i in range(dict_argument["count_music"]):
    list_music_name.append(Music("sounds/bg_"+str(i+1)+".wav",int(config["MUSIC_VOLUME"])/500))
use_sound = Sounds("sounds/use.wav",int(config["SOUNDS_VOLUME"])/100)
#Создаем список графических елементов шипов
list_spikes = []
#Создаем словарь графических елементов
dict_Graphic_elements_obj = {
                        "Circle_invible_block":Circle_invible_block,
                        "Fon":Fon,
                        "load":load,
                        "cloud":cloud,   
                        "cloud2":cloud2,
                        "invisible_block_icon":invisible_block_icon,
                        "Rope_with_saw":Rope_with_saw,
                        "Hook":Hook,
                        "button":button,
                        "text_transition_new_lvl":text_transition_new_lvl,

}