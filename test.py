from main import get_page
from bs4 import BeautifulSoup as bs

news_page = get_page('https://www.sports.ru/football/1103333463-xakan-chalxanoglu-priznatelen-milanu-no-mne-nuzhen-byl-novyj-vyzov-ni-.html')
soup = bs(news_page, 'lxml')
for p in soup.find_all(itemprop="articleBody"):
    print(p.get_text())