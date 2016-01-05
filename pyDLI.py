import os
import sys

from lxml import etree
from urlparse import urlparse

metadata = {}
havepdf = 0

def download_pdf(link, barcode):
  page = './' + barcode + '/__' + barcode
  os.system('wget %s -O %s > /tmp/%s 2>&1' % (link, page, barcode))
  
  with open(page, 'r') as metafile:
      data = metafile.read().replace('\n', '')

  html = etree.HTML(data)                                                     
  meta = html.xpath('//head/meta')

  for i in range (0, len(meta)):
    if meta[i].get('name') == 'citation_pdf_url':
      return meta[i].get('content')


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
  global havepdf

  div = td.xpath('div')
  font = div[0].xpath('font')
  a = font[0].xpath('a')

  link = a[0].get('href')
  print link

  if link.find('path1') != -1:
    metadata['link'] = urlparse(link).query.split('=')[1].split('&')[0]
  else:
    metadata['link'] = link
    print 'pdf download'
    havepdf = 1


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
      get_link(td[1])
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
  global havepdf
  
  for i in range (1, len(sys.argv)):
    havepdf = 0

    os.system('mkdir -p ./%s' % sys.argv[i])
    os.system('mkdir -p ./pdfs')
    download_meta(sys.argv[i])

    print '%-10s = %s' % ('Title', metadata['Title'])
    print '%-10s = %s' % ('Author', metadata['Author1'])
    print '%-10s = %s' % ('Pages', metadata['TotalPages'])

    pdfpath = './pdfs/' + sys.argv[i] + '.pdf'
    
    if havepdf == 0:
      download_pages(metadata['link'], metadata['TotalPages'], sys.argv[i])

      tifpath = './' + sys.argv[i]

      print 'Merging pages ...'
      os.system('tiffcp %s/0*.tif %s/result.tif > /tmp/%s 2>&1' % (tifpath, tifpath, sys.argv[i]))
      os.system('tiff2pdf %s/result.tif -o %s -p A2 -F' % (tifpath, pdfpath))
    else:
      link = download_pdf(metadata['link'], sys.argv[i])
      link = link + '?sequence=1'
      os.system('wget %s -O %s' % (link, pdfpath))


if __name__ == '__main__':
  main()

