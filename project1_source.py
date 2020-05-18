"""
Project for Week 2 of "Python Data Visualization".
Read World Bank GDP data and create some basic XY plots.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import pygal

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

def build_plot_values(gdp_info, gdpdata):
    """
    Inputs:
      gdp_info - GDP data information dictionary
      gdpdata - A single country's GDP stored in a dictionary whose
                keys are strings indicating a year and whose values
                are strings indicating the country's corresponding GDP
                for that year.

    Output: 
      Returns a list of tuples of the form (year, GDP) for the years
      between "min_year" and "max_year", inclusive, from gdp_info that
      exist in gdpdata.  The year will be an integer and the GDP will
      be a float.
    """
    start_year = gdp_info['min_year']
    end_year = gdp_info['max_year']
    tuple_list = []
    new_gdpdata = {}
    for key, val in gdpdata.items():
        try:
            if(key != '' and val != ''):
                new_gdpdata[int(key)] = float(val)
        except KeyError:
            pass
        except ValueError:
            pass
    
    for year in range(start_year, end_year+1):
        if(year in new_gdpdata):
            val = new_gdpdata[year]    
            tuple_list.append((int(year), float(val)))

    
    return tuple_list

def build_plot_dict(gdp_info, country_list):
    """
    Inputs:
      gdp_info      - GDP data information dictionary
      country_list - List of strings that are country names

    Output:
      Returns a dictionary whose keys are the country names in
      country_list and whose values are lists of XY plot values 
      computed from the CSV file described by gdp_info.

      Countries from country_list that do not appear in the
      CSV file should still be in the output dictionary, but
      with an empty XY plot value list.
    """
    tuple_dict = {}
    gdpdata = read_csv_as_nested_dict(gdp_info["gdpfile"], \
                                      gdp_info["country_name"], \
                                      gdp_info["separator"],\
                                      gdp_info["quote"])
    for value in gdpdata.values():
        value.pop(gdp_info["country_name"])
        value.pop(gdp_info["country_code"])
        
    for country in country_list:
        tuple_dict[country] = []
        for key, value in gdpdata.items():
            if key == country:
                tuple_dict[country] = build_plot_values(gdp_info, gdpdata[country])    
    return tuple_dict

def render_xy_plot(gdp_info, country_list, plot_file):
    """
    Inputs:
      gdp_info      - GDP data information dictionary
      country_list - List of strings that are country names
      plot_file    - String that is the output plot file name

    Output:
      Returns None.

    Action:
      Creates an SVG image of an XY plot for the GDP data
      specified by gdp_info for the countries in country_list.
      The image will be stored in a file named by plot_file.
    """
    return


def test_render_xy_plot():
    """
    Code to exercise render_xy_plot and generate plots from
    actual GDP data.
    """
    gdp_info = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    render_xy_plot(gdp_info, [], "isp_gdp_xy_none.svg")
    render_xy_plot(gdp_info, ["China"], "isp_gdp_xy_china.svg")
    render_xy_plot(gdp_info, ["United Kingdom", "United States"],
                   "isp_gdp_xy_uk+usa.svg")

