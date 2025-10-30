package main;

import javax.swing.*;
import java.awt.*;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.util.ArrayList;
import java.util.List;

/**
 * 캐릭멜로디 - 메인 애플리케이션 클래스
 * 귀여운 캐릭터들을 클릭하여 음악을 창작하는 프로그램
 *
 * @author 위은서
 * @version 1.0
 * @since 2025.08.29
 */
public class CharacterMelody extends JFrame {
    private SoundPlayer soundPlayer;
    private List<Character> characters;
    private JPanel characterGridPanel;
    private JButton stopAllButton;
    private JLabel titleLabel;

    public CharacterMelody() {
        soundPlayer = new SoundPlayer();
        characters = new ArrayList<>();

        // 프레임 설정
        setTitle("캐릭멜로디 - Character Melody");
        setSize(900, 700);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);

        // 닫을 때 리소스 정리
        addWindowListener(new WindowAdapter() {
            @Override
            public void windowClosing(WindowEvent e) {
                soundPlayer.cleanup();
            }
        });

        // UI 초기화
        initializeUI();

        // 캐릭터 초기화
        initializeCharacters();

        // 캐릭터 패널 생성
        createCharacterPanels();
    }

    /**
     * UI 컴포넌트를 초기화합니다
     */
    private void initializeUI() {
        setLayout(new BorderLayout(10, 10));

        // 상단 패널 (타이틀 및 컨트롤)
        JPanel topPanel = new JPanel(new BorderLayout());
        topPanel.setBackground(new Color(255, 182, 193));
        topPanel.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));

        // 타이틀
        titleLabel = new JLabel("캐릭멜로디", SwingConstants.CENTER);
        titleLabel.setFont(new Font("맑은 고딕", Font.BOLD, 36));
        titleLabel.setForeground(Color.WHITE);
        topPanel.add(titleLabel, BorderLayout.CENTER);

        // 부제목
        JLabel subtitleLabel = new JLabel("캐릭터를 클릭하여 음악을 만들어보세요!", SwingConstants.CENTER);
        subtitleLabel.setFont(new Font("맑은 고딕", Font.PLAIN, 16));
        subtitleLabel.setForeground(Color.WHITE);
        topPanel.add(subtitleLabel, BorderLayout.SOUTH);

        add(topPanel, BorderLayout.NORTH);

        // 중앙 패널 (캐릭터 그리드)
        characterGridPanel = new JPanel();
        characterGridPanel.setLayout(new GridLayout(0, 4, 20, 20));
        characterGridPanel.setBackground(new Color(255, 240, 245));
        characterGridPanel.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));

        JScrollPane scrollPane = new JScrollPane(characterGridPanel);
        scrollPane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED);
        scrollPane.getVerticalScrollBar().setUnitIncrement(16);
        add(scrollPane, BorderLayout.CENTER);

        // 하단 패널 (컨트롤 버튼)
        JPanel bottomPanel = new JPanel(new FlowLayout(FlowLayout.CENTER, 20, 10));
        bottomPanel.setBackground(new Color(255, 240, 245));
        bottomPanel.setBorder(BorderFactory.createEmptyBorder(10, 20, 20, 20));

        // 모두 정지 버튼
        stopAllButton = new JButton("모두 정지");
        stopAllButton.setFont(new Font("맑은 고딕", Font.BOLD, 16));
        stopAllButton.setPreferredSize(new Dimension(150, 40));
        stopAllButton.setBackground(new Color(255, 100, 100));
        stopAllButton.setForeground(Color.WHITE);
        stopAllButton.setFocusPainted(false);
        stopAllButton.setCursor(new Cursor(Cursor.HAND_CURSOR));
        stopAllButton.addActionListener(e -> stopAllSounds());

        bottomPanel.add(stopAllButton);
        add(bottomPanel, BorderLayout.SOUTH);
    }

    /**
     * 캐릭터들을 초기화합니다
     */
    private void initializeCharacters() {
        // 샘플 캐릭터들 추가
        characters.add(new Character("토끼", "resources/sounds/rabbit.wav",
                "resources/images/rabbit.png", new Color(255, 192, 203)));

        characters.add(new Character("고양이", "resources/sounds/cat.wav",
                "resources/images/cat.png", new Color(255, 218, 185)));

        characters.add(new Character("강아지", "resources/sounds/dog.wav",
                "resources/images/dog.png", new Color(255, 228, 196)));

        characters.add(new Character("곰", "resources/sounds/bear.wav",
                "resources/images/bear.png", new Color(210, 180, 140)));

        characters.add(new Character("새", "resources/sounds/bird.wav",
                "resources/images/bird.png", new Color(173, 216, 230)));

        characters.add(new Character("펭귄", "resources/sounds/penguin.wav",
                "resources/images/penguin.png", new Color(176, 196, 222)));

        characters.add(new Character("판다", "resources/sounds/panda.wav",
                "resources/images/panda.png", new Color(200, 200, 200)));

        characters.add(new Character("여우", "resources/sounds/fox.wav",
                "resources/images/fox.png", new Color(255, 165, 0)));

        // 사운드 로드
        for (Character character : characters) {
            soundPlayer.loadSound(character.getName(), character.getSoundPath());
        }
    }

    /**
     * 캐릭터 패널들을 생성하여 그리드에 추가합니다
     */
    private void createCharacterPanels() {
        for (Character character : characters) {
            CharacterPanel panel = new CharacterPanel(character, soundPlayer);
            characterGridPanel.add(panel);
        }
    }

    /**
     * 모든 사운드를 정지합니다
     */
    private void stopAllSounds() {
        soundPlayer.stopAll();
        for (Character character : characters) {
            character.setPlaying(false);
        }
        characterGridPanel.repaint();

        // 피드백 애니메이션
        Timer timer = new Timer(100, null);
        timer.addActionListener(e -> {
            stopAllButton.setBackground(new Color(255, 100, 100));
            timer.stop();
        });
        stopAllButton.setBackground(new Color(200, 50, 50));
        timer.start();
    }

    /**
     * 메인 메서드
     */
    public static void main(String[] args) {
        // Look and Feel 설정
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (Exception e) {
            e.printStackTrace();
        }

        // GUI를 이벤트 디스패치 스레드에서 실행
        SwingUtilities.invokeLater(() -> {
            CharacterMelody app = new CharacterMelody();
            app.setVisible(true);

            // 환영 메시지
            JOptionPane.showMessageDialog(app,
                    "캐릭멜로디에 오신 것을 환영합니다!\n\n" +
                    "귀여운 캐릭터들을 클릭하여 소리를 재생하고,\n" +
                    "여러 캐릭터를 동시에 클릭하여 나만의 음악을 만들어보세요!\n\n" +
                    "※ 주의: 현재 샘플 음원이 없어 소리가 재생되지 않을 수 있습니다.\n" +
                    "resources/sounds/ 폴더에 WAV 파일을 추가해주세요.",
                    "환영합니다!",
                    JOptionPane.INFORMATION_MESSAGE);
        });
    }
}
