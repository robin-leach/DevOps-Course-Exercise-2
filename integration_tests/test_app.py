from dotenv import find_dotenv, load_dotenv
import pytest
import json

from app import create_app
from entity.trello_list import TrelloList
from entity.trello_card import TrelloCard
from entity.mock_response import MockResponse


@pytest.fixture
def client():
    file_path = find_dotenv('test_env_file.txt')
    load_dotenv(file_path, override=True)

    test_app = create_app()

    with test_app.test_client() as client:
        yield client


def stub_lists_request(method, endpoint, extra_params={}):
    responseJson = [
        {
            'id': 'test-to-do-list-id',
            'name': 'To do'
        },
        {
            'id': 'test-doing-list-id',
            'name': 'Doing'
        },
        {
            'id': 'test-done-list-id',
            'name': 'Done'
        }
    ]
    return MockResponse(responseJson)


def stub_items_request(method, endpoint, extra_params={}):
    responseJson = [
        {
            'id': 'test-to-do-card-id',
            'name': 'Test To Do Card Title',
            'idList': 'test-to-do-list-id',
            'dateLastActivity': '2020-06-24T14:51:12.321Z'
        },
        {
            'id': 'test-doing-card-id',
            'name': 'Test Doing Card Title',
            'idList': 'test-doing-list-id',
            'dateLastActivity': '2020-06-24T14:51:12.321Z'
        },
        {
            'id': 'test-done-card-id',
            'name': 'Test Done Card Title',
            'idList': 'test-done-list-id',
            'dateLastActivity': '2020-06-24T14:51:12.321Z'
        }
    ]
    return MockResponse(responseJson)


def test_index_page(monkeypatch, client):
    monkeypatch.setattr(
        'trello_requests.lists.make_trello_request',
        stub_lists_request
    )
    monkeypatch.setattr(
        'trello_requests.items.make_trello_request',
        stub_items_request
    )

    response = client.get('/')

    content = response.data.decode('utf8')
    assert response.status_code == 200
    assert 'Test To Do Card Title' in content
    assert 'Test Doing Card Title' in content
    assert 'Test Done Card Title' in content
