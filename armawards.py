#from juicer.utils import *
import scrapy
import MySQLdb
import requests
#DOMAIN = 'https://en.wikipedia.org'
class ArmAwards(scrapy.Spider):
    start_urls = ['https://en.wikipedia.org/wiki/32nd_Independent_Spirit_Awards']
    name = "spirit_awards_browse"
    def __init__(self, *args, **kwargs):
        super(SpiritAwards, self).__init__(*args, **kwargs)
        self.URL = 'https://en.wikipedia.org'
        self.query = "insert ignore into wiki_awards_history(award_gid, award_title, category_gid, category_title, year,\
                        location, winner_nominee, program_title, role, persons, created_at, modified_at)\
                        values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),now())"
        self.ceremony_query = 'select category_gid, category_title from award_ceremony_categories where award_id= "8" and category_title like "%s"'
        self.conn = MySQLdb.connect(user="root", host = "localhost", db="AWARDS", use_unicode=True)
        self.cur  = self.conn.cursor()

    def __del__(self):
        self.conn.close()
        self.cur.close()

    def wiki_gid(self,url):
        data = requests.get(url).text
        wiki_gi = re.findall('"wgArticleId":(\d+),', data)[0]
        sel = Selector(text=data)
        wikititle = extract_data(sel, '//div[@id="content"]/h1[@id="firstHeading"]//text()')
        wikititle = re.sub('\((.*?)\)','',wikititle)
        wikititle = wikititle.strip()
        if wiki_gi:
            wikigid = 'WIKI' + wiki_gi
            return wikigid,wikititle
    def wiki_gid_table(self, text):
        pattern_ = "%s%s%s"%('%',text,'%')
        self.cur.execute(self.ceremony_query%pattern_)
        text1 = self.cur.fetchall()
        if text1:
            text1 = text1[0]
            if len(text1) == 2:
                return text1[0], text1[1]

    def parse(self,response):
        sel =  Selector(response)
        award_title = 'Film Independent Spirit Awards'
        award_gid = 'WIKI1239235'
        year = '2017'
        location = "Santa Monica, California, United States"
        nodes = sel.xpath('//table[@class="wikitable"]')
        nodes.extend(['blank'])
        for nd in nodes:
            heading_nodes, award_nodes= [[]]*2
            if 'table class="wikitable"' in str(nd):
                heading_nodes = nd.xpath('./tr')[::2]
                award_nodes = nd.xpath('./tr')[1::2]
            else:
                heading_nodes = sel.xpath("//h3[preceding-sibling::h2[span[contains(text(),'Special Awards')]] and following-sibling::h2[span[contains(text(),'References')]]]")
                award_nodes = sel.xpath("//ul[preceding-sibling::h2[span[contains(text(),'Special Awards')]] and following-sibling::h2[span[contains(text(),'References')]]]")

            for (i,j) in zip (heading_nodes,award_nodes):
                if 'table class="wikitable"' in str(nd):
                    first = i.xpath('./th')
                    second = j.xpath('./td')
                else:
                    first = [i]
                    second = [j]
                if len(first) == len(second):
                    for (f,s) in zip(first,second):
                        category_link, category_link_text = ['']*2
                        if 'table class="wikitable"' in str(nd):
                            category_link = f.xpath('./a/@href').extract()
                            category_link_text = textify(f.xpath('./a/text()').extract())
                        else:
                            category_link = i.xpath('./span/a[not(contains(@href,"edit&section"))]/@href').extract()
                            category_link_text = textify(i.xpath('./span/text()').extract()) 
                            s = j
                        if category_link:
                            category_link = [category_link[0]]
                        if category_link: category_gid = self.wiki_gid(DOMAIN+textify(category_link))
                        else:
                            if category_link_text:
                                category_gid = self.wiki_gid_table(category_link_text)
                        if 'table class="wikitable"' in str(nd):
                            music_awar_list = s.xpath('./ul/li')
                        else:
                            music_awar_list = s.xpath('./li')
                        for i in music_awar_list:
                            winner_type = ''
                            if '<b>' in str(i.xpath('./self::node()')):
                                winner_type = 'winner'
                            else:
                                winner_type = 'nominee'
                            whole_txt = textify(i.xpath('.//text()').extract())
                            program_link, befor_lks, role_link, song_title = [],[],[],[]
                            if ' as ' in whole_txt and u'\u2013' in whole_txt:
                                program_link = i.xpath('./i/a[@title]/@href').extract()
                                song_title = i.xpath('./text()[contains(.,"(")]/preceding-sibling::a/@href').extract()
                                #befor_lks = i.xpath('./text()[contains(.,"(")]/following-sibling::a/@href').extract()
                                befor_lks = i.xpath('./i//../preceding-sibling::a/@href').extract()
                                if not song_title:
                                    song_title = i.xpath('./text()[contains(.,")")]/preceding-sibling::text()').extract()
                                    if song_title:
                                        song_title = [song_title[0]]
                                if ' as ' in whole_txt:
                                    role_link = i.xpath('./text()[contains(.," as ")]/following-sibling::a/@href').extract()
                                    if not role_link:
                                        role_link = i.xpath('./i/following-sibling::text()').extract()
                            elif u'\u2013' in whole_txt:
                                program_link = i.xpath('./i/a[@title]/@href').extract()
                                if not program_link:
                                     program_link = i.xpath('./i/text()').extract()
                                befor_lks = i.xpath('./i//../following-sibling::a/@href').extract()
                                another_be = i.xpath('./text()[contains(.,"%s")]'%u"\u2013").extract()
                                if another_be:
                                    befor_lks.extend(another_be)
                                checkcon = i.xpath('./text()[contains(.," and ")]').extract()
                                if checkcon:
                                    befor_lks.extend(checkcon)
                                befor_an = i.xpath('./i//../preceding-sibling::a/@href').extract()
                                if befor_an:
                                    befor_lks.extend(befor_an)
                            else:
                                program_link = i.xpath('.//a[@title]/@href').extract()
                                if program_link:
                                    program_link = [program_link[0]]
                                else:
                                    program_link = i.xpath('./i/text()').extract()
                            final_persons_withgid,final_programs_withgid, roles_withgid, songswith_gid = [],[],[],[]
                            list_fin = []
                            list_fin.append(('program',set(program_link)))
                            list_fin.append(('person', set(befor_lks)))
                            list_fin.append(('role', set(role_link)))
                            for fper in list_fin:
                                for fpro in fper[1]:
                                    if "/wiki/" in fpro:
                                        wikiwith = self.wiki_gid(DOMAIN+fpro)
                                        name = wikiwith[1].strip() + '{%s}' %wikiwith[0].strip()
                                        name = re.sub('\((.*?)\)','',name)
                                        name = name.strip()
                                        if 'program' in fper[0]:
                                            if name: final_programs_withgid.append(name)
                                        if 'person' in fper[0]:
                                            if name: final_persons_withgid.append(name)
                                        if 'role' in fper[0]:
                                            if name: roles_withgid.append(name)
                                    else:
                                        if 'program' in fper[0]: 
                                            if fpro: final_programs_withgid.append(self.clean(fpro))
                                        if 'person' in fper[0]:
                                            if fpro: final_persons_withgid.append(self.clean(fpro))
                                        if 'role' in fper[0]:
                                            if fpro: roles_withgid.append(self.clean(fpro).replace(' / ','<>').replace('/','<>'))
                            final_persons_withgid = [ik for ik in final_persons_withgid if ik != '']
                            final_programs_withgid = [ik for ik in final_programs_withgid if ik != '']
                            roles_withgid = [ik for ik in roles_withgid if ik != '']
                            if final_persons_withgid == []: final_persons_withgi  = ''
                            if final_programs_withgid == []: final_programs_withgid = ''
                            if roles_withgid == []: roles_withgid = ''
                            if songswith_gid == []: songswith_gid = ''
                            program_check = '<>'.join(final_programs_withgid).strip('<>')
                            values  =( (normalize(award_gid)),normalize(award_title),normalize(category_gid[0]),normalize(category_gid[1]),'2017',normalize(location),normalize(winner_type),normalize(program_check.strip().replace('<><>','<>')),normalize(''.join(roles_withgid).replace('<><>','<>')),normalize('<>'.join(final_persons_withgid).replace('<><>','<>').strip('<>')))
                            self.cur.execute(self.query, values)
                            #dic.update({'award_gid':award_gid,'award_title':award_title,'category_gid':category_gid[0],'category_title':category_gid[1],'year':'2017','location':location,'winner_nominee':winner_type,"program_title":'<>'.join(final_programs_withgid).strip('<>'),"role":''.join(roles_withgid),"persons":'<>'.join(final_persons_withgid).strip('<>')})
                            print values
                            #file("goldenglobe","ab+").write("%s\n" %dic)
                                    
    def clean(self, text1):
        text1 = text1.replace(' and ',',')
        text1 = re.sub('\((.*?)\)','',text1)
        text1 = text1.split(',')
        text_list = []
        for text in text1:
            text = text.strip().replace(' and ','').replace(' as ','').replace(u'\u2013','').strip().replace('<>','').replace('(','').strip().replace('as ','').replace('*Nominees to be determined*','').strip()
            text = re.sub('\((.*?)\)','',text)
            text = text.strip()
            if text:
                text_list.append(text)
        return '<>'.join(text_list)
        
                            
                            
                            
                        
 
                            
							
								

