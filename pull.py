import json

from collections import defaultdict

from config import config
from intra import ic


def fetch():
    res = ic.pages_threaded('scale_teams', params={
        'filter[campus_id]': config['campus_id'],
        'filter[cursus_id]': config['cursus_id'],
        'range[begin_at]': config['date_range']
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
    print("Fetching evaluations, can take some time...")
    res = fetch()
    print(f"Found {len(res)} evaluations")
    print("Processing data...")
    data = process(res)
    print("Done\nWriting into data.json...")
    write(data)
    print("Done")
