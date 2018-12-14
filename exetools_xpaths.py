thread_title_xpath = '//td[@class="navbar"]//text()'
thread_topic_xpath = '//span[@class="navbar"]//text()'
all_posts_xpath = '//div[@id="posts"]//div[@align="center"]'
posted_url_xpath = '//td[@class="thead"]//div[@class="normal"]//a//@href'
posted_time_xpath = '//td[@class="thead"]//div[@class="normal"]//following-sibling::text()'
author_xpath = '//a[@class="bigusername"]//text()'
author_url_xpath = '//a[@class="bigusername"]//@href'
comment_xpath = '//tr//td[@id="%s"]//text() | //img//@title | //tr//td[@id="%s"]//div[@class="smallfont"]//@alt'
links_xpath = '//tr//td[@id="%s"]//div[@id="post_message_%s"]//a//@href'
posts_xpath = '//div[@class="smallfont"]//div[contains(text(), "Posts:")]//text()'
activetime_xpath = '//div[a[contains(@name, "post")]]//text()'
auth_sig_xpath = '//tr//td[contains(@id, "td_post_")]//div[contains(@id, "post_message_")]/following-sibling::div//text() | //tr//td[contains(@id, "td_post_")]//div[contains(@id, "post_message_")]/following-sibling::div//img[@title]//@title'
arrow_xpath = '//a[@rel="nofollow"]//img[@class="inlineimg"]/@alt'

ref_url_xpath  = '//a[@class="bigusername"]/@href'
join_date_xpath = '//div[contains(text(), "Join Date:")]//text()'
reputation_xpath = '//div[@class="smallfont"]//div[contains(text(), "Rept. Rcvd")]//text()'
group_xp_xpath = '//div[@id="postmenu_%s"]//following-sibling::div[@class="smallfont"]//text()'
next_page_xpath = '//td[@class="alt1"]//a[contains(@rel, "next")]//@href'

urls = ['https://forum.exetools.com/showthread.php?t=15279',
         'https://forum.exetools.com/showthread.php?t=14329',
         'https://forum.exetools.com/showthread.php?t=13074',
         'https://forum.exetools.com/showthread.php?t=18906',
         'https://forum.exetools.com/showthread.php?t=18937',
         'https://forum.exetools.com/showthread.php?t=18914',
         'https://forum.exetools.com/showthread.php?t=18785',
         'https://forum.exetools.com/showthread.php?t=18926']

#urls = ["https://forum.exetools.com/showthread.php?t=15279"]

site_domain = 'https://forum.exetools.com/'

