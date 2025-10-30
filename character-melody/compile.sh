#!/bin/bash

# 캐릭멜로디 컴파일 스크립트

echo "캐릭멜로디 컴파일 중..."

# bin 디렉토리 생성
mkdir -p bin

# 소스 파일 컴파일 (개별 파일 지정)
javac -d bin -encoding UTF-8 \
    src/main/Character.java \
    src/main/SoundPlayer.java \
    src/main/CharacterPanel.java \
    src/main/CharacterMelody.java

# 컴파일 결과 확인
if [ $? -eq 0 ]; then
    echo "✅ 컴파일 완료!"
    echo ""
    echo "실행하려면 다음 명령어를 사용하세요:"
    echo "  java -cp bin main.CharacterMelody"
    echo ""
    echo "또는 run.sh 스크립트를 실행하세요:"
    echo "  ./run.sh"
else
    echo "❌ 컴파일 실패!"
    exit 1
fi
