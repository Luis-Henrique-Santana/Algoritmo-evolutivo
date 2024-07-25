from random import random

import matplotlib.pyplot as plt

class Produto():
    def __init__(self, nome, espaco, valor):
        self.nome = nome
        self.espaco = espaco
        self.valor = valor
        
        
class Individuo(): # cada solução é um individuo
    def __init__(self, espacos, valores, limite_espacos, geracao=0):
        self.espacos = espacos
        self.valores = valores
        self.limite_espacos = limite_espacos
        self.nota_avaliacao = 0 # valor total transportado pela solucao
        self.espaco_usado = 0 #quanto de espaço essa solução esta ussando
        self.geracao = geracao
        self.cromossomo = [] #é conjunto solução, vai ser randomizado adianta para a primeira solucao
        
        for i in range(len(espacos)):
            if random() < 0.5:
                self.cromossomo.append("0")
            else:
                self.cromossomo.append("1")
                
    def avaliacao(self): #funcao de avaliação avalia ao individuo
        nota = 0
        soma_espacos = 0
        for i in range(len(self.cromossomo)): #percorrer todo o vetor cromossomo
           if self.cromossomo[i] == '1':#verifica se vai levar este produto
               nota += self.valores[i] # acrecenta o valor monetario do produto na variavel nota 
               soma_espacos += self.espacos[i]# acrecenta o espaco do produto na variavel soma_espacos
        if soma_espacos > self.limite_espacos: #verifica se o total de espacos e maior que o limite definido
            nota = 1 # seta o valor monetario em um valor mto baixa para rebaixar sua nota
        self.nota_avaliacao = nota
        self.espaco_usado = soma_espacos   
       
    def crossover(self, outro_individuo):
        corte = round(random()  * len(self.cromossomo)) #ponto de corte randomico
        
        filho1 = outro_individuo.cromossomo[0:corte] + self.cromossomo[corte::]
        filho2 = self.cromossomo[0:corte] + outro_individuo.cromossomo[corte::]
        #Gera os filhos acima. pega do individuo2 de zero ao corte e o individuo1 do corte ao fim.
        #inverte para o filho 2
        filhos = [Individuo(self.espacos, self.valores, self.limite_espacos, self.geracao + 1),
                  Individuo(self.espacos, self.valores, self.limite_espacos, self.geracao + 1)]
        #acima, criasse o vetor filhos com os 2 filhos ja na classe individuo
        filhos[0].cromossomo = filho1
        filhos[1].cromossomo = filho2
        #acima, Seta o cromossomo criado atravez do crossover dentro dos objetos
        
        return filhos #retorna o vetor com os objetos individuos filhos gerados

    def mutacao(self, taxa_mutacao): #muta o cromossomo. 
        #print("Antes %s " % self.cromossomo)
        for i in range(len(self.cromossomo)):#gira todo o cromossomo
            if random() < taxa_mutacao:# verifica se o random for menor que a taxa. 
                if self.cromossomo[i] == '1':#inverte o cromossomo que caiu na mutacao
                    self.cromossomo[i] = '0'
                else:
                    self.cromossomo[i] = '1'
        #print("Depois %s " % self.cromossomo)
        return self

class AlgoritmoGenetico():
    def __init__(self, tamanho_populacao):
        self.tamanho_populacao = tamanho_populacao
        self.populacao = [] # serão armazenados os muitos individuos em lista
        self.geracao = 0
        self.melhor_solucao = 0
        self.lista_solucoes = [] #melhor valor da geração
        
    def inicializa_populacao(self, espacos, valores, limite_espacos): #cria nossa primeira população
        for i in range(self.tamanho_populacao):#gira a quantidde de que queremos na população
            self.populacao.append(Individuo(espacos, valores, limite_espacos)) #cria os inidividuos
        self.melhor_solucao = self.populacao[0] #temporariamente sera o primeiro individuo 
        
    def ordena_populacao(self): #ordena o vetor da população.
        self.populacao = sorted(self.populacao,
                                key = lambda populacao: populacao.nota_avaliacao,
                                reverse = True)
            #pega o vetor população, adiciona a chave que vai ser usada para ordenar, e idica que e do menor pro maior
        
    def melhor_individuo(self, individuo):# acha o mlhor individuo da populaççao
        if individuo.nota_avaliacao > self.melhor_solucao.nota_avaliacao: 
            #acima. Verifica se o individuo passado é melhor que o memorizado na classe, se for substitui
            self.melhor_solucao = individuo

    def soma_avaliacoes(self): # soma todas as notas da população
        soma = 0
        for individuo in self.populacao:
           soma += individuo.nota_avaliacao
        return soma

    def seleciona_pai(self, soma_avaliacao):#seleciona os pais com a roleta viciada
        pai = -1 # inicia a variavel pai em -1 para n ser nenhum indice ja utilizado
        valor_sorteado = random() * soma_avaliacao # Sorteia um numero com base na soma da avaliação da população
        soma = 0
        i = 0
        while i < len(self.populacao) and soma < valor_sorteado:
            #acima. Rola a roleta onde o 1 parametro é a contagem e o segundo parametro e a saida pela soma dos resultados
            soma += self.populacao[i].nota_avaliacao
            pai += 1 #verifica em que pai vai parar a roleta
            i += 1 #controla as voltas
        return pai #retorna o indice do individuo selecionado para reproduzir
    
    def visualiza_geracao(self):
        melhor = self.populacao[0]
        print("G:%s -> Valor: %s Espaço: %s Cromossomo: %s" % (self.populacao[0].geracao,
                                                               melhor.nota_avaliacao,
                                                               melhor.espaco_usado,
                                                               melhor.cromossomo))
    
    def resolver(self, taxa_mutacao, numero_geracoes, espacos, valores, limite_espacos):
        #executa todo o codigo ja estudado no artigo anterior
        self.inicializa_populacao(espacos, valores, limite_espacos)
        
        for individuo in self.populacao: #crcia a população inicial
            individuo.avaliacao()
        
        self.ordena_populacao() #ordena a população
        self.melhor_solucao = self.populacao[0]
        self.lista_solucoes.append(self.melhor_solucao.nota_avaliacao) #adiciona o a melhor solução da geração no controle do grafico primeira solucao
        
        self.visualiza_geracao() #mostra a população
        
        for geracao in range(numero_geracoes):#inicia o loop de gerações
            soma_avaliacao = self.soma_avaliacoes() #pega a soma da nota da população
            nova_populacao = []
            
            for individuos_gerados in range(0, self.tamanho_populacao, 2): #cria os filhos da populaçao
                pai1 = self.seleciona_pai(soma_avaliacao)
                pai2 = self.seleciona_pai(soma_avaliacao)#pais localizados
                
                filhos = self.populacao[pai1].crossover(self.populacao[pai2]) #cruza e gera os filhos
                
                nova_populacao.append(filhos[0].mutacao(taxa_mutacao)) 
                nova_populacao.append(filhos[1].mutacao(taxa_mutacao)) # aplica a mutação no cromossomo
            
            self.populacao = list(nova_populacao) #substitui a população anterior pela nova população
            
            for individuo in self.populacao: #faz a avaliação da nova população
                individuo.avaliacao()
            
            self.ordena_populacao() #ordena a nova população
            
            self.visualiza_geracao() #mostra a nomva população
            
            melhor = self.populacao[0] #pega o melhor desta população
            self.lista_solucoes.append(melhor.nota_avaliacao)#adiciona o a melhor solução da geração no controle do grafico
            self.melhor_individuo(melhor) #envia para o meotodo melhor_individuo o novo melhor
        
        print("\nMelhor solução -> G: %s Valor: %s Espaço: %s Cromossomo: %s" %
              (self.melhor_solucao.geracao,
               self.melhor_solucao.nota_avaliacao,
               self.melhor_solucao.espaco_usado,
               self.melhor_solucao.cromossomo))
        
        return self.melhor_solucao.cromossomo
       
        

    
if __name__ == '__main__':
    #p1 = Produto("Iphone 6", 0.0000899, 2199.12)
    lista_produtos = []
    lista_produtos.append(Produto("Geladeira Dako", 0.751, 999.90))
    lista_produtos.append(Produto("Iphone 6", 0.0000899, 2911.12))
    lista_produtos.append(Produto("TV 55' ", 0.400, 4346.99))
    lista_produtos.append(Produto("TV 50' ", 0.290, 3999.90))
    lista_produtos.append(Produto("TV 42' ", 0.200, 2999.00))
    lista_produtos.append(Produto("Notebook Dell", 0.00350, 2499.90))
    lista_produtos.append(Produto("Ventilador Panasonic", 0.496, 199.90))
    lista_produtos.append(Produto("Microondas Electrolux", 0.0424, 308.66))
    lista_produtos.append(Produto("Microondas LG", 0.0544, 429.90))
    lista_produtos.append(Produto("Microondas Panasonic", 0.0319, 299.29))
    lista_produtos.append(Produto("Geladeira Brastemp", 0.635, 849.00))
    lista_produtos.append(Produto("Geladeira Consul", 0.870, 1199.89))
    lista_produtos.append(Produto("Notebook Lenovo", 0.498, 1999.90))
    lista_produtos.append(Produto("Notebook Asus", 0.527, 3999.00))
    #for pr in lista_produtos:
    #    print(pr.nome)
    
    espacos = []
    valores = []
    nomes = []
    for produto in lista_produtos: #adiciona nas listas acima todos os produdos da classe produto
        espacos.append(produto.espaco)
        valores.append(produto.valor)
        nomes.append(produto.nome)
    limite = 3 #limite o caminhao em 3 metros cubicos
    
    
    tamanho_populacao = 20 #tamanho da população iniciall
    taxa_mutacao = 0.01
    numero_geracoes = 1000
    
    ag = AlgoritmoGenetico(tamanho_populacao) #inicia a população
    
    resultado = ag.resolver(taxa_mutacao, numero_geracoes, espacos, valores, limite)
    for i in range(len(lista_produtos)):
        if resultado[i] == '1':
            print("Nome: %s R$ %s " % (lista_produtos[i].nome,
                                       lista_produtos[i].valor))
     
    #linha 73, 124,125, 152
    
    #for valor in ag.lista_solucoes:
    #    print(valor)
    plt.plot(ag.lista_solucoes)
    plt.title("Acompanhamento dos valores")
    plt.show()
