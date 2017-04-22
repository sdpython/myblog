#coding:utf-8
"""
<!-- SUMMARY BEGINS -->
<!-- SUMMARY ENDS -->
<!-- CUT PAGE HERE -->


<div lang="latex">
I(s) =  \frac{ X(s,t) }{ \sum_{t=10am}^{4pm} X(s,t) }
</div>


"""
import shutil, os, glob, re, datetime, sys
sys.path.append ("../pyquickhelper/src")
sys.path.append ("../pyensae/src")
sys.path.append ("../pyrsslocal/src")
sys.path.append ("../ensae_teaching_cs/src")

from pyquickhelper.loghelper import fLOG
fLOG(OutputPrint = True)
from pyquickhelper.filehelper import TransferFTP, explore_folder, synchronize_folder
from ensae_teaching_cs.homeblog import CopyFileForFtp, py_to_html_folder, modify_all_posts
from ensae_teaching_cs.homeblog import file_build_rss, file_all_keywords, build_process_all_pages

import keyring

loginame = keyring.get_password("ftp_list_modules", os.environ["COMPUTERNAME"] + "login")
password = keyring.get_password("ftp_list_modules", os.environ["COMPUTERNAME"] + "password")  
googleid = keyring.get_password("web", os.environ["COMPUTERNAME"] + "google")
this = os.path.abspath(os.path.dirname(__file__))
destination = os.path.normpath(os.path.join(this, "../../site"))
ftp_site = keyring.get_password("web", os.environ["COMPUTERNAME"] + "ftp")



def copy_site() :
    """
    """
    cwd = os.getcwd()
    p = os.path.abspath(os.path.split(__file__)[0])
    os.chdir(p)
    copy_site_cwd()
    os.chdir(cwd)

def copy_site_cwd() :
    """
    Publishes the blog.
    """    
    fLOG(OutputPrint = True)
        
    cpf = CopyFileForFtp("copyDates.txt", specificTrigger = True)
    cpf.copy_file_ext (".", "html", "blog/documents", doFTP = False)

    # process the blogs
    
    modify_all_posts(exclude = lambda f : False)
    file_build_rss(this, os.path.join(destination, "blog", "xdbrss.xml"))
    res = file_all_keywords(exclude = lambda f : False)

    # add blog files to upload
    
    cpf.copy_file_ext ("blog/giflatex", "gif", os.path.join(destination, "blog/giflatex"))
    cpf.copy_file_ext ("blog/documents", "pdf", os.path.join(destination, "blog/documents"))
    cpf.copy_file_ext ("blog/documents", "gif", os.path.join(destination, "blog/documents"))
    cpf.copy_file_ext ("blog/documents", "xlsx", os.path.join(destination, "blog/documents"))
    cpf.copy_file_ext ("blog/documents", "xlsm", os.path.join(destination, "blog/documents"))
    cpf.copy_file_ext ("blog/documents", "png", os.path.join(destination, "blog/documents"))
    cpf.copy_file_ext ("blog/documents", "jpg", os.path.join(destination, "blog/documents"))
    cpf.copy_file_ext ("blog/documents", "html", os.path.join(destination, "blog/documents"))
    cpf.copy_file_ext ("blog/documents", "zip", os.path.join(destination, "blog/documents"))
    cpf.copy_file_ext ("blog/documents", "tsv", os.path.join(destination, "blog/documents"))
    cpf.copy_file_ext ("blog/documents", "js", os.path.join(destination, "blog/documents"))
    cpf.copy_file_ext ("blog/documents", "json", os.path.join(destination, "blog/documents"))
    cpf.copy_file_ext ("blog/documents", "css", os.path.join(destination, "blog/documents"))
    cpf.copy_file_contains ("blog/documents", "study", os.path.join(destination, "blog/documents"))

    # process keywords
    
    add = build_process_all_pages(res, frequence_keywords = 2, siteFolder=os.path.join(destination, "blog"))
    
    cpf.copy_file_contains ("blog/notebooks", ".html", os.path.join(destination, "blog/notebooks"), doFTP = False)
    cpf.copy_file_contains ("blog/notebooks", ".ipynb", os.path.join(destination, "blog/notebooks"), doFTP = False)
        
    # update copyDates and copiedFiles

    for file in add :
        if "copy_site." not in file:
            cpf.add_if_modified (file)
            
    nbcopyfile = 0
    for _,reason in sorted(cpf.modifiedFile) : 
        if not "copy_site" in _ :
            nbcopyfile += 1
            print ("*",_, reason)
    print("number of files to copy:", nbcopyfile)
            
    # do not update this
    forbid = []

    if len(cpf.modifiedFile) > 0 :
        
        # checking that username is not in the file
        nbch = 0
        usernames = [os.environ["USERNAME"].lower()]
        for file, reason in sorted(cpf.modifiedFile) :
            ext = os.path.splitext(file)[-1] 
            
            if ext in [".log", ".doctree"] :
                print("skipping ", file)
                continue
            
            if os.stat(file).st_size < 2**25 and ext.lower() not in \
                    [".mp3", ".zip", ".gif", ".dll", ".exe", ".msi", 
                     ".eot", ".ttf", ".woff", ".mp4",
                     ".xlsx", ".7z", ".avi", ".xlsm",
                     ".gz", ".inv", ".pdf", ".png", ".jpg", ".jpeg"] :
                content  = None
                contentu = None
                encoding = None
                try :
                    with open(file, "r") as f: 
                        contentu = f.read()
                        content = contentu.lower()
                        encoding = None
                except UnicodeDecodeError:
                    try:
                        with open(file, "r", encoding="utf8") as f: 
                            contentu = f.read()
                            content = contentu.lower()
                            encoding = "utf8"
                    except :
                        pass
                except PermissionError:
                    print("permission error for ", file)
                        
                if content == None :
                    print("unable to check alias in ",file)
                else :
                    # ####################################
                    ###############################################
                    ############ replacements #####################
                    ###############################################
                    # ####################################
                    modif = 0
                    for username in usernames :
                        for substr,reps in [("c-3a-5c" + username,              "c-3a-5cxxx"),
                                    (r"c:\%s\__home_\_data" % username,         "root"),
                                    (r"C:\%s\__home_\_data" % username,         "root"),
                                    (r"C:\Users\%s\AppData\Local" % username,   "uroot"),
                                    ("sr1.dzr323.dza.datazoomr.com",            "hadoop.url"),
                                    ("c:/%s/__home_/_data/" % username,         "root"),
                                    ("C:/%s/__home_/_data/" % username,         "root"),
                                    ("graph for username:",                     "graph:"),
                                    ("username Directory Reference",            "Directory Reference"),
                                    #(username,                             "XXXX"),
                                    ("__GOOGLEID__",                            googleid)
                                    ] :
                            if substr in contentu :
                                contentu = contentu.replace(substr,reps)
                                modif += 1
                    
                    content = contentu.lower()
                    if modif > 0 :
                        if encoding is None :
                            with open(file, "w") as f : 
                                f.write(contentu)
                        else :
                            with open(file, "w", encoding=encoding) as f : 
                                f.write(contentu)
                        
                    nbch += 1
                    if username != "xavie" and username in content:
                        print("-- alias {0} was found in [lower] {1}".format(username, os.path.abspath(file)))
                        lines = content.split("\n")
                        linesuu = contentu.split("\n")
                        nbf = 0
                        for i,l__ in enumerate(zip(lines,linesuu)):
                            l,lu = l__
                            if username in l :
                                print("    {0} was found in line {1} : {2}".format(username, i,lu.strip("\r\n")))
                                nbf += 1
                                if nbf > 2 : 
                                    print("    ...")
                                    break
                        forbid.append(file)
                        
        print("number of checked files:", nbch)
        
        issues = []
        processed = []
        
        print("loginame", loginame)
        print("password", password)
        ftp = TransferFTP(ftp_site, loginame, password, fLOG = print)  
        nbproc = 0

        # on trie par taille pour faire les plus gros en dernier
        def sizef(name):
            ext = os.path.splitext(name)[-1]
            if ext in [".html", ".js", ".png", ".css", ".ico", ".py", ".ipynb"] :
                return 0
            else :
                return os.stat(name).st_size
        
        allfiles = [(sizef(file),file, reason) for file, reason in cpf.modifiedFile]
        allfiles.sort()
        
        for siz, file, reason in allfiles:
            
            skip = False
            for _ in forbid :
                if _ in file :
                    fLOG(" ** skipping (1)", file)
                    skip = True
                    break
            if skip :
                continue
            
            if "copy_site" in file :
                skip = True
            
            if skip or os.path.isdir(file):
                fLOG(" ** skipping (2)", file)
                continue 
                
            temp = os.path.split(file)
            d = temp[0]
            if file.startswith(destination):
                d = temp[0].replace(destination, "")
            path = "www/htdocs"
            
            if len(d) > 0 :
                path += "/" + d.replace("\\", "/")
                
            ftp_dest = os.path.split(file)[-1]
            r = ftp.transfer (file, path, ftp_dest)
            print("[upload]", file, "to", "/".join([path, ftp_dest]))
                
            if r : 
                processed.append(file)
                cpf.update_copied_file(file)
                cpf.save_dates(checkfile=processed)
                
            nbproc += 1
            if nbproc % 20 == 0 or siz > 2**25 :
                fLOG("******* processed", nbproc, "/", len(cpf.modifiedFile), " size", siz)
        
        try :
            ftp.close()
        except :
            print ("unable to close FTP connection using ftp.close")
            
        for file in issues :
            print ("ISSUES",file)
            
    html = os.listdir(".")
    for f in html :
        if ".html" in f : os.remove(f)
        
if __name__ == "__main__":
    copy_site()
    
