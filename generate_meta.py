"""
Only keep jpeg etc "pure" image; [about 90% is kept]
"""
import pandas as pd
import os
from tqdm import tqdm
import json
import argparse
parser = argparse.ArgumentParser('Format json')
parser.add_argument('--split_idx', type=str, help='split_idx should in odds')
args = parser.parse_args()

caption_file = []

def cap_gen(args, df, caption_file):
    tsv_file = 'cc12_split_{}.tsv'.format(args.split_idx)
    caption_map = {}
    with open(tsv_file) as f:
        infos = f.read().splitlines()
        for i in infos:
            i = i.split('\t')
            cpation_map[i[0]] = i[1]

    for item in tqdm(df.iterrows()):
        type = item[1]['mimetype']
        if isinstance(type, str) and 'image' in type:
            ext = type.split('/')[-1]
            if ext.lower() in ['jpeg', 'png', 'jpg']:
                img_idx = item[1]['file'].split('/')[-1]
                caption_file.append({'caption': caption_map[img_idx], 'image': 'image_split_{}.zip@/{}.{}'.format(args.split_idx, img_idx, ext)})
    return caption_file

df = pd.read_csv('./downloaded_training_report.tsv.gz', compression='gzip', sep='\t', names=["file","folder","headers","mimetype","size","status","url"])
print(pd.DataFrame(df.groupby('mimetype')['url'].count()).reset_index(level=0).sort_values(by='url', ascending=False))
caption_file = cap_gen(args, df, caption_file)

df = pd.read_csv('./downloaded_training_report.tsv.gz.part0', compression='gzip', sep='\t', names=["file","folder","headers","mimetype","size","status","url"])
print(pd.DataFrame(df.groupby('mimetype')['url'].count()).reset_index(level=0).sort_values(by='url', ascending=False))
args.split_idx = args.split_idx-1
caption_file = cap_gen(args, df, caption_file)

json.dump(caption_file, open('caption_train.json', 'w'))
