import re
import unicodedata
import scrapy
from jpbeetles.items import JpbeetlesItem


def split_name_row(name_row):
    s = ''.join(name_row).translate(str.maketrans({'/': '',
                               '　': '',
                               '\n': '',
                               "'": '',
                               '(': '',
                               ')': '',
                               ',': ''
                               })).strip()
    return s.split()

def get_subgenus(name_list):
    for name_index, name in enumerate(name_list):
        if name.istitle() and name_index == 1:
            return name
    return ''

def get_species(name_list):
    for name in name_list:
        if name.islower():
            return name
    return ''

def get_subspecies(name_list):
    sps = []
    for name in name_list:
        if name.islower():
            sps.append(name)
    if len(sps) >= 2:
        return sps[1]
    else:
        return ''

def get_scientific_name_author(name_list):
    elm = []
    for name_index, name in enumerate(name_list):
        if name_index == 0:
            pass
        elif name_index == 1:
            pass
        elif name.islower():
            pass
        elif name.isnumeric():
            pass
        elif unicodedata.east_asian_width(name[0]) == 'W':
            pass
        else:
            elm.append(name)
    if len(elm) == 0:
        return ''
    else:
        return ' '.join(elm)

def get_name_publishedin_year(name_list):
    for name in name_list:
        if name.isnumeric():
            return name
    return 0

def get_japanese_name(name_list):
    for name in name_list:
        if unicodedata.east_asian_width(name[0]) == 'W':
            return name
    return ''


class TaxaSpider(scrapy.Spider):
    name = 'taxa'
    allowed_domains = ['japanesebeetles.jimdofree.com']
    start_urls = ['https://japanesebeetles.jimdofree.com/目録/']

    def parse(self, response):
        for url in response.css('a::attr("href")').re(r'.*科/$'):
            yield response.follow(url, self.parse_families)

    def parse_families(self, response):
        family = response.meta.get('family')
        subfamily = ''
        tribe = ''
        subtribe = ''
        genus = ''
        subgenus = ''
        species = ''
        subspecies = ''
        scientific_name_author = ''
        name_publishedin_year = ''
        japanese_name = ''
        distribution = ''
        note = ''
        # 科ページがフラットな場合
        if family is None:
            family = response.css('.jtpl-main').css('p ::text').re(r'^Family.*')[0].split(' ')[1].capitalize()
        # ニセコブスジコガネ科のみ科表示の形式が違うので直接設定
        if response.request.url == 'https://japanesebeetles.jimdofree.com/目録/23-ニセコブスジコガネ科/':
            family = 'Glaresidae'
        links = [url for url in response.css('a::attr("href")').re(r'.*亜科/$')]
        if len(links) == 0:
            tds = []
            for row in response.xpath('//table/tbody/tr'):
                for td in row.xpath('td'):
                    texts = td.css('td ::text').extract()
                    texts.pop(0)
                    tds.append(texts)
            tds = [i for i in tds if i != []]
            for texts_index, texts in enumerate(tds):
                if texts[0] in {'番号', '学名 / 和名', '分布', '*', '備考', '\u3000\u3000'}:
                    continue
                for i in texts:
                    if 'Subfamily' in i:
                        words = i.split(' ')
                        words = [s for s in words if s != '']
                        subfamily = words[words.index('Subfamily') + 1]
                    elif 'Tribe' in i:
                        words = i.split(' ')
                        words = [s for s in words if s != '']
                        words = [s.rstrip('\n') for s in words]
                        try:
                            tribe = words[words.index('Tribe') + 1]
                        except IndexError:
                            tribe = 'Lagriini' # ハムシダマシのこの族だけ書式が違うため
                    elif 'Subtribe' in i:
                        words = i.split(' ')
                        words = [s for s in words if s != '']
                        words = [s.rstrip('\n') for s in words]
                        subtribe = words[words.index('Subtribe') + 1]
                if texts[0].replace('-', '0').isnumeric():
                    item = JpbeetlesItem()
                    item['kingdom'] = 'Animalia'
                    item['phylum'] = 'Arthropoda'
                    item['class_name'] = 'Insecta'
                    item['order'] = 'Coleoptera'
                    item['family'] = family
                    if family == 'Cupedidae' or family == 'Micromalthidae':
                        item['suborder'] = 'Archostemata'
                    elif family == 'Torridincolidae':
                        item['suborder'] = 'Myxophaga'
                    elif family == 'Gyrinidae' or family == 'Rhysodidae' or \
                         family == 'Carabidae' or family == 'Haliplidae' or \
                         family == 'Noteridae' or family == 'Dytiscidae':
                        item['suborder'] = 'Adephaga'
                    else:
                        item['suborder'] = 'Polyphaga'
                    item['subfamily'] = subfamily
                    item['tribe'] = tribe
                    item['subtribe'] = subtribe
                    item['genus'] = split_name_row(tds[texts_index + 1])[0]
                    item['subgenus'] = get_subgenus(split_name_row(tds[texts_index + 1]))
                    item['species'] = get_species(split_name_row(tds[texts_index + 1]))
                    item['subspecies'] = get_subspecies(split_name_row(tds[texts_index + 1]))
                    item['scientific_name_author'] = get_scientific_name_author(split_name_row(tds[texts_index + 1]))
                    item['name_publishedin_year'] = get_name_publishedin_year(split_name_row(tds[texts_index + 1]))
                    item['japanese_name'] = get_japanese_name(split_name_row(tds[texts_index + 1]))
                    distribution = ''.join(tds[texts_index + 2]).replace('\n', '').strip()
                    item['distribution'] = ''.join(tds[texts_index + 2]).replace('\n', '').strip()
                    item['note'] = ''.join(tds[texts_index + 4]).strip()
                    yield item
        # 科ページがネストされている場合
        else:
            for url in links:
                family = response.css('.jtpl-main').css('p ::text').re(r'^Family.*')[0].split(' ')[1].capitalize()
                yield response.follow(url, self.parse_families, meta={'family': family})