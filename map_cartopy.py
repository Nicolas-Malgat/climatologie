import matplotlib.pyplot as plt
import cartopy
import cartopy.io.shapereader as shpreader
import cartopy.crs as ccrs
import pandas as pd
import cartopy.feature as cfeature


def plot_countries(df,projection,colors,title,edgecolor='grey',annotation=None):

    ax = plt.axes(projection=projection)
    ax.add_feature(cartopy.feature.OCEAN, facecolor='#add8e6')
    ax.outline_patch.set_edgecolor(edgecolor)

    values = sorted(list(df.unique()))

    shpfilename = shpreader.natural_earth(resolution='110m', category='cultural', name='admin_0_countries')
    reader = shpreader.Reader(shpfilename)
    countries = reader.records()

    for country in countries:
        attribute = 'NAME_EN'

        # get classification
        try:
            classification = df[country.attributes[attribute]] #ici
            
            print(country.attributes)
            break

            ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                            facecolor=(colors[values.index(classification)]),
                            label=country.attributes[attribute],
                            edgecolor='#000000',
                            linewidth=.25)
        except:
            # print(country.attributes[attribute])
            pass


    # legend
    import matplotlib.patches as mpatches
    handles = []
    values = ['< à ' + str(v) for v in values]

    for i in range(len(values)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i]))
        plt.legend(handles, values,
                   loc='lower left', bbox_to_anchor=(0.025, -0.0), 
                   fancybox=True, frameon=False, fontsize=5)

    plt.title(title, fontsize=8)

    title = 'maps/'+title+'.png'
    plt.savefig(title, bbox_inches='tight', pad_inches=.2, dpi=300)
    print('Saved: {}'.format(title))


def main():
    df = pd.read_csv('countries.csv', index_col='ISO_CODE')

    projection = ccrs.Robinson()
    title = 'Four Regions With The Same Population'
    colors = ['#f4b042', '#92D050','#71a2d6','#b282ac','#DDDDDD']
    plot_countries(df,projection,colors,title,edgecolor='white')

    print('Done.\n')