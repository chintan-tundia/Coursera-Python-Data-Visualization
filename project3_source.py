"""
Project for Week 4 of "Python Data Visualization".
Unify data via common country codes.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import math
import pygal


def build_country_code_converter(codeinfo):
    """
    Inputs:
      codeinfo      - A country code information dictionary

    Output:
      A dictionary whose keys are plot country codes and values
      are world bank country codes, where the code fields in the
      code file are specified in codeinfo.
    """
    plot_country_code = codeinfo['plot_codes']
    data_country_code = codeinfo['data_codes']
    out_dict = {}
    with open(codeinfo['codefile'], 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=codeinfo['separator'], \
                                quotechar=codeinfo['quote'])
        for row in reader:
            out_dict[row[plot_country_code]] = row[data_country_code]
    return out_dict


def reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries):
    """
    Inputs:
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country codes used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country codes from
      gdp_countries.  The set contains the country codes from
      plot_countries that did not have a country with a corresponding
      code in gdp_countries.

      Note that all codes should be compared in a case-insensitive
      way.  However, the returned dictionary and set should include
      the codes with the exact same case as they have in
      plot_countries and gdp_countries.
    """
    mapping = build_country_code_converter(codeinfo)    
    gdp_countries_keys = gdp_countries.keys()
    out_dict = {}
    out_set = set()
    for key in plot_countries.keys():
        up_key = key.upper()
        gdp_code = mapping[up_key]
        if(gdp_code in gdp_countries_keys):
            out_dict[key] = gdp_code
        else:
            out_set.add(key)
    return out_dict, out_set

def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - Name of CSV file
      keyfield  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields

    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    
    out_dict = {}
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in reader:
            try:
                var_key = row[keyfield]
                out_dict[var_key] = row
            except KeyError:
                pass
    return out_dict

def build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year for which to create GDP mapping

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
    gdp_data = read_csv_as_nested_dict(gdpinfo["gdpfile"], \
                                      gdpinfo["country_code"], \
                                      gdpinfo["separator"],\
                                      gdpinfo["quote"])
    mapping = build_country_code_converter(codeinfo)
    tuple_set1 = set(plot_countries.keys())
    tuple_dict = {}
    tuple_set2 = set()
    filter_codes = set()
    for code in plot_countries.keys():
        if(code.upper() in mapping):
            tuple_set1.remove(code)
            filter_codes.add(code)
        elif(code.lower() in mapping):
            tuple_set1.remove(code)
            filter_codes.add(code)    
    for filter_code in filter_codes:
        for key, val in mapping.items():
            if(key.lower() == filter_code.lower()):
                if(val.lower() in gdp_data):
                    gdp_val = gdp_data[val][year]
                    if(gdp_val != ''):
                        tuple_dict[filter_code] = math.log10(float(gdp_val))
                    else:
                        tuple_set2.add(filter_code)
                elif(val.upper() in gdp_data):
                    gdp_val = gdp_data[val][year]
                    if(gdp_val != ''):
                        tuple_dict[filter_code] = math.log10(float(gdp_val))
                    else:
                        tuple_set2.add(filter_code)

                   
    return tuple_dict, tuple_set1, tuple_set2


def render_world_map(gdpinfo, codeinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year of data
      map_file       - String that is the output map file name

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data in gdp_mapping and outputs
      it to a file named by svg_filename.
    """
    return


def test_render_world_map():
    """
    Test the project code for several years
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    codeinfo = {
        "codefile": "isp_country_codes.csv",
        "separator": ",",
        "quote": '"',
        "plot_codes": "ISO3166-1-Alpha-2",
        "data_codes": "ISO3166-1-Alpha-3"
    }

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1960", "isp_gdp_world_code_1960.svg")

    # 1980
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1980", "isp_gdp_world_code_1980.svg")

    # 2000
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2000", "isp_gdp_world_code_2000.svg")

    # 2010
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2010", "isp_gdp_world_code_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

# test_render_world_map()