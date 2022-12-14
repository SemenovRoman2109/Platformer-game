from pygame import*
import os
from graphic_elements import Graphic_elements
from text import Font
init()
from constant import *
class Sprite:
    def __init__(self, name_image, sprite_x, sprite_y,
                sprite_speed, sprite_width, sprite_height,
                sprite_gravity_power,
                double_jump = None,index_layout = 0,jump_boost = SCREEN_H//10*3,
                ):
        
        self.flag_hook = 20
        self.image_path = "image/Персонажи/Двойной_прижок/" + str(name_image) + ".png"
        self.speed = sprite_speed
        self.flag_leader = False
        self.start_speed = sprite_speed
        self.list_animation = []
        self.open_door = False
        for i in range(10):

            self.list_animation.append("image/Персонажи/Двойной_прижок/"+str(i+1)+".png")
        self.flag_sprite = 0 # счетчик изменения костюмов
        self.index = 0 # счетчик индексов списка list_images
        self.flag = 'R' # отвечает за контроль направления движения
        self.gravity_speed = sprite_gravity_power
        self.jump_now = 0                       
        self.collected_paper = []                                                            
        self.count = 0
        self.fly_up_spring = False
        self.fly_up = False
        self.gravity = True
        self.move_left = True
        self.move_right = True
        self.move_up = True
        self.jummp_boost = jump_boost
        self.index2 = 0
        self.double_jump = double_jump
        self.index_layout = index_layout
        self.flag_squat = 0
        self.flag_squat2 = 3
        self.random_direction_ghost_number = None
        self.random_direction_ghost_count = [10,15]
        self.image_sprite = Graphic_elements(sprite_x,sprite_y,sprite_width,sprite_height,self.image_path)   
        self.List_layout = [[K_LEFT,K_RIGHT,K_UP,K_DOWN],[K_a,K_d,K_w,K_s],[K_RIGHT,K_LEFT,K_DOWN,K_UP],[K_d,K_a,K_s,K_w]]
        self.flag_spring = 0
        self.ghost_img = Graphic_elements(0,0,dict_argument["BLOCK_SIZE"],dict_argument["BLOCK_SIZE"]*1.86,"image/ghost_1.png")
        self.count_pressing_ghost = 0
        self.shield_img = Graphic_elements(0,0,self.image_sprite.WIDTH * 1.68,self.image_sprite.HEIGHT * 1.50,"image/shield.png")
        self.count_duration_shield = dict_argument["duration_shield"]
        self.can_move = True
        self.change_img_ghost = [0,5]


    # Отображает статистику персонажа
    def statistic_person(self):

        if len(self.collected_paper) == 4:
            dict_argument["flag_puzzle_location"] = True
            self.collected_paper.clear()     
        if len(self.collected_paper) > 0:
            paper_img = Graphic_elements(0,SCREEN_H-dict_argument["BLOCK_SIZE"],dict_argument["BLOCK_SIZE"],dict_argument["BLOCK_SIZE"],"image/paper.png")
            paper_img.show_image(screen)
            number_paper = Font("font/pixel_font.ttf",dict_argument["BLOCK_SIZE"],(255,0,0),"X"+str(len(self.collected_paper)),dict_argument["BLOCK_SIZE"],SCREEN_H-dict_argument["BLOCK_SIZE"],1)
            number_paper.show_text(screen)
 
    # Функция приседания
    def squat(self,win):
        
        for block in dict_list_border["list_border_cor"]:
            block_rect = Rect(block[4]+(block[5]-block[4])//5,block[0]+(block[1]-block[0])//1.5,(block[5]-block[4])-(block[5]-block[4])//2.5,1)
            rect_sprite = Rect(self.image_sprite.X,self.image_sprite.Y,self.image_sprite.WIDTH,self.image_sprite.HEIGHT)

            if Rect.colliderect(rect_sprite,block_rect) and block[-1] == "L" and self.gravity == False: 
                self.image_sprite.HEIGHT = self.image_sprite.start_height / 1.7
                self.image_sprite.Y = self.image_sprite.Y + (self.image_sprite.HEIGHT - self.image_sprite.start_height / 3.4)
                self.speed = self.speed//2
                if self.flag == "R":
                    self.image_sprite.image_load()
                else:
                    self.image_sprite.image_load(rotate_x=True)
                self.flag_squat2 = 3
                self.flag_squat = 1
                break
        keys = key.get_pressed()   
        if self.flag_leader == False:
            if keys[self.List_layout[self.index_layout][3]] and self.flag_squat2 == 3 and self.gravity == False:
                if self.flag_squat == 1:
                    self.flag_squat = 0
                    self.flag_squat2 = 1
                elif self.flag_squat == 0:
                    self.flag_squat = 1
                    self.flag_squat2 = 1
            if not keys[self.List_layout[self.index_layout][3]]:
                if self.flag_squat2 == 1:
                    self.flag_squat2 = 0
            
                if self.flag_squat == 1 and self.flag_squat2 == 0:
                    self.image_sprite.HEIGHT = self.image_sprite.start_height / 1.7
                    self.image_sprite.Y += (self.image_sprite.HEIGHT - self.image_sprite.start_height / 15)
                    self.speed = self.speed//2
                    if self.flag == "R":
                        self.image_sprite.image_load()
                    else:
                        self.image_sprite.image_load(rotate_x=True)
                    self.flag_squat2 = 3
                if self.flag_squat == 0 and self.flag_squat2 == 0 and self.move_up:
                    self.image_sprite.HEIGHT = self.image_sprite.start_height
                    self.image_sprite.Y = self.image_sprite.Y - (self.image_sprite.HEIGHT - self.image_sprite.start_height / 1.7)
                    if self.flag == "R":
                        self.image_sprite.image_load()
                    else:
                        self.image_sprite.image_load(rotate_x=True)
                    self.flag_squat2 = 3  
                    self.speed = self.start_speed                        
    # Функция которая отвечает за анимации персонажа
    def sprite_move(self):  
        keys = key.get_pressed()        
        if keys[self.List_layout[self.index_layout][0]] and self.image_sprite.X > SCREEN_W//80 and self.move_left:
            self.image_sprite.X -= self.speed
            self.flag = "L"
            if self.index == 10:
                self.index = 0
            self.image_sprite.path = self.list_animation[self.index]
            self.image_sprite.image_load(rotate_x=True)
            if self.index2 >= 2:
                self.index += 1
                self.index2 = 0
            self.index2 += 1
            
        elif keys[self.List_layout[self.index_layout][1]] and self.image_sprite.X < SCREEN_W - self.image_sprite.WIDTH - SCREEN_W//80 and self.move_right:
            self.image_sprite.X += self.speed
            self.flag = "R"  
            if self.index == 10:
                self.index = 0
            
            
            self.image_sprite.path = self.list_animation[self.index]
            self.image_sprite.image_load()
            if self.index2 >= 3:
                self.index += 1
                self.index2 = 0
            self.index2 += 1
        else: 
            if self.flag == "L":
                self.index = 0 
                self.index2 = 0
            elif self.flag == "R":
                self.index = 0 
                self.index2 = 0             
    # Функция прыжка    
    def jump_pressed(self): 
        keys = key.get_pressed() 
        if self.flag_leader == False:
            if keys[self.List_layout[self.index_layout][2]] and self.jump_now == 0:
                
                self.jump_now = 1
                if self.double_jump and self.double_jump != None:
                    self.jump_now = 5
                    self.double_jump = False
                self.fly_up = True
                

            if keys[self.List_layout[self.index_layout][2]] and self.jump_now == 5 and self.fly_up == False and self.double_jump != None: 
                self.jump_now = 1
                self.fly_up = True
                
            if self.fly_up:
                if self.flag == "R":
                    self.image_sprite.path = "image/Персонажи/Двойной_прижок/1.png"
                    self.image_sprite.image_load()
                elif self.flag == "L":
                    self.image_sprite.image_load(rotate_x=True)
                self.image_sprite.Y -= self.jummp_boost//15
                self.count += 1
                if self.move_up == False or self.count == 15 or self.image_sprite.Y <= SCREEN_W//80:
                    self.fly_up = False
                    self.count = 0
    # Гравитация  смена индексов и картинок   
    def sprite_gravity(self): 
        if self.double_jump != None:
            if self.image_sprite.Y < SCREEN_H - self.image_sprite.HEIGHT and self.fly_up == False and self.gravity:
                if self.jump_now != 5:
                    self.jump_now = 1
                self.image_sprite.Y += self.gravity_speed
                if  self.flag == "R":
                    self.image_sprite.path = "image/Персонажи/Двойной_прижок/1.png"
                    self.image_sprite.image_load()
                elif self.flag == "L":
                    self.image_sprite.image_load(rotate_x=True)
            elif self.fly_up == False:
                self.jump_now = 0  
                self.double_jump = True     
        else:
            if self.image_sprite.Y < SCREEN_H - self.image_sprite.HEIGHT and self.fly_up == False and self.gravity:
                self.jump_now = 1
                self.image_sprite.Y += self.gravity_speed
                if self.flag == "R":
                    self.image_sprite.path = "image/Персонажи/Двойной_прижок/1.png"
                    self.image_sprite.image_load()
                elif self.flag == "L":
                    self.image_sprite.image_load(rotate_x=True)
            elif self.fly_up == False:
                self.jump_now = 0    
    # Гравитация колизия   
    def check_col_from_ab(self):
        for i in dict_list_border["list_border_cor"]:
            if i[-1] != "П" and i[-1] != "K":
                if i[-1] == "L":
                    i_rect = Rect(i[-2].X + i[-2].WIDTH//6,i[-2].Y ,i[-2].WIDTH - i[-2].WIDTH//3,1)
                    rect_sprite = Rect(self.image_sprite.X,self.image_sprite.Y,self.image_sprite.WIDTH,self.image_sprite.HEIGHT)
                    if Rect.colliderect(rect_sprite,i_rect) and self.move_up: 
                        self.gravity = False#гравитация отключается
                        self.image_sprite.Y = i[0] - self.image_sprite.HEIGHT
                        break
                    else:
                        self.gravity = True
                else:
                    if self.image_sprite.X + self.image_sprite.WIDTH >= i[4] + dict_argument["BLOCK_SIZE"]//5 and self.image_sprite.X <= i[5] - dict_argument["BLOCK_SIZE"]//5:
                        if self.image_sprite.Y + self.image_sprite.HEIGHT >= i[0]:
                            if self.image_sprite.Y + self.image_sprite.HEIGHT <= i[0] + self.gravity_speed*2:
                                self.gravity = False#гравитация отключается
                                self.image_sprite.Y = i[0] - self.image_sprite.HEIGHT
                                
                                break
                            else:
                                self.gravity = True
                        else:
                            self.gravity = True
                    else:
                        self.gravity = True
        if self.gravity == True:
            for i in dict_list_border["list_border_cor_cracking"]:  
                if self.image_sprite.X + self.image_sprite.WIDTH >= i[4] + dict_argument["BLOCK_SIZE"]//5 and self.image_sprite.X <= i[5] - dict_argument["BLOCK_SIZE"]//5:
                    if self.image_sprite.Y + self.image_sprite.HEIGHT >= i[0]:
                        if self.image_sprite.Y + self.image_sprite.HEIGHT <= i[0] + self.gravity_speed*2:
                            self.gravity = False#гравитация отключается
                            self.image_sprite.Y = i[0] - self.image_sprite.HEIGHT
                            break
                        else:
                            self.gravity = True
                    else:
                        self.gravity = True
                else:
                    self.gravity = True
    # Проверка движения в лево
    def can_move_left(self):
        for i in dict_list_border["list_border_cor"]:                       
            if self.image_sprite.X - self.image_sprite.WIDTH//10 <= i[5] and self.image_sprite.X >= i[3] and self.image_sprite.Y  <= i[1] and self.image_sprite.Y + self.image_sprite.HEIGHT-self.image_sprite.HEIGHT//4 >= i[0]:
                self.move_left = False
                break
            else: 
                self.move_left = True

        if self.move_left == True:
            for i in dict_list_border["list_border_cor_spring"]:
                if self.image_sprite.X - self.image_sprite.WIDTH//10 <= i[5] and self.image_sprite.X >= i[3] and self.image_sprite.Y  <= i[1] and self.image_sprite.Y + self.image_sprite.HEIGHT-self.image_sprite.HEIGHT//4 >= i[0]:
                    self.move_left = False
                    break
                else: 
                    self.move_left = True
            else: 
                self.move_left = True
        if self.move_left == True:
            for i in dict_list_border["list_border_cor_cracking"]:
                if self.image_sprite.X - self.image_sprite.WIDTH//10 <= i[5] and self.image_sprite.X >= i[3] and self.image_sprite.Y  <= i[1] and self.image_sprite.Y + self.image_sprite.HEIGHT-self.image_sprite.HEIGHT//4 >= i[0]:
                    self.move_left = False
                    break
                else: 
                    self.move_left = True
    # Функция пружины
    def spring(self):
        if self.flag_spring > 0:
            self.flag_spring -= 1
        for i in dict_list_border["list_border_cor_spring"]:
            if i[-1] == "П": 
                
                rect = i[-2].RECT   
                rect = Rect(rect.x + rect.width//8,rect.y - rect.width//10,rect.width - rect.width//4,1)
                rect_sprite = Rect(self.image_sprite.X,self.image_sprite.Y,self.image_sprite.WIDTH,self.image_sprite.HEIGHT)
                if Rect.colliderect(rect_sprite,rect) and not i[-2].HEIGHT < i[-2].start_height//2: 
                    i[-2].HEIGHT -= SCREEN_H//280
                    i[-2].Y += SCREEN_H//280
                    i[0] += SCREEN_H//280
                    i[-2].image_load()
                    self.gravity = False
                    self.image_sprite.Y = i[0] - self.image_sprite.HEIGHT
                    
                if i[-2].HEIGHT < i[-2].start_height//2:
                    i[-2].Y = i[-2].start_y - i[-2].start_height /2
                    i[0] = i[-2].start_y - i[-2].HEIGHT
                    
                    i[-2].HEIGHT = i[-2].start_height *1.5
                    
                    i[-2].image_load()
                    self.flag_spring = 5
                    if Rect.colliderect(rect_sprite,rect):
                        self.fly_up_spring = True
                    
                elif i[-2].HEIGHT > i[-2].start_height:
                    if self.flag_spring != 0:
                        i[-2].Y = i[-2].start_y - i[-2].HEIGHT//(6-self.flag_spring)
                        i[0] = i[-2].start_y - i[-2].HEIGHT//(6-self.flag_spring)
                        i[-2].HEIGHT = i[-2].start_height + i[-2].HEIGHT//(6-self.flag_spring)

                    if self.flag_spring == 0:
                        i[-2].Y = i[-2].start_y
                        i[0] = i[-2].start_y
                        i[-2].HEIGHT = i[-2].start_height


                    i[-2].image_load()
            
                
                    
                
        if self.fly_up_spring:
            if self.flag == "R":
                self.image_sprite.path = "image/Персонажи/Двойной_прижок/1.png"
                self.image_sprite.image_load()
            elif self.flag == "L":
                self.image_sprite.image_load(rotate_x=True)
            self.image_sprite.Y -= (self.jummp_boost//8 + self.gravity_speed)
            self.count += 1
            if self.move_up == False or self.count == 10 or self.image_sprite.Y <= SCREEN_W//80:
                self.fly_up_spring = False
                self.count = 0            
    # Проверка движения в право    
    def can_move_right(self):
        for i in dict_list_border["list_border_cor"]:                                                 
            if self.image_sprite.X <= i[3] and self.image_sprite.X  + self.image_sprite.WIDTH + self.image_sprite.WIDTH//10 >= i[4] and self.image_sprite.Y  <= i[1] and self.image_sprite.Y + self.image_sprite.HEIGHT - self.image_sprite.HEIGHT//4 >= i[0]:
                self.move_right = False 
                break
            else: 
                self.move_right = True  
        if self.move_right == True:
            for i in dict_list_border["list_border_cor_spring"]:
                if self.image_sprite.X <= i[3] and self.image_sprite.X  + self.image_sprite.WIDTH + self.image_sprite.WIDTH//10 >= i[4] and self.image_sprite.Y  <= i[1] and self.image_sprite.Y + self.image_sprite.HEIGHT - self.image_sprite.HEIGHT//4 >= i[0]:
                    self.move_right = False 
                    break
                else: 
                    self.move_right = True   
            
        if self.move_right == True:
            for i in dict_list_border["list_border_cor_cracking"]:
                if self.image_sprite.X <= i[3] and self.image_sprite.X  + self.image_sprite.WIDTH + self.image_sprite.WIDTH//10 >= i[4] and self.image_sprite.Y  <= i[1] and self.image_sprite.Y + self.image_sprite.HEIGHT - self.image_sprite.HEIGHT//4 >= i[0]:
                    self.move_right = False 
                    break
                else: 
                    self.move_right = True   
    # Проверка движения в верх
    def can_move_up(self):
        for i in dict_list_border["list_border_cor"]:
            if i[-1] != "K":
                i_rect = Rect(i[4]+ dict_argument["BLOCK_SIZE"]//5,i[1] + SCREEN_H//500,i[5]-i[4]- dict_argument["BLOCK_SIZE"]//2.5,1)
                rect_sprite = Rect(self.image_sprite.X,self.image_sprite.Y,self.image_sprite.WIDTH,self.image_sprite.HEIGHT)
                if Rect.colliderect(rect_sprite,i_rect): 
                    self.move_up = False
                    break
                else:
                    self.move_up = True
            else:
                self.move_up = True
        if self.move_up == True:
            for i in dict_list_border["list_border_cor_cracking"]:
                i_rect = Rect(i[4]+ dict_argument["BLOCK_SIZE"]//5,i[1] + SCREEN_H//500,i[5]-i[4]- dict_argument["BLOCK_SIZE"]//2.5,1)
                rect_sprite = Rect(self.image_sprite.X,self.image_sprite.Y,self.image_sprite.WIDTH,self.image_sprite.HEIGHT)
                if Rect.colliderect(rect_sprite,i_rect): 
                    self.move_up = False
                    break
                else:
                    self.move_up = True

        if self.move_up == True:
              for i in dict_list_border["list_border_cor_spring"]:
                if i[-1] != "K" and i[-1] != "D":
                    i_rect = Rect(i[4],i[1] + SCREEN_H//500,i[5]-i[4],1)
                    rect_sprite = Rect(self.image_sprite.X,self.image_sprite.Y,self.image_sprite.WIDTH,self.image_sprite.HEIGHT)
                    if Rect.colliderect(rect_sprite,i_rect): 
                        self.move_up = False
                        break
                    else:
                        self.move_up = True
                else:
                    self.move_up = True
    #  Функция смерти и спавна призрака   
    def Touch_of_death(self,rect,spike = False):
        if spike:
            rect = Rect(rect.x + rect.width//10,rect.y,rect.width - rect.width//5,rect.height)
        
        if Rect.colliderect(rect,self.image_sprite.RECT) and not dict_argument["ghost"] and (self.count_duration_shield <= dict_argument["duration_shield"] - 1) == False:
            dict_argument["ghost"] = True
            self.ghost_img.X = self.image_sprite.X
            
            self.can_move = False
            if self.image_sprite.Y <= SCREEN_H//2:
                self.ghost_img.Y = SCREEN_H - dict_argument["BLOCK_SIZE"]
            elif self.image_sprite.Y > SCREEN_H//2:
                self.ghost_img.Y = self.image_sprite.Y
    # Функция призрака
    def ghost(self,screen):
        if dict_argument["ghost"]:
            self.ghost_img.show_image(screen)
            if self.count_pressing_ghost == 10:
                self.count_duration_shield = dict_argument["duration_shield"] - 1
                dict_argument["ghost"] = False
                self.can_move = True
                self.count_pressing_ghost = 0 
            self.ghost_img.Y -= SCREEN_H//100
            if self.random_direction_ghost_number == "L":
                if self.ghost_img.X > 0 + SCREEN_H//200:
                    self.ghost_img.X -= SCREEN_H//200
            if self.random_direction_ghost_number == "R":
                if self.ghost_img.X + self.ghost_img.WIDTH + SCREEN_H//200 <= SCREEN_W:
                    self.ghost_img.X += SCREEN_H//200
            if self.ghost_img.Y <= - self.ghost_img.HEIGHT:
                dict_argument["ghost"] = False
                self.image_sprite.X = dict_spawn_and_finish_point["lvl"+str(dict_argument["index_lvl"]+1)+"_location_"+str(dict_argument["index_location"]+1)][0][0]
                self.image_sprite.Y = dict_spawn_and_finish_point["lvl"+str(dict_argument["index_lvl"]+1)+"_location_"+str(dict_argument["index_location"]+1)][0][1]
                self.count_pressing_ghost = 0 
                self.can_move = True
                self.count_duration_shield = 0
                dict_argument["screen_dimming_flag"] = "+"
                dict_argument["index_text_drimming"] = "dead"
                

            if self.random_direction_ghost_count[0] == self.random_direction_ghost_count[1]:
                self.random_direction_ghost_count[0] = 0 
                self.random_direction_ghost_number = random.choice([None,"R","L"])
            if self.change_img_ghost[0] == self.change_img_ghost[1]:
                
                self.change_img_ghost[0] = 0
                index_img = int(self.ghost_img.path.split("_")[-1].split(".")[0])
                if index_img == 12:
                    index_img = 1
                else:
                    index_img += 1
                self.ghost_img.path = "image/ghost_"+str(index_img)+".png"
                self.ghost_img.image_load()
            self.change_img_ghost[0] += 1
            self.random_direction_ghost_count[0] += 1
    # Щит
    def shield(self,screen):  
        if self.count_duration_shield == 0:
            self.count_duration_shield = dict_argument["duration_shield"]
        if self.count_duration_shield <= dict_argument["duration_shield"] - 1: 
            self.count_duration_shield -= 1 
            self.shield_img.X = self.image_sprite.X - self.image_sprite.WIDTH * 0.34
            self.shield_img.Y = self.image_sprite.Y - self.image_sprite.HEIGHT* 0.25
            
            self.shield_img.HEIGHT = self.image_sprite.HEIGHT * 1.50    
            if self.flag == "R":
                self.shield_img.image_load(rotate_x = True)
            else:
                self.shield_img.image_load()
            self.shield_img.show_image(screen)
    # Функция для вервки            
    def Hook(self,rect):
        keys = key.get_pressed() 
        if self.flag_hook < 20:
            self.flag_hook += 1
        if Rect.colliderect(rect,self.image_sprite.RECT) and self.flag_hook == 20 and not keys[self.List_layout[self.index_layout][3]]:
            self.image_sprite.X = rect.x-self.image_sprite.WIDTH//2+rect.width//2
            self.image_sprite.Y = rect.y-self.image_sprite.HEIGHT//2+rect.height//2
            self.image_sprite.RECT.x = rect.x-self.image_sprite.WIDTH//2+rect.width//2
            self.image_sprite.RECT.y = rect.y-self.image_sprite.HEIGHT//2+rect.height//2
            self.jump_now = 0
            self.flag_hook = 20
    # Функция для спрыгивания с вервки
    def hook(self,rect):
        keys = key.get_pressed() 
        if keys[self.List_layout[self.index_layout][2]]:
            if Rect.colliderect(rect,self.image_sprite.RECT):
                self.flag_hook = 0
    # Функция лесницы    
    def ladder(self):
        keys = key.get_pressed() 
        for l in dict_list_border["list_border_cor_ladder"]:
            rect_sprite = Rect(self.image_sprite.X,self.image_sprite.Y,self.image_sprite.WIDTH,self.image_sprite.HEIGHT)
            rect = l[-2].RECT
            rect = Rect(rect.x + rect.width/6.8,rect.y,rect.width/3.4,rect.height) 
            if Rect.colliderect(rect,rect_sprite):
                
                self.gravity = False
                self.flag_leader = True
                if keys[self.List_layout[self.index_layout][2]] and self.move_up:
                    self.image_sprite.Y -= SCREEN_H//100
                if keys[self.List_layout[self.index_layout][3]]:
                    self.image_sprite.Y += SCREEN_H//100
                break
            else:
                self.flag_leader = False
    # Функция ключа    
    def paper(self):
        for paper_obj in dict_list_border["list_border_cor_paper_and_door"]:
            if paper_obj[-2].RECT.colliderect(self.image_sprite.RECT):
                index_x = paper_obj[4] // (paper_obj[5] - paper_obj[4])
                index_y = paper_obj[0] // (paper_obj[1] - paper_obj[0])
                if not [index_x,index_y] in self.collected_paper:
                    self.collected_paper.append([index_x,index_y])
                dict_argument["list_surface"][index_y][index_x] = "0"
                return "paper_true"

    # Функция колизии с финишом 
    def finish_lvl(self,shooting_lvl,Fon,move_cloud,book):
        index_lvl = dict_argument["index_lvl"]
        index_location = dict_argument["index_location"]
        
        if index_lvl == 1:
            if index_location == 1:
                if dict_spawn_and_finish_point["lvl2_location_2"][1][0] == Rect(0,0,0,0) and dict_spawn_and_finish_point["lvl2_location_2"][1][1] == Rect(0,0,0,0):
                    self.image_sprite.X = dict_spawn_and_finish_point["lvl2_location_3"][0][0]
                    self.image_sprite.start_x = dict_spawn_and_finish_point["lvl2_location_3"][0][0]
                    self.image_sprite.Y = dict_spawn_and_finish_point["lvl2_location_3"][0][1]
                    self.image_sprite.start_y = dict_spawn_and_finish_point["lvl2_location_3"][0][1]
                    list_NPC.clear()
                    
                    return "right"
                if Rect.colliderect(dict_spawn_and_finish_point["lvl2_location_2"][1][0],self.image_sprite.RECT):
                    bk = Graphic_elements(0,0,SCREEN_W,SCREEN_H,"image/room_1.png")
                    rect = Rect(SCREEN_W//1.47,SCREEN_H//2,SCREEN_W//16.78,SCREEN_H//10.5)
                    
                    run = True
                    while run:
                        Fon.show_image(screen)
                        move_cloud()
                        bk.show_image(screen)
                        for event1 in event.get():
                            if event1.type == MOUSEBUTTONDOWN:
                                if Rect.collidepoint(rect,mouse.get_pos()[0],mouse.get_pos()[1]):
                                    dict_argument["flag_book"] = True
                            if event1.type == QUIT:
                                dict_spawn_and_finish_point["lvl2_location_2"][1][0] = Rect(0,0,0,0)
                                run = False

                        if dict_argument["flag_book"]:
                            if not book():
                                dict_spawn_and_finish_point["lvl2_location_2"][1][0] = Rect(0,0,0,0)
                                run = False
                                
                            
                        
                        display.update()
                elif Rect.colliderect(dict_spawn_and_finish_point["lvl2_location_2"][1][1],self.image_sprite.RECT):
                    bk = Graphic_elements(0,0,SCREEN_W,SCREEN_H,"image/room_2.png")
                    rect = Rect(SCREEN_W//1.4,SCREEN_H//3.46,SCREEN_W//10.6,SCREEN_W//10.6)
                    picture_criminal = Graphic_elements(SCREEN_W//2 - dict_argument["BLOCK_SIZE"]*4,SCREEN_H//2 - dict_argument["BLOCK_SIZE"]*4,dict_argument["BLOCK_SIZE"]*8,dict_argument["BLOCK_SIZE"]*8,"image/Персонажи/Преступник/picture.png")
                    
                    while True:
                        Fon.show_image(screen)
                        move_cloud()
                        bk.show_image(screen)
                        for event1 in event.get():
                            if event1.type == MOUSEBUTTONDOWN:
                                if Rect.collidepoint(rect,mouse.get_pos()[0],mouse.get_pos()[1]):
                                    dict_argument["picture_flag"] = True
                            if event1.type == QUIT:
                                dict_spawn_and_finish_point["lvl2_location_2"][1][1] = Rect(0,0,0,0)
                                break
                        if dict_argument["picture_flag"]:
                            picture_criminal.show_image(screen)
                            dict_argument["picture_count"] -= 1
                            if dict_argument["picture_count"] <= 0:
                                dict_argument["picture_flag"] = False
                                dict_spawn_and_finish_point["lvl2_location_2"][1][1] = Rect(0,0,0,0)
                                break

                        display.update()
        
        if index_lvl == 0:
            key = "lvl1_location_"+str(index_location+1)
            key_next = "lvl1_location_"+str(index_location+2)
            if dict_spawn_and_finish_point[key][2] != None:
                if Rect.colliderect(dict_spawn_and_finish_point[key][1],self.image_sprite.RECT):
                    self.image_sprite.X = dict_spawn_and_finish_point[key_next][0][0]
                    self.image_sprite.start_x = dict_spawn_and_finish_point[key_next][0][0]
                    self.image_sprite.Y = dict_spawn_and_finish_point[key_next][0][1]
                    self.image_sprite.start_y = dict_spawn_and_finish_point[key_next][0][1]
                    return dict_spawn_and_finish_point[key][2]
            else:
                if Rect.colliderect(dict_spawn_and_finish_point[key][1],self.image_sprite.RECT):
                    flag_first_shooting_lvl_point = shooting_lvl(screen,100,20,False)
                    
                    while True:
                        
                        if flag_first_shooting_lvl_point >= 100:
                            break
                        
                        else:
                            print("У тебя не получилось пройти первый уровень вот тебе еще попытка")
                            flag_first_shooting_lvl_point = shooting_lvl(screen,100,20,False)
                    flag_second_shooting_lvl_point = shooting_lvl(screen,150,30,3)
                    while True:
                        
                        if flag_second_shooting_lvl_point >= 150:
                            break
                        
                        else:
                            print("У тебя не получилось пройти второй уровень вот тебе еще попытка")
                            flag_second_shooting_lvl_point = shooting_lvl(screen,150,30,3)
                    return "finish_lvl"
                
        return "False"
                    
        