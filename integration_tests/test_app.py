from dotenv import find_dotenv, load_dotenv
import pytest
import json

from app import create_app
from entity.item import Item


@pytest.fixture
def client():
    file_path = find_dotenv('test_env_file.test')
    load_dotenv(file_path, override=True)

    test_app = create_app()

    with test_app.test_client() as client:
        yield client


def stub_get_db_collection():
    return


def stub_get_all_items(collection):
    return [
        Item(
            'test-to-do-card-id',
            'Test To Do Card Title',
            'To do',
            '2020-06-24T14:51:12.321Z'
        ),
        Item(
            'test-doing-card-id',
            'Test Doing Card Title',
            'Doing',
            '2020-06-24T14:51:12.321Z'
        ),
        Item(
            'test-done-card-id',
            'Test Done Card Title',
            'Done',
            '2020-06-24T14:51:12.321Z'
        )
    ]


def test_index_page(monkeypatch, client):
    monkeypatch.setattr(
        'app.get_db_collection',
        stub_get_db_collection
    )
    monkeypatch.setattr(
        'app.get_all_items',
        stub_get_all_items
    )

    response = client.get('/')

    content = response.data.decode('utf8')
    assert response.status_code == 200
    assert 'Test To Do Card Title' in content
    assert 'Test Doing Card Title' in content
    assert 'Test Done Card Title' in content
