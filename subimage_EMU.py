# script to be run in CASA
################################################################################
#
# This section: hard coded names

# where the data files are stored 
directory = '/Volumes/TARDIS/Work/askap/'

#alternative: read in these parameters from a .txt file. 
import numpy as np
sources=np.loadtxt('EMUsources.txt',dtype='str')

# file names of the full stokes cubes and continuum EMU images
i_EMU_filename = '/Volumes/NARNIA/fullfields/image.restored.i.SB10083.contcube.conv.fits'
q_EMU_filename = '/Volumes/NARNIA/fullfields/image.restored.q.SB10083.contcube.conv.fits'
u_EMU_filename = '/Volumes/NARNIA/fullfields/image.restored.u.SB10083.contcube.conv.fits'
cont_EMU_filename= '/Volumes/NARNIA/fullfields/image.i.SB10083.cont.taylor.0.restored.conv.fits'

i_POSSUM_filename='/Volumes/NARNIA/fullfields/image.restored.i.SB10040.contcube.fits'
q_POSSUM_filename='/Volumes/NARNIA/fullfields/image.restored.q.SB10040.contcube.fits'
u_POSSUM_filename='/Volumes/NARNIA/fullfields/image.restored.u.SB10040.contcube.fits'
cont_POSSUM_filename='/Volumes/NARNIA/fullfields/image.i.SB10040.cont.taylor.0.restored.fits'


for i in range(0,sources.shape[0]):
	#for i in range(0,len(sources)):
	objectname=sources[i,0]
	POSSUMSB=sources[i,1]
	EMUSB=sources[i,2]
	rms=sources[i,3]
	#sourcecentre=sources[i,4]
	region=sources[i,5]
	print(objectname)

	################################################################################
	#Image reading in and cropping
	wise_filename=directory+objectname+'/'+objectname+'_wise.fits'
	sumss_filename=directory+objectname+'/'+objectname+'_sumss.fits'
	gleam_filename=directory+objectname+'/'+objectname+'_gleam.fits'

	# do the seperation
	imsubimage(imagename=i_EMU_filename,outfile='i_EMU_im_temp',region=region,overwrite=True,dropdeg=True)
	imsubimage(imagename=q_EMU_filename,outfile='q_EMU_im_temp',region=region,overwrite=True,dropdeg=True)
	imsubimage(imagename=u_EMU_filename,outfile='u_EMU_im_temp',region=region,overwrite=True,dropdeg=True)
	imsubimage(imagename=cont_EMU_filename,outfile='EMU_cont_im_temp',region=region,overwrite=True,dropdeg=True)
	imsubimage(imagename=cont_POSSUM_filename,outfile='POSSUM_cont_temp',region=region,overwrite=True,dropdeg=True)
	imsubimage(imagename=i_POSSUM_filename,outfile='i_POSSUM_im_temp',region=region,overwrite=True,dropdeg=True)
	imsubimage(imagename=q_POSSUM_filename,outfile='q_POSSUM_im_temp',region=region,overwrite=True,dropdeg=True)
	imsubimage(imagename=u_POSSUM_filename,outfile='u_POSSUM_im_temp',region=region,overwrite=True,dropdeg=True)

	#smooth out the POSSUM and EMU images 
	imsmooth(imagename='i_EMU_im_temp',major="18arcsec",minor="18arcsec",pa="0deg",targetres=True,outfile='i_EMU_smoothed_temp')
	imsmooth(imagename='q_EMU_im_temp',major="18arcsec",minor="18arcsec",pa="0deg",targetres=True,outfile='q_EMU_smoothed_temp')
	imsmooth(imagename='u_EMU_im_temp',major="18arcsec",minor="18arcsec",pa="0deg",targetres=True,outfile='u_EMU_smoothed_temp')
	imsmooth(imagename='EMU_cont_im_temp',major="18arcsec",minor="18arcsec",pa="0deg",targetres=True,outfile='cont_EMU_smoothed_temp')
	imsmooth(imagename='i_POSSUM_im_temp',major="18arcsec",minor="18arcsec",pa="0deg",targetres=True,outfile='i_POSSUM_smoothed_temp')
	imsmooth(imagename='q_POSSUM_im_temp',major="18arcsec",minor="18arcsec",pa="0deg",targetres=True,outfile='q_POSSUM_smoothed_temp')
	imsmooth(imagename='u_POSSUM_im_temp',major="18arcsec",minor="18arcsec",pa="0deg",targetres=True,outfile='u_POSSUM_smoothed_temp')
	imsmooth(imagename='POSSUM_cont_temp',major="18arcsec",minor="18arcsec",pa="0deg",targetres=True,outfile='cont_POSSUM_smoothed_temp')

	#regrid to POSSUM grid
	imregrid(imagename='i_EMU_smoothed_temp',template='POSSUM_cont_temp',output='i_EMU_regrid_temp')
	imregrid(imagename='q_EMU_smoothed_temp',template='POSSUM_cont_temp',output='q_EMU_regrid_temp')
	imregrid(imagename='u_EMU_smoothed_temp',template='POSSUM_cont_temp',output='u_EMU_regrid_temp')
	imregrid(imagename='cont_EMU_smoothed_temp',template='POSSUM_cont_temp',output='cont_EMU_regrid_temp')
	imregrid(imagename='i_POSSUM_smoothed_temp',template='POSSUM_cont_temp',output='i_POSSUM_regrid_temp')
	imregrid(imagename='q_POSSUM_smoothed_temp',template='POSSUM_cont_temp',output='q_POSSUM_regrid_temp')
	imregrid(imagename='u_POSSUM_smoothed_temp',template='POSSUM_cont_temp',output='u_POSSUM_regrid_temp')
	
	#non-askap images
	imregrid(imagename=wise_filename,template='EMU_cont_im_temp',output='wise_temp')
	imsubimage(imagename='wise_temp',outfile='wise_regrid_temp',region=region,overwrite=True,dropdeg=True)
	exportfits(imagename='wise_regrid_temp',fitsimage=objectname+'_wise_regrid.fits',overwrite=True)
	imregrid(imagename=sumss_filename,template='EMU_cont_im_temp',output='sumss_temp')
	imsubimage(imagename='sumss_temp',outfile='sumss_regrid_temp',region=region,overwrite=True,dropdeg=True)
	exportfits(imagename='sumss_regrid_temp',fitsimage=objectname+'_sumss_regrid.fits',overwrite=True)
	imregrid(imagename=gleam_filename,template='EMU_cont_im_temp',output='gleam_temp')
	imsubimage(imagename='gleam_temp',outfile='gleam_regrid_temp',region=region,overwrite=True,dropdeg=True)
	exportfits(imagename='gleam_regrid_temp',fitsimage=objectname+'_gleam_regrid.fits',overwrite=True)


	# convert from CASA images to .fits
	exportfits(imagename='i_EMU_smoothed_temp',fitsimage=objectname+'_i_smooth.fits',overwrite=True)
	exportfits(imagename='q_EMU_smoothed_temp',fitsimage=objectname+'_q_smooth.fits',overwrite=True)
	exportfits(imagename='u_EMU_smoothed_temp',fitsimage=objectname+'_u_smooth.fits',overwrite=True)
	exportfits(imagename='cont_EMU_smoothed_temp',fitsimage=objectname+'_cont_smooth.fits',overwrite=True)
	exportfits(imagename='i_POSSUM_smoothed_temp',fitsimage=objectname+'_i_POSSUMsmooth.fits',overwrite=True)
	exportfits(imagename='q_POSSUM_smoothed_temp',fitsimage=objectname+'_q_POSSUMsmooth.fits',overwrite=True)
	exportfits(imagename='u_POSSUM_smoothed_temp',fitsimage=objectname+'_u_POSSUMsmooth.fits',overwrite=True)
	exportfits(imagename='cont_POSSUM_smoothed_temp',fitsimage=objectname+'_cont_POSSUMsmooth.fits',overwrite=True)

	exportfits(imagename='i_EMU_regrid_temp',fitsimage=objectname+'_i_regrid.fits',overwrite=True)
	exportfits(imagename='q_EMU_regrid_temp',fitsimage=objectname+'_q_regrid.fits',overwrite=True)
	exportfits(imagename='u_EMU_regrid_temp',fitsimage=objectname+'_u_regrid.fits',overwrite=True)
	exportfits(imagename='cont_EMU_regrid_temp',fitsimage=objectname+'_cont_regrid.fits',overwrite=True)

	exportfits(imagename='i_EMU_im_temp',fitsimage=objectname+'_i.fits',overwrite=True)
	exportfits(imagename='q_EMU_im_temp',fitsimage=objectname+'_q.fits',overwrite=True)
	exportfits(imagename='u_EMU_im_temp',fitsimage=objectname+'_u.fits',overwrite=True)
	exportfits(imagename='EMU_cont_im_temp',fitsimage=objectname+'_cont.fits',overwrite=True)


	#tidy up
	os.system("rm -r *_temp")
	os.system("mv *{}* {}/".format(objectname,objectname))

os.system("mv *.log casalogs/")
os.system("mv *.last casalogs/")