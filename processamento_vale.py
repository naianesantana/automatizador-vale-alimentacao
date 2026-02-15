import pandas as pd

# --- REGRAS DE NEGÓCIO ---
def calcular_valor_vale(horas):
    '''
    a função recebe uma variável genérica,
    valida com o valor da coluna Trabalhado
    retorna a validação à coluna Valor VA
    '''
    if horas >= 7: #
        return  27.00 #
    else:
        return 10.00

# --- PROCESSO PRINCIPAL ---

#1. Importação do arquivo --- Leitura do arquivo .csv e especificação do separador ;
df = pd.read_csv('ponto-diario-JAN2026.csv',sep=';')


#2. Tratamento do arquivo
df.drop(columns=['Registros','Extras','Faltas'],inplace=True) #Remove as colunas Registros, Extras e Faltas
df['Data'] = df['Data'].ffill() #Preenche datas vazias replicando a anterior

#Remove linhas onde o Funcionário ou Carga horária possuem valor vazios (NaN)
df.dropna(subset=['Funcionário','Carga horária'], inplace=True)

df['Trabalhado'] = df['Trabalhado'].str.strip() #Limpa os espaços em branco
df = df[df['Trabalhado'] != '00:00'] #Remove dias não trabalhados

#Conversão de tempo: Transforma HH:MM em duração e depois em número decimal para cálculos
df['Trabalhado'] = pd.to_timedelta(df['Trabalhado'] + ':00')
df['Trabalhado'] = df['Trabalhado'].dt.total_seconds() / 3600


#3. Cálculos - Aplica a função de regra de negócio linha por linha
df['Valor VA'] = df['Trabalhado'].apply(calcular_valor_vale)

#Soma o valor completo de Vale-alimentação por funcionário
resultado = df.groupby('Funcionário')['Valor VA'].sum().reset_index() #.reset_index() transforma em uma tabela novamente


#4. Exportação para Excel
nome_arquivo = 'Relatorio-Vale-Alimentacao.xlsx'

#Gera o arquivo com duas abas: uma com detalhamento diário e outro com o valor mensal do VA
with pd.ExcelWriter(nome_arquivo) as writer:
    df.to_excel(writer,sheet_name='Relatorio Diário',index=False)
    resultado.to_excel(writer,sheet_name='Valor Mensal',index=False)


