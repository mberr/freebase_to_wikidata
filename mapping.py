# coding=utf-8
import json

with open('translation.json', 'r') as json_file:
    _CACHE = json.load(json_file)


def resolve_freebase_id_to_label(freebase_id: str) -> str:
    doc = _CACHE[freebase_id]
    labels = doc['label']
    if len(labels) < 1:
        return f'UNKNOWN(freebase_id="{freebase_id}"")'
    elif len(labels) > 1:
        return '{' + ','.join(labels) + '}'
    else:
        return labels[0]


def resolve_freebase_id_to_wikidata_id(freebase_id: str) -> str:
    doc = _CACHE[freebase_id]
    wikidata_ids = doc['wikidata']
    if len(wikidata_ids) < 1:
        return f'UNKNOWN(freebase_id="{freebase_id}"")'
    elif len(wikidata_ids) > 1:
        return '{' + ','.join(wikidata_ids) + '}'
    else:
        return wikidata_ids[0]
