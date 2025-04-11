#include <stdio.h>
#include <stdlib.h>

#define ROWS        480
#define COLUMNS     640
#define sqr(x)      ((x)*(x))

void save_image(const char *filename, unsigned char image[][COLUMNS], int rows, int cols) {
    FILE *fp = fopen(filename, "wb");
    if (fp == NULL) {
        fprintf(stderr, "error: couldn't open %s for writing\n", filename);
        exit(1);
    }

    for (int i = 0; i < rows; i++) {
        fwrite(image[i], 1, cols, fp);
    }

    fclose(fp);
}

int main(int argc, char **argv)
{
    int i, j;

    FILE *fp;
    const char *ifile = "/home/kimsooyoung/Documents/Study/eecs_203a/hw1/triangle.raw";
    const char *ofile = "/home/kimsooyoung/Documents/Study/eecs_203a/hw1/test.raw";
    const char *subsample4_file = "/home/kimsooyoung/Documents/Study/eecs_203a/hw1/triangles4.raw";
    const char *subsample16_file = "/home/kimsooyoung/Documents/Study/eecs_203a/hw1/triangles16.raw";
    const char *restore4_file = "/home/kimsooyoung/Documents/Study/eecs_203a/hw1/restored4.raw";
    const char *restore16_file = "/home/kimsooyoung/Documents/Study/eecs_203a/hw1/restored16.raw";

    unsigned char image[ROWS][COLUMNS];
    unsigned char subsample4[ROWS / 4][COLUMNS / 4];
    unsigned char subsample16[ROWS / 16][COLUMNS / 16];
    unsigned char restored4[ROWS][COLUMNS];
    unsigned char restored16[ROWS][COLUMNS];

    // Load original image
    if ((fp = fopen(ifile, "rb")) == NULL) {
        fprintf(stderr, "error: couldn't open %s\n", ifile);
        exit(1);
    }

	// validation
    for (i = 0; i < ROWS; i++) {
        if (fread(image[i], 1, COLUMNS, fp) != COLUMNS) {
            fprintf(stderr, "error: couldn't read enough data from %s\n", ifile);
            exit(1);
        }
    }

	if (( fp = fopen( ofile, "wb" )) == NULL ){
		fprintf( stderr, "error: could not open %s\n", ofile );
		exit( 1 );
	}
	for ( i = 0 ; i < ROWS ; i++ ) fwrite( image[i], 1, COLUMNS, fp );

    // Subsample by 4
    for (i = 0; i < ROWS / 4; i++) {
        for (j = 0; j < COLUMNS / 4; j++) {
            subsample4[i][j] = image[i * 4][j * 4];
        }
    }

    // Save subsample by 4
    fp = fopen(subsample4_file, "wb");
    for (i = 0; i < ROWS / 4; i++) {
        fwrite(subsample4[i], 1, COLUMNS / 4, fp);
    }
    fclose(fp);

    // Subsample by 16
    for (i = 0; i < ROWS / 16; i++) {
        for (j = 0; j < COLUMNS / 16; j++) {
            subsample16[i][j] = image[i * 16][j * 16];
        }
    }

    // Save subsample by 16
    fp = fopen(subsample16_file, "wb");
    for (i = 0; i < ROWS / 16; i++) {
        fwrite(subsample16[i], 1, COLUMNS / 16, fp);
    }
    fclose(fp);

    // Restore from 4x subsample (nearest neighbor)
    for (i = 0; i < ROWS; i++) {
        for (j = 0; j < COLUMNS; j++) {
            restored4[i][j] = subsample4[i / 4][j / 4];
        }
    }

    // Save restored 4x image
    fp = fopen(restore4_file, "wb");
    for (i = 0; i < ROWS; i++) {
        fwrite(restored4[i], 1, COLUMNS, fp);
    }
    fclose(fp);

    // Restore from 16x subsample (nearest neighbor)
    for (i = 0; i < ROWS; i++) {
        for (j = 0; j < COLUMNS; j++) {
            restored16[i][j] = subsample16[i / 16][j / 16];
        }
    }

    // Save restored 16x image
    fp = fopen(restore16_file, "wb");
    for (i = 0; i < ROWS; i++) {
        fwrite(restored16[i], 1, COLUMNS, fp);
    }
    fclose(fp);

    return 0;
}
