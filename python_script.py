import pandas as pd
#using `matplotlib`
import matplotlib.pyplot as plt
import yaml
import argparse
import logging
parser = argparse.ArgumentParser(description='Dataset analysis script')
parser.add_argument('Filename', type=str, help='Path to the configuration file')
parser.add_argument('--verbose', '-v', action='store_true')
parser.add_argument('--quiet', '-q', action='store_true')
args = parser.parse_args()
config_file=['user_config.yml']
config={}
if args.verbose:
    logging_level = logging.INFO
elif args.quiet:
    logging_level = logging.ERROR
else:
    logging_level = logging.WARNING
# Determine logging level based on arguments
logging_level = logging.DEBUG if args.verbose else logging.WARNING

# Initialize logging module
logging.basicConfig(
    level=logging_level, 
    handlers=[logging.StreamHandler(), logging.FileHandler('my_python_analysis.log')],
)
def load_data(dataset_path):
    try:
        # Load the dataset
        shelter_data = pd.read_csv(dataset_path)
        logging.info(f'Successfully loaded {dataset_path}')
    except Exception as e:
        logging.error('Error loading dataset', exc_info=e)
        raise e
    return shelter_data
def rename_data(data_to_rename):
     if data_to_rename is None:
          raise ValueError('No columns found')
     shelter_data=data_to_rename.rename(columns=str.lower)
     return shelter_data
# Load YAML config
for this_config_file in config_file:
        with open(this_config_file, 'r') as file:
                config = yaml.safe_load(file)
                config.update(config)
# Read the dataset path from config
shelter_data = load_data(config['dataset'])
shelter_data=rename_data(shelter_data)
#Column names info, dtypes of Occupancy_date is object, Each column's NaN count displays beside the column name
shelter_data.info()
#shape of the DataFrame
shelter_data.shape
shelter_data.head()
#Summary statistics for the data.
shelter_data.describe()  #For numeric columns: the max, min, mean, and median
#For text columns:the most common value and unique values count
shelter_data.describe(include=['object']) 
#Date of occupancy_date field seems unexpected
shelter_data['occupancy_date']=pd.to_datetime(shelter_data['occupancy_date'])
shelter_data['occupancy_date']
#Rename one or more columns in the DataFrame.
shelter_data=shelter_data.rename(columns={'sector':'sector_name','program_area':'program_location'})
shelter_data.columns  
#Select a single column and find its unique values.
shelter_data['overnight_service_type'].unique()
#Select a single text/categorical column and find the counts of its values.
shelter_data['location_address'].value_counts()
#Convert the data type of at least one of the columns. If all columns are typed correctly, convert one to `str` and back.
shelter_data['shelter_id'].dtype
# shelter_data['occupied_beds'] = pd.to_numeric(shelter_data['occupied_beds'], errors='coerce').astype('Int64')
try:
    shelter_data['shelter_id'] = shelter_data['shelter_id'].astype('str')
except ValueError as e:
    e.add_note(f"The column {shelter_data['shelter_id']} is not an integer")
    raise
shelter_data['shelter_id']
#The Data type of the column shelter_id is Object
shelter_data['shelter_id'].dtype
#Converting the column back to integer type.
shelter_data['shelter_id'] = shelter_data['shelter_id'].astype('int')
shelter_data['shelter_id'].dtype
#Write the DataFrame to a different file format than the original.
shelter_data_summary={}
# Save to new dataset as defined in config
shelter_data.to_excel('C:/Users/maild/Desktop/data/python_script/RAJASEKHAR_DELPHIN_python_assignment2_proc.xlsx', index=False)
#Creating a new column month from the occupancy date
# Check if month values are between 1 and 12
assert shelter_data["occupancy_date"].dt.month.between(1, 12).all(), "Month values should be between 1 and 12"
shelter_data["month"]=shelter_data["occupancy_date"].dt.strftime("%b")
#Creating a new column called Total Occupied and unoccupied rooms in total available rooms column
shelter_data["total_available_rooms"] = (shelter_data["occupied_rooms"]+shelter_data["unoccupied_rooms"])
shelter_data[["occupied_rooms", "unoccupied_rooms","total_available_rooms"]].head(10)
# Replace text in a column
shelter_data["organization_name"].unique()
shelter_data["organization_name"]=(shelter_data["organization_name"].str.replace(r'\bInc', 'Incorporation', regex=True))
shelter_data["organization_name"].unique()
# Removing a column program_id

shelter_data=shelter_data.drop(columns="program_id")
shelter_data.columns
shelter_data["service_user_count"].unique()
#Extraction of subset 1 using .query()----> service_user_count which has more than 500 count 
shelter_data_subset1=shelter_data.query('service_user_count>500')[['occupancy_date', 'organization_name', 'service_user_count']]
shelter_data_subset1.head(10)
#Extraction of subset 2 using .loc[]----> service_user_count which has less than 500 count
shelter_data_subset2 = shelter_data.loc[shelter_data['service_user_count'] < 500, ['occupancy_date', 'organization_name','location_address', 'service_user_count']]
shelter_data_subset2.tail(10)
#DataFrame containing records with NaNs in any column
shelter_data_with_NaNs=shelter_data[shelter_data["location_address"].isna()]
shelter_data_with_NaNs.head(1)
#Create and describe a DataFrame containing records with NaNs in a subset of columns
shelter_data_subset2_with_NaNs=shelter_data_subset2[shelter_data_subset2["location_address"].isna()]
shelter_data_subset2_with_NaNs.head(10)
#Droping records with NaNs in certain columns

cleaned_shelter_data = shelter_data.dropna(subset=['capacity_actual_room', 'capacity_funding_room'])
cleaned_shelter_data
#spliting the data into groups based on one of the columns.
month_group=shelter_data.groupby("month")
month_group["service_user_count"].mean()
shelter_data.columns
#  Calculating group sums and standardizing using agg() 
shelter_data_summary = (shelter_data
                 .groupby(config['group_col'])
                 .agg(org_count=('organization_name', 'count'),
                      total_full_rooms=('occupied_rooms', 'sum'),
                      average_funding_bed=('capacity_funding_bed', 'mean')))
shelter_data_summary.head()
#Using plot()
plt.plot(cleaned_shelter_data["capacity_actual_room"],cleaned_shelter_data["capacity_funding_room"])
#Using scatter() 
plt.scatter(cleaned_shelter_data["occupied_rooms"], cleaned_shelter_data["capacity_actual_room"], edgecolor='k', label='ACTUAL ROOMS')
plt.scatter(cleaned_shelter_data["occupied_rooms"], cleaned_shelter_data["capacity_funding_room"], edgecolor='w', label='FUNDED ROOMS')
plt.legend()
#defining the variables
fig,ax = plt.subplots()
actual_room = ax.scatter(cleaned_shelter_data['sector_name'],
           cleaned_shelter_data['capacity_actual_room'])
funding_room = ax.scatter(cleaned_shelter_data['sector_name'],
           cleaned_shelter_data['capacity_funding_room'])
#plt.savefig('BS_HW-1.png')
#Creating title,label and grid
ax.set_title(config['plot_config']['title'])
ax.set_xlabel(config['plot_config']['xlabel'])
ax.set_ylabel(config['plot_config']['ylabel'])
ax.set_axisbelow(True)
ax.grid(alpha=0.5)
fig
#plt.savefig('BS_HW-1(pdf).pdf')
#Creating legend
ax.legend([actual_room, funding_room],['Actual room', 'Funding room'],bbox_to_anchor=(1, 1),
          loc='lower left')
plt.show()
fig
logging.info('Viewing Shelter dataset')

