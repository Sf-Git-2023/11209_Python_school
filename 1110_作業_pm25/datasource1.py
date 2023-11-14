import requests
import psycopg2
import password as pw
import key_api

#__all__ = ["update_sqlite_data"]

# -----------------download data-----------------#
def __download_pm25_data() -> list[dict]:
    pm25_url = f"https://data.moenv.gov.tw/api/v2/aqx_p_02?api_key={key_api.apikey}"
    response = requests.get(pm25_url)
    response.raise_for_status()
    print("下載成功")
    data = response.json()
    return data

# ---------------連線到postgresql----------------#
conn = psycopg2.connect(
    database=pw.DATABASE,
    user=pw.USER,
    password=pw.PASSWORD,
    host=pw.HOST,
    port="5432",
)

# ---------------create sql table----------------#
def __create_table(conn) -> None:
    cursor = conn.cursor()
    cursor.execute(
        """
		CREATE TABLE IF NOT EXISTS taiwan_pm25(
			"id"	SERIAL,
            "城市名稱"	TEXT NOT NULL,
            "縣市名稱"	TEXT NOT NULL,
            "pm25"	TEXT NOT NULL,
            "時間"	TEXT NOT NULL,
			PRIMARY KEY("id"),
            UNIQUE(城市名稱,時間)
		);
		"""
    )
    conn.commit()
    cursor.close()
    print("create_table成功")

# -----------------insert data-------------------#
def __insert_data(conn, values: list[any]) -> None:
    cursor = conn.cursor()
    sql = """
        INSERT INTO taiwan_pm25(id, 城市名稱, 縣市名稱, pm25, 時間) 
        VALUES(%s,%s,%s,%s,%s)
        ON CONFLICT (城市名稱,時間) DO NOTHING   
    """
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()

def update_render_data() -> None:
    #  下載,並更新資料庫  #
    data = __download_pm25_data()
    conn = psycopg2.connect(database=pw.DATABASE,
                            user=pw.USER, 
                            password=pw.PASSWORD,
                            host=pw.HOST, 
                            port="5432")
    
    __create_table(conn)
    for item in data["records"]:
        __insert_data(
            conn,
            values=[
                "id",
                item["site"],
                item["county"],
                item["pm25"],
                item["datacreationdate"]
            ]
        )
    conn.close()


def lastest_datetime_data() -> list[tuple]:
    conn = psycopg2.connect(database=pw.DATABASE,
                            user=pw.USER, 
                            password=pw.PASSWORD,
                            host=pw.HOST, 
                            port="5432")
    cursor = conn.cursor()
    sql = """
        select a.* 
        from taiwan_pm25 a join (select distinct 城市名稱, max(時間) 時間 from taiwan_pm25 group by 城市名稱) b
        on a.時間=b.時間 and a.城市名稱=b.城市名稱
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def search_sitename(word: str) -> list[tuple]:
    conn = psycopg2.connect(database=pw.DATABASE,
                            user=pw.USER, 
                            password=pw.PASSWORD,
                            host=pw.HOST, 
                            port="5432")
    cursor = conn.cursor()
    sql = """
        SELECT id, 城市名稱, MAX(時間) AS 時間,縣市名稱,pm25
        FROM taiwan_pm25
        GROUP BY 城市名稱,縣市名稱,pm25
        HAVING 城市名稱 like %s
        """
    cursor.execute(sql, [f"%{word}%"])
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows