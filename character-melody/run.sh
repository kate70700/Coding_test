#!/bin/bash

# 캐릭멜로디 실행 스크립트

echo "캐릭멜로디 실행 중..."

# bin 디렉토리 확인
if [ ! -d "bin" ]; then
    echo "❌ 컴파일된 파일이 없습니다."
    echo "먼저 compile.sh를 실행하세요:"
    echo "  ./compile.sh"
    exit 1
fi

# 프로그램 실행
java -cp bin main.CharacterMelody
