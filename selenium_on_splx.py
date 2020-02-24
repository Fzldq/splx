from selenium import webdriver
import chromedriver_binary
import time
import datetime
import getpass
import winsound
from numpy.random import randint
import re


def main():
    count = 1

    def get_release_time():
        now = datetime.datetime.now(tz=datetime.timezone(
            datetime.timedelta(seconds=32400)))
        tomorrow = now + datetime.timedelta(days=1)
        if now.hour < 9:
            return datetime.datetime(*now.timetuple()[:3], 8, 58)
        else:
            return datetime.datetime(*tomorrow.timetuple[:3], 8, 58)

    def winalert():
        duration = 30000
        freq = 440
        winsound.Beep(freq, duration)
        winsound.PlaySound('Tik Tok.wav', winsound.SND_FILENAME)

    def boost():
        driver.get("https://mypage.1050.i-web.jpn.com/simplex2021/")
        name = input('Your ID:')
        pw = getpass.getpass('Password:')
        driver.find_element_by_name('gksid').send_keys(name)
        driver.find_element_by_name('gkspw').send_keys(pw)
        time.sleep(2)

        for i in driver.find_elements_by_tag_name("input"):
            if(i.get_attribute("onclick") == "javascript:loginSubmit();"):
                i.click()
                break
        time.sleep(2)

        for i in driver.find_elements_by_tag_name("input"):
            if (i.get_attribute('value') == "申込/確認"):
                i.click()
                break
        time.sleep(2)

        for i in driver.find_elements_by_tag_name("a"):
            if i.text == "予約開始":
                i.click()
                break
        time.sleep(2)

        for i in driver.find_elements_by_tag_name("a"):
            if i.text == "東京":
                i.click()
                break
        time.sleep(2)

    def check(count: int):
        time_start = datetime.datetime.now()
        last_day = driver.find_elements_by_tag_name(
            "tr")[-1].find_elements_by_tag_name('td')[1].text
        while datetime.datetime.now() - time_start < datetime.timedelta(seconds=3000):
            print("%d回目の試み" % (count))
            driver.refresh()
            count += 1
            for i in driver.find_elements_by_tag_name("tr")[-1:-10:-1]:
                if ((i.find_elements_by_tag_name('td')[2].text > '15:59' and
                     i.find_elements_by_tag_name('td')[0].text != "満席") or
                    (driver.find_elements_by_tag_name("tr")[-1].find_elements_by_tag_name('td')[1].text != last_day) or
                        (i.find_elements_by_tag_name('td')[0].text == "予約")):
                    print(i.text)
                    i.find_elements_by_tag_name('td')[0].click()
                    time.sleep(2)
                    for j in driver.find_elements_by_tag_name('a'):
                        if re.search("申し込み", j.text):
                            j.click()
                    for j in driver.find_elements_by_tag_name('input'):
                        if re.search("申し込み", i.get_attribute('value')):
                            j.click()
                    winalert()
                    return True, count
            last_day = driver.find_elements_by_tag_name(
                "tr")[-1].find_elements_by_tag_name('td')[1].text
            time.sleep(30 + randint(30))
        else:
            return False, count

    release_time = get_release_time()
    while datetime.datetime.now() < release_time:
        print(datetime.datetime.now())
        time.sleep(30)
    else:
        while True:
            driver = webdriver.Chrome()
            boost()
            for i in driver.find_elements_by_tag_name("tr")[-1:-10:-1]:
                if re.search("満席", i.text):
                    print(i.text)
            ms, count = check(count)
            if ms:
                break
            else:
                driver.close()
                driver.quit()


if __name__ == '__main__':
    main()
