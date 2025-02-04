#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from json import JSONEncoder
import configparser

from DtoYoisen import DtoYoisen
import sys
import requests
import logging
import os
from asterisk.agi import AGI
 

def main():

    agi = AGI()

    agi.verbose("Start AGI Joysen Script", 1)
    agi.set_variable("RESULT", "NADA")

    dataConfig = configparser.ConfigParser()
    dataConfig.read("/opt/asterisk/rest_call.ini")

    url = dataConfig["General"]["URL"]
    logFileName = dataConfig["General"]["logFile"]

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename=logFileName, encoding='utf-8', level=logging.DEBUG)
    logger.info("Iniciando Logger")
    logger.info("URL: " + url)

    serviceId= int(dataConfig["YoisenRequest"]["serviceId"])
    hsmElementName=dataConfig["HSM"]["hsmElementName"]
    hsmNamespace=dataConfig["HSM"]["hsmNamespace"]
    hsmLanguage=dataConfig["HSM"]["hsmLanguage"]
    hsmBodyParam1=dataConfig["HSM"]["hsmBodyParam1"] 
    hsmBodyParam2=dataConfig["HSM"]["hsmBodyParam2"] 
    header=dataConfig["YoisenRequest"]["Headers"]
    bearerToken=dataConfig["YoisenRequest"]["token"]
    logger.debug("Header :"+ header)

    # Get variable environment
    #extension = agi.env['agi_extension']
    #logger.debug("Extension :"+ extension)

    # Get variable in dialplan
    #phone_exten = agi.get_variable('PHONE_EXTEN')
    #logger.debug("Phone Extension :"+ phone_exten)

    caller_id = sys.argv[1] 
    #caller_id = "1125559999"
    if len(caller_id) == 10:
        caller_id = "549" + caller_id
    elif len(caller_id) < 10:
        logger.info("Numero Telefonico Incorrecto: " + caller_id)
        agi.set_variable('RESULT', 'Incorrect Telephone Number')
        # print(f'SET VARIABLE "RESULT" "FAILED"')
        sys.exit(2)

    jsonResquest = DtoYoisen()
    jsonBody= jsonResquest.get_model_hsm_without_buttons_and_tags(serviceId,
                          caller_id,
                          "null",
                          hsmElementName,
                          hsmNamespace,
                          hsmLanguage,
                          "null",
                          hsmBodyParam1,
                          hsmBodyParam2)

    logger.debug("JSON :"+ jsonBody)
   
    headers = {
    'Authorization': f'Bearer {bearerToken}',
    'Content-Type': f'{header}'
    }
    #logger.debug("Headers: " + headers)

    logger.info("Ejecutando: REST con ANI: " + caller_id)
    response = requests.post(url, data=jsonBody, headers = headers)
    logger.info("REST ejecutado para ANI: " + caller_id)
    if response.status_code == 200:
        logger.info('Success: ' + str(response.status_code))
        agi.set_variable('RESULT', 'SUCCESS')
        # print(f'SET VARIABLE "RESULT" "SUCCESS"')
        sys.exit(0)       # Código de salida 0
    elif response.status_code in (500,502,503,504):
        logger.info('Error en el servicio REST. Status Code: ' +  str(response.status_code))
        logger.info('Reintentando Ejecucion REST Service Caller ID: ' +  caller_id)
        response = requests.post(url, data=jsonBody, headers = headers)
        if response.status_code == 200:
            logger.info('Reintento Existoso. Status Code: ' + str(response.status_code))
            agi.set_variable('RESULT', 'SUCCESS')
            # print(f'SET VARIABLE "RESULT" "SUCCESS"')
            sys.exit(0)       # Código de salida 0
        else:
            logger.info('Error en el reintento al servicio REST. Status Code: ' +  str(response.status_code))
            agi.set_variable('RESULT', 'FAILED')
            sys.exit(1)       # Código de salida 1           
    else:
        logger.info('Error en el servicion REST. Status Code: ' +  str(response.status_code))
        agi.set_variable('RESULT', 'FAILED')
        # print(f'SET VARIABLE "RESULT" "FAILED"')
        sys.exit(1)       # Código de salida 1

if __name__ == "__main__":
    main()
