#Подключаем подготовленные модули нашего проекта#
from pygame import* 
import random
import json
import copy
import os
#Подключаем модули нашего проекта
from surface import *
init() #Инициализируем pygame
#Настраиваем разрешение и ограничение кадров
with open(os.path.join(os.path.abspath(__file__ + "/.."),'saves/config.json'),'r') as file:
    config = json.load(file)

if config["FULLSCREEN"]:
    SCREEN_W = display.Info().current_w
    SCREEN_H = display.Info().current_h
else:    
    SCREEN_W = int(config["SCREEN_WIDTH"])
    SCREEN_H = int(config["SCREEN_HEIGHT"])
MUSIC_VOLUME = int(config["MUSIC_VOLUME"])
SOUNDS_VOLUME = int(config["SOUNDS_VOLUME"])

#Индексы уровней
index_lvl = 0
index_location = 0


FPS = 30


#Создаем список контуров
list_border_cor_cracking = list()
list_border_cor_paper_and_door = list()
list_border_cor_saw = list()
list_border_cor_ladder = list()
list_border_cor_spring = list()
list_border_cor = list()
list_NPC = list()
list_index_NPC = list()
list_flag = list()#временный список,где будут хранится координаты
list_noot_colision_platphorm = list()

#Считаем птицу (beard в переводе - борода)
max_number_beard = random.randint(500,1000)
count_beard = 0
flag_collid_npc = False
index_npc_collid = None
number_click_npc = 0
flag_false_criminal_selected = False
#Список верёвок (анимация)
list_cor_Rope = [
    [-SCREEN_W//5.28,-SCREEN_H//5.10],
    [-SCREEN_W//5.61,-SCREEN_H//5.93],
    [-SCREEN_W//6,-SCREEN_H//7.14],
    [-SCREEN_W//6.49,-SCREEN_H//8.75],
    [-SCREEN_W//7.19,-SCREEN_H//11.1],
    [-SCREEN_W//8,-SCREEN_H//14.28],
    [-SCREEN_W//9.20,-SCREEN_H//20],
    [-SCREEN_W//11.13,-SCREEN_H//28],
    [-SCREEN_W//13.61,-SCREEN_H//41.17],
    [-SCREEN_W//18.02,-SCREEN_H//70],
    [-SCREEN_W//19.10,-SCREEN_H//140],
    [-SCREEN_W//60.95,-SCREEN_H//233.33],
    [0,0],
    [SCREEN_W//60.95,-SCREEN_H//233.33],
    [SCREEN_W//19.10,-SCREEN_H//140],
    [SCREEN_W//18.02,-SCREEN_H//70],
    [SCREEN_W//13.61,-SCREEN_H//41.17],
    [SCREEN_W//11.13,-SCREEN_H//28],
    [SCREEN_W//9.20,-SCREEN_H//20],
    [SCREEN_W//8,-SCREEN_H//14.28],
    [SCREEN_W//7.19,-SCREEN_H//11.1],
    [SCREEN_W//6.49,-SCREEN_H//8.75],
    [SCREEN_W//6,-SCREEN_H//7.14],
    [SCREEN_W//5.61,-SCREEN_H//5.93],
    [SCREEN_W//5.28,-SCREEN_H//5.10],
]
#Задаем разрешение и ограничение кадров. Настраиваем название окна
screen = display.set_mode((SCREEN_W, SCREEN_H))
display.set_caption("platformer_game")
clock = time.Clock()        

#Список пилы, верёвок и так далее
list_saw = []
list_hook = []
list_Rope_with_saw = []

#Список шипов вышедших за карту
list_spikes_outside = []

#Словарь аргументов блоков
dict_argument_block = {
    "flag_move_cloud": 1,
    "count_motion_block": 0,
    "count_spinning_motion_block":0,
    "count_img_spinning_motion_block":1,
    "flag_direction_spinning_motion_block":"+",
    "flag_load": 0,
    "count_load": 24,
    "count_spike":0,
    "direction_spike":"U",
    
}
dict_spawn_and_finish_point = {
    "lvl1_location_1":[[SCREEN_W//80,SCREEN_H-SCREEN_H//10*2.5],Rect(0,-SCREEN_W/40,round(SCREEN_W/20),1),"up"],
    "lvl1_location_2":[[SCREEN_W//80,SCREEN_H-SCREEN_H//10*2.5],Rect(SCREEN_W-SCREEN_W//80,SCREEN_H//5.53,1,SCREEN_H//5.53),"right"],
    "lvl1_location_3":[[SCREEN_W//80,SCREEN_H//5.5],Rect(SCREEN_W-SCREEN_W//80,SCREEN_H//45,1,SCREEN_H//6.31),"right"],
    "lvl1_location_4":[[SCREEN_W//80,SCREEN_H-SCREEN_H//10*2.5],Rect(SCREEN_W-SCREEN_W//80,SCREEN_H//2.48,1,SCREEN_H//7.2),None],
    "lvl2_location_1":[[round(SCREEN_W/30)*18,SCREEN_H-round(SCREEN_W/30)*3.5],Rect(0,0,0,0),"right"],
    "lvl2_location_2":[[SCREEN_W//80,SCREEN_H-round(SCREEN_W/30)*3.5],[Rect(SCREEN_W//80,round(SCREEN_W/30)*4,round(SCREEN_W/30),round(SCREEN_W/30)*1.8),Rect(SCREEN_W-round(SCREEN_W/30),0,round(SCREEN_W/30),round(SCREEN_W/30)*1.8)],"right"],
    "lvl2_location_3":[[round(SCREEN_W/30)*14,SCREEN_H-round(SCREEN_W/30)*3.5],Rect(0,0,0,0),None],
}
dict_achievement_boling = {
    "stay_in_body":False,# ГОТОВООООООО
    "and_where_is_ammunition":False,# ГОТОВООООООО
    "criminal_hit":False,# ГОТОВООООООО
    "it_was_close_but_he_flew_away":False,# ГОТОВООООООО
    "how_many_times_did_you_revive":False,# ГОТОВООООООО
    "walking_dead":False,# ГОТОВООООООО
    "direct_hit":False,# ГОТОВООООООО
    "newbie":False,# ГОТОВООООООО
    "godlike":False,# ГОТОВООООООО
    "music_player":False,# ГОТОВООООООО
    "goose":False,# ГОТОВООООООО
    "sniper":False,# ГОТОВООООООО
    "barrier":False,# ГОТОВООООООО
    "puzzle_lower":False,# ГОТОВООООООО
    "cracker":False,# ГОТОВООООООО
    "piferer":False,# ГОТОВООООООО
    "record_holder":False,# ГОТОВООООООО
    "detective":False,# ГОТОВООООООО
    "where_is_the_sound":False,# ГОТОВООООООО
    "platinum":False,# ГОТОВООООООО
}
dict_laungues_achievement = {
    "stay_in_body":[{"ua":"Залишайтеся в тілі","uk":"Stay in body"},
                    {"ua":"Пройти гру не разу не померши","uk":"Complete the game without dying"}],
    "and_where_is_ammunition":[{"ua":"А де боєприпаси?","uk":"And where is ammunition?"},
                               {"ua":"Витратити всі набої не влучивши в жоден манекен","uk":"Spend all your ammo without hitting more than one dummy"}],
    "criminal_hit":[{"ua":"Злочинне влучення","uk":"Criminal hit"},
                    {"ua":"Влучити в голову злочинця","uk":"Shoot the criminal in the head"}],
    "it_was_close_but_he_flew_away":[{"ua":"Було близько, але він вiдлетів","uk":"It was close but he flew away"},
                                     {"ua":"Привид полетів коли залишилося одне натискання на нього","uk":"The ghost flew away when there was one click left on it."}],
    "how_many_times_did_you_revive":[{"ua":"Скільки разів відродився?","uk":"How many times have you been revived?"},
                                     {"ua":"П'ять разів відродитись","uk":"be reborn five times"}],
    "walking_dead":[{"ua":"Ходячі мерці","uk":"Walking dead"},
                    {"ua":"Десять разів померти","uk":"Die ten times"}],
    "direct_hit":[{"ua":"Пряме влучення","uk":"Direct hit"},
                  {"ua":"Жодного разу не промазати на стрільбі по манекенах","uk":"Never get smacked on shooting dummies"}],
    "newbie":[{"ua":"Новачок","uk":"Newbie"},
              {"ua":"Десять разів померти на легкій складності","uk":"Die ten times on easy difficulty"}],
    "godlike":[{"ua":"Богоподібний","uk":"Godlike"},
               {"ua":"Пройти гру жодного разу не померши на складній складності","uk":"Complete the game without dying on hard difficulty"}],
    "music_player":[{"ua":"Любитель музики","uk":"Musician"},
                    {"ua":"Зібрати всі платівки","uk":"Collect all records"}],
    "goose":[{"ua":"Гусак","uk":"Goose"},
             {"ua":"Провести п'ятнадцять секунд у присіді без перерви","uk":"Spend fifteen seconds in a squat without a break"}],
    "sniper":[{"ua":"Снайпер","uk":"Sniper"},
              {"ua":"П'ять разів потрапити в голову манекена","uk":"Hit the head of a mannequin five times"}],
    "barrier":[{"ua":"Перешкода","uk":"Barrier"},
               {"ua":"П'ять разів потрапити у перешкоду","uk":"Hit the barrier five times"}],
    "puzzle_lower":[{"ua":"Любитель пазлів","uk":"Puzzle lover"},
                    {"ua":"Зібрати пазл за п'ять секунд","uk":"Solve the puzzle in five seconds"}],
    "cracker":[{"ua":"Зломщик","uk":"Cracker"},
               {"ua":"Відкрити сейф за двадцять п'ять секунд","uk":"Open the safe in twenty-five seconds"}],
    "piferer":[{"ua":"Злодюжка","uk":"Thief"},
               {"ua":"Помилитися у відкритті сейфа на легкiй складностi","uk":"Make a mistake opening the safe on easy difficulty"}],
    "record_holder":[{"ua":"Рекордсмен","uk":"Record holder"},
                     {"ua":"Пройти двадцять рівнів у флаппі берд","uk":"Complete twenty levels in a flappy bird"}],
    "detective":[{"ua":"Детектив","uk":"Detective"},
                 {"ua":"Виявити злочинця з першої спроби","uk":"Find the culprit on the first try"}],
    "where_is_the_sound":[{"ua":"Де звук?","uk":"Where is the sound?"},
                          {"ua":"Грати з повністю вимкненим звуком","uk":"Play with the sound completely muted"}],
    "platinum":[{"ua":"Платина","uk":"Platinum"},
               {"ua":"Отримати всі досягнення у грі","uk":"Get all the achievements in the game"}]
}

with open(os.path.join(os.path.abspath(__file__ + "/.."),'saves/achievement.json'),'r') as file:
    dict_achievement_boling = json.load(file)
# 

with open(os.path.join(os.path.abspath(__file__ + "/.."),'saves/saves.json'),'r') as file:
    dict_argument = json.load(file)

if dict_argument["defolt"] != "true":
    if dict_argument["index_lvl"] == 0:
        BLOCK_SIZE = round(SCREEN_W/20)
    if dict_argument["index_lvl"] == 1:
        BLOCK_SIZE = round(SCREEN_W/30)
else:
    BLOCK_SIZE = round(SCREEN_W/20)
if dict_argument["defolt"] == "true":
    #Словарь аргументов
    dict_argument = {
        "defolt":"False",
        "ghost": False, 
        "ded": True,    
        "game": True,
        "scene":"complexity",
        "list_flag_achievement":[],
        "count_dead":0,
        "count_reborn":0,
        "full_surface":list_surface,
        "list_surface":list_surface[index_lvl][index_location],
        "max_number_beard":max_number_beard,
        "count_beard":count_beard,
        "list_beard":list(),
        "index_lvl":index_lvl,
        "index_location":index_location,
        "X_MAP":0,
        "Y_MAP":0,
        "dict_argument":0,
        "duration_shield":100,
        "list_spikes_outside":list_spikes_outside,
        "screen_dimming_flag": "+",
        "screen_dimming_count": 0,
        "index_text_drimming":"first_entry_into_the_game",
        "flag_puzzle_location":False,
        "count_final_puzzle":None,
        "count_animation_book":0,
        "flag_book":False,
        "picture_flag":False,
        "picture_count":150,
        "flag_colision_game_machine":False,
        "index_music":0,
        "flag_pause":False,
        "BLOCK_SIZE":BLOCK_SIZE,
        "flag_collid_npc":flag_collid_npc,
        "number_click_npc":number_click_npc,
        "flag_false_criminal_selected":flag_false_criminal_selected,
        "index_npc_collid":index_npc_collid,
        "sprite_x":(dict_spawn_and_finish_point["lvl"+str(index_lvl+1)+"_location_"+str(index_location+1)][0][0])//BLOCK_SIZE,
        "sprite_y":(dict_spawn_and_finish_point["lvl"+str(index_lvl+1)+"_location_"+str(index_location+1)][0][1])//BLOCK_SIZE,
        "count_change_bg":0,
        "complexity":None,
        "list_flag_room":[False,False],
        "record_flappy_bird":0,
        "count_music":2,
        # настройки на средней сложности
        "DOUBLE_JUMP":None,
        "max_count_spike":150,
        "criminal_speed":SCREEN_W//250,
        "speed_safe":45,    
        "duration_invisible_block":12,
        "count_point_hit":100,    
        "count_fences":3,
        "count_ammo":20,
        "duration_door":100,
        "count_click_on_ghost":10,
        "max_count_motion_block": 7,
        "speed_transparency_broken_platforms":20,
    }

dict_argument["BLOCK_SIZE"] = BLOCK_SIZE
#Словарь аргументов ангелов
dict_argument_angle = {
    "angle_saw":0,
    "angle_Rope_with_saw":-60,
    "angle_Rope_with_saw_direction":"R",
    "index_Rope_with_saw":0,
    "angle_Hook":-60,
    "angle_Hook_direction":"R",
    "index_Hook":0
}
#Словарь списков контуров
dict_list_border = {
    "list_border_cor_cracking":list_border_cor_cracking,
    "list_border_cor_paper_and_door":list_border_cor_paper_and_door,
    "list_border_cor_ladder":list_border_cor_ladder,
    "list_border_cor_spring":list_border_cor_spring,
    "list_border_cor":list_border_cor,
    "list_flag":list_flag
}
dict_languages_mission = {
    "1":{"ua":["Ви приїхали на місце злочину"," знайдіть зачіпки ",""," Натисніть кнопку [F] "," щоб з'явилися нові платформи "],"uk":["You have arrived", "at the scene of the crime","find the clues","","Press the [F] button ","for new platforms to appear"]},
    "2":{"ua":["Ви приїхали в будинок до вбивці", "огляньте всі кімнати"],"uk":["You have arrived at the killer's houke", "look around all the rooms"]},
    "3":{"ua":["Ви приїхали на рейс до вбивці", "Дізнайтеся хто вбивця", "Вбивця міг змінити свою зовнішність"],"uk":["You're on a flight to see a killer","Find out who the killer is","The killer could have", "changed his appearance"]}
}

dict_mision_lvl_1 = {
    "location_0":dict_languages_mission["1"][config["language"]],
    "location_1":dict_languages_mission["2"][config["language"]],
    "location_2":dict_languages_mission["3"][config["language"]],
}
# Добавить перед последней стрельбой текст : Вы правельно нашли преступника но он начал убегать вам хватит одного попадания в голову или 2-ух в тело
dict_languages_drimming = {
    "1":{"ua":["Ви не змогли утримати свою душу","повертайтеся на початок рівня"],"uk":["You couldn't hold your soul", "go back to the beginning of the level"]},
    "2":{'ua':["Преступнику вдалося скрити","Ви програли"],'uk':["The killer managed to escape", "You lost"]},
    "3":{'ua':["Вам вдалося затримати злочинця", "Ви пройшли гру"],"uk":["You managed to apprehend the killer", "You completed the game"]},
    "4":{"ua":["Ви правильно вибрали злочинця","І він почав тікати підстреліть його"],"uk":["You chose the right criminal","And he started to run away, shoot him"]},
    "5":{'ua':["Ви вибрали неправильно", "У тебе залишилася одна спроба", "до рейсу"],"uk":["You chose wrong","You have one try left","until the flight"]},
    "6":{'ua':["Ви не пройшли академію", "спробуйте ще раз"],"uk":["You didn't pass the academy", "try again"]},
    "7":{"ua":["Ви померли під час розкриття справи","спробуйте ще раз"],"uk":["You died while solving the case", "try again"]},
    "8":{'ua':["Ви прибули до поліцейської академії", "Пройдіть навчання", "щоб переступити до роботи"],'uk':["You have arrived", "at the police academy", "Get your training to go to work"]},
    "9":{"ua":["Ви практично закінчили", "навчання в академії"," залишилося перевірити вашу влучність "],"uk":["You are almost done","training at the academy","to test your marksmanship"]},
    "10":{'ua':["Ви пройшли перший рівень стрілянини","наступний буде складніше"],"uk":["You have passed", "the first shooting level", "the next one will be harder"]},
    "11":{'ua':["У тебе не вийшло пройти рівень ","Спробуй знову"],"uk":["You failed the level ","Try again"]}
}

dict_text_drimming = {
    "dead":dict_languages_drimming["1"][config["language"]],
    "lose_game":dict_languages_drimming["2"][config["language"]],
    "win_game" :dict_languages_drimming["3"][config["language"]],
    "drive":dict_languages_drimming["4"][config["language"]],
    "incorrectly_selected_criminal":dict_languages_drimming["5"][config["language"]],
    "lose_all_hp_0":dict_languages_drimming["6"][config["language"]],
    "lose_all_hp_1":dict_languages_drimming["7"][config["language"]],
    "first_entry_into_the_game":dict_languages_drimming["8"][config["language"]],
    "first_shooting" :dict_languages_drimming["9"][config["language"]],
    "second_shooting":dict_languages_drimming["10"][config["language"]],
    "lose_shooting":dict_languages_drimming["11"][config["language"]]
}


dict_languages_settings = {
    "1":{"ua":"Гучність звуку:","uk":"Volume Sound:"},
    "2":{'ua':'Гучність музики:','uk':'Volume Music:'},
    "3":{'ua':"Розкладка клавіатури:","uk":"Keyboard Control:"},
    "4":{'ua':"Здатність:","uk":"Resolution:"},
    "5":{'ua':["Використовувати","Вгору","Пригнутися","Вліво","Вправо"],"uk":["Use","Jump","Crawl","Left","Right"]},
    "6":{'ua':"Повноекранний режим:",'uk':"Full Screen:"},
    "7":{"ua":"Так","uk":"Yes"},
    "8":{'ua':"Ні","uk":'No'},
    "9":{'ua':"Виберіть категорію ;у якій хочете внести зміну;;Зміни вступлять у гру;після натискання на кнопку Назад","uk":"Select the category ;in which you want to make a change;;Changes will come into play;after clicking on the Back button"},
    "10":{"ua":"Мова:","uk":"language:"},
}
dict_languages_book = {
    "1":{"ua":"Сьогодні я зроблю;;свою останню справу;;після якої я влечу;;до себе на батьківщину;;Нарешті я побачу;;свою дочку;;у неї через 3 міцяться;;день народженя. ","uk":"Today I will do;;my last thing;;after which I drag;;to my homeland;;Finally I will see;;my daughter;;her birthday will change in 3."},
    "2":{"ua":"Вона напевно скучила;;за мною.","uk":"She mukt have;;missed me."},
}

dict_laungues_safe = {
    'ua':["Натисніть кнопку ["+str(config["list_text_button_control"][0])+"]"," щоб зупинити"],
    "uk":["Press button ["+str(config["list_text_button_control"][0])+"]"," to stop"]

}
dict_laungues_criminal = {
    'ua':"Він злочинець?",
    "uk":"Is he a criminal?"
}
dict_direction_door = dict()
#Словари аргументов и ломания платформ
broken_cracking_platform = dict()
dict_argument_door_block = dict()
dict_directory_motion_block_up_down = dict()
dict_directory_motion_block_left_right = dict()