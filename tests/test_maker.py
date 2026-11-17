import simple_openapi_client
from simple_openapi_client.openapi import Document


def _make_document(paths: dict) -> Document:
    return Document(
        openapi='3.0.0',
        info={'title': 'API', 'version': '1.0'},
        paths=paths,
    )


def _operation(parameters=None) -> dict:
    return {
        'summary': 'Summary',
        'description': 'Description',
        'tags': ['Tag'],
        'parameters': parameters or [],
        'responses': {'200': {'description': 'Success'}},
    }


def _path_parameter(name: str) -> dict:
    return {'name': name, 'in': 'path', 'required': True, 'description': f'The {name}', 'schema': {'type': 'string'}}


def test_id_parameter_is_renamed():
    document = _make_document({'/instances/{id}/file': {'get': _operation([_path_parameter('id')])}})

    client_str = simple_openapi_client.make_client(document, simple_openapi_client.Config(client_name='Client'))

    assert 'def get_instances_id_file(' in client_str
    assert 'id_: str' in client_str
    assert "route=f'{self.url}/instances/{id_}/file'" in client_str


def test_id_inside_route_words_is_not_renamed():
    document = _make_document({
        '/tools/generate-uid': {'get': _operation()},
        '/tools/invalidate-tags': {'post': _operation()},
    })

    client_str = simple_openapi_client.make_client(document, simple_openapi_client.Config(client_name='Client'))

    assert "route=f'{self.url}/tools/generate-uid'" in client_str
    assert "route=f'{self.url}/tools/invalidate-tags'" in client_str
    assert 'def get_tools_generate_uid(' in client_str
    assert 'def post_tools_invalidate_tags(' in client_str
    assert 'uid_' not in client_str
    assert 'invalid_ate' not in client_str


def test_parameter_names_containing_id_are_not_renamed():
    document = _make_document({'/series/{uuid}': {'get': _operation([_path_parameter('uuid')])}})

    client_str = simple_openapi_client.make_client(document, simple_openapi_client.Config(client_name='Client'))

    assert 'uuid: str' in client_str
    assert "route=f'{self.url}/series/{uuid}'" in client_str
