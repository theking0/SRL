# SRL

## Descrizione
Analizza la rete locale per cercare dispositivi con servizi aperti e rangiungibili da remoto (es. ipcam, router ecc.).


- `Ricava la terna della rete locale in base all'ip del gateway sulla scheda di rete (di default).`
- `Scansiona l'intera terna (0/255) cercando ip con la porta 80 aperta.`
- `Su ogni ip che trova dai passaggi precedenti effettua un port scan sul range 0/9999.`
- `Verifica accessibilità sulle porte http e rtsp.`
- `Ricoscimento nomi servizi tcp.`


Molto veloce negli scan grazie al multi-threading, arriva a scansionare **2.549.745** porte, suddivise in 255 ip.. **in meno di 30 secondi**.
tutto in un singolo script python o file eseguibile Windows. 

[Download eseguibile windows](https://github.com/theking0/SRL/releases/download/untagged-7730d8725eae5197d0a6/localScan.exe)

## SCREENSHOT

![Cattura](https://user-images.githubusercontent.com/583775/186486424-6f12fdb4-efe8-4134-a761-fe7776445c76.JPG)
