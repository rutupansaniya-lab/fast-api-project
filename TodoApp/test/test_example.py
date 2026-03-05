import pytest

def test_eqaul_or_not_equal():
    assert 1==1
    assert 1!=2

def test_is_instance():
    assert isinstance('hello', str)
    assert not isinstance('10',int)

def test_boolean():
    validated=True
    assert validated is True
    assert ('hello'=='world') is False

def test_type():
    assert type('hello' is str)
    assert type('world' is not int)

def test_greater_and_less_than():
    assert 7>3
    assert 4<10

def test_list():
    num_list=[1, 2, 3, 4, 5]
    any_list=[False, True]
    assert 1 in num_list
    assert 7 not in num_list
    assert all(num_list)
    assert any(any_list)

class Student:
    def __init__(self,fisrt_name: str, last_name: str, major: str, years: int):
        self.first_name=fisrt_name
        self.last_name=last_name
        self.major=major
        self.years=years

def test_person_initialization(default_student):
    p=Student('Rutu', 'Pansaniya', 'Computer Science', 3)
    assert p.first_name == 'Rutu', 'First name should be Rutu'
    assert p.last_name == 'Pansaniya', 'Last name should be Pansaniya'
    assert p.major == 'Computer Science', 'Major should be Computer '
    assert p.years == 3   

@pytest.fixture
def default_student():
    return Student('Rutu', 'Pansaniya', 'Computer Science', 3)
