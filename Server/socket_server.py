import socket, threading
import base64
import os
import shutil
import food_database

from io import BytesIO
from PIL import Image

food_class_kor = ['가츠동', '갈비구이', '갈비찜', '갈비탕', '감자볶음', '고등어구이', '고르곤졸라피자', '곱창전골', '국수',
                  '김밥', '김치볶음밥', '김치찌개', '까르보나라', '나가사끼짬뽕', '낙지볶음', '냉면', '달걀말이', '달걀볶음밥',
                  '달걀찜', '닭갈비', '닭고기볶음', '돼지갈비찜', '돼지고기고추장불고기', '돼지고기볶음', '된장국', '된장찌개',
                  '떡갈비', '떡볶이', '마르게리따피자', '마르게리타피자', '만두', '미역국', '배추김치', '베이컨피자', '보쌈',
                  '비빔밥', '삶은', '삶은달걀', '삼겹살구이', '삼계탕', '생선회', '순대', '순대국밥', '순두부찌개', '순살찜닭',
                  '스크램블드에그', '스테이크', '쌀밥', '양념치킨', '오므라이스', '오믈렛', '장어덮밥', '짜장면', '짬뽕',
                  '쭈꾸미볶음', '초밥', '치즈피자', '카레라이스', '콤비네이션피자', '크림파스타', '토스트', '페퍼로니피자',
                  '펜네파스타', '하와이안피자', '함박스테이크', '해물찜', '해물탕', '화덕피자', '후라이드치킨']

# 일부 이미지 로딩 실패 무시
Image.LOAD_TRUNCATED_IMAGES = True
from matplotlib import pyplot as plt

# 소켓을 만든다.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 소켓 레벨과 데이터 형태를 설정한다.
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# 서버는 복수 ip를 사용하는 pc의 경우는 ip를 지정하고 그렇지 않으면 None이 아닌 ''로 설정한다.
# 포트는 pc내에서 비어있는 포트를 사용한다. cmd에서 netstat -an | find "LISTEN"으로 확인할 수 있다.
server_socket.bind(('', 9999))
# server 설정이 완료되면 listen를 시작한다.
server_socket.listen()

fooddb = food_database.foodDB()


def db_binder(client_socket, addr, length):
    # 커넥션이 되면 접속 주소가 나온다.
    print('(DB) Connected by', addr)
    try:
        # 만약 접속이 끊기게 된다면 except가 발생해서 접속이 끊기게 된다.
        # socket의 recv함수는 연결된 소켓으로부터 데이터를 받을 대기하는 함수입니다. 최초 5바이트를 대기합니다.
        # 이미지의 길이만큼 다시 데이터를 수신한다.
        data = client_socket.recv(1)  # db id 받기
        print(data)
        length -= len(data)
        db_id = int(data)  # id = 1:insert, 2:delete, 3:update, 4:select
        print('dbid', db_id)

        buf = b''
        while length:
            newbuf = client_socket.recv(1024)
            print(newbuf)
            if not newbuf:
                print(length)
                break
            buf += newbuf
            length -= len(newbuf)
            print(length)

        strb = buf.decode(encoding='utf8').split(',')

        # 위에서 얻은 newbuf를 알맞게 파싱
        food_name = strb[0]
        food_amount = ""
        if len(strb) > 1:
            food_amount = strb[1]

        if db_id == 1:
            fooddb.insert(food_name, food_amount)
        elif db_id == 2:
            fooddb.delete(food_name)
        elif db_id == 3:
            fooddb.update(food_name, food_amount)
        elif db_id == 4:
            client_socket.sendall(fooddb.select(food_name))
        elif db_id == 5:
            client_socket.sendall(fooddb.day_stat())
        elif db_id == 6:
            client_socket.sendall(fooddb.week_stat())
        else:
            print('invalid id!! ', id)
            exit(0)

    finally:
        # 접속이 끊기면 socket 리소스를 닫는다.
        client_socket.close()


def model_binder(client_socket, addr, length):
    # 커넥션이 되면 접속 주소가 나온다.
    print('(Model) Connected by', addr)
    try:
        # 만약 접속이 끊기게 된다면 except가 발생해서 접속이 끊기게 된다.

        # 이미지의 길이만큼 다시 데이터를 수신한다.
        buf = b''
        while length > 0:
            newbuf = client_socket.recv(1024)
            print(newbuf)
            if not newbuf:
                print(length)
                break
            buf += newbuf
            print(length)
            length -= len(newbuf)

        # 수신된 데이터를 bs4 형식으로 reform 시킨다.
        buf = buf.decode()
        # buf = buf[0:]
        buf = buf + '=' * (4 - len(buf) % 4)

        # bs4 형식 디코드
        img = Image.open(BytesIO(base64.b64decode(buf)))
        # 이미지 저장
        img.save("sample.jpg")

        # Yolo 처리
        if os.path.isdir('./yolov5/runs/detect/side_project'):
            shutil.rmtree('./yolov5/runs/detect/side_project')
        os.system("python ./yolov5/detect.py --source sample.jpg --weights ./yolov5/weights/best.pt --save-txt --name side_project")

        pred_cls = './yolov5/runs/detect/side_project/labels/sample.txt'

        while not os.path.isdir('./yolov5/runs/detect/side_project/labels/'):
            continue
        if os.path.isfile(pred_cls):
            with open(pred_cls, 'rt') as pc:
                list = pc.readlines()
                food_list = []
                for l in list:
                    cls = int(l.split(' ')[0])
                    food_list.append(food_class_kor[cls])
                result = fooddb.select(food_list).encode()

            os.remove(pred_cls)
            client_socket.sendall(result)
        else:
            print('Detecting 된 음식 객체가 없습니다.')

    except:
        # 접속이 끊기면 except가 발생한다.
        client_socket.sendall('')
        print("except : ", addr)
    finally:
        # 접속이 끊기면 socket 리소스를 닫는다.
        client_socket.close()


if __name__ == "__main__":
    try:
        # 서버는 여러 클라이언트를 상대하기 때문에 무한 루프를 사용한다.
        while True:
            # client로 접속이 발생하면 accept가 발생한다.
            # 그럼 client 소켓과 addr(주소)를 튜플로 받는다.
            client_socket, addr = server_socket.accept()
            print("server start!!")

            data = client_socket.recv(10)
            # 최초 5바이트는 전송할 데이터의 크기이다. 그 크기는 byte에서 int형식으로 변환한다.
            length = int(data)
            print('받은 length: ', length)
            data = client_socket.recv(1)
            id = int(data)
            length -= 1
            print('받은 id: ', id)
            # 쓰레드를 이용해서 client 접속 대기를 만들고 다시 accept로 넘어가서 다른 client를 대기한다.
            if id == 1:
                print('model thread...')
                th = threading.Thread(target=model_binder, args=(client_socket, addr, length))
                th.start()
            elif id == 2:
                print('db thread...')
                th = threading.Thread(target=db_binder, args=(client_socket, addr, length))
                th.start()
            else:
                print('invalid id', id)
                exit(0)
    # except:
    #     print("server error!")
    finally:
        # 에러가 발생하면 서버 소켓을 닫는다.
        print('server close!')
        server_socket.close()
