import pytest
import pandas as pd
from python_script import load_data
from python_script import rename_data
def test_load_dataframe():
  input="C:/Users/maild/Desktop/data/Apartment Building Evaluation.csv"
  out= load_data(input)
  assert isinstance(out, pd.DataFrame) == True, "The variable is not a DataFrame"

def test_rename_results():
  data_to_rename=pd.DataFrame({'APPLE':[31,54,88,98],'Orange':[54,76,99,65]})
  renamed_data=rename_data(data_to_rename)
  assert all(col_name.lower() in renamed_data.columns for col_name in data_to_rename.columns)

