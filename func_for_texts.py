import random


def read_and_del_articles(file_path, count, items):
    """Возвращает полученный текст и словарь с ключами в виде их позиции"""
    deleted_articles = {}
    text = []
    with open(file_path, mode="r", encoding='UTF-8') as file:
        file = file.read()
        file = file.split("\n")
        num = random.randint(1, len(file) - count)
        for i in range(num, num + count):
            part = file[i]
            if part not in text:
                text.append(part)
            else:
                part = random.choice(file)
                text.append(part)
    count_articles = 1
    end_version = []
    for part in text:
        text1 = part.split()
        for i in range(len(text1)):
            if text1[i] in items:
                deleted_articles[count_articles] = text1[i].lower()
                text1[i] = f"({count_articles})"
                count_articles += 1
        if " ".join(text1) not in end_version:
            end_version.append(" ".join(text1))

    if "\n".join(end_version):
        return "\n".join(end_version), deleted_articles
    else:
        return read_and_del_articles(file_path, count)
