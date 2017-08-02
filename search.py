#!/usr/bin/env python
# -*- coding: utf8 -*-
INDEX_DIR = "IndexFiles.index"

import sys, os, lucene, jieba

from java.io import File
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher, BooleanQuery, BooleanClause
from org.apache.lucene.util import Version

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

"""
This script is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""
def run(searcher, analyzer,search_content):
    command = search_content
    command = ' '.join(jieba.cut(command))
    query = QueryParser(Version.LUCENE_CURRENT, "title", analyzer).parse(command)
    scoreDocs = searcher.search(query, 10).scoreDocs 
    print "%s total matching documents." % len(scoreDocs)
    result_s = []
    result_s_s = []
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        print 'title:', ''.join(doc.get("title").split())
        print 'url:', doc.get("url")
        result_s.append(''.join(doc.get("title").split()))
        result_s.append(doc.get("url"))
        result_s_s.append(result_s)
        result_s = []
    return result_s_s

def init_search(search_content,vm_env):
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    lucene.initVM()
    STORE_DIR = "zhihuindex"
    print 'lucene', lucene.VERSION
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
    result_list = run(searcher, analyzer,search_content)
    del searcher
    return result_list
