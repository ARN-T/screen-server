#include <stdio.h>
#ifdef __cplusplus
extern "C" {
#endif

void fix_segment(char segment_array[]);
void invert_segment(char segment_array[]);
void bmp2segment(char bmp_1[], char bmp_2[], char output_array[]);
void myprint(void);

void myprint() {
	printf("Hello world\n");
}

void fix_segment(char segment_array[]) {

	/* Potential hotfix */
	segment_array[ 0] = segment_array[ 1];
	segment_array[ 1] = segment_array[ 2];
	segment_array[ 2] = segment_array[ 3];
	segment_array[ 3] = segment_array[ 4];
	segment_array[ 4] = segment_array[ 5];
	segment_array[ 5] = segment_array[ 6];
	segment_array[ 6] = segment_array[ 7];
	segment_array[ 7] = segment_array[ 8];
	segment_array[ 8] = segment_array[ 9];
	segment_array[ 9] = segment_array[10];
	segment_array[10] = segment_array[11];
	segment_array[11] = segment_array[12];
	segment_array[12] = segment_array[13];
	segment_array[13] = segment_array[14];
	segment_array[14] = segment_array[15];
	segment_array[15] = segment_array[16];
	segment_array[16] = segment_array[17];
	segment_array[17] = segment_array[18];
	segment_array[18] = segment_array[19];
	segment_array[19] = segment_array[20];
	segment_array[20] = segment_array[21];
	segment_array[21] = segment_array[22];
	segment_array[22] = segment_array[23];
	segment_array[23] = segment_array[24];
	segment_array[24] = segment_array[25];
	segment_array[25] = segment_array[26];
	segment_array[26] = segment_array[27];
	segment_array[27] = segment_array[28];
	segment_array[28] = segment_array[29];
	segment_array[29] = segment_array[30];
	segment_array[30] = segment_array[31];
	segment_array[31] = segment_array[32];
	segment_array[32] = segment_array[33];
	segment_array[33] = segment_array[34];
	segment_array[34] = segment_array[35];
	segment_array[35] = segment_array[36];
	segment_array[36] = segment_array[37];
	segment_array[37] = segment_array[38];
	segment_array[38] = segment_array[39];
	segment_array[39] = segment_array[40];
}

void invert_segment(char segment_array[]) {
	
	/* Optimized function for segment inversion (swap bright pixels for dark and vice versa) */
	/* This is done by XORing all used bytes with 0XFF, flipping every bit in the bitmaps */

	segment_array[ 0] ^= 0xFF;
	segment_array[ 1] ^= 0xFF;
	segment_array[ 2] ^= 0xFF;
	segment_array[ 3] ^= 0xFF;
	segment_array[ 4] ^= 0xFF;
	segment_array[ 5] ^= 0xFF;
	segment_array[ 6] ^= 0xFF;
	segment_array[ 7] ^= 0xFF;
	segment_array[ 8] ^= 0xFF;
	segment_array[ 9] ^= 0xFF;
	segment_array[10] ^= 0xFF;
	segment_array[11] ^= 0xFF;
	segment_array[12] ^= 0xFF;
	segment_array[13] ^= 0xFF;
	segment_array[14] ^= 0xFF;
	segment_array[15] ^= 0xFF;
	segment_array[16] ^= 0xFF;
	segment_array[17] ^= 0xFF;
	segment_array[18] ^= 0xFF;
	segment_array[19] ^= 0xFF;
	segment_array[20] ^= 0xFF;
	segment_array[21] ^= 0xFF;
	segment_array[22] ^= 0xFF;
	segment_array[23] ^= 0xFF;
	segment_array[24] ^= 0xFF;
	segment_array[25] ^= 0xFF;
	segment_array[26] ^= 0xFF;
	segment_array[27] ^= 0xFF;
	segment_array[28] ^= 0xFF;
	segment_array[29] ^= 0xFF;
	segment_array[30] ^= 0xFF;
	segment_array[31] ^= 0xFF;
	segment_array[32] ^= 0xFF;
	segment_array[33] ^= 0xFF;
	segment_array[34] ^= 0xFF;
	segment_array[35] ^= 0xFF;
	segment_array[36] ^= 0xFF;
	segment_array[37] ^= 0xFF;
	segment_array[38] ^= 0xFF;
	segment_array[39] ^= 0xFF;
}

void bmp2segment(char bmp_1[],char bmp_2[], char output_array[]) {

	/* The arguments bmp_1 and bmp_2 are raw monochrome bitmaps */
	/* The format is 8 pixels wide by 16 pixels tall, 0 is bright and 1 is dark */
	/* These will typically be a single rendered character each */

	/* Each newline separated block in the code equals one row of pixels */

	/*** Top half of 1st bitmap ***/

	output_array[12] += bmp_1[  0] << 0;
	output_array[ 2] += bmp_1[  1] << 0;
	output_array[13] += bmp_1[  2] << 2;
	output_array[ 3] += bmp_1[  3] << 2;
	output_array[14] += bmp_1[  4] << 5;
	output_array[ 4] += bmp_1[  5] << 5;
	output_array[19] += bmp_1[  6] << 7;
	output_array[ 9] += bmp_1[  7] << 7;

	output_array[12] += bmp_1[  8] << 1;
	output_array[ 2] += bmp_1[  9] << 1;
	output_array[13] += bmp_1[ 10] << 3;
	output_array[ 3] += bmp_1[ 11] << 3;
	output_array[14] += bmp_1[ 12] << 4;
	output_array[ 4] += bmp_1[ 13] << 4;
	output_array[19] += bmp_1[ 14] << 6;
	output_array[ 9] += bmp_1[ 15] << 6;

	output_array[12] += bmp_1[ 16] << 2;
	output_array[ 2] += bmp_1[ 17] << 2;
	output_array[13] += bmp_1[ 18] << 4;
	output_array[ 3] += bmp_1[ 19] << 4;
	output_array[14] += bmp_1[ 20] << 3;
	output_array[ 4] += bmp_1[ 21] << 3;
	output_array[19] += bmp_1[ 22] << 5;
	output_array[ 9] += bmp_1[ 23] << 5;

	output_array[12] += bmp_1[ 24] << 3;
	output_array[ 2] += bmp_1[ 25] << 3;
	output_array[13] += bmp_1[ 26] << 1;
	output_array[ 3] += bmp_1[ 27] << 1;
	output_array[14] += bmp_1[ 28] << 6;
	output_array[ 4] += bmp_1[ 29] << 6;
	output_array[19] += bmp_1[ 30] << 4;
	output_array[ 9] += bmp_1[ 31] << 4;

	output_array[12] += bmp_1[ 32] << 4;
	output_array[ 2] += bmp_1[ 33] << 4;
	output_array[13] += bmp_1[ 34] << 5;
	output_array[ 3] += bmp_1[ 35] << 5;
	output_array[14] += bmp_1[ 36] << 2;
	output_array[ 4] += bmp_1[ 37] << 2;
	output_array[19] += bmp_1[ 38] << 3;
	output_array[ 9] += bmp_1[ 39] << 3;

	output_array[12] += bmp_1[ 40] << 5;
	output_array[ 2] += bmp_1[ 41] << 5;
	output_array[13] += bmp_1[ 42] << 6;
	output_array[ 3] += bmp_1[ 43] << 6;
	output_array[14] += bmp_1[ 44] << 1;
	output_array[ 4] += bmp_1[ 45] << 1;
	output_array[19] += bmp_1[ 46] << 2;
	output_array[ 9] += bmp_1[ 47] << 2;

	output_array[12] += bmp_1[ 48] << 6;
	output_array[ 2] += bmp_1[ 49] << 6;
	output_array[13] += bmp_1[ 50] << 7;
	output_array[ 3] += bmp_1[ 51] << 7;
	output_array[14] += bmp_1[ 52] << 0;
	output_array[ 4] += bmp_1[ 53] << 0;
	output_array[19] += bmp_1[ 54] << 1;
	output_array[ 9] += bmp_1[ 55] << 1;

	output_array[12] += bmp_1[ 56] << 7;
	output_array[ 2] += bmp_1[ 57] << 7;
	output_array[13] += bmp_1[ 58] << 0;
	output_array[ 3] += bmp_1[ 59] << 0;
	output_array[14] += bmp_1[ 60] << 7;
	output_array[ 4] += bmp_1[ 61] << 7;
	output_array[19] += bmp_1[ 62] << 0;
	output_array[ 9] += bmp_1[ 63] << 0;

	/*** Bottom half of 1st bitmap ***/

	output_array[35] += bmp_1[ 64] << 0;
	output_array[25] += bmp_1[ 65] << 0;
	output_array[36] += bmp_1[ 66] << 7;
	output_array[26] += bmp_1[ 67] << 7;
	output_array[37] += bmp_1[ 68] << 0;
	output_array[27] += bmp_1[ 69] << 0;
	output_array[38] += bmp_1[ 70] << 7;
	output_array[28] += bmp_1[ 71] << 7;

	output_array[35] += bmp_1[ 72] << 1;
	output_array[25] += bmp_1[ 73] << 1;
	output_array[36] += bmp_1[ 74] << 0;
	output_array[26] += bmp_1[ 75] << 0;
	output_array[37] += bmp_1[ 76] << 7;
	output_array[27] += bmp_1[ 77] << 7;
	output_array[38] += bmp_1[ 78] << 6;
	output_array[28] += bmp_1[ 79] << 6;

	output_array[35] += bmp_1[ 80] << 2;
	output_array[25] += bmp_1[ 81] << 2;
	output_array[36] += bmp_1[ 82] << 1;
	output_array[26] += bmp_1[ 83] << 1;
	output_array[37] += bmp_1[ 84] << 6;
	output_array[27] += bmp_1[ 85] << 6;
	output_array[38] += bmp_1[ 86] << 5;
	output_array[28] += bmp_1[ 87] << 5;

	output_array[35] += bmp_1[ 88] << 3;
	output_array[25] += bmp_1[ 89] << 3;
	output_array[36] += bmp_1[ 90] << 2;
	output_array[26] += bmp_1[ 91] << 2;
	output_array[37] += bmp_1[ 92] << 5;
	output_array[27] += bmp_1[ 93] << 5;
	output_array[38] += bmp_1[ 94] << 4;
	output_array[28] += bmp_1[ 95] << 4;

	output_array[35] += bmp_1[ 96] << 4;
	output_array[25] += bmp_1[ 97] << 4;
	output_array[36] += bmp_1[ 98] << 6;
	output_array[26] += bmp_1[ 99] << 6;
	output_array[37] += bmp_1[100] << 1;
	output_array[27] += bmp_1[101] << 1;
	output_array[38] += bmp_1[102] << 3;
	output_array[28] += bmp_1[103] << 3;

	output_array[35] += bmp_1[104] << 5;
	output_array[25] += bmp_1[105] << 5;
	output_array[36] += bmp_1[106] << 3;
	output_array[26] += bmp_1[107] << 3;
	output_array[37] += bmp_1[108] << 4;
	output_array[27] += bmp_1[109] << 4;
	output_array[38] += bmp_1[110] << 2;
	output_array[28] += bmp_1[111] << 2;

	output_array[35] += bmp_1[112] << 6;
	output_array[25] += bmp_1[113] << 6;
	output_array[36] += bmp_1[114] << 4;
	output_array[26] += bmp_1[115] << 4;
	output_array[37] += bmp_1[116] << 3;
	output_array[27] += bmp_1[117] << 3;
	output_array[38] += bmp_1[118] << 1;
	output_array[28] += bmp_1[119] << 1;

	output_array[35] += bmp_1[120] << 7;
	output_array[25] += bmp_1[121] << 7;
	output_array[36] += bmp_1[122] << 5;
	output_array[26] += bmp_1[123] << 5;
	output_array[37] += bmp_1[124] << 2;
	output_array[27] += bmp_1[125] << 2;
	output_array[38] += bmp_1[126] << 0;
	output_array[28] += bmp_1[127] << 0;

	/*** Top half of 2nd bitmap ***/

	output_array[18] += bmp_2[  0] << 0;
	output_array[ 8] += bmp_2[  1] << 0;
	output_array[17] += bmp_2[  2] << 2;
	output_array[ 7] += bmp_2[  3] << 2;
	output_array[16] += bmp_2[  4] << 5;
	output_array[ 6] += bmp_2[  5] << 5;
	output_array[15] += bmp_2[  6] << 7;
	output_array[ 5] += bmp_2[  7] << 7;

	output_array[18] += bmp_2[  8] << 1;
	output_array[ 8] += bmp_2[  9] << 1;
	output_array[17] += bmp_2[ 10] << 3;
	output_array[ 7] += bmp_2[ 11] << 3;
	output_array[16] += bmp_2[ 12] << 4;
	output_array[ 6] += bmp_2[ 13] << 4;
	output_array[15] += bmp_2[ 14] << 6;
	output_array[ 5] += bmp_2[ 15] << 6;

	output_array[18] += bmp_2[ 16] << 2;
	output_array[ 8] += bmp_2[ 17] << 2;
	output_array[17] += bmp_2[ 18] << 4;
	output_array[ 7] += bmp_2[ 19] << 4;
	output_array[16] += bmp_2[ 20] << 3;
	output_array[ 6] += bmp_2[ 21] << 3;
	output_array[15] += bmp_2[ 22] << 5;
	output_array[ 5] += bmp_2[ 23] << 5;

	output_array[18] += bmp_2[ 24] << 3;
	output_array[ 8] += bmp_2[ 25] << 3;
	output_array[17] += bmp_2[ 26] << 1;
	output_array[ 7] += bmp_2[ 27] << 1;
	output_array[16] += bmp_2[ 28] << 6;
	output_array[ 6] += bmp_2[ 29] << 6;
	output_array[15] += bmp_2[ 30] << 4;
	output_array[ 5] += bmp_2[ 31] << 4;

	output_array[18] += bmp_2[ 32] << 4;
	output_array[ 8] += bmp_2[ 33] << 4;
	output_array[17] += bmp_2[ 34] << 5;
	output_array[ 7] += bmp_2[ 35] << 5;
	output_array[16] += bmp_2[ 36] << 2;
	output_array[ 6] += bmp_2[ 37] << 2;
	output_array[15] += bmp_2[ 38] << 3;
	output_array[ 5] += bmp_2[ 39] << 3;

	output_array[18] += bmp_2[ 40] << 5;
	output_array[ 8] += bmp_2[ 41] << 5;
	output_array[17] += bmp_2[ 42] << 6;
	output_array[ 7] += bmp_2[ 43] << 6;
	output_array[16] += bmp_2[ 44] << 1;
	output_array[ 6] += bmp_2[ 45] << 1;
	output_array[15] += bmp_2[ 46] << 2;
	output_array[ 5] += bmp_2[ 47] << 2;

	output_array[18] += bmp_2[ 48] << 6;
	output_array[ 8] += bmp_2[ 49] << 6;
	output_array[17] += bmp_2[ 50] << 7;
	output_array[ 7] += bmp_2[ 51] << 7;
	output_array[16] += bmp_2[ 52] << 0;
	output_array[ 6] += bmp_2[ 53] << 0;
	output_array[15] += bmp_2[ 54] << 1;
	output_array[ 5] += bmp_2[ 55] << 1;

	output_array[18] += bmp_2[ 56] << 7;
	output_array[ 8] += bmp_2[ 57] << 7;
	output_array[17] += bmp_2[ 58] << 0;
	output_array[ 7] += bmp_2[ 59] << 0;
	output_array[16] += bmp_2[ 60] << 7;
	output_array[ 6] += bmp_2[ 61] << 7;
	output_array[15] += bmp_2[ 62] << 0;
	output_array[ 5] += bmp_2[ 63] << 0;

	/*** Bottom half of 2nd bitmap ***/

	output_array[39] += bmp_2[ 64] << 0;
	output_array[29] += bmp_2[ 65] << 0;
	output_array[34] += bmp_2[ 66] << 7;
	output_array[24] += bmp_2[ 67] << 7;
	output_array[33] += bmp_2[ 68] << 0;
	output_array[23] += bmp_2[ 69] << 0;
	output_array[32] += bmp_2[ 70] << 7;
	output_array[22] += bmp_2[ 71] << 7;

	output_array[39] += bmp_2[ 72] << 1;
	output_array[29] += bmp_2[ 73] << 1;
	output_array[34] += bmp_2[ 74] << 0;
	output_array[24] += bmp_2[ 75] << 0;
	output_array[33] += bmp_2[ 76] << 7;
	output_array[23] += bmp_2[ 77] << 7;
	output_array[32] += bmp_2[ 78] << 6;
	output_array[22] += bmp_2[ 79] << 6;

	output_array[39] += bmp_2[ 80] << 2;
	output_array[29] += bmp_2[ 81] << 2;
	output_array[34] += bmp_2[ 82] << 1;
	output_array[24] += bmp_2[ 83] << 1;
	output_array[33] += bmp_2[ 84] << 6;
	output_array[23] += bmp_2[ 85] << 6;
	output_array[32] += bmp_2[ 86] << 5;
	output_array[22] += bmp_2[ 87] << 5;

	output_array[39] += bmp_2[ 88] << 3;
	output_array[29] += bmp_2[ 89] << 3;
	output_array[34] += bmp_2[ 90] << 2;
	output_array[24] += bmp_2[ 91] << 2;
	output_array[33] += bmp_2[ 92] << 5;
	output_array[23] += bmp_2[ 93] << 5;
	output_array[32] += bmp_2[ 94] << 4;
	output_array[22] += bmp_2[ 95] << 4;

	output_array[39] += bmp_2[ 96] << 4;
	output_array[29] += bmp_2[ 97] << 4;
	output_array[34] += bmp_2[ 98] << 6;
	output_array[24] += bmp_2[ 99] << 6;
	output_array[33] += bmp_2[100] << 1;
	output_array[23] += bmp_2[101] << 1;
	output_array[32] += bmp_2[102] << 3;
	output_array[22] += bmp_2[103] << 3;

	output_array[39] += bmp_2[104] << 5;
	output_array[29] += bmp_2[105] << 5;
	output_array[34] += bmp_2[106] << 3;
	output_array[24] += bmp_2[107] << 3;
	output_array[33] += bmp_2[108] << 4;
	output_array[23] += bmp_2[109] << 4;
	output_array[32] += bmp_2[110] << 2;
	output_array[22] += bmp_2[111] << 2;

	output_array[39] += bmp_2[112] << 6;
	output_array[29] += bmp_2[113] << 6;
	output_array[34] += bmp_2[114] << 4;
	output_array[24] += bmp_2[115] << 4;
	output_array[33] += bmp_2[116] << 3;
	output_array[23] += bmp_2[117] << 3;
	output_array[32] += bmp_2[118] << 1;
	output_array[22] += bmp_2[119] << 1;

	output_array[39] += bmp_2[120] << 7;
	output_array[29] += bmp_2[121] << 7;
	output_array[34] += bmp_2[122] << 5;
	output_array[24] += bmp_2[123] << 5;
	output_array[33] += bmp_2[124] << 2;
	output_array[23] += bmp_2[125] << 2;
	output_array[32] += bmp_2[126] << 0;
	output_array[22] += bmp_2[127] << 0;
}

#ifdef __cplusplus
}
#endif