import datasource
from threading import Timer
import time
import threading

def countdown(n:int)->None:
    while n > 0:
        print(f'倒數計時:{n}')
        n -= 1
        time.sleep(360)

def main():
    datasource.update_render_data()
    max_cnt = 24    # 下載10次
    count = 1
    while count != max_cnt:
        t = threading.Thread(target=countdown,args=(6,))
        t.start()

        while t.is_alive():
            print('小猴子還在做事')
            time.sleep(1)
        else:
            datasource.update_render_data()
            time.sleep(1) 
            count += 1
            print(f"第{count}次下載資料")

if __name__ == '__main__':
    main()