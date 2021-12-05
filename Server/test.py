import os
import pymysql
import shutil
import food_database


food_class_kor = ['가츠동', '갈비구이', '갈비찜', '갈비탕', '감자볶음', '고등어구이', '고르곤졸라피자', '곱창전골', '국수',
                  '김밥', '김치볶음밥', '김치찌개', '까르보나라', '나가사끼짬뽕', '낙지볶음', '냉면', '달걀말이', '달걀볶음밥',
                  '달걀찜', '닭갈비', '닭고기볶음', '돼지갈비찜', '돼지고기고추장불고기', '돼지고기볶음', '된장국', '된장찌개',
                  '떡갈비', '떡볶이', '마르게리따피자', '마르게리타피자', '만두', '미역국', '배추김치', '베이컨피자', '보쌈',
                  '비빔밥', '삶은', '삶은달걀', '삼겹살구이', '삼계탕', '생선회', '순대', '순대국밥', '순두부찌개', '순살찜닭',
                  '스크램블드에그', '스테이크', '쌀밥', '양념치킨', '오므라이스', '오믈렛', '장어덮밥', '짜장면', '짬뽕',
                  '쭈꾸미볶음', '초밥', '치즈피자', '카레라이스', '콤비네이션피자', '크림파스타', '토스트', '페퍼로니피자',
                  '펜네파스타', '하와이안피자', '함박스테이크', '해물찜', '해물탕', '화덕피자', '후라이드치킨']


def main():
    # Yolo 처리
    a = food_database.foodDB()
    if os.path.isdir('./yolov5/runs/detect/side_project'):
        shutil.rmtree('./yolov5/runs/detect/side_project')
    os.system(
        "python ./yolov5/detect.py --source sample.jpg --weights ./yolov5/weights/best.pt --save-txt --name side_project")

    pred_cls = './yolov5/runs/detect/side_project/labels/sample.txt'
    food_db = pymysql.connect(
        host='127.0.0.1',
        user='root',
        passwd='2580',
        db='food',
        charset='utf8'
    )
    while not os.path.isfile(pred_cls):
        continue
    with open(pred_cls, 'rt') as pc:
        list = pc.readlines()
        food_list = []
        send = []
        for l in list:
            cls = int(l.split(' ')[0])
            food_list.append(food_class_kor[cls])
        myCursor = food_db.cursor(pymysql.cursors.DictCursor)
        for food_name in food_list:
            myCursor.execute('SELECT * FROM essential_food_data where 식품명 = %s', food_name)
            food = myCursor.fetchone()
            name = [food['식품명']]
            nutr = [str(n) for n in [food['에너지(㎉)'], food['탄수화물(g)'], food['단백질(g)'], food['지방(g)'], food['콜레스테롤(㎎)']]]
            tmp = ','.join(name + nutr)
            send.append(tmp)
            # print(food['식품명'], food['에너지(㎉)'], food['탄수화물(g)'], food['단백질(g)'], food['지방(g)'], food['콜레스테롤(㎎)'])
        print(send)
        result = '/'.join(send).encode()

    os.remove(pred_cls)
    print(len(result))
    print(result)


if __name__ == '__main__':
    main()