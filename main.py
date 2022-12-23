from module import * #Подключаем модуль с модулями

init() #Инициализируем pygame
#Создаем функцию запуска игры
def run_game():    
    #Создаем дверь и кнопку
    door_and_button(5,7,11,9,"Д","д",sprite1)
    #Рисуем поверхности
    drawSurfaces()
    #y передвигающийся плаформы
    #Основной цыкл игры
    
    while dict_argument["game"]:
        
        for event1 in event.get(): # Получаем значение события из "списка событий" 
            # и записываем в переменную event1 
            mouse_cor = mouse.get_pos() #Включаем поддержку действия мыши
            if event1.type == MOUSEBUTTONDOWN:
                if sprite1.ghost_img.check_mouse_cor(mouse_cor):
                    sprite1.count_pressing_ghost += 1
            
            if event1.type == QUIT: # если событие равно "закрыть" выполняем метод exit()
                dict_argument["game"] = False #Отключает игру

        if dict_argument["scene"] == "deth_screen": #Сцена смерти
            screen.fill((255,50,50)) #Заполняем фон красным
        if dict_argument["scene"] == "game": #Сцена игры

            if sprite1.health <= 0: #Если у игрока закончилось здоровье
                dict_argument["scene"] = "deth_screen" #Сцена смерти

            clock.tick(FPS) #Ограничивает количество кадров
            dict_Graphic_elements_obj["Fon"].show_image(screen) #Отображаем фон 
            move_cloud() #Функция передвежения облоков

            #Перебераем все списки блоков и отррисовываем их
            for i in dict_list_border["list_border_cor"]:
                if i[-1] != "K":
                    i[-2].show_image(screen)
            for i in dict_list_border["list_border_cor_key_and_door"]:
                i[-2].show_image(screen)
            for i in dict_list_border["list_border_cor_ladder"]:
                i[-2].show_image(screen)
            
            for i in dict_list_border["list_border_cor_cracking"]:
                i[-2].show_image(screen)

            saw_function() #Функция добавляет пилу
            rope_angle("index_Hook","angle_Hook_direction","angle_Hook") #функция наклона веревки
            list_rect = [] #Список верёвок
            #перебираем все крюки 
            for hook in list_hook:
                rect_rope = rope("index_Hook",hook,"angle_Hook",20,30)
                list_rect.append(rect_rope)
                sprite1.Hook(rect_rope) 
            invisibility_block("i","I",sprite1)
            rope_angle("index_Rope_with_saw","angle_Rope_with_saw_direction","angle_Rope_with_saw")  #функция наклона веревки
            #перебираем все вереаки с пилами 
            for Rope_with_saw in list_Rope_with_saw:
                rect_rope = rope("index_Rope_with_saw",Rope_with_saw,"angle_Rope_with_saw",30,30)
                sprite1.Touch_of_death(rect_rope) #Дотронулся до пилы = сразу умер
            #Основы платформера
            sprite1.image_sprite.show_image(screen)  #Показ картинки
            if sprite1.can_move:
                
                sprite1.squat(screen)
                sprite1.sprite_move() #Анимации
                if sprite1.flag_squat == 0: 
                    sprite1.jump_pressed() #Прыгнул
                sprite1.sprite_gravity() #Графитация
                sprite1.check_col_from_ab() #Проверка колизии
                sprite1.can_move_left() #Возможность идти влево (тоже колизия)
                sprite1.can_move_right() #Возможность идти вправо (тоже колизия)
                sprite1.can_move_up() #Возможность прыгнуть вверх (тоже колизия)
                sprite1.ladder() #Лестница
            else:
                sprite1.fly_up = False
            sprite1.spring()
            sprite1.shield(screen)
            
            direction_move_map = sprite1.finish_lvl(shooting_lvl)
            if direction_move_map != "False":
                move_map(direction_move_map)
                black_fon.path = "image/lvl"+str(dict_argument["index_location"]+1)+".png"
                black_fon.image_load()
            if cracking_platform(sprite1): #Трескающаяся платформа если треснулась или починилась обновляем поверхности
                drawSurfaces()
            # перебираем все рект обекты крюков 
            for rect_rope in list_rect:
                sprite1.hook(rect_rope) 
            # Добавляем невидимые платформы
            # ключи
            key = sprite1.key()
            if key == "key_true" or key == "door":
                drawSurfaces()
            # шипы
            spike()
            
            # Облоко подсказка
            # help_function(2.5,2,3,2.5,"TEXT;TEXT","red")
            
            # Условие таймер которое двигает платформы

            if dict_argument_block["flag_direction_spinning_motion_block"] == "+":
                dict_argument_block["count_img_spinning_motion_block"] += 1
                drawSurfaces()
            else:
                dict_argument_block["count_img_spinning_motion_block"] -= 1
                drawSurfaces()
            if dict_argument_block["count_img_spinning_motion_block"] == 1:
                dict_argument_block["flag_direction_spinning_motion_block"] = "+"
            if dict_argument_block["count_img_spinning_motion_block"] == 5:
                dict_argument_block["flag_direction_spinning_motion_block"] = "-"
                    
            if dict_argument_block["count_motion_block"] == dict_argument_block["max_count_motion_block"]:

                block_motion_right_left(list_surface=dict_argument["list_surface"],dict_argument_block=dict_argument_block,platform_length=2,sprite=sprite1 )
                block_motion_down_up(list_surface=dict_argument["list_surface"],dict_argument_block=dict_argument_block,sprite=sprite1)

                drawSurfaces()
                dict_argument_block["count_motion_block"] = 0
            dict_argument_block["count_motion_block"] += 1
            
            # black_fon.show_image(screen) #ФОНННННННННННННННННННННННННННННННННННННННННННННННННННННННННННННННННННННННННННННННН
            sprite1.statistic_person() #Статистика игрока
            sprite1.ghost(screen)
            for i in dict_list_border["list_border_cor_spring"]:
                i[-2].show_image(screen)
            if dict_argument["index_location"] == 0 and dict_argument["index_lvl"] == 0:
                #Создаем дверь и кнопку
                door_and_button(4,7,None,None,"Д","д",sprite1)
            # bird() #Включает метод птицы
            
            
            # 
        # print(clock.get_fps()) #Пишит в терминале количество кадров в секунду
        display.update() #Обновление экрана
#Запускает игру
run_game()

