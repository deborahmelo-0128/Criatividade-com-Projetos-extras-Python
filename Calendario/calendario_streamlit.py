import streamlit as st
from datetime import datetime
import json
import os

# Classe Evento
class Evento:
    def __init__(self, titulo, data_hora, descricao, is_concluido=False):
        self.titulo = titulo
        self.data_hora = data_hora
        self.descricao = descricao
        self.is_concluido = is_concluido

    def to_dict(self):
        return {
            "titulo": self.titulo,
            "data_hora": self.data_hora.strftime("%Y-%m-%d %H:%M:%S"),
            "descricao": self.descricao,
            "is_concluido": self.is_concluido
        }

    @staticmethod
    def from_dict(d):
        return Evento(
            d["titulo"],
            datetime.strptime(d["data_hora"], "%Y-%m-%d %H:%M:%S"),
            d["descricao"],
            d["is_concluido"]
        )


# Classe Calendário
class Calendario:
    def __init__(self):
        self.eventos = []

    def adicionar(self, evento):
        self.eventos.append(evento)

    def salvar(self, arquivo="eventos.json"):
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump([e.to_dict() for e in self.eventos], f, ensure_ascii=False, indent=4)

    def carregar(self, arquivo="eventos.json"):
        if os.path.exists(arquivo):
            with open(arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
                self.eventos = [Evento.from_dict(d) for d in dados]


# Interface Streamlit
st.set_page_config(page_title="📅 Calendário de Eventos", layout="centered")
st.title("📅 Calendário de Eventos")

cal = Calendario()
cal.carregar()

# Formulário de criação
with st.form("novo_evento"):
    st.subheader("➕ Adicionar novo evento")
    titulo = st.text_input("Título")
    data = st.date_input("Data")
    hora = st.time_input("Hora")
    descricao = st.text_area("Descrição")
    enviar = st.form_submit_button("Adicionar Evento")

    if enviar:
        data_hora = datetime.combine(data, hora)
        novo = Evento(titulo, data_hora, descricao)
        cal.adicionar(novo)
        cal.salvar()
        st.success("Evento adicionado com sucesso!")

st.divider()
st.subheader("📋 Lista de eventos")

if cal.eventos:
    eventos_ordenados = sorted(cal.eventos, key=lambda e: e.data_hora)
    for i, e in enumerate(eventos_ordenados):
        col1, col2, col3 = st.columns([4, 2, 2])
        status = "✅" if e.is_concluido else "⏳"
        col1.markdown(f"**{status} {e.titulo}** — {e.data_hora.strftime('%d/%m/%Y %H:%M')}")
        col1.caption(e.descricao)
        if col2.button("Concluir", key=f"c{i}"):
            e.is_concluido = True
            cal.salvar()
            st.rerun()
        if col3.button("Remover", key=f"r{i}"):
            cal.eventos.remove(e)
            cal.salvar()
            st.rerun()
else:
    st.info("Nenhum evento cadastrado ainda.")
