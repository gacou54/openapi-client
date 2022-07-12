from dataclasses import dataclass
from typing import Any


@dataclass
class ExternalDocumentation:
    url: str
    description: str = None


@dataclass
class Parameter:
    name: str
    in_: str

    description: str = None
    required: bool = None
    schema: dict = None

    def __post_init__(self):
        if self.in_ not in ('query', 'header', 'path', 'cookie'):
            raise ValueError(
                f'Invalid "in" value {self.in_} of Parameter({self.name}). '
                f'Should be "query", "header", "path" or "cookie".'
            )


@dataclass
class Header:
    description: str = None
    schema: dict[str, str] = None


@dataclass
class Example:
    summary: str = None
    description: str = None
    value: Any = None
    externalValue: str = None


@dataclass
class Encoding:
    contentType: str = None
    headers: dict[str, Header] = None
    style: str = None
    explode: bool = None
    allowReserved: bool = None

    def __post_init__(self):
        if self.headers is not None:
            self.headers = {k: Header(**v) for k, v in self.headers.items()}


@dataclass
class MediaType:
    schema: dict[str, str] = None
    example: Any = None
    examples: dict[str, Example] = None
    encoding: dict[str, Encoding] = None

    def __post_init__(self):
        if self.examples is not None:
            self.examples = {k: Example(**v) for k, v in self.examples.items()}
        if self.encoding is not None:
            self.encoding = {k: Encoding(**v) for k, v in self.encoding.items()}


@dataclass
class Response:
    description: str

    headers: dict[str, Header] = None
    content: dict[str, MediaType] = None
    links: dict = None

    def __post_init__(self):
        if self.headers is not None:
            self.headers = {k: Header(**v) for k, v in self.headers.items()}
        if self.content is not None:
            self.content = {k: MediaType(**v) for k, v in self.content.items()}


@dataclass
class RequestBody:
    content: dict

    description: str = None
    require: bool = None


@dataclass
class Operation:
    responses: dict[str, Response]

    tags: list[str] = None
    summary: str = None
    description: str = None
    externalDocs: Any = None
    operationId: str = None

    parameters: list[Parameter] = None
    requestBody: RequestBody = None
    deprecated: bool = None
    security: dict = None

    def __post_init__(self):
        for param in self.parameters:
            if 'in' in param:
                param['in_'] = param.pop('in')

        self.responses = {k: Response(**v) for k, v in self.responses.items()}
        if self.parameters is not None:
            self.parameters = [Parameter(**p) for p in self.parameters]
        if self.requestBody is not None:
            self.requestBody = RequestBody(**self.requestBody)


@dataclass
class Path:
    summary: str = None
    description: str = None

    operations: dict = None

    def __init__(self, **kwargs):
        # self.summary = summary
        # self.description = description

        self.operations = {}

        for operation_name, operation_data in kwargs.items():
            # Cleaning unused data to generate the client
            operation_data.pop('servers', None)
            operation_data.pop('callbacks', None)

            self.operations[operation_name] = Operation(**operation_data)

    def __post_init__(self):
        return
        if self.operations:
                # Cleaning unused data to generate the client
                operation.pop('servers', None)
                operation.pop('callbacks', None)

                self.operations[operation] = Operation(**operation_data)

        # if self.get is not None:
        #     # Cleaning unused data to generate the client
        #     self.get.pop('servers', None)
        #     self.get.pop('callbacks', None)
        #
        #     self.get = Operation(**self.get)
        #
        # if self.post is not None:
        #     # Cleaning unused data to generate the client
        #     self.post.pop('servers', None)
        #     self.post.pop('callbacks', None)
        #
        #     self.post = Operation(**self.post)
        #
        # if self.put is not None:
        #     # Cleaning unused data to generate the client
        #     self.put.pop('servers', None)
        #     self.put.pop('callbacks', None)
        #
        #     self.put = Operation(**self.put)
        #
        # if self.delete is not None:
        #     # Cleaning unused data to generate the client
        #     self.delete.pop('servers', None)
        #     self.delete.pop('callbacks', None)
        #
        #     self.delete = Operation(**self.delete)
        #
        # if self.options is not None:
        #     # Cleaning unused data to generate the client
        #     self.options.pop('servers', None)
        #     self.options.pop('callbacks', None)
        #
        #     self.options = Operation(**self.options)
        #
        # if self.head is not None:
        #     # Cleaning unused data to generate the client
        #     self.head.pop('servers', None)
        #     self.head.pop('callbacks', None)
        #
        #     self.head = Operation(**self.head)
        #
        # if self.patch is not None:
        #     # Cleaning unused data to generate the client
        #     self.patch.pop('servers', None)
        #     self.patch.pop('callbacks', None)
        #
        #     self.patch = Operation(**self.patch)
        #
        # if self.trace is not None:
        #     # Cleaning unused data to generate the client
        #     self.trace.pop('servers', None)
        #     self.trace.pop('callbacks', None)
        #
        #     self.trace = Operation(**self.trace)
