# Подключаем нужные нам модули
from pygame import*
import os
import random
# Подключаем модули нашего проекта
from graphic_elements import Graphic_elements
from constant import *
from object import *
from text import *
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
    # очищаем списки 
    list_Rope_with_saw.clear()
    list_hook.clear()
    list_spikes.clear()
    list_saw.clear()
    dict_list_border["list_border_cor_key_and_door"].clear()
    dict_list_border["list_border_cor_ladder"].clear()
    dict_list_border["list_border_cor"].clear()
    dict_list_border["list_flag"].clear()
    # Список сиволов
    list_symbol = ["b","K","D","П","Л","л","ъ","Ъ","P","L","i","c","с","C"]
    # список символов трескающихся платформ
    list_cracking_platform = ["c","с","C"]
    # Кол-во платформ
    number_cracking = 0
    number_spring = 0
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
    WIDTH = SCREEN_W//20
    HEIGHT = SCREEN_H//11
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
                WIDTH = SCREEN_W//20
                HEIGHT = SCREEN_W//20//3.55
                NAME_LIST = "list_border_cor_cracking"
                number_cracking += 1
            elif dict_argument["list_surface"][i][j] == "R":
                list_Rope_with_saw.append(Graphic_elements(X+SCREEN_W//44-SCREEN_W//10,Y,SCREEN_W//15,SCREEN_W//20*10,"image/Rope_with_saw.png"))
            elif dict_argument["list_surface"][i][j] == "H":
                list_hook.append(Graphic_elements(X+SCREEN_W//44-SCREEN_W//60,Y,SCREEN_W//20,SCREEN_H//11*10,"image/Hook.png"))
            elif dict_argument["list_surface"][i][j] == "К":
                list_spikes.append(Graphic_elements(X,Y+(SCREEN_H//11-SCREEN_H//30),SCREEN_W//20,SCREEN_H//30,"image/spikes.png"))
            elif dict_argument["list_surface"][i][j] == "к":
                obj = Graphic_elements(X,Y,SCREEN_W//20,SCREEN_H//30,"image/spikes.png")
                obj.image_load(rotate_y=True)
                list_spikes.append(obj)
            elif dict_argument["list_surface"][i][j] == "ш":
                list_spikes.append(Graphic_elements(X,Y+(SCREEN_H//11-SCREEN_H//25),SCREEN_W//20,SCREEN_H//25,"image/spikes.png"))    



            elif dict_argument["list_surface"][i][j] == "Л":
                PATH = "image/ladder_middle.png"
                WIDTH = SCREEN_W//20
                HEIGHT = SCREEN_H//11                     
                NAME_LIST = "list_border_cor_ladder"
            elif dict_argument["list_surface"][i][j] == "л":
                
                PATH = "image/ladder_beginning.png"
                WIDTH = SCREEN_W//20
                HEIGHT = SCREEN_H//11                     
                NAME_LIST = "list_border_cor_ladder"
                if dict_argument["list_surface"][i][j + 1] == "0":
                    direction_begin_leader = "l"
                else:
                    direction_begin_leader = "r"
            elif dict_argument["list_surface"][i][j] == "ъ":
                PATH = "image/ladder_end.png"
                WIDTH = SCREEN_W//20
                HEIGHT = SCREEN_H//11                     
                NAME_LIST = "list_border_cor_ladder"

            elif dict_argument["list_surface"][i][j] == "Ъ":
                PATH = "image/ladder_beginning_end.png"
                WIDTH = SCREEN_W//20
                HEIGHT = SCREEN_H//11                     
                NAME_LIST = "list_border_cor_ladder"
                if dict_argument["list_surface"][i][j + 1] == "0":
                    direction_begin_leader = "l"
                else:
                    direction_begin_leader = "r"



            elif dict_argument["list_surface"][i][j] == "П":
                PATH = "image/spring.png"
                WIDTH = SCREEN_W//20
                HEIGHT = SCREEN_H//11
                NAME_LIST = "list_border_cor_spring"
                number_spring += 1
            elif dict_argument["list_surface"][i][j] == "s":
                list_saw.append(Graphic_elements(X+(SCREEN_W//13-SCREEN_W//20),Y+(SCREEN_H//7.1-SCREEN_H//11),SCREEN_W//13,SCREEN_H//7.1,"image/saw.png"))
            
            elif dict_argument["list_surface"][i][j] == "D":
                PATH = "image/Door.png"
                WIDTH = SCREEN_W//20
                HEIGHT = SCREEN_H//5.5
                NAME_LIST = "list_border_cor"
            elif dict_argument["list_surface"][i][j] == "P": 
                if dict_argument["list_surface"][i][j+1] == "P":
                    PATH = "image/block_motion_left.png"
                elif dict_argument["list_surface"][i][j-1] == "P":
                    PATH = "image/block_motion_right.png"
                WIDTH = SCREEN_W//20
                HEIGHT = SCREEN_H//11
                NAME_LIST = "list_border_cor"
            elif dict_argument["list_surface"][i][j] == "b": 
                PATH = "image/block.png"
                WIDTH = SCREEN_W//20
                HEIGHT = SCREEN_H//11
                NAME_LIST = "list_border_cor"
            elif dict_argument["list_surface"][i][j] == "L":
                PATH = "image/Motion_block_up_down_"+str(dict_argument_block["count_img_spinning_motion_block"])+".png"
                WIDTH = SCREEN_W//20
                HEIGHT = SCREEN_H//11//2
                NAME_LIST = "list_border_cor"
            elif dict_argument["list_surface"][i][j] == "K":
                PATH = "image/Key.png"
                WIDTH = SCREEN_W//20
                HEIGHT = SCREEN_H//11
                NAME_LIST = "list_border_cor_key"

            elif dict_argument["list_surface"][i][j] == "i":
                if dict_argument_block["count_load"] < 24 and dict_argument["ded"]:
                    PATH = "image/block.png"
                    WIDTH = SCREEN_W//20
                    HEIGHT = SCREEN_H//11
                    NAME_LIST = "list_border_cor"
            
            elif dict_argument["list_surface"][i][j] in list_key_door:
                PATH = "image/Door_block.png"
                WIDTH = SCREEN_W//20*2
                HEIGHT = SCREEN_W//20//5
                NAME_LIST = "list_border_cor"
            for obj in list_key_door:
                if dict_argument["list_surface"][i][j] in obj.lower():
                    PATH = "image/Open_door_block.png"
                    WIDTH = SCREEN_W//20*2
                    HEIGHT = SCREEN_H//11
                    NAME_LIST = "list_border_cor_key_and_door"
            
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
            X += SCREEN_W//20
        # Изменяем кординату на которой отрисовываеться картинка    
        X = dict_argument["X_MAP"]
        Y += SCREEN_H//11
    # Добавляем все в основной список 
    for i in range(len(dict_list_border["list_flag"])):
        for j in range(len(dict_list_border["list_flag"][i])):
            if len(dict_list_border["list_flag"][i][j]) != 0:
                dict_list_border[dict_list_border["list_flag"][i][j][-3]].append(dict_list_border["list_flag"][i][j])

# Функция для движения платформы вправо влево
def block_motion_right_left(list_surface,dict_argument_block,platform_length,sprite,block_size_y = SCREEN_H//11,block_size_x = SCREEN_W//20):
    # Индексы клетки
    index_y = 0
    index_x = 0
    # Перебираем матрицу
    index_vertically = 0 
    for obj in dict_argument["list_surface"]:
        if index_vertically == 0 :
            for i in obj:
                if i == "P":
                    index_vertically = dict_argument["list_surface"].index(obj)
                    break
            # Увеличиваем index для нахождения клетки с платформой
            index_x += 1
        # Увеличиваем index для нахождения клетки с платформой
        index_y += 1
        index_x = 0
    # Индексы клетки            
    index_x = 0
    
    #Перебираем цыкл столько раз сколько длина платформа
    for obj in range(platform_length):
        # Проверяем направление платформы
        if dict_argument_block["flag_directory_motion_block_left_right"] == "R":
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
                        block = [index_vertically*block_size_y,index_vertically*block_size_y+block_size_y,index_x*block_size_x-block_size_x,index_x*block_size_x]
                        if sprite.image_sprite.Y + sprite.image_sprite.HEIGHT >= block[0] and sprite.image_sprite.X + sprite.image_sprite.WIDTH >= block[2] + SCREEN_W//20//3 and sprite.image_sprite.X <= block[3] - SCREEN_W//20//3 and sprite.image_sprite.Y + sprite.image_sprite.HEIGHT <= block[0] + sprite.gravity_speed :
                            sprite.image_sprite.X += block_size_y
                        # Останавливаем цыкл
                        break
                    # Если следующая келтка не путь для платформы
                    elif dict_argument["list_surface"][index_vertically][index_x + 1] in ["0","b"] and obj == 0:
                        # Меняем направление
                        dict_argument_block["flag_directory_motion_block_left_right"] = "L"
                        # Останавливаем цыкл
                        break
                        
                index_x += 1
            index_x = 0
        # Проверяем направление платформы
        if dict_argument_block["flag_directory_motion_block_left_right"] == "L":
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
                        block = [index_vertically*block_size_y,index_vertically*block_size_y+block_size_y,index_x_2*block_size_x-block_size_x,index_x_2*block_size_x]
                        if sprite.image_sprite.Y + sprite.image_sprite.HEIGHT >= block[0] and sprite.image_sprite.X + sprite.image_sprite.WIDTH >= block[2] + SCREEN_W//20//3 and sprite.image_sprite.X <= block[3] - SCREEN_W//20//3 and sprite.image_sprite.Y + sprite.image_sprite.HEIGHT <= block[0] + sprite.gravity_speed :
                                sprite.image_sprite.X -= block_size_y
                        # Останавливаем цыкл
                        break
                    # Если следующая келтка не путь для платформы
                    elif dict_argument["list_surface"][index_vertically][::-1][index_x + 1] in ["0","b"] and obj == 1:
                        # Меняем направление
                        dict_argument_block["flag_directory_motion_block_left_right"] = "R"
                        # Останавливаем цыкл
                        break
                # Увеличиваем index
                index_x_2 -= 1
                index_x += 1

            index_x = 0

# Функция для движения платформы вверх вниз
def block_motion_down_up(list_surface,dict_argument_block,sprite,block_size_y = SCREEN_H//11,block_size_x = SCREEN_W//20):
    # Индексы клетки
    index_y = 0
    index_x = 0
    # Перебираем матрицу
    for obj in dict_argument["list_surface"]:
        for i in obj:
            # Находим платформу
            if i == "L":
                # Если направление в верх 
                if dict_argument_block["flag_directory_motion_block_up_down"] == "U":
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
                        block = [index_y*block_size_y,index_y*block_size_y+block_size_y,index_x*block_size_x,index_x*block_size_x+block_size_x]
                        if sprite.image_sprite.Y + sprite.image_sprite.HEIGHT >= block[0] and sprite.image_sprite.X + sprite.image_sprite.WIDTH >= block[2] and sprite.image_sprite.X <= block[3] and sprite.image_sprite.Y + sprite.image_sprite.HEIGHT <= block[0] + sprite.gravity_speed :
                            sprite.image_sprite.Y -= block_size_y
                        # Останавливаем функцию
                        return "stop function"
                    # Если в низ нельзя двигаться    
                    elif dict_argument["list_surface"][index_y - 1][index_x] == "0":
                        # Меняем направления
                        dict_argument_block["flag_directory_motion_block_up_down"] = "D"
                        # Останавливаем функцию
                        return "stop function"
                # Если направление в низ        
                if dict_argument_block["flag_directory_motion_block_up_down"] == "D":
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
                        block = [index_y*block_size_y,index_y*block_size_y+block_size_y,index_x*block_size_x,index_x*block_size_x+block_size_x]
                        if sprite.image_sprite.Y + sprite.image_sprite.HEIGHT >= block[0] and sprite.image_sprite.X + sprite.image_sprite.WIDTH >= block[2] and sprite.image_sprite.X <= block[3] and sprite.image_sprite.Y + sprite.image_sprite.HEIGHT <= block[0] + sprite.gravity_speed :
                            sprite.image_sprite.Y += block_size_y
                        # Останавливаем функцию
                        return "stop function"
                    # Если в верх нельзя двигаться   
                    elif dict_argument["list_surface"][index_y + 1][index_x] == "0":
                        dict_argument_block["flag_directory_motion_block_up_down"] = "U"
                        # Останавливаем функцию
                        return "stop function"
                            
            # Увеличиваем index для нахождения клетки с платформой
            index_x += 1
        # Увеличиваем index для нахождения клетки с платформой
        index_y += 1
        index_x = 0

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
    Rope_copy = transform.rotate(graphic_elements.IMG, int(dict_argument_angle[angle]))
    # Задаем x и y для нашего наконечника дабы засечь косание с ним
    x = graphic_elements.X-graphic_elements.WIDTH//2+int(list_cor_Rope[dict_argument_angle[index]][0])
    y = graphic_elements.Y+graphic_elements.HEIGHT//2-graphic_elements.WIDTH+int(list_cor_Rope[dict_argument_angle[index]][1])
    # Создаем рект обект для колизии с накончечником
    Rope_rect = Rect(x,y,graphic_elements.WIDTH,graphic_elements.WIDTH)
    # draw.rect(screen,(0,0,0),Rope_rect)
    # Отрисовываем веревку 
    screen.blit(Rope_copy, (graphic_elements.X - int(Rope_copy.get_width() / 2), graphic_elements.Y - int(Rope_copy.get_height() / 2)))
    # Возвращаем рект обект для колизии с накончечником 
    return Rope_rect

#Функия двери которая открываеться по кнопке
def door_and_button(index_button_x_1,index_button_y_1,index_button_x_2,index_button_y_2,element_door,element_door_empty,sprite1):
    # Если еще нет етого елемента в словаре всехх дверей с кнопками 
    if not str("Count_door_"+element_door) in list(dict_argument_door_block.keys()):
        #Добавляем в словарь новый ключ к нашей двери
        dict_argument_door_block[str("Count_door_"+element_door)] = 0
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
    graphik_element_button_1 = Graphic_elements(index_button_x_1*SCREEN_W//20,(index_button_y_1+1)*SCREEN_H//11-dict_Graphic_elements_obj["button"].HEIGHT,dict_Graphic_elements_obj["button"].WIDTH,dict_Graphic_elements_obj["button"].HEIGHT,dict_Graphic_elements_obj["button"].path)
    if index_button_x_2 == None:
        graphik_element_button_2 =Graphic_elements(0,0,0,0,None)
    else:
        graphik_element_button_2 = Graphic_elements(index_button_x_2*SCREEN_W//20,(index_button_y_2+1)*SCREEN_H//11-dict_Graphic_elements_obj["button"].HEIGHT,dict_Graphic_elements_obj["button"].WIDTH,dict_Graphic_elements_obj["button"].HEIGHT,dict_Graphic_elements_obj["button"].path)
    
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
        dict_argument_door_block[str("Count_door_"+element_door)] = 100 
        

        
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
                    dict_argument["list_surface"][i[0]//(SCREEN_H//11)][i[4]//(SCREEN_W//20)] = list_cracking[number+1]
                    dict_list_border["list_border_cor_cracking"][dict_list_border["list_border_cor_cracking"].index(i)][-2].path = "image/cracking_platform_"+str(number+1)+".png"
                    dict_list_border["list_border_cor_cracking"][dict_list_border["list_border_cor_cracking"].index(i)][-2].image_load()
                    dict_list_border["list_border_cor_cracking"][dict_list_border["list_border_cor_cracking"].index(i)][6] = 20
                # Если нет то удаляем платформу
                else:
                    # Убираем букву на матрицу заменяя её нулем(пустым местом)
                    dict_argument["list_surface"][i[0]//(SCREEN_H//11)][i[4]//(SCREEN_W//20)] = "0"
                    # Добавляем плуатформу в словарь сломаных трескающихся платформ дабы потом его возобновить ключом к которому являються кординаты через запятую
                    key = str(i[0]//(SCREEN_H//11))+","+str(i[4]//(SCREEN_W//20))
                    broken_cracking_platform[key] = 100
                    # Убираем ету пллатформу из списка платформ и очищаем список обектов етих платформ чтоб он мог снова заполниться
                    dict_list_border["list_border_cor_cracking"].clear()
                    # Обновляем поверхности
                    return True
            # Если счетчик востановления платформы доходит до нуля то изменяем картинку на превидущую стадию
            if i[7] <= 0:
                # Проверяем можно ли изменяем картинку на прошлую стадию
                if number - 1 >= 0:
                    dict_argument["list_surface"][i[0]//(SCREEN_H//11)][i[4]//(SCREEN_W//20)] = list_cracking[number-1]
                    dict_list_border["list_border_cor_cracking"][dict_list_border["list_border_cor_cracking"].index(i)][-2].path = "image/cracking_platform_"+str(number-1)+".png"
                    dict_list_border["list_border_cor_cracking"][dict_list_border["list_border_cor_cracking"].index(i)][-2].image_load()
                    dict_list_border["list_border_cor_cracking"][dict_list_border["list_border_cor_cracking"].index(i)][7] = 40


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
                        dict_argument["list_surface"][i+2][j] = "к"
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
        saw.Y += SCREEN_H//11
        # крутим пилу
        saw_copy = transform.rotate(saw.IMG, int(dict_argument_angle["angle_saw"]))
        # Создаем рект обект пилы
        rect_saw = Rect(saw.X - saw.WIDTH//2, saw.Y - saw.HEIGHT//2,saw.WIDTH,saw.HEIGHT)
        # draw.rect(screen,(255,0,0),rect_saw)
        # Отображаем пилу
        screen.blit(saw_copy, (saw.X - int(saw_copy.get_width() / 2), saw.Y - int(saw_copy.get_height() / 2)))
        # Убиваем игрока при косании с пилой
        sprite1.Touch_of_death(rect_saw)
        # КОСТЫЛЬ
        saw.Y -= SCREEN_H//11

# Функция облока подсказки
def help_function(index_x,index_y,indnex_width,index_height,text,color):
    # Задаем размеры
    border_width = SCREEN_W//20
    border_height = SCREEN_H//11
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
        dict_argument["list_beard"].append(Graphic_elements(-SCREEN_W//20,SCREEN_H//11,SCREEN_W//20,SCREEN_H//11//1.32,"image/beard/beard1.png",4))
    dict_argument["count_beard"] += 1

# Функция движения карты
def move_map(direction):
    # Флаг направления оси
    flag_direction = None
    # Список в который будет помещена полная карта
    full_map = []
    list_full_surface = dict_argument["full_surface"]
    # Скорость передвижаня карты
    spead_move_map = 100
    # Проверяем направление перемещения
    if direction == "right":
        # Соединяем матрицы
        for index in range(len(dict_argument["list_surface"])):
            str_list = []
            for i in dict_argument["list_surface"][index]:
                str_list.append(i)
            for i in list_full_surface[dict_argument["index_lvl"]][dict_argument["index_location"]+1][index]:
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
            for i in list_full_surface[dict_argument["index_lvl"]][dict_argument["index_location"]+1][index]:
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
        for index in list_full_surface[dict_argument["index_lvl"]][dict_argument["index_location"]+1]:
            full_map.append(index)
        # Задаем стартовую координауту отрисовки здувух матриц
        a = -SCREEN_H
         # Задаем ось для перемещнеия карты
        flag_direction = "Y_MAP"
    # Проверяем направление перемещения
    elif direction == "up":
        # Соединяем матрицы
        for index in list_full_surface[dict_argument["index_lvl"]][dict_argument["index_location"]+1]:
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
        black_fon =  Graphic_elements(0,0,SCREEN_W,SCREEN_H,"image/lvl"+str(dict_argument["index_location"]+1)+".png")
        black_fon_next =  Graphic_elements(0,0,SCREEN_W,SCREEN_H,"image/lvl"+str(dict_argument["index_location"]+2)+".png")
        if flag_direction == "Y_MAP":
            black_fon_next.Y += SCREEN_H
        else:
            black_fon_next.X += SCREEN_W
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
            for i in dict_list_border["list_border_cor_key_and_door"]:
                i[-2].show_image(screen)  
            for i in dict_list_border["list_border_cor_ladder"]:
                i[-2].show_image(screen)
            for i in dict_list_border["list_border_cor_spring"]:
                i[-2].show_image(screen)
            for i in dict_list_border["list_border_cor_cracking"]:
                i[-2].show_image(screen)
            black_fon.show_image(screen)
            black_fon_next.show_image(screen)
            # Двигаем карта
            dict_argument[flag_direction] -= SCREEN_W//spead_move_map
            if flag_direction == "Y_MAP":
                black_fon_next.Y -= SCREEN_W//spead_move_map
                black_fon.Y -= SCREEN_W//spead_move_map
            else:
                black_fon_next.X -= SCREEN_W//spead_move_map
                black_fon.X -= SCREEN_W//spead_move_map
            # Обновляем экран
            display.update()
    # Проверяем направления
    if direction == "up" or direction == "left":
        # Цыкл движения
        black_fon =  Graphic_elements(0,0,SCREEN_W,SCREEN_H,"image/lvl"+str(dict_argument["index_location"]+1)+".png")
        black_fon_next =  Graphic_elements(0,0,SCREEN_W,SCREEN_H,"image/lvl"+str(dict_argument["index_location"]+2)+".png")
        if flag_direction == "Y_MAP":
            black_fon_next.Y -= SCREEN_H
        else:
            black_fon_next.X -= SCREEN_W
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
            for i in dict_list_border["list_border_cor_key_and_door"]:
                i[-2].show_image(screen)  
            for i in dict_list_border["list_border_cor_ladder"]:
                i[-2].show_image(screen)
            for i in dict_list_border["list_border_cor_spring"]:
                i[-2].show_image(screen)
            for i in dict_list_border["list_border_cor_cracking"]:
                i[-2].show_image(screen)
            black_fon.show_image(screen)
            black_fon_next.show_image(screen)
            # Двигаем карта
            dict_argument[flag_direction] += SCREEN_W//spead_move_map
            if flag_direction == "Y_MAP":
                black_fon_next.Y += SCREEN_W//spead_move_map
                black_fon.Y += SCREEN_W//spead_move_map
            else:
                black_fon_next.X += SCREEN_W//spead_move_map
                black_fon.X += SCREEN_W//spead_move_map
            # Обновляем экран
            display.update()    
    
    # Меняем матрицу на другую
    dict_argument[flag_direction] = 0
    dict_argument["index_location"]+=1
    dict_argument["list_surface"] = list_full_surface[dict_argument["index_lvl"]][dict_argument["index_location"]]
    # Очищаем списки которые не очищаються в функции
    dict_list_border["list_border_cor_cracking"].clear()
    dict_list_border["list_border_cor_spring"].clear()
    # Обновляем матрицу
    drawSurfaces()

def shooting_lvl(screen,min_count_point,barriers):
    game = True
    mouse.set_visible(False)
   
    while game:
        screen.fill("black")
        Background_shooting.show_image(screen)
        aim.show_image(screen)
        falg_motion = False
        for event1 in event.get(): # Получаем значение события из "списка событий" 
            nouse_cor = mouse.get_pos()
            if event1.type == QUIT:
                game = False
            if event1.type == MOUSEMOTION:
                
                Background_shooting.X += int(event1.rel[0])
                print(event1.rel)
                Background_shooting.Y += int(event1.rel[1])
                falg_motion = True
                if Background_shooting.X > 0:
                    Background_shooting.X = 0
                if Background_shooting.Y > 0:
                    Background_shooting.Y = 0
                if Background_shooting.X < SCREEN_W - Background_shooting.WIDTH:
                    Background_shooting.X = SCREEN_W - Background_shooting.WIDTH
                if Background_shooting.Y < SCREEN_H - Background_shooting.HEIGHT:
                    Background_shooting.Y = SCREEN_H - Background_shooting.HEIGHT
        if nouse_cor[0]<= SCREEN_W//4 or nouse_cor[0]>= SCREEN_W - SCREEN_W//4 or nouse_cor[1]<= SCREEN_H//4 or nouse_cor[1]>= SCREEN_H - SCREEN_H//4:
            mouse.set_pos([SCREEN_W//2,SCREEN_H//2])
        if not falg_motion:
            mouse.set_pos([SCREEN_W//2,SCREEN_H//2])
        clock.tick(FPS*2)
        # print(clock.get_fps())
        display.update()
    mouse.set_visible(True)