import urllib.request
import re
import os
import argparse
parser=argparse.ArgumentParser(description='Input Conference (C) and Year (Y)')
parser.add_argument('C',type=str,default='CVPR',
                    help='a name of CVPR, ICCV or ECCV')
parser.add_argument('Y',type=int,default=2020,
                    help='the year of conference')
#parser.print_help()
args=parser.parse_args()

def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    html = html.decode('utf-8')
    return html

def download_file(download_url, file_name):
    response = urllib.request.urlopen(download_url)
    file = open(file_name, 'wb')
    file.write(response.read())
    file.close()
    print("Completed")

Conference=args.C#'ICCV'
Year=args.Y#2019
save_path = '%s%d'%(Conference,Year)
if not os.path.exists(save_path):
    os.mkdir(save_path)
url = 'http://openaccess.thecvf.com/%s%d.py'%(Conference,Year)

html = getHtml(url)
compile_text=r'\b\?day=[0-9][0-9][0-9][0-9]\-[0-9][0-9]\-[0-9][0-9]\b'#正则化模式1匹配日子
compile_paper=r'\bcontent_.*paper\.pdf\b'#正则化模式
parttern = re.compile(compile_text)
url_list = parttern.findall(html)
paper_url_list=[]
if url_list.__len__()==0:
    parttern = re.compile(compile_paper)
    paper_url_list.extend(parttern.findall(html))
else:
    for suburl in url_list:
        html = getHtml(url +suburl)
        parttern = re.compile(compile_paper)
        url_temp = parttern.findall(html)
        paper_url_list.extend(url_temp)

for url in paper_url_list:
    name = url.split('/')[-1]
    file_name = os.path.join(save_path , name)
    download_file('http://openaccess.thecvf.com/'+url, file_name)