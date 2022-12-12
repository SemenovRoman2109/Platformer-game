#Подключаем подготовленные модули нашего проекта
from pygame import * #Подключаем модуль pygame
import os #Подключаем модуль os
#Подключаем модули нашего проекта
from constant import * #Подключаем модуль файл constant
from sprite import Sprite #Подключаем модуль файл sprite
from graphic_elements import Graphic_elements #Подключаем модуль файл graphic_elements
init() #Инициализируем pygame
#Создаем спрайт и его настройки для создание графических елементов
sprite1 = Sprite(
                    name_image="1", #Имя картинки
                    sprite_x = 0, #Горизонтальное расположение спрайта
                    sprite_y = SCREEN_H-SCREEN_H//10*2.5, #Вертикальное расположение спрайта
                    sprite_speed = SCREEN_W//100, #Скорость спрайта
                    sprite_width = SCREEN_W//20, #Ширина спрайта
                    sprite_height = SCREEN_H//11*1.66, #Высота спрайта
                    border_width = SCREEN_W, #Ширина контура
                    border_height = SCREEN_H, #Высота контура
                    sprite_gravity_power = SCREEN_H//40, #Сила гравитации спрайта
                    double_jump = False, #Двойной прыжок
                    jump_boost = SCREEN_H//10*3, #Сила прыжка
                    index_layout = 0 #Индекс
                )                    
#Создаем графические елементы
Circle_invible_block = Graphic_elements(sprite1.sprite_x,sprite1.sprite_y,sprite1.image_sprite.WIDTH,sprite1.image_sprite.HEIGHT,"image/Circle_invible_block.png",None)
Fon =  Graphic_elements(0,0,SCREEN_W,SCREEN_H,"image/фон.bmp")
black_fon =  Graphic_elements(0,0,SCREEN_W,SCREEN_H,"image/lvl1.png")
load = Graphic_elements(SCREEN_W-SCREEN_W//10,SCREEN_H-SCREEN_H//10,SCREEN_W//10,SCREEN_H//10,"image/Загрузка/Загрузка0.png")
cloud = Graphic_elements(0,0,SCREEN_W*2,SCREEN_H//3.52,"image/Облоко.bmp")
cloud2 = Graphic_elements(SCREEN_W*2,0,SCREEN_W*2,SCREEN_H//3.52,"image/Облоко.bmp")
invisible_block_icon = Graphic_elements(SCREEN_W-SCREEN_W//10,SCREEN_H-SCREEN_H//10,SCREEN_W//10,SCREEN_H//10,"image/invisible_block_icon.png")
Rope_with_saw = Graphic_elements(SCREEN_W//2,SCREEN_H//15,SCREEN_W//15,SCREEN_W//20*10,"image/Rope_with_saw.png")
Hook = Graphic_elements(SCREEN_W//2,SCREEN_H//15,SCREEN_W//30,SCREEN_W//20*10,"image/Hook.png")
button = Graphic_elements(0,0,SCREEN_W//20,SCREEN_W//20//3.3846,"image/button.png")

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

}