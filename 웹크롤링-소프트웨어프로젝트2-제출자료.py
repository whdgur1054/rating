from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pymysql
import datetime
import time
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import emoji

conn = pymysql.connect(host = '######',     #MySQL 연결
                       user = '#####', password = '#####',
                       db = '####', charset='utf8mb4')
curs = conn.cursor()
print("\n\n")
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.set_page_load_timeout(10)
page = 1
url = "https://www.metacritic.com/browse/games/release-date/available/xboxone/date"
#"https://www.metacritic.com/browse/games/release-date/available/xboxone/date"  #xbox   주소
#"https://www.metacritic.com/browse/games/release-date/available/switch/date"   #switch 주소
#"https://www.metacritic.com/browse/games/release-date/available/ps4/date"      #ps4    주소

    
while (1):
    data = "%d page\n" %(page)          #몇번째 페이지인지 진행을 보기위해 
    f = open("Xbox_One_page_log.txt", 'a',-1,"utf-8")       # 크롤링을 진행하는것을 계속 보기 어려워 파일에 진행상황을 저장함.
    f.write(data)
    f.close()
    print("\n\n**********" + str(page) + "번째 페이지 **********\n\n")       #출력창에 몇번째 페이지 진입중인지 출력
    driver.get(url)
    bsObject = BeautifulSoup(driver.page_source, 'html.parser')

    game_list = driver.find_elements_by_class_name("clamp-image-wrap")
    urls = []
    for i in game_list :
        urls.append(i.find_element_by_css_selector('a').get_attribute('href'))      #해당 페이지 내에 존재하는 게임 목록들을 href주소만 따로 urls 리스트에 저장함.
    for i in urls:
        title = ''          #초기값 설정
        meta_score = 0
        user_score = 0
        user_num = 0
        publisher = ''
        image_url = ''
        developer = ''
        release_date = ''
        genre = ''
        desc = ''
        
        print("--------------------------------")
        driver.get(i)
        bsObject = BeautifulSoup(driver.page_source, 'html.parser')
        try:                #타이틀 받아오기
            title = driver.find_element_by_css_selector("#main > div > div:nth-child(1) > div.left > div.content_head.product_content_head.game_content_head > div.product_title > a > h1").text
        except:
            continue
        print(title)        
        
        try:            #메타스코어 받아오기
            metascore = bsObject.find('div' ,{'class' : "metascore_wrap highlight_metascore"}).get_text().replace("\t","").replace("  ","").replace("\n",";")[12:]
            index = metascore.find(";")
            metascore = metascore[:index]
            print(metascore)
        except:
            meta_score = 0
        if(meta_score == "tbd"):    meta_score = 0
        print(meta_score)

        try:    #유저평점 받아오기
            user_score = bsObject.find('div' ,{'class' : "userscore_wrap feature_userscore"}).get_text().replace("\t","").replace("  ","").replace("\n",";")[13:]
            index = user_score.find(";")
            user_score = user_score[:index]
        except:
            user_score = 0

        if (user_score == "tbd"):   #유저평점이 tbd(미정)일경우 0점으로 대체
            user_score = 0
        else:
            user_score = int(float(user_score) * 10)
            
        print(user_score)

        if (user_score != 0) :    #평가인원 받아오기
            try:
                user_num = driver.find_element_by_css_selector("""#main > div > div:nth-child(1) > div.left > div.module.product_data.product_data_summary >
                        div > div.summary_wrap > div.section.product_scores > div.details.side_details > div:nth-child(1) > div > div.summary > p > span.count > a""").text
            except:
                user_num = driver.find_element_by_css_selector("""#main > div > div:nth-child(1) > div.left > div.with_trailer > div > div > div.summary_wrap >
                        div.section.product_scores > div.details.side_details > div:nth-child(1) > div > div.summary > p > span.count > a""").text
        if(user_num != 0):
            index = user_num.find("R")
            user_num = int(user_num[:index])
        print(user_num)
        
        try:    #배급사 받아오기
            publisher = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div[1]/div/div/div/div/div/div/div/div/div[1]/div[1]/div[1]/div[3]/ul/li[1]/span[2]/a").text
        except:
            publisher = ""
        release_date = bsObject.find('li' ,{'class' : "summary_detail release_data"}).get_text()[15:].replace("\n","")  #출시날짜
        print(release_date)     #초기 날짜 데이터
        release_date = datetime.datetime.strptime(release_date, "%b %d, %Y")        #출시날짜를 datetime 구조에 맞도록 변화시킴
        print(release_date)     #가공 날짜 데이터
        
        try:    #이미지url 받아오기
            image_url = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div[1]/div/div/div/div/div/div/div/div/div[1]/div[1]/div[3]/div/div[1]/div/img").get_attribute('src')
        except:
            image_url = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div[1]/div/div/div/div/div/div/div/div/div[1]/div[1]/div[3]/div/div/div[1]/div/img").get_attribute('src')
        print(image_url)
        
        try:    #개발사 받아오기
            developer = driver.find_element_by_xpath("/html/body/div/div[2]/div[1]/div[1]/div/div/div/div/div/div/div/div/div[1]/div[1]/div[3]/div/div[2]/div[2]/div[2]/ul/li[1]/span[2]").text
        except:
            try:
                developer = driver.find_element_by_xpath("/html/body/div/div[2]/div[1]/div[1]/div/div/div/div/div/div/div/div/div[1]/div[1]/div[3]/div/div/div[2]/div[2]/div[2]/ul/li[1]/span[2]").text
            except:
                developer = ""
        print(developer)

        #장르 받아오기
        genre = bsObject.find('li' ,{'class' : "summary_detail product_genre"}).get_text()[10:].replace(" ","").replace(",",";")
            
        print(genre)    


        try:    #설명출력 (Expand 클릭)
            driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div[1]/div/div/div/div/div/div/div/div/div[1]/div[1]/div[3]/div/div[2]/div[2]/div[1]/ul/li/span[2]/span/span[4]").click()
        except:
            try:
                driver.find_element_by_xpath("/html/body/div/div[2]/div[1]/div[1]/div/div/div/div/div/div/div/div/div[1]/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/ul/li/span[2]/span/span[4]").click()
            except:
                pass
            
        try:    #설명 받아오기
            desc = driver.find_element_by_xpath("/html/body/div/div[2]/div[1]/div[1]/div/div/div/div/div/div/div/div/div[1]/div[1]/div[3]/div/div[2]/div[2]/div[1]/ul/li/span[2]/span/span[2]").text
            print(1)
        except :    
            try:
                desc = driver.find_element_by_xpath("/html/body/div/div[2]/div[1]/div[1]/div/div/div/div/div/div/div/div/div[1]/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/ul/li/span[2]/span/span[2]").text
                print(2)
            except:
                try:                
                    desc = driver.find_element_by_xpath("/html/body/div/div[2]/div[1]/div[1]/div/div/div/div/div/div/div/div/div[1]/div[1]/div[3]/div/div/div[2]/div[2]/div[1]/ul/li/span[2]/span/span[1]").text
                    print(3)
                except:
                    try:
                        desc = driver.find_element_by_css_selector("#main > div > div:nth-child(1) > div.left > div.module.product_data.product_data_summary > div > div.summary_wrap > div.section.product_details > div.details.main_details > ul > li > span.data > span").text
                        print(4)
                    except:
                        desc = ""
                        print(5)
        print(desc)

        link = i #관련링크(현재링크) 받아오기
        print("\n" + link)
        
        try:            #크롤링한 데이터를 mysql에 입력하는 부분
                                                        #id           #type  #price                                     를 의미
            sql = "insert ignore into game_info values (NULL,%s, %s, \'GAME\', 0, %s, %s, %s, %s, %s, %s, %s, %s, %s)" 
            curs.execute(sql, (title, image_url, developer, publisher, release_date, user_score, user_num, meta_score, desc, url,genre))
            conn.commit()
        except Exception as e:
            print(e)
            data = "Error line ...  Sql error : %s" %(e)        #에러가 날 경우 어떠한 에러가 났는지 기록
            f = open("ERROR.txt", 'a',-1,"utf-8")
            f.write(data)
            f.close()
    url = "https://www.metacritic.com/browse/games/release-date/available/xboxone/date?page=" + str(page)   #다음페이지로 넘어감
    page = page + 1
    
conn.close()
