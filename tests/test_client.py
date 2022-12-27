import asyncio
import os

import pytest

import simple_openapi_client

OPENAPI_URL = 'https://api.orthanc-server.com/orthanc-openapi.json'
CLIENT_PATH = 'generated_client.py'
CLIENT_MODULE = 'generated_client'

ASYNC_CLIENT_PATH = 'async_generated_client.py'
ASYNC_CLIENT_MODULE = 'async_generated_client'

CLIENT_NAME = 'Orthanc'


@pytest.fixture
def generate_client():
    config = simple_openapi_client.Config(client_name=CLIENT_NAME)

    document = simple_openapi_client.parse_openapi(OPENAPI_URL)
    document = _apply_corrections_to_documents(document)

    client_str = simple_openapi_client.make_client(document, config)
    async_client_str = simple_openapi_client.make_client(document, config, async_mode=True)

    with open(CLIENT_PATH, 'w') as file:
        file.write(client_str)

    with open(ASYNC_CLIENT_PATH, 'w') as file:
        file.write(async_client_str)

    yield

    if os.path.exists(CLIENT_PATH):
        os.remove(CLIENT_PATH)

    if os.path.exists(ASYNC_CLIENT_PATH):
        os.remove(ASYNC_CLIENT_PATH)


def _apply_corrections_to_documents(document):
    """Correcting Orthanc OpenAPI specs"""
    to_change = []

    for route, path in document.paths.items():
        if path.operations is not None:
            for operation_name, operation in path.operations.items():
                if operation.parameters is None:
                    continue

                for param in operation.parameters:
                    if param.name == '...':
                        param.name = 'tags_path'

                        to_change.append({
                            'old_route': route,
                            'new_route': route + '/{tags_path}',
                        })

    for change in to_change:
        document.paths[change['new_route']] = document.paths.pop(change['old_route'])

    return document


def test_generate_client(generate_client):
    # Client
    client_class = getattr(__import__(CLIENT_MODULE), CLIENT_NAME)
    client = client_class(url='https://demo.orthanc-server.com')

    system_information = client.get_system()
    assert isinstance(system_information, dict)
    assert 'ApiVersion' in system_information
    assert 'DicomAet' in system_information
    assert 'DicomPort' in system_information

    # Async client
    async_client_class = getattr(__import__(ASYNC_CLIENT_MODULE), CLIENT_NAME)
    async_client = async_client_class(url='https://demo.orthanc-server.com')

    system_information = asyncio.run(async_client.get_system())
    print(system_information)
    assert isinstance(system_information, dict)
    assert 'ApiVersion' in system_information
    assert 'DicomAet' in system_information
    assert 'DicomPort' in system_information
