import os
import sys

from lxml import etree
from urlparse import urlparse

#metadata = {}
#havepdf = 0
#
#def download_pdf(link, barcode):
#  page = './' + barcode + '/__' + barcode
#  os.system('wget %s -O %s > /tmp/%s 2>&1' % (link, page, barcode))
#  
#  with open(page, 'r') as metafile:
#      data = metafile.read().replace('\n', '')
#
#  html = etree.HTML(data)                                                     
#  meta = html.xpath('//head/meta')
#
#  for i in range (0, len(meta)):
#    if meta[i].get('name') == 'citation_pdf_url':
#      return meta[i].get('content')
#
#
#def download_pages(link, pages, barcode):
#  print 'Downloading pages ... %4s/%-4s' % (0, pages),
#  sys.stdout.flush()
#  
#  pages = int(pages)
#  for i in range (1, pages + 1):
#    if i <= 9:
#      page = '0000000' + str(i) + '.tif' 
#    elif i > 9 and i < 100:
#      page = '000000' + str(i) + '.tif' 
#    else:
#      page = '00000' + str(i) + '.tif' 
#
#    url = 'http://www.dli.gov.in/' + link + '/PTIFF/' + page
#    tifpath = './' + barcode + '/' + page
#
#    if not os.path.isfile(tifpath):
#      os.system('wget %s -O %s > /tmp/%s 2>&1' % (url, tifpath, barcode))
#
#    print '\b\b\b\b\b\b\b\b\b\b\b',
#    print '%4s/%-4s' % (i, pages),
#    sys.stdout.flush()
#
#  print ''
#
#
#def get_link(td):
#  global havepdf
#
#  div = td.xpath('div')
#  font = div[0].xpath('font')
#  a = font[0].xpath('a')
#
#  link = a[0].get('href')
#  print link
#
#  if link.find('path1') != -1:
#    metadata['link'] = urlparse(link).query.split('=')[1].split('&')[0]
#  else:
#    metadata['link'] = link
#    print 'pdf download'
#    havepdf = 1
#
#
def extract_meta(metapath):
  with open(metapath, 'r') as metafile:
    data = metafile.read().replace('\n', '')

  html = etree.HTML(data)                                                     
  tr = html.xpath('//table/tr')

  for i in range (0, len(tr)):
    td = tr[i].xpath('td')
    if td:
      a = td[0].xpath('a')
      if a:
        metaData = a[0].attrib['href']
        metaTokens = metaData.split('&')
        for j in range(0, len(metaTokens)):
          if metaTokens[j].startswith('barcode'):
            print 'barcode = %s' % (metaTokens[j].split('=')[1])
          if metaTokens[j].startswith('pages'):
            print 'pages = %s' % (metaTokens[j].split('=')[1])
          if metaTokens[j].startswith('url'):
            print 'url = %s' % (metaTokens[j].split('=')[1])
        print ''
        print ''


def download_meta():
  print 'Downloading metadata ...'
  #totalBooks = 25176
  totalBooks = 25
  perPage = 25
  for i in range(0, totalBooks/perPage):
    listStart = i * 25
    metaUrl = 'http://dli.gov.in/cgi-bin/advsearch_db.cgi?perPage=25&listStart=' + str(listStart) + '&r1=V1&title1=&author1=&year1=&year2=&subject1=Any&language1=Bengali&scentre=Any&search=Search HTTP/1.1\\r\\n'
    metaPath = './metafile'
    os.system('wget "%s" -O %s' % (metaUrl, metaPath))
    extract_meta(metaPath)


def main():
  download_meta()

#  print '____________________________________________________________'
#  print '%-10s = %s' % ('Title', metadata['Title'])
#  print '%-10s = %s' % ('Author', metadata['Author1'])
#  print '%-10s = %s' % ('Pages', metadata['TotalPages'])
#
#  pdfpath = './pdfs/' + sys.argv[i] + '.pdf'
#  if os.path.isfile(pdfpath):
#    continue
#
#  if havepdf == 0:
#    download_pages(metadata['link'], metadata['TotalPages'], sys.argv[i])
#
#    tifpath = './' + sys.argv[i]
#
#    print 'Merging pages ...'
#    os.system('tiffcp %s/0*.tif %s/result.tif > /tmp/%s 2>&1' % (tifpath, tifpath, sys.argv[i]))
#    os.system('tiff2pdf %s/result.tif -o %s -p A2 -F' % (tifpath, pdfpath))
#  else:
#    link = download_pdf(metadata['link'], sys.argv[i])
#    link = link + '?sequence=1'
#    os.system('wget %s -O %s' % (link, pdfpath))
# 
#  #os.system('rm -rf ./%s' % sys.argv[i])
#  print '____________________________________________________________'


if __name__ == '__main__':
  main()

