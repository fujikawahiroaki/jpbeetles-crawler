import re
import scrapy
from jpbeetles.items import JpbeetlesItem

class TaxaSpider(scrapy.Spider):
    name = 'taxa'
    allowed_domains = ['japanesebeetles.jimdofree.com']
    start_urls = ['https://japanesebeetles.jimdofree.com/目録/']

    def parse(self, response):
        for url in response.css('a::attr("href")').re(r'^/目録/\d.*'):
            yield response.follow(url, self.parse_families)

    def parse_families(self, response):
        family = ''
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
        family = response.css('.jtpl-main').css('p ::text').re(r'^Family.*')[0].split(' ')[1].capitalize()
        try: # 亜科ページがフラットな場合
            response.css('.jtpl-main').css('tr ::text').re(r'.*Subfamily.*')[0].split(' ')[2].capitalize()
            for row in response.xpath('//table/tbody/tr'):
                pair_counter = 0
                one_taxa = {'index': '',
                                'name': '',
                                'dist': '',
                                'zukan': '',
                                'note': ''
                                }
                for td in row.xpath('td'):
                    texts = td.css('td ::text').extract()
                    texts.pop(0)
                    if texts[0] in {'番号', '学名 / 和名', '分布', '*', '備考', '\u3000\u3000', '\u3000\u3000\u3000\u3000'}:
                        continue
                    for i in texts:
                        if 'Subfamily' in i:
                            words = i.split(' ')
                            words = [s for s in words if s != '']
                            subfamily = words[words.index('Subfamily') + 1]
                            print(subfamily)
                            continue
                        elif 'Tribe' in i:
                            words = i.split(' ')
                            words = [s for s in words if s != '']
                            words = [s.rstrip('\n') for s in words]
                            tribe = words[words.index('Tribe') + 1]
                            print('Tribe')
                            print(tribe)
                            continue
                        elif 'Subtribe' in i:
                            words = i.split(' ')
                            words = [s for s in words if s != '']
                            words = [s.rstrip('\n') for s in words]
                            subtribe = words[words.index('Subtribe') + 1]
                            print('Subtribe')
                            print(subtribe)
                            continue
                    texts = [s for s in texts if not '\n' in s]
                    print(f"texts: {texts}")
                    print(texts[0].replace('-', '0').isnumeric())
                    print(f"pair_counter: {pair_counter}")
                    if texts[0].replace('-', '0').isnumeric():
                        if pair_counter == 0:
                            one_taxa['index'] = texts
                            pair_counter += 1
                            continue
                    if pair_counter == 1:
                        one_taxa['name'] = texts
                        pair_counter += 1
                        continue
                    elif pair_counter == 2:
                        one_taxa['dist'] = texts
                        pair_counter += 1
                        continue
                    elif pair_counter == 3:
                        one_taxa['zukan'] = texts
                        pair_counter += 1
                        continue
                    elif pair_counter == 4:
                        one_taxa['note'] = texts
                        pair_counter = 0
                        continue
                print(f"one_taxa: {one_taxa}")
                print('\n\n\n')
                
        except IndexError: # 亜科ページがネストされている場合
            
            pass