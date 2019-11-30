import requests
import pandas as pd
from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)
from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.projectdb                      # 'dbsparta'라는 이름의 db를 만듭니다.


@app.route('/')
def home():
   return render_template('screener.html')

@app.route('/data', methods=['GET'])
def call():
    stock = list(db.screen.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'stock_list': stock})

if __name__ == '__main__':
   app.run('127.0.0.1',port=5000,debug=True)

'''

### dow jones stock download
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://money.cnn.com/data/dow30/',headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')
dow= soup.select('#wsod_indexConstituents > div > table > tr > td > a')

dowjones_list=[]
for d in dow:
    dowjones_list.append(d.text)

# url's
profile_url='https://financialmodelingprep.com/api/v3/company/profile/'
ratio_url='https://financialmodelingprep.com/api/v3/financial-ratios/'
ic_url='https://financialmodelingprep.com/api/v3/financials/income-statement/'
bs_url='https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/'

for d in dowjones_list:
    try:
        d_profile_url = profile_url+d
        d_ratio_url = ratio_url + d
        d_ic_url = ic_url + d
        d_bs_url = bs_url + d
        d_profile = requests.get(d_profile_url)
        d_ratio = requests.get(d_ratio_url)
        d_ic = requests.get(d_ic_url)
        d_bs = requests.get(d_bs_url)
        ticker_give = d_profile.json()['symbol']
        name_give = d_profile.json()['profile']['companyName']
        sector_give = d_profile.json()['profile']['sector']
        date_give = d_ic.json()['financials'][0]['date']
        mktcap_give = d_profile.json()['profile']['mktCap']
        price_give = d_profile.json()['profile']['price']
        rev_give = d_ic.json()['financials'][0]['Revenue']
        op_give = d_ic.json()['financials'][0]['Operating Income']
        np_give = d_ic.json()['financials'][0]['Net Income']
        asset_give = d_bs.json()['financials'][0]['Total assets']
        liab_give = d_bs.json()['financials'][0]['Total liabilities']
        equity_give = d_bs.json()['financials'][0]['Total shareholders equity']
        pe_give = d_ratio.json()['ratios'][0]['investmentValuationRatios']['priceEarningsRatio']
        pb_give = d_ratio.json()['ratios'][0]['investmentValuationRatios']['priceBookValueRatio']
        roe_give = d_ratio.json()['ratios'][0]['profitabilityIndicatorRatios']['returnOnEquity']
        divyield_give = d_ratio.json()['ratios'][0]['investmentValuationRatios']['dividendYield']
        db.screen.insert_one({'ticker': ticker_give,'name': name_give, 'sector': sector_give, 'date': date_give, 'mktcap': mktcap_give, 'price': price_give, 'rev': rev_give, 'op': op_give, 'np': np_give, 'asset': asset_give, 'liab': liab_give, 'equity': equity_give, 'p/e': pe_give, 'p/b': pb_give, 'roe': roe_give, 'divyield': divyield_give})
    except:
        pass



# profile info
profile_url='https://financialmodelingprep.com/api/v3/company/profile/'
aapl_profile_url = profile_url+"AAPL"
aapl_profile = requests.get(aapl_profile_url)
print(aapl_profile.json()['symbol'])


# ratio info
ratio_url='https://financialmodelingprep.com/api/v3/financial-ratios/'
aapl_ratio_url = ratio_url+"AAPL"
aapl_ratio = requests.get(aapl_ratio_url)
print(aapl_ratio.json()['ratios'][0])

ic_url='https://financialmodelingprep.com/api/v3/financials/income-statement/'
aapl_ic_url = ic_url+"AAPL"
aapl_ic = requests.get(aapl_ic_url)
print(aapl_ic.json()['financials'][0])


### stock list
stocklist= requests.get('https://financialmodelingprep.com/api/v3/company/stock/list').json()
a=[]

for s in stocklist['symbolsList']:
    a.append(s['symbol'])

print(len(a))


df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]
df.종목코드 = df.종목코드.map('{:06d}'.format)
#print(df.종목코드)


headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd=008490',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')
print(soup.select('#QmZIZ20rMn'))

# 매출액
#QmZIZ20rMn > table:nth-child(2) > tbody > tr:nth-child(1) > th

# 영업이익
#QmZIZ20rMn > table:nth-child(2) > tbody > tr:nth-child(2) > th


#QmZIZ20rMn > table:nth-child(2) > tbody > tr:nth-child(1) > th

## dart api
# http://dart.fss.or.kr/api/search.json?auth=36e851e3f5878ade843b95f9b23cacbbd230e709&crp_cd=005930&start_dt=19990101
# 인증키 : 36e851e3f5878ade843b95f9b23cacbbd230e709
# 발급일 : 2019-11-17

url = "http://dart.fss.or.kr/api/search.json?auth=36e851e3f5878ade843b95f9b23cacbbd230e709&crp_cd=005930&start_dt=19990101&dsp_tp=A"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

data = requests.get(url, headers=headers)
code = data.json()

# print(code["list"][0]["rcp_no"])

for i in code["list"]:
    print(i["rcp_no"])

# URL을 읽어서 HTML를 받아오고,

test = requests.get('http://dart.fss.or.kr/dsaf001/main.do?rcpNo=20191114001273',headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
soup = BeautifulSoup(test.text, 'html.parser')

patterns = re.findall(r"연결재무제표\".+?viewDoc\('(.+?)', '(.+?)', '(.+?)', '(.+?)', '(.+?)'.+?dart3.xsd", test.text, flags=re.DOTALL)
#print(patterns[0])
#print(patterns[0][0])


# /연결재무제표.+?viewDoc\('(.+?)', '(.+?)', '(.+?)', '(.+?)', '(.+?)'.+?dart3.xsd/

# select를 이용해서, tr들을 불러오기
#fin = soup.select('/html/head/script[9]/text()')
#print(fin)



# /html/head/script[9]/text()
# /html/head/script[9]/text()



df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]
df.종목코드 = df.종목코드.map('{:06d}'.format)
print(df.종목코드)

function viewDoc(rcpNo, dcmNo, eleId, offset, length, dtd) {
	currentDocValues.rcpNo = rcpNo;
	currentDocValues.dcmNo = dcmNo;
	currentDocValues.eleId = eleId;
	currentDocValues.offset = offset;
	currentDocValues.length = length;
	currentDocValues.dtd = dtd;
	var params = "";
	params += "?rcpNo=" + rcpNo;
	params += "&dcmNo=" + dcmNo;
	if (eleId != null)
		params += "&eleId=" + eleId;
	if (offset != null)
		params += "&offset=" + offset;
	if (length != null)
		params += "&length=" + length;
	params += "&dtd=" + dtd;
	document.getElementById("ifrm").src = "/report/viewer.do" + params;
}

		treeNode1.appendChild(treeNode2);
		
		treeNode2 = new Tree.TreeNode({
			text: "2. 연결재무제표",
			id: "13",
			cls: "text",
			listeners: {
				click: function() {viewDoc('20191114001273', '6958001', '13', '621477', '85372', 'dart3.xsd');}
			}
		});
		cnt++;

'''
