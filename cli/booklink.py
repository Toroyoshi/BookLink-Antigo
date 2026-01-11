import json
import os
from pathlib import Path
import requests
import typer

app = typer.Typer(no_args_is_help=True)

TOKEN_PATH = Path.home() / ".booklink_token.json"

DEFAULTS = {
    "user": "http://localhost:8001",
    "catalog": "http://localhost:8002",
    "loan": "http://localhost:8003",
    "payment": "http://localhost:8004",
}

def save_token(token: str):
    TOKEN_PATH.write_text(json.dumps({"access_token": token}, ensure_ascii=False), encoding="utf-8")

def load_token() -> str:
    if not TOKEN_PATH.exists():
        raise typer.Exit("Ainda não fizeste login. Usa: booklink.py login ...")
    return json.loads(TOKEN_PATH.read_text(encoding="utf-8"))["access_token"]

def auth_headers() -> dict:
    return {"Authorization": f"Bearer {load_token()}"}

@app.command()
def login(
    email: str = typer.Option(...),
    password: str = typer.Option(...),
    base_user: str = typer.Option(DEFAULTS["user"]),
):
    r = requests.post(f"{base_user}/auth/login", json={"email": email, "password": password}, timeout=10)
    if r.status_code != 200:
        raise typer.Exit(f"Login falhou: {r.status_code} {r.text}")
    token = r.json()["access_token"]
    save_token(token)
    typer.echo("OK: token guardado em ~/.booklink_token.json")

@app.command()
def register(
    name: str = typer.Option(...),
    email: str = typer.Option(...),
    password: str = typer.Option(...),
    role: str = typer.Option("student"),
    base_user: str = typer.Option(DEFAULTS["user"]),
):
    r = requests.post(f"{base_user}/auth/register", json={"name": name, "email": email, "password": password, "role": role}, timeout=10)
    if r.status_code != 200:
        raise typer.Exit(f"Register falhou: {r.status_code} {r.text}")
    
    token = r.json()["access_token"]
    save_token(token)
    typer.echo("OK: utilizador criado e token guardado")

@app.command()
def whoami(base_user: str = typer.Option(DEFAULTS["user"])):
    r = requests.get(f"{base_user}/users/me", headers=auth_headers(), timeout=10)
    typer.echo(r.text)

@app.command()
def search(
    query: str,
    base_catalog: str = typer.Option(DEFAULTS["catalog"]),
):
    r = requests.get(f"{base_catalog}/works", params={"query": query}, timeout=10)
    typer.echo(r.text)

@app.command()
def catalog_add_work(
    title: str = typer.Option(...),
    isbn: str = typer.Option(None),
    year: int = typer.Option(None),
    language: str = typer.Option(None),
    subjects: str = typer.Option(None),
    base_catalog: str = typer.Option(DEFAULTS["catalog"]),
):
    r = requests.post(
        f"{base_catalog}/works",
        json={"title": title, "isbn": isbn, "year": year, "language": language, "subjects": subjects},
        headers=auth_headers(),
        timeout=10,
    )
    typer.echo(r.text)

@app.command()
def catalog_add_copy(
    work_id: int = typer.Option(...),
    barcode: str = typer.Option(...),
    location: str = typer.Option(None),
    base_catalog: str = typer.Option(DEFAULTS["catalog"]),
):
    r = requests.post(
        f"{base_catalog}/copies/work/{work_id}",
        json={"barcode": barcode, "location": location},
        headers=auth_headers(),
        timeout=10,
    )
    typer.echo(r.text)

@app.command()
def loan(
    copy_id: int = typer.Option(...),
    base_loan: str = typer.Option(DEFAULTS["loan"]),
):
    r = requests.post(f"{base_loan}/loans", json={"copy_id": copy_id}, headers=auth_headers(), timeout=10)
    typer.echo(r.text)

@app.command()
def my_loans(base_loan: str = typer.Option(DEFAULTS["loan"])):
    r = requests.get(f"{base_loan}/loans", headers=auth_headers(), timeout=10)
    typer.echo(r.text)

@app.command()
def return_(
    loan_id: int = typer.Option(..., "--loan-id"),
    base_loan: str = typer.Option(DEFAULTS["loan"]),
):
    r = requests.post(f"{base_loan}/loans/{loan_id}/return", headers=auth_headers(), timeout=10)
    typer.echo(r.text)

@app.command()
def fines(base_loan: str = typer.Option(DEFAULTS["loan"])):
    r = requests.get(f"{base_loan}/fines", headers=auth_headers(), timeout=10)
    typer.echo(r.text)

@app.command()
def pay(
    fine_id: int = typer.Option(...),
    amount: float = typer.Option(...),
    method: str = typer.Option("card"),
    base_payment: str = typer.Option(DEFAULTS["payment"]),
):
    # 1) cria pagamento
    r = requests.post(
        f"{base_payment}/payments",
        json={"fine_id": fine_id, "amount_eur": amount, "method": method},
        headers=auth_headers(),
        timeout=10,
    )
    if r.status_code != 200:
        raise typer.Exit(r.text)
    payment_id = r.json()["id"]
    typer.echo(f"Criado pagamento PENDING id={payment_id}")

    # 2) confirma pagamento
    r2 = requests.post(f"{base_payment}/payments/{payment_id}/confirm", headers=auth_headers(), timeout=10)
    typer.echo(r2.text)

if __name__ == "__main__":
    app()
