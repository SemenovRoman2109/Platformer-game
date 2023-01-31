# Подключаем нужные нам модули
from pygame import*
import os
import random
# Подключаем модули нашего проекта
from graphic_elements import Graphic_elements
from constant import *
from object import *
from sounds import *
from text import *
import copy
import json
# Инициализируем настройки pygame
init()

# Создаем клас для платформ
class SurfaceRect():
    def __init__(self,path,width,height):
        # Задаем нужные свойства нашей платформе
        self.WIDTH = width
        self.HEIGHT = height
        self.SURFACE = Surface((self.WIDTH, self.HEIGHT))#создаем поверхность

# Обновляем матрицу
def drawSurfaces():
    #Проверяем выход индексов за матрицу
    def matrix_index_check(y,x,element,list_direction):
        result = True
        if "right" in list_direction:
            if x + 1 <= len(dict_argument["list_surface"][0]) - 1:
                if dict_argument["list_surface"][y][x + 1] == element:
                    result = True
                else:
                    return False
            else:
                return False
        if "left" in list_direction:
            if x - 1 >= 0:
                if dict_argument["list_surface"][y][x - 1] == element:
                    result = True
                else:
                    return False
            else:
                return False
        if "down" in list_direction:
            if y + 1 <= len(dict_argument["list_surface"]) - 1:
                if dict_argument["list_surface"][y + 1][x] == element:
                    result = True
                else:
                    return False
            else:
                return False
        if "up" in list_direction:
            if y - 1 >= 0:
                if dict_argument["list_surface"][y - 1][x] == element:
                    result = True
                else:
                    return False
            else:
                return False
        return result

    # очищаем списки 
    list_noot_colision_platphorm.clear()
    list_Rope_with_saw.clear()
    list_hook.clear()
    list_spikes.clear()
    list_saw.clear()
    dict_list_border["list_border_cor_paper_and_door"].clear()
    dict_list_border["list_border_cor_ladder"].clear()
    dict_list_border["list_border_cor"].clear()
    dict_list_border["list_flag"].clear()
    # Список сиволов
    list_symbol = ["b","K","П","Л","л","ъ","Ъ","Б","P","L","i","c","с","C"]
    # список символов трескающихся платформ
    list_cracking_platform = ["c","с","C"]
    # Кол-во платформ
    number_cracking = 0
    number_spring = 0
    number_person = 0
    # направления палки крепления лестниицы
    direction_begin_leader = "left"
    
    # Добавляем мелементы двери
    list_key_door = list()
    for key in list(dict_argument_door_block.keys()):
        keys = key.split("Count_door_")[-1]
        list_key_door.append(keys)
        list_symbol.append(keys)
        list_symbol.append(keys.lower())
    # Задаем изначальнукоодринату отрисовки 
    X = dict_argument["X_MAP"]
    Y = dict_argument["Y_MAP"]
    # Изначальные значания для всех блоков
    PATH = "image/block.png"
    WIDTH = dict_argument["BLOCK_SIZE"]
    HEIGHT = dict_argument["BLOCK_SIZE"]
    NAME_LIST = list()
    flag_pf = SurfaceRect(PATH,WIDTH,HEIGHT)
    # Перебираем матрицу
    for i in range(len(dict_argument["list_surface"])):
        dict_list_border["list_flag"].append([])#Добавляю список для ряда
        # Перебираем матрицу
        for j in range(len(dict_argument["list_surface"][i])):
            dict_list_border["list_flag"][i].append([])
            
            # ПРОЫЕРЯЕМ ВСЕ БУКВЫ И ЗАДАЕМ СООТВЕТСТВУЮЩИЕ ЗНАЧЕНИЯ РАЗМЕРОВ СПИСКА ПУТИ К КАРТИНКЕ ДЛЯ НИХ 

            if dict_argument["list_surface"][i][j] in list_cracking_platform:
                PATH = "image/cracking_platform_"+str(list_cracking_platform.index(dict_argument["list_surface"][i][j]))+".png"
                WIDTH = dict_argument["BLOCK_SIZE"]
                HEIGHT = dict_argument["BLOCK_SIZE"]//3.55
                NAME_LIST = "list_border_cor_cracking"
                number_cracking += 1
            elif dict_argument["list_surface"][i][j] == "M":
                PATH = "image/plate.png"
                WIDTH = dict_argument["BLOCK_SIZE"] // 2
                HEIGHT = dict_argument["BLOCK_SIZE"] // 2
                list_noot_colision_platphorm.append(Graphic_elements(X+dict_argument["BLOCK_SIZE"] // 4,Y+dict_argument["BLOCK_SIZE"] // 4,WIDTH,HEIGHT,PATH))
            elif dict_argument["list_surface"][i][j] == "Т":
                PATH = "image/corpse.png"
                WIDTH = dict_argument["BLOCK_SIZE"] * 2
                HEIGHT = dict_argument["BLOCK_SIZE"] * 2
                list_noot_colision_platphorm.append(Graphic_elements(X,Y,WIDTH,HEIGHT,PATH))
            elif dict_argument["list_surface"][i][j] == "R":
                list_Rope_with_saw.append(Graphic_elements(X+dict_argument["BLOCK_SIZE"]//2,Y,dict_argument["BLOCK_SIZE"]*1.36,dict_argument["BLOCK_SIZE"]*10,"image/Rope_with_saw.png"))
            elif dict_argument["list_surface"][i][j] == "H":
                list_hook.append(Graphic_elements(X+SCREEN_W//44-SCREEN_W//60,Y,dict_argument["BLOCK_SIZE"],dict_argument["BLOCK_SIZE"]*10,"image/Hook.png"))
            elif dict_argument["list_surface"][i][j] == "К":
                list_spikes.append(Graphic_elements(X,Y+(dict_argument["BLOCK_SIZE"]-dict_argument["BLOCK_SIZE"]//3),dict_argument["BLOCK_SIZE"],dict_argument["BLOCK_SIZE"]//3,"image/spikes.png"))
            elif dict_argument["list_surface"][i][j] == "к":
                obj = Graphic_elements(X,Y,dict_argument["BLOCK_SIZE"],dict_argument["BLOCK_SIZE"]//3,"image/spikes.png")
                obj.image_load(rotate_y=True)
                list_spikes.append(obj)
            elif dict_argument["list_surface"][i][j] == "ш":
                list_spikes.append(Graphic_elements(X,Y+(dict_argument["BLOCK_SIZE"]-dict_argument["BLOCK_SIZE"]//3),dict_argument["BLOCK_SIZE"],dict_argument["BLOCK_SIZE"]//3,"image/spikes.png"))    

            elif dict_argument["list_surface"][i][j] == "N" or dict_argument["list_surface"][i][j] == "n" or dict_argument["list_surface"][i][j] == "У":
                if len(list_NPC) <= number_person:
                    list_NPC.append(Graphic_elements(X,Y-dict_argument["BLOCK_SIZE"]*1.66+dict_argument["BLOCK_SIZE"],dict_argument["BLOCK_SIZE"],dict_argument["BLOCK_SIZE"]*1.66,"image/Person/person_"+str(random.randint(1,13))+".png"))
                    list_index_NPC.append([i,j])
                    if dict_argument["list_surface"][i][j] == "У":
                        list_NPC[-1].path = "image/criminal/model.png"
                    
                    if len(list_NPC) > 1:
                        stop = True
                        while stop:
                            for obj in list_NPC:
                                if obj != list_NPC[-1]:
                                    if obj.path == list_NPC[-1].path:
                                        stop = True
                                        list_NPC[-1].path = "image/Person/person_"+str(random.randint(1,13))+".png"
                                        break
                                    else:
                                        stop = False
                    if dict_argument["list_surface"][i][j] == "n":
                        list_NPC[-1].X -= BLOCK_SIZE//5
                        list_NPC[-1].image_load(rotate_x= True)
                number_person += 1
            elif dict_argument["list_surface"][i][j] == "Л":
                PATH = "image/ladder_middle.png"
                WIDTH = dict_argument["BLOCK_SIZE"]
                HEIGHT = dict_argument["BLOCK_SIZE"]                     
                NAME_LIST = "list_border_cor_ladder"
            elif dict_argument["list_surface"][i][j] == "л":
                
                PATH = "image/ladder_beginning.png"
                WIDTH = dict_argument["BLOCK_SIZE"]
                HEIGHT = dict_argument["BLOCK_SIZE"]                     
                NAME_LIST = "list_border_cor_ladder"
                if dict_argument["list_surface"][i][j + 1] == "0":
                    direction_begin_leader = "l"
                else:
                    direction_begin_leader = "r"
            elif dict_argument["list_surface"][i][j] == "ъ":
                PATH = "image/ladder_end.png"
                WIDTH = dict_argument["BLOCK_SIZE"]
                HEIGHT = dict_argument["BLOCK_SIZE"]                     
                NAME_LIST = "list_border_cor_ladder"

            elif dict_argument["list_surface"][i][j] == "Ъ":
                PATH = "image/ladder_beginning_end.png"
                WIDTH = dict_argument["BLOCK_SIZE"]
                HEIGHT = dict_argument["BLOCK_SIZE"]                     
                NAME_LIST = "list_border_cor_ladder"
                if dict_argument["list_surface"][i][j + 1] == "0":
                    direction_begin_leader = "l"
                else:
                    direction_begin_leader = "r"



            elif dict_argument["list_surface"][i][j] == "П":
                PATH = "image/spring.png"
                WIDTH = dict_argument["BLOCK_SIZE"]
                HEIGHT = dict_argument["BLOCK_SIZE"]
                NAME_LIST = "list_border_cor_spring"
                number_spring += 1
            elif dict_argument["list_surface"][i][j] == "s":
                list_saw.append(Graphic_elements(X+(dict_argument["BLOCK_SIZE"]*1.53-dict_argument["BLOCK_SIZE"]),Y+(dict_argument["BLOCK_SIZE"]*1.54-dict_argument["BLOCK_SIZE"]),dict_argument["BLOCK_SIZE"]*1.53,dict_argument["BLOCK_SIZE"]*1.54,"image/saw.png"))
            
            elif dict_argument["list_surface"][i][j] == "D" or dict_argument["list_surface"][i][j] == "d" :
                PATH = "image/Door.png"
                WIDTH = dict_argument["BLOCK_SIZE"]
                HEIGHT = dict_argument["BLOCK_SIZE"]*2
                list_noot_colision_platphorm.append(Graphic_elements(X,Y,WIDTH,HEIGHT,PATH))
                if dict_argument["list_surface"][i][j] == "d":
                    list_noot_colision_platphorm[-1].image_load(rotate_x= True)
            elif dict_argument["list_surface"][i][j] == "G": 
                WIDTH = dict_argument["BLOCK_SIZE"]*1.5
                HEIGHT = dict_argument["BLOCK_SIZE"]*3
                PATH = "image/Game_machine.png"
                list_noot_colision_platphorm.append(Graphic_elements(X,Y-dict_argument["BLOCK_SIZE"]*2,WIDTH,HEIGHT,PATH))
            elif dict_argument["list_surface"][i][j] == "P": 
                PATH = "image/block/solo_block.png"
                if dict_argument["list_surface"][i][j+1] == "P":
                    PATH = "image/block_motion_left.png"
                elif dict_argument["list_surface"][i][j-1] == "P":
                    PATH = "image/block_motion_right.png"
                WIDTH = dict_argument["BLOCK_SIZE"]
                HEIGHT = dict_argument["BLOCK_SIZE"]
                NAME_LIST = "list_border_cor"
            elif dict_argument["list_surface"][i][j] == "Б":
                PATH = "image/paper.png"
                WIDTH = dict_argument["BLOCK_SIZE"]
                HEIGHT = dict_argument["BLOCK_SIZE"]
                NAME_LIST = "list_border_cor_paper_and_door"
            elif dict_argument["list_surface"][i][j] in ["b","i"]: 
                PATH = "image/block/center.png"
                WIDTH = dict_argument["BLOCK_SIZE"]
                HEIGHT = dict_argument["BLOCK_SIZE"]
                NAME_LIST = "list_border_cor"

                if matrix_index_check(i,j,dict_argument["list_surface"][i][j],["right","left","down","up"]):
                    PATH = "image/block/center.png"
                elif matrix_index_check(i,j,dict_argument["list_surface"][i][j],["right","left","up"]):
                    PATH = "image/block/down.png"
                elif matrix_index_check(i,j,dict_argument["list_surface"][i][j],["right","left","down"]):
                    PATH = "image/block/up.png"
                elif matrix_index_check(i,j,dict_argument["list_surface"][i][j],["right","down","up"]):
                    PATH = "image/block/left.png"
                elif matrix_index_check(i,j,dict_argument["list_surface"][i][j],["left","down","up"]):
                    PATH = "image/block/right.png"
                elif matrix_index_check(i,j,dict_argument["list_surface"][i][j],["right","up"]):
                    PATH = "image/block/left_down.png"
                elif matrix_index_check(i,j,dict_argument["list_surface"][i][j],["left","up"]):
                    PATH = "image/block/right_down.png"
                elif matrix_index_check(i,j,dict_argument["list_surface"][i][j],["right","down"]):
                    PATH = "image/block/left_up.png"
                elif matrix_index_check(i,j,dict_argument["list_surface"][i][j],["left","down"]):
                    PATH = "image/block/right_up.png"
                elif matrix_index_check(i,j,dict_argument["list_surface"][i][j],["right","left"]):
                    PATH = "image/block/up_down.png"
                elif matrix_index_check(i,j,dict_argument["list_surface"][i][j],["down","up"]):
                    PATH = "image/block/left_right.png"
                elif matrix_index_check(i,j,dict_argument["list_surface"][i][j],["up"]):
                    PATH = "image/block/left_right_down.png"
                elif matrix_index_check(i,j,dict_argument["list_surface"][i][j],["down"]):
                    PATH = "image/block/left_right_up.png"
                elif matrix_index_check(i,j,dict_argument["list_surface"][i][j],["right"]):
                    PATH = "image/block/up_down_left.png"
                elif matrix_index_check(i,j,dict_argument["list_surface"][i][j],["left"]):
                    PATH = "image/block/up_down_right.png"
                else:
                    PATH = "image/block/solo_block.png"



            elif dict_argument["list_surface"][i][j] == "L":
                PATH = "image/Motion_block_up_down_"+str(dict_argument_block["count_img_spinning_motion_block"])+".png"
                WIDTH = dict_argument["BLOCK_SIZE"]
                HEIGHT = dict_argument["BLOCK_SIZE"]//2
                NAME_LIST = "list_border_cor"
            elif dict_argument["list_surface"][i][j] == "K":
                PATH = "image/Key.png"
                WIDTH = dict_argument["BLOCK_SIZE"]
                HEIGHT = dict_argument["BLOCK_SIZE"]
                NAME_LIST = "list_border_cor_paper_and_door"
            
            elif dict_argument["list_surface"][i][j] in list_key_door:
                if dict_direction_door[dict_argument["list_surface"][i][j]] == "r":
                    PATH = "image/Door_block.png"
                    WIDTH = dict_argument["BLOCK_SIZE"]*2
                    HEIGHT = dict_argument["BLOCK_SIZE"]//5
                else:
                    PATH = "image/Door_block_up.png"
                    WIDTH = dict_argument["BLOCK_SIZE"]//5
                    HEIGHT = dict_argument["BLOCK_SIZE"]*2
                NAME_LIST = "list_border_cor"
            for obj in list_key_door:
                if dict_argument["list_surface"][i][j] in obj.lower():
                    if dict_direction_door[dict_argument["list_surface"][i][j].upper()] == "r":
                        PATH = "image/Open_door_block.png"
                        WIDTH = dict_argument["BLOCK_SIZE"]*2
                        HEIGHT = dict_argument["BLOCK_SIZE"]
                    else:
                        PATH = "image/Open_door_block_up.png"
                        WIDTH = dict_argument["BLOCK_SIZE"]
                        HEIGHT = dict_argument["BLOCK_SIZE"]*2
                    NAME_LIST = "list_border_cor_paper_and_door"
                
            # Проверяем есть ди етот символ в списке символов
            if dict_argument["list_surface"][i][j] in list_symbol:
                # Проверяем если ето не пружына и платформа 
                if (NAME_LIST != "list_border_cor_spring" and NAME_LIST != "list_border_cor_cracking") or (NAME_LIST == "list_border_cor_spring" and len(dict_list_border["list_border_cor_spring"]) < number_spring) or (NAME_LIST == "list_border_cor_cracking" and len(dict_list_border["list_border_cor_cracking"]) < number_cracking):


                    flag_pf = SurfaceRect(PATH,WIDTH,HEIGHT)
                    # Создаем графический елемент
                    pf = Graphic_elements(X,Y,flag_pf.WIDTH,flag_pf.HEIGHT,PATH)

                    # Разварачиваем крипление в зависимости от стороны в которую оно крепиться
                    if NAME_LIST == "list_border_cor_ladder":
                        if direction_begin_leader == "l":
                            pf.image_load(True)

                    dict_list_border["list_flag"][i][j].append(Y)#верхний край платформы
                    dict_list_border["list_flag"][i][j].append(Y + flag_pf.HEIGHT)#нижний край платформs
                    dict_list_border["list_flag"][i][j].append(X - int(flag_pf.WIDTH / 1.55))#левая часть платформы
                    dict_list_border["list_flag"][i][j].append(X + int(flag_pf.WIDTH / 1.55))#правая часть платформы
                    dict_list_border["list_flag"][i][j].append(X)#левая часть платформы
                    dict_list_border["list_flag"][i][j].append(X + flag_pf.WIDTH)#правая часть платформы 
                    # Значения которые нужны только трескающимся платформерам а именно счетчики востановления и ломания    
                    if dict_argument["list_surface"][i][j] in list_cracking_platform:
                        dict_list_border["list_flag"][i][j].append(dict_argument["speed_transparency_broken_platforms"])
                        dict_list_border["list_flag"][i][j].append(dict_argument["speed_transparency_broken_platforms"]*2)
                    else:
                        dict_list_border["list_flag"][i][j].append(None)
                        dict_list_border["list_flag"][i][j].append(None)
                    
                    dict_list_border["list_flag"][i][j].append(NAME_LIST)# Список в котором находиться платформа
                    dict_list_border["list_flag"][i][j].append(pf)#Добавляем графический елемент
                    dict_list_border["list_flag"][i][j].append(dict_argument["list_surface"][i][j])#буква елемента

            # Изменяем кординату на которой отрисовываеться картинка
            X += dict_argument["BLOCK_SIZE"]
        # Изменяем кординату на которой отрисовываеться картинка    
        X = dict_argument["X_MAP"]
        Y += dict_argument["BLOCK_SIZE"]
    # Добавляем все в основной список 
    for i in range(len(dict_list_border["list_flag"])):
        for j in range(len(dict_list_border["list_flag"][i])):
            if len(dict_list_border["list_flag"][i][j]) != 0:
                dict_list_border[dict_list_border["list_flag"][i][j][-3]].append(dict_list_border["list_flag"][i][j])

# Функция для движения платформы вправо влево
def block_motion_right_left(list_surface,dict_argument_block,platform_length,sprite):

    # Перебираем матрицу
    list_index_vertically = [] 
    for obj in range(len(dict_argument["list_surface"])):
        for i in range(len(dict_argument["list_surface"][obj])):
            if dict_argument["list_surface"][obj][i] == "P":
                list_index_vertically.append(obj)
                break
    
    
    for index_vertically in list_index_vertically:
        if not index_vertically in dict_directory_motion_block_left_right.keys():
            dict_directory_motion_block_left_right[index_vertically] = "R"

    for index_vertically in list_index_vertically:
        # Индексы клетки            
        index_x = 0
        
        #Перебираем цыкл столько раз сколько длина платформа
        for obj in range(platform_length):
            # Проверяем направление платформы
            if dict_directory_motion_block_left_right[index_vertically] == "R":
                # Перебираем список ряда
                for block in dict_argument["list_surface"][index_vertically]:
                    # Находим платформу
                    if block == "P":
                        # Если следующая келтка путь для платформы
                        if dict_argument["list_surface"][index_vertically][index_x + 1] == "p":
                            # Добавляем ряд в отдельный список
                            list1 = dict_argument["list_surface"][index_vertically]
                            list1 = list(list1)
                            # Меняем буквы местами
                            list1[index_x + 1] = "P"
                            list1[index_x] = "p"
                            # Добавляем наш ряд в основную матрицу
                            dict_argument["list_surface"][index_vertically] = list(''.join(list1))
                            # Проверяем колизию персонажа дабы перемещать его когда он стоит на платформе
                            block = [index_vertically*dict_argument["BLOCK_SIZE"],index_vertically*dict_argument["BLOCK_SIZE"]+dict_argument["BLOCK_SIZE"],index_x*dict_argument["BLOCK_SIZE"]-dict_argument["BLOCK_SIZE"],index_x*dict_argument["BLOCK_SIZE"]]
                            if sprite.image_sprite.Y + sprite.image_sprite.HEIGHT >= block[0] and sprite.image_sprite.X + sprite.image_sprite.WIDTH >= block[2] + dict_argument["BLOCK_SIZE"]//3 and sprite.image_sprite.X <= block[3] - dict_argument["BLOCK_SIZE"]//3 and sprite.image_sprite.Y + sprite.image_sprite.HEIGHT <= block[0] + sprite.gravity_speed :
                                sprite.image_sprite.X += dict_argument["BLOCK_SIZE"]
                            # Останавливаем цыкл
                            break
                        # Если следующая келтка не путь для платформы
                        elif dict_argument["list_surface"][index_vertically][index_x + 1] in ["0","b"] and obj == 0:
                            # Меняем направление
                            dict_directory_motion_block_left_right[index_vertically] = "L"
                            # Останавливаем цыкл
                            break
                            
                    index_x += 1
                index_x = 0
            # Проверяем направление платформы
            if dict_directory_motion_block_left_right[index_vertically] == "L":
                index_x_2 = len(dict_argument["list_surface"][0])
                # Перебираем список ряда в обратном порядке
                for block in dict_argument["list_surface"][index_vertically][::-1]:
                    # Находим платформу
                    if block == "P":
                        # Если следующая келтка путь для платформы
                        if dict_argument["list_surface"][index_vertically][::-1][index_x + 1] == "p":
                            # Добавляем ряд в отдельный список
                            list1 = dict_argument["list_surface"][index_vertically][::-1]
                            list1 = list(list1)
                            # Меняем буквы местами
                            list1[index_x + 1] = "P"
                            list1[index_x] = "p"
                            # Добавляем наш ряд в основную матрицу
                            dict_argument["list_surface"][index_vertically] = list(''.join(list1[::-1]))  
                            # Проверяем колизию персонажа дабы перемещать его когда он стоит на платформе
                            block = [index_vertically*dict_argument["BLOCK_SIZE"],index_vertically*dict_argument["BLOCK_SIZE"]+dict_argument["BLOCK_SIZE"],index_x_2*dict_argument["BLOCK_SIZE"]-dict_argument["BLOCK_SIZE"],index_x_2*dict_argument["BLOCK_SIZE"]]
                            if sprite.image_sprite.Y + sprite.image_sprite.HEIGHT >= block[0] and sprite.image_sprite.X + sprite.image_sprite.WIDTH >= block[2] + dict_argument["BLOCK_SIZE"]//3 and sprite.image_sprite.X <= block[3] - dict_argument["BLOCK_SIZE"]//3 and sprite.image_sprite.Y + sprite.image_sprite.HEIGHT <= block[0] + sprite.gravity_speed :
                                    sprite.image_sprite.X -= dict_argument["BLOCK_SIZE"]
                            # Останавливаем цыкл
                            break
                        # Если следующая келтка не путь для платформы
                        elif dict_argument["list_surface"][index_vertically][::-1][index_x + 1] in ["0","b"] and obj == 1:
                            # Меняем направление
                            dict_directory_motion_block_left_right[index_vertically] = "R"
                            # Останавливаем цыкл
                            break
                    # Увеличиваем index
                    index_x_2 -= 1
                    index_x += 1

                index_x = 0

# Функция для движения платформы вверх вниз
def block_motion_down_up(list_surface,dict_argument_block,sprite):
    # Перебираем матрицу
    list_index_horizontal = [] 
    for obj in range(len(dict_argument["list_surface"])):
        for i in range(len(dict_argument["list_surface"][obj])):
            if dict_argument["list_surface"][obj][i] == "L":
                list_index_horizontal.append(i)
    
    
    for index_x in list_index_horizontal:
        if not index_x in dict_directory_motion_block_up_down.keys():
            dict_directory_motion_block_up_down[index_x] = "D"

    
    # Перебираем матрицу
    for index_x in list_index_horizontal:
        index_y = 0
        stop = False
        for obj in dict_argument["list_surface"]:
            # Находим платформу
            if stop == False:
                if dict_argument["list_surface"][index_y][index_x] == "L":
                    # Если направление в верх 
                    if dict_directory_motion_block_up_down[index_x] == "U":
                        # Если в низ может двигаться
                        if dict_argument["list_surface"][index_y - 1][index_x] == "l":
                            # Создаем список с рядом  в котором клетка на которую нужно двигаться
                            list_down = dict_argument["list_surface"][index_y - 1]
                            # Создаем список с рядом  в котором клетка передвижения
                            list_up = dict_argument["list_surface"][index_y]
                            list_up = list(list_up)
                            list_down = list(list_down)
                            # Меняем платформу и путь местами в наших списках
                            list_down[index_x] = "L"
                            list_up[index_x] = "l"
                            # заменяем ряд в матрице на ряд в котором мы изменили буквы
                            dict_argument["list_surface"][index_y] = list(''.join(list_up))  
                            dict_argument["list_surface"][index_y - 1] = list(''.join(list_down))  
                            # Проверяем колизию блока и если персонаж на нем двигаем его
                            block = [index_y*dict_argument["BLOCK_SIZE"],index_y*dict_argument["BLOCK_SIZE"]+dict_argument["BLOCK_SIZE"],index_x*dict_argument["BLOCK_SIZE"],index_x*dict_argument["BLOCK_SIZE"]+dict_argument["BLOCK_SIZE"]]
                            if sprite.image_sprite.Y + sprite.image_sprite.HEIGHT >= block[0] and sprite.image_sprite.X + sprite.image_sprite.WIDTH >= block[2] and sprite.image_sprite.X <= block[3] and sprite.image_sprite.Y + sprite.image_sprite.HEIGHT <= block[0] + sprite.gravity_speed :
                                sprite.image_sprite.Y -= dict_argument["BLOCK_SIZE"]
                            # Останавливаем функцию
                            stop = True
                        # Если в низ нельзя двигаться    
                        elif dict_argument["list_surface"][index_y - 1][index_x] == "0":
                            # Меняем направления
                            dict_directory_motion_block_up_down[index_x] = "D"
                            # Останавливаем функцию
                            stop = True
                    # Если направление в низ        
                    if dict_directory_motion_block_up_down[index_x] == "D":
                        # Если в верх может двигаться
                        if dict_argument["list_surface"][index_y + 1][index_x] == "l":
                            # Создаем список с рядом  в котором клетка на которую нужно двигаться
                            list_down = dict_argument["list_surface"][index_y + 1]
                            # Создаем список с рядом  в котором клетка передвижения
                            list_up = dict_argument["list_surface"][index_y]
                            list_up = list(list_up)
                            list_down = list(list_down)
                            # Меняем платформу и путь местами в наших списках
                            list_down[index_x] = "L"
                            list_up[index_x] = "l"
                            # заменяем ряд в матрице на ряд в котором мы изменили буквы
                            dict_argument["list_surface"][index_y] = list(''.join(list_up))  
                            dict_argument["list_surface"][index_y + 1] = list(''.join(list_down))  
                            # Проверяем колизию блока и если персонаж на нем двигаем его
                            block = [index_y*dict_argument["BLOCK_SIZE"],index_y*dict_argument["BLOCK_SIZE"]+dict_argument["BLOCK_SIZE"],index_x*dict_argument["BLOCK_SIZE"],index_x*dict_argument["BLOCK_SIZE"]+dict_argument["BLOCK_SIZE"]]
                            if sprite.image_sprite.Y + sprite.image_sprite.HEIGHT >= block[0] and sprite.image_sprite.X + sprite.image_sprite.WIDTH >= block[2] and sprite.image_sprite.X <= block[3] and sprite.image_sprite.Y + sprite.image_sprite.HEIGHT <= block[0] + sprite.gravity_speed :
                                sprite.image_sprite.Y += dict_argument["BLOCK_SIZE"]
                            # Останавливаем функцию
                            stop = True
                        # Если в верх нельзя двигаться   
                        elif dict_argument["list_surface"][index_y + 1][index_x] == "0":
                            dict_directory_motion_block_up_down[index_x] = "U"
                            # Останавливаем функцию
                            stop = True
                            
            # Увеличиваем index для нахождения клетки с платформой
            index_y += 1

# Функция повоорота веревки 
def rope_angle(index,direction,angle):
    # Меняем направления поворота когда градус достигает нужного значения
    if dict_argument_angle[angle] >= 60:
        dict_argument_angle[direction] = "L"
    if dict_argument_angle[angle] <= -60:
        dict_argument_angle[direction] = "R"

    # В зависимости от стороны поворота уменьшаем или увеличиваем градус
    if dict_argument_angle[direction] == "R":
        dict_argument_angle[angle] += 5
        dict_argument_angle[index] += 1
    if dict_argument_angle[direction] == "L":
        dict_argument_angle[angle] -= 5
        dict_argument_angle[index] -= 1

# Функция для любых веревок
def rope(index,graphic_elements,angle,width,height):    
    # Создаем копию веревки даюы удобно поворачивать её относительно основной картинки
    graphic_elements.image_load()
    Rope_copy = transform.rotate(graphic_elements.IMG, int(dict_argument_angle[angle]))
    # Задаем x и y для нашего наконечника дабы засечь косание с ним
    x = graphic_elements.X-graphic_elements.WIDTH//2+int(list_cor_Rope[dict_argument_angle[index]][0])
    y = graphic_elements.Y+graphic_elements.HEIGHT//2-graphic_elements.WIDTH+int(list_cor_Rope[dict_argument_angle[index]][1])-BLOCK_SIZE
    # Создаем рект обект для колизии с накончечником
    Rope_rect = Rect(x,y,graphic_elements.WIDTH,graphic_elements.WIDTH)
    # draw.rect(screen,(0,0,0),Rope_rect)
    # Отрисовываем веревку 
    screen.blit(Rope_copy, (graphic_elements.X - int(Rope_copy.get_width() / 2), graphic_elements.Y -BLOCK_SIZE - int(Rope_copy.get_height() / 2)))
    # Возвращаем рект обект для колизии с накончечником 
    return Rope_rect

#Функия двери которая открываеться по кнопке
def door_and_button(index_button_x_1,index_button_y_1,index_button_x_2,index_button_y_2,element_door,element_door_empty,sprite1,direction_door,duration):
    # Если еще нет етого елемента в словаре всехх дверей с кнопками 
    if not str("Count_door_"+element_door) in list(dict_argument_door_block.keys()):
        #Добавляем в словарь новый ключ к нашей двери
        dict_argument_door_block[str("Count_door_"+element_door)] = 0
        dict_direction_door[element_door] = direction_door
    # когда дверь должна закрыться 
    if dict_argument_door_block[str("Count_door_"+element_door)] == 0: 
        # Даем ей значение при которой дверь будет закрыта  
        dict_argument_door_block[str("Count_door_"+element_door)] = -1
    
    #Востанавливаем стенку на матрице 
    if str("Count_door_"+element_door) in list(dict_argument_door_block.keys()):
        if dict_argument_door_block[str("Count_door_"+element_door)] == 1: 
            for el in range(len(dict_argument["list_surface"])):
                for element in range(len(dict_argument["list_surface"][el])):
                    if dict_argument["list_surface"][el][element] == element_door_empty:
                        dict_argument["list_surface"][el][element] = element_door
            drawSurfaces()
            
    # Создаем графические елементы кнопок                        
    graphik_element_button_1 = Graphic_elements(index_button_x_1*dict_argument["BLOCK_SIZE"],(index_button_y_1+1)*dict_argument["BLOCK_SIZE"]-dict_Graphic_elements_obj["button"].HEIGHT,dict_Graphic_elements_obj["button"].WIDTH,dict_Graphic_elements_obj["button"].HEIGHT,dict_Graphic_elements_obj["button"].path)
    if index_button_x_2 == None:
        graphik_element_button_2 =Graphic_elements(0,0,0,0,None)
    else:
        graphik_element_button_2 = Graphic_elements(index_button_x_2*dict_argument["BLOCK_SIZE"],(index_button_y_2+1)*dict_argument["BLOCK_SIZE"]-dict_Graphic_elements_obj["button"].HEIGHT,dict_Graphic_elements_obj["button"].WIDTH,dict_Graphic_elements_obj["button"].HEIGHT,dict_Graphic_elements_obj["button"].path)
    
    #Если кнопка не нажата то просто отрисовываем её 
    if not Rect.colliderect(sprite1.image_sprite.RECT,graphik_element_button_1.RECT):
        graphik_element_button_1.show_image(screen)
    #Если кнопка нажата то изменя ем ее картинку и отрисовываем её 
    else:
        graphik_element_button_1.path = "image/button_pressed.png"
        graphik_element_button_1.image_load()
        graphik_element_button_1.show_image(screen)

    # Делаем все тоже самое для второй кнопки
    if not Rect.colliderect(sprite1.image_sprite.RECT,graphik_element_button_2.RECT):

        graphik_element_button_2.show_image(screen)
    else:
        graphik_element_button_2.path = "image/button_pressed.png"
        graphik_element_button_2.image_load()
        graphik_element_button_2.show_image(screen)
    
    # Если нажали хоть одну из кнопок 
    if Rect.colliderect(sprite1.image_sprite.RECT,graphik_element_button_1.RECT) or Rect.colliderect(sprite1.image_sprite.RECT,graphik_element_button_2.RECT):
        # если дверь уже должна скоро закрыться а мы стоим на кнопке то вновь открываем её
        if dict_argument_door_block[str("Count_door_"+element_door)] <= 0:
            for el in range(len(dict_argument["list_surface"])):
                for element in range(len(dict_argument["list_surface"][el])):
                    if dict_argument["list_surface"][el][element] == element_door:
                        dict_argument["list_surface"][el][element] = element_door_empty
            drawSurfaces()
        # если кнопка нажата то постоянно обновляем счетчик закрывания двери
        dict_argument_door_block[str("Count_door_"+element_door)] = duration 
        

        
    # счетчик закрытия двери        
    if str("Count_door_"+element_door) in list(dict_argument_door_block.keys()):
        if dict_argument_door_block[str("Count_door_"+element_door)] > 0:
            dict_argument_door_block[str("Count_door_"+element_door)] -= 1

# Трескающаяся платформа
def cracking_platform(sprite):
        # Перебераем список сломаных платформ для того чтоб востановить их 
        for obj in broken_cracking_platform:
            # Переменная счетчик для востановления платформы 
            broken_cracking_platform[obj] -= 1
            # Когда платформа должна востановиться
            if broken_cracking_platform[obj] <= 0:
                # Разделяем имя обекта в котором были x и y по ,
                a = obj.split(",")
                # записываем координаты x и y по соотвецтвующим переменным
                x = int(a[1])
                y = int(a[0])
                # Возвращаем букву на матрицу
                dict_argument["list_surface"][y][x] = "c"
                # Убираем ету пллатформу из списка сломаных платформ и очищаем список обектов етих платформ чтоб он мог снова заполниться
                dict_list_border["list_border_cor_cracking"].clear()
                broken_cracking_platform.pop(obj)
                # Обновляем поверхности
                return True
        # Перебираем список елементов трескающихся платформ
        for i in dict_list_border["list_border_cor_cracking"]:   
            # Все буквы(вариации ) платформы
            list_cracking = ["c","с","C"] 
            # Узнаем какая вариация у платформы по ее изображению
            number = int(i[-2].path.split("_")[-1].split(".")[0]) 
            # Флаг колизия
            falg_colision = False
            # Проверяем колизию спрайта к платформе
            if sprite.image_sprite.X + sprite.image_sprite.WIDTH >= i[4] and sprite.image_sprite.X <= i[5]:
                if sprite.image_sprite.Y + sprite.image_sprite.HEIGHT >= i[0]:
                    if sprite.image_sprite.Y + sprite.image_sprite.HEIGHT <= i[0] + sprite.gravity_speed*2:
                        #КОлизия сбылась
                        falg_colision = True

            if falg_colision == True:
                # Изменяем счетчик трескания платформы   
                dict_list_border["list_border_cor_cracking"][dict_list_border["list_border_cor_cracking"].index(i)][6] -=1       
                # Анулируем шкалу востановления платформы
                dict_list_border["list_border_cor_cracking"][dict_list_border["list_border_cor_cracking"].index(i)][7] = dict_argument["speed_transparency_broken_platforms"]*2
            else:
                # Изменяем счетчик востановления платформы  если на ней не стоять
                dict_list_border["list_border_cor_cracking"][dict_list_border["list_border_cor_cracking"].index(i)][7] -= 1
            # Если счетчик трескания платформы доходит до нуля то изменяем картинку на следующую стадию или удаляем его
            if i[6] <= 0:
                # Проверяем можно ли изменяем картинку на следующую стадию
                if len(list_cracking) -1 >= number+1:
                    dict_argument["list_surface"][i[0]//(dict_argument["BLOCK_SIZE"])][i[4]//(dict_argument["BLOCK_SIZE"])] = list_cracking[number+1]
                    dict_list_border["list_border_cor_cracking"][dict_list_border["list_border_cor_cracking"].index(i)][-2].path = "image/cracking_platform_"+str(number+1)+".png"
                    dict_list_border["list_border_cor_cracking"][dict_list_border["list_border_cor_cracking"].index(i)][-2].image_load()
                    dict_list_border["list_border_cor_cracking"][dict_list_border["list_border_cor_cracking"].index(i)][6] = dict_argument["speed_transparency_broken_platforms"]
                # Если нет то удаляем платформу
                else:
                    # Убираем букву на матрицу заменяя её нулем(пустым местом)
                    dict_argument["list_surface"][i[0]//(dict_argument["BLOCK_SIZE"])][i[4]//(dict_argument["BLOCK_SIZE"])] = "0"
                    # Добавляем плуатформу в словарь сломаных трескающихся платформ дабы потом его возобновить ключом к которому являються кординаты через запятую
                    key = str(i[0]//(dict_argument["BLOCK_SIZE"]))+","+str(i[4]//(dict_argument["BLOCK_SIZE"]))
                    broken_cracking_platform[key] = 100
                    # Убираем ету пллатформу из списка платформ и очищаем список обектов етих платформ чтоб он мог снова заполниться
                    dict_list_border["list_border_cor_cracking"].clear()
                    # Обновляем поверхности
                    return True
            # Если счетчик востановления платформы доходит до нуля то изменяем картинку на превидущую стадию
            if i[7] <= 0:
                # Проверяем можно ли изменяем картинку на прошлую стадию
                if number - 1 >= 0:
                    dict_argument["list_surface"][i[0]//(dict_argument["BLOCK_SIZE"])][i[4]//(dict_argument["BLOCK_SIZE"])] = list_cracking[number-1]
                    dict_list_border["list_border_cor_cracking"][dict_list_border["list_border_cor_cracking"].index(i)][-2].path = "image/cracking_platform_"+str(number-1)+".png"
                    dict_list_border["list_border_cor_cracking"][dict_list_border["list_border_cor_cracking"].index(i)][-2].image_load()
                    dict_list_border["list_border_cor_cracking"][dict_list_border["list_border_cor_cracking"].index(i)][7] = 40

#Функция невидимой платформы
def invisibility_block(element_door,element_door_empty,sprite1):
    keys = key.get_pressed() 
    with open(os.path.join(os.path.abspath(__file__ + "/.."),'saves/config.json'),'r') as file:
            config = json.load(file)
    list_keys = config["keys"]
    if keys[list_keys[0]]:
        if dict_argument_block["count_load"] == 24: 
            use_sound.play_sound()
            for el in range(len(dict_argument["list_surface"])):
                for element in range(len(dict_argument["list_surface"][el])):
                    if dict_argument["list_surface"][el][element] == element_door_empty:
                        dict_argument["list_surface"][el][element] = element_door
            dict_argument_block["count_load"] = 0
            dict_Graphic_elements_obj["Circle_invible_block"] = Graphic_elements(sprite1.image_sprite.X,sprite1.image_sprite.Y,sprite1.image_sprite.WIDTH,sprite1.image_sprite.HEIGHT,"image/Circle_invible_block.png",1)
            drawSurfaces()
            
                            
    if dict_argument_block["count_load"] < 24:
        load.path = "image/Загрузка/Загрузка"+str(dict_argument_block["count_load"])+".png"
        load.image_load()
        load.show_image(screen)
       
        if dict_argument_block["flag_load"] >= 15:
            dict_argument_block["count_load"] += 1
            dict_argument_block["flag_load"] = 0
        dict_argument_block["flag_load"] += 1 
    
        if dict_argument_block["count_load"] == dict_argument["duration_invisible_block"] and dict_argument_block["flag_load"] == 1:
                
            for el in range(len(dict_argument["list_surface"])):
                for element in range(len(dict_argument["list_surface"][el])):
                    if dict_argument["list_surface"][el][element] == element_door:
                        dict_argument["list_surface"][el][element] = element_door_empty
    
            drawSurfaces()
    

    invisible_block_icon.show_image(screen)
        

    if dict_Graphic_elements_obj["Circle_invible_block"].NAME != None:      
        if dict_Graphic_elements_obj["Circle_invible_block"].NAME > 0:
            dict_Graphic_elements_obj["Circle_invible_block"].WIDTH += SCREEN_W//20
            dict_Graphic_elements_obj["Circle_invible_block"].HEIGHT += SCREEN_W//20
            dict_Graphic_elements_obj["Circle_invible_block"].X -= SCREEN_W//40
            dict_Graphic_elements_obj["Circle_invible_block"].Y -= SCREEN_W//40
            dict_Graphic_elements_obj["Circle_invible_block"].image_load()
            dict_Graphic_elements_obj["Circle_invible_block"].NAME += 1
            dict_Graphic_elements_obj["Circle_invible_block"].show_image(screen)
            if dict_Graphic_elements_obj["Circle_invible_block"].NAME >= 9:
                dict_Graphic_elements_obj["Circle_invible_block"].NAME = None# отображение последнего прорисованного экрана
    
# Функция движения облоков
def move_cloud():
    # Отрисовываем две картинки облоко дабы лента из них никогда не заканчивалась
    dict_Graphic_elements_obj["cloud"].show_image(screen)
    dict_Graphic_elements_obj["cloud2"].show_image(screen)
    # Двигаем два облока
    dict_Graphic_elements_obj["cloud"].X -= dict_argument_block["flag_move_cloud"]
    dict_Graphic_elements_obj["cloud2"].X -= dict_argument_block["flag_move_cloud"]
    #Перемещаем облоко после того как оно вышло из нашего поля зрения
    if dict_Graphic_elements_obj["cloud"].X == 0 - dict_Graphic_elements_obj["cloud"].WIDTH//2:
        dict_Graphic_elements_obj["cloud2"].X = dict_Graphic_elements_obj["cloud"].WIDTH//2
    #Перемещаем облоко после того как оно вышло из нашего поля зрения
    if dict_Graphic_elements_obj["cloud2"].X == 0 - dict_Graphic_elements_obj["cloud"].WIDTH//2:
        dict_Graphic_elements_obj["cloud"].X = dict_Graphic_elements_obj["cloud"].WIDTH//2
    
#Шипы
def spike():

    # Перебераем список с шипами отрисовываем их и если прикосаемся к ним умераем 
    for i in list_spikes:
        i.show_image(screen)
        sprite1.Touch_of_death(i.RECT,spike=True) 

    # Щетчик смены направления шипов
    if dict_argument_block["count_spike"] <= 0:
        dict_argument_block["count_spike"] = dict_argument["max_count_spike"]
        # Меняем направление шипов
        if dict_argument_block["direction_spike"] == "U":
            dict_argument_block["direction_spike"] = "D"
            # Меняем букву на матрице 
            for i in range(len(dict_argument["list_surface"])):      
                for j in range(len(dict_argument["list_surface"][i])):
                    if dict_argument["list_surface"][i][j] == "К":
                        if i+2 < len(dict_argument["list_surface"]) and dict_argument["list_surface"][i+2][j] == "0":
                            dict_argument["list_surface"][i+2][j] = "к"
                        else:
                            dict_argument["list_spikes_outside"].append([i,j])
                        dict_argument["list_surface"][i][j] = "0"
                    
        # Меняем направление шипов
        elif dict_argument_block["direction_spike"] == "D":
            dict_argument_block["direction_spike"] = "U"
            # Меняем букву на матрице 
            for i in range(len(dict_argument["list_surface"])):      
                for j in range(len(dict_argument["list_surface"][i])):
                    if dict_argument["list_surface"][i][j] == "к":
                        dict_argument["list_surface"][i-2][j] = "К"
                        dict_argument["list_surface"][i][j] = "0"
            for list_y_x in dict_argument["list_spikes_outside"]:
                dict_argument["list_surface"][list_y_x[0]][list_y_x[1]] = "К"


        # обновляем поверхности 
        drawSurfaces()
    # Переменная щетчик
    dict_argument_block["count_spike"] -= 1

#Функция пилы
def saw_function():
    # крутим пилу
    if dict_argument_angle["angle_saw"] <= -360:
        dict_argument_angle["angle_saw"] = 0
    dict_argument_angle["angle_saw"] -= 20
    # перебераем список со всеми пилами
    for saw in list_saw:
        # КОСТЫЛЬ
        saw.Y += dict_argument["BLOCK_SIZE"]
        # крутим пилу
        saw.image_load()
        saw_copy = transform.rotate(saw.IMG, int(dict_argument_angle["angle_saw"]))
        # Создаем рект обект пилы
        rect_saw = Rect(saw.X - saw.WIDTH//2+saw.WIDTH//10, saw.Y - saw.HEIGHT//2+saw.HEIGHT//10,saw.WIDTH-saw.WIDTH//5,saw.HEIGHT-saw.HEIGHT//5)
        # draw.rect(screen,(255,0,0),rect_saw)
        # Отображаем пилу
        screen.blit(saw_copy, (saw.X - int(saw_copy.get_width() / 2), saw.Y - int(saw_copy.get_height() / 2)))
        # Убиваем игрока при косании с пилой
        sprite1.Touch_of_death(rect_saw)
        # КОСТЫЛЬ
        saw.Y -= dict_argument["BLOCK_SIZE"]

# Функция облока подсказки
def help_function(index_x,index_y,indnex_width,index_height,text,color):
    # Задаем размеры
    border_width = dict_argument["BLOCK_SIZE"]
    border_height = dict_argument["BLOCK_SIZE"]
    # Создаем и отображаем изображение облока
    help_img = Graphic_elements(index_x*border_width,index_y*border_height,indnex_width*border_width,index_height*border_height,"image/help.png")
    help_img.show_image(screen)
    # Создаем и отображаем текст 
    text = Font("font/pixel_font.ttf",SCREEN_W//60,color,text,index_x*border_width+border_width//2,index_y*border_height+border_height//2,len(text.split(";")),False)
    text.show_text(screen)

# Функция птицы
def bird():
    # перебераем список птиц
    for obj in dict_argument["list_beard"]:
        # удаляем птицу если она вылетела за видимую зону
        if obj.X >= SCREEN_W:
            dict_argument["list_beard"].remove(obj)
        # Двигаем птицу
        obj.X += SCREEN_W//200
        random_direction_fly_bird = random.randint(1,2)
        #Двигаем птицу по Y в зависимости от рандомного числа
        if random_direction_fly_bird == 1:
            obj.Y -= random.randint(0,SCREEN_W//800)
        else:
            obj.Y += random.randint(0,SCREEN_W//800)
        # Создаем анимацию птице
        obj.NAME += 1
        if obj.NAME == 25:
            obj.NAME = 5
        if obj.NAME % 5 == 0:
            obj.path = "image/beard/beard"+str(obj.NAME//5)+".png"
            obj.image_load()
        # Отображаем птицу
        obj.show_image(screen)

    #Создаем птиц в рандомное время
    if dict_argument["max_number_beard"] <= dict_argument["count_beard"]:
        dict_argument["max_number_beard"] = random.randint(500,1000)
        dict_argument["count_beard"] = 0
        dict_argument["list_beard"].append(Graphic_elements(-dict_argument["BLOCK_SIZE"],dict_argument["BLOCK_SIZE"],dict_argument["BLOCK_SIZE"],dict_argument["BLOCK_SIZE"]//1.32,"image/beard/beard1.png",4))
    dict_argument["count_beard"] += 1

#Функция затемнения
def function_dimming():
    if dict_argument["screen_dimming_flag"] != None:
        if dict_argument["index_text_drimming"] == None:
            text_transition_new_lvl.font_content = dict_mision_lvl_1["location_"+str(dict_argument["index_location"])]
        else:
            text_transition_new_lvl.font_content = dict_text_drimming[dict_argument["index_text_drimming"]] 
        for obj in text_transition_new_lvl.font_content:
            if len(obj) < 38:
                count_space = (38 - len(obj))//2
                string = ""
                for i in range(count_space):
                    string += " "
                text_transition_new_lvl.font_content[text_transition_new_lvl.font_content.index(obj)] = string+obj+string
            
        text_transition_new_lvl.font_y = SCREEN_H//2-text_transition_new_lvl.font_size
        if dict_argument["screen_dimming_flag"] == "+":
            dict_argument["screen_dimming_count"] += 3
            if dict_argument["screen_dimming_count"] == 300:
                dict_argument["screen_dimming_flag"] = "-"
                if dict_argument["index_text_drimming"] in ["lose_game","win_game"]:
                    dict_argument["game"] = False
                    with open(os.path.join(os.path.abspath(__file__ + "/.."),'saves/saves.json'),'w') as file:
                        json.dump({"defolt": "true"},file,indent=4,ensure_ascii=True)
        if dict_argument["screen_dimming_flag"] == "-":
            dict_argument["screen_dimming_count"] -= 3
            if dict_argument["screen_dimming_count"] == 0:
                dict_argument["screen_dimming_flag"] = None
                
                dict_argument["index_text_drimming"] = None
        dimming.IMG.set_alpha(round(dict_argument["screen_dimming_count"]))
        dimming.show_image(screen)
        text_transition_new_lvl.show_text(screen)
# Функция движения карты
def move_map(direction):
    if dict_argument["index_lvl"] == 1:
        dict_argument["screen_dimming_flag"] = "+"
        dict_argument["index_text_drimming"] = None
    
    # Флаг направления оси
    flag_direction = None
    # Список в который будет помещена полная карта
    full_map = []
    list_full_surface = dict_argument["full_surface"]
    # Скорость передвижаня карты
    if dict_argument["BLOCK_SIZE"] == round(SCREEN_W/30):
        spead_move_map = 100
    else:
        spead_move_map = 200
    # Проверяем направление перемещения
    if direction == "right":
        # Соединяем матрицы
        for index in range(len(dict_argument["list_surface"])):
            str_list = []
            for i in dict_argument["list_surface"][index]:
                str_list.append(i)
            for i in list_full_surface[dict_argument["index_lvl"]][dict_argument["index_location"]][index]:
                str_list.append(i)
            full_map.append(list(str_list))
        # Задаем стартовую координауту отрисовки здувух матриц
        a = -SCREEN_W
        # Задаем ось для перемещнеия карты
        flag_direction = "X_MAP"
    # Проверяем направление перемещения
    elif direction == "left":
        # Соединяем матрицы
        for index in range(len(dict_argument["list_surface"])):
            str_list = []
            for i in list_full_surface[dict_argument["index_lvl"]][dict_argument["index_location"]][index]:
                str_list.append(i)
            for i in dict_argument["list_surface"][index]:
                str_list.append(i)
            
            full_map.append(list(str_list))
        # Задаем стартовую координауту отрисовки здувух матриц
        a = 0
         # Задаем ось для перемещнеия карты
        flag_direction = "X_MAP"
        # Задаем стартовую кординату отрисовку матрицу
        dict_argument[flag_direction] = -SCREEN_W
    # Проверяем направление перемещения
    elif direction == "down":
        # Соединяем матрицы
        for index in dict_argument["list_surface"]:
            full_map.append(index)
        for index in list_full_surface[dict_argument["index_lvl"]][dict_argument["index_location"]]:
            full_map.append(index)
        # Задаем стартовую координауту отрисовки здувух матриц
        a = -SCREEN_H
         # Задаем ось для перемещнеия карты
        flag_direction = "Y_MAP"
    # Проверяем направление перемещения
    elif direction == "up":
        # Соединяем матрицы
        for index in list_full_surface[dict_argument["index_lvl"]][dict_argument["index_location"]]:
            full_map.append(index)
        for index in dict_argument["list_surface"]:
            full_map.append(index)
        # Задаем стартовую координауту отрисовки здувух матриц
        a = 0
        # Задаем ось для перемещнеия карты
        flag_direction = "Y_MAP"
        # Задаем стартовую кординату отрисовку матрицу
        dict_argument[flag_direction] = -SCREEN_H
    
    
    dict_argument["list_surface"] = full_map
    # Проверяем направления
    if direction == "down" or direction == "right":
        # Цыкл движения

        while dict_argument[flag_direction] >= a:
            # Очищаем списки которые не очищаються в функции
            dict_list_border["list_border_cor_cracking"].clear()
            dict_list_border["list_border_cor_spring"].clear()
            # Обновляем матрицу
            drawSurfaces()
            # Отрисовываем фон
            dict_Graphic_elements_obj["Fon"].show_image(screen)
            # Функция движения облоков
            

            # отрисовывае всее виды блоков 
            for i in dict_list_border["list_border_cor"]:
                if i[-1] != "K":
                    i[-2].show_image(screen)
            for i in dict_list_border["list_border_cor_paper_and_door"]:
                i[-2].show_image(screen)  
            for i in dict_list_border["list_border_cor_ladder"]:
                i[-2].show_image(screen)
            for i in dict_list_border["list_border_cor_spring"]:
                i[-2].show_image(screen)
            for i in dict_list_border["list_border_cor_cracking"]:
                i[-2].show_image(screen)

            # Двигаем карта
            dict_argument[flag_direction] -= SCREEN_W//spead_move_map
            function_dimming()
            # Обновляем экран
            display.update()
    # Проверяем направления
    if direction == "up" or direction == "left":
        # Цыкл движения

        while dict_argument[flag_direction] <= a:
            # Очищаем списки которые не очищаються в функции
            dict_list_border["list_border_cor_cracking"].clear()
            dict_list_border["list_border_cor_spring"].clear()
            # Обновляем матрицу
            drawSurfaces()
            # Отрисовываем фон
            dict_Graphic_elements_obj["Fon"].show_image(screen)
            # Функция движения облоков
            

            # отрисовывае всее виды блоков 
            for i in dict_list_border["list_border_cor"]:
                if i[-1] != "K":
                    i[-2].show_image(screen)
            for i in dict_list_border["list_border_cor_paper_and_door"]:
                i[-2].show_image(screen)  
            for i in dict_list_border["list_border_cor_ladder"]:
                i[-2].show_image(screen)
            for i in dict_list_border["list_border_cor_spring"]:
                i[-2].show_image(screen)
            for i in dict_list_border["list_border_cor_cracking"]:
                i[-2].show_image(screen)

            # Двигаем карта
            dict_argument[flag_direction] += SCREEN_W//spead_move_map
            function_dimming()
            # Обновляем экран
            display.update()    
    
    # Меняем матрицу на другую
    dict_argument[flag_direction] = 0
    dict_argument["list_surface"] = list_full_surface[dict_argument["index_lvl"]][dict_argument["index_location"]]
    # Очищаем списки которые не очищаються в функции
    dict_list_border["list_border_cor_cracking"].clear()
    dict_list_border["list_border_cor_spring"].clear()
    # Обновляем матрицу
    drawSurfaces()

def shooting_lvl(screen,min_count_point,ammo_count,barriers):
    game = True
    mouse.set_visible(False)
    count_point = 0 

    list_variations_barriers = [Graphic_elements(0,0,SCREEN_W//10,SCREEN_W//10 // 1.76,"image/barrier_down.png"),Graphic_elements(0,0,SCREEN_W//10,SCREEN_W//10,"image/barrier_down_big.png"),Graphic_elements(0,0,SCREEN_W//10,SCREEN_W//10*1.67,"image/barrier_up.png"),Graphic_elements(0,0,SCREEN_W//10*1.21,SCREEN_W//10*1.83,"image/barrier_up_liana.png")]
    obj_barier_position_flag = True
    
    if barriers > 5:
        barriers = 5
    list_music_name[dict_argument["index_music"]].stop_music()
    ammo_img = Graphic_elements(SCREEN_W//100,SCREEN_W//100,dict_argument["BLOCK_SIZE"],dict_argument["BLOCK_SIZE"]//1.14,"image/ammo.png")
    
    left_side_stand_for_manniquens = Graphic_elements(0,0,dict_argument["BLOCK_SIZE"],dict_argument["BLOCK_SIZE"]*2.269,"image/left_side_stand_for_mannequins.png")
    right_side_stand_for_manniquens = Graphic_elements(0,0,dict_argument["BLOCK_SIZE"],dict_argument["BLOCK_SIZE"]*2.269,"image/right_side_stand_for_mannequins.png")
    middle_stand_for_manniquens = Graphic_elements(0,0,0,dict_argument["BLOCK_SIZE"]*2.269,"image/middle_stand_for_mannequins.png")
    
    list_down_stand_for_manniquens = [left_side_stand_for_manniquens,right_side_stand_for_manniquens,middle_stand_for_manniquens,[[Graphic_elements(None,0,SCREEN_W//10,SCREEN_W//10*1.693,None),"right",[],[]],[Graphic_elements(None,0,SCREEN_W//10,SCREEN_W//10*1.693,None),"right",[],[]]],[]]                 
    list_midle_stand_for_manniquens = copy.deepcopy(list_down_stand_for_manniquens)
    list_up_stand_for_manniquens = copy.deepcopy(list_down_stand_for_manniquens)
    list_stand = [
        list_down_stand_for_manniquens,
        list_midle_stand_for_manniquens,
        list_up_stand_for_manniquens
    ]
    if barriers != False:
        for obj in list_stand:
            for i in range(random.randint(1,barriers)):
                obj[-1].append(copy.deepcopy(random.choice(list_variations_barriers)))
    
    count_shoot_barrier = 0
    count_shoot_head = 0
    count_slip = ammo_count
    count_gun = 0
    gun = Sounds("sounds/gun.wav",int(config["SOUNDS_VOLUME"])/100)
    coin = Sounds("sounds/coins.wav",int(config["SOUNDS_VOLUME"])/100)
    statstic = Font("font/pixel_font.ttf",SCREEN_W//30,"black",str(count_point) +"/" + str(min_count_point),SCREEN_W-SCREEN_W//7,0,1,True)
    ammo_statistic = Font('font/pixel_font.ttf',SCREEN_W//30,"black",str(ammo_count),0 + SCREEN_W//15,SCREEN_W//100,1,True)
    list_music_name[dict_argument["index_music"]].load_music()
    while game:
        if not list_music_name[dict_argument["index_music"]].music_play():
            list_music_name[dict_argument["index_music"]].play_music()
        screen.fill("black")
        Background_shooting.show_image(screen)
        
        falg_motion = False  
        
        list_y_stand = [Background_shooting.Y + Background_shooting.HEIGHT - SCREEN_H//1.5,Background_shooting.Y + Background_shooting.HEIGHT//2,Background_shooting.Y + SCREEN_H//1.5] 
        for obj in range(len(list_stand)):
            list_s = list_stand[obj]
            list_s[0].X = Background_shooting.X + SCREEN_W//2 + SCREEN_W//9.5 + SCREEN_W//14 * obj
            list_s[1].X = Background_shooting.X + Background_shooting.WIDTH - SCREEN_W//2 - SCREEN_W//9.5 - SCREEN_W//14 * obj - list_s[1].WIDTH
            list_s[2].X = list_s[0].X + list_s[0].WIDTH 
            
            list_s[2].WIDTH = -1 * ((list_s[0].X + list_s[0].WIDTH) - list_s[1].X)
            list_s[2].image_load()
            

            
            
            list_s[0].Y = list_y_stand[obj]
            list_s[1].Y = list_s[0].Y
            list_s[2].Y = list_s[0].Y
            list_s[2].show_image(screen)
            
            if barriers != False:
                if obj_barier_position_flag:
                    for obj_barier in list_s[-1]:
                        obj_barier.start_x = random.randint(0,int(list_s[2].WIDTH - obj_barier.WIDTH))
                        
                    if len(list_s[-1]) > 1:
                        for obj_barier in list_s[-1]:
                            
                            obj_barier_another_flag = True
                            while obj_barier_another_flag:
                                for obj_barier_another in list_s[-1]:
                                    if list_s[-1].index(obj_barier_another) != list_s[-1].index(obj_barier):
                                        if obj_barier.start_x <= obj_barier_another.start_x and obj_barier.start_x >= obj_barier_another.start_x - obj_barier_another.WIDTH *1.5:
                                            obj_barier.start_x = random.randint(0,int(list_s[2].WIDTH - obj_barier.WIDTH)) 
                                            obj_barier_another_flag = True
                                            break
                                        elif obj_barier.start_x >= obj_barier_another.start_x and obj_barier.start_x <= obj_barier_another.start_x - obj_barier_another.WIDTH *1.5:
                                            obj_barier.start_x = random.randint(0,int(list_s[2].WIDTH - obj_barier.WIDTH))
                                            obj_barier_another_flag = True
                                            break
                                        else:
                                            obj_barier_another_flag = False
                    
   
            for i in list_s[-2]:
                list_barier_obj = list_s[-1]
                object = i[0]
                direction = i[1]
                list_hit = i[2]
                object.Y = list_s[2].Y - object.HEIGHT//2
                for obj_barier in list_barier_obj:
                    
                    if obj_barier.path == "image/barrier_down.png" or obj_barier.path == "image/barrier_down_big.png":
                        obj_barier.Y = object.Y + object.HEIGHT - obj_barier.HEIGHT
                    else:
                        obj_barier.Y = list_s[2].Y - obj_barier.HEIGHT//2

                    
                


                if object.X == None:
                    
                    object.path = "image/mannequen.png"
                    object.image_load()
                    object.NAME = random.randint(SCREEN_W//200,SCREEN_W//70)
                    object.start_x = random.randint(0,list_s[2].WIDTH - object.WIDTH)
                    object.X = list_s[2].X + object.start_x
                    

                                    
                    #Мы не можем это в цикле создать потому что разные координаты у каждой зоны
                    i[-1].append(Rect(object.X+object.WIDTH//2.578,object.Y+object.HEIGHT//16.6,object.WIDTH//3.769,object.WIDTH//3.769)) #Белая зона головы
                    i[-1].append(Rect(object.X+object.WIDTH//2.13,object.Y+object.HEIGHT//9.22,object.WIDTH//9.8,object.WIDTH//9.8)) #Красная зона головы
                    i[-1].append(Rect(object.X+object.WIDTH//9.8,object.Y+object.HEIGHT//2.184,object.WIDTH//1.195,object.WIDTH//1.195)) #Белая зона живота
                    i[-1].append(Rect(object.X+object.WIDTH//2.33,object.Y+object.HEIGHT//1.53,object.WIDTH//5.44,object.WIDTH//5.44)) #Красная зона живота
                    #
                    if list_s[-2].index(i) == 1 : 
                        while True:
                            if object.start_x <= list_s[-2][0][0].start_x and object.start_x >= list_s[-2][0][0].start_x - list_s[-2][0][0].WIDTH *1.5:
                                object.start_x = random.randint(0,int(list_s[2].WIDTH - object.WIDTH))

                             
                            elif object.start_x >= list_s[-2][0][0].start_x and object.start_x <= list_s[-2][0][0].start_x - list_s[-2][0][0].WIDTH *1.5:
                                object.start_x = random.randint(0,int(list_s[2].WIDTH - object.WIDTH))
                            else:
                                break
                            
                        
                
                if direction == "left":
                    object.start_x -= object.NAME
                    if object.start_x <= 0:
                        i[1] = "right"
                if direction == "right":
                    object.start_x += object.NAME
                    if object.start_x >= list_s[2].WIDTH - object.WIDTH:
                        i[1] = "left"
                
                
                object.X = list_s[2].X + object.start_x
                i[-1][0] = Rect(object.X+object.WIDTH//2.578,object.Y+object.HEIGHT//16.6,object.WIDTH//3.769,object.WIDTH//3.769) #Белая зона головы
                i[-1][1] = Rect(object.X+object.WIDTH//2.13,object.Y+object.HEIGHT//9.22,object.WIDTH//9.8,object.WIDTH//9.8) #Красная зона головы
                i[-1][2] = Rect(object.X+object.WIDTH//9.8,object.Y+object.HEIGHT//2.184,object.WIDTH//1.195,object.WIDTH//1.195) #Белая зона живота
                i[-1][3] = Rect(object.X+object.WIDTH//2.33,object.Y+object.HEIGHT//1.53,object.WIDTH//5.44,object.WIDTH//5.44) #Красная зона живота
                for obj_barier in list_barier_obj:
                    obj_barier.X = list_s[2].X + obj_barier.start_x
                object.show_image(screen)
                for hit in list_hit:
                    hit.X = object.X + hit.start_x
                    hit.Y = object.Y + hit.start_y
                    hit.show_image(screen)
            

            for object in list_s[-1]:
                object.show_image(screen)
            
            
        obj_barier_position_flag = False
        
        mouse_cor = mouse.get_pos()
        for event1 in event.get(): # Получаем значение события из "списка событий" 
            
            if event1.type == QUIT:
                pygame.quit()
            if event1.type == MOUSEMOTION:
                
                Background_shooting.X += int(event1.rel[0]) * -1
                Background_shooting.Y += int(event1.rel[1]) * -1
                falg_motion = True
                if Background_shooting.X > 0:
                    Background_shooting.X = 0
                if Background_shooting.Y > 0:
                    Background_shooting.Y = 0
                if Background_shooting.X < SCREEN_W - Background_shooting.WIDTH:
                    Background_shooting.X = SCREEN_W - Background_shooting.WIDTH
                if Background_shooting.Y < SCREEN_H - Background_shooting.HEIGHT:
                    Background_shooting.Y = SCREEN_H - Background_shooting.HEIGHT
            if event1.type == MOUSEBUTTONDOWN:      
                if event1.button == 1:
                    if count_gun == 0:
                        ammo_count -= 1
                        gun.play_sound()
                        count_gun = 60
                        for l_s in list_stand:
                            flag_barier = False
                            rect_barier = None
                            for obj_barier in l_s[-1]:
                                if obj_barier.path == "image/barrier_down.png" or obj_barier.path == "image/barrier_down_big.png":
                                    rect_barier = obj_barier.RECT
                                else:
                                    if obj_barier.path == "image/barrier_up_liana.png":
                                        rect_barier = Rect(obj_barier.RECT.x + obj_barier.RECT.width//8,obj_barier.RECT.y,obj_barier.RECT.width-obj_barier.RECT.width//8,obj_barier.RECT.height//2)
                                    else:
                                        rect_barier = Rect(obj_barier.RECT.x,obj_barier.RECT.y,obj_barier.RECT.width,obj_barier.RECT.height//2)
                            
                                if SCREEN_W//2 > rect_barier.x and SCREEN_W//2 < rect_barier.x + rect_barier.width and SCREEN_H//2 > rect_barier.y and SCREEN_H//2 < rect_barier.y + rect_barier.height:
                                    flag_barier = True
                                    count_shoot_barrier += 1
                                    break
                                
                            for obj in l_s[-2]:
                                if not flag_barier:
                                    if obj[0].check_mouse_cor((SCREEN_W//2,SCREEN_H//2)):
                                        factor_zone = 1
                                        for i in obj[-1]:
                                            if obj[-1].index(i) % 2:
                                                if SCREEN_W//2 > i.x and SCREEN_W//2 < i.x + i.width and SCREEN_H//2 > i.y and SCREEN_H//2 < i.y + i.height:
                                                    factor_zone = 3
                                                    if obj[-1].index(i) in [0,1]:
                                                        count_shoot_head += 1
                                                        factor_zone = 6
                                                    break
                                            else:
                                                if SCREEN_W//2 > i.x and SCREEN_W//2 < i.x + i.width and SCREEN_H//2 > i.y and SCREEN_H//2 < i.y + i.height:
                                                    factor_zone = 2
                                                    if obj[-1].index(i) in [0,1]:
                                                        count_shoot_head += 1
                                                        factor_zone = 4
                                        coin.play_sound()
                                        count_point += factor_zone * int(obj[0].NAME//(SCREEN_W//400))
                                        statstic.font_content = [str(count_point) +"/" + str(min_count_point)]
                                        print("Ты попал! На тебе", factor_zone * int(obj[0].NAME//(SCREEN_W//400)), "монет!")
                                        count_slip -= 1
                                        obj[2].append(Graphic_elements(SCREEN_W//2-obj[0].X-obj[0].WIDTH//11,SCREEN_H//2-obj[0].Y-obj[0].WIDTH//11,obj[0].WIDTH//5.5,obj[0].WIDTH//5.5,"image/hit_"+str(random.randint(1,5))+".png"))
                                        break
        if count_gun > 0:
            count_gun -= 1
        
        if mouse_cor[0]<= SCREEN_W//4 or mouse_cor[0]>= SCREEN_W - SCREEN_W//4 or mouse_cor[1]<= SCREEN_H//4 or mouse_cor[1]>= SCREEN_H - SCREEN_H//4:
            mouse.set_pos([SCREEN_W//2,SCREEN_H//2])
        if not falg_motion:
            mouse.set_pos([SCREEN_W//2,SCREEN_H//2])
        aim.show_image(screen)
        ammo_img.show_image(screen)
        ammo_statistic.font_content = [str(ammo_count)]
        ammo_statistic.show_text(screen)
        statstic.show_text(screen)
        clock.tick(FPS*2)
        if count_shoot_barrier >= 5:
            if not dict_achievement_boling["barrier"]:
                dict_achievement_boling["barrier"] = True
                dict_argument["list_flag_achievement"].append("barrier")
                
        if count_shoot_head >= 5:
            if not dict_achievement_boling["sniper"]:
                dict_achievement_boling["sniper"] = True
                dict_argument["list_flag_achievement"].append("sniper")
                
        if ammo_count <= 0:
            mouse.set_visible(True)
            save_game()
            
            return[ count_point,count_slip]
        function_dimming()
        display.update()
    mouse.set_visible(True)

dict_argument["puzzle_time"] = 0
list_part_puzzle = []
background = Graphic_elements(SCREEN_W//6.6,SCREEN_H//4,SCREEN_W//1.5,SCREEN_H//2,"image/puzzle/background.png")
for i in range(6):
    width,height = (image.load(os.path.join(os.path.abspath(__file__ + "/.."),"image/puzzle/"+str(i+1)+".png"))).get_rect().size
    element = Graphic_elements(0,0,width*SCREEN_W//1000,height*SCREEN_W//1000,"image/puzzle/"+str(i+1)+".png")
    if i+1 <= 3:
        element.X = background.X + SCREEN_W//50
        element.Y = background.Y +SCREEN_H//40 + ((element.HEIGHT+SCREEN_H//20)*i)
    else:
        element.X = background.X + background.WIDTH - SCREEN_W//10  
        element.Y = background.Y + SCREEN_H//40 + ((element.HEIGHT+SCREEN_H//20)*(i-3))
    element.start_x = element.X
    element.start_y = element.Y
    
    list_part_puzzle.append(element)
def puzzle(event):
    
    dict_argument["puzzle_time"] += 1
    background.show_image(screen)
    

    list_rect = [
        Rect(SCREEN_W//2.976,SCREEN_H//2.482,SCREEN_W//3.4//3,SCREEN_H//10.284),
        Rect(SCREEN_W//2.976+SCREEN_W//3.4//3,SCREEN_H//2.482,SCREEN_W//3.4//3,SCREEN_H//10.284),
        Rect(SCREEN_W//2.976+(SCREEN_W//3.4//3*2),SCREEN_H//2.482,SCREEN_W//3.4//3,SCREEN_H//10.284),
        Rect(SCREEN_W//2.976,SCREEN_H//2.482+SCREEN_H//10.284,SCREEN_W//3.4//3,SCREEN_H//10.284),
        Rect(SCREEN_W//2.976+SCREEN_W//3.4//3,SCREEN_H//2.482+SCREEN_H//10.284,SCREEN_W//3.4//3,SCREEN_H//10.284),
        Rect(SCREEN_W//2.976+(SCREEN_W//3.4//3*2),SCREEN_H//2.482+SCREEN_H//10.284,SCREEN_W//3.4//3,SCREEN_H//10.284)
    ]    


    for obj in list_part_puzzle:
        if event != False:
            if event.type == MOUSEBUTTONDOWN:
                if obj.check_mouse_cor(mouse.get_pos()):
                    if obj.NAME != "Final":
                        flag_another_obj = True
                        for another_obj in list_part_puzzle:
                            if another_obj.NAME == "True":
                                flag_another_obj = False
                                break
                        if flag_another_obj:
                            obj.NAME = "True"
            elif event.type == MOUSEBUTTONUP:
                if obj.NAME == "True":
                    
                    if list_rect[list_part_puzzle.index(obj)-3].collidepoint(mouse.get_pos()[0],mouse.get_pos()[1]):
                        obj.X = list_rect[list_part_puzzle.index(obj)-3].x
                        if list_part_puzzle.index(obj)-3 >= 0:
                            obj.Y = list_rect[list_part_puzzle.index(obj)-3].y
                            
                        else:
                            obj.Y = list_rect[list_part_puzzle.index(obj)-3].y + list_rect[list_part_puzzle.index(obj)-3].height - obj.HEIGHT
                            
                        obj.NAME = "Final"    
                    else:
                        obj.NAME = "False"
                        obj.X = obj.start_x
                        obj.Y = obj.start_y
            if obj.NAME == "True":

                list_part_puzzle[list_part_puzzle.index(obj)].X = mouse.get_pos()[0] - obj.WIDTH//2
                list_part_puzzle[list_part_puzzle.index(obj)].Y = mouse.get_pos()[1] - obj.HEIGHT//2
    final_puzzle = True      
    for obj in list_part_puzzle:
        if obj.NAME != "Final":
            final_puzzle = False
            break
    if final_puzzle:
        if dict_argument["count_final_puzzle"] == None:
            dict_argument["count_final_puzzle"] = 100
        background.path = "image/puzzle/background_full.png"
        background.image_load()
    else:
        for obj in list_part_puzzle:
                obj.show_image(screen)
    if dict_argument["count_final_puzzle"] != None:
        if dict_argument["count_final_puzzle"] > 0:
            dict_argument["count_final_puzzle"] -= 1
        if dict_argument["count_final_puzzle"] <= 0:
            dict_argument["flag_puzzle_location"] = False
            if dict_argument["puzzle_time"] <= 30 * 5:
                if not dict_achievement_boling["puzzle_lower"]:
                    dict_achievement_boling["puzzle_lower"] = True
                    dict_argument["list_flag_achievement"].append("puzzle_lower")
                    
            
def slider(sound_power, flag_mouse_volume_sound, rect_volume_sound, mouse_volume_sound, mouse_cor, text, win, divider = 1 , plus = 0):
    sound_power.show_text(win)
    if flag_mouse_volume_sound:
        if mouse_volume_sound.x >= rect_volume_sound.x and mouse_volume_sound.x <= rect_volume_sound.x+rect_volume_sound.width:
            mouse_volume_sound.x = mouse_cor[0]-mouse_volume_sound.width//2
        if mouse_volume_sound.x <= rect_volume_sound.x:
            mouse_volume_sound.x = rect_volume_sound.x
        if mouse_volume_sound.x >= rect_volume_sound.x+rect_volume_sound.width:
            mouse_volume_sound.x = rect_volume_sound.x+rect_volume_sound.width
    count_volume = round((mouse_volume_sound.x-rect_volume_sound.x)/rect_volume_sound.width*100)
    sound_power.font_content = [text+str(int(count_volume/divider + plus))]
    rect_volume_sound.width+=mouse_volume_sound.width
    rect_volume_sound_stroke = pygame.Rect(rect_volume_sound.left - SCREEN_W//300,rect_volume_sound.top - SCREEN_W//300,rect_volume_sound.width + SCREEN_W//150,rect_volume_sound.height + SCREEN_W//150)
    pygame.draw.rect(win,"black",rect_volume_sound_stroke)
            
    if flag_mouse_volume_sound:
        pygame.draw.rect(win,"darkgreen",rect_volume_sound)
    else:
        pygame.draw.rect(win,"gray",rect_volume_sound)
    rect_volume_sound.width-=mouse_volume_sound.width
            
    mouse_volume_sound_stroke = pygame.Rect(mouse_volume_sound.left - SCREEN_W//300,mouse_volume_sound.top - SCREEN_W//300,mouse_volume_sound.width + SCREEN_W//150,mouse_volume_sound.height + SCREEN_W//150)
    pygame.draw.rect(win,"black",mouse_volume_sound_stroke)
    if flag_mouse_volume_sound:
        pygame.draw.rect(win,"green",mouse_volume_sound)
    else:
        pygame.draw.rect(win,"white",mouse_volume_sound)
  
def menu(run_game):
    with open(os.path.join(os.path.abspath(__file__ + "/.."),'saves/config.json'),'r') as file:
        config = json.load(file)
    win = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    def option():
        
        with open(os.path.join(os.path.abspath(__file__ + "/.."),'saves/saves.json'),'r') as file:
            saves = json.load(file)
        MUSIC_VOLUME = int(config["MUSIC_VOLUME"])
        SOUNDS_VOLUME = int(config["SOUNDS_VOLUME"])
        bg_option = Graphic_elements(0, 0, SCREEN_W, SCREEN_H, 'image/menu/option_bg_'+config["language"]+'.png')
        flag_option = "not"
        sound_power = Font("font/pixel_font.ttf",SCREEN_W//30,"black",dict_languages_settings["1"][config["language"]]+str(SOUNDS_VOLUME),SCREEN_W//3.2,SCREEN_H//8,bold=False)
        music_power = Font("font/pixel_font.ttf",SCREEN_W//30,"black",dict_languages_settings["2"][config["language"]]+str(MUSIC_VOLUME),SCREEN_W//3.2,SCREEN_H//3,bold=False)
        flag_mouse_volume_sound = False
        rect_volume_sound = pygame.Rect(SCREEN_W//3.2,SCREEN_H//4.5,SCREEN_W//1.6,SCREEN_H//25)
        mouse_volume_sound = pygame.Rect(SOUNDS_VOLUME*rect_volume_sound.width/100+rect_volume_sound.x,rect_volume_sound.top-(SCREEN_H//45*3-rect_volume_sound.height)//2,SCREEN_H//72*2,SCREEN_H//45*3)
        flag_mouse_volume_music = False
        rect_volume_music = pygame.Rect(SCREEN_W//3.2,SCREEN_H//2.3,SCREEN_W//1.6,SCREEN_H//25)
        mouse_volume_music = pygame.Rect(MUSIC_VOLUME*rect_volume_music.width/100+rect_volume_music.x,rect_volume_music.top-(SCREEN_H//45*3-rect_volume_music.height)//2,SCREEN_H//72*2,SCREEN_H//45*3)
        distation_button = SCREEN_H//5.15-SCREEN_H//10.3
        button_video = Graphic_elements(SCREEN_W//67.3, SCREEN_H//10.3, SCREEN_W//4.3, SCREEN_H//11.7,"image/menu/button_"+config["language"]+"/video_w.png")
        button_audio = Graphic_elements(SCREEN_W//67.3, SCREEN_H//10.3+distation_button, SCREEN_W//4.3, SCREEN_H//11.7,"image/menu/button_"+config["language"]+"/audio_w.png")
        button_control = Graphic_elements(SCREEN_W//67.3, SCREEN_H//10.3+distation_button*2, SCREEN_W//4.3, SCREEN_H//11.7,"image/menu/button_"+config["language"]+"/control_w.png")
        button_language = Graphic_elements(SCREEN_W//67.3, SCREEN_H//10.3+distation_button*3, SCREEN_W//4.3, SCREEN_H//11.7,"image/menu/button_"+config["language"]+"/language_w.png")
        button_delete = Graphic_elements(SCREEN_W//67.3, SCREEN_H-distation_button*1.6, SCREEN_W//4.3, SCREEN_H//11.7*1.5,"image/menu/button_"+config["language"]+"/delete_w.png")
        if saves["defolt"] == "true":
            button_delete.path = "image/menu/button_"+config["language"]+"/delete_not_work.png"
        text_control = Font("font/pixel_font.ttf",SCREEN_W//20,'black',dict_languages_settings["3"][config["language"]],SCREEN_W//3.2,SCREEN_H//8)
        button_display_size = Font("font/pixel_font.ttf",SCREEN_W//20,'black',dict_languages_settings["4"][config["language"]],SCREEN_W//3.2,SCREEN_H//8)
        list_buttons_display_size =[
                        Font("font/pixel_font.ttf",SCREEN_W//38,'black','1280x720',button_display_size.font_x,button_display_size.font_y+SCREEN_H//8),
                        Font("font/pixel_font.ttf",SCREEN_W//38,'black','1600x920',button_display_size.font_x+SCREEN_W//14.2*2,button_display_size.font_y+SCREEN_H//8),
                        Font("font/pixel_font.ttf",SCREEN_W//38,'black','1920x1080',button_display_size.font_x+SCREEN_W//14.2*4,button_display_size.font_y+SCREEN_H//8),
        ]
        text_language = Font("font/pixel_font.ttf",SCREEN_W//20,'black',dict_languages_settings["10"][config["language"]],SCREEN_W//3.2,SCREEN_H//8)
        list_button_text_language = [
            [Graphic_elements(SCREEN_W//3.2,SCREEN_H//7+SCREEN_W//18,SCREEN_W//38,SCREEN_W//38,"image/menu/square.png"),Font("font/pixel_font.ttf",SCREEN_W//38,'black','English',SCREEN_W//2.8,SCREEN_H//7+SCREEN_W//18)],
            [Graphic_elements(SCREEN_W//3.2,SCREEN_H//7+SCREEN_W//20*2,SCREEN_W//38,SCREEN_W//38,"image/menu/square.png"),Font("font/pixel_font.ttf",SCREEN_W//38,'black','Українська',SCREEN_W//2.8,SCREEN_H//7+SCREEN_W//20*2)]
        ]
        flag_delete_saves = False
        list_control = []
        list_text_control = dict_languages_settings["5"][config["language"]]
        list_keys = copy.deepcopy(config["keys"])
        list_text_button_control = copy.deepcopy(config["list_text_button_control"])
        for i in range(5):
            obj = Graphic_elements(SCREEN_W//3.2,SCREEN_H//4 + SCREEN_W//15 * i,SCREEN_W//2, SCREEN_W//20, "image/menu/menu_button_change.png")
            text = Font("font/pixel_font.ttf",SCREEN_W//40,'white',list_text_control[i],obj.X + SCREEN_W//40,obj.Y + SCREEN_W//90)
            text_button = Font("font/pixel_font.ttf",SCREEN_W//40,'black',list_text_button_control[i],obj.X + SCREEN_W//3,obj.Y + SCREEN_W//90)
            list_control.append([obj,text,text_button])
        
        for obj in list_buttons_display_size:
            width = SCREEN_W
            height = SCREEN_H
            obj_width = obj.font_content[0].split('x')[0]
            obj_height = obj.font_content[0].split('x')[1]
            if (int(obj_width) == width and int(obj_height) == height):
                obj.font_color = 'red'
                break

        button_display_fullsize = Font("font/pixel_font.ttf",SCREEN_W//25,'black',dict_languages_settings["6"][config["language"]],SCREEN_W//3.2,SCREEN_H//3)
        list_button_display_fullsize = [
            Font("font/pixel_font.ttf",SCREEN_W//25,'black',dict_languages_settings["7"][config["language"]],SCREEN_W//3.2*1.5,button_display_fullsize.font_y + SCREEN_H//8),
            Font("font/pixel_font.ttf",SCREEN_W//25,'black',dict_languages_settings["8"][config["language"]],SCREEN_W//3.2*1.2,button_display_fullsize.font_y + SCREEN_H//8)
        ]
        if config["language"] == "uk":
            list_button_text_language[0][0].path = "image/menu/square_selected.png"
        elif config["language"] == "ua":
            list_button_text_language[1][0].path = "image/menu/square_selected.png"
        if int(config["SCREEN_WIDTH"]) == 0 and int(config["SCREEN_HEIGHT"]) == 0:
            list_button_display_fullsize[0].font_color = 'red'
            for obj in list_buttons_display_size:
                obj.font_color = (93, 93, 93)
            
        else:
            list_button_display_fullsize[1].font_color = 'red'
        run_option = True
        list_music_name[dict_argument["index_music"]].load_music()
        while run_option: 
            if not list_music_name[dict_argument["index_music"]].music_play():
                list_music_name[dict_argument["index_music"]].play_music()
            for event in pygame.event.get():
                #Услове выхода из игры
                mouse_cor = pygame.mouse.get_pos() 

                if event.type == pygame.QUIT:
                    run_option = False
                if event.type == pygame.KEYDOWN:
                    for obj in list_control:
                        if obj[2].font_color == "yellow" and event.key != 1073741881:
                            if event.key == 13:#ЕНТЕР
                                obj[2].font_content[0] = "Enter"
                            elif event.key == 9:#ТАБ  
                                obj[2].font_content[0] = "Tab"
                            elif event.key == 32:#ПРОБЕЛ 
                                obj[2].font_content[0] = "Space"
                            elif event.key == 1073742048 or event.key == 1073742052:#КОНТРАЛ
                                obj[2].font_content[0] = "Ctrl"
                            elif event.key == 1073742049 or event.key == 1073742053:#ШИФТ
                                obj[2].font_content[0] = "Shift"
                            elif event.key == 1073742050 or event.key == 1073742054:#АЛЬТ
                                obj[2].font_content[0] = "Alt"
                            elif event.key == 1073741906:#Вверх
                                obj[2].font_content[0] = "up"
                            elif event.key == 1073741905:#вниз
                                obj[2].font_content[0] = "down"
                            elif event.key == 1073741904:#влево
                                obj[2].font_content[0] = "left"
                            elif event.key == 1073741903:#вправо
                                obj[2].font_content[0] = "right"
                            else:
                                if not event.unicode in list("йцукенгшщзхъфывапролджэячсмитьбю"):
                                    obj[2].font_content[0] = str(event.unicode)
                            if not event.unicode in list("йцукенгшщзхъфывапролджэячсмитьбю"):
                                list_keys[list_control.index(obj)] = event.key
                                list_text_button_control[list_control.index(obj)] = obj[2].font_content[0].lower()
                                obj[2].start_content = obj[2].font_content[0]
                                
                                obj[2].font_content[0] = "> "+obj[2].font_content[0]+" <"

    
                                break

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    use_sound.play_sound()
                    obj_button_option = pygame.Rect(0, 0, SCREEN_W//3.8, SCREEN_H) 
                    obj_back = pygame.Rect(SCREEN_W//91.4, SCREEN_H//130, SCREEN_W//10.24, SCREEN_H//20.571)
                    if flag_option == "language":
                        for i in list_button_text_language:
                            if i[0].check_mouse_cor(mouse_cor):
                                for obj in list_button_text_language:
                                    obj[0].path = "image/menu/square.png"
                                    obj[0].image_load()
                                i[0].path = "image/menu/square_selected.png"
                                i[0].image_load()
                    if flag_option == "control":
                        for obj in list_control:
                            if obj[0].RECT.collidepoint(mouse_cor[0],mouse_cor[1]):
                                for obj2 in list_control:
                                    obj2[0].path = "image/menu/menu_button_change.png"
                                    obj2[0].image_load()
                                    obj2[2].font_content[0] = obj2[2].start_content
                                    obj2[2].font_color = "black"
                                obj[0].path = "image/menu/presed_menu_button_change.png"
                                obj[0].image_load()
                                if not ">" in obj[2].font_content[0]:
                                    obj[2].font_content[0] = "> "+obj[2].font_content[0].split("  ")[-1]+" <"
                                obj[2].font_color = "yellow"
                                break
                            else:
                                for obj2 in list_control:
                                    obj2[0].path = "image/menu/menu_button_change.png"
                                    obj2[0].image_load()
                                    obj2[2].font_content[0] = obj2[2].start_content
                                    obj2[2].font_color = "black"

                    if obj_button_option.collidepoint(mouse_cor[0],mouse_cor[1]):
                        if obj_back.collidepoint(mouse_cor[0],mouse_cor[1]) :
                            #СДЕСЬ СОХРАНЯЕМ ДАННЫЕ
                            if list_button_display_fullsize[0].font_color == 'red':
                                FULLSCREEN = True
                                SCREEN_WIDTH = 0
                                SCREEN_HEIGHT = 0
                            else:
                                FULLSCREEN = False
                                for obj in list_buttons_display_size:
                                    if obj.font_color == 'red':
                                        SCREEN_WIDTH = obj.font_content[0].split('x')[0]
                                        SCREEN_HEIGHT = obj.font_content[0].split('x')[1]
                                        break
                            MUSIC_VOLUME = music_power.font_content[0].split(dict_languages_settings["2"][config["language"]])[-1]
                            SOUNDS_VOLUME = sound_power.font_content[0].split(dict_languages_settings["1"][config["language"]])[-1]
                            if list_button_text_language[0][0].path == "image/menu/square_selected.png":
                                language = "uk"
                            elif list_button_text_language[1][0].path == "image/menu/square_selected.png":
                                language = "ua"
                            settings = {
                                "SCREEN_WIDTH": SCREEN_WIDTH,
                                "SCREEN_HEIGHT": SCREEN_HEIGHT,
                                "SOUNDS_VOLUME": SOUNDS_VOLUME,
                                "FULLSCREEN": FULLSCREEN,
                                "MUSIC_VOLUME": MUSIC_VOLUME,
                                "list_text_button_control":list_text_button_control,
                                "keys":list_keys,
                                "language":language

                            }
                            for obj in config.keys():
                                if settings[obj] != config[obj]:
                                    run_option = False
                                    with open(os.path.join(os.path.abspath(__file__ + "/.."),'saves/config.json'),'w') as file:
                                        json.dump(settings,file,indent=4,ensure_ascii=True)
                                    return "stop"
                            
                            run_option = False
                            with open(os.path.join(os.path.abspath(__file__ + "/.."),'saves/config.json'),'w') as file:
                                json.dump(settings,file,indent=4,ensure_ascii=True)
                            if flag_delete_saves:
                                return "stop"
                        elif button_video.RECT.collidepoint(mouse_cor[0],mouse_cor[1]):
                            flag_option = "video"
                        elif button_audio.RECT.collidepoint(mouse_cor[0],mouse_cor[1]):
                            flag_option = "audio"
                        elif button_control.RECT.collidepoint(mouse_cor[0],mouse_cor[1]):
                            flag_option = "control"
                        elif button_language.RECT.collidepoint(mouse_cor[0],mouse_cor[1]):
                            flag_option = "language"
                        
                        elif button_delete.RECT.collidepoint(mouse_cor[0],mouse_cor[1]) and button_delete.path != "image/menu/button_"+config["language"]+"/delete_not_work.png":
                            button_delete.path = "image/menu/button_"+config["language"]+"/delete_not_work.png"
                            button_delete.image_load()
                            
                            
                            flag_delete_saves = True
                            with open(os.path.join(os.path.abspath(__file__ + "/.."),'saves/saves.json'),'w') as file:                                
                                json.dump({"defolt":"true"},file,indent=4,ensure_ascii=True)
                            

                                
                        else:
                            flag_option = "not"
                    if flag_option == "audio":        
                        if pygame.Rect.collidepoint(mouse_volume_sound,mouse_cor[0],mouse_cor[1]):
                            flag_mouse_volume_sound = True
                        if pygame.Rect.collidepoint(mouse_volume_music,mouse_cor[0],mouse_cor[1]):
                            flag_mouse_volume_music = True
                    if flag_option == "video":
                        if list_button_display_fullsize[1].font_color == "red":
                            for i in list_buttons_display_size:
                                if i.check_mouse_cor_font(mouse_cor):
                                    for obj in list_buttons_display_size:
                                        obj.font_color = "black"
                                    i.font_color = "red"
                                    break
                        for i in list_button_display_fullsize:
                            if i.check_mouse_cor_font(mouse_cor):
                                for obj in list_button_display_fullsize:
                                    obj.font_color = "black"
                                if i.font_content[0] == dict_languages_settings["7"][config["language"]]:
                                    for obj2 in list_buttons_display_size:
                                        obj2.font_color = (93, 93, 93)
                                        
                                else:
                                    for obj2 in list_buttons_display_size:
                                        obj2.font_color = "black"
                                    list_buttons_display_size[0].font_color = "red"
                                i.font_color = "red"
                                break

                if event.type == pygame.MOUSEBUTTONUP:
                    if flag_option == "audio":  
                        if flag_mouse_volume_sound:
                            flag_mouse_volume_sound = False
                        if flag_mouse_volume_music:
                            flag_mouse_volume_music = False
            
            
            bg_option.show_image(win)
            button_video.show_image(win)
            button_audio.show_image(win)
            button_control.show_image(win)
            button_language.show_image(win)
            button_delete.show_image(win)
            if flag_option == "not":
                help_text = Font("font/pixel_font.ttf",SCREEN_W//30,"black",dict_languages_settings["9"][config["language"]],SCREEN_W//3.2,SCREEN_H//8,bold=False,index=5)
                help_text.show_text(win)

                
            if flag_option == "video":
                if button_video.path != "image/menu/button_"+config["language"]+"/video_b.png":
                    button_video.path = "image/menu/button_"+config["language"]+"/video_b.png"
                    button_video.image_load()
                button_display_size.show_text(win)
                for i in list_buttons_display_size:
                    i.show_text(win)
                button_display_fullsize.show_text(win)
                for i in list_button_display_fullsize:
                    i.show_text(win)
            else:
                if button_video.path != "image/menu/button_"+config["language"]+"/video_w.png":
                    button_video.path = "image/menu/button_"+config["language"]+"/video_w.png"
                    button_video.image_load()
            if flag_option == "audio":
                if button_audio.path != "image/menu/button_"+config["language"]+"/audio_b.png":
                    button_audio.path = "image/menu/button_"+config["language"]+"/audio_b.png"
                    button_audio.image_load()
                slider(sound_power, flag_mouse_volume_sound, rect_volume_sound, mouse_volume_sound, mouse_cor, dict_languages_settings["1"][config["language"]],win)
                slider(music_power, flag_mouse_volume_music, rect_volume_music, mouse_volume_music, mouse_cor, dict_languages_settings["2"][config["language"]],win)
            else:
                if button_audio.path != "image/menu/button_"+config["language"]+"/audio_w.png":
                    button_audio.path = "image/menu/button_"+config["language"]+"/audio_w.png"
                    button_audio.image_load()
            if flag_option == "control":
                if button_control.path != "image/menu/button_"+config["language"]+"/control_b.png":
                    button_control.path = "image/menu/button_"+config["language"]+"/control_b.png"
                    button_control.image_load() 
                text_control.show_text(win)
                for obj in list_control:
                    obj[0].show_image(win)
                    obj[1].show_text(win)
                    obj[2].show_text(win)
            else:
                if button_control.path != "image/menu/button_"+config["language"]+"/control_w.png":
                    button_control.path = "image/menu/button_"+config["language"]+"/control_w.png"
                    button_control.image_load() 
            if flag_option == "language":
                if button_language.path != "image/menu/button_"+config["language"]+"/language_b.png":
                    button_language.path = "image/menu/button_"+config["language"]+"/language_b.png"
                    button_language.image_load() 
                text_language.show_text(win)
                for i in list_button_text_language:
                    i[0].show_image(win)
                    i[1].show_text(win)
                    if i[0].path != "image/menu/square_selected.png":
                        if i[0].check_mouse_cor(mouse_cor):
                            i[0].path = "image/menu/square_aiming.png"
                            i[0].image_load() 
                        else:
                            i[0].path = "image/menu/square.png"
                            i[0].image_load() 
            else:
                if button_language.path != "image/menu/button_"+config["language"]+"/language_w.png":
                    button_language.path = "image/menu/button_"+config["language"]+"/language_w.png"
                    button_language.image_load() 
            pygame.display.flip()

    def achievement():
        rgb_platinum = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        bg_achievement = Graphic_elements(0, 0, SCREEN_W, SCREEN_H, 'image/achivement/bg_'+config["language"]+'.png')
        list_achievement = []
        for key_achievemen in list(dict_achievement_boling.keys()):
            list_obj = [Graphic_elements(SCREEN_W//2-SCREEN_W//3.78,SCREEN_H//11,SCREEN_W//1.89,SCREEN_H//8,"image/achivement/slot.png"),
                        Graphic_elements(0,0,SCREEN_W//18,SCREEN_W//18,"image/achivement/"+key_achievemen+"_bw.png"),
                        Font("font/pixel_font.ttf",SCREEN_W//50,"white",dict_laungues_achievement[key_achievemen][0][config["language"]],0,0),
                        Font("font/pixel_font.ttf",SCREEN_W//75,(219, 219, 219),dict_laungues_achievement[key_achievemen][1][config["language"]],0,0,index=2,bold=False)
            ]
            if dict_achievement_boling[key_achievemen]:
                list_obj[1].path = "image/achivement/"+key_achievemen+"_rgb.png"
                list_achievement.insert(0,list_obj)
            else:
                list_achievement.append(list_obj)
        for obj in list_achievement:
            obj[0].Y += (SCREEN_H//7) * list_achievement.index(obj)
            obj[1].X = obj[0].X + SCREEN_W//120
            obj[1].Y = obj[0].Y + SCREEN_W//120
            obj[2].font_x = obj[0].X + SCREEN_W//15
            obj[2].font_y = obj[0].Y + SCREEN_W//120
            obj[2].start_y = obj[2].font_y
            obj[3].font_x = obj[0].X + SCREEN_W//15
            obj[3].font_y = obj[0].Y + SCREEN_W//30
            obj[3].start_y = obj[3].font_y
        run = True
        while run:
            clock.tick(FPS)
            win.fill((69, 69, 69))
            for ach_img in list_achievement:
                if ach_img[1].path.split("/")[-1].split("_rgb")[0] == "platinum":
                    for i in range(3):
                        rgb_platinum[i] += random.randint(-20,20)*2
                        if rgb_platinum[i] > 255:
                            rgb_platinum[i] = 255
                        if rgb_platinum[i] < 0:
                            rgb_platinum[i] = 0
                        
                    ach_img[2].font_color = (rgb_platinum[0],rgb_platinum[1],rgb_platinum[2])
                if ach_img[0].Y + ach_img[0].HEIGHT > 0:
                    if ach_img[0].Y < SCREEN_H:
                        ach_img[0].show_image(win)
                        ach_img[1].show_image(win)
                        ach_img[2].show_text(win)
                        ach_img[3].show_text(win)
            bg_achievement.show_image(win)
            for event in pygame.event.get():
                #Услове выхода из игры
                if event.type == pygame.MOUSEWHEEL:
                    if event.y < 0:
                        if list_achievement[-1][0].Y >= SCREEN_H - SCREEN_H//7:
                            for obj in list_achievement:
                                obj[0].Y -= SCREEN_W//20
                                obj[1].Y -= SCREEN_W//20
                                obj[3].font_y = obj[0].Y + SCREEN_W//30
                                obj[3].start_y = obj[3].font_y
                                obj[2].font_y = obj[0].Y + SCREEN_W//120
                                obj[2].start_y = obj[2].font_y
                    else:   
                        if list_achievement[0][0].Y <= list_achievement[0][0].start_y:
                            for obj in list_achievement:
                                obj[0].Y += SCREEN_W//20
                                obj[1].Y += SCREEN_W//20
                                obj[3].font_y = obj[0].Y + SCREEN_W//30
                                obj[3].start_y = obj[3].font_y
                                obj[2].font_y = obj[0].Y + SCREEN_W//120
                                obj[2].start_y = obj[2].font_y
                mouse_cor = pygame.mouse.get_pos() 

                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    
                    obj_back = pygame.Rect(SCREEN_W//91.4, SCREEN_H//130, SCREEN_W//10.24, SCREEN_H//20.571)
                    if obj_back.collidepoint(mouse_cor[0],mouse_cor[1]) :
                        use_sound.play_sound()
                        run = False
            display.update()
    bg = Graphic_elements(0, 0, SCREEN_W, SCREEN_H, 'image/menu/bg.png')
    task_board =  Graphic_elements(SCREEN_W//3,SCREEN_H//3,SCREEN_W//3,SCREEN_H//3,"image/menu/task_board.png")
    task_board.image_load()
    task_board.IMG = transform.rotate(task_board.IMG,10)
    name_menu = Graphic_elements(SCREEN_W//20,SCREEN_H//40, SCREEN_W//1.7, SCREEN_H//7, 'image/menu/name.png')
    button_play = Graphic_elements(SCREEN_W//1.395,SCREEN_H//6.1, SCREEN_W//3.5, SCREEN_H//7.8, 'image/menu/button_'+config["language"]+'/button_play.png')
    button_option = Graphic_elements(SCREEN_W//1.395,SCREEN_H//2 - SCREEN_H//15.6, SCREEN_W//3.5, SCREEN_H//7.8, 'image/menu/button_'+config["language"]+'/button_option.png')
    button_exit = Graphic_elements(SCREEN_W//1.395,SCREEN_H//1.4, SCREEN_W//3.5, SCREEN_H//7.8, 'image/menu/button_'+config["language"]+'/button_exit.png')
    run = True
    list_music_name[dict_argument["index_music"]].load_music()
    while run: 
        if not list_music_name[dict_argument["index_music"]].music_play():
            list_music_name[dict_argument["index_music"]].play_music()
        for event in pygame.event.get():
            #Услове выхода из игры
            mouse_cor = pygame.mouse.get_pos() 

            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if task_board.check_mouse_cor(mouse_cor):
                    achievement()
                if button_exit.check_mouse_cor(mouse_cor):
                    run = False
                    use_sound.play_sound()
                if button_option.check_mouse_cor(mouse_cor):
                    use_sound.play_sound()
                    if option() == "stop":
                        return "stop"
                if button_play.check_mouse_cor(mouse_cor):
                    use_sound.play_sound()
                    sprite1.image_sprite.X = dict_argument["BLOCK_SIZE"]*dict_argument["sprite_x"]
                    sprite1.image_sprite.Y = dict_argument["BLOCK_SIZE"]*dict_argument["sprite_y"]
                    dict_argument["game"] = True
                    run_game()
                    
                    
                
                            
                        


            
        bg.show_image(win)    
        name_menu.show_image(win)
        button_play.show_image(win)
        button_option.show_image(win)
        button_exit.show_image(win)
        task_board.show_image(win)
        get_achievement()
        
        if button_play.check_mouse_cor(mouse_cor):
            button_play.X = button_play.start_x
        else:
            button_play.X = SCREEN_W//1.1
        if button_option.check_mouse_cor(mouse_cor):
            button_option.X = button_option.start_x
        else:
            button_option.X = SCREEN_W//1.1
        if button_exit.check_mouse_cor(mouse_cor):
            button_exit.X = button_exit.start_x
        else:
            button_exit.X = SCREEN_W//1.1
        pygame.display.flip()
  
def book():
    with open(os.path.join(os.path.abspath(__file__ + "/.."),'saves/config.json'),'r') as file:
        config = json.load(file)
    dict_argument["count_animation_book"] += 1
    
    if dict_argument["count_animation_book"] < 45:
        width,height = (image.load(os.path.join(os.path.abspath(__file__ + "/.."),"image/book_"+str(dict_argument["count_animation_book"]//15 + 1)+".png"))).get_rect().size
        element = Graphic_elements(0,0,width*SCREEN_W//500,height*SCREEN_W//500,"image/book_"+str(dict_argument["count_animation_book"]//15 + 1)+".png")
        element.X = (SCREEN_W - element.WIDTH ) //2
        element.Y = (SCREEN_H - element.HEIGHT) //2
        element.show_image(screen)
    else:
        width,height = (image.load(os.path.join(os.path.abspath(__file__ + "/.."),"image/book_4.png"))).get_rect().size
        element = Graphic_elements(0,0,width*SCREEN_W//500,height*SCREEN_W//500,"image/book_4.png")
        element.X = (SCREEN_W - element.WIDTH ) //2
        element.Y = (SCREEN_H - element.HEIGHT) //2
        text_book = Font("font/pixel_font.ttf",SCREEN_W//65,'black',dict_languages_book["1"][config["language"]],element.X + SCREEN_W//30,element.Y + SCREEN_W//30,7)
        text_book_2 = Font("font/pixel_font.ttf",SCREEN_W//65,'black',dict_languages_book["2"][config["language"]],element.X + SCREEN_W//4,element.Y + SCREEN_W//30,7)
        element.show_image(screen)
        text_book.show_text(screen)
        text_book_2.show_text(screen)
        
        
    if dict_argument["count_animation_book"] >= 400:
        dict_argument["flag_book"] = False
        return False
    return True
    
def finish_shooting():
    with open(os.path.join(os.path.abspath(__file__ + "/.."),'saves/config.json'),'r') as file:
        config = json.load(file)
    game = True
    list_music_name[dict_argument["index_music"]].stop_music()
    mouse.set_visible(False)
    Background_finish_shooting = Graphic_elements(-SCREEN_W//2,-SCREEN_H,SCREEN_W*2,SCREEN_H*2,"image/finish_shooting_bg.png")
    Background_finish_shooting.image_load()
    criminal = Graphic_elements(Background_finish_shooting.WIDTH //2 ,Background_finish_shooting.HEIGHT-dict_argument["BLOCK_SIZE"]*6.64,dict_argument["BLOCK_SIZE"]*5,dict_argument["BLOCK_SIZE"]*8.3,"image/criminal/1.png")
    direction_move_criminal = None
    count_move_criminal = 0 
    count_change_direction_criminal = 15
    falg_motion = False
    health_criminal = 2
    gun = Sounds("sounds/gun.wav",int(config["SOUNDS_VOLUME"])/100)
    coin = Sounds("sounds/coins.wav",int(config["SOUNDS_VOLUME"])/100)
    count_gun = 0
    list_music_name[dict_argument["index_music"]].load_music()
    while game:
        if not list_music_name[dict_argument["index_music"]].music_play():
            list_music_name[dict_argument["index_music"]].play_music()
        Background_finish_shooting.show_image(screen)
        mouse_cor = mouse.get_pos()
        
        criminal.X = Background_finish_shooting.X + criminal.start_x
        criminal.Y = Background_finish_shooting.Y + criminal.start_y
        
        criminal.start_y -= dict_argument["criminal_speed"]
        criminal.WIDTH -= SCREEN_W/(1706*1.5)
        criminal.HEIGHT -= SCREEN_H/(578*1.5)
        if criminal.WIDTH > 0 and criminal.HEIGHT > 0:
            criminal.image_load()
        if direction_move_criminal != None and count_move_criminal > 0:
            if direction_move_criminal == "R":
                if criminal.X < Background_finish_shooting.X + Background_finish_shooting.WIDTH - SCREEN_W//1.6:
                    criminal.start_x += SCREEN_W//200
            else:
                if criminal.X > Background_finish_shooting.X + SCREEN_W//1.6:
                    criminal.start_x -= SCREEN_W//200
            count_move_criminal -= 1
        for event1 in event.get(): # Получаем значение события из "списка событий" 
            
            if event1.type == QUIT:
                pygame.quit()
            if event1.type == MOUSEMOTION:
                
                Background_finish_shooting.X += int(event1.rel[0]) * -1
                Background_finish_shooting.Y += int(event1.rel[1]) * -1
                falg_motion = True
                if Background_finish_shooting.X > 0:
                    Background_finish_shooting.X = 0
                if Background_finish_shooting.Y > 0:
                    Background_finish_shooting.Y = 0
                if Background_finish_shooting.X < SCREEN_W - Background_finish_shooting.WIDTH:
                    Background_finish_shooting.X = SCREEN_W - Background_finish_shooting.WIDTH
                if Background_finish_shooting.Y < SCREEN_H - Background_finish_shooting.HEIGHT:
                    Background_finish_shooting.Y = SCREEN_H - Background_finish_shooting.HEIGHT
            if event1.type == MOUSEBUTTONDOWN and event1.button == 1:
                if count_gun == 0:
                    count_gun = 60
                    gun.play_sound()
                    if criminal.check_mouse_cor((SCREEN_W//2,SCREEN_H//2)):
                        coin.play_sound()
                        health_criminal -= 1
                        head_criminal = Graphic_elements(criminal.X,criminal.Y,criminal.WIDTH,criminal.HEIGHT//2,None)
                        if criminal.check_mouse_cor((SCREEN_W//2,SCREEN_H//2)):
                            if not dict_achievement_boling["criminal_hit"]:
                                dict_achievement_boling["criminal_hit"] = True
                                dict_argument["list_flag_achievement"].append("criminal_hit")
                                

                

        if mouse_cor[0]<= SCREEN_W//4 or mouse_cor[0]>= SCREEN_W - SCREEN_W//4 or mouse_cor[1]<= SCREEN_H//4 or mouse_cor[1]>= SCREEN_H - SCREEN_H//4:
            mouse.set_pos([SCREEN_W//2,SCREEN_H//2])
        if not falg_motion:
            mouse.set_pos([SCREEN_W//2,SCREEN_H//2])
        if count_gun > 0 :
            count_gun -= 1
        if count_change_direction_criminal >= 20:

            count_change_direction_criminal = 0 
            direction_move_criminal = random.choice(["R","R","R","L","L","L",None])
            count_move_criminal = 60 
            
        if criminal.Y < Background_finish_shooting.Y + SCREEN_H//1.5:

            mouse.set_visible(True)
            return False
        if health_criminal <= 0:

            mouse.set_visible(True)
            return True
        criminal.show_image(screen)
        aim.show_image(screen)
        clock.tick(FPS*2)
        display.update() #Обновление экрана
        count_change_direction_criminal += 1

def safe():
    dict_argument["sprite_x"] = sprite1.image_sprite.X//dict_argument["BLOCK_SIZE"]
    dict_argument["sprite_y"] = sprite1.image_sprite.Y//dict_argument["BLOCK_SIZE"]
    with open(os.path.join(os.path.abspath(__file__ + "/.."),'saves/saves.json'),'w') as file:
        json.dump(dict_argument,file,indent=4,ensure_ascii=True)
    with open(os.path.join(os.path.abspath(__file__ + "/.."),'saves/config.json'),'r') as file:
        config = json.load(file)
    bk = Graphic_elements(0,0,SCREEN_W,SCREEN_H,"image/room_1.png")
    rect = Rect(SCREEN_W//6.71,SCREEN_H//5,SCREEN_W//8.28,SCREEN_H//6)
    bg_safe = Graphic_elements(SCREEN_W//6,SCREEN_H//6,SCREEN_W//1.5,SCREEN_H//1.5,"image/safe/bg.png")
    big_part_minigame_safe = Graphic_elements(bg_safe.X + bg_safe.WIDTH//2 - SCREEN_W//12,bg_safe.Y + bg_safe.HEIGHT//2 - SCREEN_W//12,SCREEN_W//6,SCREEN_W//6,"image/safe/big_part_minigame_safe.png")
    smalle_part_minigame_safe = Graphic_elements(bg_safe.X + bg_safe.WIDTH//2 - SCREEN_W//12,bg_safe.Y + bg_safe.HEIGHT//2 - SCREEN_W//12,SCREEN_W//6,SCREEN_W//6,"image/safe/smalle_part_minigame_safe.png")
    red_zone_safe_minigame = Graphic_elements(bg_safe.X + bg_safe.WIDTH//2 - SCREEN_W//4,bg_safe.Y + bg_safe.HEIGHT//2,SCREEN_W//2,SCREEN_W//20,"image/safe/red_zone_safe_minigame.png")
    green_zone_safe_minigame = Graphic_elements(random.randint(red_zone_safe_minigame.X + SCREEN_W//100,red_zone_safe_minigame.X + red_zone_safe_minigame.WIDTH - SCREEN_W//20 - SCREEN_W//100),red_zone_safe_minigame.Y,red_zone_safe_minigame.HEIGHT,red_zone_safe_minigame.HEIGHT,"image/safe/green_zone_safe_minigame.png")
    arrow_safe_minigame = Graphic_elements(red_zone_safe_minigame.X + SCREEN_W//100,red_zone_safe_minigame.Y + red_zone_safe_minigame.HEIGHT - green_zone_safe_minigame.HEIGHT//2.5,green_zone_safe_minigame.HEIGHT//2.5,green_zone_safe_minigame.HEIGHT//2.5,"image/safe/arrow_safe_minigame.png")
    direction_arrow_safe_minigame = "R"
    direction_green_zone_safe_minigame = "R"
    flag_safe = False
    number_completed_lvl_safe = 0
    
    comleted_safe = 0 
    list_red_led = []
    for i in range(5):
        list_red_led.append(Graphic_elements(bg_safe.X + bg_safe.WIDTH - SCREEN_W//30,bg_safe.Y + SCREEN_W//30 * (i+1),SCREEN_W//50,SCREEN_W//50,"image/safe/red_led_off.png"))
    angle_safe = 0
    list_angle_safe = [random.randint(1,359),random.randint(1,359),random.randint(1,359)]
    for i in list_angle_safe:
        if i % 2:
            list_angle_safe[list_angle_safe.index(i)] += 1
    text_presed_f = Font("font/pixel_font.ttf",SCREEN_W//40,"black",dict_laungues_safe[config["language"]][0],big_part_minigame_safe.X - SCREEN_W//20,big_part_minigame_safe.Y + SCREEN_W//5)
    run = True
    presed_f_last = False
    open_safe = Graphic_elements(bg_safe.X + bg_safe.WIDTH//3,bg_safe.Y + bg_safe.HEIGHT//3,bg_safe.WIDTH//3,bg_safe.WIDTH//3//1.5,"image/safe/open_safe_book.png")
    time_count = 0
    text_time = Font("font/pixel_font.ttf",SCREEN_W//40,"red",str(dict_argument["speed_safe"]),bg_safe.X + SCREEN_W//30,bg_safe.Y + SCREEN_W//30)
    with open(os.path.join(os.path.abspath(__file__ + "/.."),'saves/config.json'),'r') as file:
            config = json.load(file)
    list_keys = config["keys"]
    list_music_name[dict_argument["index_music"]].stop_music()
    list_music_name[dict_argument["index_music"]].load_music()
    while run:
        if not list_music_name[dict_argument["index_music"]].music_play():
            list_music_name[dict_argument["index_music"]].play_music()
        screen.fill("blue")
        move_cloud()
        bk.show_image(screen)
        clock.tick(30)
        if flag_safe:
            

            bg_safe.show_image(screen)
            text_time.show_text(screen)
            for red_led in list_red_led:
                red_led.show_image(screen)
            keys = key.get_pressed()  

            if comleted_safe > 1:
                comleted_safe -=1
                open_safe.show_image(screen)
            
            if comleted_safe == 1:
                flag_safe = False
                dict_argument["flag_book"] = True
                if dict_argument["speed_safe"] - int(text_time.font_content[0]) <= 25:
                    if not dict_achievement_boling["cracker"]:
                        dict_achievement_boling["cracker"] = True
                        dict_argument["list_flag_achievement"].append("cracker")
                        

            if comleted_safe == 0:
                time_count += 1
                if int(text_time.font_content[0]) <= 0:
                    text_time.font_content = [str(dict_argument["speed_safe"])]
                    if dict_argument["complexity"] == "easy":
                        if not dict_achievement_boling["piferer"]:
                            dict_achievement_boling["piferer"] = True
                            dict_argument["list_flag_achievement"].append("piferer")
                            
                    number_completed_lvl_safe = 0
                    for i in list_red_led:
                        i.path = "image/safe/red_led_off.png"
                        i.image_load()
                if time_count == 30:
                    time_count = 0
                    text_time.font_content = [str(int(text_time.font_content[0]) - 1)]
                if number_completed_lvl_safe <= 2:
                    text_presed_f.font_content = [dict_laungues_safe[config["language"]][0]]
                    if keys[list_keys[4]]:  
                        angle_safe +=2
                    if keys[list_keys[3]]:
                        angle_safe -=2
                    big_part_minigame_safe.show_image(screen)
                    smalle_part_minigame_safe.image_load()
                    smalle_part_minigame_safe_copy = transform.rotate(smalle_part_minigame_safe.IMG, angle_safe*-1) 
                    screen.blit(smalle_part_minigame_safe_copy, (smalle_part_minigame_safe.X + smalle_part_minigame_safe.WIDTH//2 - int(smalle_part_minigame_safe_copy.get_width() / 2), smalle_part_minigame_safe.Y + smalle_part_minigame_safe.HEIGHT//2 - int(smalle_part_minigame_safe_copy.get_height() / 2)))
                    

                    if angle_safe > 360:
                        angle_safe -= 360
                    elif angle_safe < 0:
                        angle_safe += 360

                        
                    if angle_safe == list_angle_safe[number_completed_lvl_safe]:
                        list_red_led[number_completed_lvl_safe].path = "image/safe/red_led_on.png"
                        list_red_led[number_completed_lvl_safe].image_load()
                        text_presed_f.show_text(screen)
                        if keys[list_keys[0]] and not presed_f_last:
                            use_sound.play_sound()
                            presed_f_last = True
                            number_completed_lvl_safe += 1
                            angle_safe = 0
                        if not keys[list_keys[0]]:
                            presed_f_last = False
                        
                        
                    else:
                        list_red_led[number_completed_lvl_safe].path = "image/safe/red_led_off.png"
                        list_red_led[number_completed_lvl_safe].image_load()
            
                else:
                    
                    if direction_arrow_safe_minigame == "R":
                        arrow_safe_minigame.X += SCREEN_W//70
                    elif direction_arrow_safe_minigame == "L":    
                        arrow_safe_minigame.X -= SCREEN_W//70
                    if arrow_safe_minigame.X >= red_zone_safe_minigame.X + red_zone_safe_minigame.WIDTH - SCREEN_W//20 - SCREEN_W//100:
                        direction_arrow_safe_minigame = "L"
                    elif arrow_safe_minigame.X <= red_zone_safe_minigame.X + SCREEN_W//100:
                        direction_arrow_safe_minigame = "R"
                    if number_completed_lvl_safe == 4:
                        if direction_green_zone_safe_minigame == "R":
                            green_zone_safe_minigame.X += SCREEN_W//140
                        elif direction_green_zone_safe_minigame == "L":    
                            green_zone_safe_minigame.X -= SCREEN_W//140
                        if green_zone_safe_minigame.X >= red_zone_safe_minigame.X + red_zone_safe_minigame.WIDTH - SCREEN_W//20 - SCREEN_W//100:
                            direction_green_zone_safe_minigame = "L"
                        elif green_zone_safe_minigame.X <= red_zone_safe_minigame.X + SCREEN_W//100:
                            direction_green_zone_safe_minigame = "R"
                    if keys[list_keys[0]] and presed_f_last == False:
                        use_sound.play_sound()
                        presed_f_last = True
                        if Rect.colliderect(arrow_safe_minigame.RECT,green_zone_safe_minigame.RECT):
                            list_red_led[number_completed_lvl_safe].path = "image/safe/red_led_on.png"
                            list_red_led[number_completed_lvl_safe].image_load()
                            if number_completed_lvl_safe == 4: 
                                comleted_safe = 100
                            else:
                                green_zone_safe_minigame.X = random.randint(red_zone_safe_minigame.X + SCREEN_W//100,red_zone_safe_minigame.X + red_zone_safe_minigame.WIDTH - SCREEN_W//20 - SCREEN_W//100)
                                number_completed_lvl_safe += 1

                        else:
                            text_time.font_content = [str(dict_argument["speed_safe"])]
                            if dict_argument["complexity"] == "easy":
                                if not dict_achievement_boling["piferer"]:
                                    dict_achievement_boling["piferer"] = True
                                    dict_argument["list_flag_achievement"].append("piferer")
                                     
                            number_completed_lvl_safe = 0
                            for i in list_red_led:
                                i.path = "image/safe/red_led_off.png"
                                i.image_load()
                    if not keys[list_keys[0]]:
                        presed_f_last = False
                    text_presed_f.font_content = dict_laungues_safe[config["language"]]
                    red_zone_safe_minigame.show_image(screen)
                    green_zone_safe_minigame.show_image(screen)
                    arrow_safe_minigame.show_image(screen)
                    text_presed_f.show_text(screen)

        if dict_argument["flag_book"]:
            if not book():
                dict_spawn_and_finish_point["lvl2_location_2"][1][0] = Rect(0,0,0,0)
                dict_argument["list_flag_room"][0] = True
                run = False
        for event1 in event.get():
            if event1.type == MOUSEBUTTONDOWN:
                if Rect.collidepoint(rect,mouse.get_pos()[0],mouse.get_pos()[1]):
                    flag_safe = True
            if event1.type == QUIT:
                quit()
                                    
        display.update()

def flappy_bird():
    list_music_name[dict_argument["index_music"]].stop_music()
    flappy_bird = Graphic_elements(SCREEN_W//2-SCREEN_W//40,SCREEN_H//2,SCREEN_W//20,SCREEN_W//20//1.41,"image/flappy_bird/bird_1.png")
    border = Graphic_elements(0,0,SCREEN_W,SCREEN_H,"image/flappy_bird/border.png")
    index_img_bird = 1
    count_change_img_bird = 3
    count_append_pipe = -30
    count_up_bird = 0
    list_pipe = []
    run = True
    number_point = 0
    run_move_bird = False
    direction_not_run_move_bird = "D"
    change_not_run_move_bird = 5
    angle = 0
    flappy_bird.image_load()
    text_record = Font("font/pixel_font.ttf",SCREEN_W//30,"yellow",str(dict_argument["record_flappy_bird"]),SCREEN_W//2,SCREEN_H//6)
    text = Font("font/pixel_font.ttf",SCREEN_W//30,"black",str(number_point),SCREEN_W//2,SCREEN_H//4)
    list_music_name[dict_argument["index_music"]].load_music()
    while run:
        if number_point > int(text_record.font_content[0]):
            text_record.font_content[0] = str(number_point)
        if not list_music_name[dict_argument["index_music"]].music_play():
            list_music_name[dict_argument["index_music"]].play_music()
        
        screen.fill("blue")
        if run_move_bird:
            count_append_pipe += 1
            if count_append_pipe >= 50:
                count_append_pipe = random.randint(0,10)
                list = [
                    Graphic_elements(SCREEN_W,0,SCREEN_H//7,SCREEN_H,"image/flappy_bird/pipe.png"),
                    Graphic_elements(SCREEN_W,0,SCREEN_H//7,SCREEN_H,"image/flappy_bird/pipe.png")
                ]
                random_number = random.randint(SCREEN_H//3,SCREEN_H-SCREEN_H//6)
                list[-1].Y = random_number
                list[-1].image_load(rotate_y = True)
                list[0].Y = list[-1].Y - flappy_bird.HEIGHT * 4.5 - list[0].HEIGHT
                list_pipe.append(list)
            for l in list_pipe:
                for obj in l:
                    obj.X -= SCREEN_W // 100
                    obj.show_image(screen)  
                    if obj.X < flappy_bird.X and l.index(obj) == 0 and obj.NAME != False:
                        number_point += 1
                        obj.NAME = False
                        text.font_content = [str(number_point)]
                    if obj.X - obj.WIDTH < 0 :
                        list_pipe.pop(list_pipe.index(l))
                        break
                    if Rect.colliderect(obj.RECT,flappy_bird.RECT):
                        if dict_argument["record_flappy_bird"] < number_point:
                            dict_argument["record_flappy_bird"] = number_point
                        return number_point
                        
        for event1 in event.get():
            if event1.type == MOUSEBUTTONDOWN:
                use_sound.play_sound()
                run_move_bird = True
                count_up_bird = 10
                angle = 0
            if event1.type == QUIT:
                quit()
        flappy_bird.show_image(screen)
        count_change_img_bird -= 1
        if count_change_img_bird <= 0:
            count_change_img_bird = 3
            index_img_bird += 1
            if index_img_bird >= 4:
                index_img_bird = 1
            flappy_bird.path = "image/flappy_bird/bird_"+str(index_img_bird)+".png"
            flappy_bird.image_load()

                
        
        if count_up_bird > 0 and not flappy_bird.Y < 0 :
            flappy_bird.Y -= SCREEN_W // 120
            count_up_bird -= 1
            angle += 5
            flappy_bird.image_load()
            flappy_bird.IMG = transform.rotate(flappy_bird.IMG,angle)
        else:
            count_up_bird = 0
            
        
        if run_move_bird:
            if count_up_bird <= 0:
                flappy_bird.Y += SCREEN_W // 80
                if angle >= -70:
                    angle -= 10
                flappy_bird.image_load()
                flappy_bird.IMG = transform.rotate(flappy_bird.IMG,angle)
        else:

            if direction_not_run_move_bird == "U":
                if change_not_run_move_bird <= 0:
                    change_not_run_move_bird = 6
                    direction_not_run_move_bird = "D"
                flappy_bird.Y -= SCREEN_W // 700
            elif direction_not_run_move_bird == "D":
                if change_not_run_move_bird <= 0:
                    change_not_run_move_bird = 6
                    direction_not_run_move_bird = "U"
                flappy_bird.Y += SCREEN_W // 700
        change_not_run_move_bird -= 1
        
        if flappy_bird.Y+ flappy_bird.HEIGHT > SCREEN_H:
            if dict_argument["record_flappy_bird"] < number_point:
                dict_argument["record_flappy_bird"] = number_point

            list_music_name[dict_argument["index_music"]].stop_music()
            return number_point
        text.show_text(screen)
        text_record.show_text(screen)
        clock.tick(30)
        border.show_image(screen)
        display.update()

def save_game(): 
    dict_argument["sprite_x"] = sprite1.image_sprite.X/dict_argument["BLOCK_SIZE"]
    dict_argument["sprite_y"] = sprite1.image_sprite.Y/dict_argument["BLOCK_SIZE"]
    with open(os.path.join(os.path.abspath(__file__ + "/.."),'saves/saves.json'),'w') as file:
        json.dump(dict_argument,file,indent=4,ensure_ascii=True)
    with open(os.path.join(os.path.abspath(__file__ + "/.."),'saves/achievement.json'),'w') as file:
        json.dump(dict_achievement_boling,file,indent=4,ensure_ascii=True)


def get_achievement():
    if len(dict_argument["list_flag_achievement"]) > 0:
        if achievement_img.path == None:
            achievement_img.path = "image/achivement/"+dict_argument["list_flag_achievement"][0]+"_rgb.png"
    if achievement_img.path != None:
        if achievement_img.X > SCREEN_W//2:
            achievement_img.X -= SCREEN_W//70
            achievement_img.Y -= SCREEN_H//70
            if achievement_img.path != "image/plate.png":
                achievement_img.path = "image/achivement/"+dict_argument["list_flag_achievement"][0]+"_rgb.png"
            achievement_img.image_load()
            achievement_img.NAME = str(int(achievement_img.NAME) + 20)
            achievement_img_copy = transform.rotate(achievement_img.IMG,int(achievement_img.NAME))
            screen.blit(achievement_img_copy, (achievement_img.X - int(achievement_img_copy.get_width() / 2), achievement_img.Y - int(achievement_img_copy.get_height() / 2)))
        elif achievement_img.WIDTH < SCREEN_W//5:
            achievement_img.X = SCREEN_W//2 - achievement_img.WIDTH//2
            achievement_img.Y = SCREEN_H//2 - achievement_img.HEIGHT//2
            achievement_img.WIDTH += SCREEN_W//80
            achievement_img.HEIGHT += SCREEN_W//80
            achievement_img.image_load()
            achievement_img.show_image(screen)
            achievement_img.NAME = "400"
        elif int(achievement_img.NAME) > 0:
            achievement_img.NAME = str(int(achievement_img.NAME) - 5)
            achievement_img.IMG.set_alpha(int(achievement_img.NAME))
            achievement_img.show_image(screen)
        else:
            if achievement_img.path != "image/plate.png":
                dict_argument["list_flag_achievement"].pop(0)
            achievement_img.X = SCREEN_W
            achievement_img.Y = SCREEN_H
            achievement_img.WIDTH = achievement_img.start_width
            achievement_img.HEIGHT = achievement_img.start_height
            achievement_img.path = None
        
