#Подключаем подготовленные модули нашего проекта#
from pygame import* 
import random
#Подключаем модули нашего проекта
from surface import *
init() #Инициализируем pygame
#Настраиваем разрешение и ограничение кадров
SCREEN_W = display.Info().current_w
SCREEN_H = display.Info().current_h
SCREEN_W = 1280
SCREEN_H = 720
FPS = 30
flags = SCALED

#Создаем список контуров
list_border_cor_cracking = list()
list_border_cor_key_and_door = list()
list_border_cor_saw = list()
list_border_cor_ladder = list()
list_border_cor_spring = list()
list_border_cor = list()
list_flag = list()#временный список,где будут хранится координаты
#Индексы уровней
index_lvl = 0
index_location = 0
#Считаем птицу (beard в переводе - борода)
max_number_beard = random.randint(500,1000)
count_beard = 0
#Список верёвок (анимация)
list_cor_Rope = [
    [-SCREEN_W//5.28,-SCREEN_H//5.10],
    [-SCREEN_W//5.61,-SCREEN_H//5.93],
    [-SCREEN_W//6,-SCREEN_H//7.14],
    [-SCREEN_W//6.49,-SCREEN_H//8.75],
    [-SCREEN_W//7.19,-SCREEN_H//11.1],
    [-SCREEN_W//8,-SCREEN_H//14.28],
    [-SCREEN_W//9.20,-SCREEN_H//20],
    [-SCREEN_W//11.13,-SCREEN_H//28],
    [-SCREEN_W//13.61,-SCREEN_H//41.17],
    [-SCREEN_W//18.02,-SCREEN_H//70],
    [-SCREEN_W//19.10,-SCREEN_H//140],
    [-SCREEN_W//60.95,-SCREEN_H//233.33],
    [0,0],
    [SCREEN_W//60.95,-SCREEN_H//233.33],
    [SCREEN_W//19.10,-SCREEN_H//140],
    [SCREEN_W//18.02,-SCREEN_H//70],
    [SCREEN_W//13.61,-SCREEN_H//41.17],
    [SCREEN_W//11.13,-SCREEN_H//28],
    [SCREEN_W//9.20,-SCREEN_H//20],
    [SCREEN_W//8,-SCREEN_H//14.28],
    [SCREEN_W//7.19,-SCREEN_H//11.1],
    [SCREEN_W//6.49,-SCREEN_H//8.75],
    [SCREEN_W//6,-SCREEN_H//7.14],
    [SCREEN_W//5.61,-SCREEN_H//5.93],
    [SCREEN_W//5.28,-SCREEN_H//5.10],
]
#Задаем разрешение и ограничение кадров. Настраиваем название окна
screen = display.set_mode((SCREEN_W, SCREEN_H))
display.set_caption("Игра на pygame")
clock = time.Clock()        

#Список пилы, верёвок и так далее
list_saw = []
list_hook = []
list_Rope_with_saw = []

#Словарь аргументов блоков
dict_argument_block = {
    "flag_move_cloud": 1,
    "count_motion_block": 0,
    "max_count_motion_block": 7,
    "count_spinning_motion_block":0,
    "count_img_spinning_motion_block":1,
    "flag_direction_spinning_motion_block":"+",
    "flag_directory_motion_block_left_right": "R",
    "flag_directory_motion_block_up_down": "D",
    "flag_load": 0,
    "count_load": 24,
    "count_spike":150,
    "direction_spike":"U",
}
#Словарь аргументов
dict_argument = {
    "ghost": False, 
    "keys": key.get_pressed(), 
    "ded": True,    
    "game": True,
    "scene":"game",
    "full_surface":list_surface,
    "list_surface":list_surface[index_lvl][index_location],
    "max_number_beard":max_number_beard,
    "count_beard":count_beard,
    "list_beard":list(),
    "index_lvl":index_lvl,
    "index_location":index_location,
    "X_MAP":0,
    "Y_MAP":0,
    "duration_shield":60,


}
#Словарь аргументов ангелов
dict_argument_angle = {
    "angle_saw":0,
    "angle_Rope_with_saw":-60,
    "angle_Rope_with_saw_direction":"R",
    "index_Rope_with_saw":0,
    "angle_Hook":-60,
    "angle_Hook_direction":"R",
    "index_Hook":0
}
#Словарь списков контуров
dict_list_border = {
    "list_border_cor_cracking":list_border_cor_cracking,
    "list_border_cor_key_and_door":list_border_cor_key_and_door,
    "list_border_cor_ladder":list_border_cor_ladder,
    "list_border_cor_spring":list_border_cor_spring,
    "list_border_cor":list_border_cor,
    "list_flag":list_flag
}

dict_spawn_and_finish_point = {
    "lvl1_location_1":[[SCREEN_W//80,SCREEN_H-SCREEN_H//10*2.5],Rect(0,-SCREEN_W/40,SCREEN_W//20,1),"up"],
    "lvl1_location_2":[[SCREEN_W//80,SCREEN_H-SCREEN_H//10*2.5],Rect(SCREEN_W-SCREEN_W//80,SCREEN_H//5.53,1,SCREEN_H//5.53),"right"],
    "lvl1_location_3":[[SCREEN_W//80,SCREEN_H//5.5],Rect(SCREEN_W-SCREEN_W//80,SCREEN_H//45,1,SCREEN_H//6.31),"right"],
    "lvl1_location_4":[[SCREEN_W//80,SCREEN_H-SCREEN_H//10*2.5],Rect(SCREEN_W-SCREEN_W//80,SCREEN_H//2.48,1,SCREEN_H//7.2),None]
}
#Словари аргументов и ломания платформ
broken_cracking_platform = dict()
dict_argument_door_block = dict()