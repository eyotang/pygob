import pytest
import collections
import pygob


@pytest.mark.parametrize(('value', 'encoded'), [
    (False, [3, 2, 0, 0]),
    (True, [3, 2, 0, 1]),
])
def test_bool(value, encoded):
    assert pygob.dump(value) == bytes(encoded)


@pytest.mark.parametrize(('value', 'encoded'), [
    (-2, [3, 4, 0, 3]),
    (-1, [3, 4, 0, 1]),
    (0, [3, 4, 0, 0]),
    (1, [3, 4, 0, 2]),
    (2, [3, 4, 0, 4]),
    (-256, [5, 4, 0, 254, 1, 255]),
    (-255, [5, 4, 0, 254, 1, 253]),
    (255, [5, 4, 0, 254, 1, 254]),
    (256, [5, 4, 0, 254, 2, 0]),
])
def test_int(value, encoded):
    assert pygob.dump(value) == bytes(encoded)


@pytest.mark.parametrize(('value', 'encoded'), [
    (0.0, [3, 8, 0, 0]),
    (1.0, [5, 8, 0, 254, 240, 63]),
    (-2.0, [4, 8, 0, 255, 192]),
    (3.141592, [11, 8, 0, 248, 122, 0, 139, 252, 250, 33, 9, 64]),
    (float('-inf'), [5, 8, 0, 254, 240, 255]),
    (float('+inf'), [5, 8, 0, 254, 240, 127]),
    (float('nan'), [5, 8, 0, 254, 248, 127]),
])
def test_float(value, encoded):
    assert pygob.dump(value) == bytes(encoded)


@pytest.mark.parametrize(('value', 'encoded'), [
    (b'', b'\x03\x0a\x00\x00'),
    (b'\x00', b'\x04\x0a\x00\x01\x00'),
    (b'abc', b'\x06\x0a\x00\x03abc'),
])
def test_bytes(value, encoded):
    assert pygob.dump(value) == encoded


@pytest.mark.parametrize(('value', 'encoded'), [
    ('', b'\x03\x0c\x00\x00'),
    ('hello', b'\x08\x0c\x00\x05hello'),
    ('alpha: α', b'\x0c\x0c\x00\x09alpha: \xce\xb1'),
])
def test_str(value, encoded):
    assert pygob.dump(value) == encoded


@pytest.mark.parametrize(('value', 'encoded'), [
    (0.0 + 0.0j, [4, 14, 0, 0, 0]),
    (0.0 + 1.0j, [6, 14, 0, 0, 254, 240, 63]),
    (3.0 + 4.0j, [8, 14, 0, 254, 8, 64, 254, 16, 64]),
    (-2.71828 + 3.14159j, [
        20, 14, 0, 248, 144, 247, 170, 149, 9, 191, 5, 192, 248, 110, 134, 27,
        240, 249, 33, 9, 64
    ]),
])
def test_complex(value, encoded):
    assert pygob.dump(value) == bytes(encoded)


def test_user_struct():
    encoded = [34, 255, 129, 3, 1, 1, 4, 85, 115, 101, 114, 1, 255, 130, 0, 1, 2, 1, 2, 73, 100, 1, 4, 0, 1, 4, 78, 97, 109, 101, 1, 12, 0, 0, 0, 14, 255, 130, 1, 2, 1, 7, 101, 121, 111, 116, 97, 110, 103, 0]
    User = collections.namedtuple('User', ['Id', 'Name'])
    assert pygob.dump(User(1, b'eyotang')) == bytes(encoded)
