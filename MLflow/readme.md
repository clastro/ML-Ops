### MLflow란?

A Machine Learning Lifecycle Platform

ML 모델의 실험을 tracking하고 model을 공유 및 관리할 수 있도록 지원하는 라이브러리

Install MLFlow

``` pip install mlflow ```

MLFlow UI 보기

``` mlflow ui --host 0.0.0.0 -p 5001 # 외부 접속 Port는 5001로 열기 ``` 

``` docker에서 접근 허용된 PORT를 입력할 것 ```


MLFLOW 기본 폴더에 접근

``` 
mlflow.get_experiment("0")
mlflow.get_experiment_by_name("Default")
```

