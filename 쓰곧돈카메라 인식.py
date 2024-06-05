import cv2
import os
import requests
from bs4 import BeautifulSoup

def search_similar_images(image_path):
    # Google 이미지 검색 URL
    url = 'https://www.google.com/searchbyimage/upload'

    # 이미지 파일 열기
    with open(image_path, 'rb') as f:
        # 파일을 multipart/form-data 형식으로 변환
        files = {'encoded_image': (image_path, f), 'image_content': ''}
        
        # 요청 보내기
        response = requests.post(url, files=files)

    # 응답 페이지 HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    # 유사 이미지 검색 결과 URL 가져오기
    similar_images_link = soup.find('a', class_='iu-card-header')
    if similar_images_link:
        return True
    else:
        return False

# 저장할 폴더 경로 (필요한 경로로 변경하세요)
save_folder = 'C:/Users/pc/Pictures/Saved Pictures'
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# 파일명을 위한 카운터 초기화
file_counter = 1

# 웹캠을 캡처 객체로 열기
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("웹캠을 열 수 없습니다.")
    exit()

while True:
    # 프레임 읽기
    ret, frame = cap.read()

    if not ret:
        print("프레임을 읽을 수 없습니다.")
        break

    # 프레임을 창에 표시
    cv2.imshow('Webcam', frame)

    # 키 입력 대기
    key = cv2.waitKey(1) & 0xFF

    # 'p' 키를 누르면 사진을 찍고 저장
    if key == ord('p'):
        # 파일명 생성 (숫자 증가)
        file_name = f'captured_image_{file_counter}.jpg'
        file_path = os.path.join(save_folder, file_name)
        
        # 사진 저장
        cv2.imwrite(file_path, frame)
        print(f'Saved: {file_path}')

        # Google 이미지 검색을 위해 저장한 이미지를 업로드하고 결과 확인
        search_result = search_similar_images(file_path)

        # 결과 확인 후 메시지 출력
        if search_result:
            print("유사한 이미지가 있습니다.")
        else:
            print("동일한 결과가 없습니다.")

        # 카운터 증가
        file_counter += 1

    # 'q' 키를 누르면 프로그램 종료
    elif key == ord('q'):
        break

# 캡처 객체와 창 닫기
cap.release()
cv2.destroyAllWindows()
