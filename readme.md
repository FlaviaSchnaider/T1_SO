#### Esta avaliação tem por objetivo consolidar o aprendizado sobre conceitos de IPC, threads, concorrência e paralelismo.
#### Linguagem utilizada: Python

#### Problemática: Sistema de processamento paralelo para processamento de imagens

<br>

## Descrição Geral
##### O estudo de Sistemas Operacionais envolve compreender como processos e threads
##### podem cooperar e competir pelos recursos do sistema. A comunicação entre processos (IPC)
##### permite que aplicações independentes troquem dados de forma organizada, enquanto o uso de
##### threads possibilita a exploração do paralelismo, distribuindo o trabalho em múltiplas unidades
##### de execução que compartilham memória.

##### No contexto de processamento de imagens, essas técnicas assumem papel essencial,
##### pois operações sobre pixels podem ser naturalmente paralelizadas, reduzindo tempo de
##### execução em imagens de grande porte. Entretanto, o paralelismo exige mecanismos de
##### sincronização (como mutexes e semáforos) para garantir consistência dos dados e evitar
##### condições de corrida. Assim, a combinação de IPC, threads e sincronização fornece uma base
##### prática para projetar sistemas eficientes que unem concorrência e correção na manipulação
##### de dados visuais.

<br>

## Fundamentação Teórica
##### A comunicação entre processos (IPC) é um mecanismo essencial para que aplicações
##### distintas possam trocar dados e coordenar atividades. Entre os métodos disponíveis em
##### sistemas Unix, destacam-se os FIFOs (named pipes), que permitem a transmissão de fluxos
##### de bytes entre processos independentes.

##### No nível intra-processo, a utilização de threads possibilita a execução concorrente em
##### um espaço de memória compartilhado, favorecendo o paralelismo de dados em aplicações
##### que envolvem grande volume de operações repetitivas, como no processamento de imagens.
##### Entretanto, o uso de threads introduz a necessidade de sincronização. Mecanismos como
##### mutexes (para exclusão mútua) e semáforos (para controle de acesso e sinalização de
##### eventos) são fundamentais para evitar condições de corrida, garantir integridade de dados e
##### coordenar corretamente a execução concorrente.

##### No campo do processamento digital de imagens, operações como filtro negativo
##### (transformação linear simples: out = 255 – in) e limiarização com fatiamento (manutenção de
##### valores dentro de uma faixa [t1, t2] e supressão dos demais) são particularmente adequadas
##### para estudo, pois envolvem processamento independente por pixel, permitindo observar
##### ganhos concretos com o uso de paralelismo.

<br>

## Componentes do Sistema Arquitetura da Solução
##### A solução proposta é composta por dois processos independentes que se comunicam
##### através de um FIFO nomeado:
##### 1. Processo Emissor (Sender): responsável por carregar a imagem de entrada no formato
##### PGM (P5), empacotar os metadados (largura, altura, valor máximo de intensidade) e
##### transmitir os dados de pixels pelo FIFO.
##### 2. Processo Trabalhador (Worker): recebe os dados da imagem via FIFO, instancia um pool
##### de threads e distribui as tarefas em uma fila protegida por mutex e semáforos. Cada
##### thread processa um subconjunto das linhas da imagem, aplicando o filtro especificado
##### (negativo ou limiarização com fatiamento). Ao final, o processo trabalhador salva a
##### imagem resultante em disco.
##### A sincronização é garantida por:
##### • Mutex, para proteger a fila de tarefas;
##### • Semáforos contadores, para coordenar produção e consumo das tarefas;
##### • Semáforo de conclusão, para indicar o término do processamento.


## Resultados Esperados
##### A execução da solução deverá evidenciar:
##### • A correta transmissão de dados entre processos independentes por meio de FIFO,
##### validando o uso de IPC;
##### • A aplicação correta dos filtros de imagem, resultando em arquivos processados (negativo
##### e limiarização por fatiamento) de acordo com os parâmetros fornecidos;
##### • A redução do tempo de processamento em imagens de grande porte, proporcionada pela
##### distribuição de trabalho entre múltiplas threads;
##### • O funcionamento adequado dos mecanismos de sincronização, garantindo a integridade
##### dos dados e a ausência de condições de corrida;
##### • A demonstração prática da relevância dos conceitos de processos, threads, paralelismo
##### e sincronização para problemas reais de computação 

### Comando Worker Negativo: 
````
```
python worker.py /tmp/imgpipe saida_neg.pgm negativo 4
```
````

### Comando Worker Slice: 
````
```
python worker.py /tmp/imgpipe saida_slice.pgm slice 4
```
````

### Comando Sender: 
````
```
python sender.py /tmp/imgpipe ./tmp/imgpipe.png
```
````