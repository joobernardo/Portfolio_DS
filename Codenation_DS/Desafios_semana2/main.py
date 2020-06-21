#!/usr/bin/env python
# coding: utf-8

# # Desafio 1
# 
# Para esse desafio, vamos trabalhar com o data set [Black Friday](https://www.kaggle.com/mehdidag/black-friday), que reúne dados sobre transações de compras em uma loja de varejo.
# 
# Vamos utilizá-lo para praticar a exploração de data sets utilizando pandas. Você pode fazer toda análise neste mesmo notebook, mas as resposta devem estar nos locais indicados.
# 
# > Obs.: Por favor, não modifique o nome das funções de resposta.

# ## _Set up_ da análise

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


black_friday = pd.read_csv("black_friday.csv")


# ## Inicie sua análise a partir daqui

# # Vamos ver como os dados sao distribuidos no dataset

# In[3]:


#Como os dados estao no dataframe
black_friday.sample(5)


# Qual o tamanho do dataset

# In[4]:


# Tamanho do dataset
black_friday.shape


# Entendendo sobre os tipos de variaveis dentro do dataset

# In[5]:


# Vendo as sobre as colunas do dataframe
black_friday.info()


# # Entendendo melhor sobre o perfil de cliente que mais comprou na Black Friday
# 
# Valores maximos de cada coluna em destaque

# In[6]:


df = black_friday.groupby(['Age', 'Gender']).agg({'User_ID':'nunique', "Purchase":"sum"}).unstack()
df.columns = ['_'.join(col).rstrip('_') for col in [c[::-1] for c in df.columns.values]]
df.columns = ('F_n_users', 'M_n_users', 'F_Purchase_sum', 'M_Purchase_sum')
df.style.highlight_max(axis=0)


# Os top 10 clientes que mais compraram na Black Friday

# In[7]:


df = black_friday.groupby(["User_ID"]).agg(
        {'Product_ID':'count', 
        "Purchase":"sum"}
        ).sort_values(
            "Product_ID", 
            ascending = False
    ).head(10)

df.columns = ('Number_of_Purchased_itens', 'Purchase_sum')
df.style.highlight_max(axis=0)


# Top 10 profissoes que compraram mais

# In[8]:


df = black_friday.groupby(["Occupation"]).agg(
        {'Product_ID':'count', 
        "Purchase":"sum"}
        ).sort_values(
            "Product_ID", 
            ascending = False
    ).head(10)

df.columns = ('Number_of_Purchased_itens', 'Purchase_sum')
df.style.highlight_max(axis=0)


# Qual estado civil comprou mais?

# In[9]:


df = black_friday.groupby(
    ['Marital_Status']
    ).agg(
        {'Product_ID':'count', 
        "Purchase":"sum"}
        )
df.columns = ('Number_of_sales', 'Purchase_sum')
df.style.highlight_max(axis=0)


# Compras por categoria de cidades

# In[10]:


df = black_friday.groupby(
    ['City_Category']
    ).agg(
        {'Product_ID':'count', 
        "Purchase":"sum"}
        )
df.columns = ('Number_of_sales', 'Purchase_sum')
df.style.highlight_max(axis=0)


# # Entendendo sobre os produtos mais vendidos
# top 10 produtos mais vendidos e com maiores faturamentos

# In[11]:


#top 10 pridutos mais vendidos e com maiores faturamentos
df = black_friday.groupby(
    ['Product_ID']
    ).agg(
        {'Product_ID':'count', 
        "Purchase":"sum"}
        ).sort_values(
            "Purchase", 
            ascending = False
    ).head(10)
df.columns = ('Number_of_sales', 'Purchase_sum')
df.style.highlight_max(axis=0)


# Categoria primaria mais vendida

# In[12]:


#top 10 pridutos mais vendidos e com maiores faturamentos

df = black_friday.groupby(
    ['Product_Category_1']
    ).agg(
        {'Product_ID':'count', 
        "Purchase":"sum"}
        ).sort_values(
            "Purchase", 
            ascending = False
    ).head(10)
df.columns = ('Number_of_sales', 'Purchase_sum')
df.style.highlight_max(axis=0)


# Entrando no detalhe das categoria dos produtos

# In[13]:


#top 10 pridutos mais vendidos e com maiores faturamentos
fillnulldf = black_friday.fillna("-")
df = fillnulldf.groupby(
    ['Product_Category_1',"Product_Category_2","Product_Category_3"]
    ).agg(
        {'Product_ID':'count', 
        "Purchase":"sum"}
        ).sort_values(
            "Purchase", 
            ascending = False
    ).head(10)
df.columns = ('Number_of_sales', 'Purchase_sum')
df.style.highlight_max(axis=0)


# ## Questão 1
# 
# Quantas observações e quantas colunas há no dataset? Responda no formato de uma tuple `(n_observacoes, n_colunas)`.

# In[14]:


def q1():
    # Retorne aqui o resultado da questão 1.
    # Tamanho do dataset
    return black_friday.shape
    #pass


# ## Questão 2
# 
# Há quantas mulheres com idade entre 26 e 35 anos no dataset? Responda como um único escalar.

# In[34]:


def q2():
    # Retorne aqui o resultado da questão 2.
    # Há quantas mulheres com idade entre 26 e 35 anos no dataset? Responda como um único escalar.
    filter1 = (black_friday['Gender'] == 'F') #apenas genero feminino
    filter2 = (black_friday['Age'] == '26-35') # categoria de idade
    return int(black_friday[(filter1) & (filter2)].User_ID.count())
    #pass


# ## Questão 3
# 
# Quantos usuários únicos há no dataset? Responda como um único escalar.

# In[16]:


def q3():
    # Retorne aqui o resultado da questão 3.
    return black_friday['User_ID'].nunique()
    #pass


# ## Questão 4
# 
# Quantos tipos de dados diferentes existem no dataset? Responda como um único escalar.

# In[17]:


def q4():
    # Retorne aqui o resultado da questão 4.
    return black_friday.dtypes.nunique()
    #pass


# ## Questão 5
# 
# Qual porcentagem dos registros possui ao menos um valor null (`None`, `ǸaN` etc)? Responda como um único escalar entre 0 e 1.

# In[18]:


def q5():
    # Retorne aqui o resultado da questão 5.
    return sum(black_friday.isna().any(axis=1))/len(black_friday)
    #pass


# ## Questão 6
# 
# Quantos valores null existem na variável (coluna) com o maior número de null? Responda como um único escalar.

# In[19]:


def q6():
    # Retorne aqui o resultado da questão 6.
    return max(black_friday.isna().sum())
    #pass


# ## Questão 7
# 
# Qual o valor mais frequente (sem contar nulls) em `Product_Category_3`? Responda como um único escalar.

# In[20]:


def q7():
    # Retorne aqui o resultado da questão 7.
    return black_friday["Product_Category_3"].value_counts().index[0]
    pass


# ## Questão 8
# 
# Qual a nova média da variável (coluna) `Purchase` após sua normalização? Responda como um único escalar.

# In[21]:


def q8():
    # Retorne aqui o resultado da questão 8.
#    from sklearn.preprocessing import MinMaxScaler
#    scaler = MinMaxScaler()
#    scaled = scaler.fit_transform(black_friday[['Purchase']].astype('float'))
    scaled = (black_friday['Purchase'] - black_friday['Purchase'].min())/(black_friday['Purchase'].max() - black_friday['Purchase'].min())
    return float(scaled.mean())
    #pass


# ## Questão 9
# 
# Quantas ocorrências entre -1 e 1 inclusive existem da variáel `Purchase` após sua padronização? Responda como um único escalar.

# In[22]:


def q9():
    # Retorne aqui o resultado da questão 9.
    #Quantas ocorrências entre -1 e 1 inclusive existem da variáel Purchase após sua padronização? Responda como um único escalar.
#    from sklearn.preprocessing import StandardScaler
#    stdscaler = StandardScaler().fit_transform(black_friday[['Purchase']])
#    return int((np.abs(stdscaler) <= 1).sum())
    return int((abs((black_friday['Purchase'] - black_friday['Purchase'].mean())/black_friday['Purchase'].std())<=1).sum())
    #pass


# ## Questão 10
# 
# Podemos afirmar que se uma observação é null em `Product_Category_2` ela também o é em `Product_Category_3`? Responda com um bool (`True`, `False`).

# In[23]:


def q10():
    # Retorne aqui o resultado da questão 10.
    return bool(
                    (
                        black_friday["Product_Category_2"].isna() == # retornar nulls de cat 2
                        (black_friday["Product_Category_2"].isna()) & (black_friday['Product_Category_3'].isna()) # retornar nulls de cat 2 e cat 3
                    ).all()
                )
    # pass

