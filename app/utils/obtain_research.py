import json


def get_publication_list() -> list:
    with open('app/data/researchgate_profile.json') as f:
        researchgate = json.load(f)

    for p in researchgate['publications']:
        p['year_published'] = p['date_published'].split(' ')[-1]

    return researchgate['publications']
