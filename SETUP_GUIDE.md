# 제주 퀘스트 - 설정 가이드

## 1. Supabase 프로젝트 생성 가이드

### Step 1: 회원가입
1. https://supabase.com 접속
2. **Start your project** 클릭
3. GitHub 계정으로 로그인 (가장 간편)

### Step 2: 새 프로젝트 생성
1. **New Project** 클릭
2. 정보 입력:
   ```
   Organization: (기본값 사용)
   Project name: jeju-quest
   Database Password: (강력한 비밀번호 - 기억해두세요!)
   Region: Northeast Asia (Seoul) ← 한국 리전 선택!
   ```
3. **Create new project** 클릭
4. 2-3분 대기 (프로젝트 생성 중...)

### Step 3: API 키 복사
프로젝트 생성 완료 후:

1. 왼쪽 메뉴 **Project Settings** (톱니바퀴) 클릭
2. **API** 탭 클릭
3. 두 가지 복사:

```
Project URL: https://xxxxxxxx.supabase.co
         ↓
.env 파일의 SUPABASE_URL에 입력

service_role key (secret): eyJhbGciOiJ...
         ↓
.env 파일의 SUPABASE_KEY에 입력
```

> **주의**: `anon key`가 아닌 `service_role key`를 복사하세요!

### Step 4: 데이터베이스 테이블 생성
1. 왼쪽 메뉴 **SQL Editor** 클릭
2. **New query** 클릭
3. `supabase_schema.sql` 파일 내용 전체 복사 → 붙여넣기
4. **Run** (Ctrl+Enter) 클릭
5. "Success" 메시지 확인

### Step 5: 테이블 확인
1. 왼쪽 메뉴 **Table Editor** 클릭
2. 생성된 테이블 확인:
   - `quests` (샘플 퀘스트 5개 포함)
   - `profiles`
   - `quest_completions`
   - `badges`
   - `user_badges`
   - `coupons`
   - `user_coupons`

---

## 2. 카카오맵 API 설정 가이드

### Step 1: 카카오 개발자 가입
1. https://developers.kakao.com 접속
2. **로그인** (카카오 계정 필요)
3. 처음이면 개발자 등록 진행

### Step 2: 애플리케이션 생성
1. 상단 메뉴 **내 애플리케이션** 클릭
2. **애플리케이션 추가하기** 클릭
3. 정보 입력:
   ```
   앱 이름: 제주퀘스트
   사업자명: (본인 이름)
   ```
4. **저장** 클릭

### Step 3: JavaScript 키 복사
1. 생성된 앱 클릭
2. **앱 키** 섹션에서:
   ```
   JavaScript 키: xxxxxxxxxxxxxxxxxxxxxx
            ↓
   .env 파일의 KAKAO_JS_KEY에 입력
   ```

### Step 4: 플랫폼 등록 (중요!)
1. 왼쪽 메뉴 **플랫폼** 클릭
2. **Web 플랫폼 등록** 클릭
3. 사이트 도메인 추가:

**로컬 개발용:**
```
http://localhost:8000
```

**Railway 배포 후 추가:**
```
https://your-app-name.up.railway.app
```

4. **저장** 클릭

### Step 5: 동의항목 설정 (선택)
지도만 사용하면 별도 설정 불필요. 카카오 로그인 추가 시 필요.

---

## 3. Railway 배포 가이드

### Step 1: Railway 가입
1. https://railway.app 접속
2. **Login** → **Login with GitHub** 클릭
3. GitHub 권한 허용

### Step 2: GitHub 저장소 생성
먼저 프로젝트를 GitHub에 올려야 합니다:

```bash
cd C:\Users\user\Jeju-Quest

# Git 초기화
git init

# 모든 파일 추가
git add .

# 첫 커밋
git commit -m "Initial commit: Jeju Quest MVP"

# GitHub에서 새 저장소 생성 후 연결
# (GitHub에서 jeju-quest 저장소 만들기)
git remote add origin https://github.com/YOUR_USERNAME/jeju-quest.git
git branch -M main
git push -u origin main
```

### Step 3: Railway 프로젝트 생성
1. Railway 대시보드에서 **New Project** 클릭
2. **Deploy from GitHub repo** 선택
3. **Configure GitHub App** → 저장소 접근 허용
4. `jeju-quest` 저장소 선택
5. **Deploy Now** 클릭

### Step 4: 환경 변수 설정 (중요!)
배포가 시작되면:

1. 프로젝트 클릭 → **Variables** 탭
2. **New Variable** 클릭하여 추가:

```
SUPABASE_URL = https://xxxxxxxx.supabase.co
SUPABASE_KEY = eyJhbGciOiJ... (service_role key)
KAKAO_JS_KEY = xxxxxxxxxxxxxxxxxxxxxx
SECRET_KEY = 랜덤문자열-32자이상-아무거나
DEBUG = false
```

3. 변수 추가하면 자동으로 재배포됨

### Step 5: 도메인 확인
1. **Settings** 탭 클릭
2. **Domains** 섹션에서 URL 확인:
   ```
   https://jeju-quest-production.up.railway.app
   ```
3. 이 URL을 카카오 개발자 플랫폼에 추가!

### Step 6: 배포 확인
1. **Deployments** 탭에서 로그 확인
2. 성공하면 URL 클릭하여 사이트 확인

---

## 4. .env 파일 설정

위 과정을 완료하면 `.env` 파일을 이렇게 채우세요:

```env
# App
DEBUG=false
SECRET_KEY=my-super-secret-key-change-this-123

# Supabase (Step 1에서 복사)
SUPABASE_URL=https://abcdefgh.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Kakao Map (Step 2에서 복사)
KAKAO_JS_KEY=1234567890abcdef1234567890abcdef
```

---

## 5. 체크리스트

| 단계 | 작업 | 완료 |
|------|------|------|
| 1-1 | Supabase 가입 | ☐ |
| 1-2 | 프로젝트 생성 (Tokyo 리전) | ☐ |
| 1-3 | API 키 복사 (service_role) | ☐ |
| 1-4 | SQL 스키마 실행 | ☐ |
| 2-1 | 카카오 개발자 가입 | ☐ |
| 2-2 | 앱 생성 | ☐ |
| 2-3 | JavaScript 키 복사 | ☐ |
| 2-4 | localhost:8000 플랫폼 등록 | ☐ |
| 3-1 | GitHub 저장소 생성 및 push | ☐ |
| 3-2 | Railway 프로젝트 생성 | ☐ |
| 3-3 | 환경 변수 4개 설정 | ☐ |
| 3-4 | Railway URL을 카카오 플랫폼에 추가 | ☐ |

---

## 6. 예상 소요 시간
- Supabase: 10분
- 카카오맵: 5분
- Railway: 10분
- **총 25분**

---

## 7. 로컬 개발 환경 (선택)

배포 전 로컬에서 테스트하려면:

```bash
# 가상환경 생성
python -m venv .venv
.venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# .env 파일 생성
copy .env.example .env
# .env 편집하여 키 입력

# 서버 실행
uvicorn app.main:app --reload

# 브라우저에서 http://localhost:8000 접속
```

---

## 8. 문제 해결

### Supabase 연결 오류
- `SUPABASE_URL`과 `SUPABASE_KEY`가 정확한지 확인
- `service_role` 키를 사용했는지 확인 (anon key 아님)

### 카카오맵이 안 보임
- 플랫폼에 도메인이 등록되었는지 확인
- JavaScript 키가 정확한지 확인
- 브라우저 콘솔(F12)에서 오류 확인

### Railway 배포 실패
- **Deployments** 탭에서 로그 확인
- 환경 변수가 모두 설정되었는지 확인
- `Dockerfile`이 프로젝트 루트에 있는지 확인
