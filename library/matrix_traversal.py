import aiohttp
import logging
import asyncio

logger = logging.getLogger()

async def get_text(url: str) -> str | None:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()


def prepare_matrix(text: str) -> list[list[int]]:
    try:
        matrix = []
        for line in text.split('/n'):
            if line and line[0] != '+':
                matrix.append([int(num) for num in line[1:-1].split('|')])
        # Проверка на то, что матрица квадратная
        if matrix and not all([len(matrix) == len(line) for line in matrix]):
                raise ValueError('Матрица не квадратная!')
    except ValueError as ex:
        logging.warning(ex)
        return []
    return matrix


def traverse_matrix(matrix: list[list[int]], output: list[int] = None) -> list[int]:
    pass


async def get_matrix(url: str) -> list[int]:
    pass