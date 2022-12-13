#ипортируем модули 
import pygame
import os
#инициализировать модуль шрифта
pygame.font.init()
#Класс для удобного отображения text
class Font():
    def __init__(self,font_path,font_size,font_color,font_content,font_x,font_y,index,bold = True):#
        #Свойства класса
        self.font_path = os.path.join(os.path.abspath(__file__+'/..'),font_path)
        
        self.font_size = font_size
        self.font_color = font_color
        self.font_content = font_content
        self.start_content = self.font_content
        self.font_x = font_x
        self.bold = bold
        self.font_y = font_y
        self.start_y = self.font_y
        if self.font_content != None and index != 1:
            self.font_content = self.font_content.split(';')
        self.font_content = [self.font_content]
        self.index = len(self.font_content)
    #Метод для отображения show_text 
    def show_text(self,win):
        # Цикл чтоб разделить текст на столько строк, чему равно значение index.
        for i in range(len(self.font_content)):
            #создает обект текста 
            self.font = pygame.font.Font(self.font_path,self.font_size)
            #задает тексту жирность
            pygame.font.Font.set_bold(self.font,self.bold)
            #загружаем текст
            self.font = self.font.render(str(self.font_content[i]),True,self.font_color)
            #Отображаем елемент
            win.blit(self.font,(self.font_x,self.font_y))
            #Перемещаем текст на строчку вниз
            self.font_y += self.font_size
        # Перемещаем текст обратно на первую строку
        self.font_y = self.start_y