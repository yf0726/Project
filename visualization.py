import numpy as np
import json
import folium
import branca.colormap as cm
import copy

def createcm(df,factor):
    """
    The function is used to create a linear colormap.
    
    Parameters:
        df: The dataframe containing information to plot.
        factor: The column of dataframe to plot.
    """
    color_range = ['#023858','#084081','#0868ac','#2b8cbe','#4eb3d3','#7bccc4','#a8ddb5','#ccebc5','#e0f3db','#f7fcf0','#fff7bc']
    colormap = cm.LinearColormap(
        color_range[::-1],
        vmin =  0, 
        vmax = round(max(df[factor])+1),
        index = np.linspace(round(min(df[factor])),round(max(df[factor])+1),11),
        caption = ''.join([factor,' of each country'])
    )
    return colormap

def color_map(country_name,colormap,countries,df,factor):
    """
    This function is used to return RGB value of corresponding data according to input colormap.
    
    Parameters:
        country_name: The country needed to be colored.
        colormap: Linear colormap.
        countries: Lists of countries with data.
        df: The dataframe containing information to plot.
        factor: The column of dataframe to plot.
        
    Returns:
        RGB value in hex. Setting the fillColor in style_function of the polygon.
    
    """
    
    if country_name not in countries:
        return '#999999'
    # For the country not in our cuisine list we return gray color.
    else:
        return colormap(df.loc[country_name][factor])
    # Fill the country with RGB proportionally to data value.
    
def global_visualization(topo_json_data,countries,df,factor,layer_name):
    """
    The function is used to create popup map.
    
    Parameters:
        topo_json_data: The geometric data.
        countries: Lists of countries with data.
        df: The dataframe containing information to plot.
        factor: The column of dataframe to plot.
        layer_name: Returned layer name
    Return:
        The layer to be added over map.
    """
    popup = folium.FeatureGroup(name=layer_name,overlay = True,show = True)
    colormap1 = createcm(df,factor)

    for data in topo_json_data['objects']['countries1']['geometries']:
        country_topo = copy.deepcopy(topo_json_data)
        country_topo['objects']['countries1']['geometries'] = [data]
        country_name = country_topo['objects']['countries1']['geometries'][0]['properties']['name']
        country_layer = folium.TopoJson(country_topo,object_path = 'objects.countries1',control=False,
                                        show = False,
                                              style_function = lambda feature:{
                                                'fillColor': color_map(feature['properties']['name'],\
                                                                       colormap1,countries,df,factor),
                                                'color' : 'black',
                                                'fillOpacity': 1,
                                                'weight' : 1,
                                                'dashArray' : '5, 5'
                                      })
        if country_name not in countries:
            country_layer.add_child(folium.Tooltip(country_name+': data not collected.'))
        else:
            country_layer.add_child(folium.Tooltip('The '+factor+' of '+country_name+' is :'+str(df.loc[country_name][factor])))
        country_layer.add_to(popup)
    return popup