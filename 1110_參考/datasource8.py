import requests
import psycopg2
import password as pw
import key_api

__all__=['update_sqlite_data']

def __download_pm25_data()->list[dict]:
    '''
    下載細懸浮微粒資料（PM2.5）基本資料
    https://data.moenv.gov.tw/swagger/#/大氣/get_aqx_p_02
    '''
    pm25_url = f'https://data.moenv.gov.tw/api/v2/aqx_p_02?api_key={key_api.apikey}'
    response = requests.get(pm25_url)
    response.raise_for_status()
    print("下載成功")
    data= response.json()
    return data
    
def __create_table(conn)->None:    
    cursor = conn.cursor()
    cursor.execute(
         '''
        CREATE TABLE IF NOT EXISTS taiwan_pm25(
            "id"	SERIAL,
            "測站名稱"  TEXT NOT NULL,
            "縣市名稱"  TEXT NOT NULL,
            "PM25"      TEXT NOT NULL,
            "資料時間"  TEXT NOT NULL,
            PRIMARY KEY("id"),
            UNIQUE(測站名稱,資料時間)
            );
        '''
    )
    conn.commit()
    cursor.close()
    # print("create_table成功")

def __insert_data(conn,values:list[any])->None:
    cursor = conn.cursor()
    sql = '''
    INSERT INTO taiwan_pm25(測站名稱, 縣市名稱, PM25, 資料時間)
    VALUES (%s,%s,%s,%s)
    ON CONFLICT (測站名稱,資料時間) DO NOTHING
    '''
    cursor.execute(sql,values)    
    conn.commit()
    cursor.close()

def update_render_data()->None:
    '''
    下載,並更新資料庫
    '''
    data = __download_pm25_data()
    #---------------連線到postgresql----------------#
    conn = psycopg2.connect(database=pw.DATABASE,
                                user=pw.USER, 
                                password=pw.PASSWORD, host=pw.HOST, 
                                port="5432")
   
    __create_table(conn)
    for item in data['records']: 
        __insert_data(conn,values=[item['site'],item['county'],item['pm25'],item['datacreationdate']])
    conn.close()
    