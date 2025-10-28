// DOM 요소 가져오기
const startScreen = document.getElementById('startScreen');
const gameScreen = document.getElementById('gameScreen');
const bgVideo = document.getElementById('bgVideo');

// 게임 시작 플래그
let gameStarted = false;

// 시작 화면 클릭 이벤트
startScreen.addEventListener('click', startGame);

// 키보드 이벤트 (스페이스바, 엔터로도 시작 가능)
document.addEventListener('keydown', (event) => {
    if (!gameStarted && (event.key === ' ' || event.key === 'Enter')) {
        startGame();
    }
});

// 게임 시작 함수
function startGame() {
    if (gameStarted) return; // 이미 시작했으면 중복 실행 방지

    gameStarted = true;

    // 시작 화면 페이드 아웃
    startScreen.style.opacity = '0';

    // 1초 후 화면 전환
    setTimeout(() => {
        startScreen.classList.remove('active');
        startScreen.style.display = 'none';

        // 게임 화면 표시
        gameScreen.classList.add('active');
        gameScreen.style.display = 'flex';

        // 배경 영상 정지 (선택사항)
        bgVideo.pause();

        console.log('게임이 시작되었습니다!');
    }, 1000);
}

// 영상 로드 에러 처리
bgVideo.addEventListener('error', (e) => {
    console.warn('영상을 불러올 수 없습니다. 기본 배경이 표시됩니다.');
    // 영상이 없어도 게임은 정상 작동하도록 함
});

// 페이지 로드 시 영상 재생 시도
window.addEventListener('load', () => {
    // 일부 브라우저에서 자동 재생이 막힐 수 있으므로 재시도
    bgVideo.play().catch(err => {
        console.log('자동 재생이 차단되었습니다. 클릭하여 시작하세요.');
    });
});
