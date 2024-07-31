#include <stdio.h>
#include <stdlib.h>
#include <string.h>

unsigned char buf[32 * 24];
unsigned char row[32];
char filename[10];
int main(int argc, char** argv){
    FILE* fp = NULL, *ofp;
    int width, height, idx;
    int count = 1;
    int scale;
    unsigned int enter;
    if (argc < 2) {
        fprintf(stderr, "Wrong usage!!!\n");
        return -1;
    }
    memset(buf, 0, sizeof(buf));
    while (count < argc) {
        if ((fp = fopen(argv[count], "rb")) == NULL) {
            printf("%s\n", argv[count]);
            fprintf(stderr, "Input file corrupted.\n");
            return -1;
        }
        fgets(buf, sizeof(buf), fp);
        fgets(buf, sizeof(buf), fp);
        if (sscanf(buf, "%d %d", &width, &height) != 2) {
            fprintf(stderr, "Image format error.\n");
            fclose(fp);
            return -1;
        }
        if(width > 32 || height > 24){
            fprintf(stderr, "Image is too big.\n");
            fclose(fp);
            return -1;
        }
        fgets(buf, sizeof(buf), fp); // this should be 255
        sscanf(buf, "%d", &scale);
        if(scale != 255){
            fclose(fp);
            return -1;
        }
        //fgets(buf, sizeof(buf), fp);
        //fclose(fp);
        // try to read all the remaining data
        
        fread(buf, 1, 32*24, fp);
        fclose(fp);
        
        ofp = fopen("debug.txt", "at");
        for (int i = 0; i < height; i++) {
            for (int j = 0; j < width; j++) {
                //printf("%4d", buf[i*width+j]);
                if (buf[i*width+j] > 100) { // white 1
                    enter = (enter << 1) | 1;
                }
                else { // black 0
                    enter = enter << 1;
                }
            }
            //printf("\n");
            fprintf(ofp, "%u, ", enter);
        }
        fprintf(ofp, "\n");
        fclose(ofp);
        printf("%i DONE", count);
        count++;
    }
}