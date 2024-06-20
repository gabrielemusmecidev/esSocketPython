#Questa è la libreria che contiene tutto quello che può servire quando si usano le socket
#Generalmente dovrebbe essere importata in automatico quando si usa una sua funzione
import socket


serverIP="127.0.0.1" #Indirizzo IP del server, lo imposto di default al localhost
serverPorta=8080 #Porta del server, lo imposto di default al 8080
server =(serverIP,serverPorta) #Tupla di indirizzo IP e porta del server
nconnessione=1 #Numero di richieste di connessione contemporanee, generalmente si mette a 5 ma essendo un esercizio meramente
#didattico lo lascio a 1 

#Funzione che si occupa della ricezione dei dati, passo come parametro la socket creata dal metodo accept() in avvioServer
def RiceviMessaggi(conn):

    #Ciclo infinito perchè voglio continuare a ricevere i messaggi finchè la connessione è attiva
    while True:
        
        #Leggo il messaggio e lo metto dentro la variabile messaggio, accetto 1024 bytes di dati alla volta
        messaggio = conn.recv(1024)
        
        #Se il messaggio è vuoto, ad esempio il client si è disconnesso senza mandare il messaggio "exit"
        if not messaggio:
            print("Client disconnesso in maniera inattesa")
            break
        
        #Se il messaggio è pieno invece lo decodifico, la codifica standard di Python è utf-8
        messaggio_decodificato = messaggio.decode()
        
        if messaggio_decodificato == "exit":
            print("Client disconnesso")
            break
        
        #Stampo il messaggio ricevuto
        print("Messaggio ricevuto: "+messaggio_decodificato)
        
        #Preparo la risposta al client della riuscito invio
        data = f"Messaggio ricevuto{messaggio_decodificato} "
        
        #Mando al client la risposta, codificandola in utf-8
        conn.sendall(data.encode())
        

def avvioServer():
    
    #Tento la connessione
    try:
        
        #Creo la socket
        s = socket.socket()
        
        #"Lego" la socket al server
        s.bind(server)
        
        #Metto di ascolto la socket
        s.listen(nconnessione)
        
        print("In attesa di connessioni...")
        
    #Se la connessione non riuscisse l'errore sarebbe contenuto in socket.error, lo catturo
    #e lo metto dentro la variabile errore
    except socket.error as errore:
        print("Si è verificato un errore: "+str(errore))
        print("Riavvio il server...")

        #Riprovo a far partire il server, per farlo richiamo dentro se stessa la funzione avvioServer, in questa maniera si
        #crea un ciclo infinito che continua finchè il server non si avvia. Per evitare un loop infinito in caso di un errore specifico
        #Potrei mettere un contatore per eseguire il ciclo un numero definito di volte
        avvioServer()
    
    #Se la connessione riuscisse, allora continuo
    
    #Accetto le richieste di connessione
    #conn equivale ad una nuova socket usabile per inviare e ricevere i dati, il principio è simile a quello del token - refresh token
    #indirizzo_client invece contiene l'indirizzo ip del client
    conn, indirizzo_client = s.accept()
    print("Connessione accettata da: "+str(indirizzo_client))

    #Chiamo la funzione per ricevere i messaggi
    RiceviMessaggi(conn)
    
    
    
if __name__ == "__main__":
    avvioServer()