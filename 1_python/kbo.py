import requests 
import re 
import pickle
from multiprocessing import Pool
from bs4 import BeautifulSoup
import time


def crawling_kbo(player_id):
    url = "https://www.koreabaseball.com/Record/Player/PitcherDetail/Basic.aspx?playerId={}"
    r = requests.get(url.format(player_id))
    bs = BeautifulSoup(r.text, 'lxml')
    tmp_dict = dict()
    for x in bs.find("div", {'class' :'player_basic'}).findAll("li"):
        key, value = x.text.split(":")
        tmp_dict[key.strip()] = value.strip()
    tmp_dict['team'] = bs.find("h4", id="h4Team").text
    return tmp_dict



if __name__=="__main__":
    start = time.time()
    print(f"start -> {start}")
    
    with open("./kbo.pkl", "rb" ) as f:
        kbo= pickle.load(f)
        
    pool = Pool(processes=4)

    result = pool.map(crawling_kbo, kbo)
        
            
    with open("./kbo_result.pkl", "wb") as f:
        pickle.dump(result, f)
    print(f"time --> {time.time()-start}")
