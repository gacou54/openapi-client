import os
import dataclasses

import jinja2

from openapi_client.config import Config
from openapi_client.openapi import Document
from openapi_client.openapi.path import Parameter, Response

TYPES = {
    'boolean': 'bool',
    'number': 'int',
    'string': 'str',
    'array': 'list',
}
STATUS_CODES = {
    '200': 'success',
    '201': 'created',
}


def write_client(document: Document, config: Config):
    path = os.path.join(os.path.dirname(__file__), 'templates')
    template_loader = jinja2.FileSystemLoader(searchpath=path)
    template_env = jinja2.Environment(loader=template_loader)

    elements = []

    # Main Client
    template_client = template_env.get_template('client.jinja')
    output = template_client.render(
        CLIENT=config.client_name,
        document=dataclasses.asdict(document)
    )
    elements.append(output)

    # Methods
    for route, path in document.paths.items():
        template_method = template_env.get_template('method.jinja')

        # Rename "id" to "id_" because "id" is a builtin function in Python.
        route = route.replace('id', 'id_')

        if path.get is not None:
            output = template_method.render(
                FUNCTION_NAME=_make_function_name(route, 'get'),
                METHOD='get',
                ROUTE=route,
                OPERATION=path.get,
                FUNCTION_PARAMETERS=_make_parameters(path.get.parameters),
                HEADERS=_make_headers_passed_arg(path.get.parameters),
                TYPES=TYPES,
                RESPONSES=_make_responses(path.get.responses)
            )
            elements.append(output)
        # if path.post is not None:
        #     output = template_method.render(
        #         FUNCTION_NAME=_make_function_name(route, 'post')
        #     )
        #     elements.append(output)
        # if path.put is not None:
        #     output = template_method.render(
        #         FUNCTION_NAME=_make_function_name(route, 'put')
        #     )
        #     elements.append(output)
        # if path.delete is not None:
        #     output = template_method.render(
        #         FUNCTION_NAME=_make_function_name(route, 'delete')
        #     )
        #     elements.append(output)
        # if path.head is not None:
        #     output = template_method.render(
        #         FUNCTION_NAME=_make_function_name(route, 'head')
        #     )
        #     elements.append(output)
        # if path.options is not None:
        #     output = template_method.render(
        #         FUNCTION_NAME=_make_function_name(route, 'options')
        #     )
        #     elements.append(output)
        # if path.patch is not None:
        #     output = template_method.render(
        #         FUNCTION_NAME=_make_function_name(route, 'patch')
        #     )
        #     elements.append(output)
        # if path.trace is not None:
        #     output = template_method.render(
        #         FUNCTION_NAME=_make_function_name(route, 'trace')
        #     )
        #     elements.append(output)

    with open(f'./{config.package_name}.py', 'w') as file:
        file.write('\n\n'.join(elements))


def _make_function_name(route: str, method: str) -> str:
    """Makes function name from the route (e.g. /api/potato) and from method (e.g. get, post)"""
    # "/" to "_"
    name = route.replace('/', '_')
    name = f'_{name}' if name[0] != '_' else name

    # "{*}" to "*"
    name = name.replace('{', '').replace('}', '')

    # "-" to "_" and "." to "_"
    name = name.replace('-', '_').replace('.', '_')

    # Removing double "__"
    name = name.replace('__', '_')

    # Removing end "_", if applicable
    name = name[:-1] if name[-1] == '_' else name

    return f'{method}{name}'.lower()


def _make_parameters(parameters: list[Parameter]) -> str:
    params_in_route = [p for p in parameters if p.in_ == 'path']

    if len(params_in_route) == 0:
        return ''

    parameters_str = []

    for param in params_in_route:
        # Rename "id" to "id_" because "id" is a builtin function in Python.
        param_name = param.name.replace('id', 'id_')
        param_type = TYPES[param.schema['type']]
        param_str = f'{param_name}: {param_type}'

        parameters_str.append(param_str)

    return ', '.join(parameters_str) + ', '


def _make_headers_passed_arg(parameters: list[Parameter]) -> dict:
    headers = {p.name: p.description for p in parameters if p.in_ == 'header'}

    return headers


def _make_responses(responses: dict[str, Response]) -> list:
    responses_str = []

    for status_code, response in responses.items():
        for _, mediatype in response.content.items():
            responses_str.append({
                'result': STATUS_CODES[status_code],
                'description': 'No description' if mediatype.schema is None else mediatype.schema['description']
            })

    return responses_str
