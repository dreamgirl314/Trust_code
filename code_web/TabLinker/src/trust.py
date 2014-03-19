# Write code here to read the ttl files and use the trust algorithm 

# read and write to training and test set

from collections import defaultdict
from datetime import date
import collections
#from cornetto.simcornet import SimCornet
from collections import defaultdict
import rdflib
from nltk.corpus import wordnet
from nltk.corpus import wordnet as wn

from collections import Counter

import re
import math




categories = ["usefulness-useful","evaluation","comments","todo","judgement-negative","judgement-positive","problematic-foreign","problematic-huh","problematic-misperception","problematic-misspelling","problematic-no_consensus","problematic-personal","usefulness-not_useful"]
train = rdflib.Graph()
train.parse("../output/train_marked.ttl",format = "n3")
test = rdflib.Graph()
test.parse("../output/test_marked.ttl",format="n3")



def test_set_build1():
	 values1 = [(s,u,v,i,t) for s,p1,o in test.triples((None,rdflib.URIRef("http://lod.cedar-project.nl/core/isObservation"),None))
     for i in test.objects(o,rdflib.URIRef("http://lod.cedar-project.nl/core/Sheet1/Image_ID"))
     for u in test.objects(o,rdflib.URIRef("http://lod.cedar-project.nl/core/Sheet1/User_id"))
     for t in test.objects(o,rdflib.URIRef("http://lod.cedar-project.nl/core/populationSize"))      
     for v in test.objects(o,rdflib.URIRef("http://lod.cedar-project.nl/core/Sheet1/Annotation_ID"))]
     #for e in train.objects(o,rdflib.URIRef("http://lod.cedar-project.nl/core/Sheet1/Evaluation"))
	 #if (e.toPython()!="typo" and e.toPython()!="?" and e.toPython()!="todo")]
	 return values1
	
	 # for a1,p1,o in train.triples((None,rdflib.URIRef("http://lod.cedar-project.nl/core/isObservation"),None)):
		# #print a1,p1,o
		# print "\n"
		# for o,p2,o2 in train.triples((o,None,None)):

		# 	print a1,p2,o2
def train_set_build1():
	 values2 = [(s,u,v,i,t,e) for s,p1,o in train.triples((None,rdflib.URIRef("http://lod.cedar-project.nl/core/isObservation"),None))
     for i in train.objects(o,rdflib.URIRef("http://lod.cedar-project.nl/core/Sheet1/Image_ID"))
     for u in train.objects(o,rdflib.URIRef("http://lod.cedar-project.nl/core/Sheet1/User_id"))
     for t in train.objects(o,rdflib.URIRef("http://lod.cedar-project.nl/core/populationSize"))      
     for v in train.objects(o,rdflib.URIRef("http://lod.cedar-project.nl/core/Sheet1/Annotation_ID"))
     for e in train.objects(o,rdflib.URIRef("http://lod.cedar-project.nl/core/Sheet1/Evaluation"))
	 if (e.toPython()!="typo" and e.toPython()!="?" and e.toPython()!="todo")]
	 return values2

def get_word(evaluation):
	word = evaluation.toPython()
	return word

def build_rep_user():
	f = open('../output/output.txt', 'w')
	#print "Tag \t Prediction"
	true = 0
	false = 0
	accuracy = 0
	train_set = train_set_build1()
	test_set = test_set_build1()
	similarity = 0.0
	N = len(categories)
	for i in test_set:
		tag2 = get_word(i[4])
		p = 0.0
		rep = dict([(x,0.0) for x in categories])
		for j in train_set:
			if i[1]==j[1]:		
				tag1 = get_word(j[4])
				print tag1,tag2
				similarity = wup_words(tag1,tag2)
				p = p + similarity
				evaluation = get_word(j[5])
				rep[evaluation] = p
		e = dict([(x,float(y+1)/(sum(rep.values()) + N)) for x,y in rep.iteritems()])
		max_predicted_value = max(e.values())
		for opinion, value in e.iteritems():
			if value == max_predicted_value:
				prediction = opinion
		print tag2,"\t",prediction
		print >> f,tag2,prediction
	f.close()


if __name__=="__main__":
	build_rep_user()
	
	
	
	
	

