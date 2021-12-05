import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import base64

from io import BytesIO
from PIL import Image


food_db = pymysql.connect(
    host='127.0.0.1',
    user='root',
    passwd='2580',
    db='food',
    charset='utf8'
)

food_class_kor = ['가츠동', '갈비구이', '갈비찜', '갈비탕', '감자볶음', '고등어구이', '고르곤졸라피자', '곱창전골', '국수',
                  '김밥', '김치볶음밥', '김치찌개', '까르보나라', '나가사끼짬뽕', '낙지볶음', '냉면', '달걀말이', '달걀볶음밥',
                  '달걀찜', '닭갈비', '닭고기볶음', '돼지갈비찜', '돼지고기고추장불고기', '돼지고기볶음', '된장국', '된장찌개',
                  '떡갈비', '떡볶이', '마르게리따피자', '마르게리타피자', '만두', '미역국', '배추김치', '베이컨피자', '보쌈',
                  '비빔밥', '삶은 고구마', '삶은달걀', '삼겹살구이', '삼계탕', '생선회', '순대', '순대국밥', '순두부찌개', '순살찜닭',
                  '스크램블드에그', '스테이크', '쌀밥', '양념치킨', '오므라이스', '오믈렛', '장어덮밥', '짜장면', '짬뽕',
                  '쭈꾸미볶음', '초밥', '치즈피자', '카레라이스', '콤비네이션피자', '크림파스타', '토스트', '페퍼로니피자',
                  '펜네파스타', '하와이안피자', '함박스테이크', '해물찜', '해물탕', '화덕피자', '후라이드치킨']

myCursor = food_db.cursor(pymysql.cursors.DictCursor)


class foodDB:
    # food db class
    def __init__(self):
        print('create food db class!!')

    def insert(self, food_name, food_amount, diet_id):  # 음식, 양
        addition = "insert into addition(식단ID, 날짜, 식품명, 1회제공량, 에너지, 탄수화물, 단백질, 나트륨, 콜레스테롤, 지방, 양, 총당류) select %s, now(), 식품명, 1회제공량, 에너지, 탄수화물, 단백질, 나트륨, 콜레스테롤, 지방, %s, 총당류 from essential_food_data where 식품명 = %s"
        myCursor.execute(addition, (food_amount, food_name))
        addition2 = "update addition set 에너지 = 에너지 * 양, 탄수화물 = 탄수화물 * 양, 단백질 = 단백질 * 양, 지방=지방*양, 나트륨 = 나트륨*양, 콜레스테롤=콜레스테롤*양, 총당류 = 총당류 * 양 where 식품명 = %s and 식단ID = %s;"
        myCursor.execute(addition2, (food_name, diet_id))
        food_db.commit()
        print('insert success!')

    def delete(self, food_name, diet_id):  # 음식
        delete = "DELETE FROM addition where 식품명 = %s and DATE_FORMAT(날짜, '%%Y-%%m-%%d %%H') = DATE_FORMAT(now(), '%%Y-%%m-%%d %%H')"
        myCursor.execute(delete, food_name)
        food_db.commit()
        print('delete success!')

    def update(self, food_name, food_amount):  # 음식, 양
        self.delete(food_name)
        self.insert(food_name, food_amount)
        print('update success!')

    def select(self, food_list):  # 음식 리스트
        send = []
        if str(type(food_list)) == "<class 'str'>":
            food_list = [food_list]
        for food_name in food_list:
            myCursor.execute('SELECT * FROM essential_food_data where 식품명 = %s', food_name)
            food = myCursor.fetchone()
            name = [food['식품명']]
            nutr = [str(n) for n in [food['에너지'], food['탄수화물'], food['단백질'], food['지방'], food['나트륨'], food['당']]]
            tmp = ','.join(name + nutr)
            send.append(tmp)
            # print(food['식품명'], food['에너지(㎉)'], food['탄수화물(g)'], food['단백질(g)'], food['지방(g)'], food['콜레스테롤(㎎)'])
        result = '/'.join(send)
        print('select success!')
        return result

    # 일간 통계
    def day_stat(self):
        day_query = "select date_format(날짜, '%Y-%m-%d') as 기준일, sum(나트륨) from addition where date_format(날짜, '%Y-%m-%d') = date_format(now(), '%Y-%m-%d') or date_format(날짜, '%Y-%m-%d') = date_sub(date(now()), interval 1 day) group by date_format(날짜, '%Y-%m-%d') order by 날짜 desc"
        myCursor.execute(day_query)
        day_food = myCursor.fetchall()
        day_food = pd.DataFrame(day_food)
        day_food = day_food.set_index('기준일')
        plt.rc('font', family='Malgun Gothic')
        food_plot = day_food[['총탄수화물', '총단백질', '총지방']]
        food_plot.plot(figsize=(15, 5))
        plt.savefig('sample.png')
        with open('./sample.png', 'rb') as img:
            base64_string = base64.b64encode(img.read())

        return base64_string

    # 주간 통계
    def week_stat(self):
        week_query = "select date_format(날짜, '%Y/%U') as 기준일, sum(에너지) from addition where date_format(날짜, '%Y/%U') = date_format(now(), '%Y/%U') or date_format(날짜, '%Y/%U') = date_format(date_sub(date(now()), interval 1 week), '%Y/%U') group by 기준일 order by 날짜"
        myCursor.execute(week_query)
        week_food = myCursor.fetchall()
        week_food = pd.DataFrame(week_food)
        week_food = week_food.set_index('기준일')
        plt.rc('font', family='Malgun Gothic')
        food_plot = week_food[['총탄수화물', '총단백질', '총지방']]
        food_plot.plot(figsize=(15, 5))
        plt.savefig('sample.png')
        with open('./sample.png', 'rb') as img:
            base64_string = base64.b64encode(img.read())

        return base64_string
