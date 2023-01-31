#R - пила на нитке
#H - крюк
#s - пила (ставить на клетку выКе чем нужно)
#l,L - двигающаяся платформа вверх вниз маленькая буква путь больКая сам а платформа
#P,p - двигающаяся платформа вправо влево маленькая буква путь больКая сам а платформа
#D - Дверь 
#Д - Дверь по кноке
#П - пружина
#K(руская) - Кипи не двиг
#К - Кипи 
#K(английская) - ключ
#b - блок
#c - трескающаясь платформа
#Л - лесница середина   л - лесница начало    ъ - лесница конец    Ъ -   Лесница конец начало
#I - невидимая платформа
#M - музыкальная пластинка

#Матрица для первой локации первого уровня
list_surface_lvl1_location_1 = [
    
                list('Л0000000000000000000'),
                list('Л0000000000000000000'),
                list('ъM000000000000000000'),
                list('bbb00000000000bbЪ000'),
                list('bbb00ccc00Д000000000'),
                list('00000000000000000000'),
                list('00000000000s00000cc0'),
                list('0000000PPpppppppp000'),
                list('00bbb000000000000000'),
                list('000000000000000шшшшш'),
                list('bbbbbbbbbbbbbbbbbbbb'),
                list('bbbbbbbbbbbbbbbbbbbb'),
]
#Матрица для второй локации первого уровня
list_surface_lvl1_location_2 = [
                list('00000000000000000000'),
                list('00000000000H0000M000'),
                list('00000000000000000000'),
                list('00000000000000000000'),
                list('00000cc0000000000bbb'),
                list('bbЪ00000000000000000'),
                list('00000000000000000000'),
                list('00000000000000000000'),
                list('000bb000000000000000'),
                list('00000000000000000000'),
                list('bbbbbbbbbbbbbbbbbbbb'),
                list('bbbbbbbbbbbbbbbbbbbb'),
]
#Матрица для третий локации первого уровня
list_surface_lvl1_location_3 = [
                list('000000b0000000000000'),
                list('000000b0000000000000'),
                list('000000b00000000000bb'),
                list('000000b0000000000000'),
                list('bb0L00bbЪ00c00000000'),
                list('000l00b000000000П000'),
                list('000l00b000000000b000'),
                list('000l00b0000000000000'),
                list('000l000000c000000000'),
                list('00000000000000000000'),
                list('bbbbbbbbbbbbbbbbbbbb'),
                list('bbbbbbbbbbbbbbbbbbbb'),
]
#Матрица для четвертой локации первого уровня
list_surface_lvl1_location_4 = [
                list('00000000000000000R00'),
                list('00000000000000000000'),
                list('00ppPPpppppb00000000'),
                list('bb000000000b00000000'),
                list('000cc000000b00000000'),
                list('00000000000bcc000000'),
                list('0000000cc00b00000лbb'),
                list('00000000000b00000Л00'),
                list('000bb000000b00000ъ00'),
                list('00000000000bM0000000'),
                list('bbbbbbbbbbbbbbbbbbbb'),
                list('bbbbbbbbbbbbbbbbbbbb'),
                
]
#Список локаций первого уровня
list_surface_lvl1 = [list_surface_lvl1_location_1,list_surface_lvl1_location_2,list_surface_lvl1_location_3,list_surface_lvl1_location_4]

#Матрица для первой локации второго уровня
# Б - бумажка

list_surface_lvl2_location_1 = [
                list('0000000000000000ЛБb00000000000'),
                list('0000000000000000Л0b00000000000'),
                list('Б000000000000000ъ0b00Б00000000'),
                list('bb0000000000000000b0КК00000000'),
                list('000000000cc000II00b0bbЪ0000000'),
                list('0000II00000000ККККb00000000000'),
                list('0000000000000лbbbbb00000000000'),
                list('0000000000000ъ0000b00000КК0000'),
                list('M00IIIIII000000000b00000bb0000'),
                list('БК0000000000000000b000000000II'),
                list('bb0000s00000000000b00000000000'),
                list('000PPpppppppp00000b00Т000000cc'),
                list('000000000000000000b00000000000'),
                list('00000000000000bb000000000bb000'),
                list('шшшшш0000000000000000000000000'),
                list('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'),
                list('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'),
]
#Матрица для второй локации второго уровня
list_surface_lvl2_location_2 = [
                list('0000000000000000000b000000000d'),
                list('0000000000000000000b0000000000'),  
                list('0000000000000000000b000000lIbb'),
                list('D000000000000000000b000000l000'),
                list('0000000000000000000b000000l00M'),
                list('bbpppPPp0000000I000b000000L000'),
                list('0000000000bbb00000I0000000l000'),
                list('000000000000000000000000000000'),
                list('0000000000000000лbbbb000000000'),
                list('0000000000000000ъ00b00000000П0'),
                list('0000000000000000000b0000000bbb'),
                list('0000000000000000000b0III000000'),
                list('0000000000IIII00000b0000000000'),
                list('00000bb000000000000b0000000000'),
                list('0000000шшшшшшшшшшшшbшшшшшшшшшш'),
                list('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'),
                list('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'),

]
#Матрица для третей локации второго уровня
list_surface_lvl2_location_3 = [
                list('00000000000000b000000000000000'),
                list('00000000000000b0N0000000000000'),
                list('У0000000000000bbbbbл000000000n'),
                list('bb0IIIII00l000b0000ъ00000cc0bb'),
                list('0000000000L000b00000000l000000'),
                list('0000000000l000b00000000l000000'),
                list('N000000000l00nb00000000L00000n'),
                list('bb00000000l0bbb000ККК00l0cc0bb'),
                list('00000КККК0l000b00Ъbbb000000000'),
                list('00000bbbb0l000b000000000000000'),
                list('00II0000000000b000000000000000'),
                list('00000000000000b000000000000000'),    
                list('00000000000000bb00000000000000'),
                list('000000000000000000000000000000'),
                list('0П00ККККККК0N00000G0шшшшшшшшшш'),    
                list('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'),
                list('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'),
]

list_surface_lvl2 = [list_surface_lvl2_location_1,list_surface_lvl2_location_2,list_surface_lvl2_location_3]
#Список уровней
list_surface = [list_surface_lvl1,list_surface_lvl2]

