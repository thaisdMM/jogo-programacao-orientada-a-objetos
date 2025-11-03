# Linguagem: Python
# Objetivo: inserir comentários que expliquem onde e como princípios de Programação Orientada a Objetos (OOP)
# e boas práticas foram aplicados.

import random
from time import sleep


# === GeradorDano ===
# Esta classe mostra uso de "composition" / injeção de dependência: em vez
# de usar random diretamente nas classes Personagem, o gerador é um objeto
# separado que fornece a funcionalidade de geração de números aleatórios.
# Isso melhora testabilidade (pode-se injetar um gerador determinístico).
class GeradorDano:

    def gerar_dano_base(self) -> int:
        return random.randint(2, 4)

    def gerar_dano_especial(self) -> int:
        return random.randint(5, 8)


# === Personagem (classe base) ===
# - Encapsulamento: atributos com underscore (_nome, _vida, _nivel) indicam
#   que são "protegidos" (convenção em Python).
# - Propriedades (@property) expõem leitura e escrita controlada (validação
#   centralizada no setter de vida).
# - Responsabilidade única: Personagem é responsável por seu próprio estado
#   (vida, receber dano, calcular ataque básico). Evita que outras classes
#   manipulem diretamente atributos internos.
class Personagem:
    def __init__(self, nome: str, vida: int, nivel: int, gerador_dano: GeradorDano):
        # Atributos protegidos: convenção que facilita herança e testes.
        self._nome = nome
        # Usa o setter de `vida` para validação inicial (boa prática).
        self.vida = vida
        self._nivel = nivel
        # Dependência injetada: o objeto de geração de dano.
        self.gerador_dano = gerador_dano

    # Expor nome via propriedade (mais idiomático do que get_nome())
    @property
    def nome(self):
        return self._nome

    # Propriedade vida com validação no setter: mantém consistência do estado
    @property
    def vida(self):
        return self._vida

    @vida.setter
    def vida(self, novo_valor_vida: int):
        # Validação simples: garante que vida é inteiro e não fica negativa.
        # Isso centraliza regras de negócio (SRP - Single Responsibility).
        if isinstance(novo_valor_vida, int):
            if novo_valor_vida < 0:
                # Normaliza em 0 para evitar estados inválidos.
                self._vida = 0
            else:
                self._vida = novo_valor_vida
        else:
            # Lançar erro claro ajuda a detectar uso incorreto na fase de testes.
            raise ValueError("O novo valor da vida deve ser inteiro.")

    @property
    def nivel(self):
        return self._nivel

    def exibir_detalhes(self):
        # Método de instância que combina propriedades para apresentação.
        # Polimorfismo: subclasses podem estender este método (veja Heroi e Inimigo).
        return f"Nome: {self.nome}\nVida: {self.vida}\nNivel: {self.nivel}"

    def receber_ataque(self, dano: int):
        # Operação semântica para aplicar dano. Mantém encapsulamento do estado.
        # Evita que outros objetos manipulem `_vida` diretamente.
        self.vida -= dano

    def atacar(self, alvo):
        # Cálculo de dano delegando ao gerador injetado: favorece testabilidade.
        dano = self.gerador_dano.gerar_dano_base() * self.nivel
        alvo.receber_ataque(dano)
        # Retornar o dano aplicado é bom para separar lógica e apresentação.
        return dano

    def format_ataque_response(self, alvo, dano: int):
        # Método que formata saída textual. Separar formatação da lógica é
        # uma boa prática (Single Responsibility e testabilidade).
        return f"\n{self.nome} atacou {alvo.nome} e causou {dano} de dano! 🔥"


# === Heroi (subclasse de Personagem) ===
# - Demonstra herança: Heroi especializa Personagem.
# - Polimorfismo: sobreposição de exibir_detalhes e adição de ataque_especial.
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

    # Polimorfismo: estende a apresentação do personagem.
    def exibir_detalhes(self):
        return f"{super().exibir_detalhes()}\nHabilidade: {self.habilidade}\n"

    def ataque_especial(self, alvo):
        # Usa o gerador de dano especial injetado; mantendo a lógica de cálculo
        # no objeto evita duplicação e facilita troca do gerador (injeção).
        dano = self.gerador_dano.gerar_dano_especial() * self.nivel
        alvo.receber_ataque(dano)
        return dano

    def format_ataque_especial_response(self, alvo: Personagem, dano: int):
        # Separação entre lógica e apresentação: formatar a mensagem é responsabilidade
        # do método de formatação, não do método que aplica o dano.
        return f"\n{self.nome} usou a habilidade especial  {self.habilidade} 👊 em {alvo.nome} e causou {dano} de dano! 🔥"


# === Inimigo (subclasse de Personagem) ===
# - Herança simples: reaproveita comportamento comum e adiciona `tipo`.
class Inimigo(Personagem):
    def __init__(
        self, nome: str, vida: int, nivel: int, gerador_dano: GeradorDano, tipo: str
    ):
        super().__init__(nome, vida, nivel, gerador_dano)
        self._tipo = tipo

    @property
    def tipo(self):
        return self._tipo

    # Polimorfismo: personaliza exibição para incluir o tipo do inimigo.
    def exibir_detalhes(self):
        return f"{super().exibir_detalhes()}\nTipo: {self.tipo}\n"


# === VisualizadorBatalha ===
# - Separação de responsabilidades (SRP): essa classe cuida exclusivamente de I/O
#   (print/inputs). Isso facilita trocar a interface (ex.: GUI) sem mudar o motor.
# - Observação: para testes automatizados, é comum fornecer uma implementação
#   "mock" que registra chamadas em vez de fazer print/input reais.
class VisualizadorBatalha:

    def titulo(self, mensagem: str):
        self.linha()
        print(mensagem)
        self.linha()

    def linha(self, tamanho=20):
        print("=-" * tamanho)

    def exibir_mensagem(self, mensagem: str):
        print(mensagem)

    def menu_das_jogadas(self):
        # Método de exibição do menu; não realiza leitura (boa prática: separar
        # exibição da leitura). A leitura deve ser feita pelo método `escolha_jogador`.
        print(
            """
        [1] Ataque Normal
        [2] Ataque com Habilidade Especial 
        [3] Sair do Jogo
"""
        )

    def abertura_do_jogo(self, heroi: Heroi, inimigo: Inimigo):
        # Mostra o estado atual dos personagens; não altera estado do jogo.
        print()
        self.titulo("JOGO DE COMBATE ENTRE INIMIGO E HERÓI")
        sleep(1)
        self.exibir_mensagem("\nHERÓI:")
        print(heroi.exibir_detalhes())
        self.linha()
        sleep(1)
        self.exibir_mensagem("\nINIMIGO:")
        print(inimigo.exibir_detalhes())
        self.linha()
        sleep(1)

    def final_do_jogo(self, heroi: Heroi, inimigo: Inimigo):
        # Apenas exibe o resultado final. Opcionalmente poderia retornar um booleano
        # para sinalizar ao motor que o jogo acabou; no seu design atual, isso não
        # é necessário porque o loop principal já encerra com base nas vidas.
        if heroi.vida > 0 and inimigo.vida <= 0:
            self.exibir_mensagem(
                f"\nParabéns, o seu herói, [{heroi.nome}], venceu a batalha!"
            )
        elif inimigo.vida > 0 and heroi.vida <= 0:
            self.exibir_mensagem(
                f"Você foi derrotado pelo inimigo [{inimigo.nome}]. Boa sorte na próxima vez!"
            )

    def escolha_jogador(self):
        # Método responsável por ler a escolha do jogador. Pode-se adicionar validação
        # aqui (loop até entrada válida) para simplificar o motor do jogo.
        escolha = input("Digite a sua escolha para jogar: ")
        return escolha

    def resultado_das_escolhas(
        self, escolha: str, heroi: Heroi, inimigo: Inimigo, retorno_da_escolha: dict
    ):
        # Exibe o resultado de uma jogada. Recebe os dados já calculados pelo motor
        # do jogo (boa separação de responsabilidades).
        sleep(1)

        if escolha == "1":
            sleep(1)
            self.exibir_mensagem("\n>>>> ATAQUE NORMAL!!! <<<<\n")
            sleep(1)
            print(
                heroi.format_ataque_response(
                    inimigo, retorno_da_escolha["dano_do_heroi"]
                )
            )
            sleep(1)
            print(
                inimigo.format_ataque_response(
                    heroi, retorno_da_escolha["dano_do_inimigo"]
                )
            )
        elif escolha == "2":
            sleep(1)
            self.exibir_mensagem("\n>>>> ATAQUE ESPECIAL DO HERÓI <<<<\n")
            sleep(1)
            print(
                heroi.format_ataque_especial_response(
                    inimigo, retorno_da_escolha["dano_do_heroi"]
                )
            )
            sleep(1)
            print(
                inimigo.format_ataque_response(
                    heroi, retorno_da_escolha["dano_do_inimigo"]
                )
            )
        elif escolha == "3":
            self.exibir_mensagem("\nEscolheu sair do jogo. Até a próxima!")
            return

        else:
            self.exibir_mensagem("\nEscolha inválida. Escolha entre as opções do Menu.")


# === Jogo (orquestrador) ===
# - Responsabilidade clara: o motor controla o fluxo do jogo, chama o visualizador
#   para exibir e lê a escolha por turno. Não contém lógica de exibição.
# - Isso é um exemplo de "Separation of Concerns" e facilita testes unitários.
class Jogo:
    """Classe orquestradora do jogo"""

    def __init__(
        self, heroi: Heroi, inimigo: Inimigo, visualizador: VisualizadorBatalha
    ):
        self.heroi = heroi
        self.inimigo = inimigo
        self.visualizador = visualizador

    def ataque_normal(self) -> dict:
        # Executa ações de ataque e retorna um dicionário com resultados. Retornar
        # dados em estruturas simples facilita o consumo pelo visualizador.
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
        # Método que mapeia a escolha do jogador para ações no motor do jogo.
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

        # Loop principal do jogo: repete enquanto ambos estiverem vivos.
        while self.heroi.vida > 0 and self.inimigo.vida > 0:

            # Sequência por turno: exibir estado, mostrar menu, ler escolha,
            # executar ação e exibir resultado.
            self.visualizador.abertura_do_jogo(self.heroi, self.inimigo)
            self.visualizador.menu_das_jogadas()
            escolha = self.visualizador.escolha_jogador()
            resultado = self.acoes_das_escolhas(escolha)
            self.visualizador.resultado_das_escolhas(
                escolha, self.heroi, self.inimigo, resultado
            )
            if resultado.get("sair_do_jogo"):
                break
            if resultado.get("escolha_invalida"):
                continue

        # Ao final do loop, exibe o resultado final (quem venceu).
        self.visualizador.final_do_jogo(self.heroi, self.inimigo)


# Fim do arquivo
# Comentários adicionados: indicação de padrões OOP usados (encapsulamento,
# injeção de dependência, herança, polimorfismo, separação de responsabilidades,
# validação centralizada via properties).


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
