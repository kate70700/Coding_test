package main;

import java.awt.Color;

/**
 * 캐릭터 모델 클래스
 * 각 캐릭터는 고유한 소리와 시각적 특성을 가집니다.
 */
public class Character {
    private String name;
    private String soundPath;
    private String imagePath;
    private Color color;
    private boolean isPlaying;

    public Character(String name, String soundPath, String imagePath, Color color) {
        this.name = name;
        this.soundPath = soundPath;
        this.imagePath = imagePath;
        this.color = color;
        this.isPlaying = false;
    }

    // Getters
    public String getName() {
        return name;
    }

    public String getSoundPath() {
        return soundPath;
    }

    public String getImagePath() {
        return imagePath;
    }

    public Color getColor() {
        return color;
    }

    public boolean isPlaying() {
        return isPlaying;
    }

    // Setters
    public void setPlaying(boolean playing) {
        this.isPlaying = playing;
    }

    @Override
    public String toString() {
        return "Character{" +
                "name='" + name + '\'' +
                ", soundPath='" + soundPath + '\'' +
                ", isPlaying=" + isPlaying +
                '}';
    }
}
