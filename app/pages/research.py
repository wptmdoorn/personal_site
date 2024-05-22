from operator import itemgetter
from itertools import groupby
from nicegui import ui

import json


def content() -> None:
    # load json
    with open('app/data/researchgate_profile.json') as f:
        researchgate = json.load(f)

    for p in researchgate['publications']:
        p['year_published'] = p['date_published'].split(' ')[-1]

    publications = groupby(
        sorted(researchgate['publications'],
               key=itemgetter('year_published'), reverse=True),
        key=itemgetter('year_published'),

    )

    with ui.list().props('separator').style('width: 100%; font-size:1.0rem'):
        for year, group in publications:
            ui.item_label(year).props('header').classes('text-bold')
            ui.separator()

            for p in group:
                print(p)

                with ui.item(on_click=lambda p=p: ui.open(p['publication_link'])):
                    with ui.item_section().props('avatar'):
                        ui.icon('person')
                    with ui.item_section():
                        _authors = ', '.join(
                            p['authors'][:-1]) + ' and ' + p['authors'][-1]
                        ui.item_label(p['title'])
                        ui.item_label(_authors).props('caption')
