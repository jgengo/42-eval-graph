from config import config
from intra import ic
from helpers import process_scale_teams, write


def fetch():
    res = ic.pages_threaded('scale_teams', params={
        'filter[campus_id]': config['campus_id'],
        'filter[cursus_id]': config['cursus_id'],
        'range[begin_at]': config['date_range']
    })

    return res


if __name__ == "__main__":
    ic.progress_enable()
    print("Fetching evaluations, can take some time...")
    scale_teams = fetch()
    print(f"Found {len(scale_teams)} evaluations")
    print("Processing data...")
    data = process_scale_teams(scale_teams)
    print("Done\nWriting into data.json...")
    write(data)
    print("Done")
