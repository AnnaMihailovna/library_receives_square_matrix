import aiohttp
import logging
import asyncio
from asyncio import TimeoutError
from aiohttp import ClientError

logger = logging.getLogger()

SOURCE_URL = 'https://raw.githubusercontent.com/avito-tech/' \
             'python-trainee-assignment/main/matrix.txt'


async def get_text(url: str) -> str | None:
    """
    Получение текста с удалённого сервера async.

    Args:
        url (str): наш URL для получения данных.

    Returns:
        (str | None): матрица в виде строки.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if 400 <= resp.status < 500:
                    logger.error('Ошибка клиента')
                elif resp.status >= 500:
                    logger.error('Ошибка сервера')
                else:
                    return await resp.text()
    except ClientError as ex:
        logger.error(f'Есть проблемы с связью {ex}')
    except TimeoutError as ex:
        logger.error(f'Ошибка тайм-аута {ex}')


def prepare_matrix(text: str) -> list[list[int]]:
    """
    Подготовливает матрицу из необработанной строки
    в объект вложенного списка Python.

    Args:
        text (str): необраотанная строка,
        считанная из файла функцией get_text().

    Returns:
        list[list[int]]: подготовленная для обхода
        матрица.
    """
    try:
        matrix = []
        for line in text.split('\n'):
            if line and line[0] != '+':
                matrix.append([int(num) for num in line[1:-1].split('|')])
        # Проверка на то, что матрица квадратная
        if matrix and not all([len(matrix) == len(line) for line in matrix]):
                raise ValueError('Матрица не квадратная!')
    except ValueError as ex:
        logging.warning(ex)
        return []
    return matrix


def traverse_matrix(matrix: list[list[int]],
                    output: list[int] = None) -> list[int]:
    """
    Обход матрицы по спирали против часовой стрелка,
    начиная с верхнего левого элемента.

    Args:
        matrix (list[list[int]]): подготовленный для обхода
        объект матрицы.
        output (list[int], optional): переменная для
        рекурсивных запусков, изначально None.
    Returns:
        list[int]: список обхода матрицы в заданном порядке.
    """
    if output is None:
        output = []

    if not len(matrix):
        return output
    # разворачиваем внешний список, распаковываем, изпользуя zip
    # получаем список из нулевых элементов, список из первых элементов и т. д.
    matrix = list(zip(*matrix[::-1]))
    output.extend(matrix[0][::-1])
    traverse_matrix(matrix[1:], output)


async def get_matrix(url: str) -> list[int]:
    """
    Главная функция: получает url, преобразовывает
    матрицу, обрабатывает сетевые ошибки.

    Args:
        url (str): наш URL для получения данных.

    Returns:
        list[int]: список обхода матрицы по спирали
        против часовой стрелки, начиная с верхнего левого элемента.
    """
    output = []
    text = await get_text(url)
    traverse_matrix(prepare_matrix(text), output)
    return output

get_matrix = asyncio.run(get_matrix(SOURCE_URL))
print(get_matrix)
