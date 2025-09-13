#### Esta avaliação tem por objetivo consolidar o aprendizado sobre conceitos de IPC, threads, concorrência e paralelismo.
#### Linguagem utilizada: Python

## Códigos Base:
### Tipos e estruturas comuns
#### struct PGM {
####  int w, h, maxv; // maxv = 255
####  unsigned char* data; // w*h bytes (tons de cinza)
#### };

#### struct Header {
####  int w, h, maxv; // metadados da imagem
####  int mode; // 0=NEGATIVO, 1=SLICE
####  int t1, t2; // válido se mode=SLICE
#### };

#### struct Task {
####  int row_start; // linha inicial (inclusiva)
####  int row_end; // linha final (exclusiva)
#### };

### Funções utilitárias (I/O de PGM) 
#### int read_pgm(const char* path, PGM* img);
#### int write_pgm(const char* path, const PGM* img);

### Constantes de modo 
#### #define MODE_NEG 0
#### #define MODE_SLICE 1

<br>

### FIFO 
#### const char* FIFO_PATH = "/tmp/imgpipe";

#### // estrutura base do processo emissor
#### int main_sender(int argc, char** argv) {
####  // argv: img_sender <fifo_path> <entrada.pgm>
####  // Emissor só envia a imagem; quem decide o filtro é o worker pelo CLI dele.
####  parse_args_or_exit();
####  const char* fifo = argv[1];
####  const char* inpath = argv[2];

####  1. Garante a existência do FIFO (mkfifo se necessário)
#### 
####  2. Lê a imagem PGM (P5) do disco
#### 
####  3. Prepara cabeçalho (mode/t1/t2 serão ignorados pelo worker;
####  Aqui enviamos apenas metadados da imagem)

####  4. Abre FIFO para escrita (bloqueia até worker abrir para leitura)
#### 
####  5. Envia cabeçalho + pixels
#### 
####  6. Fecha FIFO e libera memória

####  7. Fim
####  return 0;

<br>

## Processo Worker (que realiza o processamento de imagens) – Variáveis globais
###  Fila de tarefas (circular) + sincronização
#### #define QMAX 128
#### Task queue_buf[QMAX];
#### int q_head = 0, q_tail = 0, q_count = 0;

#### pthread_mutex_t q_lock = MUTEX_INIT;
#### sem_t sem_items; // quantas tarefas disponíveis
#### sem_t sem_space; // espaço livre na fila

<br>

###  Sinalização de término
#### pthread_mutex_t done_lock = MUTEX_INIT;
#### sem_t sem_done; // sinaliza quando todas as tarefas finalizam
#### int remaining_tasks = 0;

<br>

###  Dados compartilhados para processamento
#### PGM g_in, g_out;
#### int g_mode; // MODE_NEG ou MODE_SLICE
#### int g_t1, g_t2;
#### int g_nthreads = 4;