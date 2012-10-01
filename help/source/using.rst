Using the Plugin
================

This plugins generates a surface representing probability density of points in space. This kind of surface is also called a heatmap.

This surface is obtained with the gaussian_kde function of scipy.stats.kde, to which the points obtained from a vector point layer are passed.

Kernel density estimates are typically calculated from the simple distribution of points, without any value associated with them. This plugin however, allows the user to select a variable in the point layer to represent intensity of the points and, in this case, generates a so called 3D Kernel map, which ammounts to the regular kernel weighted by the point´s intensity values.

The result is a single-band GEOTIFF image which can then be loaded and viewed on QGIS. This raster layer is parameterized from the vector layer, and will position itself automatically on top of the region it was calculated from. After loading the image you must set a colormap on the image in order to see the kernel density map. giving it some transparency is also nice to see the point pattern together with it.

This plugins defaults to calculationg the Density over all the points in the selected layer, but can also be configured to use only selected points. 
