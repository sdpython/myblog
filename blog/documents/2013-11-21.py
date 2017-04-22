#coding:latin-1
import pandas
t2012 = pandas.read_csv("a2012.csv", sep=";", encoding="utf8", thousands = " ")
t2014 = pandas.read_csv("a2014.csv", sep=";", encoding="utf8", thousands = " ")
t2012.columns = ["col%d" % i for i in range(len(t2012.columns)) ]
t2014.columns = ["col%d" % i for i in range(len(t2014.columns)) ]
t2012 = t2012 [ [ "col%d" % i for i in range(6) ] ]
t2014 = t2014 [ [ "col%d" % i for i in range(5) ] ]
t2014 = t2014.ix [ t2014["col0"].map( lambda row : not row.startswith("Total")), : ]

t2012.to_csv("at2012.csv", sep="\t", encoding="utf8", index=False)
t2014.to_csv("at2014.csv", sep="\t", encoding="utf8", index=False)

import sys
sys.path.append(r"C:\username\__home_\_data\program\python\pyensae\src")

from pyensae import import_flatfile_into_database
dbf = "a2012_2014.db3"
import_flatfile_into_database(dbf, "at2014.csv")
import_flatfile_into_database(dbf, "at2012.csv")

