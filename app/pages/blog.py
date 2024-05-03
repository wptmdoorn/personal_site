from nicegui import ui
import glob
import json
import pandas as pd
import os


def content() -> None:
    files = glob.glob('app/blogs/*')
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
    metadata = metadata.sort_values('jaar', ascending=False)

    with ui.list().props('separator').style('width: 100%'):
        for year, group in metadata.groupby('jaar', sort=False):
            ui.item_label(year).props('header').classes('text-bold')
            ui.separator()

            for _, row in group.iterrows():
                with ui.item(on_click=lambda row=row: ui.open(f'/blog/{row["file_name"]}')):
                    with ui.item_section().props('avatar'):
                        ui.icon('person')
                    with ui.item_section():
                        ui.item_label(row['title'])
                        ui.item_label(
                            f'Published on {row["pub_date"]}').props('caption')
