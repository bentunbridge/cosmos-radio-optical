A brief overview of each script provided in this directory.

Imaging from visabilities.

COSMOS_calib.py: This outlines the calibration steps taken in this work. A brief overview of this is provided in section 2.1.1 Data Reduction.

clean_cal_imaging.py: once calibrated the imaging can take place. The masking of sources was done my hand during the clean task imaging procedure. The data was initially cleaned to the threshold with no primary beam correction, then additionally cleaned with a primary beam correction to a level if 0.5. This process is performed on each of the 23 COSMOS pointing individually, creating 23 individual images.

linear_mosaic.py: This final script simply combines the resultant 23 COSMOS images into one via a linear mosaic technique in casa.


The Simulations.

simulate_VLA_cosmos_catalog.py: This script uses the GalSim package to simulate many Gaussian sources in positions recorded from previous source catalogues. This is done separately for each of the 23 pointings in the COSMOS survey.

fits2image.py: This script converts the output of the previous script from a fits file to a .image file.


