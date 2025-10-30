package main;

import javax.swing.*;
import java.awt.*;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.io.File;
import javax.imageio.ImageIO;

/**
 * 캐릭터를 표현하는 UI 패널
 * 클릭하면 캐릭터의 사운드가 재생됩니다.
 */
public class CharacterPanel extends JPanel {
    private Character character;
    private SoundPlayer soundPlayer;
    private Image characterImage;
    private boolean isHovered = false;

    private static final int PANEL_WIDTH = 150;
    private static final int PANEL_HEIGHT = 180;

    public CharacterPanel(Character character, SoundPlayer soundPlayer) {
        this.character = character;
        this.soundPlayer = soundPlayer;

        setPreferredSize(new Dimension(PANEL_WIDTH, PANEL_HEIGHT));
        setBackground(Color.WHITE);
        setBorder(BorderFactory.createLineBorder(Color.GRAY, 2));
        setCursor(new Cursor(Cursor.HAND_CURSOR));

        // 이미지 로드
        loadImage();

        // 마우스 이벤트 리스너
        addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                toggleSound();
            }

            @Override
            public void mouseEntered(MouseEvent e) {
                isHovered = true;
                repaint();
            }

            @Override
            public void mouseExited(MouseEvent e) {
                isHovered = false;
                repaint();
            }
        });
    }

    /**
     * 캐릭터 이미지를 로드합니다
     */
    private void loadImage() {
        try {
            File imageFile = new File(character.getImagePath());
            if (imageFile.exists()) {
                characterImage = ImageIO.read(imageFile);
            }
        } catch (Exception e) {
            System.err.println("이미지 로드 실패: " + character.getImagePath());
        }
    }

    /**
     * 사운드 재생/정지를 토글합니다
     */
    private void toggleSound() {
        if (character.isPlaying()) {
            soundPlayer.stop(character.getName());
            character.setPlaying(false);
        } else {
            soundPlayer.play(character.getName());
            character.setPlaying(true);
        }
        repaint();
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2d = (Graphics2D) g;
        g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

        // 배경색 설정 (재생 중이거나 호버 시 변경)
        if (character.isPlaying()) {
            g2d.setColor(new Color(character.getColor().getRed(),
                                   character.getColor().getGreen(),
                                   character.getColor().getBlue(), 180));
            g2d.fillRect(0, 0, getWidth(), getHeight());
        } else if (isHovered) {
            g2d.setColor(new Color(240, 240, 240));
            g2d.fillRect(0, 0, getWidth(), getHeight());
        }

        // 캐릭터 이미지 그리기
        if (characterImage != null) {
            int imgWidth = 100;
            int imgHeight = 100;
            int x = (getWidth() - imgWidth) / 2;
            int y = 20;
            g2d.drawImage(characterImage, x, y, imgWidth, imgHeight, this);
        } else {
            // 이미지가 없으면 원으로 대체
            int diameter = 80;
            int x = (getWidth() - diameter) / 2;
            int y = 30;
            g2d.setColor(character.getColor());
            g2d.fillOval(x, y, diameter, diameter);

            // 얼굴 그리기
            g2d.setColor(Color.BLACK);
            // 눈
            g2d.fillOval(x + 20, y + 25, 10, 10);
            g2d.fillOval(x + 50, y + 25, 10, 10);
            // 입
            g2d.drawArc(x + 20, y + 40, 40, 20, 0, -180);
        }

        // 캐릭터 이름
        g2d.setColor(Color.BLACK);
        g2d.setFont(new Font("맑은 고딕", Font.BOLD, 14));
        FontMetrics fm = g2d.getFontMetrics();
        int textWidth = fm.stringWidth(character.getName());
        int textX = (getWidth() - textWidth) / 2;
        g2d.drawString(character.getName(), textX, 140);

        // 재생 상태 표시
        if (character.isPlaying()) {
            g2d.setFont(new Font("맑은 고딕", Font.PLAIN, 12));
            String status = "♪ 재생 중";
            textWidth = fm.stringWidth(status);
            textX = (getWidth() - textWidth) / 2;
            g2d.setColor(new Color(0, 150, 0));
            g2d.drawString(status, textX, 160);
        }
    }

    /**
     * 캐릭터 객체를 반환합니다
     */
    public Character getCharacter() {
        return character;
    }
}
