from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.core.audio import SoundLoader
from kivy.utils import get_color_from_hex
from kivy.graphics.texture import Texture
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window

import cv2
import numpy as np 

imagelvl1 = ['p11.png', 'p12.png', 'p13.png', 'p14.png', 'p15.png', 'p16.png', 'p17.png']
imagelvl2 = ['p21.png', 'p22.png', 'p23.png', 'p24.png', 'p25.png', 'p26.png']


level_music_1 = ['textlv11.mp3', 'textlv12.mp3', 'textlv13.mp3', 'textlv14.mp3', 'textlv15.mp3', 'textlv16.mp3', 'textlv17.mp3']
level_music_2 = ['textlv21.mp3', 'textlv22.mp3', 'textlv23.mp3', 'textlv24.mp3', 'textlv25.mp3', 'textlv26.mp3', 'textlv27.mp3']

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.music = None
        self.button_click_sound = SoundLoader.load('button_click.mp3')

        layout = FloatLayout()
        Window.size = (600, 800)

        # Image
        image = Image(source='menu_image.png', size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5}, allow_stretch=True, keep_ratio=False)
        layout.add_widget(image)

        # Decorate Play button
        play_button = Button(text='Chơi', size_hint=(None, None), size=(250, 50),
                             pos_hint={'center_x': 0.5, 'center_y': 0.35},
                             background_color=(0, 0.5, 1, 1), font_size=24, color=(1, 1, 1, 1))
        play_button.bind(on_release=self.go_to_levels)
        play_button.bind(on_press=self.play_button_sound)
        layout.add_widget(play_button)

        # Decorate Credits button
        credits_button = Button(text='Thông tin', size_hint=(None, None), size=(100, 50),
                                pos_hint={'x': 0.02, 'y': 0.02},
                                background_color=(0, 0.5, 1, 1), font_size=14, color=(1, 1, 1, 1))
        credits_button.bind(on_release=self.show_credits)
        credits_button.bind(on_press=self.play_button_sound)
        layout.add_widget(credits_button)

        # Decorate Instruction button
        instruction_button = Button(text='Hướng dẫn', size_hint=(None, None), size=(100, 50),
                                    pos_hint={'center_x': 0.5, 'y': 0.02},
                                    background_color=(0, 0.5, 1, 1), font_size=14, color=(1, 1, 1, 1))
        instruction_button.bind(on_release=self.show_instruction)
        instruction_button.bind(on_press=self.play_button_sound)
        layout.add_widget(instruction_button)

        # Decorate Contact us button
        contact_button = Button(text='Liên hệ', size_hint=(None, None), size=(100, 50),
                                pos_hint={'right': 0.98, 'y': 0.02},
                                background_color=(0, 0.5, 1, 1), font_size=14, color=(1, 1, 1, 1))
        contact_button.bind(on_release=self.show_contact)
        contact_button.bind(on_press=self.play_button_sound)
        layout.add_widget(contact_button)

        self.add_widget(layout)

    def on_enter(self, *args):
        self.play_music('menu_music.mp3')

    def on_leave(self, *args):
        self.stop_music()

    def play_music(self, filename):
        self.music = SoundLoader.load(filename)
        if self.music:
            self.music.loop = True
            self.music.play()

    def stop_music(self):
        if self.music:
            self.music.stop()
            self.music.unload()

    def play_button_sound(self, instance):
        if self.button_click_sound:
            self.button_click_sound.play()

    def go_to_levels(self, instance):
        self.manager.current = 'levels'

    def show_popup(self, title, text):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        scrollview = ScrollView(size_hint=(1, None), size=(Window.width * 0.8, Window.height * 0.6))
        
        text_label = Label(text=text, size_hint_y=None, height=Window.height * 0.6)
        text_label.bind(texture_size=text_label.setter('size'))
        
        scrollview.add_widget(text_label)
        content.add_widget(scrollview)

        close_button = Button(text='Đóng', size_hint=(None, None), size=(100, 50),
                              background_color=(1, 0, 0, 1), font_size=14, color=(1, 1, 1, 1))
        content.add_widget(close_button)

        popup = Popup(title=title, content=content, size_hint=(0.8, 0.8))
        close_button.bind(on_release=popup.dismiss)
        close_button.bind(on_release=self.play_button_sound)
        popup.open()

    def show_credits(self, instance):
        self.show_popup('Credits', 'Ứng dụng này được tạo bởi SayDoo Team')

    def show_instruction(self, instance):
        self.show_popup('Instruction', '''
    Chào mừng các bố mẹ và các bé đến
    với PaintPal, ứng dụng tô màu đầy
    thú vị và bổ ích dành cho các bé! 
    PaintPal không chỉ là một trò 
    chơi giải trí mà còn là công cụ 
    giáo dục giúp các bé khám phá 
    và hiểu thêm về những câu chuyện
    cổ tích Việt Nam qua từng bức tranh 
    đầy màu sắc. Dưới đây là hướng dẫn 
    ngắn để bố mẹ có thể giúp các bé 
    làm quen với PaintPal!

    Hướng dẫn tô màu:
    -Bước 1: Trên giao diện chính, chọn
    một câu chuyện cổ tích mà bé muốn 
    khám phá. Mỗi câu chuyện sẽ bao 
    gồm nhiều bức tranh để bé tô màu. 
    -Bước 2: Chọn một bức tranh từ câu 
    chuyện đã chọn. Bé có thể chọn màu 
    sắc yêu thích từ bảng màu ở phía 
    dưới màn hình. 
    -Bước 3: Dùng ngón tay để tô màu 
    từng vùng trên bức tranh. Hoàn thiện 
    bức tranh sẽ giúp câu chuyện 
    tiếp tục.

    Tích Hợp Kể Chuyện Bằng Giọng Nói:
    -Bước 1: Sau khi hoàn thành từng
    bức tranh, ứng dụng sẽ tự động 
    kích hoạt tính năng kể chuyện 
    bằng giọng nói.
    -Bước 2: Bé có thể lắng nghe và 
    theo dõi câu chuyện thông qua giọng 
    kể sinh động, giúp bé dễ dàng nắm 
    bắt nội dung và ý nghĩa của câu 
    chuyện.

    Lời Khuyên Cho Bố Mẹ
    -Thời Gian Chơi: Giới hạn thời
    gian chơi để bảo vệ mắt và sức
    khỏe của bé.
    -Khuyến Khích Sáng Tạo: Khuyến 
    khích bé tự do chọn màu sắc và tô 
    màu theo ý thích của mình.
    -Thảo Luận Câu Chuyện: Sau khi 
    hoàn thành mỗi câu chuyện, bố mẹ 
    có thể thảo luận cùng bé về 
    nội dung và ý nghĩa của câu chuyện,
    giúp bé phát triển tư duy và kỹ
    năng ngôn ngữ.

    Chúc bố mẹ và các bé có những 
    giờ phút vui vẻ và bổ ích cùng 
    PaintPal!!
''')

    def show_contact(self, instance):
        self.show_popup('Contact Us', '''
    Liên hệ với chúng tôi qua email: 
    saydoocorp@gmail.com
                        ''')



class LevelSelectScreen(Screen):
    def __init__(self, **kwargs):
        super(LevelSelectScreen, self).__init__(**kwargs)
        self.music = None
        self.button_click_sound = SoundLoader.load('button_click.mp3')

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        level1_layout = BoxLayout(orientation='vertical', spacing=10)
        level1_thumbnail = Image(source='level1_thumbnail.png', size_hint=(1, None), height=200, allow_stretch=True, keep_ratio=False)
        level1_button = Button(text='Sọ Dừa', size_hint=(None, None), size=(200, 50))
        level1_button.bind(on_release=lambda x: self.go_to_level(1, imagelvl1[0], level_music_1[0]))
        level1_button.bind(on_press=self.play_button_sound)
        level1_layout.add_widget(level1_thumbnail)
        level1_layout.add_widget(level1_button)
        
        level2_layout = BoxLayout(orientation='vertical', spacing=10)
        level2_thumbnail = Image(source='level2_thumbnail.png', size_hint=(1, None), height=200, allow_stretch=True, keep_ratio=False)
        level2_button = Button(text='Tấm Cám', size_hint=(None, None), size=(200, 50))
        level2_button.bind(on_release=lambda x: self.go_to_level(2, imagelvl2[0], level_music_2[0]))
        level2_button.bind(on_press=self.play_button_sound)
        level2_layout.add_widget(level2_thumbnail)
        level2_layout.add_widget(level2_button)

        back_button = Button(text='Back', size_hint=(0.15, 0.2), pos_hint={'x': 0, 'top': 1})
        back_button.bind(on_press=self.on_back)

        layout.add_widget(back_button)      
        layout.add_widget(level1_layout)
        layout.add_widget(level2_layout)

        
        self.add_widget(layout)

    #def on_enter(self, *args):
        #self.play_music('level_music.mp3')

    def on_leave(self, *args):
        self.stop_music()

    def play_music(self, filename):
        self.music = SoundLoader.load(filename)
        if self.music:
            self.music.loop = True
            self.music.play()

    def stop_music(self):
        if self.music:
            self.music.stop()
            self.music.unload()

    def play_button_sound(self, instance):
        if self.button_click_sound:
            self.button_click_sound.play()

    def go_to_level(self, level_number, level_image, level_music):
        game_screen = self.manager.get_screen('game')
        game_screen.level = level_number
        game_screen.level_image = level_image
        game_screen.level_music = level_music
        #game_screen.level_text = level_text
        self.manager.current = 'game'

    def on_back(self, instance):
        self.manager.current = 'menu'

class ColoringWidget(Widget):
    def __init__(self, source, **kwargs):
        super(ColoringWidget, self).__init__(**kwargs)
        self.canvas_image = None
        self.current_color = [0, 0, 0, 1]
        self.eraser_mode = False
        self.history = []

        with self.canvas:
            self.canvas_image = Image(source=source, size_hint=(None, None), size=(600, 800), pos_hint={'x': 0, 'y': 0})
            self.canvas_image.bind(on_touch_down=self.on_touch_down)
    
    def on_touch_down(self, touch):
        if self.canvas_image.collide_point(*touch.pos):
            self.history.append(self.canvas_image.texture.pixels)
            local_x = touch.x - self.canvas_image.pos[0]
            local_y = touch.y - self.canvas_image.pos[1]
            self.flood_fill((local_x, local_y))
    
    def flood_fill(self, pos):
        x, y = int(pos[0]), int(pos[1])
        img_data = self.canvas_image.texture.pixels
        img_array = np.frombuffer(img_data, dtype=np.uint8).reshape(self.canvas_image.texture.height, self.canvas_image.texture.width, 4).copy()

        # Flip the image array vertically
        img_array = np.flipud(img_array)

        target_color = img_array[y, x].tolist()
        
        replacement_color = [int(c * 255) for c in (self.current_color if not self.eraser_mode else [1, 1, 1, 1])]

        if target_color == replacement_color:
            return

        # Convert RGBA to RGB
        rgb_img_array = img_array[:, :, :3]

        # Convert to a format compatible with OpenCV
        rgb_img_array = np.ascontiguousarray(rgb_img_array)

        # Create mask
        mask = np.zeros((rgb_img_array.shape[0] + 2, rgb_img_array.shape[1] + 2), np.uint8)
        
        # Perform flood fill on the RGB image
        cv2.floodFill(rgb_img_array, mask, (x, y), replacement_color[:3])

        # Combine the modified RGB image with the original alpha channel
        img_array[:, :, :3] = rgb_img_array

        # Flip the image array back vertically
        img_array = np.flipud(img_array)

        # Update texture
        new_texture = Texture.create(size=(img_array.shape[1], img_array.shape[0]), colorfmt='rgba')
        new_texture.blit_buffer(img_array.tobytes(), colorfmt='rgba', bufferfmt='ubyte')
        new_texture.flip_vertical()
        self.canvas_image.texture = new_texture

    def apply_zoom(self, scale, translation):
        # Get the current texture
        texture = self.canvas_image.texture
        # Get the current size of the texture
        width, height = texture.size
        # Get the current position of the texture
        x, y = self.canvas_image.pos
        # Calculate the new size of the texture
        new_width = width * scale
        new_height = height * scale
        # Calculate the new position of the texture
        new_x = x - (new_width - width) * (translation[0] / width)
        new_y = y - (new_height - height) * (translation[1] / height)
        # Update the size and position of the texture
        self.canvas_image.size = (new_width, new_height)
        self.canvas_image.pos = (new_x, new_y)

    def zoom_image_hand_gesture(self, touch):
        if len(touch) == 2:
            # Get the two touches
            touch1, touch2 = touch
            # Get the current distance between the touches
            current_distance = touch1.distance(touch2)
            # Get the previous distance between the touches
            previous_distance = touch1.prev_distance
            # Calculate the scale factor
            scale = current_distance / previous_distance
            # Get the current center of the touches
            center = touch1.pos
            # Get the previous center of the touches
            previous_center = touch1.prev_pos
            # Calculate the translation vector
            translation = np.array(center) - np.array(previous_center)
            # Apply the scale factor and translation to the image
            self.apply_zoom(scale, translation)

    def undo(self):
        if self.history:
            last_state = self.history.pop()
            new_texture = Texture.create(size=(self.canvas_image.texture.width, self.canvas_image.texture.height), colorfmt='rgba')
            new_texture.blit_buffer(last_state, colorfmt='rgba', bufferfmt='ubyte')
            new_texture.flip_vertical()
            self.canvas_image.texture = new_texture

class CompletePopup(Popup):
    def __init__(self, **kwargs):
        super(CompletePopup, self).__init__(**kwargs)
        self.title = 'Xin chúc mừng!'
        self.content = Label(text='Bạn đã hoàn thành màn rồi, giỏi quá!')
        self.size_hint = (0.5, 0.5)
        self.auto_dismiss = True

class ColoringApp(Screen):
    def __init__(self, level_image=None, **kwargs):
        super(ColoringApp, self).__init__(**kwargs)
        self.level_image = level_image
        self.coloring_widget = None

    def on_enter(self, *args):
        global sound
        self.clear_widgets()
        layout = FloatLayout()
        Window.size = (600, 800)
        # Play music
        sound = SoundLoader.load(self.level_music)
        if sound:
            sound.play()
        
        # Main coloring area
        self.coloring_widget = ColoringWidget(source=self.level_image, size_hint=(None, None), size=(600, 800), pos_hint={'x': 0, 'y': 0})
        layout.add_widget(self.coloring_widget)

        # Back and Complete buttons
        back_button = Button(text='Quay lại', size_hint=(0.15, 0.1), pos_hint={'x': 0, 'top': 1})
        back_button.bind(on_press=self.on_back)
        complete_button = Button(text='Xong!', size_hint=(0.15, 0.1), pos_hint={'right': 1, 'top': 1})
        complete_button.bind(on_press=self.complete)
        layout.add_widget(back_button)
        layout.add_widget(complete_button)

        # Play sound button
        self.play_music('game_music.mp3')
        play_button = Button(text='Kể chuyện', size_hint=(0.15, 0.1), pos_hint={'center_x': 0.5, 'top': 1})
        play_button.bind(on_press=self.play_sound)
        layout.add_widget(play_button)

        # Color palette
        self.current_color_button = None
        self.eraser_button = None
        palette_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), pos_hint={'x': 0, 'y': 0})
        scroll_view = ScrollView(size_hint=(0.8, 1))
        color_grid = GridLayout(cols=10, size_hint_y=None)
        color_grid.bind(minimum_height=color_grid.setter('height'))
        
        # Add color buttons in color order
        colors = [
            '000000', '808080', 'C0C0C0', '800000', 'FF0000', '800080', 'FF00FF', '008000', '00FF00', '808000',
            '808000', 'FFFF00', '008080', '00FFFF', '000080', '0000FF', 'A52A2A', 'FFA07A', 'FFD700', 'FF8C00',
            'FF4500', 'FF6347', 'FF69B4', 'FF1493', 'FF00FF', 'FF00FF', 'FF69B4', 'FF1493', 'FF4500', 'FF6347',
            'FF8C00', 'FFA07A', 'FFD700', 'FF8C00', 'FF4500', 'FF6347', 'FF69B4', 'FF1493', 'FF00FF', 'FF00FF',
            'FF69B4', 'FF1493', 'FF4500', 'FF6347', 'FF8C00', 'FFA07A', 'FFD700', 'FF8C00', 'FF4500', 'FF6347',
        ]
        
        for color in colors:
            btn = ToggleButton(background_color=get_color_from_hex(color), size_hint_y=None, height=50)
            btn.bind(on_press=self.on_color_select)
            color_grid.add_widget(btn)
        
        scroll_view.add_widget(color_grid)
        palette_layout.add_widget(scroll_view)
        
        # Undo and Eraser buttons
        undo_button = Button(text='Lùi lại', size_hint=(0.1, 1))
        self.eraser_button = ToggleButton(text='Tẩy', size_hint=(0.1, 1))
        undo_button.bind(on_press=self.on_undo)
        self.eraser_button.bind(on_press=self.on_eraser)
        palette_layout.add_widget(undo_button)
        palette_layout.add_widget(self.eraser_button)
        
        layout.add_widget(palette_layout)

        self.add_widget(layout)

    def on_color_select(self, instance):
        if self.current_color_button:
            self.current_color_button.state = 'normal'
        self.current_color_button = instance
        instance.state = 'down'
        self.coloring_widget.current_color = instance.background_color
        self.coloring_widget.eraser_mode = False
        if self.eraser_button:
            self.eraser_button.state = 'normal'

    def on_undo(self, instance):
        self.coloring_widget.undo()

    def on_eraser(self, instance):
        if self.current_color_button:
            self.current_color_button.state = 'normal'
        self.current_color_button = None
        self.coloring_widget.eraser_mode = True
        instance.state = 'down'

    def on_back(self, instance):
        # Stop the music
        if sound:
            sound.stop()
        # Go back to level select screen
        self.manager.current = 'levels'

    def play_sound(self, instance):
        sound = SoundLoader.load(self.level_music)
        if sound:
            sound.play()

    def play_music(self, filename, volume=0.5):
        self.music = SoundLoader.load(filename)
        if self.music:
            self.music.loop = True
            self.music.volume = volume
            self.music.play()

    def complete(self, instance):
        # Stop the music
        if sound:
            sound.stop()
            
        # Make small popup that says "Congratulations! You have completed the level!"
        complete_popup = CompletePopup()
        complete_popup.open()

        # Determine the appropriate lists based on the current level
        if self.level == 1:
            image_list = imagelvl1
            music_list = level_music_1
            # text_list = level_text_1  # Uncomment if using texts
        elif self.level == 2:
            image_list = imagelvl2
            music_list = level_music_2
            # text_list = level_text_2  # Uncomment if using texts
        else:
            self.manager.current = 'levels'
            return
             
        next_index = image_list.index(self.level_image) + 1
        if next_index < len(image_list):
            self.level_image = image_list[next_index]
            self.level_music = music_list[next_index]
            # self.level_text = text_list[next_index]  # Uncomment if using texts
            self.on_enter()  # Reload the screen with the new image and music
        else:
            self.manager.current = 'levels'  # If no more images, go back to the level select screen

class PaintPalApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(LevelSelectScreen(name='levels'))
        sm.add_widget(ColoringApp(name='game'))
        return sm

if __name__ == '__main__':
    PaintPalApp().run()
