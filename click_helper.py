import os

import keyboard as keyb
import time
import pyautogui


def main():
    # print(pyautogui.position())
    print('copyright 2021. KST & HeoSeokYong All Rights Reserved.\n')
    print('키를 입력할 때 CVAT 기존 단축키와 겹치지 않게 입력해 주세요.\n')
    custom_click = ''
    custom_all = ''
    custom_opencv = ''
    custom_grid = ''
    answer = ''
    while len(custom_click) != 1:
        custom_click = input('마우스 클릭을 대신할 키를 입력해 주세요. (추천: b)')
    while len(custom_all) != 1:
        custom_all = input('마우스 더블클릭을 대신할 키를 입력해 주세요. (추천: z)')
    sleep_time = float(input('마우스 클릭 사이 간격을 입력해 주세요. (추천: 0.05 ~ 0.1)'))
    use = input('grid를 자동으로 열고닫는 키를 쓰시려면 "o" 아니라면 아무 키를 입력해주세요.(초기 설정이 조금 번거로울 수 있음)')
    if use == 'o':
        # print('먼저 opencv를 load 해주세요.')
        # while len(custom_opencv) != 1:
        #     custom_opencv = input('opencv를 키고 끌 키를 입력해 주세요. (추천: a)')
        while len(custom_grid) != 1:
            custom_grid = input('grid를 키고 끌 키를 입력해 주세요. (추천: s)')
        # while answer != 'o':
        #     answer = input('CVAT의 opencv 부분에 마우스를 갖다 대고 "o"키를 입력해주세요.')
        # answer = ''
        # opencv_mx, opencv_my = pyautogui.position()
        # while answer != 'o':
        #     answer = input('opencv를 클릭하고 Image라고 써진 부분에 마우스를 갖다 대고 "o"키를 입력해주세요.')
        # answer = ''
        # o_image_mx, o_image_my = pyautogui.position()
        # while answer != 'o':
        #     answer = input('Image를 클릭하여 주시고 opencv를 키고 끄는 부분에 마우스를 갖다 대고 "o"키를 입력해주세요.')
        # answer = ''
        # o_i_mx, o_i_my = pyautogui.position()
        while answer != 'o':
            answer = input('CVAT의 아래에 있는 grid 설정창을 여는 ^모양 키에 마우스를 갖다 대고 "o"키를 입력해주세요.')
        answer = ''
        grid_mx, grid_my = pyautogui.position()
        while answer != 'o':
            answer = input('grid 설정창에서 grid를 키고 끄는 체크박스 부분에 마우스를 갖다 대고 "o"키를 입력해주세요.')
        answer = ''
        g_c_mx, g_c_my = pyautogui.position()

    os.system('cls')
    print('grid를 키고 끌때 전체화면이어야 하고, 마우스를 도중에 움직이면 안됩니다.\n프로그램을 일시정지/시작 하려면 F4키를 눌러주세요.')
    print('running...')
    while True:
        if keyb.is_pressed(custom_click):
            pyautogui.click()
            time.sleep(sleep_time)
        if keyb.is_pressed(custom_all):
            pyautogui.doubleClick()
            time.sleep(sleep_time)
        if keyb.is_pressed('f4'):
            print('pause!')
            time.sleep(1)
            while True:
                if keyb.is_pressed('f4'):
                    os.system('cls')
                    print('grid를 키고 끌때 전체화면이어야 하고, 마우스를 도중에 움직이면 안됩니다.\n프로그램을 일시정지/시작 하려면 F4키를 눌러주세요.')
                    print('running...')
                    time.sleep(1)
                    break

        if use == 'o':
            # if keyb.is_pressed(custom_opencv):
            #     pyautogui.moveTo(opencv_mx, opencv_my)
            #     pyautogui.click()
            #     time.sleep(0.2)
            #     pyautogui.moveTo(o_image_mx, o_image_my)
            #     pyautogui.click()
            #     pyautogui.moveTo(o_i_mx, o_i_my)
            #     pyautogui.click()
            #     pyautogui.moveTo(990, 540)
            #     pyautogui.click()
            if keyb.is_pressed(custom_grid):
                pyautogui.moveTo(grid_mx, grid_my)
                pyautogui.click()
                time.sleep(0.1)
                pyautogui.moveTo(g_c_mx, g_c_my)
                pyautogui.click()
                pyautogui.moveTo(990, 540)
                pyautogui.click()

    print('finish')


if __name__ == "__main__":
    main()
