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

conn = pymysql.connect(host = 'localhost', user = 'test', password = 'testing',
                       db = 'test2', charset='utf8mb4')
curs = conn.cursor()
#sql = "select * from game_info"
#curs.execute(sql)

#rows = curs.fetchall()
#print(rows)

print("\n\n")

#url = "https://store.steampowered.com/app/397540"
#driver = webdriver.Chrome()
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.set_page_load_timeout(10)
#driver.implicitly_wait(5)


f_r = open("applist.txt",'r')
lines = f_r.readlines()


def setting():
        
    url = "https://store.steampowered.com/app/" + "550"
    driver.get(url)
    bsObject = BeautifulSoup(driver.page_source, 'html.parser')

    dayField = driver.find_element_by_id("ageDay")
    dayField.send_keys("11")
    monthField = driver.find_element_by_id("ageMonth")
    monthField.send_keys("Octorber")
    yearField = driver.find_element_by_id("ageYear")
    yearField.send_keys("1995", Keys.TAB, Keys.ENTER)


    url = "https://store.steampowered.com/app/" + "550"
    driver.get(url)
    bsObject = BeautifulSoup(driver.page_source, 'html.parser')
    language = driver.find_element_by_id("language_pulldown")
    language.click()
    driver.find_element_by_xpath('//*[@onclick="ChangeLanguage( \'koreana\' ); return false;"]').click()
    driver.implicitly_wait(15)
    time.sleep(1)


setting()

for i in range(20000,20000):
    url = "https://store.steampowered.com/app/" + lines[i]
    try:
        driver.get(url)
    except TimeoutException as e:
        i+=1
        print("***************%d" %i)
        continue
    bsObject = BeautifulSoup(driver.page_source, 'html.parser')
    print("\t*****%d*****" %i)

    data = "\n**%d" %i
    f = open("ERROR.txt", 'a',-1,"utf-8")
    f.write(data)
    f.close()
    
    try:                                                                                                    #Get_Title
        title = bsObject.find('div',{'class' : "apphub_AppName"}).get_text()
        dev_row = bsObject.find_all('div',{'class' : "dev_row"})
    except Exception as e:
        title_name = bsObject.head.title.get_text()
        if(title_name != "Steam에 오신 것을 환영합니다"):
            print ("\t**** ERROR PAGE ****")
            data = "Error : %d line...  Error Page : %s" %(i,e)
            f = open("ERROR.txt", 'a',-1,"utf-8")
            f.write(data)
            f.close()
        continue
    
    try:                                                                                                    #Get_Price
        price = int (bsObject.find('div',{'class' : "game_area_purchase_game_wrapper"}).find('div',{'class' : "discount_original_price"}).get_text().replace(",","")[2:])
    except Exception as e:  #game_purchase_price price
        try:
            price = int (bsObject.find('div',{'class' : "game_area_purchase_game_wrapper"}).find('div',{'class' : "game_purchase_price price"}).get_text().strip().replace(",","")[2:])
        except:
            price = 0

    print(title)
    print(price)
    #print(dev_row)

                                                                                                            #TypeChecking
    type = bsObject.find('div' ,{'class' : "blockbg"}).get_text()
    #print(type)
    if(type.find("모든 게임")>0):
        if(type.find("다운로드 가능한 콘텐츠")>0):
            print("DLC")
            type = "DLC"
        else:
            print("GAME")
            type = "GAME"
    elif(type.find("모든 소프트웨어")>0):
        print("Software")
        continue
    elif(type.find("모든 사운드트랙")>0):
        print("soundtrack")
        continue
    elif(type.find("모든 비디오")>0):
        print("Video")
        continue
    elif(type.find("디자인과 일러스트레이션")>0):
        print("Design")
        continue
        
    try:                                                                                                    #Get_Publisher and Developer
        dev = dev_row[2].text.rstrip('\n')
        temp = dev.find(":")
        dev = dev[temp+1:].strip()
    except:
        dev = ""
    print(dev)
    
    try:
        pub = dev_row[3].text
        temp = pub.find(":")
        pub = pub[temp+1:].strip()
    except:
        pub=""
    print(pub)
    
    try:                                                                                                    #Get_ReleaseDate
        release = bsObject.find('div',{'class' : 'date'}).get_text()
        release = datetime.datetime.strptime(release, '%Y년 %m월 %d일').date()
    except:
        try:
            release = datetime.datetime.strptime(release, '%Y년 %b월').date()
        except:
            try:
                if(bsObject.find('div',{'class' : 'date'}).get_text().find('TSD')):
                    release = datetime.datetime.strptime('2999-12-31', '%Y-%m-%d')
            except:
                release = 00000000
    print("%s" %release)


    try:                                                                                                    #Get_Description
        desc = bsObject.find('div', {'class' : "game_description_snippet"}).get_text().strip()
    except:
        desc = ""
    print(desc)

    try:
        genre_all = bsObject.find('div',{'class' :"glance_tags popular_tags"}).get_text().replace("\t","")
        genre_all = genre_all[1:].lstrip("\n").replace("\n","|").replace("+","")
        #print(genre_all)
    except:
        genre_1=""
        genre_2=""
        genre_3=""

    try:                                                                                                    #Get_Genre
        temp = genre_all.find("|")
        genre_1 = genre_all[:temp].strip()
        genre_all = genre_all[temp+1:]
        print("%s" %genre_1)
    except:
        genre_1=""
        genre_2=""
        genre_3=""
        
    try:
        temp = genre_all.find("|")
        genre_2 = genre_all[:temp].strip()
        genre_all = genre_all[temp+1:]
        print("%s" %genre_2)
    except:
        genre_2=""
        genre_3=""
        
    try:
        temp = genre_all.find("|")
        genre_3 = genre_all[:temp].strip()
        genre_all = genre_all[temp+1:]
        print("%s" %genre_3)
    except:
        genre_3=""

    try:                                                                                                    #Get_GameRate
        point_all = bsObject.find('div',{'itemprop' : "aggregateRating"}).get_text()
        temp = point_all.find('%')
        point = point_all[temp-3:temp].strip()
        temp_start = point_all.find("사용자 평가")
        temp_end = point_all.find("개")
        user_num = int (point_all[temp_start+7 : temp_end].strip().replace(",",""))
    except:
        user_num = 0
        point = 0
    print("%s" %point)
    print("%d" %user_num)


    try:                                                                                                    #Get_Meta_Score
        meta_score = bsObject.find('div',{'class' : "score high"}).get_text().strip()
    except:
        meta_score = 0
    print(meta_score)
        
    try:                                                                                                    #Set_MySQL
        sql = "insert ignore into game_info values (NULL,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" 
        curs.execute(sql, (title, type, price, dev, pub, release, point, user_num, meta_score, desc, url))
        #conn.commit()
        sql = "insert ignore into game_genre values (NULL,%s, %s, %s, %s)"
        curs.execute(sql, (title, genre_1, genre_2, genre_3))
        conn.commit()
    except Exception as e:
        print(e)
        data = "Error %d line ...  Sql error : %s" %(i, e)
        f = open("ERROR.txt", 'a',-1,"utf-8")
        f.write(data)
        f.close()
        continue
    print("-----------------------------------------\n\n")

conn.close()
