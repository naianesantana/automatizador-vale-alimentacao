import pandas as pd
pd.set_option('display.max_columns',None)

#Variáveis que recebem os arquivos .csv
arquivo_ponto = 'exportacao-relatorio-ponto-diario.csv'
arquivo_abono = 'exportacao-ausencias.csv'

#Funções para conversão dos tipos de dados
def converter_data(df,coluna,formato):
    df[coluna] = df[coluna].str.strip()
    df[coluna] = pd.to_datetime(df[coluna],format=formato)
    return df

def converter_tempo(df,coluna):
    df[coluna] = (df[coluna]
                  .fillna('00:00')
                  .str.strip())
    df[coluna] = pd.to_timedelta(df[coluna] + ':00')
    df[coluna] = df[coluna].dt.total_seconds() / 3600
    return df

#Função com as regras de negócio para sucesso no cálculo do valor do vale alimentação diário
def calcular_valor_vale(linha):
    carga_horaria = linha['Carga horária']
    trabalhado = linha['Total horas']
    dia_semana = linha['Dia semana']

    if trabalhado == 0:
        return 0.00
    elif carga_horaria < 8 and 0 < trabalhado < 8 and dia_semana != 'sáb' and dia_semana != 'dom':
        return 10.00
    else:
        return 27.00

#1. Leitura das variáveis e especificação de quais colunas serão consideradas
df_ponto = pd.read_csv(arquivo_ponto,sep=';',
                 usecols=['Data','Funcionário','Trabalhado','Carga horária'])

df_abono = pd.read_csv(arquivo_abono,sep=';',
            usecols=['Tipo','Funcionário','Ocorrência','Data inicial'])

#2. Início do processo de Tratamento dos dados
df_ponto['Data'] = df_ponto['Data'].ffill()

df_ponto['Dia semana'] = (df_ponto['Data']
                    .str.split()
                    .str.get(-1)
                    .str.strip())

df_ponto['Data'] = (df_ponto['Data']
              .str.split()
              .str.get(0)
              .str.strip())

df_ponto.dropna(subset='Funcionário', inplace=True)

df_abono['Ocorrência'] = (df_abono['Ocorrência']
                          .str.split()
                          .str.get(-1)
                          .str.strip('()'))

#Chamada das funções de conversão dos dados para datetime
df_ponto= converter_data(df_ponto,'Data','%d/%m/%y')
df_abono = converter_data(df_abono,'Data inicial','%d/%m/%Y')

#Filtro que permiti somente as linhas com tipo Abono
df_abono = df_abono[df_abono['Tipo'].str.contains('Abono',na=False)]

#3. Agrupamento dos dois dataframes
df_agrupado = pd.merge(
    df_ponto,
    df_abono,
    how='left',
    left_on=['Funcionário','Data'],
    right_on=['Funcionário','Data inicial']
)

#4. Continuação no Tratamento dos dados (Agora dos dataframes agrupados)

#Chamada das funções de coversão para tempo e númerico
df_agrupado = converter_tempo(df_agrupado,'Carga horária')
df_agrupado = converter_tempo(df_agrupado,'Trabalhado')
df_agrupado = converter_tempo(df_agrupado,'Ocorrência')

df_agrupado['Tipo'] = df_agrupado['Tipo'].fillna('-')
df_agrupado['Total horas'] = df_agrupado['Trabalhado'] + df_agrupado['Ocorrência']

#5. Crição de um df final que receberá o valor diário do VA
df_final = df_agrupado[['Data','Dia semana', 'Funcionário','Trabalhado','Carga horária','Tipo','Ocorrência','Total horas']]

df_final['Valor VA'] = df_final[['Total horas','Carga horária','Dia semana']].apply(calcular_valor_vale, axis=1)
df_final['Data'] = df_final['Data'].dt.strftime('%d/%m/%Y')


#6. Emissão do relatório em Excel com os valores diários e mensal - agrupado por funcionário
resultado = df_final.groupby('Funcionário')['Valor VA'].sum().reset_index()
relatorio_diario = df_final.groupby('Funcionário')

nome_arquivo = 'Relatorio-VA1.xlsx'

with pd.ExcelWriter(nome_arquivo) as writer:
    resultado.to_excel(writer,sheet_name='Valor Mensal',index=False)

    nome_func = df_final['Funcionário']
    grupo = df_final.groupby('Funcionário').groups
    for nome_func,grupo in relatorio_diario:
        grupo.to_excel(writer,sheet_name=f'{nome_func}',index=False)

    print('Relatório salvo!')