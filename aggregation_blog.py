#coding:utf-8
import os
from datetime import datetime
from ensae_teaching_cs.automation import get_teaching_modules
from pyrsslocal.cli import compile_rss_blogs


def collect_blogs(url="http://www.xavierdupre.fr/",
                  dest="build/blog/blogagg",
                  fLOG=print):
    year = datetime.now().year - 2
    links = [# url + "blog/xdbrss.xml",
             "http://lesenfantscodaient.fr/_downloads/rss.xml"]
    for mod in get_teaching_modules():
        if mod in {'_benchmarks', 'machinelearningext',
                   'code_beatrix', 'myblog', 'csharpy',
                   'csharpyml'}:
            continue
        links.append(url + "/app/{}/helpsphinx/_downloads/rss.xml".format(mod))
    
    if not os.path.exists(dest):
        os.makedirs(dest)
    
    out_html = os.path.join(dest, "index.html")
    out_rss = os.path.join(dest, "index_agg_rss.xml")
    
    compile_rss_blogs(links, url + "blogagg/index.html",
                      'Aggregation of blog posts published on <a href='
                      '"http://www.xavierdupre.fr">xavierdupre.fr</a>',
                      title="Recent posts",
                      author="Xavier Dupré",
                      out_html=out_html, out_rss=out_rss,
                      validate=lambda b: b.pubDate.year >= year and "A quoi sert ce module ?" not in b.title,
                      fLOG=fLOG)

if __name__ == "__main__":
    from pyquickhelper.loghelper import fLOG
    fLOG(OutputPrint=True)
    collect_blogs(fLOG=fLOG)
