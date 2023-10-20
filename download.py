#!/usr/bin/env python
# coding: utf-8

# # Install ArcGis for python
# Dokumentasi bisa dilihat melalui tautan https://developers.arcgis.com/python/ dan https://developers.arcgis.com/python/api-reference/  
# Module arcgis dapat diinstall menggunakan command `conda install -c esri ArcGIS`

# In[54]:


from arcgis.features import FeatureLayerCollection
import os


# ## Inisasi variable
# 1. Variabel `skala_peta` hanya tersedia opsi `25K, 50K, 250K`  
# 2. Variabel`url` digunakan untuk mendapatkan me-load MapServer milik BIG. Untuk detail penjelasan terkait FeaturesCollection bisa dilihat melalui tautan 
# https://developers.arcgis.com/python/guide/working-with-feature-layers-and-features/  
# 3. Variabel `url_download` digunakan untuk mendownload peta yang tersedia di server BIG

# In[68]:


skala_peta = '25K'
url = 'https://geoservices.big.go.id/gis/rest/services/PPIG/IDX_Download/MapServer/'
url_download = 'https://tanahair.indonesia.go.id/portal-web/downloadpetacetak/Zip?skala={}&namaFile='.format(skala_peta)
output_directory = 'output'
download_using_python = False


# ## Get features collection from MapServer
# Meload map service dari server BIG

# In[3]:


feature_layer_collection = FeatureLayerCollection(url)


# In[4]:


feature_layer_collection


# ---
# Melihat ketersediaan FeatureLayers pada FeaturesCollection

# In[5]:


feature_layers = feature_layer_collection.layers


# In[6]:


feature_layers


# In[10]:


for layer in feature_layers:
    print(layer.properties.name)


# ---
# Fungsi ini digunakan memilih FeatureLayer berdasarkan skala peta yang dipilih

# In[7]:


def select_feature_layers(feature_layers, skala_peta):
    if skala_peta == '25K':
        return feature_layers[1]
    if skala_peta == '50K':
        return feature_layers[2]
    if skala_peta == '250K':
        return feature_layers[3]


# In[39]:


feature_layer = select_feature_layers(feature_layers, '25K')


# In[40]:


feature_layer


# ---
# Mendapatkan daftar field attributes dari FeatureLayer

# In[41]:


fields = feature_layer.properties.fields


# In[42]:


for f in fields:
    print(f['name'])


# ---
# ## Mendapatkan seluruh data attributes dari FeatureLayer
# Dokumentasi terkait `query()` method dapat dilihat pada tautan berikut https://developers.arcgis.com/python/api-reference/arcgis.features.toc.html

# In[43]:


query = feature_layer.query(return_geometry=False)


# Merubah ke dalam format pandas dataframe

# In[44]:


df = query.sdf


# In[45]:


df


# ## Menambahkan kolom download_link pada dataframe

# In[47]:


def add_download_link(nomor_peta):
    return '{}{}{}'.format(url_download, nomor_peta, '.zip')


# In[48]:


df['download_link'] = df['NOMOR_PETA'].apply(add_download_link)


# In[52]:


df


# ### Export download link
# Dapat digunakan untuk mendownload menggunakan download manager

# In[69]:


batch_download_for_download_manager = '{}_batch_download.txt'.format(skala_peta)


# In[70]:


df['download_link'].to_csv(batch_download_for_download_manager, header=False, index=False)


# ## Download Menggunakan python
# 
# BELUM BERES

# In[62]:


output = os.path.join(os.getcwd(), output_directory)
os.makedirs(output, exist_ok=True)


# In[61]:





# In[ ]:




