# Automatizador de Cálculo: Vale-Alimentação

Esse projeto automatiza a conferência e o cálculo do vale-alimentação por hora trabalhada.

A ideia surgiu da necessidade da atual empresa que atuo de validar o cálculo por meio de regras mais específicas que, muitos aplicativos de ponto eletrônico, não realizam.

## Principais funcionalidade:
* **Limpeza de Dados**: Remoção de colunas irrelevantes e tratamento de valores nulos.
* **Tratamento de Tempo**: Conversão de registros de horas (HH:MM) para formato decimal para cálculos matemáticos.
* **Processamento Inteligente**: Uso da biblioteca Pandas para manipular grandes volumes de dados de forma eficiente.
* **Exportação Multitab**: Geração de arquivo `.xlsx` com duas abas:
    1.  **Relatório Diário**: Detalhamento de cada dia trabalhado e o valor do VA correspondente.
    2.  **Valor Mensal**: Resumo consolidado com o total que cada funcionário deve receber no mês.

## Tecnologias Utilizadas:
* **Python **
* **Pandas**: Para manipulação e análise de dados.
* **Openpyxl**: Engine para suporte à exportação de arquivos Excel.
