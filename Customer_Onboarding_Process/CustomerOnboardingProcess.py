authtoken = "X"
import requests
import json
import pandas as pd

# API connection PowerBI - Pipefy ==============
url = "https://api.pipefy.com/graphql"
query = "{organization(id: "+ str(314358) + ") {name pipes{id name phases {name cards_count}}}}"
payload = "{\"query\":\"" + query + "\"}"
headers = {
    'authorization': "Bearer " + authtoken, # authtoken = Pipefy authorization token
    'content-type': "application/json"
    }
response = requests.request("POST", url, data=payload, headers=headers)
JsonPipeFy = json.loads(response.text)

# Converting json data into Pandas structure
Pipe = [] # Pipeline's name
Phase = [] # Phase's name
NumCli = [] # Number of customers in respectively phases
phase_id = [] # Phase id - used for table connection 
for x in JsonPipeFy['data']['organization']['pipes']:
  for i in x['phases']:
    Pipe.append(x['name'])  
    Phase.append(i['name'])
    NumCli.append(i['cards_count'])
    phase_id.append(x['id'])

dict = {'Pipe': Pipe, 'Phase': Phase, 'NumCli': NumCli, 'Phase_Id': phase_id}
dfx = pd.DataFrame(dict)
dfx.NumCli = dfx.NumCli.astype(str).astype(int)

# Avoiding data that do not need in dashboard
Gestao_filter = (dfx["Phase"].str.contains('I  - TFV')== False) & (dfx["Phase"].str.contains('Passado para GV')== False)
Canais_filter = (dfx["Phase"].str.contains('H - Aguardar Dia G')== False) & (dfx["Phase"].str.contains('I - Enviar Feedback e Solicitar NF')== False) & (dfx["Phase"].str.contains('J - Aguardar NF')== False) & (dfx["Phase"].str.contains('K - Enviar Comprovante de Pagamento')== False) & (dfx["Phase"].str.contains('L - Processo Finalizado')== False)  & (dfx["Phase"].str.contains('M - Sem Integração')== False) & (dfx["Phase"].str.contains('H - Dia G')== False) 
General_filter = (dfx["Phase"].str.contains('Cancela') == False)
Exec_filter = (dfx["Phase"].str.contains('D - FUP pós dia G') == False) & (dfx["Phase"].str.contains('E - Concluído') == False)
Cardapio_filter = (dfx["Phase"].str.contains('Implementação feita') == False)
IDV_filter = (dfx["Phase"].str.contains('Implementação feita') == False)
Logistica_filter = (dfx["Phase"].str.contains('Implementação feita') == False)
Operacao_filter = (dfx["Phase"].str.contains('Implementação feita') == False)
Tablet_filter = (dfx["Phase"].str.contains('Implementação feita') == False)

# Applying filters
Phase_Filter = (Exec_filter) & (General_filter) & (Canais_filter) & (Gestao_filter) & (Cardapio_filter) & (IDV_filter) & (Logistica_filter) & (Operacao_filter) & (Tablet_filter)
df = dfx[(dfx["Pipe"].str.contains('[IMP]') == True) & (dfx["Pipe"].str.contains('Impedit') == False) & (Phase_Filter)]

# Calculating scores
# Scores
v_Pipename = []
v_ScorePipe = []
for i in df.Pipe.unique():

  w1 = 1 # Phase Weight increases as customer goes through phases
  ScorePhase = 0 # Score Phase = Number of customer * Phase Weight 
  ScorePhaseSum = 0 # Pipe Score = ScorePhaseSum = sum (ScorePhase)

  for j in df[(df.Pipe == i)].Phase.unique():
    ScorePhase = (float(df[(df.Pipe == i) & (df.Phase == j)].NumCli)*w1)
    ScorePhaseSum = ScorePhaseSum + ScorePhase
    w1 = w1 +1
  ScorePipe = ScorePhaseSum/(df[(df.Pipe == i)].NumCli.sum()*(w1-1))
  v_Pipename.append(i)
  v_ScorePipe.append(ScorePipe)

dict = {'Pipename': v_Pipename, 'ScorePipe': v_ScorePipe}
df_score = pd.DataFrame(dict) # Pipe Score for all the parallel process
IMP_score = df_score.ScorePipe.mean() 

dict = {"Score_Geral": float(str(IMP_score))}
df_IMPscore = pd.DataFrame([dict]) # Department score

phase_id_vector = df.Phase_Id.unique()

# Manipulating data for 360º view for each customer
Pipe_id = [] # Pipe id to connect tables in PowerBI
Phase_name = [] # Phase name
CustomerName = [] # Customer Name 
for i in range(0,len(phase_id_vector)):
  query = "{allCards(pipeId: "+str(phase_id_vector[i]) +"){edges {node {id title current_phase {name}}}}}"
  payload = "{\"query\":\"" + query + "\"}"
  response = requests.request("POST", url, data=payload, headers=headers)
  JsonPipeFy = json.loads(response.text)
  #print(response.text)

  for x in range(0,len(JsonPipeFy['data']['allCards']['edges'])):
    Pipe_id.append(phase_id_vector[i])
    Phase_name.append(JsonPipeFy['data']['allCards']['edges'][x]['node']['current_phase']['name'])
    CustomerName.append(JsonPipeFy['data']['allCards']['edges'][x]['node']['title'])

dict = {'Pipe_id': Pipe_id, 'Phase_name': Phase_name, 'Customer_Name': CustomerName}
df2 = pd.DataFrame(dict) # 360º view matrix
