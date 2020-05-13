from automagica import *

# Opening scripts to get data from databases by SQL and Posgresql queries
display_osd_message(message='Atualizando csv', seconds=5)
press_key_combination('win', 'r')
task = r'C:\filepath\ScriptName.py'
set_to_clipboard(task)
press_key("backspace")
press_key_combination('ctrl', 'v')
press_key("enter")
wait(seconds = 5)
#Waiting script to finish
display_osd_message(message='30 segundos', seconds=5)
wait(seconds = 5)
display_osd_message(message='25 segundos', seconds=5)
wait(seconds = 5)
display_osd_message(message='20 segundos', seconds=5)
wait(seconds = 5)
display_osd_message(message='15 segundos', seconds=5)
wait(seconds = 5)
display_osd_message(message='10 segundos', seconds=5)
wait(seconds = 5)
display_osd_message(message='05 segundos', seconds=5)
wait(seconds = 5)

#Open Google Chrome and access google sheetspread
display_osd_message(message='Abrindo o Google Sheets no Chrome', seconds=5)
press_key_combination('win', 'r')
press_key("backspace")
typing("chrome", clear=True, interval_seconds=0.01)
press_key('enter')
click(x=147, y=83, delay=0.5)
#click(x=990, y=50, delay=1)
#get_from_clipboard()
press_key('enter')
wait(seconds = 10)
click(x=95, y=150, delay=1)
click(x=120, y=300, delay=1)
click(x=700, y=225, delay=1)

#Importing new csv file
display_osd_message(message='Exportando arquivo csv atualizado', seconds=5)
click(x=688, y=455, delay=1)
path = r'C:\filepath'
set_to_clipboard(path)
click(x=825, y=200, delay=1)
press_key("backspace")
press_key_combination('ctrl', 'v')
press_key('enter')
click(x=631, y=596, delay=1)
typing("filename.csv", clear=True, interval_seconds=0.01)

#Transforming data in source spreadsheet
display_osd_message(message='Formatando dados', seconds=5)
click(x=955, y=627, delay=1)
wait(seconds = 10)
click(x=545, y=327, delay=1)
click(x=545, y=624, delay=1)
click(x=637, y=675, delay=1)
press_key_combination('ctrl', 'a')
wait(seconds = 1)
press_key_combination('ctrl', 'h')
wait(seconds = 1)
typing(".", clear=True, interval_seconds=0.01)
press_key('tab')
typing(",", clear=True, interval_seconds=0.01)
click(x=740, y=625, delay=2)
click(x=890, y=625, delay=1)
press_key_combination('ctrl', 'a')
click(x=360, y=184, delay=1)
click(x=360, y=300, delay=1)
click(x=92, y=240, delay=1)
click(x=360, y=184, delay=1)
click(x=645, y=722, delay=1)
click(x=408, y=712, delay=1)
display_osd_message(message='Finalizado', seconds=5)
press_key_combination('ctrl', 'w')
