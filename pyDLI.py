import os
import sys

from lxml import etree
from urlparse import urlparse

metadata = {}

def download_pages(link, pages, barcode):
  print 'Downloading pages ...'
  
  pages = int(pages)
  for i in range (1, pages + 1):
    if i <= 9:
      page = '0000000' + str(i) + '.tif' 
    elif i > 9 and i < 100:
      page = '000000' + str(i) + '.tif' 
    else:
      page = '00000' + str(i) + '.tif' 

    url = 'http://www.dli.gov.in/' + link + '/PTIFF/' + page
    tifpath = './' + barcode + '/' + page

    if not os.path.isfile(tifpath):
      os.system('wget %s -O %s > /tmp/%s 2>&1' % (url, tifpath, barcode))


def get_link(td):
  div = td.xpath('div')
  font = div[0].xpath('font')
  a = font[0].xpath('a')

  o = urlparse(a[0].get('href'))
  return o.query.split('=')[1].split('&')[0]


def extract_meta(metapath):
  with open(metapath, 'r') as metafile:
      data = metafile.read().replace('\n', '')

  html = etree.HTML(data)                                                     
  tr = html.xpath('//table/tr')

  for i in range (0, len(tr)):
    td = tr[i].xpath('td')
    
    div = td[0].xpath('div')
    strong = div[0].xpath('strong')
    font = strong[0].xpath('font')
    
    if font[0].text == 'Read Online':
      metadata['link'] = get_link(td[1])
    else:
      div = td[1].xpath('div')
      font2 = div[0].xpath('font')
      metadata[font[0].text] = font2[0].text


def download_meta(barcode):
  print 'Downloading metadata ...'
  metaurl = 'http://www.dli.ernet.in/cgi-bin/DBscripts/allmetainfo.cgi?barcode=' + barcode
  metapath = './' + barcode + '/' + barcode
  os.system('wget %s -O %s > /tmp/%s 2>&1' % (metaurl, metapath, barcode))

  extract_meta(metapath)


def main():
  for i in range (1, len(sys.argv)):
    os.system('mkdir -p ./%s' % sys.argv[i])
    os.system('mkdir -p ./pdfs')
    download_meta(sys.argv[i])

    print '%-10s = %s' % ('Title', metadata['Title'])
    print '%-10s = %s' % ('Author', metadata['Author1'])
    print '%-10s = %s' % ('Pages', metadata['TotalPages'])
    
    download_pages(metadata['link'], metadata['TotalPages'], sys.argv[i])

    tifpath = './' + sys.argv[i]
    pdfpath = './pdfs/' + sys.argv[i] + '.pdf'

    print 'Merging pages ...'
    os.system('tiffcp %s/0*.tif %s/result.tif > /tmp/%s 2>&1' % (tifpath, tifpath, sys.argv[i]))
    os.system('tiff2pdf %s/result.tif -o %s -p A2 -F' % (tifpath, pdfpath))


if __name__ == '__main__':
  main()

