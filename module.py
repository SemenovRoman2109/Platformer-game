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
                    list_NPC.append(Graphic_elements(X,Y-dict_argument["BLOCK_SIZE"]*1.66+dict_argument["BLOCK_SIZE"],dict_argument["BLOCK_SIZE"],dict_argument["BLOCK_SIZE"]*1.66,"image/Персонажи/Person/person_"+str(random.randint(1,13))+".png"))
                    list_index_NPC.append([i,j])
                    if dict_argument["list_surface"][i][j] == "У":
                        list_NPC[-1].path = "image/Персонажи/Преступник/model.png"
                    
                    if len(list_NPC) > 1:
                        stop = True
                        while stop:
                            for obj in list_NPC:
                                if obj != list_NPC[-1]:
                                    if obj.path == list_NPC[-1].path:
                                        stop = True
                                        list_NPC[-1].path = "image/Персонажи/Person/person_"+str(random.randint(1,13))+".png"
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
                        dict_list_border["list_flag"][i][j].append(20)
                        dict_list_border["list_flag"][i][j].append(40)
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
                dict_list_border["list_border_cor_cracking"][dict_list_border["list_border_cor_cracking"].index(i)][7] = 40
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
                    dict_list_border["list_border_cor_cracking"][dict_list_border["list_border_cor_cracking"].index(i)][6] = 20
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
    
    if keys[K_f]:
        if dict_argument_block["count_load"] == 24: 
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
    
        if dict_argument_block["count_load"] == 12 and dict_argument_block["flag_load"] == 1:
                
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
        dict_argument_block["count_spike"] = 150
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
            
        text_transition_new_lvl.font_y = SCREEN_H//2-text_transition_new_lvl.font_size
        if dict_argument["screen_dimming_flag"] == "+":
            dict_argument["screen_dimming_count"] += 3
            if dict_argument["screen_dimming_count"] == 300:
                dict_argument["screen_dimming_flag"] = "-"
                if dict_argument["index_text_drimming"] in ["lose_game","win_game"]:
                    dict_argument["game"] = False
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
            move_cloud()

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
            move_cloud()

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

    ammo_img = Graphic_elements(SCREEN_W//100,SCREEN_W//100,dict_argument["BLOCK_SIZE"],dict_argument["BLOCK_SIZE"]//1.14,"image/ammo.png")
    
    left_side_stand_for_manniquens = Graphic_elements(0,0,dict_argument["BLOCK_SIZE"],dict_argument["BLOCK_SIZE"]*2.269,"image/left_side_stand_for_mannequins.png")
    right_side_stand_for_manniquens = Graphic_elements(0,0,dict_argument["BLOCK_SIZE"],dict_argument["BLOCK_SIZE"]*2.269,"image/right_side_stand_for_mannequins.png")
    middle_stand_for_manniquens = Graphic_elements(0,0,0,right_side_stand_for_manniquens.HEIGHT//9.83,"image/middle_stand_stand_for_mannequins.png")
    
    list_down_stand_for_manniquens = [left_side_stand_for_manniquens,right_side_stand_for_manniquens,middle_stand_for_manniquens,[[Graphic_elements(None,0,SCREEN_W//10,SCREEN_W//10*1.693,None),"right",[]],[Graphic_elements(None,0,SCREEN_W//10,SCREEN_W//10*1.693,None),"right",[]]],[]]                 
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
    

    count_gun = 0
    gun = Sounds("sounds/gun.wav",100)
    coin = Sounds("sounds/coins.wav",100)
    statstic = Font("font/pixel_font.ttf",SCREEN_W//30,"black",str(count_point) +"/" + str(min_count_point),SCREEN_W-SCREEN_W//7,0,1,True)
    ammo_statistic = Font('font/pixel_font.ttf',SCREEN_W//30,"black",str(ammo_count),0 + SCREEN_W//15,SCREEN_W//100,1,True)
    while game:
        screen.fill("black")
        Background_shooting.show_image(screen)
        
        falg_motion = False  
        
        list_y_stand = [Background_shooting.Y + Background_shooting.HEIGHT - SCREEN_H//1.5,Background_shooting.Y + Background_shooting.HEIGHT//2,Background_shooting.Y + SCREEN_H//1.5] 
        for obj in range(len(list_stand)):
            list_s = list_stand[obj]
            list_s[0].X = Background_shooting.X + SCREEN_W//2
            list_s[1].X = Background_shooting.X + Background_shooting.WIDTH - SCREEN_W//2 - list_s[1].WIDTH
            list_s[2].X = list_s[0].X + list_s[0].WIDTH 
            
            list_s[2].WIDTH = -1 * ((list_s[0].X + list_s[0].WIDTH) - list_s[1].X)
            list_s[2].image_load()

            
            
            list_s[0].Y = list_y_stand[obj]
            list_s[1].Y = list_s[0].Y
            list_s[2].Y = list_s[0].Y

            if barriers != False:
                if obj_barier_position_flag:
                    for obj_barier in list_s[-1]:
                        obj_barier.start_x = random.randint(0,int(list_s[2].WIDTH - obj_barier.WIDTH))
                        
                    if len(list_s[-1]) > 1:
                        for obj_barier in list_s[-1]:
                            
                            obj_barier_another_flag = True
                            # print("Входит в цикл вайл")
                            while obj_barier_another_flag:
                                # print("Входит в цикл фор")
                                for obj_barier_another in list_s[-1]:
                                    if list_s[-1].index(obj_barier_another) != list_s[-1].index(obj_barier):
                                        # print("зашло в цикл с индексом ",list_s[-1].index(obj_barier_another))
                                        if obj_barier.start_x <= obj_barier_another.start_x and obj_barier.start_x >= obj_barier_another.start_x - obj_barier_another.WIDTH *1.5:
                                            obj_barier.start_x = random.randint(0,int(list_s[2].WIDTH - obj_barier.WIDTH)) 
                                            obj_barier_another_flag = True
                                            # print("Меняем")
                                            break
                                        elif obj_barier.start_x >= obj_barier_another.start_x and obj_barier.start_x <= obj_barier_another.start_x - obj_barier_another.WIDTH *1.5:
                                            obj_barier.start_x = random.randint(0,int(list_s[2].WIDTH - obj_barier.WIDTH))
                                            obj_barier_another_flag = True
                                            # print("Меняем")
                                            break
                                        else:
                                            # print(" НЕ Меняем")
                                            obj_barier_another_flag = False
                    
                        
                    
                

            
            for i in list_s[-2]:
                list_barier_obj = list_s[-1]
                object = i[0]
                direction = i[1]
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
                    i[2].append(Rect(object.X+object.WIDTH//2.578,object.Y+object.HEIGHT//16.6,object.WIDTH//3.769,object.WIDTH//3.769)) #Белая зона головы
                    i[2].append(Rect(object.X+object.WIDTH//2.13,object.Y+object.HEIGHT//9.22,object.WIDTH//9.8,object.WIDTH//9.8)) #Красная зона головы
                    i[2].append(Rect(object.X+object.WIDTH//9.8,object.Y+object.HEIGHT//2.184,object.WIDTH//1.195,object.WIDTH//1.195)) #Белая зона живота
                    i[2].append(Rect(object.X+object.WIDTH//2.33,object.Y+object.HEIGHT//1.53,object.WIDTH//5.44,object.WIDTH//5.44)) #Красная зона живота
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
                
                for obj_barier in list_barier_obj:
                    obj_barier.X = list_s[2].X + obj_barier.start_x
                object.X = list_s[2].X + object.start_x
                i[2][0] = Rect(object.X+object.WIDTH//2.578,object.Y+object.HEIGHT//16.6,object.WIDTH//3.769,object.WIDTH//3.769) #Белая зона головы
                i[2][1] = Rect(object.X+object.WIDTH//2.13,object.Y+object.HEIGHT//9.22,object.WIDTH//9.8,object.WIDTH//9.8) #Красная зона головы
                i[2][2] = Rect(object.X+object.WIDTH//9.8,object.Y+object.HEIGHT//2.184,object.WIDTH//1.195,object.WIDTH//1.195) #Белая зона живота
                i[2][3] = Rect(object.X+object.WIDTH//2.33,object.Y+object.HEIGHT//1.53,object.WIDTH//5.44,object.WIDTH//5.44) #Красная зона живота
            
            for i in list_s:
                if type(i) != type([]):
                    i.show_image(screen)
                
            for object in list_s[-2]:
                object[0].show_image(screen)

            for object in list_s[-1]:
                object.show_image(screen)
            
        obj_barier_position_flag = False
        
        mouse_cor = mouse.get_pos()
        for event1 in event.get(): # Получаем значение события из "списка событий" 
            
            if event1.type == QUIT:
                game = False
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
                                    break
                                
                            for obj in l_s[-2]:
                                if not flag_barier:
                                    if obj[0].check_mouse_cor((SCREEN_W//2,SCREEN_H//2)):
                                        factor_zone = 1
                                        for i in obj[2]:
                                            if obj[2].index(i) % 2:
                                                if SCREEN_W//2 > i.x and SCREEN_W//2 < i.x + i.width and SCREEN_H//2 > i.y and SCREEN_H//2 < i.y + i.height:
                                                    factor_zone = 3
                                                    break
                                            else:
                                                if SCREEN_W//2 > i.x and SCREEN_W//2 < i.x + i.width and SCREEN_H//2 > i.y and SCREEN_H//2 < i.y + i.height:
                                                    factor_zone = 2
                                        coin.play_sound()
                                        count_point += factor_zone * int(obj[0].NAME//(SCREEN_W//400))
                                        statstic.font_content = [str(count_point) +"/" + str(min_count_point)]
                                        print("Ты попал! На тебе", factor_zone * int(obj[0].NAME//(SCREEN_W//400)), "монет!")
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
        if ammo_count <= 0:
            mouse.set_visible(True)
            return count_point
        display.update()
    mouse.set_visible(True)


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
    win = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    def option():
        bg_option = Graphic_elements(0, 0, SCREEN_W, SCREEN_H, 'image/menu/option_not.png')
        flag_option = "not"
        sound_power = Font("font/pixel_font.ttf",SCREEN_W//30,"black","Громкость звука 50",SCREEN_W//3.2,SCREEN_H//8,bold=False)
        music_power = Font("font/pixel_font.ttf",SCREEN_W//30,"black","Громкость музики 50",SCREEN_W//3.2,SCREEN_H//3,bold=False)
        flag_mouse_volume_sound = False
        rect_volume_sound = pygame.Rect(SCREEN_W//3.2,SCREEN_H//4.5,SCREEN_W//1.6,SCREEN_H//25)
        mouse_volume_sound = pygame.Rect(50*rect_volume_sound.width/100+rect_volume_sound.x,rect_volume_sound.top-(SCREEN_H//45*3-rect_volume_sound.height)//2,SCREEN_H//72*2,SCREEN_H//45*3)
        flag_mouse_volume_music = False
        rect_volume_music = pygame.Rect(SCREEN_W//3.2,SCREEN_H//2.3,SCREEN_W//1.6,SCREEN_H//25)
        mouse_volume_music = pygame.Rect(50*rect_volume_music.width/100+rect_volume_music.x,rect_volume_music.top-(SCREEN_H//45*3-rect_volume_music.height)//2,SCREEN_H//72*2,SCREEN_H//45*3)
        
        
        button_display_size = Font("font/pixel_font.ttf",SCREEN_W//20,'black','Разрешение:',SCREEN_W//3.2,SCREEN_H//8)
        list_buttons_display_size =[
                        Font("font/pixel_font.ttf",SCREEN_W//38,'black','1280x720',button_display_size.font_x,button_display_size.font_y+SCREEN_H//8),
                        Font("font/pixel_font.ttf",SCREEN_W//38,'black','1600x920',button_display_size.font_x+SCREEN_W//14.2*2,button_display_size.font_y+SCREEN_H//8),
                        Font("font/pixel_font.ttf",SCREEN_W//38,'black','1920x1080',button_display_size.font_x+SCREEN_W//14.2*4,button_display_size.font_y+SCREEN_H//8),
        ]

        for obj in list_buttons_display_size:
            width = SCREEN_W
            height = SCREEN_H
            obj_width = obj.font_content[0].split('x')[0]
            obj_height = obj.font_content[0].split('x')[1]
            if (int(obj_width) == width and int(obj_height) == height):
                obj.font_color = 'red'
                break

        button_display_fullsize = Font("font/pixel_font.ttf",SCREEN_W//25,'black','Полноэкранный режим:',SCREEN_W//3.2,SCREEN_H//3)
        list_button_display_fullsize = [
            Font("font/pixel_font.ttf",SCREEN_W//25,'black','Да',SCREEN_W//3.2*1.5,button_display_fullsize.font_y + SCREEN_H//8),
            Font("font/pixel_font.ttf",SCREEN_W//25,'black','Нет',SCREEN_W//3.2*1.2,button_display_fullsize.font_y + SCREEN_H//8)
        ]

        if FULLSCREEN:
            list_button_display_fullsize[0].font_color = 'red'
        else:
            list_button_display_fullsize[1].font_color = 'red'
        run_option = True
        while run_option: 
            for event in pygame.event.get():
                #Услове выхода из игры
                mouse_cor = pygame.mouse.get_pos() 
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    obj_button_option = pygame.Rect(0, 0, SCREEN_W//3.8, SCREEN_H) 
                    obj_video = pygame.Rect(SCREEN_W//67.3, SCREEN_H//10.3, SCREEN_W//4.3, SCREEN_H//12.2)
                    obj_back = pygame.Rect(SCREEN_W//91.4, SCREEN_H//130, SCREEN_W//10.24, SCREEN_H//20.571)
                    obj_audio = pygame.Rect(SCREEN_W//67.3, SCREEN_H//5.15, SCREEN_W//4.3, SCREEN_H//12.2)
                    if obj_button_option.collidepoint(mouse_cor[0],mouse_cor[1]):
                        if obj_back.collidepoint(mouse_cor[0],mouse_cor[1]):
                            #СДЕСЬ СОХРАНЯЕМ ДАННЫЕ
                            settings = {
                                "FULLSCREEN":list_button_display_fullsize[0].font_color == "red"
                            }
                            #
                            run_option = False
                        elif obj_video.collidepoint(mouse_cor[0],mouse_cor[1]):
                            flag_option = "video"
                        elif obj_audio.collidepoint(mouse_cor[0],mouse_cor[1]):
                            flag_option = "audio"
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
                                if i.font_content[0] == "Да":
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
            
            bg_option.path = 'image/menu/option_'+flag_option+'.png'
            bg_option.image_load()
            bg_option.show_image(win)
            
            if flag_option == "not":
                help_text = Font("font/pixel_font.ttf",SCREEN_W//30,"black","Выберите категорию ;в которой хотите внести изменение;;Изменения вступят в игру;после нажатия кнопки назад",SCREEN_W//3.2,SCREEN_H//8,bold=False,index=5)
                help_text.show_text(win)
            if flag_option == "video":
                button_display_size.show_text(win)
                for i in list_buttons_display_size:
                    i.show_text(win)
                button_display_fullsize.show_text(win)
                for i in list_button_display_fullsize:
                    i.show_text(win)
            if flag_option == "audio":
                
                slider(sound_power, flag_mouse_volume_sound, rect_volume_sound, mouse_volume_sound, mouse_cor, "Громкость звука ",win)
                slider(music_power, flag_mouse_volume_music, rect_volume_music, mouse_volume_music, mouse_cor, "Громкость музики ",win)
            pygame.display.flip()

  
    bg = Graphic_elements(0, 0, SCREEN_W, SCREEN_H, 'image/menu/bg.png')
    
    name_menu = Graphic_elements(SCREEN_W//20,SCREEN_H//40, SCREEN_W//1.7, SCREEN_H//7, 'image/menu/name.png')
    button_play = Graphic_elements(SCREEN_W//1.395,SCREEN_H//6.1, SCREEN_W//3.5, SCREEN_H//7.8, 'image/menu/button_play.png')
    button_option = Graphic_elements(SCREEN_W//1.395,SCREEN_H//2 - SCREEN_H//15.6, SCREEN_W//3.5, SCREEN_H//7.8, 'image/menu/button_option.png')
    button_exit = Graphic_elements(SCREEN_W//1.395,SCREEN_H//1.4, SCREEN_W//3.5, SCREEN_H//7.8, 'image/menu/button_exit.png')
    run = True
    
    while run: 
        for event in pygame.event.get():
            #Услове выхода из игры
            mouse_cor = pygame.mouse.get_pos() 

            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_exit.check_mouse_cor(mouse_cor):
                    run = False
                if button_option.check_mouse_cor(mouse_cor):
                    option()
                if button_play.check_mouse_cor(mouse_cor):
                    run_game()
                    
                    
                
                            
                        


            
        bg.show_image(win)    
        name_menu.show_image(win)
        button_play.show_image(win)
        button_option.show_image(win)
        button_exit.show_image(win)
        
        
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
        text_book = Font("font/pixel_font.ttf",SCREEN_W//65,'black',"Сьогодні я зроблю;;свою останню справу;;після якої я влечу;;до себе на батьківщину;;Нарешті я побачу;;свою дочку;;у неї через 3 міцяться;;день народженя. ",element.X + SCREEN_W//30,element.Y + SCREEN_W//30,7)
        text_book_2 = Font("font/pixel_font.ttf",SCREEN_W//65,'black',"Вона напевно скучила;;за мною.",element.X + SCREEN_W//4,element.Y + SCREEN_W//30,7)
        element.show_image(screen)
        text_book.show_text(screen)
        text_book_2.show_text(screen)
        
        
    if dict_argument["count_animation_book"] >= 400:
        dict_argument["flag_book"] = False
        return False
    return True
    
def finish_shooting():
    game = True
    mouse.set_visible(False)
    criminal = Graphic_elements(Background_shooting.WIDTH //2 ,Background_shooting.HEIGHT-dict_argument["BLOCK_SIZE"]*6.64,dict_argument["BLOCK_SIZE"]*5,dict_argument["BLOCK_SIZE"]*8.3,"image/Персонажи/Преступник/1.png")
    direction_move_criminal = None
    count_move_criminal = 0 
    count_change_direction_criminal = 15
    falg_motion = False
    health_criminal = 2
    gun = Sounds("sounds/gun.wav",100)
    coin = Sounds("sounds/coins.wav",100)
    count_gun = 0
    while game:
        Background_shooting.show_image(screen)
        mouse_cor = mouse.get_pos()
        
        criminal.X = Background_shooting.X + criminal.start_x
        criminal.Y = Background_shooting.Y + criminal.start_y
        
        criminal.start_y -= SCREEN_W//250
        criminal.WIDTH -= SCREEN_W/(1706*1.5)
        criminal.HEIGHT -= SCREEN_H/(578*1.5)
        if criminal.WIDTH > 0 and criminal.HEIGHT > 0:
            criminal.image_load()
        if direction_move_criminal != None and count_move_criminal > 0:
            if direction_move_criminal == "R":
                criminal.start_x += SCREEN_W//200
            else:
                criminal.start_x -= SCREEN_W//200
            count_move_criminal -= 1
        for event1 in event.get(): # Получаем значение события из "списка событий" 
            
            if event1.type == QUIT:
                game = False
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
            if event1.type == MOUSEBUTTONDOWN and event1.button == 1:
                if count_gun == 0:
                    count_gun = 60
                    gun.play_sound()
                    if criminal.check_mouse_cor((SCREEN_W//2,SCREEN_H//2)):
                        coin.play_sound()
                        health_criminal -= 1
                

        if mouse_cor[0]<= SCREEN_W//4 or mouse_cor[0]>= SCREEN_W - SCREEN_W//4 or mouse_cor[1]<= SCREEN_H//4 or mouse_cor[1]>= SCREEN_H - SCREEN_H//4:
            mouse.set_pos([SCREEN_W//2,SCREEN_H//2])
        if not falg_motion:
            mouse.set_pos([SCREEN_W//2,SCREEN_H//2])
        if count_gun > 0 :
            count_gun -= 1
        if count_change_direction_criminal >= 20:

            count_change_direction_criminal = 0 
            direction_move_criminal = random.choice(["L","L","L","R","R","R",None])
            count_move_criminal = 60 
            
        if criminal.start_y < -criminal.HEIGHT:

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
