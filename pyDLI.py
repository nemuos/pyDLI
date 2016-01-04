import os
import sys

def download(link, pages):
  for i in range (0, pages +1):
    if i < 9:
      path = 'http://www.dli.gov.in/' + link + '/PTIFF/0000000' + str(i) + '.tif';
    elif i > 9 and i < 100:
      path = 'http://www.dli.gov.in/' + link + '/PTIFF/000000' + str(i) + '.tif';
    else:
      path = 'http://www.dli.gov.in/' + link + '/PTIFF/00000' + str(i) + '.tif';

    os.system('wget %s' % path)


def main():
  link = sys.argv[1]
  pages = int(sys.argv[2])
  download(link, pages)
  os.system('tiffcp *.tif result.tif')
  os.system('tiff2pdf result.tif -o result.pdf -p A2 -F')
  

if __name__ == '__main__':
  main()

