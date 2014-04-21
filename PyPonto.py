#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#
#This file is part of PyPonto
#
#PyPonto is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#PyPonto is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with ProjectRisc.  If not, see <http://www.gnu.org/licenses/>.
#
#Copyright 2014 tadeucruz <contato@tadeucruz.com>
#

import pdb
import getopt
import sys
from time import gmtime, strftime
from datetime import datetime, timedelta, date

base = '.ponto-python'

#Var Global
DB = []
DATADIA = strftime("%d-%m-%Y", gmtime())

#Private
HORAIDE = ""
HORAIDS = ""
HORAIDSA = ""
HORAIDEA = ""
HORAEXTRA = ""
DATAF = ""
OPHORASAIR = 0

def salvarDB():
	#pdb.set_trace()
	DB.sort()
	f = open(base,'w+')
	for registro in DB:
		f.write(registro[0] + "|" + registro[1] + "|" + registro[2] + "|" + registro[3] + "|" + registro[4] + "|" + registro[5] + "|" + registro[6] + "\n")
	f.close()

def carregaDB():
	f = open(base,'r');
	for linha in f:
		DB.append(linha.strip().split('|'))
	f.close()
	DB.sort()

def insertDataDB(HORA,INDEX):
	for registro in DB: 
		if registro[1] == DATADIA:
			if registro[INDEX] != '':
				raise NameError('Data ja existente')
			else:
				registro[INDEX] = HORA
			return True 
	#Caso não ache o dia vai ser criado um novo registro.
	novaLinha = ['','','','','','','']
	tmp = DATADIA.split("-") 
	novaLinha[0] = date(int(tmp[2]),int(tmp[1]),int(tmp[0])).strftime("%s")
	novaLinha[1] = DATADIA
	novaLinha[INDEX] = HORA
	DB.append(novaLinha)

def insertDataEntradaDB(HORA): 
	try:
		insertDataDB(HORA,2)	
	except NameError, (erro):
		print str(erro) + " para entrada do dia " + DATADIA

def insertDataSaidaDB(HORA):
	if DATAF == "":
		tmp = datetime(datetime.now().year,datetime.now().month,datetime.now().day,0,0)
		volta = 1
		if tmp.weekday() == 0:
			volta = 3
		global DATADIA
		OLDDATADIA = DATADIA
		tmp = tmp - timedelta(weeks=0, days=volta, hours=0, minutes=0, seconds=0)
		DATADIA = tmp.strftime("%d-%m-%Y")
		try:
                	insertDataDB(HORA,5)
        	except NameError, (erro):
                	print str(erro) + " para saida do dia " + DATADIA
		DATADIA = OLDDATADIA
	else:
		try:
                        insertDataDB(HORA,5)
                except NameError, (erro):
                        print str(erro) + " para saida do dia " + DATADIA

def insertDataSaidaAlmocoDB(HORA):
        try:
                insertDataDB(HORA,3)
        except NameError, (erro):
                print str(erro) + " para saida para almoco do dia " + DATADIA

def insertDataEntradaAlmocoDB(HORA):
	try:
                insertDataDB(HORA,4)
        except NameError, (erro):
                print str(erro) + " para volta do almoco do dia " + DATADIA

def insertDataExtraDB(HORA):
        if DATAF == "":
                tmp = datetime(datetime.now().year,datetime.now().month,datetime.now().day,0,0)
                volta = 1
                if tmp.weekday() == 0:
                        volta = 3
                global DATADIA
                OLDDATADIA = DATADIA
                tmp = tmp - timedelta(weeks=0, days=volta, hours=0, minutes=0, seconds=0)
                DATADIA = tmp.strftime("%d-%m-%Y")
                try:
                        insertDataDB(HORA,6)
                except NameError, (erro):
                        print str(erro) + " para hora extra do dia " + DATADIA
                DATADIA = OLDDATADIA
        else:
                try:
                        insertDataDB(HORA,6)
                except NameError, (erro):
                        print str(erro) + " para hora extra do dia " + DATADIA


def subTempo(HORA1, HORA2):
	a = HORA1.split(":")
	SAIDAH=a[0]
	SAIDAM=a[1]
	a = HORA2.split(":")
	ENTRAH=a[0]
	ENTRAM=a[1]
	TMPH = int(ENTRAH) - int(SAIDAH)
	TMPH = TMPH * 60
	TMPM = int(ENTRAM) - int(SAIDAM)
	if (TMPM < 0 ):
		TMPM = TMPM * -1;
	if ( SAIDAM > ENTRAM ):
		TMP = TMPH - TMPM
	else:
		TMP = TMPH + TMPM

	if TMP > 0:
		RESULH = TMP / 60
		RESULM = TMP % 60
	else:
		RESULH = TMP / -60
		RESULH = RESULH * -1
		RESULM = TMP % -60

	if (len(str(RESULH)) < 2):
		RESULH = "0" + str(RESULH)
	if (len(str(RESULM)) < 2):
		RESULM = "0" + str(RESULM)
	return str(RESULH) + ":" + str(RESULM)

def sumTempo(HORA1, HORA2):
        a = HORA1.split(":")
        SAIDAH=a[0]
        SAIDAM=a[1]
        a = HORA2.split(":")
        ENTRAH=a[0]
        ENTRAM=a[1]
	TMPH = int(ENTRAH) + int(SAIDAH)
	TMPH = TMPH * 60
	if (ENTRAM < 0):
		ENTRAM = ENTRAM * -1
	if (SAIDAM < 0):
		SAIDAM = SAIDAM * -1
	TMPM = int(ENTRAM) + int(SAIDAM)
	TMP = TMPH + TMPM
	RESULH = TMP / 60
	RESULM = TMP % 60
	if len(str(RESULM)) < 2:
		RESULM = "0" + str(RESULM)
	if len(str(RESULH)) < 2:
		RESULH = "0" + str(RESULH)
	return str(RESULH) + ":" + str(RESULM)

def buscaDataDB(DATA,INDICE):
	saida = ""
        for registro in DB:
                if registro[1] == DATA:
                        try:
                                saida=registro[INDICE]
                        except IndexError:
                                saida=""
        return saida

def buscaDataEntradaBD(DATA):
	return buscaDataDB(DATA,2) 

def buscaDataSaidaBD(DATA):
	return buscaDataDB(DATA,5)

def buscaDataEntradaAlmocoBD(DATA):
        return buscaDataDB(DATA,4)

def buscaDataSaidaAlmocoBD(DATA):
        return buscaDataDB(DATA,3)

def buscaDataHoraExtra(DATA):
	return buscaDataDB(DATA,6)

def horaSair():
	HORAENTRADA = buscaDataEntradaBD(DATADIA)
	HORAALMOCOSAIDA = buscaDataSaidaAlmocoBD(DATADIA)
	HORAALMOCOENTRADA = buscaDataEntradaAlmocoBD(DATADIA)

	if HORAALMOCOSAIDA == "":
		HORAALMOCOSAIDA='12:00'
	if HORAALMOCOENTRADA == "":
		HORAALMOCOENTRADA='13:00'
	if HORAENTRADA == "":
		print "Ponto de entrada do dia " + DATADIA + " nao cadastrado"
		return "NaN"
	a = HORAENTRADA.split(":")
	SAIDAH = a[0]
	SAIDAM = a[1]
	SAIDAH = int(SAIDAH) + 8
	HORA = str(SAIDAH) + ":" + str(SAIDAM)

	TEMPO = subTempo(HORAALMOCOSAIDA,HORAALMOCOENTRADA)

	return sumTempo(HORA,str(TEMPO))	

def listaDias():
	volta = []
	for registro in DB:
		volta.append(registro[1])
	return volta

def horaTotalMes():
	#pdb.set_trace()
	num_resultado = 0
	TOTAL = "00:00"
	CONTROLE = "00:00"
	print "+------------+--------------+-------------------+---------------------+------------+----------+------------+"
	print "| Dia        | Hora entrada | Hora saida almoco | Hora entrada almoco | Hora saida | Hora Dia | Hora Extra |"
	print "+------------+--------------+-------------------+---------------------+------------+----------+------------+"

	#pdb.set_trace()	
	lista = listaDias()	

	for DATA in lista:
		#DATA = registro[1]
		HORAE = buscaDataEntradaBD(DATA)
		HORAS = buscaDataSaidaBD(DATA)
		HORAAE = buscaDataEntradaAlmocoBD(DATA)
		HORAAS = buscaDataSaidaAlmocoBD(DATA)
		HORASEXTRA = buscaDataHoraExtra(DATA)
		if HORAE == "":
			print "| "+DATA+" | Opa!!! Voce nao cadastrou hora de entrada para o dia: " + DATA + "               |"
			break
		if HORAS == "":
			#HORAS = horaSair()
			HORAS = "18:30"
		if HORAAE == "":
			HORAAE = "13:00"
		if HORAAS == "":
			HORAAS = "12:00"
		if HORASEXTRA == "":
			HORASEXTRA = "00:00"
		
		TMP1 = subTempo(HORAE,HORAS)
		TMP2 = subTempo(HORAAS,HORAAE)
		TMP = subTempo(TMP2,TMP1)
		TOTAL = sumTempo(TOTAL,TMP)
		TOTAL = sumTempo(TOTAL,HORASEXTRA)
		#pdb.set_trace()
		HORADIA = subTempo("08:00",TMP)
		
		if len(HORADIA) == 5:
			print "| " + DATA + " | " + HORAE + "        | " + HORAAS + "             | " + HORAAE + "               | " + HORAS + "      | " + HORADIA + "    | " + HORASEXTRA + "      |"
		else:
			print "| " + DATA + " | " + HORAE + "        | " + HORAAS + "             | " + HORAAE + "               | " + HORAS + "      | " + HORADIA + "   | " + HORASEXTRA + "      |"
		CONTROLE = sumTempo(CONTROLE,"08:00")
		HORADIA="00:00"
		num_resultado = num_resultado + 1

	print "+------------+--------------+-------------------+---------------------+------------+----------+------------+"
	print "Total: " + str(num_resultado)
	print "Hora total mes: " + TOTAL
	print "Horas para pagar ou extra: "  + subTempo(CONTROLE,TOTAL)

def PhoraTotalMes():
	TOTAL='00:00'
	CONTROLE='00:00'
	lista = listaDias()
	for DATA in lista:
		HORAE = buscaDataEntradaBD(DATA)
                HORAS = buscaDataSaidaBD(DATA)
                HORAAE = buscaDataEntradaAlmocoBD(DATA)
                HORAAS = buscaDataSaidaAlmocoBD(DATA)
		HORASEXTRA = buscaDataHoraExtra(DATA)
		if HORAE == "":
			HORAE = "09:30"
		if HORAS == "":
                        HORAS = horaSair()
                if HORAAE == "":
                        HORAAE = "13:00"
                if HORAAS == "":
                        HORAAS = "12:00"
		if HORASEXTRA == "":
                        HORASEXTRA = "00:00"

                TMP1 = subTempo(HORAE,HORAS)
                TMP2 = subTempo(HORAAS,HORAAE)
                TMP = subTempo(TMP2,TMP1)
                TOTAL = sumTempo(TOTAL,TMP)
		TOTAL = sumTempo(TOTAL,HORASEXTRA)
		CONTROLE = sumTempo(CONTROLE,"08:00")
		HORADIA="00:00"
	return subTempo(CONTROLE,TOTAL)	

def ajustaHora():
	RESULTADO = horaSair()
	HORA = PhoraTotalMes()
	return subTempo(HORA,RESULTADO)

def usage():
	print sys.argv[0] 
	print "-c cadastra hora de entrada"
        print "-s cadastra hora de saida"
        print "-a cadastra hora de saida do almoco"
        print "-v cadastra hora de entrada do almoco"
	print "-x cadastra hora extra"
        print "-y mostra a hora de sair"
        print "-r relatorio do de hora mensal"
        print "-f forcar uma data"
        print "-w fechar o ponto"

def parseOpcao():
	global HORAIDE 
	global HORAIDS
	global HORAIDSA
	global HORAIDEA
	global DATAF
	global OPHORASAIR
	global HORAEXTRA
	if len(sys.argv[1:]) == 0:
		usage();
	try:
		options, remainder = getopt.getopt(sys.argv[1:], ':s:c:a:v:i:f:t:x:yrw', )
	except getopt.GetoptError, (err):
		print str(err)
		sys.exit(2)
	
	for opt, arg in options:
		if opt in ('-c'):
			HORAIDE = arg
		elif opt in ('-s'):
			HORAIDS = arg
		elif opt in ('-a'):
			HORAIDSA = arg
		elif opt in ('-v'):
			HORAIDEA = arg
		elif opt in ('-f'):
			DATAF = arg
		elif opt in ('-y'):
			OPHORASAIR = 1
		elif opt in ('-r'):
			horaTotalMes()
		elif opt in ('-x'):
			HORAEXTRA = arg
			 

def main():
	global DATADIA
	#pdb.set_trace()
	carregaDB()
	parseOpcao()
	if DATAF != "":
		DATADIA = DATAF
	if HORAIDE != "":
		insertDataEntradaDB(HORAIDE)
	if HORAIDS != "":
		insertDataSaidaDB(HORAIDS)
	if HORAIDSA != "":
		insertDataSaidaAlmocoDB(HORAIDSA)
	if HORAIDEA != "":
		insertDataEntradaAlmocoDB(HORAIDEA)
	if HORAEXTRA != "":
		insertDataExtraDB(HORAEXTRA)
	if OPHORASAIR == 1:
		print "Horario de sair: " + horaSair()  
		print "Horario de sair ajustado: "+ ajustaHora()
	salvarDB()


if __name__ == "__main__":
    main()

