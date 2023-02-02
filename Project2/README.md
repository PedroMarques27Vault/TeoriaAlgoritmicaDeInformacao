# TAI_Project2
Este programa tem como objetivo a identificação da linguagem num ficheiro de texto
Todos os ficheiros de texto de treino estao na pasta languages/train. Os de teste estao na pasta languages/test e os ficheiros com multiplos idiomas
estão na pasta languages/mixed
Para correr o código:
-Abrir linha de comandos na pasta bin
-Executar um dos script combLocateLang.py, locateLang.py ou findLang.py  fornecendo alguns argumentos na seguinte ordem (apenas o filename é obrigatório):
    -filename -> Nome do ficheiro inicial
    -k -> dimensão do contexto, não meter caso esteja a usar o combLocateLang.py
    -a -> alpha para cálculo da estimativa de probabilidades

    Exemplo:
        -python3 locateLang.py sherlock.txt 3 0.01 
    
