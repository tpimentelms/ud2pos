import os
import argparse
import re
import csv
import json
import pickle
from conllu import parse_incr


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--language",
                        help="The language to use",
                        required=True,
                        type=str)
    parser.add_argument("--ud-path",
                        help="The path to raw ud data",
                        default='data/ud/ud-treebanks-v2.5/',
                        required=False,
                        type=str)
    parser.add_argument("--output-file",
                        help="The file to save processed ud data",
                        required=True,
                        type=str)
    args = parser.parse_args()
    print(args)

    return args


def get_ud_file_base(ud_path, language):
    regex_lang = re.compile('UD_%s-' % (language.capitalize()))

    treebanks = os.listdir(ud_path)
    treebanks = [x for x in treebanks if regex_lang.match(x)]
    return [os.path.join(ud_path, x) for x in treebanks]


def get_ud_fname(path, mode):
    regex_file = re.compile('.+-ud-%s.conllu' % (mode))
    files = os.listdir(path)
    file = [x for x in files if regex_file.match(x)]

    if len(file) == 0:
        return None

    assert len(file) == 1, 'Should have one match with file name'
    return os.path.join(path, file[0])


def process_file(ud_file):
    ud_data = {}
    # adjectives, verbs = set(), set()
    with open(ud_file, "r", encoding="utf-8") as file:
        for token_list in parse_incr(file):
            for item in token_list:
                word_info = (
                    item['lemma'].lower(),
                    item['form'].lower(),
                    item['upos'],
                    # json.dumps(item['feats']),
                )
                ud_data[word_info] = ud_data.get(word_info, 0) + 1

    return ud_data


def merge_dicts(dict_counts1, dict_counts2):
    keys = set(dict_counts1.keys()) | set(dict_counts2.keys())
    return {
        key: dict_counts1.get(key, 0) + dict_counts2.get(key, 0)
        for key in keys
    }


def clean_data(instances):
    instances = sorted(instances.items(), key=lambda x: x[1], reverse=True)
    cleaned_data = {}
    for item, count in instances:
        wordform = item[1]
        if wordform not in cleaned_data:
            cleaned_data[wordform] = item

    print('# Instances: %d. # Cleaned instances: %d' % (len(instances), len(cleaned_data)))
    cleaned_data = list(cleaned_data.values())
    return [
        {
            'lemma': x[0],
            'form': x[1],
            'pos': x[2],
            # 'feats': json.loads(x[3]),
        }
        for x in cleaned_data
    ]


def process(language, ud_path, output_file):
    print("Precessing language %s" % language)
    ud_paths = get_ud_file_base(ud_path, language)
    ud_data = {}

    for path in ud_paths:
        for mode in ['train', 'dev', 'test']:
            ud_file = get_ud_fname(path, mode)
            if ud_file is None:
                continue

            ud_data_temp = process_file(ud_file)
            ud_data = merge_dicts(ud_data, ud_data_temp)

    ud_data = clean_data(ud_data)
    return ud_data


def write_data(filename, data):
    with open(filename, "w") as f:
        writer = csv.DictWriter(f, data[0].keys(), delimiter='\t')
        writer.writeheader()
        writer.writerows(data)


def main():
    args = get_args()

    language = args.language
    ud_path = args.ud_path
    output_file = args.output_file

    results = process(language, ud_path, output_file)
    write_data(args.output_file, results)


if __name__ == "__main__":
    main()
