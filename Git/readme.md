## 먼저 git을 다운로드 받아 설치한다

### 로컬 컴퓨터에서 초기 환경 설정

``` 
git config --global user.name "clastro"
git config --global user.email "email@example.com"
```

### Repository에 있는 git 주소 복사

``` 
https://github.com/folder/project.git
```

### Git 복사

```
git clone https://github.com/folder/project.git #이러면 하드에 해당 Github 폴더가 만들어짐
```

### 업데이트할 폴더에 새로운 파일을 옮겨 놓거나 그 폴더에서 파일 생성 

``` 
cp /some/path/analysis1.ipynb /path/of/projectA/
```

### git 추가하기
```
git add analysis1.ipynb
```

### git 상태보기
```
git status
```

### git commit
```
git commit -m "깃헙에 커밋하는 메세지"
```

### git push

```
git push #동기화 완료 직전에 권한 어떻게 줄 거냐고 물어봄
```

### git 여러 개 

```
git tag; git branch # ; : 여러개 명령어 묶어서 사용
```
