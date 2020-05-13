print("Importando bibliotecas python ...")
import sys
import requests
import pandas as pd
import datetime
import numpy as np
import psycopg2
import json

print("Conectando com BD Postgresql ...")
connection = psycopg2.connect(user=u1,
                                password=p1,
                                host=h1,
                                port=pt1,
                                database=d1)
Estat3 = connection.cursor()

print("Conectando com BD MySQL ...")
#CONNECTIONS!!!!!!!!!!!!!!!!!!!

##### MARIADB #####
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

db = MySQLdb.connect(host=h2,    # your host, usually localhost
                     user=u2,         # your username
                     passwd=p2,  # your password
                     db=d2)        # name of the data base
Painel = db.cursor()

sql = sqlquery1

print("Executando Query 1 de 2 ...")
Painel.execute(sql)
table_rows = Painel.fetchall() 
dfx = pd.DataFrame(list(table_rows))
data = pd.DataFrame()
data = dfx#.T
data.columns = [desc[0] for desc in Painel.description]
GoomerGo = data
GoomerGo.Num_produtos = GoomerGo.Num_produtos.fillna(0)
GoomerGo["data_criacao"] = GoomerGo.estab_createdat.dt.date
GGo = GoomerGo.loc[(GoomerGo.Tipo_de_Licenca == "goomer_go") & (GoomerGo.estab_createdat >= "2020-01-01 00:00:00")]
Cadastro_tl = pd.DataFrame(GGo.groupby("data_criacao").Nome_do_estabelecimento.count())

#Banco de dados de pedidos do GoomerGo
postgreSQL_select_Query = sqlquery2

print("Executando Query 2 de 2 ...")
Estat3.execute(postgreSQL_select_Query)
table_rows = Estat3.fetchall() 
dfx = pd.DataFrame(table_rows)
data = pd.DataFrame()
data = dfx#.T
data.columns = [desc[0] for desc in Estat3.description]
Pedidos = data
Pedidos.total_value = pd.to_numeric(Pedidos.total_value)
#Pedidos.faturamento = pd.to_numeric(Pedidos.faturamento)

#dataset1 = Pedidos
#dataset1.set_index('establishment_id', inplace = True)

print("Montando tabela de metricas ...")

Pedidos["data_norm"] = Pedidos.enviado_em.dt.date
Pedidos_idx = Pedidos[Pedidos.establishment_id.isin(GGo.id.unique())].sort_values("enviado_em").reset_index()
Ativos_tl = pd.DataFrame(pd.DataFrame(Pedidos_idx.groupby("establishment_id").enviado_em.nth(7).dt.date).reset_index().groupby("enviado_em").establishment_id.count())

Nro_Pedidos = pd.DataFrame(Pedidos.groupby("data_norm").establishment_id.count())

Faturamento = pd.DataFrame(Pedidos.groupby("data_norm").total_value.sum())

M = pd.concat([Cadastro_tl, Ativos_tl, Nro_Pedidos, Faturamento],axis = 1, sort=False)
M.columns = ["Cadastros", "Ativos", "Pedidos", "Faturamento"]
print("Salvando csv ...")
import os
pathname = os.path.dirname(sys.argv[0])        
print('Arquivo csv sera salvo em > ', os.path.abspath(pathname)) 
M.to_csv("GoomerGo_metrics.csv")

print("Pronto!")
