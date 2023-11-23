from IPython.display import display

from pandas.plotting import  table
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']#显示中文字体

import pandas as pd
import requests
import time
import json

# 用來計算漲跌百分比的函式
def count_per(x):
    if isinstance(x[0], int) == False:
        x[0] = 0.0
    
    result = (x[0] - float(x[1])) / float(x[1]) * 100

    return pd.Series(['-' if x[0] == 0.0 else x[0], x[1], '-' if result == -100 else result])

# 紀錄更新時間
def time2str(t):
    print(t)
    t = int(t) / 1000 + 8 * 60 * 60. # UTC時間加8小時為台灣時間
    
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))

def get_stock(stock_number,mode):
    # 打算要取得的股票代碼
    # stock_list_tse = ['0050', '0056', '2330', '2317', '1216']
    # stock_list_otc = ['6547', '6180']
    stock_list_tse=[]
    stock_list_otc=[]

    if mode=='上市':
        stock_list_tse = stock_number
        print(stock_list_tse)
        print("LENNNNNN",len(stock_list_tse))
        print("LENNNNNN",len(stock_list_otc))
    if mode=='上櫃':
         stock_list_otc = stock_number
         print(stock_list_otc)
         print("LENNNNNN",len(stock_list_otc))

    # 組合API需要的股票清單字串
    if len(stock_list_tse) != 0:
        stock_list1 = '|'.join('tse_{}.tw'.format(stock) for stock in stock_list_tse) 

    # 6字頭的股票參數不一樣
    if  len(stock_list_otc) != 0:
        stock_list2 = '|'.join('otc_{}.tw'.format(stock) for stock in stock_list_otc) 
    
    if len(stock_list_tse) != 0 and len(stock_list_otc) != 0:
        stock_list = stock_list1 + '|' + stock_list2
    elif len(stock_list_tse) != 0:
        stock_list = stock_list1
    elif len(stock_list_otc) != 0:
        stock_list = stock_list2

    print(stock_list)

    #　組合完整的URL
    query_url = f'http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch={stock_list}'

    # 呼叫股票資訊API
    response = requests.get(query_url)

    # 判斷該API呼叫是否成功
    if response.status_code != 200:
        raise Exception('取得股票資訊失敗.')
    else:
        print(response.text)

    # 將回傳的JSON格式資料轉成Python的dictionary
    data = json.loads(response.text)

    # 過濾出有用到的欄位
    columns = ['c','n','z','tv','v','o','h','l','y']
    df = pd.DataFrame(data['msgArray'], columns=columns)
    df.columns = ['股票代號','公司簡稱','成交價','成交量','累積成交量','開盤價','最高價','最低價','昨收價']

    # 自行新增漲跌百分比欄位
    df.insert(9, "漲跌百分比", 0.0) 


    # 填入每支股票的漲跌百分比
    df[['成交價', '昨收價', '漲跌百分比']] = df[['成交價', '昨收價', '漲跌百分比']].apply(count_per, axis=1)


    # 把API回傳的秒數時間轉成容易閱讀的格式
    # df['資料更新時間'] = df['資料更新時間'].apply(time2str)

    df = df.apply(lambda x: '        ' + x + '  ')


    # 顯示股票資訊

    # 修復terminating with uncaught exception of type NSException
    plt.switch_backend('Agg') 

    fig = plt.figure(figsize=(4, 3), dpi=1400)  # dpi表示清晰度
    ax = fig.add_subplot(111, frame_on=False)
    ax.xaxis.set_visible(False)  # hide the x axis
    ax.yaxis.set_visible(False)  # hide the y axis

    table(ax, df, loc='center')  # 将df换成需要保存的dataframe即可

    # 調整字體大小
    table_obj = table(ax, df, loc='center')
    table_obj.auto_set_font_size(False)
    table_obj.set_fontsize(3)

    # 調整表格間距
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=5)

    plt.savefig('stock.jpg')
