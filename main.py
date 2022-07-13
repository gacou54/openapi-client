from openapi_client.openapi import Document
from openapi_client import Config, parse_openapi, make_client


def apply_corrections_to_documents(document: Document) -> Document:
    """Correcting Orthanc OpenAPI specs"""
    to_change = []

    for route, path in document.paths.items():
        if path.operations is not None:
            for operation_name, operation in path.operations.items():
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


if __name__ == '__main__':
    config = Config(
        client_name='Orthanc'
    )

    document = parse_openapi(url_or_path='https://api.orthanc-server.com/orthanc-openapi.json')
    # document = parse_openapi(url_or_path='./orthanc-openapi.json')

    document = apply_corrections_to_documents(document)

    client_str = make_client(document, config)

    with open(f'./{config.package_name}.py', 'w') as file:
        file.write(client_str)
