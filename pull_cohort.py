import sys

from datetime import datetime, timedelta

from config import config
from intra import ic
from pull import process, write


def range_date(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    next_day = date + timedelta(days=1)
    return f"{date_str},{next_day.strftime('%Y-%m-%d')}"


def slice(elems, n_elems):
    return [elems[i:i + n_elems] for i in range(0, len(elems), n_elems)]


def fetch_users(begin_at):
    ranged_date = range_date(begin_at)

    cursus_users = ic.pages_threaded('cursus_users', params={
        'filter[campus_id]': config['campus_id'],
        'filter[cursus_id]': config['cursus_id'],
        'range[begin_at]': ranged_date
    })

    return [str(cu['user']['id']) for cu in cursus_users]


def validate_params():
    # Check if the argument is provided
    if len(sys.argv) < 2:
        print("Error: No date provided. Please provide a date in the format YYYY-mm-dd.")
        sys.exit(1)

    date_str = sys.argv[1]

    # Try to parse the date
    try:
        datetime.strptime(date_str, "%Y-%m-%d").date()
        return date_str
    except ValueError:
        print(f"Error: The date '{date_str}' is not in the correct format YYYY-mm-dd.")
        sys.exit(1)


if __name__ == '__main__':
    date = validate_params()

    print(f'Fetching users where cursus started on {date}')
    users = fetch_users(date)
    print(f'Found {len(users)}')

    if len(users) == 0:
        sys.exit(0)

    print("Fetching evaluations, can take some time...")
    scale_teams = []
    for uids in slice(users, 25):
        res = ic.pages_threaded('scale_teams', params={
            'filter[user_id]': ','.join(uids)
        })
        scale_teams.extend(res)

    print(f"Found {len(scale_teams)} evaluations")
    print("Processing data...")
    data = process(scale_teams)
    print("Done\nWriting into data.json")
    write(data)
    print("Done")
