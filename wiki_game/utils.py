ONE_MINUTE = 60
ONE_HOUR = ONE_MINUTE * 60


def format_duration(seconds: float) -> str:
    """
    Форматирует продолжительность в удобный формат (секунды, минуты, часы).
    """

    if seconds < ONE_MINUTE:
        return f"{int(seconds)} секунд"
    if seconds < ONE_HOUR:
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes} минут {seconds} секунд"
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours} часов {minutes} минут {seconds} секунд"
