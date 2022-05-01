from playwright.sync_api import sync_playwright
import requests


def get_cookie_playwright():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.forbes.com/billionaires")
        page.click("button.trustarc-agree-btn")
        # print(context.cookies())
        cookie_for_requests = context.cookies()[3]['value']
        browser.close()
    return cookie_for_requests


def req_with_cookie(cookie_for_requests):
    cookies = dict(
        Cookie=f'notice_preferences=2:; notice_gdpr_prefs=0,1,2::implied,eu; euconsent-v2={cookie_for_requests};')
    r = requests.get("https://www.forbes.com/billionaires/page-data/index/page-data.json", cookies=cookies)
    return r.json()


if __name__ == '__main__':
    data = req_with_cookie(get_cookie_playwright())
    print(data['result']['pageContext']['tableData'][0])
