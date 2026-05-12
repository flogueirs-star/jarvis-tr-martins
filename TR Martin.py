import json
import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.core.window import Window
from datetime import datetime

Window.clearcolor = (0.02, 0.02, 0.05, 1)

ARQUIVO = "frota.json"

veiculos = []
gastos = []


def salvar_dados():
    dados = {
        "veiculos": veiculos,
        "gastos": gastos
    }

    with open(ARQUIVO, "w") as f:
        json.dump(dados, f)


def carregar_dados():
    global veiculos, gastos

    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r") as f:
            dados = json.load(f)
            veiculos = dados.get("veiculos", [])
            gastos = dados.get("gastos", [])


class TRMartinApp(App):

    def build(self):
        carregar_dados()

        tela = BoxLayout(
            orientation="vertical",
            padding=8,
            spacing=5
        )

        logo = Label(
            text="[b]TR MARTIN[/b]\nTRANSPORTE E CONTROLE DE FROTA",
            markup=True,
            font_size=28,
            color=(1, 0.8, 0.1, 1),
            size_hint_y=None,
            height=120
        )
        tela.add_widget(logo)

        self.resumo = Label(
            text="",
            font_size=13,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=65
        )
        tela.add_widget(self.resumo)

        self.seletor = Spinner(
            text="Selecione um veículo",
            values=[],
            size_hint_y=None,
            height=45,
            background_color=(0.2, 0.2, 0.2, 1)
        )
        tela.add_widget(self.seletor)

        self.placa = TextInput(
            hint_text="Placa do veículo",
            multiline=False,
            size_hint_y=None,
            height=38
        )
        tela.add_widget(self.placa)

        self.motorista = TextInput(
            hint_text="Motorista",
            multiline=False,
            size_hint_y=None,
            height=38
        )
        tela.add_widget(self.motorista)

        self.tipo = TextInput(
            hint_text="Tipo: cavalo, carreta, bitrem...",
            multiline=False,
            size_hint_y=None,
            height=38
        )
        tela.add_widget(self.tipo)

        btn_cadastrar = Button(
            text="Cadastrar veículo",
            size_hint_y=None,
            height=45,
            background_color=(0, 0.25, 0.55, 1)
        )
        btn_cadastrar.bind(on_press=self.cadastrar_veiculo)
        tela.add_widget(btn_cadastrar)

        titulo2 = Label(
            text="Manutenção / Gastos",
            font_size=15,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=28
        )
        tela.add_widget(titulo2)

        self.valor = TextInput(
            hint_text="Valor do gasto R$",
            multiline=False,
            input_filter="float",
            size_hint_y=None,
            height=38
        )
        tela.add_widget(self.valor)

        self.km = TextInput(
            hint_text="KM atual",
            multiline=False,
            input_filter="int",
            size_hint_y=None,
            height=38
        )
        tela.add_widget(self.km)

        self.obs = TextInput(
            hint_text="Observação",
            multiline=False,
            size_hint_y=None,
            height=38
        )
        tela.add_widget(self.obs)

        self.proxima_troca = TextInput(
            hint_text="KM próxima troca de óleo",
            multiline=False,
            input_filter="int",
            size_hint_y=None,
            height=38
        )
        tela.add_widget(self.proxima_troca)

        btn_salvar = Button(
            text="Salvar gasto do veículo",
            size_hint_y=None,
            height=45,
            background_color=(0, 0.45, 0.15, 1)
        )
        btn_salvar.bind(on_press=self.salvar_gasto)
        tela.add_widget(btn_salvar)

        btn_relatorio = Button(
            text="Ver relatório do veículo",
            size_hint_y=None,
            height=45,
            background_color=(0.35, 0.18, 0, 1)
        )
        btn_relatorio.bind(on_press=self.ver_relatorio)
        tela.add_widget(btn_relatorio)

        btn_excluir = Button(
            text="Excluir último gasto",
            size_hint_y=None,
            height=45,
            background_color=(0.55, 0, 0, 1)
        )
        btn_excluir.bind(on_press=self.excluir_ultimo)
        tela.add_widget(btn_excluir)

        btn_grafico = Button(
            text="Mostrar gráfico da frota",
            size_hint_y=None,
            height=45,
            background_color=(0.1, 0.05, 0.45, 1)
        )
        btn_grafico.bind(on_press=self.mostrar_grafico)
        tela.add_widget(btn_grafico)

        btn_reset = Button(
            text="RESETAR FROTA",
            size_hint_y=None,
            height=45,
            background_color=(0.7, 0, 0, 1)
        )
        btn_reset.bind(on_press=self.resetar_frota)
        tela.add_widget(btn_reset)

        self.relatorio = Label(
            text="",
            markup=True,
            font_size=12,
            color=(1, 1, 1, 1),
            halign="left",
            valign="top",
            size_hint_y=None
        )
        self.relatorio.bind(texture_size=self.ajustar_altura)

        scroll = ScrollView()
        scroll.add_widget(self.relatorio)
        tela.add_widget(scroll)

        self.seletor.values = [v["nome"] for v in veiculos]

        self.atualizar_resumo()

        return tela

    def ajustar_altura(self, instance, size):
        self.relatorio.height = self.relatorio.texture_size[1] + 30
        self.relatorio.text_size = (self.relatorio.width, None)

    def aviso(self, titulo, mensagem):
        popup = Popup(
            title=titulo,
            content=Label(text=mensagem),
            size_hint=(0.85, 0.45)
        )
        popup.open()

    def cadastrar_veiculo(self, instance):
        placa = self.placa.text.strip().upper()
        motorista = self.motorista.text.strip()
        tipo = self.tipo.text.strip()

        if placa == "" or motorista == "" or tipo == "":
            self.aviso("Erro", "Preencha placa, motorista e tipo.")
            return

        nome = f"{placa} - {motorista} - {tipo}"

        veiculos.append({
            "placa": placa,
            "motorista": motorista,
            "tipo": tipo,
            "nome": nome
        })

        salvar_dados()

        self.seletor.values = [v["nome"] for v in veiculos]
        self.seletor.text = nome

        self.placa.text = ""
        self.motorista.text = ""
        self.tipo.text = ""

        self.atualizar_resumo()
        self.aviso("Sucesso", "Veículo cadastrado!")

    def salvar_gasto(self, instance):
        if self.seletor.text == "Selecione um veículo":
            self.aviso("Erro", "Selecione um veículo.")
            return

        valor = self.valor.text.strip()
        km = self.km.text.strip()
        obs = self.obs.text.strip()
        proxima = self.proxima_troca.text.strip()

        if valor == "" or km == "" or obs == "":
            self.aviso("Erro", "Preencha todos os campos.")
            return

        try:
            valor_float = float(valor)
        except:
            self.aviso("Erro", "Valor inválido.")
            return

        try:
            km_atual = int(km)
            km_troca = int(proxima)

            if km_atual >= km_troca:
                alerta = "⚠ TROCA DE ÓLEO VENCIDA!"
            else:
                faltam = km_troca - km_atual
                alerta = f"✅ Faltam {faltam} KM para troca"
        except:
            alerta = "KM de troca não informado."

        gasto = {
            "veiculo": self.seletor.text,
            "valor": valor_float,
            "km": km,
            "obs": obs,
            "alerta": alerta,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M")
        }

        gastos.append(gasto)

        salvar_dados()

        self.valor.text = ""
        self.km.text = ""
        self.obs.text = ""
        self.proxima_troca.text = ""

        self.atualizar_resumo()
        self.ver_relatorio(None)

    def ver_relatorio(self, instance):
        escolhido = self.seletor.text

        if escolhido == "Selecione um veículo":
            self.aviso("Erro", "Selecione um veículo.")
            return

        texto = "[b]RELATÓRIO DO VEÍCULO[/b]\n\n"
        total = 0

        for g in gastos:
            if g["veiculo"] == escolhido:
                texto += f"🚛 {g['veiculo']}\n"
                texto += f"📅 {g['data']}\n"
                texto += f"🔧 {g['obs']} - R$ {g['valor']:.2f}\n"
                texto += f"📍 KM: {g['km']}\n"
                texto += f"{g['alerta']}\n"
                texto += "-----------------------------\n"
                total += g["valor"]

        texto += f"\n[b]TOTAL DO VEÍCULO: R$ {total:.2f}[/b]"

        self.relatorio.text = texto

    def excluir_ultimo(self, instance):
        escolhido = self.seletor.text

        for i in range(len(gastos) - 1, -1, -1):
            if gastos[i]["veiculo"] == escolhido:
                gastos.pop(i)

                salvar_dados()

                self.atualizar_resumo()
                self.ver_relatorio(None)

                self.aviso("Sucesso", "Último gasto excluído.")
                return

        self.aviso("Aviso", "Não existem gastos para excluir.")

    def mostrar_grafico(self, instance):
        texto = "[b]GRÁFICO DA FROTA[/b]\n\n"

        for v in veiculos:
            total = 0

            for g in gastos:
                if g["veiculo"] == v["nome"]:
                    total += g["valor"]

            barras = int(total / 50)

            if barras < 1 and total > 0:
                barras = 1

            texto += f"🚛 {v['placa']} | R$ {total:.2f}\n"
            texto += "█" * barras + "\n\n"

        self.relatorio.text = texto

    def resetar_frota(self, instance):
        veiculos.clear()
        gastos.clear()

        salvar_dados()

        self.seletor.values = []
        self.seletor.text = "Selecione um veículo"

        self.relatorio.text = ""

        self.atualizar_resumo()

        self.aviso("Sistema", "Toda a frota foi resetada.")

    def atualizar_resumo(self):
        total_frota = sum(g["valor"] for g in gastos)

        self.resumo.text = (
            f"🚛 Veículos: {len(veiculos)}\n"
            f"💰 Total frota: R$ {total_frota:.2f}\n"
            f"🔧 Manutenções: {len(gastos)}"
        )


TRMartinApp().run()