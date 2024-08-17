import json

from collections import defaultdict


def process_scale_teams(data):
    nodes = set()
    links = defaultdict(int)

    for entry in data:
        corrector = entry['corrector']['login']
        correcteds = entry['correcteds']

        # Add the corrector to the nodes set
        nodes.add(corrector)

        # Loop through each corrected student and build the links
        for corrected in correcteds:
            corrected_login = corrected['login']
            nodes.add(corrected_login)

            pair = tuple(sorted([corrector, corrected_login]))
            links[pair] += 1

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
        json.dump(data, f, indent=2)


def chunk_list(elems, n_elems):
    return [elems[i:i + n_elems] for i in range(0, len(elems), n_elems)]
