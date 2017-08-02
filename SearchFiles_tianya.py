#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys, os, lucene
import math
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from myword.models import *
"""
This script is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""

import jieba
def run(searcher, analyzer,search_content):
    command = search_content
    seg_list = jieba.cut(command)
    command=" ".join(seg_list)
    print "Searching for:", command
    query = QueryParser(Version.LUCENE_CURRENT, "info",
                            analyzer).parse(command)
    scoreDocs = searcher.search(query, 50).scoreDocs
    result_s = []
    result = []
    print "%s total matching documents." % len(scoreDocs)
    print '-----------------------------------------------------------------'
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        '''print 'url:', doc.get("url")
        #print 'title:', doc.get("title")
        print 'title:', ''.join(doc.get("info").split())
        print 'time:',doc.get("time")
        print 'reply',doc.get("reply")
        print 'go_through',doc.get("go_through")
        print '===================================================================='''
        url = doc.get("url")
        title = ''.join(doc.get("info").split())
        reply = doc.get("reply")
        go_through = doc.get("go_through")
        time = doc.get("time")
        filterResult = BBS_hupu_tianya.objects.filter(title = title)
        if len(filterResult) <= 0:
            bbs = BBS_hupu_tianya.objects.create(title =title,reply = reply,url = url, time = time, go_through = go_through)
            bbs.save()
        result.append(doc.get("url"))
        result.append(''.join(doc.get("info").split()))
        result.append(doc.get("time"))
        result.append(doc.get("reply"))
        result.append(doc.get("go_through"))
        result.append(scoreDoc.score)
        result.append(0)
        result_s.append(result)
        result = []
    sort(result_s)
    return result_s
def sort_gothrough(result_s):
    len1 = len(result_s)
    for i in range(0,len1-1):
        for j in range(i+1,len1):
            if int(result_s[i][4]) < int(result_s[j][4]):
                tmp = result_s[i]
                result_s[i] = result_s[j]
                result_s[j] = tmp
def sort_reply(result_s):
    len1 = len(result_s)
    for i in range(0,len1-1):
        for j in range(i+1,len1):
            if int(result_s[i][3]) < int(result_s[j][3]):
                tmp = result_s[i]
                result_s[i] = result_s[j]
                result_s[j] = tmp
def sort(result_s):
    len1 = len(result_s)
    score_max = result_s[0][5]
    alfha = 0.2
    beta = 0.3
    gama = 0.45
    lamada = 0.05
    x = 1000
    y = 40
    date='20170112'
    for item in result_s:
        a= alfha * ( item[5] / score_max ) * 100
        b= 100 * beta * (2/math.pi) * math.atan(int(item[4]) / x )
        c= 100 * gama * (2/math.pi) * math.atan(int(item[3]) / y)
        #item[6] = item[6]
        data_list = item[2][0:5].split('-')
        data_rank = judge(data_list)
        d=data_rank*lamada
        #print a,b,c,d
        item[6]=a+b+c+d
    for i in range(0,len1-1):
        for j in range(i+1,len1):
            if int(result_s[i][6]) < int(result_s[j][6]):
                tmp = result_s[i]
                result_s[i] = result_s[j]
                result_s[j] = tmp
def judge(data_list):
    data_list=[int(data_list[0]),int(data_list[1])]
    date=[1,17]
    if date==data_list:
        return 100
    elif date[0]==data_list[0]:
        return 60
    else: 
        return 0



def init_search(search_content,vm_env):
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    lucene.initVM()
    STORE_DIR = "index"
    print 'lucene', lucene.VERSION
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
    result_s = run(searcher, analyzer,search_content)
    del searcher
    print(result_s)
    return result_s
