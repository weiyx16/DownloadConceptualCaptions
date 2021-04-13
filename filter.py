"""
Only keep jpeg etc "pure" image; [about 90% is kept]
"""
import pandas as pd
import os
from tqdm import tqdm

df = pd.read_csv('./downloaded_training_report.tsv.gz', compression='gzip', sep='\t', names=["file","folder","headers","mimetype","size","status","url"])
print(pd.DataFrame(df.groupby('mimetype')['url'].count()).reset_index(level=0).sort_values(by='url', ascending=False))
for item in tqdm(df.iterrows()):
    type = item[1]['mimetype']
    if isinstance(type, str) and 'image' in type:
        ext = type.split('/')[-1]
        if ext.lower() in ['jpeg', 'png', 'jpg']:
            os.system("mv {} {}.{}".format(item[1]['file'], item[1]['file'].replace('training', 'training_filtered'), ext))
