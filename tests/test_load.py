import math

import pytest

import pygob


@pytest.mark.parametrize(('data', 'expected'), [
    ([3, 6, 0, 1], 1),
    ([3, 6, 0, 2], 2),
    ([3, 6, 0, 3], 3),
    ([4, 6, 0, 255, 255], 255),
    ([5, 6, 0, 254, 1, 0], 256),
    ([5, 6, 0, 254, 1, 1], 257),
])
def test_uint(data, expected):
    assert pygob.load(bytes(data)) == expected


@pytest.mark.parametrize(('data', 'expected'), [
    ([3, 4, 0, 5], -3),
    ([3, 4, 0, 3], -2),
    ([3, 4, 0, 1], -1),
    ([3, 4, 0, 0], 0),
    ([3, 4, 0, 2], 1),
    ([3, 4, 0, 4], 2),
    ([3, 4, 0, 6], 3),
    ([5, 4, 0, 254, 1, 255], -256),
    ([5, 4, 0, 254, 1, 253], -255),
    ([5, 4, 0, 254, 1, 254], 255),
    ([5, 4, 0, 254, 2, 0], 256),
])
def test_int(data, expected):
    assert pygob.load(bytes(data)) == expected


@pytest.mark.parametrize(('data', 'expected'), [
    ([3, 2, 0, 1], True),
    ([3, 2, 0, 0], False),
])
def test_bool(data, expected):
    assert pygob.load(bytes(data)) == expected


@pytest.mark.parametrize(('data', 'expected'), [
    ([3, 8, 0, 0], 0),
    ([5, 8, 0, 254, 240, 63], 1),
    ([4, 8, 0, 255, 192], -2),
    ([11, 8, 0, 248, 122, 0, 139, 252, 250, 33, 9, 64], 3.141592),
    ([5, 8, 0, 254, 240, 255], -math.inf),
    ([5, 8, 0, 254, 240, 127], +math.inf),
])
def test_float(data, expected):
    assert pygob.load(bytes(data)) == expected


def test_float_nan():
    data = [11, 8, 0, 248, 1, 0, 0, 0, 0, 0, 248, 127]
    result = pygob.load(bytes(data))
    assert math.isnan(result)


@pytest.mark.parametrize(('data', 'expected'), [
    ([3, 10, 0, 0], b''),
    ([4, 10, 0, 1, 97], b'a'),
    ([5, 10, 0, 2, 97, 98], b'ab'),
    ([6, 10, 0, 3, 97, 98, 99], b'abc'),
])
def test_byte_slice(data, expected):
    result = pygob.load(bytes(data))
    assert type(result) == bytearray
    assert result == expected


@pytest.mark.parametrize(('data', 'expected'), [
    ([3, 12, 0, 0], b''),
    ([4, 12, 0, 1, 97], b'a'),
    ([5, 12, 0, 2, 97, 98], b'ab'),
    ([6, 12, 0, 3, 97, 98, 99], b'abc'),
])
def test_string(data, expected):
    result = pygob.load(bytes(data))
    assert type(result) == bytes
    assert result == expected


@pytest.mark.parametrize(('data', 'expected'), [
    ([4, 14, 0, 0, 0], 0 + 0j),
    ([6, 14, 0, 0, 254, 240, 63], 0 + 1j),
    ([8, 14, 0, 254, 8, 64, 254, 16, 64], 3 + 4j),
    ([
        20, 14, 0, 248, 144, 247, 170, 149, 9, 191, 5, 192, 248, 110, 134, 27,
        240, 249, 33, 9, 64
    ], -2.71828 + 3.14159j),
])
def test_complex(data, expected):
    assert pygob.load(bytes(data)) == expected


@pytest.mark.parametrize(('data', 'expected'), [
    ([12, 255, 133, 1, 1, 2, 255, 134, 0, 1, 4, 0, 0, 4, 255, 134, 0, 0], ()),
    ([
        14, 255, 135, 1, 1, 2, 255, 136, 0, 1, 4, 1, 2, 0, 0, 5, 255, 136, 0,
        1, 34
    ], (17, )),
    ([
        14, 255, 137, 1, 1, 2, 255, 138, 0, 1, 4, 1, 6, 0, 0, 10, 255, 138, 0,
        3, 34, 255, 234, 254, 1, 178
    ], (17, 117, 217)),
])
def test_int_array(data, expected):
    assert pygob.load(bytes(data)) == expected


def test_int_matrix():
    data = [
        15, 255, 141, 1, 1, 2, 255, 142, 0, 1, 255, 140, 1, 6, 0, 0, 14, 255,
        139, 1, 1, 2, 255, 140, 0, 1, 4, 1, 6, 0, 0, 16, 255, 142, 0, 3, 3, 0,
        2, 4, 3, 6, 8, 10, 3, 12, 14, 16
    ]
    expected = ((0, 1, 2), (3, 4, 5), (6, 7, 8))
    assert pygob.load(bytes(data)) == expected


@pytest.mark.parametrize(('data', 'expected'), [
    ([12, 255, 131, 1, 1, 2, 255, 132, 0, 1, 2, 0, 0, 4, 255, 132, 0, 0], ()),
    ([
        14, 255, 133, 1, 1, 2, 255, 134, 0, 1, 2, 1, 4, 0, 0, 6, 255, 134, 0,
        2, 1, 0
    ], (True, False)),
])
def test_bool_array(data, expected):
    assert pygob.load(bytes(data)) == expected


def test_extra_array_elements():
    data = [
        14, 255, 135, 1, 1, 2, 255, 136, 0, 1, 4, 1, 2, 0, 0, 5, 255, 136, 0,
        7, 34
    ]
    with pytest.raises(AssertionError) as excinfo:
        pygob.load(bytes(data))
    excinfo.match('expected 1 elements, found 7')


@pytest.mark.parametrize(('data', 'expected'), [
    ([12, 255, 143, 2, 1, 2, 255, 144, 0, 1, 8, 0, 0, 4, 255, 144, 0, 0], []),
    ([
        12, 255, 145, 2, 1, 2, 255, 146, 0, 1, 8, 0, 0, 22, 255, 146, 0, 2,
        248, 31, 133, 235, 81, 184, 30, 9, 64, 248, 125, 195, 148, 37, 173, 73,
        178, 84
    ], [3.14, 1e100]),
])
def test_float_slice(data, expected):
    assert pygob.load(bytes(data)) == expected
