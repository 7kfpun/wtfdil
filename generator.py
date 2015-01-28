import json
import requests
import sys


def main(username):
    page = 0
    while True:
        url = 'https://api.github.com/users/{}/starred?page={}'.format(username, page)  # noqa

        response = requests.get(url)
        print(response)
        if response.status_code != 200 or response.content == '[]':
            print(response.content)
            return True

        with open('README.md', 'a') as file:
            starred = json.loads(response.content)
            for star in starred:
                text = u'* [{}]({}) {}\n'.format(
                    star['full_name'],
                    star['html_url'],
                    star['description'],
                ).encode('utf-8')
                file.write(text)

        page = page + 1


if __name__ == '__main__':
    with open('README.md', 'w') as file:
        file.write("# wtfil\n\nWhat the F*** I learnt.\n")

    main(sys.argv[1])
