# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 17:06:22 2020

@author: NatalyR
"""
import folium
#from folium.plugins import MarkerCluster

from colour import Color

db = Color("red")
colors = list(db.range_to(Color("yellow"), 10))

def color_price(data):
    if(data < 19.81):
        return str(colors[9]).split()[0]
    elif(19.81 >= data < 32.02):
        return str(colors[8]).split()[0]
    elif(32.02 >= data < 44.23):
        return str(colors[7]).split()[0]
    elif(44.23 >= data < 56.44):
        return str(colors[6]).split()[0]
    elif(56.44 >= data < 68.66):
        return str(colors[4]).split()[0]
    elif(68.66 >= data < 80.87):
        return str(colors[3]).split()[0]
    elif(80.87 >= data < 93.08):
        return str(colors[2]).split()[0]
    elif(93.08 >= data < 105.29):
        return str(colors[1]).split()[0]
    elif(data >= 105.29):
        return str(colors[0]).split()[0]
    

def color_stores(data):
    if(data < 2):
        return str(colors[9]).split()[0]
    elif(data == 2):
        return str(colors[8]).split()[0]
    elif(data == 3):
        return str(colors[7]).split()[0]
    elif(data == 4):
        return str(colors[6]).split()[0]
    elif(data == 5):
        return str(colors[5]).split()[0]
    elif(data == 6):
        return str(colors[4]).split()[0]
    elif(data == 7):
        return str(colors[3]).split()[0]
    elif(data == 8):
        return str(colors[2]).split()[0]
    elif(data == 9):
        return str(colors[1]).split()[0]
    elif(data == 10):
        return str(colors[0]).split()[0]


def color_dist(data):
    if(data < 741.6):
        return str(colors[0]).split()[0]
    elif(741.6 >= data < 1459.97):
        return str(colors[2]).split()[0]
    elif(1459.97 >= data < 2178.26):
        return str(colors[3]).split()[0]
    elif(2178.26 >= data < 2896.56):
        return str(colors[4]).split()[0]
    elif(2896.56 >= data < 3614.85):
        return str(colors[5]).split()[0]
    elif(3614.85 >= data < 4333.14):
        return str(colors[6]).split()[0]
    elif(4333.14 >= data < 5051.43):
        return str(colors[7]).split()[0]
    elif(5051.43 >= data < 5769.73):
        return str(colors[8]).split()[0]
    elif(data >= 5769.73):
        return str(colors[9]).split()[0]   
    
    
def price_folium_map(df):
    lat = df['latitude']
    lon = df['longitude']
    price = df['price']

    price_map = folium.Map(location=[24.966,121.52], zoom_start=13,
                           width=600, height=500, tiles='Stamen Terrain')

    for lat, lon, price in zip(lat, lon, price):
        folium.CircleMarker(location=[lat, lon], radius=5, 
                            popup=str(price)+" per/unit", 
                            fill_color=color_price(price), 
                            color=None, fill_opacity = 0.8).add_to(price_map)
    price_map.save("html/price_map.html")
    
    
def stores_folium_map(df):
    lat = df['latitude']
    lon = df['longitude']
    num_stores = df['num_stores']

    stores_map = folium.Map(location=[24.966,121.52], zoom_start=13,
                            width=600, height=500, tiles='Stamen Terrain',)

    for lat, lon, num_stores in zip(lat, lon, num_stores):
        folium.CircleMarker(location=[lat, lon], radius=5,
                            popup=str(num_stores),
                            fill_color=color_stores(num_stores),
                            color=None, fill_opacity = 0.8).add_to(stores_map)
    stores_map.save("html/stores_map.html")
    
    
def dist_folium_map(df):
    lat = df['latitude']
    lon = df['longitude']
    dist_mrt = df['dist_mrt']

    dist_map = folium.Map(location=[24.966,121.52], zoom_start=13, 
                 width=600, height=500, tiles='Stamen Terrain',)

    for lat, lon, dist_mrt in zip(lat, lon, dist_mrt):
        folium.CircleMarker(location=[lat, lon], radius=5,
                            popup=str(dist_mrt)+" m",
                            fill_color=color_dist(dist_mrt),
                            color=None, fill_opacity = 0.8).add_to(dist_map)
    dist_map.save("html/dist_map.html")
    
    
def check_folium_map(df):
    lat = df['latitude']
    lon = df['longitude']
    price = df['price']

    check_map = folium.Map(location=[24.966,121.53], zoom_start=13, 
                 width=500, height=500, tiles='Stamen Terrain',)

    for lat, lon, price in zip(lat, lon, price):
        folium.CircleMarker(location=[lat, lon], radius=5, 
                        popup=str(price)+" per/unit", 
                        color='brown', fill_opacity = 0.8).add_to(check_map)
    check_map.save("html/check_map.html")    
    