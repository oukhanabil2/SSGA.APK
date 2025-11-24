from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class SGAApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='SGA - Appuyez sur DÉMARRER'))
        btn = Button(text='🚀 DÉMARRER')
        btn.bind(on_press=lambda x: self.start_app())
        layout.add_widget(btn)
        return layout
    
    def start_app(self):
        try:
            from interface_console import main
            main()
        except Exception as e:
            print(f"Erreur: {e}")

SGAApp().run()
