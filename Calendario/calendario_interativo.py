from datetime import datetime
import csv
import json

# ----------------------------
# CLASSE EVENTO
# ----------------------------
class Evento:
    total_eventos = 0

    def __init__(self, titulo, data_hora, descricao):
        self.titulo = titulo
        self.data_hora = data_hora
        self.descricao = descricao
        self.is_concluido = False
        Evento.total_eventos += 1

    def __str__(self):
        return (f"Evento: {self.titulo}, Data: {self.data_hora.strftime('%d/%m/%Y %H:%M')}, "
                f"Descrição: {self.descricao}, Concluído: {self.is_concluido}")

    # Comparações
    def __lt__(self, other): return self.data_hora < other.data_hora

    # Ações
    def concluir_evento(self):
        self.is_concluido = True
        print(f"✅ O evento '{self.titulo}' foi concluído com sucesso!")

    def reagendar_evento(self, nova_data_hora):
        antiga_data = self.data_hora
        self.data_hora = nova_data_hora
        print(f"📅 O evento '{self.titulo}' foi reagendado de {antiga_data} para {nova_data_hora}.")

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
        evento.is_concluido = dados.get("is_concluido", False)
        return evento


# ----------------------------
# CLASSE CALENDARIO
# ----------------------------
class Calendario:
    def __init__(self):
        self.eventos = []

    def adicionar_evento(self, evento):
        self.eventos.append(evento)
        print(f"✅ Evento '{evento.titulo}' adicionado com sucesso!")

    def remover_evento(self, titulo):
        for evento in self.eventos:
            if evento.titulo.lower() == titulo.lower():
                self.eventos.remove(evento)
                print(f"🗑️ Evento '{titulo}' removido com sucesso!")
                return
        print(f"⚠️ Evento '{titulo}' não encontrado.")

    def listar_eventos(self):
        if not self.eventos:
            print("📭 Nenhum evento cadastrado.")
            return
        print("\n📅 Lista de eventos (ordenados por data):")
        for evento in sorted(self.eventos):
            print(" -", evento)

    def buscar_evento(self, titulo):
        encontrados = [e for e in self.eventos if titulo.lower() in e.titulo.lower()]
        if encontrados:
            print(f"\n🔍 Eventos encontrados com '{titulo}':")
            for e in encontrados:
                print(" -", e)
        else:
            print(f"❌ Nenhum evento encontrado com o título '{titulo}'.")

    def salvar_json(self, nome_arquivo="eventos.json"):
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            json.dump([e.to_dict() for e in self.eventos], f, ensure_ascii=False, indent=4)
        print(f"💾 Eventos salvos em '{nome_arquivo}'")

    def carregar_json(self, nome_arquivo="eventos.json"):
        try:
            with open(nome_arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
                self.eventos = [Evento.from_dict(item) for item in dados]
            print(f"📂 Eventos carregados de '{nome_arquivo}'")
        except FileNotFoundError:
            print(f"⚠️ Arquivo '{nome_arquivo}' não encontrado.")

    def salvar_csv(self, nome_arquivo="eventos.csv"):
        with open(nome_arquivo, "w", newline="", encoding="utf-8") as f:
            campos = ["titulo", "data_hora", "descricao", "is_concluido"]
            escritor = csv.DictWriter(f, fieldnames=campos)
            escritor.writeheader()
            for evento in self.eventos:
                escritor.writerow(evento.to_dict())
        print(f"📁 Eventos salvos em '{nome_arquivo}'")

    def carregar_csv(self, nome_arquivo="eventos.csv"):
        try:
            with open(nome_arquivo, "r", encoding="utf-8") as f:
                leitor = csv.DictReader(f)
                self.eventos = [Evento.from_dict(linha) for linha in leitor]
            print(f"📂 Eventos carregados de '{nome_arquivo}'")
        except FileNotFoundError:
            print(f"⚠️ Arquivo '{nome_arquivo}' não encontrado.")


# ----------------------------
# INTERFACE INTERATIVA
# ----------------------------
def menu():
    calendario = Calendario()
    while True:
        print("\n=== MENU CALENDÁRIO ===")
        print("1. Adicionar evento")
        print("2. Listar eventos")
        print("3. Buscar evento")
        print("4. Concluir evento")
        print("5. Reagendar evento")
        print("6. Remover evento")
        print("7. Salvar eventos (JSON)")
        print("8. Carregar eventos (JSON)")
        print("9. Salvar eventos (CSV)")
        print("10. Carregar eventos (CSV)")
        print("0. Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            titulo = input("Título do evento: ")
            data_str = input("Data e hora (formato: DD/MM/AAAA HH:MM): ")
            descricao = input("Descrição: ")
            try:
                data_hora = datetime.strptime(data_str, "%d/%m/%Y %H:%M")
                evento = Evento(titulo, data_hora, descricao)
                calendario.adicionar_evento(evento)
            except ValueError:
                print("⚠️ Formato de data inválido.")

        elif opcao == "2":
            calendario.listar_eventos()

        elif opcao == "3":
            termo = input("Digite parte do título: ")
            calendario.buscar_evento(termo)

        elif opcao == "4":
            titulo = input("Título do evento a concluir: ")
            for e in calendario.eventos:
                if e.titulo.lower() == titulo.lower():
                    e.concluir_evento()
                    break
            else:
                print("⚠️ Evento não encontrado.")

        elif opcao == "5":
            titulo = input("Título do evento a reagendar: ")
            nova_data = input("Nova data e hora (DD/MM/AAAA HH:MM): ")
            for e in calendario.eventos:
                if e.titulo.lower() == titulo.lower():
                    try:
                        nova_data_hora = datetime.strptime(nova_data, "%d/%m/%Y %H:%M")
                        e.reagendar_evento(nova_data_hora)
                    except ValueError:
                        print("⚠️ Formato de data inválido.")
                    break
            else:
                print("⚠️ Evento não encontrado.")

        elif opcao == "6":
            titulo = input("Título do evento a remover: ")
            calendario.remover_evento(titulo)

        elif opcao == "7":
            calendario.salvar_json()

        elif opcao == "8":
            calendario.carregar_json()

        elif opcao == "9":
            calendario.salvar_csv()

        elif opcao == "10":
            calendario.carregar_csv()

        elif opcao == "0":
            print("👋 Encerrando o programa...")
            break

        else:
            print("⚠️ Opção inválida! Tente novamente.")


# Executa o menu se rodar o arquivo diretamente
if __name__ == "__main__":
    menu()
