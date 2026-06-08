import json
from typing import Optional


# ── Entrada ──────────────────────────────────────────────────

def ler_registros(caminho: str) -> list:
    """Lê notas.txt e retorna uma lista de dicionários {nome, nota}."""
    registros = []

    try:
        with open(caminho, "r", encoding="utf-8") as f:
            for numero, linha in enumerate(f, start=1):
                registro = _parsear_linha(linha.strip(), numero)
                if registro:
                    registros.append(registro)
    except FileNotFoundError:
        print(f'Erro: arquivo "{caminho}" não encontrado.')

    return registros


def _parsear_linha(linha: str, numero: int) -> Optional[dict]:
    """Converte 'Nome: nota' em {'nome': ..., 'nota': ...}. Retorna None se inválido."""
    try:
        partes = linha.split(":")
        if len(partes) != 2:
            raise ValueError("formato esperado: Nome: nota")
        nome = partes[0].strip()
        nota = float(partes[1].strip())
        if not (0.0 <= nota <= 10.0):
            raise ValueError(f"nota {nota} fora do intervalo 0–10")
        return {"nome": nome, "nota": nota}
    except ValueError as e:
        print(f"Linha {numero} ignorada: {e}")
        return None


# ── Processamento ─────────────────────────────────────────────

def calcular_estatisticas(registros: list[dict]) -> dict:
    """Retorna média, maior nota, menor nota e total de alunos."""
    notas = [r["nota"] for r in registros]
    return {
        "media": sum(notas) / len(notas),
        "maior": max(notas),
        "menor": min(notas),
        "total": len(notas),
    }


def classificar_aluno(nota: float) -> str:
    """Retorna o status do aluno conforme a nota."""
    if nota >= 7.0:
        return "Aprovado"
    elif nota >= 5.0:
        return "Recuperação"
    else:
        return "Reprovado"


# ── Saída ─────────────────────────────────────────────────────

def imprimir_relatorio(registros: list[dict], stats: dict) -> None:
    """Imprime o relatório no terminal, ordenado por nota decrescente."""
    linha = "=" * 42
    print(linha)
    print("     RELATÓRIO DE NOTAS — TURMA 2026.1")
    print(linha)
    print(f"{'ALUNO':<22} {'NOTA':>5}  STATUS")
    print("-" * 42)

    for r in sorted(registros, key=lambda x: x["nota"], reverse=True):
        print(f"{r['nome']:<22} {r['nota']:>5.1f}  {r['status']}")

    print("-" * 42)
    print(f"Média: {stats['media']:.2f}   Maior: {stats['maior']:.1f}   Menor: {stats['menor']:.1f}")
    print(linha)


def salvar_relatorio(registros: list[dict], stats: dict, destino: str) -> None:
    """Serializa os dados para JSON e salva no arquivo destino."""
    payload = {
        "turma": "2026.1",
        "estatisticas": stats,
        "alunos": registros,
    }
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, sort_keys=True)
    print(f'Relatório salvo em "{destino}".')


# ── Ponto de entrada ──────────────────────────────────────────

if __name__ == "__main__":
    dados = ler_registros("notas.txt")

    for r in dados:
        r["status"] = classificar_aluno(r["nota"])

    stats = calcular_estatisticas(dados)
    imprimir_relatorio(dados, stats)
    salvar_relatorio(dados, stats, "relatorio.json")
