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
                              ('------------------------------------>>', 'Japan', 'China', 'Philippines','Korea','S/SE Asia', 'ETOPS', 'MASTER LIST'))
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

st.markdown('**Last Update To Duty Lists:** 2022-06-02')

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
    dct['jpn'] = [x for x in df_master_list['JPN'] if str(x) != 'nan']
    dct['chn'] = [x for x in df_master_list['CHN'] if str(x) != 'nan']
    dct['phn'] = [x for x in df_master_list['PHN'] if str(x) != 'nan']
    dct['kor'] = [x for x in df_master_list['KOR'] if str(x) != 'nan']
    dct['asn'] = [x for x in df_master_list['ASN'] if str(x) != 'nan']
    dct['etp'] = [x for x in df_master_list['ETP'] if str(x) != 'nan']
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
        ##debug    cols = st.sidebar.columns([.5,.75,1,1])
            cols =  st.siderbar.columns([.5,.75,1,1])
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
    
    
    ## debugcols = st.sidebar.columns([.5,.75,1,1])
    cols = st.columns([.5,.75,1,1])
    cols[0].markdown(f'**{search_icao}**')
    if cols[1].button('Radar'):
        radar_button(search_icao, dct)
    if cols[2].button('Map'):
        map_button(search_icao, dct)
    if cols[3].button('Satellite'):
        satellite_button(search_icao, dct)
    
    
    
    

dct_duty = connect_gs()

# Build duty lists
lst_jpn = dct_duty.get('jpn')
lst_chn = dct_duty.get('chn')
lst_asn = dct_duty.get('asn')
lst_phn = dct_duty.get('phn')
lst_kor = dct_duty.get('kor')
lst_etp = dct_duty.get('etp')
lst_master = dct_duty.get('master')

# Build the dictionaries
dct_jpn = create_dct(lst_jpn)
dct_chn = create_dct(lst_chn)
dct_asn = create_dct(lst_asn)
dct_phn = create_dct(lst_phn)
dct_kor = create_dct(lst_kor)
dct_etp = create_dct(lst_etp)
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
        st.error('Otherwise, please contact Jeff at torger@wni.com or Mandy at zhan-m@wni.com to have ICAO added to master list.')

# Create sidebar scroll options
# create_scroll_item(region, 'JGP', dct_jgp, lst_jgp, search_icao)
create_scroll_item(region, 'Japan', dct_jpn, lst_jpn, search_icao)
create_scroll_item(region, 'China', dct_chn, lst_chn, search_icao)
create_scroll_item(region, 'Philippines', dct_phn, lst_phn, search_icao)
create_scroll_item(region, 'Korea', dct_kor, lst_kor, search_icao)
create_scroll_item(region, 'S/SE Asia', dct_asn, lst_asn, search_icao)
create_scroll_item(region, 'ETOPS', dct_etp, lst_etp, search_icao)
create_scroll_item(region, 'MASTER LIST', dct_master, lst_master, search_icao)


    