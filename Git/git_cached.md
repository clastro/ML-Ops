### Git에서 DS_Store 라는 파일을 모든 폴더에서 찾고 Git Server에서만 삭제 하는 방법

```
find . -name .DS_Store -exec git rm --cached {} \;
```

### 최근 커밋을 취소하고, 커밋된 변경 사항을 스테이징 상태로 유지

```
git reset --soft HEAD~1
```
- --soft : 커밋을 되돌리지만, 스테이징 영역에 그대로 두고 파일은 변경되지 않은 상태 유지
- HEAD~1 : 현재 기준 1단계 이전 커밋으로
