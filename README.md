# Sistema Automatizado de Análise de Missões Espaciais

**FIAP — Global Solution 2026 | AI for RPA | 1º Semestre**

Solução automatizada que processa logs de missões espaciais e imagens de sensores, gerando um relatório Excel completo com os resultados da análise.

---

## O que o projeto faz

O pipeline funciona em três etapas:

1. **NLP** — lê os arquivos de log das missões, extrai eventos com horário, classifica a severidade (CRITICO / ALERTA / NORMAL / INFO) e identifica as palavras mais frequentes com NLTK
2. **Visão Computacional** — analisa as imagens dos sensores com OpenCV, detecta anomalias térmicas e classifica cada imagem
3. **Relatório Excel** — consolida tudo automaticamente em um `.xlsx` com 5 abas formatadas

---

## Estrutura do projeto

```
RPAGS/
├── main.py                        # pipeline principal
├── nlp_module.py                  # módulo de NLP
├── vision_module.py               # módulo de visão computacional
├── gerar_imagens.py               # gera imagens de sensor simuladas para teste
├── GS2026_Missoes_Espaciais.ipynb # notebook para rodar no Google Colab
├── requirements.txt               # dependências
├── data/
│   ├── logs/                      # arquivos .txt com logs das missões
│   └── images/                    # imagens .png dos sensores
└── outputs/
    ├── relatorio_missoes.xlsx      # relatório Excel gerado automaticamente
    ├── grafico_nlp.png             # gráfico de eventos por missão
    ├── grafico_visao.png           # grade das imagens analisadas
    └── documentacao_projeto.docx  # documentação completa do projeto
```

---

## Como executar

### Opção 1 — Google Colab (recomendado)

1. Abra o arquivo `GS2026_Missoes_Espaciais.ipynb` no [Google Colab](https://colab.research.google.com/)
2. Execute todas as células em ordem (`Ctrl+F9`)
3. O relatório Excel será baixado automaticamente ao final

### Opção 2 — Local

```bash
# instalar dependências
pip install -r requirements.txt

# gerar imagens de teste (se não tiver imagens próprias)
python gerar_imagens.py

# executar o pipeline
python main.py
```

O relatório será salvo em `outputs/relatorio_missoes.xlsx`.

---

## Dependências

| Biblioteca | Versão | Uso |
|---|---|---|
| nltk | >=3.8 | Tokenização, stopwords e palavras-chave |
| opencv-python | >=4.8 | Análise de imagens e detecção de anomalias |
| pandas | >=2.0 | DataFrames no notebook |
| openpyxl | >=3.1 | Geração do relatório Excel |
| Pillow | >=10.0 | Criação das imagens simuladas |
| numpy | >=1.24 | Operações com arrays de pixels |
| matplotlib | >=3.7 | Gráficos no notebook |

---

## Critérios atendidos (GS 2026)

| Critério | Peso | Como foi atendido |
|---|---|---|
| Domínio Técnico e Integração de Conceitos | 40% | NLP (NLTK) + Visão Computacional (OpenCV) integrados em um único pipeline |
| Arquitetura de Fluxo e Engenharia de Software | 25% | Pipeline modularizado com tratamento de exceções e separação de responsabilidades |
| Inteligência de Dados e Recursos de IA | 20% | Tokenização, classificação por palavras-chave, threshold e análise estatística de pixels |
| Entrega de Artefatos e Outputs Técnicos | 15% | Excel com 5 abas, 2 gráficos PNG e DataFrames exibidos no notebook |
