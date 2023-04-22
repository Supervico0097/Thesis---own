from datetime import datetime, timedelta


GLOBAL_START_DATE = datetime.strptime('2020-01-01', '%Y-%m-%d')
GLOBAL_END_DATE = datetime.strptime('2021-12-31', '%Y-%m-%d')

result = GLOBAL_START_DATE + timedelta(days=7)
GLOBAL_END_DATE
