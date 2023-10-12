from google_images_search import GoogleImagesSearch
import os

def retrieve_from_google(query, limit):
    #current_directory = os.getcwd()
    folder_path = os.path.join(os.getcwd(), "Images")

    gis = GoogleImagesSearch('AIzaSyBm-zMIEyDd-9cyf3kzRbLCPdRit4hhjqs', 'd445dfdd970e94217')
    _search_params = {
    'q': query,
    'num': limit,
    'fileType': 'jpg|gif|png',
    #'rights': 'cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived',
    #'safe': 'active|high|medium|off|safeUndefined', ##
    #'imgType': 'clipart|face|lineart|stock|photo|animated|imgTypeUndefined', ##
    #'imgSize': 'huge|icon|large|medium|small|xlarge|xxlarge|imgSizeUndefined', ##
    #'imgDominantColor': 'black|blue|brown|gray|green|orange|pink|purple|red|teal|white|yellow|imgDominantColorUndefined', ##
    # 'imgColorType': "['imgColorTypeUndefined', 'mono', 'gray', 'color', 'trans']" ##
}
    # gis.search(search_params=_search_params)
    gis.search(search_params=_search_params, path_to_dir=folder_path)