#include <stdio.h>
#include <stdlib.h>

#define ROWS		480
#define COLUMNS		640

#define sqr(x)		((x)*(x))

int main( int argc, char **argv )
{
	int		i;
	int		threshold;
	FILE		*fp;
	char		*ifile, *ofile;
	unsigned char	image[ROWS][COLUMNS];
	
	ifile = "/home/kimsooyoung/Documents/Study/eecs_203a/hw1/triangle.raw";

	// TODO: subsamples the image by 4 to 120 * 160 img
	subsample4 = "/home/kimsooyoung/Documents/Study/eecs_203a/hw1/triangles4.raw";
	// TODO: subsamples the image by 16 to 30 * 40 img
	subsample16 = "/home/kimsooyoung/Documents/Study/eecs_203a/hw1/triangles4.raw";
	// TODO: use nearest neighbor interpolation to transform 4 subsampled image to a 480 * 640 image
	restore4 = "/home/kimsooyoung/Documents/Study/eecs_203a/hw1/triangles4.raw";
	// TODO: use nearest neighbor interpolation to transform 16 subsampled image to a 480 * 640 image
	restore16 = "/home/kimsooyoung/Documents/Study/eecs_203a/hw1/triangles4.raw";

	if (( fp = fopen( ifile, "rb" )) == NULL )
	{
	  fprintf( stderr, "error: couldn't open %s\n", ifile );
	  exit( 1 );
	}

	for ( i = 0; i < ROWS ; i++ ){
		// fprintf("")
		if ( fread( image[i], 1, COLUMNS, fp ) != COLUMNS ){
			fprintf( stderr, "error: couldn't read enough stuff\n" );
			exit( 1 );
		}
	}
	fclose( fp );

	// TODO: subsamples the image by 4 to 120 * 160 img and save
	



	if (( fp = fopen( ofile, "wb" )) == NULL ){
		fprintf( stderr, "error: could not open %s\n", ofile );
		exit( 1 );
	}
	for ( i = 0 ; i < ROWS ; i++ ) 
		fwrite( image[i], 1, COLUMNS, fp );

	fclose( fp );

	return 0;
}

