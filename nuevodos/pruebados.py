import pygame
from tkinter import Tk, Label, Button, filedialog, Listbox, messagebox, Scale
from tkinter.ttk import Progressbar

class ReproductorMusica:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Reproductor de música")

        self.etiqueta = Label(ventana, text="Reproductor de música")
        self.etiqueta.pack()

        self.btn_seleccionar = Button(ventana, text="Seleccionar canciones", command=self.seleccionar_canciones)
        self.btn_seleccionar.pack()

        self.lista_reproduccion = Listbox(ventana, selectmode="SINGLE")
        self.lista_reproduccion.pack()

        self.btn_reproducir = Button(ventana, text="Reproducir", command=self.reproducir)
        self.btn_reproducir.pack()

        self.btn_pausar = Button(ventana, text="Pausar", command=self.pausar)
        self.btn_pausar.pack()

        self.btn_detener = Button(ventana, text="Detener", command=self.detener)
        self.btn_detener.pack()

        self.barra_progreso = Progressbar(ventana, orient="horizontal", length=200, mode="determinate")
        self.barra_progreso.pack()

        self.volumen = Scale(ventana, from_=0, to=1, resolution=0.1, orient="horizontal", label="Volumen", command=self.cambiar_volumen)
        self.volumen.set(0.5)
        self.volumen.pack()

        self.lista_canciones = []
        self.cancion_actual = None

    def seleccionar_canciones(self):
        canciones = filedialog.askopenfilenames(initialdir="/", title="Seleccionar canciones", filetypes=(("Archivos de audio", "*.mp3"), ("Todos los archivos", "*.*")))
        for cancion in canciones:
            self.lista_canciones.append(cancion)
            self.lista_reproduccion.insert("end", cancion)

    def reproducir(self):
        if not self.cancion_actual:
            seleccion = self.lista_reproduccion.curselection()
            if seleccion:
                indice = seleccion[0]
                self.cancion_actual = self.lista_canciones[indice]
                pygame.mixer.init()
                pygame.mixer.music.load(self.cancion_actual)
                pygame.mixer.music.play()
                self.barra_progreso["maximum"] = pygame.mixer.music.get_length()
                self.actualizar_progreso()
        else:
            pygame.mixer.music.unpause()

    def pausar(self):
        if self.cancion_actual:
            pygame.mixer.music.pause()

    def detener(self):
        if self.cancion_actual:
            pygame.mixer.music.stop()
            self.cancion_actual = None
            self.barra_progreso["value"] = 0

    def actualizar_progreso(self):
        if pygame.mixer.music.get_busy():
            self.barra_progreso["value"] = pygame.mixer.music.get_pos()
            self.ventana.after(1000, self.actualizar_progreso)

    def cambiar_volumen(self, valor):
        pygame.mixer.music.set_volume(float(valor))

if __name__ == "__main__":
    ventana_principal = Tk()
    reproductor = ReproductorMusica(ventana_principal)
    ventana_principal.mainloop()
