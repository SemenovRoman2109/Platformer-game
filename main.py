from module import * #Подключаем модуль с модулями
from sprite import Sprite
init() #Инициализируем pygame
#Создаем функцию запуска игры
def run_game():    
    
    #Рисуем поверхности
    drawSurfaces()

    #y передвигающийся плаформы+
    #Основной цыкл игры
    dict_argument["list_surface"] = list_surface[dict_argument["index_lvl"]][dict_argument["index_location"]]
    sprite1.image_sprite.X = dict_spawn_and_finish_point["lvl"+str(dict_argument["index_lvl"]+1)+"_location_"+str(dict_argument["index_location"]+1)][0][0]
    sprite1.image_sprite.Y = dict_spawn_and_finish_point["lvl"+str(dict_argument["index_lvl"]+1)+"_location_"+str(dict_argument["index_location"]+1)][0][1]
    
    while dict_argument["game"]:
        clock.tick(FPS)

        for event1 in event.get(): # Получаем значение события из "списка событий" 
            # и записываем в переменную event1 
            mouse_cor = mouse.get_pos() #Включаем поддержку действия мыши
            
            if dict_argument["flag_puzzle_location"]:
                puzzle(event1)
            if event1.type == MOUSEBUTTONDOWN and event1.button == 1:
                if sprite1.ghost_img.check_mouse_cor(mouse_cor):
                    sprite1.count_pressing_ghost += 1
                if dict_argument["flag_collid_npc"]:
                    for i in list_button_collid:
                        if i.check_mouse_cor_font(mouse_cor):
                            if list_NPC[dict_argument["index_npc_collid"]].path == "image/Персонажи/Преступник/model.png":
                                if i.font_content == ["Да"]:
                                    if finish_shooting():
                                        dict_argument["screen_dimming_flag"] =  "+"
                                        dict_argument["index_text_drimming"] = "win_game"

                                    else:
                                        dict_argument["screen_dimming_flag"] =  "+"
                                        dict_argument["index_text_drimming"] = "lose_game" 
                                else:
                                    dict_argument["flag_false_criminal_selected"] = True
                            else:
                                if i.font_content == ["Да"]:
                                    if dict_argument["number_click_npc"] == 0:
                                        dict_argument["screen_dimming_flag"] = "+"
                                        dict_argument["index_text_drimming"] = "incorrectly_selected_criminal"
                                        sprite1.image_sprite.X = dict_spawn_and_finish_point["lvl"+str(dict_argument["index_lvl"]+1)+"_location_"+str(dict_argument["index_location"]+1)][0][0]
                                        sprite1.image_sprite.Y = dict_spawn_and_finish_point["lvl"+str(dict_argument["index_lvl"]+1)+"_location_"+str(dict_argument["index_location"]+1)][0][1]
                                        dict_argument["number_click_npc"] += 1
                                        dict_argument["list_surface"][list_index_NPC[dict_argument["index_npc_collid"]][0]][list_index_NPC[dict_argument["index_npc_collid"]][1]] = "0"
                                        list_NPC.pop(dict_argument["index_npc_collid"])
                                    else:
                                        dict_argument["screen_dimming_flag"] = "+"
                                        dict_argument["index_text_drimming"] = "lose_game"
                                else:
                                    dict_argument["flag_false_criminal_selected"] = True

            if dict_argument["flag_collid_npc"]:
                for i in list_button_collid:
                    if i.check_mouse_cor_font(mouse_cor):
                        for obj in list_button_collid:
                            obj.font_color = "darkgrey"
                        i.font_color = "red"
                    else:
                        i.font_color = "darkgrey"

            
            if event1.type == QUIT: # если событие равно "закрыть" выполняем метод exit()
                dict_argument["game"] = False #Отключает игру

        
        if dict_argument["scene"] == "game": #Сцена игры

            
            dict_Graphic_elements_obj["Fon"].show_image(screen) #Отображаем фон 
            move_cloud() #Функция передвежения облоков

            #Перебераем все списки блоков и отррисовываем их
            for i in dict_list_border["list_border_cor"]:
                i[-2].show_image(screen)
            for i in dict_list_border["list_border_cor_paper_and_door"]:
                i[-2].show_image(screen)
            for i in dict_list_border["list_border_cor_ladder"]:
                i[-2].show_image(screen)
            
            for i in dict_list_border["list_border_cor_cracking"]:
                i[-2].show_image(screen)
            dict_argument["flag_collid_npc"] = False
            for p in list_noot_colision_platphorm:
                p.show_image(screen)
            for i in list_NPC:
                
                i.show_image(screen)
                if Rect.colliderect(sprite1.image_sprite.RECT,i.RECT) :
                    if not dict_argument["flag_false_criminal_selected"]:
                        dict_argument["flag_collid_npc"] = True
                        dict_argument["index_npc_collid"] = list_NPC.index(i)
                        text_collid = Font("font/pixel_font.ttf",SCREEN_W//20,"red","Он преступник?",0,SCREEN_H-SCREEN_W//18)
                        text_collid.show_text(screen)
                        for i in list_button_collid:
                            i.show_text(screen)
                else:
                    if list_NPC.index(i) == dict_argument["index_npc_collid"]:
                        dict_argument["flag_false_criminal_selected"] = False
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
            if sprite1.can_move and dict_argument["screen_dimming_flag"] == None and not dict_argument["flag_puzzle_location"]:
                
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
            print(dict_argument["index_location"])
            direction_move_map = sprite1.finish_lvl(shooting_lvl,dict_Graphic_elements_obj["Fon"],move_cloud,book)
            if direction_move_map != "False" and direction_move_map != "finish_lvl":
                dict_argument["index_location"] += 1
                move_map(direction_move_map)
                list_NPC.clear()
            elif direction_move_map == "finish_lvl":
                
                dict_argument["BLOCK_SIZE"] = round(SCREEN_W/30)
                dict_argument["index_lvl"] = 1
                dict_argument["index_location"] = 0
                dict_argument["screen_dimming_flag"] = "+"
                dict_argument["index_text_drimming"] = None
                dict_argument["list_surface"] = list_surface[dict_argument["index_lvl"]][dict_argument["index_location"]]
                dict_list_border["list_border_cor_cracking"].clear()
                drawSurfaces()
                
                
                sprite1.image_sprite.X = dict_argument["BLOCK_SIZE"]*18
                sprite1.image_sprite.Y = SCREEN_H-dict_argument["BLOCK_SIZE"]*3.5
                
                sprite1.speed = dict_argument["BLOCK_SIZE"]//5
                sprite1.image_sprite.WIDTH = dict_argument["BLOCK_SIZE"]
                sprite1.image_sprite.HEIGHT = dict_argument["BLOCK_SIZE"]*1.66
                sprite1.image_sprite.image_load()
                sprite1.jummp_boost = dict_argument["BLOCK_SIZE"]*1.1*3
                sprite1.image_sprite.start_x =  sprite1.image_sprite.X
                sprite1.image_sprite.start_y =  sprite1.image_sprite.Y
                sprite1.count_duration_shield = dict_argument["duration_shield"]
                sprite1.ghost_img = Graphic_elements(0,0,dict_argument["BLOCK_SIZE"],dict_argument["BLOCK_SIZE"]*1.86,"image/ghost_1.png")
                sprite1.shield_img = Graphic_elements(0,0,sprite1.image_sprite.WIDTH * 1.68,sprite1.image_sprite.HEIGHT * 1.50,"image/shield.png")
                
            if cracking_platform(sprite1): #Трескающаяся платформа если треснулась или починилась обновляем поверхности
                drawSurfaces()
            # перебираем все рект обекты крюков 
            for rect_rope in list_rect: 
                sprite1.hook(rect_rope) 
            # Добавляем невидимые платформы
            # ключи
            paper = sprite1.paper()
            if paper == "paper_true":
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

            sprite1.statistic_person() #Статистика игрока
            sprite1.ghost(screen)
            for i in dict_list_border["list_border_cor_spring"]:
                i[-2].show_image(screen)
            if dict_argument["index_location"] == 0 and dict_argument["index_lvl"] == 0:
                #Создаем дверь и кнопку
                door_and_button(4,7,None,None,"Д","д",sprite1,"r",100)

            # bird() #Включает метод птицы
            
                
            function_dimming()
            # 
            

            if dict_argument["count_final_puzzle"] != None and dict_argument["count_final_puzzle"] <= 0:
                sprite1.image_sprite.X = dict_spawn_and_finish_point["lvl2_location_2"][0][0]
                sprite1.image_sprite.Y = dict_spawn_and_finish_point["lvl2_location_2"][0][1]
                sprite1.image_sprite.start_x = sprite1.image_sprite.X
                sprite1.image_sprite.start_y = sprite1.image_sprite.Y
                dict_argument["index_location"] += 1
                move_map("right")
                dict_argument["count_final_puzzle"] = None
            if dict_argument["flag_puzzle_location"]:
                puzzle(False)

        # print(clock.get_fps()) #Пишит в терминале количество кадров в секунду
        display.update() #Обновление экрана
#Запускает игру
menu(run_game)


