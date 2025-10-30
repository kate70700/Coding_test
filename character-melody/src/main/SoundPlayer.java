package main;

import javax.sound.sampled.*;
import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

/**
 * 사운드 재생 시스템
 * 오디오 파일을 로드하고 재생하는 기능을 제공합니다.
 */
public class SoundPlayer {
    private Map<String, Clip> clips;
    private Map<String, FloatControl> volumeControls;

    public SoundPlayer() {
        clips = new HashMap<>();
        volumeControls = new HashMap<>();
    }

    /**
     * 사운드 파일을 로드합니다.
     * @param name 사운드 식별자
     * @param filePath 사운드 파일 경로
     */
    public void loadSound(String name, String filePath) {
        try {
            File soundFile = new File(filePath);
            if (!soundFile.exists()) {
                System.err.println("사운드 파일을 찾을 수 없습니다: " + filePath);
                return;
            }

            AudioInputStream audioStream = AudioSystem.getAudioInputStream(soundFile);
            Clip clip = AudioSystem.getClip();
            clip.open(audioStream);

            clips.put(name, clip);

            // 볼륨 컨트롤 설정
            if (clip.isControlSupported(FloatControl.Type.MASTER_GAIN)) {
                FloatControl volumeControl = (FloatControl) clip.getControl(FloatControl.Type.MASTER_GAIN);
                volumeControls.put(name, volumeControl);
            }

            System.out.println("사운드 로드 완료: " + name);
        } catch (UnsupportedAudioFileException e) {
            System.err.println("지원하지 않는 오디오 형식: " + filePath);
        } catch (IOException e) {
            System.err.println("파일 읽기 오류: " + filePath);
        } catch (LineUnavailableException e) {
            System.err.println("오디오 라인을 사용할 수 없습니다: " + filePath);
        }
    }

    /**
     * 사운드를 재생합니다 (루프)
     * @param name 사운드 식별자
     */
    public void play(String name) {
        Clip clip = clips.get(name);
        if (clip != null) {
            clip.setFramePosition(0);
            clip.loop(Clip.LOOP_CONTINUOUSLY);
            clip.start();
        }
    }

    /**
     * 사운드를 정지합니다
     * @param name 사운드 식별자
     */
    public void stop(String name) {
        Clip clip = clips.get(name);
        if (clip != null && clip.isRunning()) {
            clip.stop();
            clip.setFramePosition(0);
        }
    }

    /**
     * 사운드가 재생 중인지 확인합니다
     * @param name 사운드 식별자
     * @return 재생 중이면 true
     */
    public boolean isPlaying(String name) {
        Clip clip = clips.get(name);
        return clip != null && clip.isRunning();
    }

    /**
     * 볼륨을 설정합니다
     * @param name 사운드 식별자
     * @param volume 볼륨 (0.0 ~ 1.0)
     */
    public void setVolume(String name, float volume) {
        FloatControl volumeControl = volumeControls.get(name);
        if (volumeControl != null) {
            float min = volumeControl.getMinimum();
            float max = volumeControl.getMaximum();
            float gain = min + (max - min) * volume;
            volumeControl.setValue(gain);
        }
    }

    /**
     * 모든 사운드를 정지합니다
     */
    public void stopAll() {
        for (Clip clip : clips.values()) {
            if (clip.isRunning()) {
                clip.stop();
                clip.setFramePosition(0);
            }
        }
    }

    /**
     * 리소스를 해제합니다
     */
    public void cleanup() {
        for (Clip clip : clips.values()) {
            clip.close();
        }
        clips.clear();
        volumeControls.clear();
    }
}
