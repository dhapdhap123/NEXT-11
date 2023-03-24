from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import csv
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import requests
import re

# 디버깅 모드
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# chrome_driver = '아무거나'
chrome_driver = 'C:/Users/dhapd/OneDrive/바탕 화면/NEXT/practice/실습5/chromedriver.exe'
driver = webdriver.Chrome(chrome_driver, options= chrome_options)

# 실행할 웹페이지 불러오기 (멜론 차트)
driver.get("https://movie.naver.com/movie/sdb/rank/rmovie.naver")
time.sleep(1)
# rankingbtn = driver.find_element(By.XPATH, '/html/body/div/div[3]/div/div[1]/div/div/ul/li[3]/a')
# rankingbtn.click()

file = open('movie.csv', mode='w', newline="")
writer = csv.writer(file)
writer.writerow(["rank", "movie"])

j = 1
for i in range(2, 23):
        if i == 12:
            continue
        movie_titles = driver.find_element(By.XPATH, f'/html/body/div/div[4]/div/div/div/div/div[1]/table/tbody/tr[{i}]/td[2]/div/a').text
        writer.writerow([j, movie_titles])
        j += 1
time.sleep(1)

writer.writerow(["index", 'date', "director", 'score'])
for i in range(2, 23):
    if i == 12:
        continue
    title_btn = driver.find_element(By.XPATH, f'/html/body/div/div[4]/div/div/div/div/div[1]/table/tbody/tr[{i}]/td[2]/div/a')      
    title_btn.click()
  
    time.sleep(1)
    url = driver.current_url
    res = requests.get(url)
    html = res.text
    soup = BeautifulSoup(html, "html.parser")
    movie_index = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(2) > p')
    index_list = movie_index.getText().split()
    for i in range(len(index_list)):
        index_list[i] = index_list[i].strip(',')
    release_day = ''
    release_day = index_list[-3] + index_list[-2] + index_list[-1]
    movie_director = soup.select_one("#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(4) > p > a").text
    titles = []
    scores = []
    if soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > div.main_score > div:nth-child(1) > div > span > em'):
        movie_star_title_1 = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > div.main_score > div:nth-child(1) > div > span > em').text
        movie_star_score_1 = soup.select('#actualPointPersentBasic > div > em')
        titles.append(movie_star_title_1)
        scores.append(movie_star_score_1)
    if soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > div.main_score > div:nth-child(2) > div > a > span > em'):
        movie_star_title_2 = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > div.main_score > div:nth-child(2) > div > a > span > em').text
        movie_star_score_2 = soup.select('#content > div.article > div.mv_info_area > div.mv_info > div.main_score > div:nth-child(2) > div > a > div > em')
        titles.append(movie_star_title_2)
        scores.append(movie_star_score_2)
    if soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > div.main_score > div.score.score_left > div.uio_ntz_btn > span > em'):
        movie_star_title_3 = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > div.main_score > div.score.score_left > div.uio_ntz_btn > span > em').text
        movie_star_score_3 = soup.select('#pointNetizenPersentBasic > em')
        titles.append(movie_star_title_3)
        scores.append(movie_star_score_3)
  
    movie_stars = {}
    score = ''
    for i in range(len(titles)):
        for j in scores[i]:
            score += j.text
            movie_stars[titles[i]] = score
        score = ''
    writer.writerow([', '.join(index_list[0:-3]), release_day, movie_director, movie_stars])
    driver.back()


time.sleep(1)
title_input = driver.find_element(By.XPATH, '/html/body/div/div[2]/div/div/fieldset/div/span/input')
title_input.click()
title_input.send_keys("인터스텔라(Interstellar)")
input_btn = driver.find_element(By.XPATH, '//*[@id="jSearchArea"]/div/button')
input_btn.click()
driver.find_element(By.XPATH, '/html/body/div/div[4]/div/div/div/div/div[1]/ul[2]/li[1]/dl/dt/a').click()

url = driver.current_url
res = requests.get(url)
html = res.text
soup = BeautifulSoup(html, "html.parser")


writer.writerow(["title", "director", "comments"])

movie_title = soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > h3 > a').text
movie_director = soup.select_one("#content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(4) > p > a").text
driver.execute_script("window.scrollTo(0, 1800)")
time.sleep(1)
movie_title_1 = soup.select_one('#content > div.article > div.section_group.section_group_frst > div:nth-child(5) > div:nth-child(2) > div.score_area > div.netizen_score > a > strong > em').text
movie_title_2 = soup.select_one('#content > div.article > div.section_group.section_group_frst > div:nth-child(5) > div:nth-child(2) > div.score_area > div.special_score > a > strong > em').text
movie_score_1 = soup.select_one("#content > div.article > div.section_group.section_group_frst > div:nth-child(5) > div:nth-child(2) > div.score_area > div.netizen_score > div > div > em").text
movie_score_2 = soup.select_one("#content > div.article > div.section_group.section_group_frst > div:nth-child(5) > div:nth-child(2) > div.score_area > div.special_score > div > div > em").text
movie_comments = soup.select_one("#content > div.article > div.section_group.section_group_frst > div:nth-child(5) > div:nth-child(2) > div.score_total > strong > em").text.strip()
writer.writerow([movie_title, movie_director, movie_comments])

# # 멜론 차트 버튼 클릭
# chartbtn = driver.find_element(By.XPATH, '//*[@id="gnb_menu"]/ul[1]/li[1]/a/span[2]')
# chartbtn.click()
# # 1위곡명 가져오기
# first = driver.find_element(By.XPATH, '//*[@id="lst50"]/td[6]/div/div/div[1]/span/a').text
# print(first)
# time.sleep(1)

# 1위부터 20위까지 가져오기
# for i in range(1,21):
#     titles = driver.find_element(By.XPATH,f"/html/body/div/div[3]/div/div/div[3]/form/div/table/tbody/tr[{i}]/td[6]/div/div/div[1]/span/a").text
#     print(titles)
# time.sleep(2)
# 스크롤 내리기

# 실시간 급상승 가수 가져오기
# charts = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[2]')
# time.sleep(2)
# ActionChains(driver).move_to_element(charts).perform()
# time.sleep(2)
# file = open('melon.csv', mode='w', newline="")
# writer = csv.writer(file)
# writer.writerow(["rank", "title", "singer"])
# for i in range(1, 11):
#     singers = driver.find_element(By.XPATH, f"/html/body/div[1]/div[2]/div/div[1]/div[2]/div/ol/li[{i}]/a").text
#     print(singers)
#     writer.writerow([singers])
# file.close()

# 곡의 장르 가져오기
# chartbtn = driver.find_element(By.XPATH, '//*[@id="lst50"]/td[4]/div/a/span')
# time.sleep(2)
# chartbtn.click()
# time.sleep(2)
# genre = driver.find_element(By.XPATH, '//*[@id="conts"]/div[2]/div/div[2]/div[2]/dl/dd[2]').text
# time.sleep(2)
# print(genre)
# time.sleep(2)
# 좋아하는 가수의 곡명 10개

# 순위, 곡명, 가수명 가져오기

# csv 파일로 변환