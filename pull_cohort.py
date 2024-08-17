from datetime import datetime, timedelta
from pull import process, write
from intra import ic
from config import config


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


if __name__ == '__main__':
    date = "2023-10-23"
    print(f'Fetching users where cursus started on {date}')
    users = fetch_users(date)
    print(f'Found {len(users)}')

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
