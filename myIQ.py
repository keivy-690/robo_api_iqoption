from iqoptionapi.stable_api import IQ_Option
import time, json
from datetime import datetime
from dateutil import tz
#foi excluida a linha de importação de e-mail e senha.



print('Aguarde enquanto o login está sendo feito...')
API = IQ_Option(email, senha) #coloque seu email e senha. Ex: "fulano@gmail.com","minhasenha"
API.connect()
while True:
	if API.check_connect() == False:
		print('Erro ao se conectar')
		API.connect()
	else:
		print('Conectado!')#sucesso na conexão
		break
	
	time.sleep(1)

changeB = input("Pratica ou Real? 1- Pratica 2- Real:") 
if changeB == '1':
    changeBs = 'PRACTICE'
elif changeB == '2':
    changeBs = 'REAL'
    
API.change_balance(changeBs) # Vai usar dinheiro FICTICIO OU REAL = PRACTICE / REAL

global valorPR
valorPR = input("Escolha o valor de aposta (Minimo pratica-1 Minimo para real-2): ")


vitoria = 0
vitoriaV = 0
perda = 0
perdaV = 0

# Para pegar de apenas uma paridade #################


# AQUI É AONDE A FUNÇÃO FAZ APOSTAR PRA SUBIR - OPÇÃO BINARIO!
def apostarSubir():
    #par="AUDUSD"
    duration=1#minute 1 or 5 
    amount=valorPR
    action="call"#put
    
    _,id=API.buy(amount,par,action,duration)
    while API.get_async_order(id)==None:
        pass
    #print(API.get_async_order(id))
    print("__BINARIO_APOSTOU_SUBIR__")
    print('Meu id:', id)
    print(API.check_win_v3(id))
    if 'win' in API.check_win_v3(id):
        #print(API.check_win_v3(id)) $apareceu 2 pq deixei esse ativo, so vai aceitar a alteracao quando eu parar o robo
        print('ganhou!')
        time.sleep(10) # ESPERA 10 SEGUNDOS
        humorT()
    elif 'loose' in API.check_win_v3(id):
        print('perdeu :(')
        time.sleep(10)
        humorT()
    elif 'equal' in API.check_win_v3(id):
        print('EMPATE - Robô parado')
        pausar()
    
# AQUI É AONDE A FUNÇÃO FAZ APOSTAR PRA DESCER - OPÇÃO BINARIO!
def apostarDescer():
    #par="AUDUSD"
    duration=1#minute 1 or 5
    amount=valorPR
    action="put"#put

    
    _,id=API.buy(amount,par,action,duration)
    while API.get_async_order(id)==None:
        pass
    #print(API.get_async_order(id))
    print("__BINARIO_APOSTOU_DESCER__")
    print('Meu id:', id)
    print(API.check_win_v3(id))
    if 'win' in API.check_win_v3(id):
        print('ganhou!')
        time.sleep(10)
        humorT()
    elif 'loose' in API.check_win_v3(id):
        print('perdeu :(')
        time.sleep(10)
        humorT()
    elif 'equal' in API.check_win_v3(id):
        print('EMPATE - Robô parado')
        pausar()
   
# AQUI É AONDE A FUNÇÃO FAZ APOSTAR PRA SUBIR - OPÇÃO DIGITAL!
def apostarSubirD():
    #par="AUDUSD"
    duration=1#minute 1 or 5
    amount=valorPR
    action="call"#put
    
    global vitoria
    global vitoriaV
    global perda
    global perdaV
    
    liquidoD = vitoria - perda
    liquidoVD = vitoriaV - perdaV
    
    if liquidoD <= (-3):
        PerdaD = input("Vc ja ta perdendo R$ "+str(liquidoVD)+", deseja continuar? 1-Não   2-Sim: ")
        if PerdaD == '1':
            pausar()
        elif PerdaD == '2': 
            perda = 0
            BinDig()
            
    _,id=(API.buy_digital_spot(par,amount,action,duration))
    if 'expiration_out_of_schedule' in str(id):
        print('Expirado para aposta, redirecionando...')
        humorT()
    print(id)
    print("__DIGITAL__")
    if id !="error":
        while True:
            check,win=API.check_win_digital_v2(id)
            if check==True:
                break
        if win<0:
            perda += 1
            perdaV += win
            print("Você perdeu "+str(win)+"$")
            time.sleep(180)
        else:
            vitoria += 1
            vitoriaV += win
            print("Você ganhou "+str(win)+"$")
            time.sleep(60)
    
    else:
        print('EMPATE - Robô parado')
        pausar()
    
    humorT()

# AQUI É AONDE A FUNÇÃO FAZ APOSTAR PRA DESCER - OPÇÃO DIGITAL!
def apostarDescerD():
    #par="AUDUSD"
    duration=1#minute 1 or 5
    amount=valorPR
    action="put"#call 
    global vitoria
    global vitoriaV
    global perda
    global perdaV
    
    liquidoD = vitoria - perda
    liquidoVD = vitoriaV - perdaV
    
    if liquidoD <= (-3):#SE VC PERDER 3 SEGUIDAS O ROBO DA UMA PARADA E PERGUNTA SE DESEJA CONTINUAR
        PerdaD = input("Vc ja ta perdendo R$ "+str(liquidoVD)+", deseja continuar? 1-Não   2-Sim: ")
        if PerdaD == '1':
            pausar()
        elif PerdaD == '2': 
            perda = 0
            BinDig()    
    
    _,id=(API.buy_digital_spot(par,amount,action,duration))
    if 'expiration_out_of_schedule' in str(id):
        print('Expirado para aposta, redirecionando...')
        humorT()
    print(id)
    print("__DIGITAL__")
    if id !="error":
        while True:
            check,win=API.check_win_digital_v2(id)
            if check==True:
                break
        if win<0:
            perda += 1
            perdaV += win
            print("Você perdeu "+str(win)+"$")
            time.sleep(180) #TIME DE 180 SEGUNDOS
        else:
            vitoria += 1
            vitoriaV += win
            print("Você ganhou "+str(win)+"$")
            time.sleep(60)
    
    else:
        print('EMPATE - Robô parado')
        pausar()
    
    humorT()


def BinDig(): #ESCOLHA A OPÇÃO, BINARIA OU DIGITAL
    OptionBD = input("Binaria ou Digital? 1- Binaria 2- Digital:") 
    global par 
    if OptionBD == '1':  
        OptionBx = input("Escolha a opção Binaria: 1-USD/CAD 2-EUR/USD 3-AUD/USD 4-AUD/JPY 5-EUR/AUD 6-CAD/JPY 7-EUR/NZD 8-EURJPY 9-NZD/USD-OTC 10-EUR/JPY-OTC 11-AUD/CAD-OTC 12- EUR/USD-OTC 13-EUR/GBP-OTC: ")
        if OptionBx == '1':
            parX = 'USDCAD'
        elif OptionBx == '2':
            parX = 'EURUSD'
        elif OptionBx == '3':
            parX = 'AUDUSD'
        elif OptionBx == '4':
            parX = 'AUDJPY'
        elif OptionBx == '5':
            parX = 'EURAUD'
        elif OptionBx == '6':
            parX = 'CADJPY'
        elif OptionBx == '7':
            parX = 'EURNZD' 
        elif OptionBx == '8':
            parX = 'EURJPY'
        elif OptionBx == '9':
            parX = 'NZDUSD-OTC'
        elif OptionBx == '10':
            parX = 'EURJPY-OTC' 
        elif OptionBx == '11':
            parX = 'AUDCAD-OTC' 
        elif OptionBx == '12':
            parX = 'EURUSD-OTC'  
        elif OptionBx == '13':
            parX = 'EURGBP-OTC'             
         
        par = parX
        print('Voce selecinou a opção:'+OptionBx+'-'+par)
        humorT()
    elif OptionBD == '2':  
        OptionBx = input("Escolha a opção Digital: 1-USD/CAD 2-EUR/USD 3-AUD/CAD 4-AUD/JPY 5-EUR/AUD 6-EUR/GBP 7-GBP/USD 8-GBP/JPY 9-EUR/USD-OTC 10-EUR/JPY-OTC 11-AUD/CAD-OTC: ")
        if OptionBx == '1':
            parX = 'USDCAD'
        elif OptionBx == '2':
            parX = 'EURUSD'
        elif OptionBx == '3':
            parX = 'AUDCAD'
        elif OptionBx == '4':
            parX = 'AUDJPY'
        elif OptionBx == '5':
            parX = 'EURAUD'
        elif OptionBx == '6':
            parX = 'EURGBP'
        elif OptionBx == '7':
            parX = 'GBPUSD' 
        elif OptionBx == '8':
            parX = 'GBPJPY' 
        elif OptionBx == '9':
            parX = 'EURUSD-OTC'
        elif OptionBx == '10':
            parX = 'EURJPY-OTC' 
        elif OptionBx == '11':
            parX = 'AUDCAD-OTC'
        
        par = parX
        print('Voce selecinou a opção:'+OptionBx+'-'+par)
        print('Calculando as probabilidades...Aguarde.')
        humorT()
    

def humorT():      # AQUI SELECIONA O HUMOR
    print('Calculando probabilidades...Aguarde.')
    API.start_mood_stream(par)

    while True:
        x = API.get_traders_mood(par)
        #print(int(100 * round(x, 2)))
        
        if int(100 * round(x, 2)) > 60 :            #SE o humor TIVER ACIMA DE 60 ELE APOSTA PRA SUBIR
            apostarSubir()
            
        elif int(100 * round(x, 2)) < 50 : #SE TIVER ABAIXO DE 50 ELE APOSTA PRA DESCER
            print("APOSTADO PRA DESCER!")
            apostarDescer()
                
        time.sleep(1)


    print("\n\n")
    API.stop_mood_stream(par)
    


def pausar():
    pausado = input("Programa pausado, deseja continuar? 1- Sim 2- Não:")
    if pausado == '1':
        BinDig()
    elif pausado == '2':
        print('Obrigado pelo uso do robô, pode fechar o programa :-)')

BinDig()





