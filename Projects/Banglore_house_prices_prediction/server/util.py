import os, numpy as np
import json, pickle

__other_columns = None
__locations = None
__area_types = None
__society = None
__model = None

def get_estimated_price(location, society, area_type, total_sqft, bath, balcony, bhk):
    global __model
    
    x = np.zeros(len(__other_columns) + len(__locations) + len(__area_types) + len(__society))
    
    x[0] = total_sqft
    x[1] = bath
    x[2] = balcony
    x[3] = bhk
    x[4 + __locations.index(location.lower())] = 1
    x[4 + len(__locations) + __society.index(society.lower())] = 1
    x[4 + len(__locations) + len(__society) + __area_types.index(area_type.lower())] = 1
    
    return round(__model.predict([x])[0], 2)


def get_location_names():
    return __locations

def get_society_names():
    return __society

def get_area_type_names():
    return __area_types

def load_saved_artifacts():
    global __other_columns
    global __locations
    global __area_types
    global __society
    global __model

    script_dir = os.path.dirname(__file__) 
    artifacts_path = os.path.join(script_dir, 'artifacts')

    with open(os.path.join(artifacts_path, 'columns.json'), 'r') as f:
        data = json.load(f)
        __other_columns = data['other_columns']
        __locations = data['location_columns']
        __society = data['society_columns']
        __area_types = data['area_type_columns']

    with open(os.path.join(artifacts_path, 'banglore_home_price_prediction_model.pkl'), 'rb') as f:
        __model = pickle.load(f)

    print('done')

if __name__ == '__main__':
    load_saved_artifacts()
    print(get_location_names())