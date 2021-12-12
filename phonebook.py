from pprint import pprint
import csv
import re


def split_str_by_space(str_to_split):
    '''Ф-ия разделяет строку на слова при наличии в ней пробелов.'''
    res = re.split(r' ', str_to_split)
    return res

def merge_notes(notes):
    '''Ф-ия принимает словарь списков и объединяет дублирующуюся инфо по фамилии и имени,
    при этом дубли из словаря удаляются.'''
    key1 = 1        #словарь начинается с ключа 1
    del_keys = []   #список для хранения ключей словаря, которые нужно будет удалить
    while key1 != len(notes.keys())+1:
        for key2 in range(key1+1, len(notes.keys())+1):
            #условие проверки наличия в словаре одинаковых фамилии и имени
            if notes[key1][0] == notes[key2][0] and notes[key1][1] == notes[key2][1]:
                #цикл объединяет дубли
                for i in range(7):
                    if notes[key1][i] == '':
                        notes[key1][i] += notes[key2][i]
                #запоминаем ключи-дубли, которые нужно будет удалить
                del_keys.append(key2)
        key1 += 1
    #удаление ключей-дублей
    for i in range(len(del_keys)):
        notes.pop(del_keys[i])
    return notes

with open("phonebook_raw.csv", encoding='utf-8', newline='') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

contacts_dict = {}
#цикл проходит по "внешнему" списку с данными за исключением 1-ого эл-та
for i in range(1, len(contacts_list)):
    flag = True
    j = 0
    #цикл проходит по первым трём эл-ам вложенного списка (ФИО) и форматирует их (Ф + И + О)
    while flag and j < 3:
        #условие наличия пробела в эл-те списка (если ФИО объединены)
        if contacts_list[i][j].find(' ') != -1:
            #str012 - строка, объединяющая ФИО
            str012_concat = f"{contacts_list[i][0]} {contacts_list[i][1]} {contacts_list[i][2]}"
            list_of_str012 = split_str_by_space(str012_concat)
            flag = False
            contacts_list[i][0] = list_of_str012[0]
            contacts_list[i][1] = list_of_str012[1]
            contacts_list[i][2] = list_of_str012[2]
        j += 1
    #формирование словаря для дальнейшей обработки
    contacts_dict[i] = contacts_list[i]

new_contacts_list = [contacts_list[0]]          #присвоение 1-ому элементу нового списка наименований полей
new_contacts_dict = merge_notes(contacts_dict)

#цикл формирует новый список
for key in new_contacts_dict:
    new_contacts_list.append(new_contacts_dict[key])

#шаблон для определения номеров телефона
pattern = r"(\+7|8)\s*" \
          r"(\()?(\d..)(\))?([-\s*])?" \
          r"(\d..)([-\s*])?" \
          r"(\d.)([-\s*])?" \
          r"(\d.)" \
          r"((\s*)((\()?(доб\.)\s*(\d+))(\))?)?"
#цикл форматирует телефонные номера под новый унифицированный шаблон
for i in range(1, len(new_contacts_list)):
    new_contacts_list[i][5] = re.sub(pattern, r"+7(\3)\6-\8-\10\12\15\16", new_contacts_list[i][5])


# код для записи файла в формате CSV
with open("phonebook.csv", "w") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(new_contacts_list)