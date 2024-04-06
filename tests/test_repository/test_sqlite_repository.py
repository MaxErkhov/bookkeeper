from bookkeeper.repository.sqlite_repository import SQLiteRepository

import pytest


@pytest.fixture
def custom_class():
    class Custom():
        pk_: int = 0
        name: str = "$uicideboy$"
        value: int = 47
        real: float = 1.5

        def __str__(self) -> str:
            return f'pk_={self.pk_} name={self.name} value={self.value}'

        def __eq__(self, other) -> bool:
            if not isinstance(other, Custom):
                return NotImplemented

            return self.pk_ == other.pk_ and self.name == other.name and self.value == other.value

    return Custom


@pytest.fixture
def repo(custom_class):
    return SQLiteRepository("databases/test_database.db", custom_class)


def test_crud(repo, custom_class):
    obj = custom_class()
    pk_ = repo.add(obj)
    assert obj.pk_ == pk_
    assert repo.get(pk_) == obj
    obj2 = custom_class()
    obj2.pk_ = pk_
    repo.update(obj2)
    assert repo.get(pk_) == obj2
    repo.delete(pk_)
    assert repo.get(pk_) is None

def test_update(repo, custom_class):
    obj = custom_class()
    pk_ = repo.add(obj)
    obj.name = "update"
    assert repo.get(pk_) != obj
    repo.update(obj)
    assert repo.get(pk_) == obj


def test_cannot_add_with_pk_(repo, custom_class):
    obj = custom_class()
    obj.pk_ = 1
    with pytest.raises(ValueError):
        repo.add(obj)


def test_cannot_add_without_pk_(repo):
    with pytest.raises(ValueError):
        repo.add(0)


def test_cannot_delete_unexistent(repo):
    with pytest.raises(KeyError):
        repo.delete(-1)


def test_cannot_update_without_pk_(repo, custom_class):
    obj = custom_class()
    with pytest.raises(ValueError):
        repo.update(obj)


def test_get_all(repo, custom_class):
    repo.delete_all()
    objects = [custom_class() for i in range(5)]
    for o in objects:
        repo.add(o)
    assert repo.get_all() == objects


def test_get_all_with_condition(repo, custom_class):
    repo.delete_all()
    objects = []
    for i in range(5):
        o = custom_class()
        o.value = i
        o.name = 'test'
        repo.add(o)
        objects.append(o)

    assert repo.get_all({'value': 0}) == [objects[0]]
    assert repo.get_all({'name': 'test'}) == objects
