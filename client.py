#Questa è la libreria che contiene tutto quello che può servire quando si usano le socket
#Generalmente dovrebbe essere importata in automatico quando si usa una sua funzione
import socket

serverIP="127.0.0.1" #Indirizzo IP del server, lo imposto di default al localhost
serverPorta=8080 #Porta del server, lo imposto di default al 8080
server =(serverIP,serverPorta) #Tupla di indirizzo IP e porta del server

#Funzione che gestisce l'invio dei messaggi, mi passo come parametro la socket creata 
#dalla funzione connesioneServer, così posso usarla e non devo fare una nuova connesione
def inviaMessaggio(s):
    
    #Dato che devo continuare ad inviare finchè non viene esplicitamente detto faccio
    #un ciclo infinito
    while True:
        
        #Prendo in input il messaggio da inviare
        messaggio = input("Inserisci il tuo messaggio: ")
        
        if messaggio == "exit": #Se il messaggio è exit esco dal ciclo
            break
        
        #Invio il messaggio usando la funzione send() della socket s passando come 
        #parametro il messaggio
        else:
            
            #Uso il metodo send della socket s, usando un encode (devo assicurarmi 
            #che il messagio sia nello stesso formato sia dal client che dal server,
            # per esempio non posso mandare un messagio in cirillico e aspettarmi che il 
            # server che lavora con i caratteri italiani lo capisca)
            #di default Python lavora con codifica UTF-8
            s.send(messaggio.encode())
            
            #Usando il metodo rcv della socket ricevo la risposta del server e la metto dentro data
            #Limito la ricezione a 4096 byte per non creare troppo traffico
            data = s.recv(4096)
            
            #Stampo la risposta decodificandola in UTF-8 (Default di Python).
            print(data.decode())
                
def connessioneServer():
    #Tento la connessione
    try:
        #creo una socket di nome s usando il metodo socket() della libreria socket
        s = socket.socket()
        
        #Connesione al server usando il metodo connect() della socket s
        s.connect(server)
        print(f"Connesso al server {serverIP}:{serverPorta}")
    
    #Se la connesione non riuscisse l'errore sarebbe contenuto in socket.error, lo catturo
    #e lo metto dentro la variabile errore
    except socket.error as errore:
        print(f"Impossibile connettersi al server {serverIP}:{serverPorta}")
        #Stampo l'errore
        print(errore)
        exit()
    
    #Se tutto va bene e la connesione è stabilita invio i messaggi usando la funzione inviaMessagio
    #passando come parametro la socket creata (s)    
    inviaMessaggio(s)


#Come main choamo la funzione connesioneServer  
if __name__ == "__main__":
    connessioneServer()
    