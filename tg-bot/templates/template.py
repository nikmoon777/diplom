from os import walk
from pathlib import Path

REP_TEMPLATE = '{{__}}'
TEMPLATE_DIR = Path('./templates/')
MIME_TYPE = 'txt'

TEMPLATE_CONTAINER = dict()

for folder, _, files in walk(TEMPLATE_DIR):
    if Path(folder) == TEMPLATE_DIR:
        for file in files:
            file_desc = file.split('.')
            if file_desc[1] == MIME_TYPE:
                with open(TEMPLATE_DIR.joinpath(file), encoding='utf-8') as inp:
                    TEMPLATE_CONTAINER[file_desc[0]] = ''.join(inp.readlines())


def template_get(key: str, *replacements) -> str:
    result = TEMPLATE_CONTAINER[key]
    for rep in replacements:
        result = result.replace(REP_TEMPLATE, rep)
    return result
