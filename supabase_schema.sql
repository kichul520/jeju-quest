-- Supabase 테이블 스키마
-- Supabase 대시보드 > SQL Editor에서 실행

-- 퀘스트 테이블
CREATE TABLE quests (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    question TEXT NOT NULL,           -- 퀴즈 질문
    answer VARCHAR(100) NOT NULL,     -- 정답
    latitude DECIMAL(10, 8) NOT NULL, -- 위도
    longitude DECIMAL(11, 8) NOT NULL,-- 경도
    points INTEGER DEFAULT 100,       -- 획득 포인트
    category VARCHAR(50),             -- 카테고리 (관광지, 맛집, 역사 등)
    difficulty VARCHAR(20) DEFAULT 'easy', -- 난이도
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 사용자 프로필 테이블 (Supabase Auth 연동)
CREATE TABLE profiles (
    id UUID REFERENCES auth.users(id) PRIMARY KEY,
    nickname VARCHAR(50),
    total_points INTEGER DEFAULT 0,
    hp INTEGER DEFAULT 100,
    level INTEGER DEFAULT 1,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 퀘스트 완료 기록
CREATE TABLE quest_completions (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id),
    quest_id INTEGER REFERENCES quests(id),
    completed_at TIMESTAMPTZ DEFAULT NOW(),
    points_earned INTEGER,
    UNIQUE(user_id, quest_id)
);

-- 인벤토리 (뱃지)
CREATE TABLE badges (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    image_url TEXT,
    requirement_type VARCHAR(50),  -- 'quest_count', 'category', 'special'
    requirement_value VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 사용자 뱃지
CREATE TABLE user_badges (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id),
    badge_id INTEGER REFERENCES badges(id),
    earned_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, badge_id)
);

-- 쿠폰
CREATE TABLE coupons (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    store_name VARCHAR(100),
    discount_type VARCHAR(20),     -- 'percent', 'fixed'
    discount_value INTEGER,
    image_url TEXT,
    valid_until DATE,
    points_required INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 사용자 쿠폰
CREATE TABLE user_coupons (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id),
    coupon_id INTEGER REFERENCES coupons(id),
    acquired_at TIMESTAMPTZ DEFAULT NOW(),
    used_at TIMESTAMPTZ,
    is_used BOOLEAN DEFAULT false
);

-- 샘플 퀘스트 데이터
INSERT INTO quests (title, description, question, answer, latitude, longitude, points, category) VALUES
('성산일출봉의 비밀', '성산일출봉 정상에서 제주의 일출을 감상하세요. 정상에 도착하면 특별한 미션이 주어집니다.', '성산일출봉 입구 안내판에 적힌 유네스코 등재 연도는?', '2007', 33.4588, 126.9425, 200, '관광지'),
('동문시장 탐험가', '제주에서 가장 큰 재래시장, 동문시장을 탐험해보세요!', '동문시장 입구 간판의 색깔은?', '빨간색', 33.5122, 126.5275, 100, '시장'),
('용두암의 전설', '용이 되지 못한 바위, 용두암의 전설을 찾아보세요.', '용두암 안내판에 적힌 바위의 높이는 몇 미터?', '10', 33.5167, 126.5119, 150, '관광지'),
('한라산 어리목', '한라산 어리목 탐방로 입구에서 시작하는 퀘스트입니다.', '어리목 탐방안내소 앞 이정표에서 윗세오름까지의 거리는?', '4.7km', 33.3936, 126.4953, 250, '자연'),
('제주 4.3 평화공원', '제주 4.3의 역사를 기억하고 평화를 기원합니다.', '4.3 평화기념관 입구의 상징 조형물 이름은?', '비설', 33.4289, 126.6714, 200, '역사');

-- 샘플 뱃지 데이터
INSERT INTO badges (name, description, image_url, requirement_type, requirement_value) VALUES
('첫 발자국', '첫 번째 퀘스트를 완료했습니다!', NULL, 'quest_count', '1'),
('탐험가', '10개의 퀘스트를 완료했습니다!', NULL, 'quest_count', '10'),
('역사 탐방가', '역사 카테고리 퀘스트를 모두 완료했습니다.', NULL, 'category', '역사'),
('시장 전문가', '시장 카테고리 퀘스트를 모두 완료했습니다.', NULL, 'category', '시장');

-- RLS (Row Level Security) 정책
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE quest_completions ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_badges ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_coupons ENABLE ROW LEVEL SECURITY;

-- 사용자가 자신의 데이터만 접근 가능
CREATE POLICY "Users can view own profile" ON profiles FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own profile" ON profiles FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can view own completions" ON quest_completions FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own completions" ON quest_completions FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view own badges" ON user_badges FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can view own coupons" ON user_coupons FOR SELECT USING (auth.uid() = user_id);

-- 퀘스트, 뱃지, 쿠폰은 모든 사용자가 읽기 가능
CREATE POLICY "Anyone can view quests" ON quests FOR SELECT USING (true);
CREATE POLICY "Anyone can view badges" ON badges FOR SELECT USING (true);
CREATE POLICY "Anyone can view coupons" ON coupons FOR SELECT USING (true);

-- 프로필 자동 생성 트리거
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO profiles (id, nickname)
    VALUES (NEW.id, NEW.raw_user_meta_data->>'nickname');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION handle_new_user();
