select *
from 細懸浮微粒濃度

drop table 細懸浮微粒濃度

delete from 細懸浮微粒濃度

INSERT INTO 細懸浮微粒濃度 (測站名稱, 縣市名稱, PM25, 資料時間) 
VALUES ('大城','大彰化縣','6','2023-11-12 16:00')

ON CONFLICT (站點名稱,更新時間) DO UPDATE 
  SET 總車輛數 = 100, 
      可借 = 100,
	  可還 = 100;

select * 
from 台pm25
where 站點名稱='YouBike2.0_捷運科技大樓站'


INSERT INTO pm25 (站點名稱, 行政區, 更新時間, 地址, 總車輛數, 可借, 可還) 
VALUES ('YouBike2.0_一壽橋','文山區','2023-11-08 10:43:16','樟新街64號前方',0,0,0)
ON CONFLICT (站點名稱,更新時間) DO NOTHING