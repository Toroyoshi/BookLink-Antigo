# bookLink — Starter Kit (FastAPI + Microserviços + Docker)

Este repositório é um **starter kit completo** para o projeto **bookLink** (gestão de biblioteca) com:
- **4 microserviços**: `user-service`, `catalog-service`, `loan-service`, `payment-service`
- **Python + FastAPI**
- **Docker + Docker Compose**
- **Autenticação JWT**
- **CLI** (linha de comandos) para testar fluxos (sem GUI)

## 1) Como correr

Pré-requisitos: Docker e Docker Compose.

```bash
docker compose up --build
```

Serviços expostos no host:
- user-service: http://localhost:8001/docs
- catalog-service: http://localhost:8002/docs
- loan-service: http://localhost:8003/docs
- payment-service: http://localhost:8004/docs

## 2) Inicializar dados (opcional)
Depois de subir os serviços, podes criar um utilizador staff e inserir livros/cópias via Swagger.

## 3) CLI
A CLI fica em `cli/booklink.py`.

Instalar deps localmente (opcional, fora de Docker):
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r cli/requirements.txt
```

Exemplos:
```bash
python cli/booklink.py login --email staff@uni.pt --password 1234 --base-user http://localhost:8001
python cli/booklink.py whoami

python cli/booklink.py catalog-add-work --title "Clean Architecture" --isbn "9780134494166" --year 2017
python cli/booklink.py catalog-add-copy --work-id 1 --barcode "BC-0001" --location "Piso 1"

python cli/booklink.py search "clean"
python cli/booklink.py loan --copy-id 1
python cli/booklink.py my-loans
python cli/booklink.py return --loan-id 1
python cli/booklink.py fines
python cli/booklink.py pay --fine-id 1 --method card
```

> Nota: para ações de staff (criar obras/cópias), faz login com um utilizador `role=staff`.

## 4) Decisões (simples e eficazes para projeto académico)
- **DB por serviço** (PostgreSQL)
- Consistência “quase transacional” no empréstimo:
  - `loan-service` pede ao `catalog-service` para **claim** da cópia (`AVAILABLE -> LOANED`)
  - se falhar, não cria empréstimo
- Pagamentos são simulados:
  - cria `PENDING` e depois confirmas com endpoint/CLI

## 5) Variáveis de ambiente
Estão no `docker-compose.yml`. Podes ajustar:
- `JWT_SECRET`
- `FINE_PER_DAY_EUR`
- prazos (`LOAN_DAYS_STUDENT`, etc.)

## 6) Próximos passos
- Adicionar Alembic migrations
- Adicionar fila de espera completa para reservas
- Adicionar eventos (RabbitMQ) para desacoplar pagamentos/multas
