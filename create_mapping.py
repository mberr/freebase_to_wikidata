#!/usr/bin/env python3
# coding=utf-8
import argparse
import json
import logging
from os import path

import pandas

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_root', required=False, default='.')
    parser.add_argument('--output_root', required=False, default='.')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(msg)s')
    used_freebase = pandas.read_csv(path.join(args.data_root, 'freebase_ids.csv'), header=None, names=['freebase_id'])
    fb15k_237_total = used_freebase.shape[0]
    logging.info(f'Loaded {fb15k_237_total} freebase IDs')

    wikidata_to_freebase = pandas.read_csv(path.join(args.data_root, 'wikidata.to.freebase.tsv'), sep=' ', header=None, names=['wikidata_id', 'freebase_id'])
    logging.info(f'Loaded {wikidata_to_freebase.shape[0]} Wikidata IDs')

    wikidata_to_freebase_selection = pandas.merge(left=used_freebase, right=wikidata_to_freebase, on='freebase_id', how='left')
    found = wikidata_to_freebase_selection.wikidata_id.count()
    logging.info(f'Found {found} matches in Wikidata.')

    wikidata_to_label = pandas.read_csv(path.join(args.data_root, 'wikidata.to.label.tsv'), sep=' ', escapechar='\\', header=None, names=['wikidata_id', 'label'])
    logging.info(f'Loaded {wikidata_to_label.shape[0]} English Wikidata labels.')

    join = pandas.merge(left=wikidata_to_freebase_selection, right=wikidata_to_label, on='wikidata_id', how='left')

    result = {}
    for row_id, row in join.iterrows():
        freebase_id = row.freebase_id
        # There are some freebase IDs with 0-3 associated wikidata IDs
        result.setdefault(freebase_id, {
            'label': [],
            'wikidata_id': [],
        })

        label = row.label
        if isinstance(label, str):
            result[freebase_id]['label'].append(label)

        wikidata_id = row.wikidata_id
        if isinstance(wikidata_id, str):
            result[freebase_id]['wikidata_id'].append(wikidata_id)

    output_path = path.join(args.output_root, 'translation.json')
    with open(output_path, 'w') as json_file:
        json.dump(result, json_file, indent=2, sort_keys=True)
    logging.info(f'Written result to {output_path}.')
