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
        language_url = 'https://api.github.com/repos/{}/languages'

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

            language_response = requests.get(
                language_url.format(star['full_name']),
                auth=basic_auth,
            )

            if language_response.status_code != 200 or language_response.content == '[]':  # noqa
                print(language_response.content)
                starred_repos[star['full_name']]['language'] = json.loads(language_response.content)  # noqa

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
        for key, group in group_repos:
            language = key if key else 'Others'
            file.write("### {}\n\n".format(language))
            for repo in group:
                text = u'* [{}]({}) {}\n'.format(
                    repo['full_name'],
                    repo['html_url'],
                    repo['description'],
                ).encode('utf-8')
                file.write(text)
            file.write("\n")
