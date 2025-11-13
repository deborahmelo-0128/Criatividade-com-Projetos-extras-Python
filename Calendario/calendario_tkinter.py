import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
import json

# Classe Evento
class Evento:
    def __init__(self, titulo, data_hora, descricao):
        self.titulo = titulo
        self.data_hora = data_hora
        self.descricao = descricao
        self.is_concluido = False

    def __str__(self):
        status = "✅" if self.is_concluido else "⏳"
        return f"{status} {self.titulo} - {self.data_hora.strftime('%d/%m/%Y %H:%M')}"

    def to_dict(self):
        return {
            "titulo": self.titulo,
            "data_hora": self.data_hora.strftime("%Y-%m-%d %H:%M:%S"),
            "descricao": self.descricao,
            "is_concluido": self.is_concluido
        }

    @staticmethod
    def from_dict(dados):
        evento = Evento(
            dados["titulo"],
            datetime.strptime(dados["data_hora"], "%Y-%m-%d %H:%M:%S"),
            dados["descricao"]
        )
        evento.is_concluido = dados["is_concluido"]
        return evento


# Classe Calendário
class Calendario:
    def __init__(self):
        self.eventos = []

    def adicionar_evento(self, evento):
        self.eventos.append(evento)

    def listar_eventos(self):
        return sorted(self.eventos, key=lambda e: e.data_hora)

    def salvar_json(self, nome_arquivo="eventos.json"):
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            json.dump([e.to_dict() for e in self.eventos], f, ensure_ascii=False, indent=4)

    def carregar_json(self, nome_arquivo="eventos.json"):
        try:
            with open(nome_arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
                self.eventos = [Evento.from_dict(d) for d in dados]
        except FileNotFoundError:
            pass


# Interface Tkinter
class AppCalendario:
    def __init__(self, root):
        self.calendario = Calendario()
        self.calendario.carregar_json()

        root.title("📅 Calendário de Eventos")
        root.geometry("500x400")

        self.lista = tk.Listbox(root, width=70, height=15)
        self.lista.pack(pady=10)

        tk.Button(root, text="➕ Adicionar Evento", command=self.adicionar_evento).pack(pady=3)
        tk.Button(root, text="✅ Concluir Evento", command=self.concluir_evento).pack(pady=3)
        tk.Button(root, text="💾 Salvar", command=self.salvar).pack(pady=3)
        tk.Button(root, text="🔄 Recarregar", command=self.recarregar).pack(pady=3)

        self.atualizar_lista()

    def atualizar_lista(self):
        self.lista.delete(0, tk.END)
        for evento in self.calendario.listar_eventos():
            self.lista.insert(tk.END, str(evento))

    def adicionar_evento(self):
        titulo = simpledialog.askstring("Novo Evento", "Título:")
        if titulo is None:
            return
        data = simpledialog.askstring("Novo Evento", "Data e hora (DD/MM/AAAA HH:MM):")
        if data is None:
            return
        descricao = simpledialog.askstring("Novo Evento", "Descrição:")
        if descricao is None:
            return
        try:
            data_hora = datetime.strptime(data, "%d/%m/%Y %H:%M")
            evento = Evento(titulo, data_hora, descricao)
            self.calendario.adicionar_evento(evento)
            self.atualizar_lista()
        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido!")

    def concluir_evento(self):
        selecionado = self.lista.curselection()
        if not selecionado:
            return
        idx = selecionado[0]
        evento = self.calendario.listar_eventos()[idx]
        evento.is_concluido = True
        self.atualizar_lista()

    def salvar(self):
        self.calendario.salvar_json()
        messagebox.showinfo("Salvo", "Eventos salvos com sucesso!")

    def recarregar(self):
        self.calendario.carregar_json()
        self.atualizar_lista()


if __name__ == "__main__":
    root = tk.Tk()
    app = AppCalendario(root)
    root.mainloop()
 