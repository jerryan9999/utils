import pymongo
import argparse
from datetime import datetime, date, time, timedelta

airbnb_input = ('123.207.166.66', None, 'Airbnb2')
airbnb_output = ('123.207.166.66', None, 'Airbnb2')
ONE_DAY = timedelta(days=1)

# command line argument config
def parse_args():
  parser = argparse.ArgumentParser(description="drop airbnb history data")
  parser.add_argument('--start', type=str, help="starting date,for example:2017-01-01")
  parser.add_argument('--end', type=str, help="end date,for example:2017-01-10")
  args = parser.parse_args()
  return args

class mongo_database():
  def __init__(self, config):
    self.client = None
    self.config = config

  def __enter__(self):
    host, replicaSet, dbName = self.config
    self.client = pymongo.MongoClient(
      host,
      27017,
      replicaset=replicaSet,
      readPreference='secondaryPreferred'
    )
    return self.client
  def __exit__(self, *args):
    self.client.close()

def get_collection_name_from_db(airbnb_input):
  with mongo_database(config=airbnb_input) as client:
    database = client[airbnb_input[2]]
    daily_collection = set(c for c in database.collection_names() if c!='RoomID')
    return daily_collection

def del_period_of_time_data(start_time, end_time, daily_collection):
  daily_collection = get_collection_name_from_db(airbnb_input)
  with mongo_database(config=airbnb_input) as client:
    database = client[airbnb_input[2]]
    while start_time <= end_time:
      collection_name = 'Airbnb-' + str(start_time)
      print(collection_name)
      if collection_name in daily_collection:
        database.drop_collection(collection_name)
      start_time += ONE_DAY

def del_one_collection_data(date_time, daily_collection):
  collection_name = 'Airbnb-' + str(date_time-30*ONE_DAY)
  print(collection_name)
  with mongo_database(config=airbnb_input) as client:
    database = client['airbnb_input']
    if collection_name in daily_collection:
      database.drop_collection(collection_name)

def str_convert_time(str_time):
  # str_time example: 2017-01-01
  date_time = datetime.strptime(str_time, '%Y-%m-%d').date()
  return date_time

if __name__ == '__main__':
  args = parse_args()

  # (for historical process) start_date and end_date from command line argument 
  start_date = args.start
  end_date = args.end

  # get all collection names
  daily_collection = get_collection_name_from_db(airbnb_input)

  if not (start_date and end_date):
    today = date.today()
    del_one_collection_data(today,daily_collection)
  else:
    start_time = str_convert_time(args.start)
    end_time = str_convert_time(args.end)
    del_period_of_time_data(start_time, end_time, daily_collection)    


