from intra import ic
import json
from collections import defaultdict


CAMPUS_ID = 13
CURSUS_ID = 21

def fetch():
    res = ic.pages_threaded('scale_teams', params={
        'filter[campus_id]': CAMPUS_ID,
        'filter[cursus_id]': CURSUS_ID,
        'range[begin_at]': "2023-08-10,2024-08-10"
    })

    return res

def process(res):
    nodes = set()
    links = defaultdict(int)

    for entry in res:
        corrector = entry['corrector']['login']
        correcteds = entry['correcteds']

        # Add the corrector to the nodes set
        nodes.add(corrector)

        # Loop through each corrected student and build the links
        for corrected in correcteds:
            corrected_login = corrected['login']
            nodes.add(corrected_login)
            # Increment the count of evaluations between corrector and corrected
            links[(corrector, corrected_login)] += 1

    # Convert nodes set to a list of dictionaries
    nodes_data = [{"id": node} for node in nodes]

    # Convert links dictionary to a list of dictionaries
    links_data = [{"source": source, "target": target, "value": value} for (source, target), value in links.items()]

    # Create the final data structure
    return {
        "nodes": nodes_data,
        "links": links_data
    }

def write(data):
    with open('web/data.json', 'w') as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    ic.progress_enable()
    res = fetch()
    data = process(res)
    write(data)



