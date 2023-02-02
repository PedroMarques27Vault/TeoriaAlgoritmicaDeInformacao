# TAI_Project1
Este programa tem como objetivo a recolha de dados estatísticos de um texto fornecido 
bem como a geração de um novo texto que obedece às mesmas estatísticas
Para correr o código:
-Abrir linha de comandos na pasta bin
-Executar o script generator.py fornecendo alguns argumentos na seguinte ordem (apenas o filename é obrigatório):
    -filename -> Nome do ficheiro inicial
    -k -> dimensão do contexto
    -a -> alpha para cálculo da estimativa de probabilidades
    -length -> dimensão do texto gerado
    -text -> texto inicial
    Exemplo:
        -python3 generator.py sherlock.txt 3 0.01 1000 'She'
    
-O texto gerado encontra-se no ficheiro output.txt na pasta src