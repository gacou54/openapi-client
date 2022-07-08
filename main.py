import copy

from openapi_client.openapi import Document
from openapi_client.parser import parse_openapi
from openapi_client.config import Config
from openapi_client.writer import write_client


def apply_corrections_to_documents(document: Document) -> Document:
    """Correcting Orthanc OpenAPI specs"""
    to_change = []

    for route, path in document.paths.items():
        if path.get is not None:
            for param in path.get.parameters:
                if param.name == '...':
                    print(path)
                    param.name = 'tags_path'

                    to_change.append({
                        'old_route': route,
                        'new_route': route + '/{tags_path}',
                    })

    for change in to_change:
        document.paths[change['new_route']] = document.paths.pop(change['old_route'])

    return document


config = Config(
    client_name='Orthanc'
)

# openapi_document = parse_openapi(url_path='https://api.orthanc-server.com/orthanc-openapi.json')
document = parse_openapi(url_or_path='./orthanc-openapi.json')

document = apply_corrections_to_documents(document)

write_client(document, config)
