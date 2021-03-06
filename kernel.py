import numpy as np
from scipy import stats as st
from scipy import interpolate
import matplotlib.pyplot as plt
from osgeo import gdal, osr
    
    
class Kernel2d(object):
    def __init__(self, lon, lat,zvals=None, bw=None, size=400):
        self.x = lon
        self.y = lat
        if zvals is None:
            self.zvals = None
        else:
            zvals = np.ma.fix_invalid(zvals)
            self.zvals = zvals.filled(0)
            self.zvals = self.zvals - min(self.zvals) #make z positive with minimum at 0
        
        self.bw = bw
        self.values = np.vstack([self.x, self.y])
        self.X, self.Y = np.mgrid[self.x.min():self.x.max():size*1j,
                                  self.y.min():self.y.max():size*1j]
        self.positions = np.vstack([self.X.ravel(), self.Y.ravel()])

        
    def run(self):
        self.kernel = st.gaussian_kde(self.values, self.bw)
        print "==> Factor: ", self.kernel.factor
        self.Z = np.reshape(self.kernel(self.positions).T, self.X.shape)
        if self.zvals is not None: #Small z is the variable associates with z values for points
            self.Z = self._weigh()
        self.Z = self.Z.clip(0) * 100.0/self.Z.max()#making sure there are no negative values
        return self.X, self.Y, self.Z
    
    def _weigh(self):
        """
        Weigh the KDE with values provided for each point.
        """
        #print self.zvals
        #~ weights = interpolate.griddata(np.array([self.x, self.y]).T, self.zvals,(self.X,self.Y),method='cubic')
        rbf = interpolate.Rbf(self.x,self.y,self.zvals, function='linear')
        weights = rbf(self.X,self.Y)
        #print weights, self.Z
        weights /= np.nansum(weights)
        Z = self.Z * weights
        return Z
        
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
    #~ d = dados_corte()
    #~ print d.shape
    m1, m2 = gen_random_data()
    m1,m2 = d[:,1],d[:,0]
    k = Kernel2d(m1,m2,.1)
    k.plot()
    
    
    






