from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class SGAApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        title = Label(
            text='SGA - Système Gestion Agents\n\nAppuyez sur DÉMARRER',
            size_hint=(1, 0.4),
            font_size='20sp'
        )
        
        start_btn = Button(
            text='🚀 DÉMARRER',
            size_hint=(1, 0.2),
            background_color=(0.2, 0.7, 0.3, 1)
        )
        start_btn.bind(on_press=self.start_app)
        
        self.output = TextInput(
            text='Bienvenue au SGA...\n',
            size_hint=(1, 0.4),
            readonly=True
        )
        
        layout.add_widget(title)
        layout.add_widget(start_btn)
        layout.add_widget(self.output)
        
        return layout
    
    def start_app(self, instance):
        try:
            self.output.text += "Lancement du SGA...\n"
            from interface_console import main
            main()
            self.output.text += "Application terminée!\n"
        except Exception as e:
            self.output.text += f"Erreur: {e}\n"

if __name__ == '__main__':
    SGAApp().run()
