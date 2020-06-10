import json
import os
import errno

import httpx
from bs4 import BeautifulSoup

protocol = 'https'
base_url = protocol + '://monsterhunterworld.wiki.fextralife.com'
search_quest = 'The Great Glutton'
search_page_url = base_url + '/' + '+'.join(search_quest.split())
client = httpx.Client()
response = client.get(search_page_url)

if response.status_code != 200:
    print('Failed to lookup quest list: ' + str(response.status_code))
    exit(1)

# TODO: Is it worth including lxml package?
soup = BeautifulSoup(response.text, 'lxml')
all_quest_a_tags = soup.select('div#tagged-pages-container > a.wiki_link')
quests = {
    q.text: {
        'link': f'{protocol}:{q["href"]}'
    } for q in all_quest_a_tags
}
quests[search_quest] = {
    'link': search_page_url
}

for key in quests:
    response = client.get(quests[key]['link'])
    if response.status_code != 200:
        print(f'failed to lookup info for quest [{key}] at [{quests[key]["link"]}]')
        exit(1)

    soup = BeautifulSoup(response.text, 'lxml')

    category_results = soup.select('#breadcrumbs-container > a:last-of-type')
    if len(category_results) == 1:
        quests[key]['category'] = category_results[0].text
    else:
        print(
            f'unexpected category_results length [{len(category_results)}] for quest [{key}] at [{quests[key]["link"]}]')

    info = {}
    content_block = soup.find(id='wiki-content-block')
    if content_block is not None:
        title = ''
        quote = content_block.find('blockquote')
        if quote is not None:
            quests[key]['quote'] = quote.text
            info_tags = quote.next_siblings
        else:
            # this is kinda hacky (surprise, suprise), but we want a list of siblings, *including* the first h3.bonfire
            first_h3 = content_block.find('h3', class_='bonfire')
            if first_h3 is not None:
                previous = first_h3.previous_sibling
                info_tags = previous.next_siblings
            else:
                info_tags = []
        for tag in info_tags:
            # stop when we hit the 'Quests' table
            if tag.name == 'div':
                break
            if tag.name == 'h3':
                title = tag.text
            # filter NavigableStrings
            elif tag.name is not None and len(title) > 0:
                # filter empty sections
                if not tag.text.endswith('goes here.'):
                    info[title] = info.get(title, [])
                    info[title].append(tag.text)

    quests[key]['info'] = info

path = '../data/quests.json'
if not os.path.exists(os.path.dirname(path)):
    try:
        os.makedirs(os.path.dirname(path))
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

with open(path, 'w') as f:
    json.dump(quests, f, indent=4)
