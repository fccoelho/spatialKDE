import numpy as np
from scipy import stats as st
import matplotlib.pyplot as plt
from osgeo import gdal, osr
    
    
class Kernel2d(object):
    def __init__(self, lon, lat, bw=None):
        self.x = lon
        self.y = lat
        self.bw = bw
        self.values = np.vstack([self.x, self.y])
        self.X, self.Y = np.mgrid[self.x.min():self.x.max():400j,
                                  self.y.min():self.y.max():400j]
        self.positions = np.vstack([self.X.ravel(), self.Y.ravel()])

        
    def run(self):
        self.kernel = st.gaussian_kde(self.values, self.bw)
        print "==> Factor: ", self.kernel.factor
        self.Z = np.reshape(self.kernel(self.positions).T, self.X.shape)
        return self.X, self.Y, self.Z
        
    def to_geotiff(self,fname, epsg):
        '''
        saves the kernel as a GEOTIFF image
        '''
        driver = gdal.GetDriverByName("GTiff")
        out = driver.Create(fname, len(self.X), len(self.Y), 1, gdal.GDT_Float32)
        #pixel sizes
        xps = (self.x.max() - self.x.min()) / float(len(self.X))
        yps = (self.y.max() - self.y.min()) / float(len(self.Y))
        out.SetGeoTransform((self.x.min(), xps, 0, self.y.min(), 0, yps))
        coord_system = osr.SpatialReference()
        coord_system.ImportFromEPSG(epsg)
        out.SetProjection(coord_system.ExportToWkt())
        out.GetRasterBand(1).WriteArray(self.Z.T)


    def plot(self, show_points=True):
        fig = plt.figure('2D Kernel Density')
        ax = fig.add_subplot(111)
        ax.imshow(np.rot90(self.Z),origin='upper', cmap=plt.cm.gist_earth_r,extent=[self.x.min(), self.x.max(), self.y.min(), self.y.max()])
        if show_points:
            ax.plot(self.x, self.y, 'k.', markersize=1)
        ax.set_xlim([self.x.min(), self.x.max()])
        ax.set_ylim([self.y.min(), self.y.max()])
        plt.show()
        
if __name__=="__main__":
    d = dados_corte()
    print d.shape
    #~ m1, m2 = gen_random_data()
    m1,m2 = d[:,1],d[:,0]
    k = Kernel2d(m1,m2,.1)
    k.plot()
    
    
    






