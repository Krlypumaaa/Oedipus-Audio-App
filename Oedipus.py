# Imports
import os
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QFileDialog, QSlider, QVBoxLayout, QHBoxLayout, QGraphicsBlurEffect, QGraphicsScene, QGraphicsPixmapItem
from PyQt6.QtCore import Qt, QUrl, QTimer, QSize
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtGui import QPixmap, QImage, QPainter, QIcon
from mutagen.id3 import ID3, ID3NoHeaderError


# App
class AudioApp(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.appUI()
        self.event_handler()

    # Settings
    def settings(self):
        self.setWindowTitle('Audio Player')
        self.setGeometry(50, 200, 400, 600)
        self.setFixedSize(400, 600)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setObjectName('MainWindow')
        self.current_folder = None

    # Design
    def appUI(self):
        self.bg_widget = QWidget(self)
        self.bg_widget.setObjectName("BackgroundWidget")
        self.bg_widget.lower()
        self.bg_widget.paintEvent = self.bg_paint

        #Title Bar
        self.btn_close = QPushButton('X')
        self.btn_close.setFixedSize(30, 30)
        self.btn_close.setObjectName('CloseButton')
        self.btn_minimize = QPushButton('—')
        self.btn_minimize.setFixedSize(30, 30)
        self.btn_minimize.setObjectName('MinimizeButton')

        self.song_title = QLabel('')
        self.song_title.setObjectName('SongTitle')

        #Buttons and list
        self.file_list = QListWidget()
        
        self.btn_opener = QPushButton('Select Folder')
        self.btn_opener.setObjectName('File')

        self.btn_play = QPushButton('Play')
        self.btn_play.setObjectName('Play')

        self.btn_next = QPushButton('')
        self.btn_next.setObjectName('Next')
        self.btn_next.setIcon(QIcon(r'Images/Forward.svg'))
        self.btn_next.setIconSize(QSize(32, 32))

        self.btn_pause = QPushButton('')
        self.btn_pause.setObjectName('Pause')
        self.btn_pause.setIcon(QIcon(r'Images/Pause.svg'))
        self.btn_pause.setIconSize(QSize(32, 32))

        self.btn_reset = QPushButton('')
        self.btn_reset.setObjectName('Backtrack')
        self.btn_reset.setIcon(QIcon(r'Images/Backtrack.svg'))
        self.btn_reset.setIconSize(QSize(32, 32))

        self.btn_resume = QPushButton('')
        self.btn_resume.setObjectName('Resume')
        self.btn_resume.setIcon(QIcon(r'Images/Play.svg'))
        self.btn_resume.setIconSize(QSize(32, 32))

        self.btn_loop = QPushButton('')
        self.btn_loop.setObjectName('Loop')
        loopIcon = QIcon()
        loopIcon.addFile(r'Images/Loop.svg', state=QIcon.State.On)
        loopIcon.addFile(r'Images/Loop-off.svg', state=QIcon.State.Off)
        self.btn_loop.setIcon(loopIcon)
        self.btn_loop.setCheckable(True)
        self.btn_loop.setIconSize(QSize(32, 32))

        self.btn_next.setDisabled(True)
        self.btn_pause.setDisabled(True)
        self.btn_resume.setDisabled(True)
        self.btn_reset.setDisabled(True)
        self.btn_loop.setEnabled(True)

        #Sliders
        self.slider = QSlider(Qt.Orientation.Vertical)
        self.slider.setRange(0, 100)
        self.slider.setValue(100)
        self.slider_text = QLabel('Volume: 100%')
        self.slider_text.setFixedWidth(85)

        self.slider_rate = QSlider(Qt.Orientation.Vertical)
        self.slider_rate.setRange(0, 50)
        self.slider_rate.setValue(10)
        self.slider_rate_text = QLabel('Rate: 1.0x')
        self.slider_rate_text.setObjectName('Rate')
        self.slider_rate_text.setFixedWidth(62)

        self.progress = QSlider(Qt.Orientation.Horizontal)
        self.progress.setRange(0,0)
        self.progress.setValue(0)

        self.progress_text = QLabel('0:00')
        self.progress_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        progress_layout = QHBoxLayout()
        progress_layout.addWidget(self.progress_text)
        progress_layout.addWidget(self.progress)
        
        #Song info and Settings
        parent_layout = QVBoxLayout()

        child_layout = QHBoxLayout()
        child_col1 = QVBoxLayout()
        child_col2 = QHBoxLayout()
        child_col3 = QHBoxLayout()
        child_col1.addWidget(self.slider_text, alignment=Qt.AlignmentFlag.AlignTop)
        child_col2.addWidget(self.slider, alignment=Qt.AlignmentFlag.AlignLeft)
        child_col1.addWidget(self.slider_rate_text, alignment=Qt.AlignmentFlag.AlignTop)
        child_col2.addWidget(self.slider_rate, alignment=Qt.AlignmentFlag.AlignLeft)
        child_layout.addStretch(5)
        self.album_cover = QLabel('')
        self.album_cover.setObjectName('Cover')
        child_col3.addWidget(self.album_cover, alignment=Qt.AlignmentFlag.AlignJustify)

        child_layout.addLayout(child_col1, 0)
        child_col1.addLayout(child_col2, 0)
        child_layout.addLayout(child_col3, 200)

        parent_layout.addLayout(child_layout)

        #check for loop
        self.is_Looping = False

        # Special Audio Classes from PyQt
        self.audio_output = QAudioOutput()
        self.media_player = QMediaPlayer()
        self.media_player.setAudioOutput(self.audio_output)


        # Layout
        self.master = QVBoxLayout()
        row = QVBoxLayout()
        col1 = QHBoxLayout()
        col2 = QVBoxLayout()
        col3 = QHBoxLayout()

        titlebar = QHBoxLayout()
        titlebar.addWidget(self.song_title, alignment=Qt.AlignmentFlag.AlignLeft)
        titlebar.addStretch()
        titlebar.addWidget(self.btn_minimize, alignment=Qt.AlignmentFlag.AlignRight)
        titlebar.addWidget(self.btn_close, alignment=Qt.AlignmentFlag.AlignRight)
        self.master.addLayout(titlebar)

        #self.master.addWidget(self.title)
        self.master.addLayout(parent_layout)
        self.master.addLayout(progress_layout)

        col1.addWidget(self.btn_reset)
        col1.addWidget(self.btn_pause)
        col1.addWidget(self.btn_resume)
        col1.addWidget(self.btn_loop)
        col1.addWidget(self.btn_next)
        self.master.addStretch
        col2.addWidget(self.file_list)
        col3.addWidget(self.btn_play)
        col3.addWidget(self.btn_opener)

        row.addLayout(col1, 2)
        row.addLayout(col2, 1)
        row.addLayout(col3, 1)

        self.master.addLayout(row)
        self.setLayout(self.master)

        self.style()


    #Style
    def style(self):
        with open('styling.css', 'r') as file:
            self.setStyleSheet(file.read())


    # EventHandle
    def event_handler(self):
        self.slider.valueChanged.connect(self.update_slider_volume)
        self.slider_rate.valueChanged.connect(self.update_slider_playback)
        self.btn_opener.clicked.connect(self.open_file)
        self.btn_play.clicked.connect(self.play_audio)
        self.btn_pause.clicked.connect(self.pause_audio)
        self.btn_resume.clicked.connect(self.resume_audio)
        self.media_player.durationChanged.connect(self.update_progress_max)
        self.media_player.positionChanged.connect(self.update_progress_position)
        self.progress.sliderMoved.connect(self.seek_media)
        self.file_list.itemSelectionChanged.connect(self.play_new)
        self.media_player.mediaStatusChanged.connect(self.audio_progression)
        self.btn_loop.clicked.connect(self.loop_toggle)
        self.btn_close.clicked.connect(self.close)
        self.btn_minimize.clicked.connect(self.showMinimized)
        self.btn_reset.clicked.connect(self.previous_song)
        self.btn_next.clicked.connect(self.next_song)
        self.btn_reset.clicked.connect(self.reset_audio)



    #Album Data
    def mp3_cover(self, file_path):
        try:
            tags = ID3(file_path)
            apic_frames = tags.getall('APIC')

            if apic_frames:
                image_data = apic_frames[0].data
                image = QImage()
                image.loadFromData(image_data)
                pixmap = QPixmap.fromImage(image)
                scaled_pixmap = pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation,)
                self.album_cover.setPixmap(scaled_pixmap)
                
                self.current_bg = pixmap

                scaled = pixmap.scaled(self.size(),Qt.AspectRatioMode.KeepAspectRatioByExpanding,Qt.TransformationMode.SmoothTransformation)
                self.blurred_bg = self.blur_pixmap(scaled, radius=40)
                self.bg_widget.update()

            else:
                self.album_cover.setText('')
                self.current_bg = None
            
        except Exception as e:
            print(f'Error reading MP3 tags: {e}')
            self.album_cover.setText('Error Loading Image')
    
    def mp3_title(self, file_path):
        try:
            self.song_title.setToolTip('')
            tags = ID3(file_path)
            title = tags.get('TIT2').text[0]
            self.song_title.setText(f'Now Playing: {title}')
            self.song_title.setToolTip(title)

        except ID3NoHeaderError:
            self.song_title.setText(f'Now Playing: {os.path.splitext(os.path.basename(file_path))[0]}')
        except Exception:
            self.song_title.setText('Unknown Title')


    # Change slider audio label
    def update_slider_volume(self):
        audio = self.slider.value()
        self.slider_text.setText(f'Volume: {audio}%')
        volume_float = audio / 100
        self.audio_output.setVolume(volume_float)

    #Change Audio Playback Rate
    def update_slider_playback(self):
        playback_rate = self.slider_rate.value()
        if playback_rate > 0:
            playback_float = playback_rate / 10
        elif playback_rate == 0:
            playback_float = 0.1
        self.slider_rate_text.setText(f'Rate: {playback_float:.1f}x')
        self.media_player.setPlaybackRate(playback_float)

    def update_progress_max(self, duration):
        self.progress.setMaximum(duration)

    def update_progress_position(self, position):
        self.progress.blockSignals(True)
        self.progress.setValue(position)
        self.total_seconds = position // 1000
        minutes, seconds = divmod(self.total_seconds, 60)
        self.progress_text.setText(f'{minutes}:{seconds:02d}')
        self.progress.blockSignals(False)
    
    def seek_media(self, position):
        self.media_player.setPosition(position)


    #Folder Select
    def open_file(self):
        path = QFileDialog.getExistingDirectory(self, 'Select Folder')

        if path:
            self.current_folder = path
            self.file_list.clear()
            for file_name in os.listdir(path):
                if file_name.lower().endswith(('.mp3', '.ogg', '.wav', '.flac', '.mp4')):
                    self.file_list.addItem(file_name)

    # Play Audio
    def play_audio(self):
        if self.file_list.selectedItems():
            file_name = self.file_list.selectedItems()[0].text()
            file_path = os.path.join(self.current_folder, file_name)
            file_url = QUrl.fromLocalFile(file_path)
            
            self.media_player.setSource(file_url)
            self.media_player.play()
            self.mp3_cover(file_path)
            self.mp3_title(file_path)
            self.update

            self.btn_pause.setEnabled(True)
            self.btn_resume.setDisabled(True)
            self.btn_reset.setEnabled(True)
            self.btn_play.setDisabled(True)
            self.btn_loop.setEnabled(True)
            self.btn_next.setEnabled(True)
    
    def play_new(self):
        self.btn_play.setEnabled(len(self.file_list.selectedItems()) > 0)

    def pause_audio(self):
        self.media_player.pause()
        self.btn_pause.setDisabled(True)
        self.btn_resume.setEnabled(True)

    def resume_audio(self):
        self.media_player.play()
        self.btn_pause.setEnabled(True)
        self.btn_resume.setDisabled(True)
    
    #Backtrack, Reset, Previous Song, and Next Song
    def previous_song(self, position):
        current_row = self.file_list.currentRow()
        previous_row = current_row - 1
        if self.total_seconds <= 1.5:
            if previous_row >= 0:
                self.file_list.setCurrentRow(previous_row)
                self.play_audio()
        else:
            pass

    def next_song(self):
        current_row = self.file_list.currentRow()
        next_row = current_row + 1
        if next_row < self.file_list.count():
            self.file_list.setCurrentRow(next_row)
            self.play_audio()
        else:
            pass

    def reset_audio(self):
        if self.media_player.isPlaying():
            self.media_player.stop
        
        if self.total_seconds > 1.5:
            self.media_player.setPosition(0)
            self.audio_output.setVolume(self.slider.value())
            self.media_player.play

            self.btn_reset.setDisabled(True)
            self.btn_play.setDisabled(True)

            QTimer.singleShot(100, lambda: self.btn_reset.setEnabled(True))
        else:
            pass

    #Loop
    def loop_toggle(self):
        self.is_Looping = self.btn_loop.isChecked()

    def audio_progression(self, status):
        current_row = self.file_list.currentRow()
        next_row = current_row + 1
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            if self.is_Looping:
                self.media_player.setPosition(0)
                self.media_player.play()
                
            elif next_row < self.file_list.count():
                self.file_list.setCurrentRow(next_row)
                self.play_audio()


    #Move Window
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            new_pos = self.pos() + (event.globalPosition().toPoint() - self.drag_pos)
            self.move(new_pos)
            self.drag_pos = event.globalPosition().toPoint()

    #Bg Blur
    def resizeEvent(self, event):
        self.bg_widget.resize(self.size())
        super().resizeEvent(event)

    def blur_pixmap(self, pixmap, radius=40):
        scene = QGraphicsScene()
        item = QGraphicsPixmapItem(pixmap)
        blur = QGraphicsBlurEffect()
        blur.setBlurRadius(radius)
        item.setGraphicsEffect(blur)
        scene.addItem(item)
        blurred = QPixmap(pixmap.size())
        blurred.fill(Qt.GlobalColor.transparent)

        painter = QPainter(blurred)
        scene.render(painter)
        painter.end()

        return blurred

    def bg_paint(self, event):
        if hasattr(self, "blurred_bg") and self.blurred_bg:
            painter = QPainter(self.bg_widget)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
            painter.drawPixmap(0, 0, self.blurred_bg)

# Boilerplate
if __name__ in "__main__":
    app = QApplication([])
    main = AudioApp()
    main.show()
    app.exec()