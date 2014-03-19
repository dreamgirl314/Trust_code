
from bottle import route, run, template, request, static_file,get,post,request
import bottle
import logging
from ConfigParser import SafeConfigParser
import glob
import sys
import traceback
import os
from os import listdir
from os.path import isfile, join
import rdflib





import traceback
import sys
from xlutils.margins import number_of_good_cols, number_of_good_rows
from xlutils.copy import copy
from xlutils.styles import Styles
from xlrd import open_workbook, XL_CELL_EMPTY, XL_CELL_BLANK, cellname, colname
import glob
from rdflib import ConjunctiveGraph, Namespace, Literal, RDF, RDFS, BNode, URIRef
import re
from ConfigParser import SafeConfigParser
import urllib
from urlparse import urlparse
import logging
import os
import time
import datetime



# This is to import tablinker from another path
sys.path.insert(0, '/Users/sna210/Dropbox/IFIPTM14/Code/web_service/code_web/TabLinker/src')
from tablinker import TabLinker



fileList = []

@route('/trust/home')
def trust():
	
    #inPath = "../input/"
    inPath = "../input/"
    outPath = "../output/"
    inFiles = [ f for f in listdir(inPath) if isfile(join(inPath,f)) ]
    outFiles = [ f for f in listdir(outPath) if isfile(join(outPath,f)) ]
    #return template('tl-service', state='start', inFiles=inFiles, outFiles=outFiles)
    #return inPath
    return "Hello World!"


@get('/upload')
def upload_view():
    return """
        <form action="/upload" method="post" enctype="multipart/form-data">
          Train set: <input type="text" name="name1" />
          <input type="file" name="data1" />
          
          Test set: <input type="text" name="name2" />
          <input type="file" name="data2" />
          <input type="submit" name="submit" value="upload now" />
        </form>
        """    

@post('/upload')
def do_upload():
	# upload train set
	train_name = request.forms.get('name1')
	train_data = request.files.get('data1')
	save_path = '../input/' + train_data.filename
	fileList.append(train_data.filename)
	train_data.save(save_path, overwrite = True)

	# upload test set
	test_name = request.forms.get('name2')
	test_data = request.files.get('data2')
	save_path = '../input/' + test_data.filename
	fileList.append(test_data.filename)
	test_data.save(save_path, overwrite = True)
        
        #os.system("/Users/sna210/Dropbox/IFIPTM14/Code/web_service/code_web/Tablinker/src/tablinker.py")
        if train_data is not None and train_name is not None and test_data is not None and test_name is not None:
            raw_train = train_data.file.read()
            filename_train = train_data.filename
            raw_test = test_data.file.read()
            filename_test = test_data.filename
            return "Hello  ! You uploaded %s (%d bytes) and %s(%d bytes) ." % (filename_train, len(raw_train),filename_test,len(raw_test))#,test_name,filename_test,len(raw_test))
        return "Damn!!!"




@route('/tablinker/run')
def tablinker():
    logging.basicConfig(level=logging.INFO)
    logging.info('Reading configuration file')
    
    config = SafeConfigParser()
    try :
        config.read('../config.ini')
        srcMask = config.get('paths', 'srcMask')
        targetFolder = config.get('paths','targetFolder')
        verbose = config.get('debug','verbose')
        if verbose == "1" :
            logLevel = logging.DEBUG
        else :
            logLevel = logging.INFO
    except :
        logging.error("Could not find configuration file, using default settings!")
        srcMask = '../input/*_marked.xls'
        targetFolder = config.get('paths', 'targetFolder')
        logLevel = logging.DEBUG
        
    logging.basicConfig(level=logLevel)
    
    # Get list of annotated XLS files
    files = glob.glob(srcMask)
    logging.info("Found {0} files to convert.".format(len(files)))
    
    for filename in files :
        logging.info('Starting TabLinker for {0}'.format(filename))
        
        tLinker = TabLinker(filename, config, logLevel)
        
        logging.debug('Calling linker')
        tLinker.doLink()
        logging.debug('Done linking')

        turtleFile = targetFolder + tLinker.fileBasename +'.ttl'
        turtleFileAnnotations = targetFolder + tLinker.fileBasename +'_annotations.ttl'
        logging.info("Generated {} triples.".format(len(tLinker.graph)))
        logging.info("Serializing graph to file {}".format(turtleFile))
        try :
            fileWrite = open(turtleFile, "w")
            #Avoid rdflib writing the graph itself, as this is buggy in windows.
            #Instead, retrieve string and then write (probably more memory intensive...)
            turtle = tLinker.graph.serialize(destination=None, format=config.get('general', 'format'))
            fileWrite.writelines(turtle)
            fileWrite.close()
            
            #Annotations
            if tLinker.config.get('annotations', 'enabled') == "1":
                logging.info("Generated {} triples.".format(len(tLinker.annotationGraph)))
                logging.info("Serializing annotations to file {}".format(turtleFileAnnotations))
                fileWriteAnnotations = open(turtleFileAnnotations, "w")
                turtleAnnotations = tLinker.annotationGraph.serialize(None, format=config.get('general', 'format'))
                fileWriteAnnotations.writelines(turtleAnnotations)
                fileWriteAnnotations.close()
        except :
            logging.error("Whoops! Something went wrong in serializing to output file")
            logging.info(sys.exc_info())
            traceback.print_exc(file=sys.stdout)
            
        logging.info("Done")
    return "Hello"








@route('/trust/my_ip')
def show_ip():
    ip = request.environ.get('REMOTE_ADDR')
    return template("Your IP is: {{ip}}", ip=ip)

run(host='localhost', port=8080, debug=True)