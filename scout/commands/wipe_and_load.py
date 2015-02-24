#!/usr/bin/env python
# encoding: utf-8
"""
wipe_and_load.py

Script to clean the database and reload it with new data.

Created by Måns Magnusson on 2015-01-14.
Copyright (c) 2015 __MoonsoInc__. All rights reserved.

"""


from __future__ import absolute_import, unicode_literals, print_function

import sys
import os

import click

import scout

from tempfile import NamedTemporaryFile
from pprint import pprint as pp
from pymongo import MongoClient, Connection
from mongoengine import connect, DoesNotExist
from mongoengine.connection import _get_db

from scout.commands.wipe_mongo import wipe_mongo
from scout.commands.load_mongo import load_mongo

from scout.ext.backend import ConfigParser

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(scout.__file__), '..'))

@click.command()
@click.option('-config', '--config_file',
                nargs=1,
                type=click.Path(exists=True),
                default=os.path.join(BASE_PATH, 'configs/config_test.ini'),
                help="Path to the config file for loading the variants. Default configs/config_test.ini"
)
@click.option('-db', '--mongo-db',
                default='variantDatabase'
)
@click.option('-u', '--username',
                type=str
)
@click.option('-p', '--password',
                type=str
)
@click.option('-port', '--port',
                default=27017,
                help='Specify the port where to look for the mongo database.'
)
@click.option('-h', '--host',
                default='localhost',
                help='Specify the host where to look for the mongo database.'
)
@click.option('-v', '--verbose',
                is_flag=True,
                help='Increase output verbosity.'
)
@click.pass_context
def wipe_and_load(ctx, config_file, mongo_db, username, password, port, host,
                  verbose):
  """
  Drop the mongo database given and rebuild it again with the test cases from 
  tests/vcf_data/.
  """
  
  if not mongo_db:
    print("Please specify a database to wipe and populate with flag"
          " '-db/--mongo-db'.")
    sys.exit(0)
  
  ######## Wipe cases and variants from the existing database ######
  ctx.invoke(wipe_mongo, 
                  mongo_db=mongo_db, 
                  username=username, 
                  password=password, 
                  port=port, 
                  verbose=verbose
                  )
  
  ######## Update the paths from the config file #########
  
  # Start with the clinical variants for test case 1:
  
  scout_config_file_1_clinical = os.path.join(
                                BASE_PATH,
                                'tests/vcf_examples/1/scout_config_test_clinical.ini'
                                )
  clinical_1_config = ConfigParser(scout_config_file_1_clinical)
  
  clinical_1_config['vcf'] = os.path.join(
                                          BASE_PATH,
                                          clinical_1_config['vcf']
                                        )
  
  clinical_1_config['ped'] = os.path.join(
                                          BASE_PATH,
                                          clinical_1_config['ped']
                                        )
  
  clinical_1_config['madeline'] = os.path.join(
                                          BASE_PATH,
                                          clinical_1_config['madeline']
                                        )
  
  # Save the updated information to a temporary file:
  
  case_1_clinical_temp = NamedTemporaryFile(delete=False)
  case_1_clinical_temp.close()
  clinical_1_config.filename = case_1_clinical_temp.name
  clinical_1_config.write()
  
  # pp(dict(clinical_1_config))
  # sys.exit()
  # Load the family 1 clinical data:
  ctx.invoke(load_mongo,
                  scout_config_file = case_1_clinical_temp.name,
                  config_file=config_file, 
                  family_type='cmms', 
                  mongo_db=mongo_db, 
                  username=username,
                  variant_type='clinical', 
                  password=password, 
                  port=port, 
                  host=host, 
                  verbose=verbose
                  )
  
  scout_config_file_1_research = os.path.join(
                                BASE_PATH,
                                'tests/vcf_examples/1/scout_config_test_research.ini'
                                )
  
  research_1_config = ConfigParser(scout_config_file_1_research)
  
  research_1_config['vcf'] = os.path.join(
                                          BASE_PATH,
                                          research_1_config['vcf']
                                        )
  
  research_1_config['ped'] = os.path.join(
                                          BASE_PATH,
                                          research_1_config['ped']
                                        )
  
  research_1_config['madeline'] = os.path.join(
                                          BASE_PATH,
                                          research_1_config['madeline']
                                        )
  
  # Save the updated information to a temporary file:
  
  case_1_research_temp = NamedTemporaryFile(delete=False)
  case_1_research_temp.close()
  research_1_config.filename = case_1_research_temp.name
  research_1_config.write()
  
  # Load the family 1 clinical data:
  ctx.invoke(load_mongo,
                  scout_config_file = case_1_research_temp.name,
                  config_file=config_file, 
                  family_type='cmms', 
                  mongo_db=mongo_db, 
                  username=username,
                  variant_type='research', 
                  password=password, 
                  port=port, 
                  host=host, 
                  verbose=verbose
                  )
  
  
  
  scout_config_file_coriell_clinical = os.path.join(
                                BASE_PATH,
                                'tests/vcf_examples/P575_coriell/scout_config_test_clinical.ini'
                                )
  
  clinical_coriell_config = ConfigParser(scout_config_file_coriell_clinical)
  
  clinical_coriell_config['vcf'] = os.path.join(
                                          BASE_PATH,
                                          clinical_coriell_config['vcf']
                                        )
  
  clinical_coriell_config['ped'] = os.path.join(
                                          BASE_PATH,
                                          clinical_coriell_config['ped']
                                        )
  
  clinical_coriell_config['madeline'] = os.path.join(
                                          BASE_PATH,
                                          clinical_coriell_config['madeline']
                                        )
  
  # Save the updated information to a temporary file:
  
  coriell_clinical_temp = NamedTemporaryFile(delete=False)
  coriell_clinical_temp.close()
  clinical_coriell_config.filename = coriell_clinical_temp.name
  clinical_coriell_config.write()
  
  # Load the coriell family clinical data:
  ctx.invoke(load_mongo,
                  scout_config_file = coriell_clinical_temp.name,
                  config_file=config_file, 
                  family_type='cmms', 
                  mongo_db=mongo_db, 
                  username=username,
                  variant_type='clinical', 
                  password=password, 
                  port=port, 
                  host=host, 
                  verbose=verbose
                  )
  
  
  scout_config_file_coriell_research = os.path.join(
                                BASE_PATH,
                                'tests/vcf_examples/P575_coriell/scout_config_test_research.ini'
                                )
  
  
  research_coriell_config = ConfigParser(scout_config_file_coriell_research)
  
  research_coriell_config['vcf'] = os.path.join(
                                          BASE_PATH,
                                          research_coriell_config['vcf']
                                        )
  
  research_coriell_config['ped'] = os.path.join(
                                          BASE_PATH,
                                          research_coriell_config['ped']
                                        )
  
  research_coriell_config['madeline'] = os.path.join(
                                          BASE_PATH,
                                          research_coriell_config['madeline']
                                        )
  
  # Save the updated information to a temporary file:
  
  coriell_research_temp = NamedTemporaryFile(delete=False)
  coriell_research_temp.close()
  research_coriell_config.filename = coriell_research_temp.name
  research_coriell_config.write()
  
  # Load the family 1 clinical data:
  ctx.invoke(load_mongo,
                  scout_config_file = coriell_research_temp.name,
                  config_file=config_file, 
                  family_type='cmms', 
                  mongo_db=mongo_db, 
                  username=username,
                  variant_type='research', 
                  password=password, 
                  port=port, 
                  host=host, 
                  verbose=verbose
                  )
  
  

if __name__ == '__main__':
    wipe_and_load()
