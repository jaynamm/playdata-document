import requests
from bs4 import BeautifulSoup

header = {
    "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}

url = "https://finance.naver.com/item/sise_day.naver?code={}&page={}"

def get_stock(code=None, s_page=None, e_page=None):
    result = []

    for p in range(s_page, e_page+1):
        r = requests.get(url.format(code, p), headers=header)
        
        bs = BeautifulSoup(r.text, 'lxml').find("table", {'class': 'type2'}).find_all("span", "tah") 
	
        for i in range(0, 64, 7):
            result.append([d.text.strip() for d in bs[i:i+7]])

            
    return result

if __name__ == "__main__":
    print(get_stock('005930', 1, 1))
