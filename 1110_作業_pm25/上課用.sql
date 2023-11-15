''' 顯示Table 內容'''
select * from taiwan_pm25

''' 刪除Table 內容'''
delete from taiwan_pm25

''' 刪除Table 表頭欄位'''
drop table taiwan_pm25

''' 插入Table 內容'''
INSERT INTO taiwan_pm25 (城市名稱, 縣市名稱, pm25, 時間) 
VALUES ('大城','大彰化縣','6','2023-11-12 16:00')

''' 新建Table 表頭欄位'''
CREATE TABLE IF NOT EXISTS taiwan_pm25(
			"id"	SERIAL,
      "城市名稱"	TEXT NOT NULL,
      "縣市名稱"	TEXT NOT NULL,
      "pm25"	TEXT NOT NULL,
      "時間"	TEXT NOT NULL,
			PRIMARY KEY("id"),
      UNIQUE(城市名稱,時間)
);