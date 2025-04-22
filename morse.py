import tkinter as tk
from tkinter import ttk, scrolledtext
import pygame
import time
import math  # Aggiunto import del modulo math

class MorseConverter:
    def __init__(self):
        # Dizionario per la conversione in codice Morse
        self.morse_dict = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 
            'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 
            'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 
            'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 
            'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 
            'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--', 
            '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
            '9': '----.', '.': '.-.-.-', ',': '--..--', '?': '..--..', 
            '!': '-.-.--', ' ': '/'
        }
        
        # Inizializzo pygame per i suoni
        pygame.mixer.init()

    def convert_to_morse(self, text):
        """Converte il testo in codice Morse"""
        text = text.upper()
        morse_code = []
        
        for char in text:
            if char in self.morse_dict:
                morse_code.append(self.morse_dict[char])
            else:
                morse_code.append(char)  # Caratteri non tradotti rimangono uguali
                
        return ' '.join(morse_code)
    
    def play_morse_sound(self, morse_code):
        """Riproduce i suoni del codice Morse"""
        # Definizione delle durate
        dit_duration = 0.1  # durata di un punto
        dah_duration = dit_duration * 3  # durata di una linea
        symbol_space = dit_duration  # spazio tra simboli
        letter_space = dit_duration * 3  # spazio tra lettere
        word_space = dit_duration * 7  # spazio tra parole
        
        # Creazione dei suoni
        frequency = 800  # frequenza del suono in Hz
        
        for letter in morse_code.split():
            if letter == '/':  # Spazio tra parole
                time.sleep(word_space)
                continue
                
            for symbol in letter:
                if symbol == '.':
                    self.beep(frequency, dit_duration)
                elif symbol == '-':
                    self.beep(frequency, dah_duration)
                    
                time.sleep(symbol_space)
                
            time.sleep(letter_space - symbol_space)  # Spazio aggiuntivo tra lettere
    
    def beep(self, frequency, duration):
        """Riproduce un suono alla frequenza e durata specificate"""
        # Genera un suono sinusoidale
        sample_rate = 44100
        sound_array = pygame.sndarray.make_sound(
            pygame.mixer.Sound(
                buffer=bytes([int(127 * (0.5 * (1 + math.sin(2 * math.pi * frequency * t / sample_rate))))  # Corretto: math.sin invece di pygame.math.sin
                             for t in range(int(sample_rate * duration))])
            )
        )
        sound_array.play()
        pygame.time.wait(int(duration * 1000))  # Attende il completamento del suono

class MorseConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Convertitore Testo-Morse")
        self.root.geometry("1024x768")  # GUI grande
        self.root.resizable(True, True)
        
        # Configurazione stile
        self.configure_styles()
        
        # Istanzia il convertitore
        self.converter = MorseConverter()
        
        # Crea l'interfaccia
        self.create_interface()
        
    def configure_styles(self):
        """Configura gli stili per l'interfaccia"""
        self.root.configure(bg="#2C3E50")  # Sfondo scuro
        
        style = ttk.Style()
        style.theme_use('clam')
        
        # Stile pulsanti
        style.configure('TButton', 
                       font=('Arial', 12, 'bold'),
                       background="#3498DB", 
                       foreground="white",
                       padding=10)
        
        # Stile etichette
        style.configure('TLabel', 
                       font=('Arial', 12),
                       background="#2C3E50", 
                       foreground="white")
        
        # Stile titolo
        style.configure('Title.TLabel', 
                       font=('Arial', 16, 'bold'),
                       background="#2C3E50", 
                       foreground="#E74C3C",
                       padding=10)
        
    def create_interface(self):
        """Crea l'interfaccia utente"""
        # Frame principale
        main_frame = ttk.Frame(self.root, padding="20", style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.configure(style='TFrame')
        
        # Titolo
        title_label = ttk.Label(main_frame, text="Convertitore Testo-Morse", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Area input testo
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        input_label = ttk.Label(input_frame, text="Inserisci il testo da convertire:", style='TLabel')
        input_label.pack(anchor=tk.W)
        
        self.input_text = scrolledtext.ScrolledText(input_frame, height=5, width=50, font=('Arial', 12))
        self.input_text.pack(fill=tk.BOTH, expand=True, pady=5)
        self.input_text.configure(bg="#ECF0F1", fg="#2C3E50")
        
        # Area output Morse
        output_frame = ttk.Frame(main_frame)
        output_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        output_label = ttk.Label(output_frame, text="Codice Morse:", style='TLabel')
        output_label.pack(anchor=tk.W)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=5, width=50, font=('Courier', 12))
        self.output_text.pack(fill=tk.BOTH, expand=True, pady=5)
        self.output_text.configure(bg="#ECF0F1", fg="#2C3E50", state=tk.DISABLED)
        
        # Frame pulsanti
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        # Pulsanti colorati in stile calcolatrice
        self.convert_button = ttk.Button(button_frame, text="Converti", command=self.convert_text, style='TButton')
        self.convert_button.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        self.play_button = ttk.Button(button_frame, text="Riproduci Suono", command=self.play_sound, style='TButton')
        self.play_button.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        self.clear_button = ttk.Button(button_frame, text="Cancella", command=self.clear_fields, style='TButton')
        self.clear_button.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        # Personalizza i pulsanti con colori diversi
        self.convert_button.configure(style='Convert.TButton')
        self.play_button.configure(style='Play.TButton')
        self.clear_button.configure(style='Clear.TButton')
        
        style = ttk.Style()
        style.configure('Convert.TButton', background="#27AE60", foreground="white")
        style.configure('Play.TButton', background="#3498DB", foreground="white")
        style.configure('Clear.TButton', background="#E74C3C", foreground="white")
        
        # Footer
        footer_label = ttk.Label(main_frame, text="© 2025 Test Convertitore Morse 2025", style='TLabel')
        footer_label.pack(pady=(20, 0))
    
    def convert_text(self):
        """Converte il testo inserito in codice Morse"""
        input_text = self.input_text.get("1.0", tk.END).strip()
        
        if input_text:
            morse_code = self.converter.convert_to_morse(input_text)
            
            # Aggiorna l'area di output
            self.output_text.configure(state=tk.NORMAL)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", morse_code)
            self.output_text.configure(state=tk.DISABLED)
        
    def play_sound(self):
        """Riproduce il suono del codice Morse visualizzato"""
        morse_code = self.output_text.get("1.0", tk.END).strip()
        
        if morse_code:
            self.convert_button.configure(state=tk.DISABLED)
            self.play_button.configure(state=tk.DISABLED)
            self.clear_button.configure(state=tk.DISABLED)
            
            # Aggiorna la GUI durante la riproduzione
            self.root.update()
            
            # Riproduci il suono
            self.converter.play_morse_sound(morse_code)
            
            # Riattiva i pulsanti
            self.convert_button.configure(state=tk.NORMAL)
            self.play_button.configure(state=tk.NORMAL)
            self.clear_button.configure(state=tk.NORMAL)
    
    def clear_fields(self):
        """Cancella i campi di input e output"""
        self.input_text.delete("1.0", tk.END)
        
        self.output_text.configure(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.configure(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = MorseConverterApp(root)
    root.mainloop()