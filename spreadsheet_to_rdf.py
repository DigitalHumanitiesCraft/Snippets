from __future__ import print_function

import os.path
from unittest import FunctionTestCase

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

#importing rdf and panda
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS, RDF, RDFS, SKOS, XSD, SDO, FOAF, VOID, DC, OWL
import pandas as pd
import urllib
import unidecode
from datetime import date

######

# normalize and prettify uri
def normalize_prettify_uri(string):
  string = string.replace(" ", "")
  string = string.replace("/", "_")
  string = string.replace(",", "_")
  string = unidecode.unidecode(string)
  string = urllib.parse.quote(string)

  return string 


########################################################################################
# normalize string (remove whitespaces, line breaks, tabs and make valid json)
def normalize_string_for_JSON(string):
    string = string.replace("\n", " ")
    string = string.replace("\t", " ")
    string = string.replace('"', '\\"')
    string = " ".join(string.split())
    return string



#generating a graph
result_graph = Graph()
#
verfied_dict = {}


#creating namespaces and prefixes in rdf
VOID = Namespace("http://rdfs.org/ns/void#")
DCTERMS = Namespace("http://purl.org/dc/terms/")
DC = Namespace("http://purl.org/dc/elements/1.1/")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
EXIL = Namespace("https://gams.uni-graz.at/o:exil.ontology#")
OWL = Namespace("http://www.w3.org/2002/07/owl#")
SDO = Namespace("https://schema.org/")
GAMS = Namespace("https://gams.uni-graz.at/o:gams-ontology#")
WDT = Namespace("http://www.wikidata.org/prop/direct/")
GEO = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")


result_graph.bind("void", VOID)
result_graph.bind("schema", SDO)
result_graph.bind("dcterms", DCTERMS)
result_graph.bind("dc", DC)
result_graph.bind("foaf", FOAF)
result_graph.bind("rdfs", RDFS)
result_graph.bind("xsd", XSD)
result_graph.bind("skos", SKOS)
result_graph.bind("exil", EXIL)
result_graph.bind("owl", OWL)
result_graph.bind("gams", GAMS)
result_graph.bind("wdt", WDT)
result_graph.bind("geo", GEO)

# GLOABL VARIABLES
BASE_URL = "https://gams.uni-graz.at/context:exil" 
WIKIDATA_BASE_URL = "http://www.wikidata.org/entity/"
VIAF_BASE_URL = "https://viaf.org/viaf/"
GEONAMES_BASE_URL = "http://www.geonames.org/"


female = URIRef(BASE_URL + "#Female")
male = URIRef(BASE_URL + "#Male")
#####

#####
#Function
#####

# ExilTrans_biographische Datenbank: https://docs.google.com/spreadsheets/d/1-P59JLlwZWTQoBsrvGhe6nKwakJe2XY00nPvEf0_sOA/edit#gid=713256902
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1-P59JLlwZWTQoBsrvGhe6nKwakJe2XY00nPvEf0_sOA'



def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()

        
        # select data in first spreadsheet
        SAMPLE_RANGE_NAME = "A3:L395"
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])
        
        # select data in tab "Beruf_Tätigkeit"
        SAMPLE_RANGE_NAME_beruf = "'Beruf_Tätigkeit'!A3:M395"
        result_beruf = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME_beruf).execute()
        values_beruf = result_beruf.get('values', [])
        
        # select data in tab "Exilstationen" 
        SAMPLE_RANGE_NAME_exilstationen = "'Exilstationen'!A3:BTA395"
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME_exilstationen).execute()
        values_exilstationen = result.get('values', [])
        
        # select data in tab "Sprachen" 
        SAMPLE_RANGE_NAME_sprachen = "'Sprachen'!A3:Q395"
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME_sprachen).execute()
        values_sprachen = result.get('values', [])
        
        # select data in tab "Profil" 
        SAMPLE_RANGE_NAME_profil = "'Profil'!A3:M395"
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME_profil).execute()
        values_profil = result.get('values', []) 
        
        # select data in tab "Quellen" 
        SAMPLE_RANGE_NAME_quellen = "'Quellen'!A3:AY395"
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME_quellen).execute()
        values_quellen = result.get('values', [])
        
        # select data in tab "Archive" 
        SAMPLE_RANGE_NAME_archive = "'Archive'!A3:H395"
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME_archive).execute()
        values_archive = result.get('values', []) 

        # select data in tab "dropdown"
        SAMPLE_RANGE_NAME_dropdown = "'dropdown'!A2:I170"
        result_dropdown = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME_dropdown).execute()
        values_dropdown = result_dropdown.get('values', [])

        # select data in tab "Normalisierung"
        '''
        SAMPLE_RANGE_NAME_normalisierung = "'Normalisierung'!A2:W403"
        result_normalisierung = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME_normalisierung).execute()
        values_normalisierung = result_normalisierung.get('values', [])
        '''

        # select data in tab "ORimport" 
        SAMPLE_RANGE_NAME_ORimport = "'ORimport'!A2:S462"
        result_ORimport = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME_ORimport).execute()
        values_ORimport = result_ORimport.get('values', [])          
        

        if not values:
            print('No data found.')
            return

        ########################################################################################
        ### https://www.w3.org/TR/void/
        ########################################################################################
        VOID_Dataset = URIRef(BASE_URL)
        result_graph.add((VOID_Dataset, RDF.type, VOID.Dataset ))
        # foaf
        result_graph.add((VOID_Dataset, FOAF.homepage, URIRef(BASE_URL)))
        # generated
        result_graph.add((VOID_Dataset, DCTERMS.modified, Literal(date.today())))
        # void: 
        result_graph.add((VOID_Dataset, VOID.feature, URIRef("http://www.w3.org/ns/formats/RDF_XML")))
        result_graph.add((VOID_Dataset, VOID.dataDump, URIRef("https://gams.uni-graz.at/o:exil.data/ONTOLOGY")))
        result_graph.add((VOID_Dataset, VOID.vocabulary, URIRef("https://gams.uni-graz.at/o:exil.ontology#")))
        result_graph.add((VOID_Dataset, VOID.vocabulary, URIRef("https://gams.uni-graz.at/o:gams-ontology#")))
        result_graph.add((VOID_Dataset, VOID.vocabulary, URIRef("http://xmlns.com/foaf/spec/")))
        result_graph.add((VOID_Dataset, VOID.vocabulary, URIRef("http://purl.org/dc/terms/")))
        result_graph.add((VOID_Dataset, VOID.vocabulary, URIRef("http://www.w3.org/2003/01/geo/wgs84_pos#")))
        result_graph.add((VOID_Dataset, VOID.vocabulary, URIRef("http://www.wikidata.org/prop/direct/")))
        result_graph.add((VOID_Dataset, VOID.vocabulary, URIRef("https://schema.org/")))
        #result_graph.add((VOID_Dataset, VOID.triples, Literal(0)))
        # descriptiv metadata, dc:
        result_graph.add((VOID_Dataset, DC.title, Literal("Exil:Trans. Forschungsprojekt und Datenbank zu Leben und Arbeit verfolgter Übersetzer und Übersetzerinnen")))
        result_graph.add((VOID_Dataset, DC.creator, Literal("Digital Humanities Craft OG") ))
        result_graph.add((VOID_Dataset, DC.creator, Literal("Steiner, Christian") ))
        result_graph.add((VOID_Dataset, DC.creator, Literal("Pollin, Christopher") ))
        result_graph.add((VOID_Dataset, DC.date, Literal("2022") ))
        result_graph.add((VOID_Dataset, DC.contributor, Literal("Kremmel, Stefanie") ))
        result_graph.add((VOID_Dataset, DC.language, Literal("ger") ))
        result_graph.add((VOID_Dataset, RDFS.seeAlso, Literal("https://exiltrans.univie.ac.at/") ))
        result_graph.add((VOID_Dataset, DC.source, Literal("https://exiltrans.univie.ac.at/") ))
        # gams projects categories
        result_graph.add((VOID_Dataset, DC.subject, Literal("Translationswissenschaft", lang="de") ))
        result_graph.add((VOID_Dataset, DC.subject, Literal("Translation Studies", lang="en") ))
        result_graph.add((VOID_Dataset, DC.subject, Literal("Biography", lang="en") ))
        result_graph.add((VOID_Dataset, DC.subject, Literal("Database", lang="en") ))
        result_graph.add((VOID_Dataset, DC.subject, Literal("Datenbank", lang="de") ))
        result_graph.add((VOID_Dataset, DC.subject, Literal("Biografie", lang="de") ))
        result_graph.add((VOID_Dataset, DC.subject, Literal("Contemporary", lang="en") ))
        result_graph.add((VOID_Dataset, DC.subject, Literal("Gegenwart", lang="de") ))
        result_graph.add((VOID_Dataset, DC.description, Literal("Das Projekt Exil:Trans setzt es sich zum Ziel, Übersetzer*innen, die durch das NS-Regime zum Gang ins Exil gezwungen wurden, systematisch zu untersuchen. Die Exil:Trans Datenbank bietet einen Einblick in die wichtigsten Lebensdaten von durch das NS-Regime verfolgten Übersetzern und Übersetzerinnen. Die Datenbank enthält Personendaten, das translatorische Profil sowie die Daten zu den Exilwegen inklusive einer möglichen Remigration der Übersetzer*innen.", lang="de") ))
        # publisher
        result_graph.add((VOID_Dataset, DC.publisher, Literal( "Centre for Translation Studies, University of Vienna" ) ))
        result_graph.add((VOID_Dataset, DC.publisher, Literal( "Institute Centre for Information Modelling, University of Graz" ) ))
        # rights
        result_graph.add((VOID_Dataset, DC.rights, Literal( "Creative Commons BY-NC 4.0" ) ))
        result_graph.add((VOID_Dataset, DC.rights, Literal( "https://creativecommons.org/licenses/by-nc/4.0/" ) ))


        # creat a dictonary to globaly store if an entry is verified (v) or not verified (vn)
        # v'365': 'v'; '349': 'nv
        for row in values:
            id = row[0]
            verfied_dict[id] = row[11]

        for row in values_ORimport:         
            # schema:Person = foaf:Person
            try:
                if(row[1]):
                    if(verfied_dict[row[0]] == 'v'):
                        person_uri = URIRef(BASE_URL + "#person." + str(row[0]))
                        result_graph.add((person_uri , RDF.type, SDO.Person))
                        result_graph.add((person_uri , GAMS.isMemberOfCollection, URIRef(BASE_URL) ))
                        result_graph.add((person_uri , GAMS.textualContent, Literal(normalize_string_for_JSON(row[1])) ))
                        result_graph.add((person_uri , RDFS.label, Literal(normalize_string_for_JSON(row[1])) ))
                        if(row[2]):
                            result_graph.add((person_uri , OWL.sameAs, URIRef(WIKIDATA_BASE_URL + normalize_prettify_uri(row[2]) )))
                            result_graph.add((person_uri , SDO.identifier, URIRef(WIKIDATA_BASE_URL + normalize_prettify_uri(row[2]) )))
                        # wikipedia
                        try:
                            if(row[18]):
                                # Wikipedia URL
                                result_graph.add((person_uri, SDO.subjectOf, URIRef(row[18])))
                        except:
                            pass
            except:
                    pass


            # occupation, beruf / tätigkeiten
            try:
                if(row[3]):
                    occupation_string = row[3]
                    occupation_uri = URIRef(BASE_URL + "#occupation." + normalize_prettify_uri(occupation_string))
                    result_graph.add((occupation_uri , RDF.type, SDO.Occupation))
                    result_graph.add((occupation_uri , RDFS.label, Literal(normalize_string_for_JSON(occupation_string)) ))
                    
                    try:
                        if(row[4]):
                            try:
                                # owl:sameAs
                                result_graph.add((occupation_uri , OWL.sameAs, URIRef(WIKIDATA_BASE_URL + normalize_prettify_uri(row[4]) )))
                                # wikidata
                                result_graph.add((occupation_uri , SDO.identifier, URIRef(WIKIDATA_BASE_URL + normalize_prettify_uri(row[4]) )))
                            except:
                                pass
                    except:
                        pass
                    # Berufe Kategorie
                    try:
                        if(row[5]):
                            # exil:category
                            occupation_category_uri = URIRef(BASE_URL + "#occupation_category." + normalize_prettify_uri(row[5]) )
                            result_graph.add((occupation_uri , EXIL.category, occupation_category_uri ))
                            result_graph.add((occupation_category_uri, RDF.type, EXIL.Category ))
                            result_graph.add((occupation_category_uri, RDFS.label, Literal(normalize_string_for_JSON(row[5])) ))
                    except:
                        pass
            except:
                    pass
            
            # places
            try:
                if(row[6]):
                    places_string = row[6]
                    places_uri = URIRef(BASE_URL + "#place." + normalize_prettify_uri(places_string))
                    result_graph.add((places_uri , RDF.type, SDO.Place))
                    result_graph.add((places_uri , RDFS.label, Literal(normalize_string_for_JSON(places_string)) ))
                    result_graph.add((places_uri , SDO.name, Literal(normalize_string_for_JSON(places_string)) ))
            except:
                pass 
           
            try:
                # owl:sameAs
                result_graph.add((places_uri , OWL.sameAs, URIRef(WIKIDATA_BASE_URL + normalize_prettify_uri(row[7]) )))
                # wikidata
                result_graph.add((places_uri , SDO.identifier, URIRef(WIKIDATA_BASE_URL + normalize_prettify_uri(row[7]) )))
            except:
                pass
                #
            try:
                # latitude, geo:lat 
                if(row[8]):
                    result_graph.add((places_uri , GEO.lat, Literal(normalize_string_for_JSON(row[8]) )))
                # longitude, geo:long
                if(row[9]):
                    result_graph.add((places_uri , GEO.long, Literal(normalize_string_for_JSON(row[9]) )))
            except:
                pass         

            # archive: Schweizerische Nationalbibliothek|Q201787
            try:
                if(row[10]):
                    archive_uri = URIRef(BASE_URL + "#archive." + normalize_prettify_uri(row[10]))
                    result_graph.add((archive_uri , RDF.type, SDO.Archive))
                    result_graph.add((archive_uri , RDFS.label, Literal(normalize_string_for_JSON(row[10])) ))
                    result_graph.add((archive_uri , SDO.name, Literal(normalize_string_for_JSON(row[10])) ))
                    if(row[11]):
                        # owl:sameAs
                        result_graph.add((archive_uri , OWL.sameAs, URIRef(WIKIDATA_BASE_URL + normalize_prettify_uri(row[11]) )))
                        #
                        result_graph.add((archive_uri , SDO.identifier, URIRef(WIKIDATA_BASE_URL + normalize_prettify_uri(row[11]) )))
            except:
                pass

            # languages: Hebräisch|Q9288
            try:
                if(row[12]):
                    language_uri = URIRef(BASE_URL + "#language." + normalize_prettify_uri(row[12]))
                    result_graph.add((language_uri , RDF.type, SDO.Language))
                    result_graph.add((language_uri , RDFS.label, Literal(normalize_string_for_JSON(row[12])) ))
                    result_graph.add((language_uri , SDO.name, Literal(normalize_string_for_JSON(row[12])) ))
                    try:
                        if(row[13]):
                            # owl:sameAs
                            result_graph.add((language_uri , OWL.sameAs, URIRef(WIKIDATA_BASE_URL + normalize_prettify_uri(row[13]) )))
                            #
                            result_graph.add((language_uri , SDO.identifier, URIRef(WIKIDATA_BASE_URL + normalize_prettify_uri(row[13]) )))
                    except:
                        pass
            except:
                pass

            # schema:Country
            try:
                country_string = row[14]
                country_uri = URIRef(BASE_URL + "#country." + normalize_prettify_uri(country_string))
                result_graph.add((country_uri , RDF.type, SDO.Country))
                result_graph.add((country_uri , RDFS.label, Literal(normalize_string_for_JSON(country_string))))
                result_graph.add((country_uri , SDO.name, Literal(normalize_string_for_JSON(country_string))))
                try:
                    if(row[15]):
                        # owl:sameAs
                        result_graph.add((country_uri , OWL.sameAs, URIRef(WIKIDATA_BASE_URL + normalize_prettify_uri(row[15]) )))
                        #
                        result_graph.add((country_uri , SDO.identifier, URIRef(WIKIDATA_BASE_URL + normalize_prettify_uri(row[15]) )))
                except:
                    pass  
                try:
                # latitude, geo:lat 
                    if(row[16]):
                        result_graph.add((country_uri , GEO.lat, Literal(normalize_string_for_JSON(row[16]) )))
                    # longitude, geo:long
                    if(row[17]):
                        result_graph.add((country_uri , GEO.long, Literal(normalize_string_for_JSON(row[17]) )))
                except:
                    pass  

            except:
                    pass

        # iteration first tab
        for row in values:
            if(verfied_dict[row[0]] == 'v'):
                person_uri = URIRef(BASE_URL + "#person." + str(row[0]))

                # name
                result_graph.add((person_uri , SDO.familyName, Literal(normalize_string_for_JSON(row[1])) ))
                try:
                    result_graph.add((person_uri , SDO.givenName , Literal(normalize_string_for_JSON(row[2])) ))
                except: 
                    pass
                try:
                    if(row[3]):
                        result_graph.add((person_uri , SDO.additionalName  , Literal(normalize_string_for_JSON(row[3])) ))
                except: 
                    pass
                # sex
                if(row[4] == "w"):
                    result_graph.add((person_uri, SDO.gender, female ))
                if(row[4] == "m"):
                    result_graph.add((person_uri, SDO.gender, male ))
                # birth
                try:
                    # schema:birthDate
                    result_graph.add((person_uri, SDO.birthDate, Literal(normalize_string_for_JSON(row[5])) ))
                except: 
                    pass
                try:
                    # schema:birthPlace
                    result_graph.add((person_uri, SDO.birthPlace, URIRef(BASE_URL + "#place." + normalize_prettify_uri(row[6])) ))
                except: 
                    pass
                try:
                    # exil:birthCountry
                    result_graph.add((person_uri, EXIL.birthCountry, URIRef(BASE_URL + "#country." + normalize_prettify_uri(row[7])) ))
                except: 
                    pass
                
                # death
                try:
                    # schema:deathDate
                    result_graph.add((person_uri, SDO.deathDate , Literal(normalize_string_for_JSON(row[8])) ))
                except: 
                    pass
                try:
                    # schema:deathPlace
                    result_graph.add((person_uri, SDO.deathPlace, URIRef(BASE_URL + "#place." + normalize_prettify_uri(row[9])) ))
                except: 
                    pass
                try:
                    # exil:deathCountry
                    result_graph.add((person_uri, EXIL.deathCountry, URIRef(BASE_URL + "#country." + normalize_prettify_uri(row[10])) ))
                except: 
                    pass

    # process data in tab "Normalisierung"
        for row in values_beruf:
            if(verfied_dict[row[0]] == 'v'): 
                person_uri = URIRef(BASE_URL + "#person." + str(row[0]))
                for index in range(3,12):
                    try:
                        occupation_uri = URIRef(BASE_URL + "#occupation." + normalize_prettify_uri(row[index]))
                        result_graph.add((person_uri , SDO.hasOccupation, occupation_uri ))
                    except:
                        pass       

    # process data in tab "Exilstationen"
        for row in values_exilstationen:
            if(verfied_dict[row[0]] == 'v'): 
                person_uri = URIRef(BASE_URL + "#person." + str(row[0]))
                # 3,4,5 - 6,7,8 - 9,10,11
                # 20 exils, 3 infomration for every exil
                # stil one exil:Exil too much
                for index in range(1,60,3):
                    if 0 <= index < len(row):
                        if(row[index]):
                            # here is redundant code as creating a same uris leads to "falling together" entities/triples in rdflib;
                            try:
                                if(row[index + 2]):
                                    exil_base_uri = URIRef(BASE_URL + "#exil." + str(row[0]) + str(index))
                                    result_graph.add((person_uri , EXIL.exiled,  exil_base_uri))
                                    result_graph.add((exil_base_uri , EXIL.place,  URIRef(BASE_URL + "#place." + normalize_prettify_uri(row[index + 2]) )))
                            except:
                                pass
                            try:                    
                                if(row[index + 3]):
                                    exil_base_uri = URIRef(BASE_URL + "#exil." + str(row[0]) + str(index))
                                    result_graph.add((person_uri , EXIL.exiled,  exil_base_uri))
                                    result_graph.add((exil_base_uri , RDF.type,  EXIL.Exil))
                                    result_graph.add((exil_base_uri , EXIL.country,  URIRef(BASE_URL + "#country." + normalize_prettify_uri(row[index + 3]) )))
                            except:
                                pass
                            try:  
                                if(row[index + 4]):
                                    exil_base_uri = URIRef(BASE_URL + "#exil." + str(row[0]) + str(index))
                                    result_graph.add((person_uri , EXIL.exiled,  exil_base_uri))
                                    result_graph.add((exil_base_uri , RDF.type,  EXIL.Exil))
                                    result_graph.add((exil_base_uri , EXIL.year,  Literal(normalize_string_for_JSON(row[index + 4])) ))  
                            except:
                                pass
                try:
                    #todo: if row[66] is empty then remigration is not created
                    if(row[63]):
                        remigration_uri_1 = URIRef(BASE_URL + "#remigration.1" + str(row[0]) + str(index))
                        result_graph.add((person_uri , EXIL.remigrated,  remigration_uri_1))
                        result_graph.add((remigration_uri_1 , RDF.type,  EXIL.Remigration))
                        result_graph.add((remigration_uri_1 , EXIL.place,  URIRef(BASE_URL + "#place." + normalize_prettify_uri(row[63]) )))
                except:
                    pass

                try:
                    if(row[64]):
                        remigration_uri_1 = URIRef(BASE_URL + "#remigration.1" + str(row[0]) + str(index))
                        result_graph.add((person_uri , EXIL.remigrated,  remigration_uri_1))
                        result_graph.add((remigration_uri_1 , RDF.type,  EXIL.Remigration))
                        result_graph.add((remigration_uri_1 , EXIL.country,  URIRef(BASE_URL + "#country." + normalize_prettify_uri(row[64]) )))  
                except:
                    pass

                try:
                    if(row[65]):
                        remigration_uri_1 = URIRef(BASE_URL + "#remigration.1" + str(row[0]) + str(index))
                        result_graph.add((person_uri , EXIL.remigrated,  remigration_uri_1))
                        result_graph.add((remigration_uri_1 , RDF.type,  EXIL.Remigration))
                        result_graph.add((remigration_uri_1 , EXIL.year,  Literal(normalize_string_for_JSON(row[65])) ))  
                except:
                    pass

                try:
                    #todo: if row[66] is empty then remigration is not created
                    if(row[66]):
                        remigration_uri_2 = URIRef(BASE_URL + "#remigration.2" + str(row[0]) + str(index))
                        result_graph.add((person_uri , EXIL.remigrated,  remigration_uri_2))
                        result_graph.add((remigration_uri_2 , RDF.type,  EXIL.Remigration))
                        result_graph.add((remigration_uri_2 , EXIL.place,  URIRef(BASE_URL + "#place." + normalize_prettify_uri(row[66]) )))  
                except:
                    pass
                try:
                    if(row[67]):
                        remigration_uri_2 = URIRef(BASE_URL + "#remigration.2" + str(row[0]) + str(index))
                        result_graph.add((person_uri , EXIL.remigrated,  remigration_uri_2))
                        result_graph.add((remigration_uri_2 , RDF.type,  EXIL.Remigration))
                        result_graph.add((remigration_uri_2 , EXIL.country,  URIRef(BASE_URL + "#country." + normalize_prettify_uri(row[67]) )))
                except:
                    pass
                try:
                    if(row[68]):
                        remigration_uri_2 = URIRef(BASE_URL + "#remigration.2" + str(row[0]) + str(index))
                        result_graph.add((person_uri , EXIL.remigrated,  remigration_uri_2))
                        result_graph.add((remigration_uri_2 , RDF.type,  EXIL.Remigration))
                        result_graph.add((remigration_uri_2 , EXIL.year,  Literal(normalize_string_for_JSON(row[68])) ))  
                except:
                    pass

                # place of activity
                # wirkungsort_ort
                try:
                    if(row[69]):
                        placeOfActivity_uri = URIRef(BASE_URL + "#placeOfActivity." + str(row[0]) + str(index))
                        result_graph.add((person_uri , EXIL.placeOfActivity,  placeOfActivity_uri))
                        result_graph.add((placeOfActivity_uri , RDF.type,  EXIL.PlaceOfActivityBeforeExile))
                        result_graph.add((placeOfActivity_uri , EXIL.place,  URIRef(BASE_URL + "#place." + normalize_prettify_uri(row[69]) )))
                except:
                    pass
                # wirkungsort_land
                try:
                    if(row[70]):
                        result_graph.add((person_uri , EXIL.placeOfActivity,  placeOfActivity_uri))
                        result_graph.add((placeOfActivity_uri , RDF.type,  EXIL.PlaceOfActivityBeforeExile))
                        result_graph.add((placeOfActivity_uri , EXIL.country,  URIRef(BASE_URL + "#country." + normalize_prettify_uri(row[70]) )))
                except:
                    pass
                # wirkungsort_jahr
                try:
                    if(row[71]):
                        result_graph.add((person_uri , EXIL.placeOfActivity,  placeOfActivity_uri))
                        result_graph.add((placeOfActivity_uri , RDF.type,  EXIL.PlaceOfActivityBeforeExile))
                        result_graph.add((placeOfActivity_uri , EXIL.year,  Literal(normalize_string_for_JSON(row[71])) ))
                except:
                    pass


        # process data in tab "Sprachen"
        for row in values_sprachen:
            if(verfied_dict[row[0]] == 'v'): 
                person_uri = URIRef(BASE_URL + "#person." + str(row[0]))
                for index in range(3,6):
                    try:
                        if(row[index]):
                            #
                            profil_uri = URIRef(BASE_URL + "#profil." + str(row[0]))
                            result_graph.add((profil_uri, RDF.type, EXIL.Profile  ))
                            #
                            language_uri = URIRef(BASE_URL + "#language." + normalize_prettify_uri(str(row[index])))
                            result_graph.add((language_uri , RDF.type,  SDO.Language))
                            result_graph.add((language_uri , RDFS.label,  Literal(normalize_string_for_JSON(row[index])) ))
                            result_graph.add((profil_uri , EXIL.targetLanguage ,  URIRef(language_uri) ))
                            result_graph.add((person_uri, EXIL.profile, profil_uri  ))
                    except:
                        pass
                for index in range(7,16):
                    try:
                        if(row[index]):
                            #
                            profil_uri = URIRef(BASE_URL + "#profil." + str(row[0]))
                            result_graph.add((profil_uri, RDF.type, EXIL.Profile  ))
                            #
                            language_uri = URIRef(BASE_URL + "#language." + normalize_prettify_uri(str(row[index])))
                            result_graph.add((language_uri , RDF.type,  SDO.Language))
                            result_graph.add((language_uri , RDFS.label,  Literal(normalize_string_for_JSON(row[index])) ))
                            result_graph.add((profil_uri , EXIL.sourceLanguage ,  URIRef(language_uri) ))
                            result_graph.add((person_uri, EXIL.profile, profil_uri  ))
                    except:
                        pass



        # process data in tab "Quellen"
        for row in values_quellen:
            if(verfied_dict[row[0]] == 'v'): 
                person_uri = URIRef(BASE_URL + "#person." + str(row[0]))
                for index in range(3,20):
                    try:
                        if(row[index]):
                            source_uri = URIRef(BASE_URL + "#source." + str(row[0]))
                            result_graph.add((source_uri, EXIL.documents,  person_uri))
                            result_graph.add((source_uri, RDF.type, EXIL.Source))
                            # source_entity
                            source_entity_uri = URIRef(BASE_URL + "#source_entity." + str(row[0]) + "." + str(index))
                            result_graph.add((source_entity_uri, RDF.type, EXIL.SourceEntity))
                            result_graph.add((source_uri, EXIL.source, source_entity_uri))
                            if(index>12):
                                result_graph.add((source_entity_uri, RDFS.label, Literal(normalize_string_for_JSON(row[index])) ))
                            else:
                                source_abbreviation = row[index]
                                result_graph.add((source_entity_uri, EXIL.abbreviation, Literal(normalize_string_for_JSON(source_abbreviation)) ))
                                # full title from dropdown tab
                                for row_dropdown in values_dropdown:
                                    try:
                                        if(source_abbreviation == row_dropdown[7]):
                                            result_graph.add((source_entity_uri, RDFS.label, Literal(normalize_string_for_JSON(row_dropdown[8])) ))
                                    except:
                                        pass
                    except:
                        pass

        # process data in tab "Archive"
        for row in values_archive:
            if(verfied_dict[row[0]] == 'v'): 
                person_uri = URIRef(BASE_URL + "#person." + str(row[0]))
                for index in range(3,7):
                    try:
                        if(row[index]):
                            result_graph.add((person_uri, EXIL.archive, Literal(normalize_string_for_JSON(row[index])) ))
                    except:
                        pass

        # process data in tab "Profil"
        for row in values_profil: 
            if(verfied_dict[row[0]] == 'v'):
                person_uri = URIRef(BASE_URL + "#person." + str(row[0]))
                for index in range(3,13):
                    try:
                        if(row[index]):
                            profil_uri = URIRef(BASE_URL + "#profil." + str(row[0]))
                            field_of_work_uri = URIRef(BASE_URL + "#field." + normalize_prettify_uri(str(row[index]) ))
                            result_graph.add((profil_uri, RDF.type, EXIL.Profile  ))
                            result_graph.add((person_uri, EXIL.profile, profil_uri  ))
                            result_graph.add((profil_uri, EXIL.workedIn, field_of_work_uri ))
                            try:
                                result_graph.add((field_of_work_uri, RDF.type, EXIL.FieldOfWork ))
                                result_graph.add((field_of_work_uri, RDFS.label, Literal(normalize_string_for_JSON(str(row[index].split(" - ",1)[1]))) ))
                                # Dewey Decimal Classification
                                result_graph.add((field_of_work_uri, WDT.P1036, URIRef("http://dewey.info/class/" + normalize_prettify_uri(row[index].split(" - ",1)[0]))  ))
                            except:
                                pass
                    except:
                        pass
            
            
    except HttpError as err:
        print(err)


    # Female and Male SKOS Concepts
    result_graph.add(( female , RDF.type, SDO.GenderType))
    result_graph.add(( female , RDFS.label, Literal("female", lang='en') ))
    result_graph.add(( female , RDFS.label, Literal("weiblich", lang='de') ))
    result_graph.add(( male, RDF.type, SDO.GenderType))
    result_graph.add(( male , RDFS.label, Literal("male", lang='en') ))
    result_graph.add(( male , RDFS.label, Literal("männlich", lang='de') ))

    #creating an output file
    result_graph.serialize(destination = "exil_trans.xml", format="pretty-xml")
    result_graph.serialize(destination = "exil_trans.ttl", format="turtle")

if __name__ == '__main__':
    main()



