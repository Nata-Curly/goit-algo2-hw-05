from bloomfilter import BloomFilter


def check_password_uniqueness(bloom: BloomFilter, passwords: list) -> dict:
    """
    Перевіряє, чи є паролі унікальними за допомогою буферу Блума.

    :param bloom: буфер Блума
    :param passwords: список паролів
    :return: словник з результатами перевірки, де ключ - пароль, а значення - один з наступних:
        - "некоректне значення" - якщо пароль не є строкою, або якщо строка порожня
        - "вже використаний" - якщо пароль вже є в буфері
        - "унікальний" - якщо пароль є унікальним
    """
    if not isinstance(passwords, list):
        raise TypeError("Паролі мають бути списком")

    result = {}
    for password in passwords:
        if not isinstance(password, str) or password.strip() == "":
            result[str(password)] = "некоректне значення"
        elif bloom.contains(password):
            result[password] = "вже використаний"
        else:
            result[password] = "унікальний"
            bloom.add(password)
    return result


if __name__ == "__main__":
    # Ініціалізація фільтра Блума
    bloom = BloomFilter(size=1000, num_hashes=3)

    # Додавання існуючих паролів
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    # Перевірка нових паролів
    new_passwords_to_check = [
        "password123",
        "newpassword",
        "admin123",
        "guest",
        "",
        None,
        123,
    ]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Виведення результатів
    for password, status in results.items():
        print(f"Пароль '{password}' — {status}.")
