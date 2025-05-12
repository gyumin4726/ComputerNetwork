# GUI를 구현하기 위한 tkinter 모듈 불러오기
import tkinter as tk

# Socket 라이브러리 기능을 포함한, 보다 고수준 HTTP 프로토콜 모듈 불러오기
import http.client

#`GET` 메서드를 사용하여 요청을 보내는 함수
def send_get_request():
    send_request("GET") #`send_request` 함수를 `GET` 메서드로 호출

#`PUT` 메서드를 사용하여 요청을 보내는 함수
def send_put_request():
    send_request("PUT") #`send_request` 함수를 `PUT` 메서드로 호출

#`HEAD` 메서드를 사용하여 요청을 보내는 함수
def send_head_request():
    send_request("HEAD") #`send_request` 함수를 `HEAD` 메서드로 호출

#`POST` 메서드를 사용하여 요청을 보내는 함수
def send_post_request():
    send_request("POST") #`send_request` 함수를 `POST` 메서드로 호출

    

# 주어진 HTTP Method를 활용하여 요청을 보내는 함수
def send_request(method):
    conn = http.client.HTTPConnection("localhost", 8088) #로컬호스트(127.0.0.1)의 8088 포트에 연결 설정

    # 사용자로부터 입력 받은 경로와 본문 사용
    path = path_entry.get() # 경로를 가져옴
    body = body_entry.get() # 본문을 가져옴

    # 본문이 존재하면, 'Content-Length'라는 헤더에 본문의 길이를 설정
    # 본문이 없다면, 빈 딕셔너리로 초기화
    headers = {'Content-Length': len(body.encode())} if body else {}

    # 'computer-network'라는 사용자 지정 헤더를 추가하고, 그 값으로 'Essential'을 설정
    headers['computer-network'] = 'Essential'

    # 사용자로부터 입력 받은 토큰 사용
    token = token_entry.get() #토큰을 가져
    #'Authorization'(인증) 헤더에 토큰 값을 설정
    headers['Authorization'] = token

    # 요청 보내기
    conn.request(method, path, body=body, headers=headers)
    # 응답 받기
    response = conn.getresponse()
    
    # 리다이렉트 응답을 받았을 때의 처리 로직
    if response.status in [301, 303, 307]:
        # 'Location' 헤더에서 리다이렉트 대상 경로 불러오기
        new_path = response.getheader('Location')
        if new_path is not None:
            # 리다이렉트 대상 경로로 재요청 전송
            conn.request(method, new_path, body=body, headers=headers)
            # 재요청에 대한 응답 받기
            response = conn.getresponse()

    # 응답 정보를 출력
    response_label['text'] = f"{method} {path}: {response.status} {response.reason}"

    # 연결 종료
    conn.close()

# GUI 생성
root = tk.Tk()
# GUI 창의 제목 설정
root.title("Send Method Request")
#GUI 창의 크기 설정
root.geometry("500x700")

# 경로 입력 라벨 생성과 배치
path_label = tk.Label(root, text="경로를 입력하세요:") # 라벨 생성
path_label.pack() # 라벨 배치
# 경로 입력 필드 생성과 배치
path_entry = tk.Entry(root, width=50) # 필드 생성
path_entry.pack(pady=10) # 필드 배치

# 본문 입력 라벨 생성과 배치
body_label = tk.Label(root, text="본문을 입력하세요:") # 라벨 생성
body_label.pack() # 라벨 배치
# 본문 입력 필드 생성과 배치
body_entry = tk.Entry(root, width=50) # 필드 생성
body_entry.pack(pady=10) # 필드 배치

# 보안 토큰 입력 라벨 생성과 배치
token_label = tk.Label(root, text="토큰을 입력하세요:") # 라벨 생성
token_label.pack() # 라벨 배치
# 보안 토큰 입력 필드 생성과 배치
token_entry = tk.Entry(root, width=50) # 필드 생성
token_entry.pack(pady=10) # 필드 배치

# GET Method 전송 버튼 생성과 배치
get_button = tk.Button(root, text="Send GET Request", command=send_get_request, width=50, height=5) # GET 전송 버튼 생성
get_button.pack(pady=10) # GET 전송 버튼 배치

# PUT Method 전송 버튼 생성과 배치
put_button = tk.Button(root, text="Send PUT Request", command=send_put_request, width=50, height=5) # PUT 전송 버튼 생성
put_button.pack(pady=10) # PUT 전송 버튼 배치

# HEAD Method 전송 버튼 생성과 배치
head_button = tk.Button(root, text="Send HEAD Request", command=send_head_request, width=50, height=5) # HEAD 전송 버튼 생성
head_button.pack(pady=10) # HEAD 전송 버튼 배치

# POST Method 전송 버튼 생성과 배치
post_button = tk.Button(root, text="Send POST Request", command=send_post_request, width=50, height=5) # POST 전송 버튼 생성
post_button.pack(pady=10) # POST 전송 버튼 배치


# 응답 정보 출력 라벨 생성과 배치
response_label = tk.Label(root, text="") # 라벨 생성
response_label.pack() # 라벨 배치

# GUI 실행
root.mainloop()
