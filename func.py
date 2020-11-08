"""Функции для файла new_user"""


def isalphadidgit(string):
    return string.isalpha() or string.isdigit()


def check_letter(string):
    abc = "qwertyuiopasdfghjklzxcvbnm-1234567890"
    for i in string:
        if i not in abc:
            return False
    return True


def empty_or_not(login, password, name):
    if not login:
        return "login"
    elif not password:
        return "пароль"
    elif not name:
        return "имя"
    return '1'


"""-------------------------------------"""
"""общие функции"""


def verify_password(password):
    """Проверки пароля, более 8-ми символов и состоящая из букв и цифр, и только из латиницы"""
    if len(password) <= 8:
        return "Пароль должен быть более восьми символов"
    if isalphadidgit(password):
        return "Пароль должен включать и буквы, и цифры"
    if not check_letter(password):
        return "Пароль должен включать только буквы латинского алфавита и '-"
    return "1"



"""Функции для файла change_password"""


def isempty(password, login):
    if not login:
        return "login"
    elif not password:
        return "новый пароль"
    return "1"
