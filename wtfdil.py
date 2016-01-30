from itertools import groupby
from requests.auth import HTTPBasicAuth
import json
import requests
import sys


def main(username, password):
    """Main."""
    basic_auth = HTTPBasicAuth(username, password)
    starred_repos = {}
    page = 0
    while True:
        starred_url = 'https://api.github.com/users/{}/starred?page={}'

        response = requests.get(
            starred_url.format(username, page),
            auth=basic_auth,
        )
        print(response)
        if response.status_code != 200 or response.content == '[]':
            print(response.content)
            break

        starred = json.loads(response.content)
        for star in starred:
            text = u'* [{}]({}) {}\n'.format(
                star['full_name'],
                star['html_url'],
                star['description'],
            ).encode('utf-8')
            print(text)

            starred_repos[star['full_name']] = star

        page = page + 1

    return groupby(
        sorted(starred_repos.values(), key=lambda x: x['language']),
        lambda x: x['language'],
    )


if __name__ == '__main__':
    with open('README.md', 'w') as file:
        file.write("""# wtfdil

What the F*** did I learn?

## Usage

```bash
pip install requests
python wtfdil.py `username` `password`
```

""")

    with open('README.md', 'a') as file:
        if (len(sys.argv) < 3):
            username = raw_input('Enter GitHub username or email: ')
            password = raw_input('Enter password: ')
        else:
            username = sys.argv[1]
            password = sys.argv[2]

        group_repos = main(username, password)

        statistics_string = """## Statistics

| Language | number of repos |
|----------|-----------------|
"""
        repos_string = ""

        for key, group in group_repos:
            repos_sorted = sorted(group, key=lambda x: x['stargazers_count'], reverse=True)

            language = key if key else 'Others'
            statistics_string += u'| {} | {} |\n'.format(
                language, ':white_medium_small_square:' * len(repos_sorted)
            ).encode('utf-8')
            repos_string += "### {}\n\n".format(language)

            for repo in repos_sorted:
                repos_string += u'* {} [{}]({}) {}\n'.format(
                    ':zap:' * (repo['stargazers_count'] / 5000),
                    repo['full_name'],
                    repo['html_url'],
                    repo['description'],
                ).encode('utf-8')
            repos_string += "\n"

        file.write(statistics_string)
        file.write(repos_string)
