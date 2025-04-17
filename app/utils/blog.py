import glob
import pandas as pd
import json
import os


def get_blog_metadata():
    files = glob.glob('app/blogs/*')
    print(files)
    metadata = []

    for file in files:
        with open(f'{file}/blog.md', encoding='utf-8') as f:
            metadata.append(
                json.loads(f.read().split('---')
                           [1]) | {'file_name': os.path.basename(file).replace('.md', '')}
            )

    metadata = pd.DataFrame.from_dict(metadata)
    metadata['jaar'] = pd.to_datetime(
        metadata['pub_date'], format="%Y-%m-%d").dt.year

    # sort by last year first
    return metadata.sort_values('jaar', ascending=False).to_dict('records')
