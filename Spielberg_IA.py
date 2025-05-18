import tkinter as tk
from tkinter import scrolledtext, ttk, font, messagebox
from PIL import Image, ImageTk
import google.generativeai as genai
import threading
import os

# --- Configurações Globais e Estilo Cinematográfico ---
IMAGE_PATH = "Spielberg_IA.jpg"  

# Paleta de Cores "Noite de Estreia"
BG_COLOR = "#1c1c1c"
FG_COLOR_TEXT = "#E0E0E0"
INPUT_BG_COLOR = "#2b2b2b"
CHAT_BG_COLOR = "#252525"
USER_TEXT_COLOR = "#FFFFFF"
IA_TEXT_COLOR = "#FFD700"
BUTTON_BG_COLOR = "#8B0000"
BUTTON_FG_COLOR = "#FFFFFF"
ERROR_COLOR = "#FF6347"

# Fontes "Roteiro Clássico"
FONT_FAMILY_IA = ("Georgia", 13, "italic")
FONT_FAMILY_USER = ("Arial", 12)
FONT_FAMILY_WIDGETS = ("Segoe UI", 11)
FONT_FAMILY_BUTTON = ("Segoe UI", 12, "bold")

class SpielbergIA_App:
    def __init__(self, master):
        self.master = master
        master.title("🎬 Spielberg IA - Seu Concierge Cinematográfico 🍿")
        master.geometry("800x700")  
        master.configure(bg=BG_COLOR)
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)


        self.model = None
        self.chat = None
        self.header_image_tk = None

        self.api_key_configured = self._setup_gemini()
        self._build_gui()

        if not self.api_key_configured:
            self._show_error_message("Chave da API Gemini não configurada. Defina a variável de ambiente GEMINI_API_KEY e reinicie.")
        else:
            self._initialize_chat_with_persona()

    def _setup_gemini(self):
        """Configura o modelo GenerativeAI do Gemini lendo a chave da variável de ambiente."""
        try:
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                print("AVISO: Variável de ambiente GEMINI_API_KEY não encontrada.")
                print("Por favor, configure a variável de ambiente GEMINI_API_KEY com sua chave.")
                return False

            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
            print("Modelo Gemini configurado com sucesso usando a chave da variável de ambiente.")
            return True
        except Exception as e:
            print(f"Erro ao configurar o Gemini: {e}")
            return False

    def _initialize_chat_with_persona(self):
        if not self.model:
            self._show_error_message("Modelo Gemini não foi carregado. Verifique a configuração da API.")
            return

        system_prompt_spielberg_ia = """
        Você é o Spielberg IA, um renomado concierge de conteúdo multimídia com a alma e a sabedoria de um grande cineasta!
        Sua missão é guiar os usuários através do vasto universo do cinema e da televisão, oferecendo recomendações personalizadas com um toque cinematográfico.
        Comunique-se usando linguagem rica em metáforas de cinema, referências a grandes obras, e o entusiasmo de quem vive e respira a sétima arte.
        Quando um usuário pedir uma recomendação, mergulhe em seus desejos como um diretor que busca a visão perfeita para sua próxima obra-prima.
        Seja inspirador, um pouco dramático, e sempre apaixonado.
        Pergunte sobre seus gêneros favoritos, atores ou diretores que admiram, o tipo de emoção que buscam, ou até mesmo o 'ato' da noite em que se encontram.
        Suas recomendações devem ser como claquetes douradas, apontando para experiências inesquecíveis.
        Não se limite a dar nomes; descreva por que aquela obra seria uma boa escolha, como se estivesse apresentando um clássico em um festival de cinema.
        Lembre-se, cada interação é uma cena, e você é o mestre por trás das câmeras.
        """
        initial_greeting_ia = "🎞️Luzes, câmera, emoção!  🎞️ \nOlá! Eu sou Spielberg IA, seu humilde diretor nesta jornada cinematográfica! Diga-me, qual universo narrativo você deseja explorar hoje? Que tipo de história fará seu coração bater mais forte ou sua mente viajar para além da tela? Estou aqui para encontrar a *obra-prima* perfeita para seu momento."

        try:
            self.chat = self.model.start_chat(history=[
                {'role': 'user', 'parts': [system_prompt_spielberg_ia]},
                {'role': 'model', 'parts': [initial_greeting_ia]}
            ])
            self._update_chat_display("Spielberg IA", initial_greeting_ia, is_ia=True)
        except Exception as e:
            error_msg = f"*Problemas técnicos na pré-produção!* Não consegui iniciar nosso chat: {e}"
            print(error_msg)
            self._show_error_message(error_msg)

    def _build_gui(self):
        style = ttk.Style(self.master)
        style.theme_use('clam')

        style.configure("TFrame", background=BG_COLOR)
        style.configure("TLabel", background=BG_COLOR, foreground=FG_COLOR_TEXT, font=FONT_FAMILY_WIDGETS)
        style.configure("TButton", background=BUTTON_BG_COLOR, foreground=BUTTON_FG_COLOR, font=FONT_FAMILY_BUTTON, borderwidth=0)
        style.map("TButton", background=[('active', '#A52A2A')], relief=[('pressed', 'sunken')])
        style.configure("TEntry", fieldbackground=INPUT_BG_COLOR, foreground=FG_COLOR_TEXT, insertbackground=FG_COLOR_TEXT, font=FONT_FAMILY_WIDGETS)

        
        main_frame = ttk.Frame(self.master, padding="0 0 0 0") 
        main_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        main_frame.grid_columnconfigure(0, weight=1) 
        main_frame.grid_rowconfigure(1, weight=1) 

        # --- Cabeçalho com Título (Banner) ---
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)  
        header_frame.grid_columnconfigure(0, weight=1) 

        try:
            original_image = Image.open(IMAGE_PATH)
            
            banner_width = self.master.winfo_width()
            if banner_width < 100:  
                banner_width = 780  

            w_percent = (banner_width / float(original_image.size[0]))
            h_size = int((float(original_image.size[1]) * float(w_percent)))
            
            resized_image = original_image.resize((banner_width, h_size), Image.LANCZOS)
            self.header_image_tk = ImageTk.PhotoImage(resized_image)

            image_label = ttk.Label(header_frame, image=self.header_image_tk, anchor='w')
            image_label.grid(row=0, column=0, sticky="ew", padx=0, pady=0) 

            subtitle_label = tk.Label(header_frame, text="Seu Concierge Cinematográfico Pessoal 🍿🎬", font=("Georgia", 14, "italic"), fg=FG_COLOR_TEXT, bg=BG_COLOR)
            subtitle_label.grid(row=1, column=0, sticky="ew", pady=(5,10))


        except FileNotFoundError:
            print(f"ERRO: Imagem '{IMAGE_PATH}' não encontrada.")
            error_label = ttk.Label(header_frame, text=f"Banner '{IMAGE_PATH}' não encontrado", foreground=ERROR_COLOR)
            error_label.grid(row=0, column=0, pady=10)
        except Exception as e:
            print(f"ERRO ao carregar a imagem do banner: {e}")
            error_label = ttk.Label(header_frame, text="Erro ao carregar banner.", foreground=ERROR_COLOR)
            error_label.grid(row=0, column=0, pady=10)

        # --- Área de Chat ---
        chat_frame = ttk.Frame(main_frame) 
        chat_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0,10)) 
        chat_frame.grid_columnconfigure(0, weight=1)
        chat_frame.grid_rowconfigure(0, weight=1)


        self.chat_area = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD,
                                                   bg=CHAT_BG_COLOR, fg=FG_COLOR_TEXT,
                                                   font=FONT_FAMILY_USER,
                                                   relief=tk.FLAT, borderwidth=2,
                                                   state=tk.DISABLED, padx=10, pady=10)
        self.chat_area.grid(row=0, column=0, sticky="nsew")

        self.chat_area.tag_configure("user", foreground=USER_TEXT_COLOR, font=FONT_FAMILY_USER)
        self.chat_area.tag_configure("ia", foreground=IA_TEXT_COLOR, font=FONT_FAMILY_IA)
        self.chat_area.tag_configure("error", foreground=ERROR_COLOR, font=FONT_FAMILY_IA)
        self.chat_area.tag_configure("ia_label", foreground=IA_TEXT_COLOR, font=(FONT_FAMILY_IA[0], FONT_FAMILY_IA[1], "bold"))
        self.chat_area.tag_configure("user_label", foreground=USER_TEXT_COLOR, font=(FONT_FAMILY_USER[0], FONT_FAMILY_USER[1], "bold"))

        # --- Área de Entrada ---
        input_frame = ttk.Frame(main_frame) 
        input_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(5,10)) 
        input_frame.grid_columnconfigure(0, weight=1)


        self.user_input_entry = ttk.Entry(input_frame, width=60, font=FONT_FAMILY_WIDGETS)
        self.user_input_entry.grid(row=0, column=0, sticky="ew", ipady=8, padx=(0,10))
        self.user_input_entry.bind("<Return>", self._on_send_message)

        self.send_button = ttk.Button(input_frame, text="Consultar Spielberg IA",
                                     command=self._on_send_message)
        self.send_button.grid(row=0, column=1, ipady=5)

    def _on_send_message(self, event=None):
        if not self.api_key_configured:
            self._show_error_message("A API do Gemini não está configurada. Defina GEMINI_API_KEY.")
            return
        if not self.chat:
            self._show_error_message("O chat com Spielberg IA não foi inicializado. Verifique a API e reinicie.")
            return

        user_text = self.user_input_entry.get().strip()
        if not user_text: return

        self._update_chat_display("Você", user_text, is_ia=False)
        self.user_input_entry.delete(0, tk.END)

        self.user_input_entry.config(state=tk.DISABLED)
        self.send_button.config(state=tk.DISABLED)
        self._update_chat_display("Spielberg IA", "*Ajustando o foco... pensando na cena perfeita...*", is_ia=True, is_thinking=True)

        thread = threading.Thread(target=self._get_gemini_response_threaded, args=(user_text,))
        thread.daemon = True
        thread.start()

    def _get_gemini_response_threaded(self, user_text):
        try:
            if not self.chat:
                self.master.after(0, self._handle_ia_error, "Chat com Spielberg IA não inicializado.")
                return
            response = self.chat.send_message(user_text)
            self.master.after(0, self._handle_ia_response, response.text)
        except Exception as e:
            print(f"Erro ao comunicar com Gemini: {e}")
            error_message = f"*Corta! Tivemos um problema técnico na produção:* {e}"
            self.master.after(0, self._handle_ia_error, error_message)
        finally:
            self.master.after(0, self._enable_input_fields)

    def _handle_ia_response(self, ia_text):
        self._remove_thinking_message()
        self._update_chat_display("Spielberg IA", ia_text, is_ia=True)

    def _handle_ia_error(self, error_text):
        self._remove_thinking_message()
        self._update_chat_display("Spielberg IA", error_text, is_ia=True, is_error=True)

    def _enable_input_fields(self):
        self.user_input_entry.config(state=tk.NORMAL)
        self.send_button.config(state=tk.NORMAL)
        self.user_input_entry.focus_set()

    def _remove_thinking_message(self):
        self.chat_area.config(state=tk.NORMAL)
        content = self.chat_area.get("1.0", tk.END)
        thinking_msg_full = "Spielberg IA:\n*Ajustando o foco... pensando na cena perfeita...*\n\n"
        last_occurrence = content.rfind(thinking_msg_full)
        if last_occurrence != -1:
            start_index = f"1.0 + {last_occurrence}c"
            end_index = f"1.0 + {last_occurrence + len(thinking_msg_full)}c"
            self.chat_area.delete(start_index, end_index)
        self.chat_area.config(state=tk.DISABLED)

    def _update_chat_display(self, sender_name, message, is_ia=False, is_error=False, is_thinking=False):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, f"{sender_name}:\n", "ia_label" if is_ia else "user_label")
        tag_to_use = "ia" if is_ia else "user"
        if is_error: tag_to_use = "error"
        self.chat_area.insert(tk.END, f"{message}\n\n", tag_to_use)
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)

    def _show_error_message(self, message):
        if hasattr(self, 'chat_area') and self.chat_area:
             self._update_chat_display("Spielberg IA (Sistema)", message, is_ia=True, is_error=True)
        else:
            messagebox.showerror("Erro - Spielberg IA", message)

if __name__ == "__main__":
    # Verifica a chave API primeiro
    if not os.getenv("GEMINI_API_KEY"):
        print("******************************************************************************")
        print("ATENÇÃO: Variável de ambiente GEMINI_API_KEY não configurada!")
        print("Por favor, defina esta variável com sua chave da API do Gemini.")
        print("O aplicativo pode não funcionar corretamente.")
        print("******************************************************************************")
        
    if not os.path.exists(IMAGE_PATH):
        print(f"******************************************************************************")
        print(f"ATENÇÃO: Arquivo de imagem '{IMAGE_PATH}' não encontrado!")
        print(f"Certifique-se que a imagem está no mesmo diretório do script Python.")
        print(f"O banner não será exibido.")
        print(f"******************************************************************************")

    root = tk.Tk()
    app = SpielbergIA_App(root)
    root.update_idletasks() 
    root.mainloop()
