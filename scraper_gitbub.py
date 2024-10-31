import time
import csv
import requests

headers = {"Authorization": "Bearer GITHUB_TOKEN"}


def get_users(page=1, results_per_page=100):
    url = 'https://api.github.com/search/users?q=location:Zurich+followers:>50'
    # query = f'location:Zurich followers:>={min_followers}'
    params = {
        # 'q': query,
        'per_page': results_per_page,  # max results per page
        'page': page
    }
    res = requests.get(url, headers=headers,params=params)
    users = res.json()
    return users['items'], users['total_count']


def get_user_details(username):
    url = f'https://api.github.com/users/{username}'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        user_data = response.json()
        return user_data
    else:
        print(f"Error fetching details for {username}: {response.status_code}")
        return None

def fetch_recent_repos(username, max_repos=500):
    repos = []
    page = 1
    per_page = 100  # maximum items per page

    while len(repos) < max_repos:
        api_url = f"https://api.github.com/users/{username}/repos"
        params = {
            "sort": "pushed",
            "direction": "desc",
            "per_page": per_page,
            "page": page
        }

        response = requests.get(api_url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if not data:
                break  # Exit if no more repositories are returned

            # Add repositories to the list
            repos.extend(data)

            # Stop if we've fetched enough repositories
            if len(repos) >= max_repos:
                repos = repos[:max_repos]  # Trim the list to max_repos
                break

            page += 1
            time.sleep(1)  # Pause to respect API rate limits
        else:
            print(f"Error fetching repositories: {response.json().get('message')}")
            break
    return repos


if __name__ == '__main__':
    directory = '/path/tds/'
    csv_file = directory + "users.csv"
    repo_csv_file = directory + "repositories.csv"
    columns = [
        'login', 'name', 'company', 'location', 'email', 'hireable', 'bio',
        'public_repos', 'followers', 'following', 'created_at'
    ]
    repo_columns = [
        'login', 'full_name', 'created_at', 'stargazers_count', 'watchers_count', 'language', 'has_projects',
        'has_wiki', 'license_name'
    ]

    import math
    users = []
    _page = 1
    _per_page = 100
    _users, _total = get_users(page=_page, results_per_page=_per_page)
    users.extend(_users)
    no_of_pages = math.ceil(_total/_per_page)
    if no_of_pages > 1:
        _page = 2
    while _page <= no_of_pages:
        _users, _total = get_users(page=_page, results_per_page=_per_page)
        users.extend(_users)
        _page += 1

    file = open(csv_file, 'a', newline='', encoding="utf-8")
    writer = csv.writer(file)

    repo_file = open(repo_csv_file, 'a', newline='', encoding="utf-8")
    repo_writer = csv.writer(repo_file)

    writer.writerow(columns)
    repo_writer.writerow(repo_columns)

    for c, user in enumerate(users):
        print(c)
        data = []
        u_data = get_user_details(user['login'])
        repo_data = fetch_recent_repos(user['login'], max_repos=500)

        for column in columns:
            if column == 'login':
                data.append(user['login'])
            if column in ['name', 'email', 'followers', 'location', 'hireable', 'following', 'bio', 'created_at', 'public_repos']:
                val = u_data[column]
                if val:
                    if column == 'location':
                        if ',' in val:
                            val = val.replace(",", "")
                    if column == 'hireable':
                        if val:
                            val = 'true'
                        else:
                            val = 'false'
                    data.append(val)
                    # data.append(val.encode("utf-8") if type(val) == str else val)
                else:
                    data.append('')

            if column == 'company':
                companies = u_data.get('company')
                company_str = ''
                if companies:
                    companies = companies.split(' ')
                    for company in companies:
                        company_str += company.lstrip('@')
                data.append(company_str.upper())
        writer.writerow(data)

        for repo in repo_data:
            _data=[]
            for repo_column in repo_columns:
                if repo_column == 'login':
                    _data.append(user['login'])
                elif repo_column == 'license_name':
                    lic = repo.get('license')
                    if lic:
                        _val = lic.get('name', '')
                    else:
                        _val = ''

                    _data.append(_val)
                else:
                    _val = repo[repo_column]
                    if _val:
                        if repo_column in ('has_projects', 'has_wiki'):
                            if _val:
                                _val = 'true'
                            else:
                                _val = 'false'
                        _data.append(_val)
                    else:
                        _data.append('')
            repo_writer.writerow(_data)
