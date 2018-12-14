import scrapy
import requests
import json


class YahooSingapore(scrapy.Spider):
    name = "yahoo_sg"
    start_urls = ["https://sg.news.yahoo.com/singapore"]

    def parse(self, response):
        headers = {
            'origin': 'https://sg.news.yahoo.com',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,te;q=0.8',
            'x-requested-with': 'XMLHttpRequest',
            'cookie': 'B=co2ua4he0s065&b=3&s=k8; GUCS=AdtcM29f; GUC=AQEBAQFcD0lc70IfLAQa&s=AQAAAAcJi-Jo&g=XA4BNg; cmp=t=1544421690&j=0',
            'pragma': 'no-cache',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'content-type': 'application/json',
            'accept': '*/*',
            'cache-control': 'no-cache',
            'authority': 'sg.news.yahoo.com',
            'referer': 'https://sg.news.yahoo.com/singapore',
        }

        params = (
            ('bkt', 'news-SG-en-SG-def'),
            ('crumb', 'Jkw5JpfDv3R'),
            ('device', 'desktop'),
            ('feature', 'cacheContentCanvas,enableGDPRFooter,enableCMP,enableConsentData,enableGuceJs,enableGuceJsOverlay,videoDocking,newContentAttribution,livecoverage,enableVideoMicrodata,newsVideo,deferModalCluster,clusterBackfill,hideLREC2Singleton'),
            ('intl', 'sg'),
            ('lang', 'en-SG'),
            ('partner', 'none'),
            ('prid', '3guqm19e0s0aa'),
            ('region', 'SG'),
            ('site', 'news'),
            ('tz', 'Asia/Kolkata'),
            ('ver', '0.0.3548'),
        )
        fr = "".join(response.xpath('//script[contains(text(), "(function (root)")]//text()').extract())
        dt = fr.replace('\n', '').replace('\r', '').rstrip(";")
        dt = fr.replace('\n', '').replace('\r', '').rstrip(";").replace(';}(this))','').replace("(function (root) {/* -- Data -- */root.App || (root.App = {});root.App.now = 1544423892587;root.App.main = ",'')


        import pdb;pdb.set_trace()
        data = '{"requests":{"g0":{"resource":"StreamService.items","operation":"read","params":{"ui":{"comments":true,"comments_offnet":true,"dispatch_content_store":true,"editorial_featured_count":1,"image_quality_override":true,"link_out_allowed":true,"needtoknow_template":"carousel","ntk_bypassA3c":true,"pubtime_maxage":-1,"relative_links":true,"show_comment_count":true,"smart_crop":true,"storyline_count":2,"storyline_enabled":true,"storyline_min":2,"summary":true,"thumbnail_size":100,"tiles":{"allowPartialRows":true,"doubleTallStart":0,"featured_label":false,"gradient":false,"height":175,"resizeImages":false,"textOnly":[{"backgroundColor":"#fff","foregroundColor":"#000"}],"width_max":300,"width_min":200},"view":"mega"},"category":"LISTID:7b5e7745-f19f-44b3-9454-1dc24b6015fc","forceJpg":true,"offnet":{"include_lcp":true},"subtype_enabled":true,"use_content_site":true,"use_mags_nydc":true,"content_site":"news","pageContext":{"site":"news","pageType":"section","renderTarget":"default"},"uuids":["48bb1c1e-89e7-31d5-a076-2745cef3fac9","35355ead-fd81-38bc-b686-a594c3a20ac4","fdc91708-67b3-365a-9fb1-a45fa165e204","0a91f4ef-8f7a-3ce1-8e36-d4b46982d30c","12539967-0dc7-3b36-8f48-c1c4f093d237","4cfd783d-5b0c-3ef8-9530-61867e32dd75","b2e31a38-0be7-376a-8bf0-6cd6a4f2c239","8ba6ff5a-1a6a-34f0-a818-c21271e22635","943667a1-e744-3d34-9826-10ec42457f99","8e08a2fa-54bf-3735-b6d9-366c8272e233","9f6cb77e-ccd8-324e-9c58-ab624c98c6fa","3430b8c5-e5f1-3841-ac56-da0ef7d22fd7","a9e08574-bba2-3b93-80dd-cdcca211f0af","0b3e8d65-7482-3f16-beaf-d2e911eda539","733bcfa6-38e8-35d3-bb1e-bf564a57262a"]}}},"context":{"feature":"cacheContentCanvas,enableGDPRFooter,enableCMP,enableConsentData,enableGuceJs,enableGuceJsOverlay,videoDocking,newContentAttribution,livecoverage,enableVideoMicrodata,newsVideo,deferModalCluster,clusterBackfill,hideLREC2Singleton","bkt":"news-SG-en-SG-def","crumb":"Jkw5JpfDv3R","device":"desktop","intl":"sg","lang":"en-SG","partner":"none","prid":"3guqm19e0s0aa","region":"SG","site":"news","tz":"Asia/Kolkata","ver":"0.0.3548"}}'
        data_ = json.loads(response.text)
        #hj = data_.get('g0','')
        url_ = hj.get('data','')
        gt = url_.get(u'stream_items','')
        for i  in gt:
            response = requests.post('https://sg.news.yahoo.com/_td/api/resource', headers=headers, params=params, data=data)

        import pdb;pdb.set_trace()
        #NB. Original query string below. It seems impossible to parse and
        #reproduce query strings 100% accurately so the one below is given
        #in case the reproduced version is not "correct".
        # response = requests.post('https://sg.news.yahoo.com/_td/api/resource?bkt=news-SG-en-SG-def&crumb=Jkw5JpfDv3R&device=desktop&feature=cacheContentCanvas%2CenableGDPRFooter%2CenableCMP%2CenableConsentData%2CenableGuceJs%2CenableGuceJsOverlay%2CvideoDocking%2CnewContentAttribution%2Clivecoverage%2CenableVideoMicrodata%2CnewsVideo%2CdeferModalCluster%2CclusterBackfill%2ChideLREC2Singleton&intl=sg&lang=en-SG&partner=none&prid=3guqm19e0s0aa&region=SG&site=news&tz=Asia%2FKolkata&ver=0.0.3548', headers=headers, data=data)

