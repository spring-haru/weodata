import os
if not os.getenv('PYTHONIOENCODING', None):
    os.environ['PYTHONIOENCODING'] = 'utf_8'

import csv
import urllib.request
import logging
import codecs
import sys
import pandas as pd
import numpy as np
import shutil


logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

# Specifying the locale of the source
import locale
locale.setlocale(locale.LC_ALL, 'en_US')


def url_generator(version, base_url):
    tmp_url = base_url + str(version) + '/01/weodata//WEOApr' + str(version) + 'all.xls'
    return tmp_url

# directory/file where files are stored
fp = './archive_weo/imf-weo.tsv'

def download(version, base_url):
    logger.info('Retrieving source database ...')
    f=urllib.request.urlopen(url_generator(version,base_url))
    output=f.read().decode('cp1252')

    path=os.path.dirname(fp)
    if not os.path.exists(path):
        os.makedirs(path)

    with codecs.open(fp, "w", "utf-8") as temp:
        temp.write(output)


def f_open(fn):
    if sys.version_info >= (3,0,0):
        f = open(fn, 'w', newline='', encoding='utf-8')
    else:
        f = open(filename, 'wb')
    return f



def extract():
    reader = csv.DictReader(open(fp, encoding='utf-8'), delimiter='\t')
    indicators = {}
    WEOcountry_names=dict()
    WEOcountry_codes=dict()
    values = []

    years = reader.fieldnames[9:-1]

    for count, row in enumerate(reader):
        # last 2 rows are blank/metadata
        # so get out when we hit a blank row
        if not row['Country']:
            break

        indicators[row['WEO Subject Code']] = [
            row['Subject Descriptor']+' ({0}; {1})'.format(row['Units'],row['Scale']),
            row['Subject Notes']
            ]

        # not sure we really need given iso is standard
        # just for double check on data integrity and names encoding
        if row['ISO'] not in WEOcountry_names:
            WEOcountry_names[row['ISO']] = row['Country']
            try:
                WEOcountry_codes[row['ISO']] = row['WEO Country Code']
            except:
                print(row)
                break;

        notes = row['Country/Series-specific Notes']

        newrow = {
            'Country': row['ISO'],
            'Indicator': row['WEO Subject Code'],
            'Year': None,
            'Value': None
            }
        for year in years:
            if row[year] == 'n/a':
                row[year] = np.nan
            if row[year] == '--':
                row[year] = np.nan
            tmprow = dict(newrow)
            try:
                tmprow['Value'] = locale.atof (row[year] )          # Converting "1,033.591" to 1033.591
            except:
                tmprow['Value'] = row[year]
            tmprow['Year'] = year
            values.append(tmprow)

        # TODO: indicate whether a value is an estimate using
        # 'Estimates Start After'

    outfp = 'archive_weo/indicators.csv'

    path=os.path.dirname(outfp)
    if not os.path.exists(path):
        os.makedirs(path)

    writer = csv.writer(f_open(outfp))
    indheader = ['id', 'title', 'description']
    writer.writerow(indheader)
    for k in sorted(indicators.keys()):
        writer.writerow( [k] + indicators[k] )

    outfp = 'archive_weo/country.csv'
    writer = csv.writer(f_open(outfp))
    header = ['ISO', 'WEO', 'Name']
    writer.writerow(header)
    for k in sorted(WEOcountry_names.keys()):
        writer.writerow( [k] + [WEOcountry_codes[k],WEOcountry_names[k],])

    outfp = 'archive_weo/values.csv'
    f = f_open(outfp)
    writer = csv.writer(f)
    header = ['Country', 'Indicator', 'Year', 'Value']
    writer = csv.DictWriter(f, header)
    writer.writeheader()
    writer.writerows(values)

    # logger.info('Completed data extraction (^_^)')


def load(version=2019,
         base_url='http://www.imf.org/external/pubs/ft/weo/',
         multi_index=False,description=False,country=False):
    """
    Load the IMF World Economic Outlook as a pandas DataFrame object.

    Parameters
    ----------
        version : int, optional(default=2019)
            Version number for IMF World Economic Outlook data.
        base_url : str, optional(default='http://www.imf.org/external/pubs/ft/weo/')
            Part of url to use for the download.
        multi_index : boolean, optional (default=False)
            MultiIndex with countrycode and year as row labels
        description : boolean, optional (default=False)
            Shows variable definitions
        country : boolean, optional (default=False)
            Shows the list of full country names

    Returns
    -------
        pd.DataFrame containing the IMF World Economic Outlook data.

        In addition to the above, a folder './archive_weo/' is created with two files (overritten if exist):
            * indicators.csv (description of variables)
            * country.csv (list of full country names)

    """
    download(version, base_url)
    extract()
    _df = pd.read_csv('./archive_weo/values.csv')
    _country = pd.read_csv('./archive_weo/country.csv')
    _indicators = pd.read_csv('./archive_weo/indicators.csv').set_index('id')

    weo_data_multi = _df.set_index(['Country', 'Year', 'Indicator'])['Value'].unstack('Indicator').sort_index(1)
    weo_data_multi.index.names = (None,None)
    weo_data_multi.columns.name = None

    weo_data = weo_data_multi.rename_axis(['Country','Year']).reset_index()

    # remove file
    os.remove(fp)
    os.remove('./archive_weo/values.csv')

    if (country == True) & (description == False) & (multi_index == False):
        return _country
    elif (country == False) & (description == True) & (multi_index == False):
        return _indicators
    elif (country == False) & (description == False) & (multi_index == True):
        return weo_data_multi
    elif (country == False) & (description == False) & (multi_index == False):
        return weo_data

# df = load(multi_index=False)
# df.head()
