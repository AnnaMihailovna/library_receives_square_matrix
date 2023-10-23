import asyncio

from library.matrix_traversal import prepare_matrix, \
    traverse_matrix, get_matrix

TRAVERSAL = [
    10, 50, 90, 130,
    140, 150, 160, 120,
    80, 40, 30, 20,
    60, 100, 110, 70
]

PREPARED_MATRIX = [[10, 20, 30, 40],
                   [50, 60, 70, 80],
                   [90, 100, 110, 120],
                   [130, 140, 150, 160]]

SOURCE_URL = 'https://raw.githubusercontent.com/avito-tech/' \
             'python-trainee-assignment/main/matrix.txt'

def test_prepare_matrix():
    with open("test_matrix.txt") as file:
        assert prepare_matrix(file.read()) == PREPARED_MATRIX
    assert prepare_matrix("") == []
    assert prepare_matrix("+----+\n| 1 | 3 |\n+_____+") == []

def test_traverse_matrix():
    output_matrix = []
    traverse_matrix(PREPARED_MATRIX, output_matrix)
    assert output_matrix == TRAVERSAL

def test_get_matrix():
    assert asyncio.run(get_matrix(SOURCE_URL)) == TRAVERSAL
