# Docker
docker를 공부하고 정리하는 공간

## 접근 명령어

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
docker run -d --gpus all # gpu 사용 
      -p 8889:8888  # host port : jupyter의 default port 
      -p 6006:6006  # tensorboard의 default port 
      --name tensorflow_gpu_shea  # 컨테이너 이름을 tensorflow_gpu_shea 로 설정
      tensorflow/tensorflow:latest-gpu-jupyter # 이미지의 이름과 
      jupyter notebook  # 주피터 노트북을 열라는 명령어 
      --allow-root  # 루트계정에서 서버를 여는 것을 허용 
      --ip 0.0.0.0  # default 값으로 ip설정 
      --NotebookApp.token=''  # 서버에 등록하는 인증절차를 생략 
      --no-browser # 주피터 접속 기억 실행하지 않도록
      
docker run -d --gpus all #GPU 사용
           -it -v /home/weladmin/Desktop/data:/smc_work # : /home/weladmin/Desktop/data 경로를 /smc_work 경로로
           -p 48001:8889 -p 6006:6006 #jupyter notebook 포트와 tensorboard 포트 설정
           --name smc_shea #docker 이름
           tensorflow/tensorflow:latest-gpu-jupyter 
           jupyter notebook --allow-root #루트 권한으로 jupyter notebook 실행 
           --ip 0.0.0.0 #모든 ip 허용
           --NotebookApp.token='' #서버에 등록하는 인증절차 생략 
           --no-browser /bin/bash 
docker run -d --gpus all # gpu 사용 
      -p 8889:8888  # host port : jupyter의 default port 
      -p 6006:6006  # tensorboard의 default port 
      --name tensorflow_gpu_shea  # 컨테이너 이름을 tensorflow_gpu_shea 로 설정
      tensorflow/tensorflow:latest-gpu-jupyter # 이미지의 이름과 
      jupyter notebook  # 주피터 노트북을 열라는 명령어 
      --allow-root  # 루트계정에서 서버를 여는 것을 허용 
      --ip 0.0.0.0  # default 값으로 ip설정 
      --NotebookApp.token=''  # 서버에 등록하는 인증절차를 생략 
      --no-browser # 주피터 접속 기억 실행하지 않도록
      
docker run -d --gpus all -it -v /:/smc_work -p 20300:8888 -p 8400:8400 --name jupyter_notebook_shea tensorflow/tensorflow:latest-gpu-jupyter jupyter notebook --allow-root --ip 0.0.0.0 --NotebookApp.token='' --no-browser /bin/bash 
           
```
