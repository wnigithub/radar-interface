import streamlit as st
import requests
import bs4 as bs
import webbrowser
import pandas as pd

# Build the app
st.set_page_config(layout='wide', page_title='Radar Regions', page_icon='https://p1.hiclipart.com/preview/994/283/642/rainmeter-tabbed-dock-grey-and-yellow-lightning-icon-png-clipart.jpg')

st.markdown("""
<style>
body {
    color: #000;
    background-color: #e8f4ff;
}
</style>
    """, unsafe_allow_html=True)

ph_readme = st.empty()
ph_title = st.empty()
ph_subtitle = st.empty()
ph_subtitle2 = st.empty()
ph_warning = st.empty()
ph_iframe = st.empty()
ph_iframe2 = st.empty()
ph_ui = st.sidebar.empty()
ph_sib = st.sidebar.empty()
#ph_cb = st.sidebar.empty()

search_icao = (ph_ui.text_input('Search ICAO')).upper()


    
#click_clear = ph_cb.button('Clear Input', key=1)
#if click_clear:
#    search_icao = ph_ui.text_input('Search ICAO', value='', key=1)
    
#st.sidebar.title('Select Region 地域選択')
region = st.sidebar.selectbox('Select Region',
                              ('------------------------------------>>', 'JGP', 'OK1', 'OK2', 'OK3', 'OK4', 'SG1', 'SG2', 'SG3', 'SG4', 'SGD', 'SJD', 'SJN', 'MASTER LIST'))
st.markdown(
    """
<style>
.css-1aumxhk {
background-color: #ededed;
background-image: none;
color: #000000
}
</style>
""",
    unsafe_allow_html=True,
)

# Default Page

st.markdown('**Last Update To Duty Lists:** 2021-06-03')

@st.cache
def create_dct(lst_icao):
    '''

    '''
    dct = {}
    for a in range(0, len(lst_icao)):
        url1 = f'http://www.gcmap.com/airport/{lst_icao[a]}'
        soup = bs.BeautifulSoup(requests.get(url1).text, 'html.parser')

        try:
            city = soup.find('span', {'class': 'locality'}).text
            #region = soup.find('span', {'class': 'region'}).text
            country = soup.find('span', {'class': 'country-name'}).text
            lat = soup.findAll('abbr', {'class': 'latitude'})[0]['title']
            lon = soup.findAll('abbr', {'class': 'longitude'})[0]['title']
            elev = soup.findAll('td', {'colspan': '2'})[9].text
            try:
                tz = soup.findAll('abbr', {'class': 'tz'})[0]['title']
            except IndexError:
                pass
        except AttributeError:
            pass
        except IndexError:
            pass
       

        try:
            dct[f'{lst_icao[a]}'] = {'City': city, 'Country': country, 'Lat': round(float(lat), 2), 'Lon': round(float(lon), 2), 'Elevation': elev, 'Timezone': f'UTC{tz}'}
        except UnboundLocalError:
            pass

    return dct


@st.cache
def connect_gs():
    '''
    '''
    # Import Master lst
    df_master_list = pd.read_csv(r'Duty_Regions_Master_List.csv')

    dct = {}
    dct['jgp'] = [x for x in df_master_list['JGP'] if str(x) != 'nan']
    dct['ok1'] = [x for x in df_master_list['OK1'] if str(x) != 'nan']
    dct['ok2'] = [x for x in df_master_list['OK2'] if str(x) != 'nan']
    dct['ok3'] = [x for x in df_master_list['OK3'] if str(x) != 'nan']
    dct['ok4'] = [x for x in df_master_list['OK4'] if str(x) != 'nan']
    dct['sg1'] = [x for x in df_master_list['SG1'] if str(x) != 'nan']
    dct['sg2'] = [x for x in df_master_list['SG2'] if str(x) != 'nan']
    dct['sg3'] = [x for x in df_master_list['SG3'] if str(x) != 'nan']
    dct['sg4'] = [x for x in df_master_list['SG4'] if str(x) != 'nan']
    dct['sgd'] = [x for x in df_master_list['SGD'] if str(x) != 'nan']
    dct['sja'] = [x for x in df_master_list['SJA'] if str(x) != 'nan']
    dct['sjd'] = [x for x in df_master_list['SJD'] if str(x) != 'nan']
    dct['sjn'] = [x for x in df_master_list['SJN'] if str(x) != 'nan']
    dct['master'] = [x for x in df_master_list['MASTER'] if str(x) != 'nan']

    return dct


def radar_button(icao_key, dct):
    '''
    '''
    lst_warning = ['RP', 'ZY', 'ZB', 'OP', 'VK', 'WA', 'WI', 'CY', 'VY', 'VE', 'VG', 'OE', 'UH', 'UE', 'VI',
                   'UI', 'UN', 'UO', 'UN', 'UA', 'UT', 'UY', 'UT', 'US', 'UW', 'UR', 'UU', 'UL', 'HK', 'HE', 'PW',                   
                   'ZM', 'ZW', 'ZL', 'ZP', 'ZH', 'VC', 'VR', 'VO', 'VA', 'VE', 'VD', 'VV', 'VT', 'VL', 'ZU', 'PG', ]
    ph_title.title(f'{icao_key} - {(dct.get(icao_key)).get("City")}, {(dct.get(icao_key)).get("Country")}')
    ph_subtitle.markdown(f'''**Coordinates(Lat,Lon):** {(dct.get(icao_key)).get("Lat")}, {(dct.get(icao_key)).get("Lon")} **Timezone:** {(dct.get(icao_key)).get("Timezone")}''')
    if icao_key[:2] in lst_warning:
        ph_warning.error('Radar data in this region could be unreliable or non-existent. Please cross-reference with satellite data for best analysis.')
    ph_iframe.markdown(f'<iframe src="https://www.rainviewer.com/map.html?loc={(dct.get(icao_key)).get("Lat")},{(dct.get(icao_key)).get("Lon")},8&oFa=1&oC=1&oU=1&oCS=1&oF=1&oAP=0&rmt=1&c=5&o=49&lm=0&th=0&sm=0&sn=1" width="100%" frameborder="0" style="border:0;height:80vh;" allowfullscreen></iframe>', unsafe_allow_html=True)
    

def map_button(icao_key, dct):
    '''
    '''
    ph_title.title(f'{icao_key} - {(dct.get(icao_key)).get("City")}, {(dct.get(icao_key)).get("Country")}')
    ph_subtitle.markdown(f'**Coordinates:** {(dct.get(icao_key)).get("Lat")}, {(dct.get(icao_key)).get("Lon")}  **Timezone:** {(dct.get(icao_key)).get("Timezone")}')
    ph_iframe.markdown(f'<iframe src="https://map.blitzortung.org/index.php?interactive=1&NavigationControl=0&FullScreenControl=0&LightningCheckboxChecked=0&CourseCheckboxChecked=0&CirclesCheckboxChecked=0&Cookies=0&InfoDiv=0&MenuButtonDiv=0&ScaleControl=0&LinksCheckboxChecked=0&LinksRangeValue=0&MapStyle=3&MapStyleRangeValue=8&Advertisment=0#9.8/{(dct.get(icao_key)).get("Lat")}/{(dct.get(icao_key)).get("Lon")}" width="100%" frameborder="0" style="border:0;height:80vh;" allowfullscreen></iframe>', unsafe_allow_html=True)


def satellite_button(icao_key, dct):
    '''
    '''
    ph_title.title(f'{icao_key} - {(dct.get(icao_key)).get("City")}, {(dct.get(icao_key)).get("Country")}')
    ph_subtitle.markdown(f'**Coordinates:** {(dct.get(icao_key)).get("Lat")}, {(dct.get(icao_key)).get("Lon")}  **Timezone:** {(dct.get(icao_key)).get("Timezone")}')
    # ph_iframe.markdown(f'<iframe src="https://www.tsohost.com/assets/uploads/blog/under-construction-pages-1-image-library.jpg" width="100%" frameborder="0" style="border:0;height:80vh;" allowfullscreen></iframe>', unsafe_allow_html=True)
    # url = 'https://rammb-slider.cira.colostate.edu/?sat=himawari&sec=full_disk&x=10576&y=7952&z=1&angle=0&im=6&ts=3&st=0&et=0&speed=130&motion=loop&maps%5Bborders%5D=white&maps%5Bairports%5D=pink&lat=0&p%5B0%5D=geocolor&p%5B1%5D=band_13&opacity%5B0%5D=1&opacity%5B1%5D=0.15&pause=0&slider=-1&hide_controls=0&mouse_draw=0&follow_feature=0&follow_hide=0&s=rammb-slider&draw_color=FFD700&draw_width=6'
    # webbrowser.open_new_tab(url
    
def get_sat_url(icao):
    lst_japan_region = ['RO', 'RJ']
    lst_korea_region = ['RK']
    lst_nechina_region = ['ZY', 'ZB']
    lst_sechina_region = ['ZS', 'ZH', 'ZL', 'ZU', 'ZG', 'ZP', 'VH', 'VM', 'ZJ']
    lst_wchina_region = ['ZW', 'ZM']
    lst_indochina_region = ['VY', 'VT', 'VD', 'VV', 'VL']
    lst_phil_region = ['RP']
    lst_indonesia_region = ['WM', 'WS', 'WI', 'WB', 'WA', 'WR']
    lst_oceania_region = ['YS', 'YM', 'NZ']
    lst_westpac_region = ['PG', 'PW']
    lst_sasia_region = ['VE', 'VI', 'VA', 'VC', 'VR', 'VO', 'NK', 'OP', 'OK', 'OI']
    lst_russia_region = ['UA', 'UN', 'US', 'UW', 'UR', 'UT', 'UD', 'UB', 'UU']
    lst_europe_region = ['L', 'E', 'UM' ]
    lst_africa_region = ['H']
    lst_usa_region = ['K']
    lst_canada_region = ['C']
    lst_alaska_region = ['PA']
    
    if icao[:2] in lst_japan_region:
        return 'https://rammb-slider.cira.colostate.edu/?sat=himawari&sec=full_disk&x=10044&y=3802&z=4&angle=0&im=6&ts=3&st=0&et=0&speed=130&motion=loop&maps%5Bborders%5D=white&maps%5Bairports%5D=pink&lat=0&p%5B0%5D=geocolor&p%5B1%5D=band_13&opacity%5B0%5D=1&opacity%5B1%5D=0.45&pause=0&slider=-1&hide_controls=0&mouse_draw=0&follow_feature=0&follow_hide=0&s=rammb-slider&draw_color=FFD700&draw_width=6'
    if icao[:2] in lst_korea_region:
        return 'https://rammb-slider.cira.colostate.edu/?sat=himawari&sec=full_disk&x=8543&y=3869&z=5&angle=0&im=6&ts=3&st=0&et=0&speed=130&motion=loop&maps%5Bborders%5D=white&maps%5Bairports%5D=pink&lat=0&p%5B0%5D=geocolor&p%5B1%5D=band_13&opacity%5B0%5D=1&opacity%5B1%5D=0.45&pause=0&slider=-1&hide_controls=0&mouse_draw=0&follow_feature=0&follow_hide=0&s=rammb-slider&draw_color=FFD700&draw_width=6'
    if icao[:2] in lst_nechina_region:
        return 'https://rammb-slider.cira.colostate.edu/?sat=himawari&sec=full_disk&x=8438&y=2520&z=4&angle=0&im=6&ts=3&st=0&et=0&speed=130&motion=loop&maps%5Bborders%5D=white&maps%5Bairports%5D=pink&lat=0&p%5B0%5D=geocolor&p%5B1%5D=band_13&opacity%5B0%5D=1&opacity%5B1%5D=0.45&pause=0&slider=-1&hide_controls=0&mouse_draw=0&follow_feature=0&follow_hide=0&s=rammb-slider&draw_color=FFD700&draw_width=6'
    if icao[:2] in lst_sechina_region:
        return 'https://rammb-slider.cira.colostate.edu/?sat=himawari&sec=full_disk&x=5092&y=5080&z=3&angle=0&im=6&ts=3&st=0&et=0&speed=130&motion=loop&maps%5Bborders%5D=white&maps%5Bairports%5D=pink&lat=0&p%5B0%5D=geocolor&p%5B1%5D=band_13&opacity%5B0%5D=1&opacity%5B1%5D=0.45&pause=0&slider=-1&hide_controls=0&mouse_draw=0&follow_feature=0&follow_hide=0&s=rammb-slider&draw_color=FFD700&draw_width=6'
    if icao[:2] in lst_wchina_region:
        return 'https://rammb-slider.cira.colostate.edu/?sat=himawari&sec=full_disk&x=2968&y=4548&z=3&angle=0&im=6&ts=3&st=0&et=0&speed=130&motion=loop&maps%5Bborders%5D=white&maps%5Bairports%5D=pink&lat=0&p%5B0%5D=geocolor&p%5B1%5D=band_13&opacity%5B0%5D=1&opacity%5B1%5D=0.45&pause=0&slider=-1&hide_controls=0&mouse_draw=0&follow_feature=0&follow_hide=0&s=rammb-slider&draw_color=FFD700&draw_width=6'
    if icao[:2] in lst_indochina_region:
        return 'https://rammb-slider.cira.colostate.edu/?sat=himawari&sec=full_disk&x=3692&y=7892&z=3&angle=0&im=6&ts=3&st=0&et=0&speed=130&motion=loop&maps%5Bborders%5D=white&maps%5Bairports%5D=pink&lat=0&p%5B0%5D=geocolor&p%5B1%5D=band_13&opacity%5B0%5D=1&opacity%5B1%5D=0.45&pause=0&slider=-1&hide_controls=0&mouse_draw=0&follow_feature=0&follow_hide=0&s=rammb-slider&draw_color=FFD700&draw_width=6'
    if icao[:2] in lst_phil_region:
        return 'https://rammb-slider.cira.colostate.edu/?sat=himawari&sec=full_disk&x=6584&y=8452&z=3&angle=0&im=6&ts=3&st=0&et=0&speed=130&motion=loop&maps%5Bborders%5D=white&maps%5Bairports%5D=pink&lat=0&p%5B0%5D=geocolor&p%5B1%5D=band_13&opacity%5B0%5D=1&opacity%5B1%5D=0.45&pause=0&slider=-1&hide_controls=0&mouse_draw=0&follow_feature=0&follow_hide=0&s=rammb-slider&draw_color=FFD700&draw_width=6'
    if icao[:2] in lst_indonesia_region:
        return 'https://rammb-slider.cira.colostate.edu/?sat=himawari&sec=full_disk&x=3908&y=11420&z=3&angle=0&im=6&ts=3&st=0&et=0&speed=130&motion=loop&maps%5Bborders%5D=white&maps%5Bairports%5D=pink&lat=0&p%5B0%5D=geocolor&p%5B1%5D=band_13&opacity%5B0%5D=1&opacity%5B1%5D=0.45&pause=0&slider=-1&hide_controls=0&mouse_draw=0&follow_feature=0&follow_hide=0&s=rammb-slider&draw_color=FFD700&draw_width=6'       
    if icao[:2] in lst_oceania_region:
        return 'https://rammb-slider.cira.colostate.edu/?sat=himawari&sec=full_disk&x=13360&y=18312&z=3&angle=0&im=6&ts=3&st=0&et=0&speed=130&motion=loop&maps%5Bborders%5D=white&maps%5Bairports%5D=pink&lat=0&p%5B0%5D=geocolor&p%5B1%5D=band_13&opacity%5B0%5D=1&opacity%5B1%5D=0.45&pause=0&slider=-1&hide_controls=0&mouse_draw=0&follow_feature=0&follow_hide=0&s=rammb-slider&draw_color=FFD700&draw_width=6'
    if icao[:2] in lst_westpac_region:
        return 'https://rammb-slider.cira.colostate.edu/?sat=himawari&sec=full_disk&x=13432&y=7512&z=3&angle=0&im=6&ts=3&st=0&et=0&speed=130&motion=loop&maps%5Bborders%5D=white&maps%5Bairports%5D=pink&lat=0&p%5B0%5D=geocolor&p%5B1%5D=band_13&opacity%5B0%5D=1&opacity%5B1%5D=0.45&pause=0&slider=-1&hide_controls=0&mouse_draw=0&follow_feature=0&follow_hide=0&s=rammb-slider&draw_color=FFD700&draw_width=6'    
    if icao[:2] in lst_sasia_region:
        return 'https://rammb-slider.cira.colostate.edu/?sat=meteosat-8&sec=full_disk&x=2826&y=1168&z=3&angle=0&im=6&ts=3&st=0&et=0&speed=130&motion=loop&maps%5Bborders%5D=white&maps%5Bairports%5D=pink&lat=0&p%5B0%5D=geocolor&p%5B1%5D=band_13&opacity%5B0%5D=1&pause=0&slider=-1&hide_controls=0&mouse_draw=0&follow_feature=0&follow_hide=0&s=rammb-slider&draw_color=FFD700&draw_width=6'
    #if icao[:2] or icao[:1] in lst_europe_region:
    #    return 'https://rammb-slider.cira.colostate.edu/?sat=meteosat-11&sec=full_disk&x=2103&y=353&z=3&angle=0&im=6&ts=3&st=0&et=0&speed=130&motion=loop&maps%5Bborders%5D=white&maps%5Bairports%5D=pink&lat=0&p%5B0%5D=geocolor&p%5B1%5D=band_13&opacity%5B0%5D=1&pause=0&slider=-1&hide_controls=0&mouse_draw=0&follow_feature=0&follow_hide=0&s=rammb-slider&draw_color=FFD700&draw_width=6'
    #if icao[:2] or icao[:1] in lst_africa_region:
    #    return 'https://rammb-slider.cira.colostate.edu/?sat=meteosat-8&sec=full_disk&x=742&y=1480&z=2&angle=0&im=6&ts=3&st=0&et=0&speed=130&motion=loop&maps%5Bborders%5D=white&maps%5Bairports%5D=pink&lat=0&p%5B0%5D=geocolor&p%5B1%5D=band_13&opacity%5B0%5D=1&pause=0&slider=-1&hide_controls=0&mouse_draw=0&follow_feature=0&follow_hide=0&s=rammb-slider&draw_color=FFD700&draw_width=6'
   # if icao[:2] or icao[:1] in lst_usa_region:
    #    return 'https://rammb-slider.cira.colostate.edu/?sat=goes-16&sec=full_disk&x=6240&y=3856&z=2&angle=0&im=6&ts=3&st=0&et=0&speed=130&motion=loop&maps%5Bborders%5D=white&maps%5Bairports%5D=pink&lat=0&p%5B0%5D=geocolor&p%5B1%5D=band_13&opacity%5B0%5D=1&pause=0&slider=-1&hide_controls=0&mouse_draw=0&follow_feature=0&follow_hide=0&s=rammb-slider&draw_color=FFD700&draw_width=6'
    #if icao[:2] or icao[:1] in lst_canada_region:
    #    return 'https://rammb-slider.cira.colostate.edu/?sat=goes-16&sec=full_disk&x=7688&y=1400&z=3&angle=0&im=6&ts=3&st=0&et=0&speed=130&motion=loop&maps%5Bborders%5D=white&maps%5Bairports%5D=pink&lat=0&p%5B0%5D=geocolor&p%5B1%5D=band_13&opacity%5B0%5D=1&pause=0&slider=-1&hide_controls=0&mouse_draw=0&follow_feature=0&follow_hide=0&s=rammb-slider&draw_color=FFD700&draw_width=6'
    #if icao[:2] in lst_alaska_region:
    #    return 'https://rammb-slider.cira.colostate.edu/?sat=goes-17&sec=full_disk&x=9224&y=416&z=4&angle=0&im=6&ts=3&st=0&et=0&speed=130&motion=loop&maps%5Bborders%5D=white&maps%5Bairports%5D=pink&lat=0&p%5B0%5D=geocolor&p%5B1%5D=band_13&opacity%5B0%5D=1&pause=0&slider=-1&hide_controls=0&mouse_draw=0&follow_feature=0&follow_hide=0&s=rammb-slider&draw_color=FFD700&draw_width=6'
    else:
        return 'https://rammb-slider.cira.colostate.edu/?sat=himawari&sec=full_disk&x=11008&y=11008&z=0&angle=0&im=6&ts=3&st=0&et=0&speed=130&motion=loop&maps%5Bborders%5D=white&maps%5Bairports%5D=pink&lat=0&p%5B0%5D=geocolor&p%5B1%5D=band_13&opacity%5B0%5D=1&pause=0&slider=-1&hide_controls=0&mouse_draw=0&follow_feature=0&follow_hide=0&s=rammb-slider&draw_color=FFD700&draw_width=6'
   


def region_lightning(coords, zoom):
    '''
    '''
    ph_iframe2.markdown(f'<iframe src="https://map.blitzortung.org/index.php?interactive=1&NavigationControl=0&FullScreenControl=0&LightningCheckboxChecked=0&CourseCheckboxChecked=0&CirclesCheckboxChecked=0&Cookies=0&InfoDiv=0&MenuButtonDiv=0&ScaleControl=0&LinksCheckboxChecked=0&LinksRangeValue=0&MapStyle=3&MapStyleRangeValue=11&Advertisment=0#11/22.2924/114.1877" width="100%" frameborder="0" style="border:0;height:80vh;" allowfullscreen></iframe>', unsafe_allow_html=True)


def region_radar(coords, zoom):
    '''
    '''
    ph_iframe.markdown(f'<iframe src="https://www.rainviewer.com/map.html?loc={coords},{zoom}&oFa=1&oC=1&oU=1&oCS=1&oF=1&oAP=0&rmt=1&c=5&o=49&lm=0&th=0&sm=0&sn=1" width="100%" frameborder="3" style="border:2;height:80vh;" allowfullscreen></iframe>', unsafe_allow_html=True)

def clear_user_input():
    
    search_icao = ph_ui.text_input('Search ICAO', value='')
    
def create_scroll_item(region, duty, dct, lst, search_icao):
    '''
    '''
    if region == duty:
        i = 0
        while i <= len(dct)-1:
            cols = st.sidebar.beta_columns([.5,.75,1,1])
            cols[0].markdown(f'**{list(dct.keys())[i]}**')
            if cols[1].button('Radar', key=i+10000):
                radar_button(lst[i], dct)
                search_icao = ph_ui.text_input('Search ICAO', value='', key=i+10000)
            if cols[2].button('Map', key=i+10001):
                map_button(lst[i], dct)
            #if cols[2].button('Satellite', key=i+10002):
            #    satellite_button(lst[i], dct)
            url = get_sat_url(list(dct.keys())[i])
            cols[3].markdown(f'[Satellite]({url})', unsafe_allow_html=True)
            i = i+1
            
def create_search_item(search_icao, dct):
    
    
    cols = st.sidebar.beta_columns([.5,.75,1,1])
    cols[0].markdown(f'**{search_icao}**')
    if cols[1].button('Radar'):
        radar_button(search_icao, dct)
    if cols[2].button('Map'):
        map_button(search_icao, dct)
    if cols[3].button('Satellite'):
        satellite_button(search_icao, dct)
    
    
    
    

dct_duty = connect_gs()

# Build duty lists
lst_jgp = dct_duty.get('jgp')
lst_ok1 = dct_duty.get('ok1')
lst_ok2 = dct_duty.get('ok2')
lst_ok3 = dct_duty.get('ok3')
lst_ok4 = dct_duty.get('ok4')
lst_sg1 = dct_duty.get('sg1')
lst_sg2 = dct_duty.get('sg2')
lst_sg3 = dct_duty.get('sg3')
lst_sg4 = dct_duty.get('sg4')
lst_sgd = dct_duty.get('sgd')
lst_sja = dct_duty.get('sja')
lst_sjd = dct_duty.get('sjd')
lst_sjn = dct_duty.get('sjn')
lst_master = dct_duty.get('master')

# Build the dictionaries
dct_jgp = create_dct(lst_jgp)
dct_ok1 = create_dct(lst_ok1)
dct_ok2 = create_dct(lst_ok2)
dct_ok3 = create_dct(lst_ok3)
dct_ok4 = create_dct(lst_ok4)
dct_sg1 = create_dct(lst_sg1)
dct_sg2 = create_dct(lst_sg2)
dct_sg3 = create_dct(lst_sg3)
dct_sg4 = create_dct(lst_sg4)
dct_sgd = create_dct(lst_sgd)
# dct_sja = create_dct(lst_sja)
dct_sjd = create_dct(lst_sjd)
dct_sjn = create_dct(lst_sjn)
dct_master = create_dct(lst_master)

if search_icao:
    if search_icao in lst_master:
        radar_button(search_icao, dct_master)
        cols = ph_sib.beta_columns([.88,.80,1,1])
        #if cols[0].button('Clear', key=1):
        #    search_icao = ph_ui.text_input('Search ICAO', value='', key=1)
        if cols[0].button('Radar', key=2):
            radar_button(search_icao, dct_master)
        if cols[1].button('Map', key=4):
            map_button(search_icao, dct_master)
        url = get_sat_url(search_icao)
        cols[2].markdown(f'[Satellite]({url})', unsafe_allow_html=True)
        
    else:
        st.error('ICAO NOT FOUND: Please check input text for errors.')
        st.error('Otherwise, please contact Jeff at torger@wni.com or Ben at mielke@wni.com to have ICAO added to master list.')

# Create sidebar scroll options
create_scroll_item(region, 'JGP', dct_jgp, lst_jgp, search_icao)
create_scroll_item(region, 'OK1', dct_ok1, lst_ok1, search_icao)
create_scroll_item(region, 'OK2', dct_ok2, lst_ok2, search_icao)
create_scroll_item(region, 'OK3', dct_ok3, lst_ok3, search_icao)
create_scroll_item(region, 'OK4', dct_ok4, lst_ok4, search_icao)
create_scroll_item(region, 'SG1', dct_sg1, lst_sg1, search_icao)
create_scroll_item(region, 'SG2', dct_sg2, lst_sg2, search_icao)
create_scroll_item(region, 'SG3', dct_sg3, lst_sg3, search_icao)
create_scroll_item(region, 'SG4', dct_sg4, lst_sg4, search_icao)
create_scroll_item(region, 'SGD', dct_sgd, lst_sgd, search_icao)
create_scroll_item(region, 'SJD', dct_sjd, lst_sjd, search_icao)
create_scroll_item(region, 'SJN', dct_sjn, lst_sjn, search_icao)
create_scroll_item(region, 'MASTER LIST', dct_master, lst_master, search_icao)


    