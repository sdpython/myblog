import clr
clr.AddReference("csharp_office_helper")
from csharp_office_helper import WordHelper

file1 = "liste_projets_dupre_2013-2014.docx"
file2 = "file.pdf"
WordHelper.SaveAsPDF(file1, file2)
