import requests
import xml.etree.ElementTree as ET
import sys

def article_info(cod):
    title_path = './front/article-meta/title-group/article-title'
    author_path = './front/article-meta/contrib-group/contrib'

    r = requests.get('http://www.scielo.br/scieloOrg/php/articleXML.php',
            params={'pid':cod})
    root = ET.fromstring(r.text.encode('iso8859-1'))
    print('\n')
    print('Title:')
    print(root.find(title_path).text + '\n')

    authors = root.findall(author_path)
    print('Authors:')
    for author in authors:
        print author[0][1].text, author[0][0].text

article_info(sys.argv[1])
