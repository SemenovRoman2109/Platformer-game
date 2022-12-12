import pygame #Подключаем модуль pygame
import os #Подключает модуль os
# Создаем класс Sounds
class Sounds():
    def __init__(self, path, volume):
        self.path = path #Расположение файла звука
        self.volume = volume #Громкость
    def play_sound(self,index=0): #Включаем звук
        self.sound = pygame.mixer.Sound(os.path.join(os.path.abspath(__file__ + "/.."), self.path)) #Загружаем файл звука
        self.sound.set_volume(self.volume) #Ставим громкость
        self.sound.play(index) #Играет музыка
    def stop_sound(self): #Останавливает звук
        pygame.mixer.Sound.stop(self.sound) #Останавливаем звук