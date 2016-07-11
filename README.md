
This page provides supplementary material to arXiv:number

Radio-Optical Galaxy Shape Correlations in theCOSMOS Field
Ben Tunbridge, Ian Harrison, Michael L. Brown

Abstract:
We investigate the correlations in galaxy shapes between optical and radio wavelengths using archival observations of the COSMOS field. Cross-correlation studies between different wavebands will become increasingly important for precision cosmology as future large surveys may be dominated by systematic rather than statistical errors. In the case of weak lensing, galaxy shapes must be measured to extraordinary accuracy (shear systematics of < 0.01%) in order to achieve good constraints on dark energy parameters. By using shape information from overlapping surveys in optical and radio bands, robustness to systematics may be significantly improved without loss of constraining power. Here we use HST-ACS optical data, VLA radio data, and extensive simulations to investigate both our ability to make precision measurements of source shapes from realistic radio data, and to constrain the intrinsic astrophysical scatter between the shapes of galaxies as measured in the optical and radio wavebands. By producing a new image from the VLA-COSMOS L-band radio visibility data that is well suited to galaxy shape measurements, we are able to extract precise measurements of galaxy position angles. Comparing to corresponding measurements from the HST optical image, we set a lower limit on the intrinsic astrophysical scatter in position angles, between the optical and radio bands, of sigma_alpha > 0.212 pi radians (or 38.2 degrees) at a 95% confidence level.

The following can be found at:
ftp://ftp.jb.man.ac.uk/pub/cosmos-radio-optical/

Content:

data/:
We include the data used in this study in this directory. The calibrated radio visabilities can be found in measurement set form, split up into individual pointings. These are labelled 1 to 23 and found as data/msfiles/COSMOS_F??.ms.
The combined mosaic image (COSMOS_VLA_image.fits) is also found in the data directory. This is the final image used in the shape analysis.

catalogs/:
We additionally provide the source catalogs. This includes the measured shape outputs from our IM3SHAPE based galaxy shape analysis.
cosmos_vla_shapes_natural.fits is the catalog detailing shape recovery from the image created using a natural weighting scheme.
cosmos_vla_shapes_uniform.fits is the catalog detailing shape recovery from the image created using a uniform weighting scheme.

Radio_optical_match_fit_with_zurich_morphology_natural.fits is a catalog detailing the optical and radio shape comparisions. The radio shapes are taken from the natural weighting scheme image in this case and only included if a suitable match to an optical source is found. This included a positional match to within a 1 arcsecond tolorence.

radio_optical_cutouts/:
A side by side image comparison of radio and optical shapes are provided in the directory radio_optical_cutouts/. In each case the cutouts display an equal area of 11:2"x11:2" in the optical (left) and radio (right).



Send any questions to: Ben Tunbridge (benjamin.tunbridge@manchester.ac.uk).

###########################################
Last updated 08/07/2016
