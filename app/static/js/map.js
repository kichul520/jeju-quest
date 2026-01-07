// 지도 앱 - Alpine.js와 카카오맵 연동
function mapApp() {
    return {
        map: null,
        myLocation: { lat: 33.4996, lng: 126.5312 }, // 제주시 기본 좌표
        myMarker: null,
        questMarkers: [],
        quests: [],
        selectedQuest: null,
        hp: 100,
        points: 0,
        watchId: null,

        async init() {
            // 카카오맵 초기화
            const container = document.getElementById('map');
            const options = {
                center: new kakao.maps.LatLng(this.myLocation.lat, this.myLocation.lng),
                level: 5
            };
            this.map = new kakao.maps.Map(container, options);

            // 현재 위치 추적 시작
            this.startWatchingPosition();

            // 퀘스트 마커 로드
            await this.loadQuests();

            // 전역에서 접근 가능하도록
            window.mapApp = this;
        },

        startWatchingPosition() {
            if (!navigator.geolocation) {
                console.error('Geolocation not supported');
                return;
            }

            // 현재 위치 한 번 가져오기
            navigator.geolocation.getCurrentPosition(
                (pos) => this.updateMyLocation(pos),
                (err) => console.error('위치 오류:', err),
                { enableHighAccuracy: true }
            );

            // 위치 계속 추적
            this.watchId = navigator.geolocation.watchPosition(
                (pos) => this.updateMyLocation(pos),
                (err) => console.error('위치 추적 오류:', err),
                {
                    enableHighAccuracy: true,
                    timeout: 10000,
                    maximumAge: 5000
                }
            );
        },

        updateMyLocation(position) {
            this.myLocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

            const latLng = new kakao.maps.LatLng(this.myLocation.lat, this.myLocation.lng);

            // 내 위치 마커 업데이트
            if (this.myMarker) {
                this.myMarker.setPosition(latLng);
            } else {
                // 커스텀 마커 이미지 (파란 점)
                const markerImage = new kakao.maps.MarkerImage(
                    'data:image/svg+xml,' + encodeURIComponent(`
                        <svg width="24" height="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <circle cx="12" cy="12" r="8" fill="#3B82F6" stroke="white" stroke-width="3"/>
                        </svg>
                    `),
                    new kakao.maps.Size(24, 24),
                    { offset: new kakao.maps.Point(12, 12) }
                );

                this.myMarker = new kakao.maps.Marker({
                    position: latLng,
                    map: this.map,
                    image: markerImage,
                    zIndex: 10
                });
            }

            // 주변 퀘스트 거리 업데이트
            this.updateQuestDistances();
        },

        async loadQuests() {
            try {
                const response = await fetch(
                    `/api/quests/nearby?latitude=${this.myLocation.lat}&longitude=${this.myLocation.lng}&radius=5000`
                );
                const data = await response.json();
                this.quests = data.quests || [];

                // 기존 마커 제거
                this.questMarkers.forEach(m => m.setMap(null));
                this.questMarkers = [];

                // 퀘스트 마커 추가
                this.quests.forEach(quest => {
                    this.addQuestMarker(quest);
                });
            } catch (error) {
                console.error('퀘스트 로드 실패:', error);
            }
        },

        addQuestMarker(quest) {
            const latLng = new kakao.maps.LatLng(quest.latitude, quest.longitude);

            // 퀘스트 마커 이미지 (주황색 핀)
            const markerImage = new kakao.maps.MarkerImage(
                'data:image/svg+xml,' + encodeURIComponent(`
                    <svg width="32" height="40" viewBox="0 0 32 40" xmlns="http://www.w3.org/2000/svg">
                        <path d="M16 0C7.163 0 0 7.163 0 16c0 12 16 24 16 24s16-12 16-24C32 7.163 24.837 0 16 0z" fill="#F97316"/>
                        <circle cx="16" cy="14" r="6" fill="white"/>
                        <text x="16" y="17" text-anchor="middle" font-size="10" fill="#F97316">Q</text>
                    </svg>
                `),
                new kakao.maps.Size(32, 40),
                { offset: new kakao.maps.Point(16, 40) }
            );

            const marker = new kakao.maps.Marker({
                position: latLng,
                map: this.map,
                image: markerImage,
                title: quest.title
            });

            // 마커 클릭 이벤트
            kakao.maps.event.addListener(marker, 'click', () => {
                this.showQuest(quest);
            });

            this.questMarkers.push(marker);
        },

        showQuest(quest) {
            // 거리 계산
            quest.distance = this.calculateDistance(
                this.myLocation.lat, this.myLocation.lng,
                quest.latitude, quest.longitude
            );
            this.selectedQuest = quest;
        },

        calculateDistance(lat1, lon1, lat2, lon2) {
            const R = 6371000; // 지구 반지름 (미터)
            const phi1 = lat1 * Math.PI / 180;
            const phi2 = lat2 * Math.PI / 180;
            const deltaPhi = (lat2 - lat1) * Math.PI / 180;
            const deltaLambda = (lon2 - lon1) * Math.PI / 180;

            const a = Math.sin(deltaPhi / 2) ** 2 +
                      Math.cos(phi1) * Math.cos(phi2) * Math.sin(deltaLambda / 2) ** 2;
            const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

            return Math.round(R * c);
        },

        updateQuestDistances() {
            this.quests.forEach(quest => {
                quest.distance = this.calculateDistance(
                    this.myLocation.lat, this.myLocation.lng,
                    quest.latitude, quest.longitude
                );
            });
        },

        moveToMyLocation() {
            if (this.myLocation) {
                const latLng = new kakao.maps.LatLng(this.myLocation.lat, this.myLocation.lng);
                this.map.setCenter(latLng);
                this.map.setLevel(3);
            }
        },

        navigateTo(lat, lng) {
            // 카카오맵 길찾기 열기
            const url = `https://map.kakao.com/link/to/퀘스트,${lat},${lng}`;
            window.open(url, '_blank');
        },

        destroy() {
            if (this.watchId) {
                navigator.geolocation.clearWatch(this.watchId);
            }
        }
    };
}
