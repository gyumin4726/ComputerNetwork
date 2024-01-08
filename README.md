# 프로젝트 소개
컴퓨터 네트워크 소켓 통신 구현 과제

# 프로젝트 멤버
·20201914 박규민

# 개발 환경
·Windows 11

·Python 3.12 (64-bit) 

·IDLE (Python 3.12 64-bit) 

·PC 1대를 이용한 localhost(127.0.0.1) 루프백 

# 개발 목표
·Client에서 GET/HEAD/POST/PUT Request 구현

·Server에서 상황에 따른 2xx, 3xx, 4xx, 5xx 응답 메시지 Response 구현 

·와이어 샤크로 해당 메서드의 HTTP format 캡쳐

# 사용 방법
1. 우선 Server 코드를 먼저 실행시킵니다.
![스크린샷(113)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/1a46b5a8-a0b5-46eb-b149-9c11f073d322)
Server가 정상적으로 실행된 화면입니다.

2. 그 후 Client 코드를 실행시킵니다.
![스크린샷(114)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/aaa3ee11-9077-4511-b2c8-15141855903b)
Client가 정상적으로 실행된 화면입니다.

3. Send Method Request 인터페이스를 통해 간편하게 각 Method에 대한 요청을 서버로 전송할 수 있습니다.

4. 경로는 각 Method 별로 www.get.com / www.put.com / www.head.com / www.post.com 입니다.

5. 기본적인 필수 헤더인 computer-length는 이미 포함되어 있습니다. Put Method와 Post Method일 경우 본문에 right-body를 입력해야 오류 없이 정상적인 응답을 받을 수 있습니다.

6. 보안 토큰 Pass를 입력하지 않으면, 서버로부터 접근 권한을 부여받을 수 없어 오류 코드가 반환됩니다.

7. 정확한 경로와, 적절한 본문과 보안 토큰을 입력하면 정상적으로 송수신이 이루어집니다. 이때, 서버 오류 상황이 생길 경우 5xx 오류 코드가 반환됩니다. 정상적인 송수신이 이루어지면 2xx 코드가 반환됩니다.

# 소스 파일 설명 (Client)
```
# GUI를 구현하기 위한 tkinter 모듈 불러오기
import tkinter as tk

# Socket 라이브러리 기능을 포함한, 보다 고수준 HTTP 프로토콜 모듈 불러오기
import http.client
```
```
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
```
```
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
```
```
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
```

# 소스 파일 설명 (Server)
```
# 랜덤 상황을 위한 랜덤 모듈 불러오기
import random
# http.server 모듈로부터 BaseHTTPRequestHandler와 HTTPServer 불러오기
from http.server import BaseHTTPRequestHandler, HTTPServer

# BaseHTTPRequestHandler를 상속받아 SimpleHTTPRequestHandler 클래스 정의
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    # 보안 토큰을 통한 인증 로직
    def check_auth(self):
        # HTTP 헤더에서 'Authorization' 항목을 가져오기
        auth_header = self.headers.get('Authorization')
        # 'Authorization' 항목이 없거나 값이 'Pass'가 아니면 401 Unauthorized 전송
        if auth_header is None or auth_header != 'Pass':
            self.send_response(401)
            self.end_headers()
            return False # 인증 실패
        return True # 인증 성공
```
```
    # GET 요청에 대한 응답 메서드
    def do_GET(self):

        # 요청 경로가 올바른 경로인 "www.get.com"인 경우
        if self.path == "www.get.com":

            # 요청 헤더에서 'computer-network' 항목 확인
            special_header = self.headers.get('computer-network')

            # 'computer-network' 항목이 없으면 400 Bad Request 전송
            if special_header is None:
                self.send_response(400)

            else:
                # 보안 인증 체크
                if not self.check_auth():
                    return

                # 서버 상태 랜덤 결정
                server_state = random.randrange(0,9)

                # 서버 상태에 따라 다른 HTTP 상태 코드 전송
                if server_state == 0:
                    self.send_response(500) # 500 Internal Server Error 전송
                elif server_state == 1:
                    self.send_response(501) # 501 Not Implemented 전송
                elif server_state == 2:
                    self.send_response(502) # 502 Bad Gateway 전송

                else:
                    # 30% 확률로 리다이렉트 수행
                    if random.random()<0.3:

                        # 리다이렉트 코드 랜덤 결정
                        redirect_code = random.choice([301,303,307,404])

                        # 선택된 코드를 응답으로 전송
                        self.send_response(redirect_code)

                        # 상태 코드에 따라 다른 위치로 리다이렉트
                        if redirect_code == 301:
                            self.send_header('Location', 'www.new-get.com/')
                            self.end_headers()
                        elif redirect_code == 303:
                            self.send_header('Location', 'www.see-other-get.com/')
                            self.end_headers()
                        elif redirect_code == 307:
                            self.send_header('Location', 'www.temporary-get.com/')
                            self.end_headers()
                        else:
                            self.send_header('Location', 'Unkown')
                            self.end_headers()

                    else:
                        # 리다이렉트를 수행하지 않는 경우, 200 OK 응답 전송
                        self.send_response(200)

        # 'www.new-get.com/', 'www.see-other-get.com/', 'www.temporary-get.com/' 경로로 들어온 요청을 처리
        elif self.path == "www.new-get.com/" or self.path =='www.see-other-get.com/' or self.path =='www.temporary-get.com/':

            # 요청 헤더에서 'computer-network' 항목 확인
            special_header = self.headers.get('computer-network')

            # 'computer-network' 항목이 없으면 400 Bad Request 응답 전송
            if special_header is None:
                self.send_response(400)

            else:
                # 보안 인증 체크
                if not self.check_auth():
                    return

                # 인증이 성공할 경우, 200 OK 응답 전송
                self.send_response(200,self.path)
                self.end_headers()

        # 위의 모든 경우에 해당하지 않는 잘못된 경로에 대해서는 404 Not Found 응답 전송
        else:
            self.send_response(404) 
        self.end_headers()
```
```
    # PUT 요청에 대한 응답 메서드
    def do_PUT(self):

        # 요청 경로가 올바른 경로인 "www.put.com"인 경우
        if self.path == "www.put.com":

            # 요청 헤더에서 'computer-network' 항목 확인
            special_header = self.headers.get('computer-network')

            # 'computer-network' 항목이 없으면 400 Bad Request 전송
            if special_header is None:
                self.send_response(400)

            else:
                # 'content_length'를 HTTP 헤더에서 불러들이기
                content_length = self.headers.get('Content-Length')

                # 'content_length'를 정수로 변환
                length = int(content_length)

                # 'length'에 해당하는 길이만큼 요청 본문 읽어들이기
                body = self.rfile.read(length)

                # 읽은 본문을 디코딩하고, 그 내용이 'right-body'와 일치하는지 확인
                if body.decode() != 'right-body':

                    # 본문 내용이 'right-body'와 일치하지 않으면 400 Bad Request 응답
                    self.send_response(400)

                else:
                    # 보안 인증 체크
                    if not self.check_auth(): 
                        return

                    # 서버 상태 랜덤 결정
                    server_state = random.randrange(0,9)

                    # 서버 상태에 따라 다른 HTTP 상태 코드 전송
                    if server_state == 0:
                        self.send_response(500) # 500 Internal Server Error 전송
                    elif server_state == 1:
                        self.send_response(501) # 501 Not Implemented 전송
                    elif server_state == 2:
                        self.send_response(502) # 502 Bad Gateway 전송

                    else:
                        # 30% 확률로 리다이렉트 수행
                        if random.random()<0.3:

                            # 리다이렉트 코드 랜덤 결정
                            redirect_code = random.choice([301,303,307,404])

                            # 선택된 코드를 응답으로 전송
                            self.send_response(redirect_code)

                            # 상태 코드에 따라 다른 위치로 리다이렉트
                            if redirect_code == 301:
                                self.send_header('Location', 'www.new-put.com/')
                                self.end_headers()
                            elif redirect_code == 303:
                                self.send_header('Location', 'www.see-other-put.com/')
                                self.end_headers()
                            elif redirect_code == 307:
                                self.send_header('Location', 'www.temporary-put.com/')
                                self.end_headers()
                            else:
                                self.send_header('Location', 'Unkown')
                                self.end_headers()

                        else:
                            # 리다이렉트를 수행하지 않는 경우, 200 OK 응답 전송
                            self.send_response(200)

        # 'www.new-get.com/', 'www.see-other-get.com/', 'www.temporary-get.com/' 경로로 들어온 요청을 처리
        elif self.path == "www.new-put.com/" or self.path =='www.see-other-put.com/' or self.path =='www.temporary-put.com/':

            # 요청 헤더에서 'computer-network' 항목 확인
            special_header = self.headers.get('computer-network')

            # 'computer-network' 항목이 없으면 400 Bad Request 응답 전송
            if special_header is None:
                self.send_response(400)

            else:
                # 보안 인증 체크
                if not self.check_auth(): 
                    return

                # 인증이 성공할 경우, 200 OK 응답 전송
                self.send_response(200,self.path)
                self.end_headers()

        # 위의 모든 경우에 해당하지 않는 잘못된 경로에 대해서는 404 Not Found 응답 전송
        else:
            self.send_response(404)
        self.end_headers()
```
```
    # HEAD 요청에 대한 응답 메서드
    def do_HEAD(self):

        # 요청 경로가 올바른 경로인 "www.head.com"인 경우
        if self.path == "www.head.com":

            # 보안 인증 체크
            if not self.check_auth():
                return

            # 서버 상태 랜덤 결정
            server_state = random.randrange(0,9)

            # 서버 상태에 따라 다른 HTTP 상태 코드 전송
            if server_state == 0:
                self.send_response(500) # 500 Internal Server Error 전송
            elif server_state == 1:
                self.send_response(501) # 501 Not Implemented 전송
            elif server_state == 2:
                self.send_response(502) # 502 Bad Gateway 전송

            else:
                # 30% 확률로 리다이렉트 수행  
                if random.random()<0.3:

                    # 리다이렉트 코드 랜덤 결정
                    redirect_code = random.choice([301,303,307,404])

                    # 선택된 코드를 응답으로 전송
                    self.send_response(redirect_code)

                    # 상태 코드에 따라 다른 위치로 리다이렉트
                    if redirect_code == 301:
                        self.send_header('Location', 'www.new-head.com/')
                        self.end_headers()
                    elif redirect_code == 303:
                        self.send_header('Location', 'www.see-other-head.com/')
                        self.end_headers()
                    elif redirect_code == 307:
                        self.send_header('Location', 'www.temporary-head.com/')
                        self.end_headers()
                    else:
                        self.send_header('Location', 'Unkown')
                        self.end_headers()

                else:
                    # 리다이렉트를 수행하지 않는 경우, 200 OK 응답 전송
                    self.send_response(200)

        # 'www.new-get.com/', 'www.see-other-get.com/', 'www.temporary-get.com/' 경로로 들어온 요청을 처리
        elif self.path == "www.new-head.com/" or self.path =='www.see-other-head.com/' or self.path =='www.temporary-head.com/':

            # 요청 헤더에서 'computer-network' 항목 확인
            special_header = self.headers.get('computer-network')

            # 'computer-network' 항목이 없으면 400 Bad Request 응답 전송
            if special_header is None:
                self.send_response(400)

            else:
                # 보안 인증 체크
                if not self.check_auth():  # 인증 체크
                    return
              
                # 인증이 성공할 경우, 200 OK 응답 전송
                self.send_response(200,self.path)
                self.end_headers()

        # 위의 모든 경우에 해당하지 않는 잘못된 경로에 대해서는 404 Not Found 응답 전송
        else:
            self.send_response(404)     
        self.end_headers()
```
```     
    # POST 요청에 대한 응답 메서드
    def do_POST(self):

        # 요청 경로가 올바른 경로인 "www.post.com"인 경우
        if self.path == "www.post.com":

            # 요청 헤더에서 'computer-network' 항목 확인
            special_header = self.headers.get('computer-network')

            # 'computer-network' 항목이 없으면 400 Bad Request 전송
            if special_header is None:
                self.send_response(400)

            else:
                # 'content_length'를 HTTP 헤더에서 불러들이기
                content_length = self.headers.get('Content-Length')

                # 'content_length'를 정수로 변환
                length = int(content_length)

                # 'length'에 해당하는 길이만큼 요청 본문 읽어들이
                body = self.rfile.read(length)

                # 읽은 본문을 디코딩하고, 그 내용이 'right-body'와 일치하는지 확인
                if body.decode() != 'right-body':

                    # 본문 내용이 'right-body'와 일치하지 않으면 400 Bad Request 응답 전
                    self.send_response(400)

                else:
                    # 보안 인증 체크
                    if not self.check_auth():
                        return

                    # 서버 상태 랜덤 결정
                    server_state = random.randrange(0,9)

                    # 서버 상태에 따라 다른 HTTP 상태 코드 전송
                    if server_state == 0:
                        self.send_response(500) # 500 Internal Server Error 전송
                    elif server_state == 1:
                        self.send_response(501) # 501 Not Implemented 전송
                    elif server_state == 2: 
                        self.send_response(502) # 502 Bad Gateway 전송

                    else:
                        # 30% 확률로 리다이렉트 수행  
                        if random.random()<0.3:

                            # 리다이렉트 코드 랜덤 결정
                            redirect_code = random.choice([301,303,307,404])

                            # 선택된 코드를 응답으로 전송
                            self.send_response(redirect_code)

                            # 상태 코드에 따라 다른 위치로 리다이렉트
                            if redirect_code == 301:
                                self.send_header('Location', 'www.new-post.com/')
                                self.end_headers()
                            elif redirect_code == 303:
                                self.send_header('Location', 'www.see-other-post.com/')
                                self.end_headers()
                            elif redirect_code == 307:
                                self.send_header('Location', 'www.temporary-post.com/')
                                self.end_headers()
                            else:
                                self.send_header('Location', 'Unkown')
                                self.end_headers()
                        
                        else:
                            # 리다이렉트를 수행하지 않는 경우, 201 Created 응답 전송
                            self.send_response(201)

        # 'www.new-get.com/', 'www.see-other-get.com/', 'www.temporary-get.com/' 경로로 들어온 요청을 처리
        elif self.path == "www.new-post.com/" or self.path =='www.see-other-post.com/' or self.path =='www.temporary-post.com/':

            # 요청 헤더에서 'computer-network' 항목 확인
            special_header = self.headers.get('computer-network')

            # 'computer-network' 항목이 없으면 400 Bad Request 응답 전송
            if special_header is None:
                self.send_response(400)

            else:
                # 보안 인증 체크
                if not self.check_auth():
                    return

                # 인증이 성공할 경우, 201 Created 응답 전송
                self.send_response(201,self.path)
                self.end_headers()
        # 위의 모든 경우에 해당하지 않는 잘못된 경로에 대해서는 404 Not Found 응답 전송
        else:
            self.send_response(404) 
        self.end_headers()
```
```
# 서버를 실행는 메서드
def start_server():

    # 서버가 동작할 주소와 포트를 'localhost' 주소의 8088 포트로 설정
    server_address = ('localhost', 8088)

    # HTTPServer 객체를 생성, 요청을 처리할 핸들러로 'SimpleHTTPRequestHandler'를 사용
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)

    # 서버가 실행됨을 알리는 메시지를 출력
    print(f"Starting server on {server_address[0]}:{server_address[1]}")

    # 서버를 실행하고, 클라이언트로부터의 요청을 무한히 대기하며, 요청이 들어오면 처리
    httpd.serve_forever()

#'start_server' 함수를 호출하여 서버를 시작
if __name__ == "__main__":
    start_server()
```

# 실행 (Get Method)

![스크린샷(55)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/8299a9ed-486c-45db-bb85-a80715423a65)

잘못된 경로를 입력할 경우, 404 Not Found 응답 코드가 수신됩니다.

<br />

![스크린샷(57)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/34c9d7bf-0718-4975-9e5e-a59cb416e061)

제대로 된 경로를 입력했지만, 보안 토큰을 입력하지 않은 경우 401 Unauthorized 응답 코드가 수신됩니다.

<br />

![스크린샷(63)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/05f70b90-832a-45c4-92a0-50a4c7b6fc76)

제대로 된 경로와, 정확한 보안 토큰 값을 입력하면 성공적으로 200 OK 응답 코드가 수신됩니다.

<br />

![스크린샷(62)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/b6356fd4-18fa-4ca4-ac53-1832abefeea2)
![스크린샷(61)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/73d1cd32-4e1f-42e3-82c4-43c32ee71ecb)


제대로 된 경로와, 정확한 보안 토큰 값을 입력하여도 서버에 오류가 생기면 5xx 응답 코드들이 수신됩니다.

<br />

![스크린샷(60)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/46d9ee4d-b6e1-4147-bc27-157060325d0b)
![스크린샷(59)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/9a50cc67-20b7-4497-82ab-14655617f0dc)

경우에 따라 새로운 경로로 응답을 Redirect합니다. 이 경우, 새로운 경로를 통해 성공적으로 200 OK 응답 코드가 수신됩니다.

<br />

![스크린샷(58)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/f3ec007d-ac6d-4f9c-966f-cfa82eeb5fc8)

Redirect 되더라도, 경로가 잘못 지정되면 404 Not Found 응답 코드가 수신됩니다.

<br />

# 실행 (Put Method)

![스크린샷(64)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/acff50b2-ddcc-4d8c-8a0a-2ee9edf5c685)

잘못된 경로를 입력할 경우, 404 Not Found 응답 코드가 수신됩니다.

<br />

![스크린샷(66)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/be8387c8-65c1-46be-9c1f-262db06d4cc7)

제대로 된 경로를 입력했지만, 적절한 본문을 입력하지 않은 경우 400 Bad Request 응답 코드가 수신됩니다.

<br />

![스크린샷(67)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/04c8f2e1-b3c9-4b4d-a8d0-00d7cf13f2ca)

제대로 된 경로와 적절한 본문을 입력했지만, 보안 토큰을 입력하지 않은 경우 401 Unauthorized 응답 코드가 수신됩니다.

<br />

![스크린샷(68)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/5c7f96da-5bc3-486a-bd9d-02fd95d2d331)

제대로 된 경로와 적절한 본문, 정확한 보안 토큰 값을 입력하면 성공적으로 200 OK 응답 코드가 수신됩니다.

<br />

![스크린샷(73)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/9ec30607-355b-41f0-9bf0-fb562d4dd9ec)
![스크린샷(69)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/a0b8f106-74c7-4792-a6d8-3fb72aac1e6d)
![스크린샷(72)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/44e5b854-fbfb-4faa-a32a-196011579275)

제대로 된 경로와 적절한 본문, 정확한 보안 토큰 값을 입력하여도 서버에 오류가 생기면 5xx 응답 코드들이 수신됩니다.

<br />

![스크린샷(71)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/7c9f5606-41e2-4df8-8687-54b3cb3e18e3)
![스크린샷(70)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/474a8918-77ae-4be9-a2bc-60729389f071)

경우에 따라 새로운 경로로 응답을 Redirect합니다. 이 경우, 새로운 경로를 통해 성공적으로 200 OK 응답 코드가 수신됩니다.

<br />

![스크린샷(74)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/bd14d1c1-7d10-4644-9352-7fe30deb234b)

Redirect 되더라도, 경로가 잘못 지정되면 404 Not Found 응답 코드가 수신됩니다.

<br />

# 실행 (Head Method)

![스크린샷(75)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/8e3c3175-00cb-4461-a202-05b06ed8e19b)

잘못된 경로를 입력할 경우, 404 Not Found 응답 코드가 수신됩니다.

<br />

![스크린샷(76)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/8c5bd0e1-377b-4ee1-9d4f-57fbc864378b)

제대로 된 경로를 입력했지만, 보안 토큰을 입력하지 않은 경우 401 Unauthorized 응답 코드가 수신됩니다.

<br />

![스크린샷(79)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/20d7dcae-4f05-4444-93a1-7eaf3bbbeddf)

제대로 된 경로와, 정확한 보안 토큰 값을 입력하면 성공적으로 200 OK 응답 코드가 수신됩니다.

<br />

![스크린샷(80)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/2d5bfeaa-be93-495e-adf2-fcd400b65231)
![스크린샷(77)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/3c976a7a-9fdc-4c63-8376-53bf7f3d56a5)


제대로 된 경로와, 정확한 보안 토큰 값을 입력하여도 서버에 오류가 생기면 5xx 응답 코드들이 수신됩니다.

<br />

![스크린샷(78)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/3edb3e71-69ee-4774-b9e0-93833cced3d6)
![스크린샷(81)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/e2b11ce1-d426-4338-910d-a1c18889d87b)

경우에 따라 새로운 경로로 응답을 Redirect합니다. 이 경우, 새로운 경로를 통해 성공적으로 200 OK 응답 코드가 수신됩니다.

<br />

![스크린샷(82)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/1777daef-2052-4e6d-95ad-f158cd7a2a1e)

Redirect 되더라도, 경로가 잘못 지정되면 404 Not Found 응답 코드가 수신됩니다.

<br />

# 실행 (Post Method)

![스크린샷(83)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/49bcb234-7af1-462d-b5e3-b142ed3030b2)

잘못된 경로를 입력할 경우, 404 Not Found 응답 코드가 수신됩니다.

<br />

![스크린샷(84)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/22baeaab-68d9-4087-b085-412a1d9100f9)
제대로 된 경로를 입력했지만, 적절한 본문을 입력하지 않은 경우 400 Bad Request 응답 코드가 수신됩니다.

<br />

![스크린샷(85)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/ef8902ad-1bbd-48ff-a917-ee4224ab50ad)

제대로 된 경로와 적절한 본문을 입력했지만, 보안 토큰을 입력하지 않은 경우 401 Unauthorized 응답 코드가 수신됩니다.

<br />

![스크린샷(86)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/79877080-7082-4826-b5a5-062af728b4d1)

제대로 된 경로와 적절한 본문, 정확한 보안 토큰 값을 입력하면 성공적으로 201 Created 응답 코드가 수신됩니다.

<br />

![스크린샷(89)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/bc4b9428-809c-442a-a5b5-2d90b95381a8)
![스크린샷(87)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/1f23d7a7-80e9-4116-aff0-98c615e3cd80)

제대로 된 경로와 적절한 본문, 정확한 보안 토큰 값을 입력하여도 서버에 오류가 생기면 5xx 응답 코드들이 수신됩니다.

<br />

![스크린샷(88)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/4d5524cb-cff8-4740-ba35-2afcde7dd0c5)
![스크린샷(90)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/aa52fcbc-94d8-4d7d-8ceb-c47ab3887cbd)
경우에 따라 새로운 경로로 응답을 Redirect합니다. 이 경우, 새로운 경로를 통해 성공적으로 201 Created 응답 코드가 수신됩니다.
<br />

![스크린샷(91)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/88e22a7a-6ec6-4da9-8589-7147a49b5660)

Redirect 되더라도, 경로가 잘못 지정되면 404 Not Found 응답 코드가 수신됩니다.

<br />

# WireShark를 이용한 HTTP Format 캡쳐 및 분석
길이가 너무 길어지는 관계로, 4개의 Method들 중에 대표로 가장 복합적인 기능을 지닌 Post Method를 이용하여 HTTP Format을 캡쳐 및 분석해보겠습니다.

### CASE.1 (잘못된 경로 입력)

![스크린샷(95)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/6d7f3532-0d57-4446-8290-36bb22f42c86)
우선, 잘못된 경로가 입력되었을 경우입니다.
위 사진은, Client가 Server에게 전송한 HTTP Format입니다.

가장 첫 줄에는 Request MEthod, Request URI, Request Version의 내용이 담겨 있는 Request Line이 나타납니다.

그 다음에는 HOST 헤더가 위치합니다. 이 헤더에는 요청을 보내는 서버의 주소와 포트 넘버가 담겨져 있습니다. 이 경우에는, 루프백을 이용하고 있으므로 자기자신을 가리키는 localhost, 그리고 코드에서 임의로 설정한 포트 넘버인 8088이 나타납니다.

Accept-Encoding 헤더는 클라이언트가 서버에게 어떤 형식으로 데이터를 받고 싶은지 요청하는 헤더입니다. 이 경우에는 identity라는 헤더 값이 포함되어 있으므로, 클라이언트가 서버로부터 압축되지 않은 원본 데이터를 받기를 원한다고 요청하고 있습니다.

Content-Length 헤더는 입력받은 HTTP 본문의 길이를 바이트 단위로 나타내는 헤더입니다. 실제로 전송하려는 데이터를 담은 본문의 크기를 알려주는 헤더로, 수신자는 이 정보를 이용해 메시지를 올바르게 해석하고 처리할 수 있게 도와줍니다.

computer-network 헤더는 제가 코드를 통해 임의로 포함시킨 커스텀 헤더입니다. 이 헤더가 포함되야 정상적인 응답을 받을 수 있도록 설정했으며, 헤더 값으로는 필수를 의미하는 Essential을 임의로 설정했습니다.

Authorization 헤더는 클라이언트가 서버에게 자신의 인증 정보를 전달하는 데 사용되는 헤더입니다. 올바른 토큰 값을 입력 받았을 때, 서버가 클라이언트에게 특정 자원에 대한 접근 권한을 부여할 수 있도록 하였습니다.

<br />

![스크린샷(96)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/40d93951-1f64-4914-9216-409395537ced)

이 사진은 이에 대해 Server가 Client에게 응한 HTTP Format입니다.

가장 첫 줄에는 Status Line이 나타납니다. 이 부분은 Response Version과 Status Code, 그리고 각 상태 코드에 따른 Response Phrase로 구성되어 있습니다. 이 경우엔 잘못된 경루과 입력되어 404 Not Found가 나타납니다.

Server" 헤더는 웹 서버의 소프트웨어 및 버전 정보를 담고 있습니다. BaseHTTP/0.6은 파이썬의 내장 HTTP 서버인 BaseHTTP의 0.6 버전을 사용하고 있음을 의미하며, Python/3.12.1은 파이썬 언어의 3.12.1 버전을 사용하고 있음을 의미합니다.

Date 헤더에는 응답을 전송한 날짜와 시간이 나타납니다. 기본적으로 GMT를 기준으로 나타납니다.

<br />

### CASE.2 (올바른 경로 입력)

![스크린샷(97)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/4ea7d2a1-5371-49ec-9fe2-5b6d1e1734c0)

이번엔, 올바른 경로를 입력했을 경우입니다.
첫 번째 케이스와 마찬가지로 Format의 대부분이 동일하지만, 경로만 www.wrong.com에서 www.post.com으로 변한 것을 확인할 수 있습니다.

<br />

![스크린샷(98)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/ee94797b-26e6-4442-9d65-cb888354e574)

응답도 마찬가지로, 대부분 동일하지만 시간과 Status Code 그리고 이에 따른 Response Phrase만 변한 것을 확인할 수 있습니다.

<br />

### CASE.3 (올바른 경로 입력, 필수 본문 입력)

![스크린샷(99)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/50d58579-557e-4618-8565-1720cb833588)

이번엔 필수 본문까지 입력하여 올바른 경로로 전송했을 경우입니다.
이 경우에는 앞선 2번의 케이스에서는 확인하지 못한, HTTP의 본문을 확인할 수 있습니다.
가장 아래 DATA 부분에, right-body가 인코딩되어 숫자 형태로 나타나 있는 것을 확인할 수 있습니다.
또한, Content-Length 헤더에도, 본문의 length인 10이라는 값이 할당된 것을 확인할 수 있습니다.

<br />

![스크린샷(100)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/df23036e-f69c-4be9-b783-54a316d33fc1)

이번 응답도, 상황에 맞는 401 Status Code와 Unquthorized Response Phrase가 나타나는 것을 확인할 수 있습니다.

<br />

### CASE.4 (올바른 경로, 필수 본문, 보안 토큰 입력)

![스크린샷(105)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/063722dd-37ac-4579-a225-cab7d2855ebf)

이번엔 알맞은 보안 토큰까지 입력한 경우입니다.
앞선 케이스들과의 차이점은, Authorization 헤더에 Pass라는 값이 할당되었다는 것입니다.
이때, 알맞은 값이 할당되면 서버는 클라이언트에게 접근 권한을 부여합니다.

<br />

![스크린샷(106)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/71cdb655-cfb9-44d4-8b91-69cb1410f98a)

접근 권한을 부여 받은 클라이언트는, 서버에게서 201 Created 응답을 받게 됩니다.

<br />

### CASE.5 (올바른 경로, 필수 본문, 보안 토큰 입력, Redirect되는 경우)

![스크린샷(104)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/b12d3f86-1e62-45fa-8bf1-bc097578466e)

위와 같이 올바른 경로와 필수 본문, 보안 토큰을 입력하여 요청을 보냈을 때 경로가 바뀌었다면 서버에서 자동적으로 바뀐 경로로 클라이언트를 Redirect 해주게 됩니다.

<br />

![스크린샷(107)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/c344a696-dacf-43a2-9dba-b97beeefc099)

Redirect를 위해서, 서버는 우선 새로운 위치의 정보를 Location 헤더에 담아 클라이언트에게 전송해줍니다.
위 사진을 보면, 여태까지의 응답들과는 다르게 Location 헤더가 추가 되고 새로운 URI인 www.temporary-post.com가 해당 헤더에 값으로 할당되어 있다는 것을 확인할 수 있습니다.

<br />

![스크린샷(101)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/76b0a65a-86a1-43dd-81f7-98b32a9a5d84)

이후에 클라이언트는 서버에게서 받은 새로운 URI 정보를 토대로, 해당 URI로 또 다시 같은 내용의 요청을 전송합니다.

<br />

![스크린샷(102)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/87e508c9-c823-437d-80a6-1b7ffd8e4f92)

새로운 URI에 대한 Redirect가 성공하면, 서버는 201 상태 코드를 Response합니다. Response Phrase에는 제가 임의로 Redirect를 확인할 수 있도록 Created 대신 새로운 URI를 설정해 놓았습니다.

<br />

![스크린샷(112)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/3407e837-d687-43d1-a142-d0589b11c1bd)

만약 위와 같이 새로운 경로를 찾을 수 없거나, 새로운 경로가 잘못 되었을 때 (Unknown) 404 Not Found 상태 코드를 응답으로 전송합니다.

<br />

### CASE.6 (올바른 경로, 필수 본문, 보안 토큰 입력, 서버 오류가 생겼을 때의 응답)

![스크린샷(109)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/f24c3e1f-4e5b-43ed-92a5-d7edc0e12910)

<br />

![스크린샷(110)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/d426977c-6565-4910-8e06-3dac622d3415)

<br />

![스크린샷(111)](https://github.com/RYUCHOHEE/ComputerNetwork/assets/155864402/ddead576-41b6-46e0-8979-61f49a8fff91)

위 케이스는, 서버에 오류가 생겼을 때 전송되는 서버의 응답들입니다.

Status Code와 Response Phrase를 제외하고는 다른 응답들과 동일합니다.

클라이언트의 요청은 동일하기 때문에 생략하겠습니다.
