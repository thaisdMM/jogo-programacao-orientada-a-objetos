# versao refatorada

import random
from time import sleep


# Classes:
# Personagem: classe mãe
# Heroi: controlado pelo usuário
# Inimigo: adversario do usuario


class GeradorDano:

    def gerar_dano_base(self) -> int:
        return random.randint(2, 4)

    def gerar_dano_especial(self) -> int:
        return random.randint(5, 8)


class Personagem:
    def __init__(self, nome: str, vida: int, nivel: int, gerador_dano: GeradorDano):
        self._nome = nome
        self.vida = vida
        self._nivel = nivel
        self.gerador_dano = gerador_dano

    @property
    def nome(self):
        return self._nome

    @property
    def vida(self):
        return self._vida

    @vida.setter
    def vida(self, novo_valor_vida: int):
        if isinstance(novo_valor_vida, int):
            if novo_valor_vida < 0:
                self._vida = 0
            else:
                self._vida = novo_valor_vida
        else:
            raise ValueError("O novo valor da vida deve ser inteiro.")

    @property
    def nivel(self):
        return self._nivel

    def exibir_detalhes(self):
        return f"Nome: {self.nome}\nVida: {self.vida}\nNivel: {self.nivel}"

    def receber_ataque(self, dano: int):
        self.vida -= dano

    def atacar(self, alvo):
        # dano: baseado no nivel
        dano = self.gerador_dano.gerar_dano_base() * self.nivel
        alvo.receber_ataque(dano)
        return dano

    def format_ataque_response(self, alvo, dano: int):
        return f"\n{self.nome} atacou {alvo.nome} e causou {dano} de dano! 🔥"


class Heroi(Personagem):
    def __init__(
        self,
        nome: str,
        vida: int,
        nivel: int,
        gerador_dano: GeradorDano,
        habilidade: str,
    ):
        super().__init__(nome, vida, nivel, gerador_dano)
        self._habilidade = habilidade

    @property
    def habilidade(self):
        return self._habilidade

    # Polimorfismo
    def exibir_detalhes(self):
        return f"{super().exibir_detalhes()}\nHabilidade: {self.habilidade}\n"

    def ataque_especial(self, alvo):
        # dano aumentando
        dano = self.gerador_dano.gerar_dano_especial() * self.nivel
        alvo.receber_ataque(dano)
        return dano

    def format_ataque_especial_response(self, alvo: Personagem, dano: int):
        return f"\n{self.nome} usou a habilidade especial  {self.habilidade} 👊 em {alvo.nome} e causou {dano} de dano! 🔥"


class Inimigo(Personagem):
    def __init__(
        self, nome: str, vida: int, nivel: int, gerador_dano: GeradorDano, tipo: str
    ):
        super().__init__(nome, vida, nivel, gerador_dano)
        self._tipo = tipo

    @property
    def tipo(self):
        return self._tipo

    # Polimorfismo
    def exibir_detalhes(self):
        return f"{super().exibir_detalhes()}\nTipo: {self.tipo}\n"


class VisualizadorBatalha:
    def __init__(self):
        self.delay = False

    def titulo(self, mensagem: str):
        self.linha()
        print(mensagem)
        self.linha()
        self.maybe_delay_jogo()

    def linha(self, tamanho=20):
        print("=-" * tamanho)

    def exibir_mensagem(self, mensagem: str):
        print(mensagem)
        self.maybe_delay_jogo()

    def maybe_delay_jogo(self):
        if self.delay:
            sleep(1)

    def configurar_delay(self):
        escolhe_delay = (
            input(
                """
        \n>>> ATENÇÃO <<<:
                
Quer jogar com delay visual de 1 segundo por jogada? 
Digite [S] se sim ou outro comando se Não: """
            )
            .upper()
            .strip()
        )
        if escolhe_delay == "S":
            self.delay = True
        else:
            self.delay = False

    def menu_das_jogadas(self):
        self.maybe_delay_jogo()
        print(
            """
        [1] Ataque Normal
        [2] Ataque com Habilidade Especial 
        [3] Sair do Jogo
            """
        )

    def abertura_do_jogo(self, heroi: Heroi, inimigo: Inimigo):
        print()
        self.titulo("JOGO DE COMBATE ENTRE INIMIGO E HERÓI")
        self.exibir_mensagem("\nHERÓI:")
        self.exibir_mensagem(heroi.exibir_detalhes())
        self.linha()
        self.exibir_mensagem("\nINIMIGO:")
        self.exibir_mensagem(inimigo.exibir_detalhes())
        self.linha()

    def final_do_jogo(self, heroi: Heroi, inimigo: Inimigo):
        if heroi.vida > 0 and inimigo.vida <= 0:
            self.exibir_mensagem(
                f"\nParabéns, o seu herói, [{heroi.nome}], venceu a batalha!"
            )
        elif inimigo.vida > 0 and heroi.vida <= 0:
            self.exibir_mensagem(
                f"Você foi derrotado pelo inimigo [{inimigo.nome}]. Boa sorte na próxima vez!"
            )

    def escolha_jogador(self):
        while True:
            escolha = input("Digite a sua escolha para jogar: ")
            if escolha == "1" or escolha == "2" or escolha == "3":
                break
            else:
                self.exibir_mensagem(
                    "Escolha inválida. Escolha 1 ou 2 para atacar, ou 3 para sair do jogo."
                )
            self.linha()
        return escolha

    def resultado_das_escolhas(
        self, escolha: str, heroi: Heroi, inimigo: Inimigo, retorno_da_escolha: dict
    ):
        #

        if escolha == "1":

            self.exibir_mensagem("\n>>>> ATAQUE NORMAL!!! <<<<\n")

            self.exibir_mensagem(
                heroi.format_ataque_response(
                    inimigo, retorno_da_escolha["dano_do_heroi"]
                )
            )

            self.exibir_mensagem(
                inimigo.format_ataque_response(
                    heroi, retorno_da_escolha["dano_do_inimigo"]
                )
            )
        elif escolha == "2":

            self.exibir_mensagem("\n>>>> ATAQUE ESPECIAL DO HERÓI <<<<\n")

            self.exibir_mensagem(
                heroi.format_ataque_especial_response(
                    inimigo, retorno_da_escolha["dano_do_heroi"]
                )
            )

            self.exibir_mensagem(
                inimigo.format_ataque_response(
                    heroi, retorno_da_escolha["dano_do_inimigo"]
                )
            )
        elif escolha == "3":
            self.exibir_mensagem("\nEscolheu sair do jogo. Até a próxima!")
            return

        else:
            self.exibir_mensagem("\nEscolha inválida. Escolha entre as opções do Menu.")


class Jogo:
    """Classe orquestradora do jogo"""

    def __init__(
        self, heroi: Heroi, inimigo: Inimigo, visualizador: VisualizadorBatalha
    ):
        self.heroi = heroi
        self.inimigo = inimigo
        self.visualizador = visualizador

    def ataque_normal(self) -> dict:
        dano_do_heroi = self.heroi.atacar(self.inimigo)
        dano_do_inimigo = 0
        if self.inimigo.vida > 0:
            dano_do_inimigo = self.inimigo.atacar(self.heroi)
        return {"dano_do_heroi": dano_do_heroi, "dano_do_inimigo": dano_do_inimigo}

    def ataque_especial_heroi(self) -> dict:
        dano_do_heroi = self.heroi.ataque_especial(self.inimigo)
        dano_do_inimigo = 0
        if self.inimigo.vida > 0:
            dano_do_inimigo = self.inimigo.atacar(self.heroi)
        return {"dano_do_heroi": dano_do_heroi, "dano_do_inimigo": dano_do_inimigo}

    def acoes_das_escolhas(self, escolha: str) -> dict:
        if escolha == "1":
            dano = self.ataque_normal()
            return dano

        elif escolha == "2":
            dano = self.ataque_especial_heroi()
            return dano

        elif escolha == "3":
            return {"sair_do_jogo": True}
        else:
            return {"escolha_invalida": True}

    def iniciar_jogo(self):

        self.visualizador.configurar_delay()

        while self.heroi.vida > 0 and self.inimigo.vida > 0:

            self.visualizador.abertura_do_jogo(self.heroi, self.inimigo)
            self.visualizador.menu_das_jogadas()
            escolha = self.visualizador.escolha_jogador()
            resultado = self.acoes_das_escolhas(escolha)
            self.visualizador.resultado_das_escolhas(
                escolha, self.heroi, self.inimigo, resultado
            )
            if resultado.get("sair_do_jogo"):
                break

        self.visualizador.final_do_jogo(self.heroi, self.inimigo)


# testes
gerar_dano = GeradorDano()
# base = gerador_dano.gerar_dano_base()
lucifer = Inimigo(
    nome="Lúcifer", vida=80, nivel=5, gerador_dano=gerar_dano, tipo="Demônio"
)
asta = Heroi(
    nome="Asta",
    vida=100,
    nivel=5,
    gerador_dano=gerar_dano,
    habilidade="Super Força anti-magia",
)


visualizador1 = VisualizadorBatalha()
jogo1 = Jogo(asta, lucifer, visualizador1)
jogo1.iniciar_jogo()
