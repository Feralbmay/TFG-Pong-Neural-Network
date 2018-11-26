# TFG-Pong-Neural-Network
Repositori del TFG del Joc del pong amb una Xarxa Neuronal

# Primera Versio (Pong Simple):
Creacio del Joc del Pong, basat en el video de Youtube de Sirajology.
Inclusio de una xarxa Neuronal, sense aprenentatge, amb 12 imputs i 3 outputs.

Instalació:
* numpy
* random
* pygame

##Execució:

```
python main.py
```
# Segona Versio (Pong Simple generacions):
Creacio del Joc del Pong, basat en el video de Youtube de Sirajology.
Inclusio de 50 xarxes Neuronals, sense aprenentatge, amb 12 imputs i 3 outputs.
Les xarxes nomes funcionen fins a que perden(deixen pasar la pilota). 
Es generen altres 50 noves, filles de la generacio anterior, fins que s'aconseguixi una xarxa 
que copegui la pilota 20 pics seguits.

Instalació:
* numpy
* random
* pygame

##Execució:

```
python main.py
```

# Segona Versio per extraccio de dades(Pong Simple generacions Probes)
Modificacio de la versio anterior, per a poder extraeure dades de diferents configuracions alhora.
La versio extreu dades de la convinacio del següents imputs(la posicio actual de la pilota i la paleta(4), la posicio actual de la pilota, les dues anteriors i la posicio actual de la paleta(8) i la posicio actual de la pilota, les cuatre anteriors i la posicio actual de la paleta(12)
