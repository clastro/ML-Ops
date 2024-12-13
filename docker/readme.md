# Docker
docker를 공부하고 정리하는 공간

## 접근 명령어

docker file을 사용해서 이미지 만들기

```
docker build -t dockerImage .
```

docker가 설치된 폴더 확인

```
docker info | grep "Docker Root Dir"
```

docker 패키지 설치

```
sudo wget -qO- https://get.docker.com/ | sh
```

docker 이미지 다운로드

```
docker pull ubuntu:20.04
```


docker 이미지 리스트 확인

```
docker images 
docker image ls
```
docker 이미지 실행 (컨테이너 띄우기)

```
docker run --gpus all -it -v /home/wellysis-tft/Desktop/code:/works -p 47203:47203 --name version1_shea tensorflow/tensorflow:latest-gpu /bin/bash

```

docker의 컨테이너 리스트 조회하기 : -a는 종료된 컨테이너를 포함

```
docker ps -a 
```

docker의 container를 그대로 복사해 image로 보관 (commit)

```
docker commit container1 image_name
```

정지된 Container 삭제하기

```
docker container prune
docker container prune --filter "until=12h" # 12시간 내 사용하지 않은 container 
```

docker 시작하기

```
docker start version1_shea
```

컨테이너에 접속하기

```
docker attach version1_shea
```

Shell로 접속

```
docker exec -it smc_shea /bin/bash
```

컨테이너 삭제하기

```
docker rm myName
```

Jupyter Notebook Docker 열기

```

      
docker run -d 
--gpus all 
-it 
-v /:/folder
--shm-size=10.24G
-p 주소창에 입력할 port :8888 
-p 주소창에 입력할 port:서버에 할당된 Port 
--name docker_name 
tensorflow/tensorflow:latest-gpu-jupyter jupyter notebook --allow-root --ip 0.0.0.0 --NotebookApp.token='' --no-browser /처음 접속할 때 보이는 폴더 

Ex]
docker run -d --gpus all -it -v /:/wellysis --shm-size=10.24G -p 36975:8888 -p 8400:6006 --name jupyter_shea tensorflow/tensorflow:latest-gpu-jupyter jupyter notebook --allow-root --ip 0.0.0.0 --NotebookApp.token='' --no-browser /
           
```
