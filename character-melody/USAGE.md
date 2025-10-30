# 캐릭멜로디 사용 가이드

## 빠른 시작

### 1. 컴파일

```bash
cd character-melody
./compile.sh
```

또는 수동 컴파일:

```bash
mkdir -p bin
javac -d bin -encoding UTF-8 \
    src/main/Character.java \
    src/main/SoundPlayer.java \
    src/main/CharacterPanel.java \
    src/main/CharacterMelody.java
```

### 2. 실행

```bash
./run.sh
```

또는:

```bash
java -cp bin main.CharacterMelody
```

## 상세 설정

### 음원 준비

1. `resources/sounds/` 폴더에 WAV 파일 추가:
   - rabbit.wav
   - cat.wav
   - dog.wav
   - bear.wav
   - bird.wav
   - penguin.wav
   - panda.wav
   - fox.wav

2. 음원은 2-4초 길이의 루프 가능한 소리 권장

### 이미지 추가 (선택사항)

`resources/images/` 폴더에 PNG 파일 추가
- 이미지가 없어도 자동으로 귀여운 기본 캐릭터가 표시됩니다.

## 조작 방법

1. **캐릭터 클릭**: 캐릭터를 클릭하여 소리 재생 시작
2. **다시 클릭**: 같은 캐릭터를 다시 클릭하여 소리 정지
3. **여러 캐릭터**: 여러 캐릭터를 동시에 클릭하여 음악 조합
4. **모두 정지**: 하단의 "모두 정지" 버튼으로 모든 소리 중지

## 문제 해결

### 소리가 나지 않아요
- `resources/sounds/` 폴더에 WAV 파일이 있는지 확인
- 파일 이름이 정확한지 확인 (rabbit.wav, cat.wav 등)
- WAV 형식인지 확인 (MP3는 지원하지 않음)

### 컴파일 오류
- Java 8 이상이 설치되어 있는지 확인
- `javac -version` 명령으로 확인

### 한글이 깨져요
- 컴파일 시 `-encoding UTF-8` 옵션이 포함되었는지 확인
- compile.sh 스크립트 사용 권장

## 시스템 요구사항

- Java 8 이상
- 오디오 출력 장치
- 그래픽 디스플레이 (GUI)

## 추가 정보

자세한 내용은 README.md를 참조하세요.
