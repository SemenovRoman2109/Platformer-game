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

class Music(Sounds):
    def __init__(self,path,volume):
        super().__init__(path=path,volume=volume)
        
    def load_music(self):
        pygame.mixer.music.load(os.path.join(os.path.abspath(__file__ + "/.."), self.path))
        pygame.mixer.music.set_volume(self.volume) 
    def music_play(self):
        if pygame.mixer.music.get_busy():
            return True
        if not pygame.mixer.music.get_busy():
            return False
    def play_music(self):
        pygame.mixer.music.play()
    def stop_music(self):
        pygame.mixer.music.stop()
    def unload_music(self):
       pygame.mixer.music.unload()
    def pause_music(self):
       pygame.mixer.music.pause()
    def unpause_music(self):
       pygame.mixer.music.unpause()