#### Esta avaliação tem por objetivo consolidar o aprendizado sobre conceitos de IPC, threads, concorrência e paralelismo.
#### Linguagem utilizada: Python

## Códigos Base:
### Tipos e estruturas comuns
#####  struct PGM {
#####   int w, h, maxv; // maxv = 255
#####   unsigned char* data; // w*h bytes (tons de cinza)
#####  };

##### struct Header {
#####  int w, h, maxv; // metadados da imagem
#####  int mode; // 0=NEGATIVO, 1=SLICE
#####  int t1, t2; // válido se mode=SLICE
##### };

##### struct Task {
#####  int row_start; // linha inicial (inclusiva)
#####  int row_end; // linha final (exclusiva)
##### };

### Funções utilitárias (I/O de PGM) 
##### int read_pgm(const char* path, PGM* img);
##### int write_pgm(const char* path, const PGM* img);

### Constantes de modo 
##### #define MODE_NEG 0
##### #define MODE_SLICE 1

<br>

## FIFO 
##### const char* FIFO_PATH = "/tmp/imgpipe";

##### // estrutura base do processo emissor
##### int main_sender(int argc, char** argv) {
#####  // argv: img_sender <fifo_path> <entrada.pgm>
#####  // Emissor só envia a imagem; quem decide o filtro é o worker pelo CLI dele.
#####  parse_args_or_exit();
#####  const char* fifo = argv[1];
#####  const char* inpath = argv[2];

#####  1. Garante a existência do FIFO (mkfifo se necessário)
##### 
#####  2. Lê a imagem PGM (P5) do disco
##### 
#####  3. Prepara cabeçalho (mode/t1/t2 serão ignorados pelo worker;
#####  Aqui enviamos apenas metadados da imagem)

#####  4. Abre FIFO para escrita (bloqueia até worker abrir para leitura)
##### 
#####  5. Envia cabeçalho + pixels
##### 
#####  6. Fecha FIFO e libera memória

#####  7. Fim
#####  return 0;

<br>

## Processo Worker (que realiza o processamento de imagens) – Variáveis globais
###  Fila de tarefas (circular) + sincronização
##### #define QMAX 128
##### Task queue_buf[QMAX];
##### int q_head = 0, q_tail = 0, q_count = 0;

<BR>

#####  pthread_mutex_t q_lock = MUTEX_INIT;
#####  sem_t sem_items; // quantas tarefas disponíveis
#####  sem_t sem_space; // espaço livre na fila

<br>

##  Sinalização de término
#####  pthread_mutex_t done_lock = MUTEX_INIT;
#####  sem_t sem_done; // sinaliza quando todas as tarefas finalizam
#####  int remaining_tasks = 0;

<br>

##  Dados compartilhados para processamento
#####  PGM g_in, g_out;
#####  int g_mode; // MODE_NEG ou MODE_SLICE
#####  int g_t1, g_t2;
#####  int g_nthreads = 4;

<BR>

## Funções da fila (produtor/consumidor), base do filtro e thread base
#### //filtros
#### void apply_negative_block(int rs, int re) {
####  //lógica do filtro
#### }
#### void apply_slice_block(int rs, int re, int t1, int t2) {
####  // lógica do filtro
#### }
#### //thread base
#### void* worker_thread(void* arg) {
####  while (1) {
####  //lógica da thread
####  }
####  return NULL;
#### }

<BR>

## Função principal
####  int main_worker(int argc, char** argv) {
####    // argv: img_worker <fifo_path> <saida.pgm> <negativo|slice> [t1 t2] [nthreads]
####    parse_args_or_exit();
####    const char* fifo = argv[1];
####    const char* outpth = argv[2];
####    const char* mode = argv[3];
####    if (mode == "negativo") {
####    g_mode = MODE_NEG;
####    g_nthreads = (argc >= 5) ? atoi(argv[4]) : 4;
####    } else if (mode == "slice") {
####    g_mode = MODE_SLICE;
####    g_t1 = atoi(argv[4]);
####    g_t2 = atoi(argv[5]);
####    g_nthreads = (argc >= 7) ? atoi(argv[6]) : 4;
####    } else {
####    exit_error("Modo inválido");
####    }
####    // 1) Garante FIFO e abre para leitura (bloqueia até sender abrir em escrita)
####    // 2) Lê cabeçalho + pixels do FIFO
####    
####    // 3) Cria pool de threads e fila de tarefas – porém, não é necessário ser um pool de threads
####    
####    // 5) Aguarda término de todas as tarefas
####    
####    // 7) Grava imagem de saída
####    
####    // 8) Libera recursos
####    // 9) Fim
####    return 0;
#### }
#### 

## Base matemática e código base dos filtros
#### Operação de negativo: 𝑠 = 𝑇(𝑟) = 𝐿 − 1 − 𝑟 = 255 − 𝑟
#### onde 𝑟 representa o pixel de entrada e 𝐿 é o máximo valor representado pela quantidade e pixel na imagem


## Pseudo código do negativo
#### Loop 1 de 0 até tamanho x:
####  Loop 2 de 0 até tamanho y:
####  novo_pixel[x,y] = 255 – valor_pixel_original[x,y]
