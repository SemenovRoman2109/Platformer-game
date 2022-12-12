import os #ипорт os 
from pygame import* # ипортирование pygame
#Класс для удобного отображения графических єлементов
class Graphic_elements(): 
    def __init__(self,x,y,width,height,path,name = 'name'): # Аргументы класса
        #Свойства класса
        self.X = x
        self.Y = y
        self.start_x = x
        self.start_y = y
        self.HEIGHT = height
        self.WIDTH = width
        self.start_height = height
        self.start_width = width
        self.NAME = name
        self.path = path
        
        if path != None:#
            self.image_load()#
            
        self.RECT = Rect(self.X,self.Y,self.WIDTH,self.HEIGHT) #
    #Метод для отображения картинки
    def show_image(self,screen_object):
        #переопределяем rect обект нашего елемента
        self.RECT = Rect(self.X,self.Y,self.WIDTH,self.HEIGHT)
        #Проверка картинки
        if self.path != None:
            #Отображаем елемент
            screen_object.blit(self.IMG, (self.X,self.Y))
    #Метод загрузки изображения
    def image_load(self,rotate_x = False,rotate_y = False):
        #Загружаем и задаем размеры и подключаем картинку
        self.IMG = os.path.join(os.path.abspath(__file__ + "/.."), self.path)
        self.IMG = image.load(self.IMG)
        self.IMG = transform.scale(self.IMG, (self.WIDTH,int(self.HEIGHT)))
        self.IMG = transform.flip(self.IMG,rotate_x,rotate_y)
    #Метод наведения мышкой на объект
    def check_mouse_cor(self,mouse_cor):
        #Условие наведения мышкой на объект
        if mouse_cor[0] > self.X and mouse_cor[0] < self.X + self.WIDTH and mouse_cor[1] > self.Y and mouse_cor[1] < self.Y + self.HEIGHT:
            return True

