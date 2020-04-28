//  oled.c Display useful information on the 0.96" OLED display.
//  Uses this library: https://github.com/bitbank2/oled_96
//  Written by mosquito@darlingevil.com, 2019-11-15


#include <stdint.h>
#include <string.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <linux/kernel.h>
#include <sys/sysinfo.h>

#include "oled96.h"

#define SLEEP_SEC 15
#define OLED_SMALL_CHARS 21
#define OLED_NORMAL_CHARS 16
#define OLED_BIG_CHARS 8
#define OLED_LINE_SIZE 128
#define OLED_SMALL_SPACES "                      "
#define OLED_NORMAL_SPACES "                 "
#define OLED_BIG_SPACES "         "

int
shell_run(char* cmd, char* output, int size)
{
  FILE *fp;

  if ((fp = (FILE*) popen(cmd, "r")) != NULL) {
    char buf[BUFSIZ];
    int length=0;

    if (fgets(buf, BUFSIZ, fp) != NULL) {
      pclose(fp);
      length = strlen(buf);
      if (length > 0 && length < size) {
        (void) bzero(output,length);
        (void) bcopy(buf,output,length-1);
        return 0;
      }
    }
  }
  return -1;
}

int
oled_center_small(int line, char* message)
{
  int len = strlen(message);

  if (len <= OLED_SMALL_CHARS) {
    char tmp[BUFSIZ];
    char* padding = "";
    int half = (OLED_SMALL_CHARS - strlen(message)) / 2;

    if (half > 0 && half < (OLED_SMALL_CHARS - 1)) padding = &(OLED_SMALL_SPACES[OLED_SMALL_CHARS - half]);
    (void) snprintf(tmp, BUFSIZ, "%s%s%s", padding, message, OLED_SMALL_SPACES);
    oledWriteString(0, line, tmp, FONT_SMALL);
    return(1);
  }
  return(0);
}


int
oled_center_normal(int line, char* message)
{
  int len = strlen(message);

  if (len <= OLED_NORMAL_CHARS) {
    char tmp[BUFSIZ];
    char* padding = "";
    int half = (OLED_NORMAL_CHARS - strlen(message)) / 2;

    if (half > 0 && half < (OLED_NORMAL_CHARS - 1)) padding = &(OLED_NORMAL_SPACES[OLED_NORMAL_CHARS - half]);
    (void) snprintf(tmp, BUFSIZ, "%s%s%s", padding, message, OLED_NORMAL_SPACES);
    oledWriteString(0, line, tmp, FONT_NORMAL);
    return(1);
  }
  return(0);
}

int
oled_center_big(int line, char* message)
{
  int len = strlen(message);

  if (len <= OLED_BIG_CHARS) {
    char tmp[BUFSIZ];
    char* padding = "";
    int half = (OLED_BIG_CHARS - strlen(message)) / 2;

    if (half > 0 && half < (OLED_BIG_CHARS - 1)) padding = &(OLED_BIG_SPACES[OLED_BIG_CHARS - half]);
    (void) snprintf(tmp, BUFSIZ, "%s%s%s", padding, message, OLED_BIG_SPACES);
    oledWriteString(0, line, tmp, FONT_BIG);
    return(1);
  }
  return(0);
}

int
oled_init()
{
  int iOLEDAddr = 0x3c;
  int iOLEDType = OLED_128x64;
  int bFlip = 0, bInvert = 0;
  int i = -1;
  int iChannel = -1;

  while (i != 0 && iChannel < 2) {
    iChannel++;
    i=oledInit(iChannel, iOLEDAddr, iOLEDType, bFlip, bInvert);
  }
  if (0 != i) {
    return(-1);
  }
  oledFill(0);
  return(0);
}

/*
 * catch interrupts and stop
 */
static volatile int loop = 1;

void
intHandler(int sig)
{
  loop = 0;
}

long
get_uptime()
{
  struct sysinfo s_info;

  (void) sysinfo(&s_info);

  return s_info.uptime;
}

int
main(int argc, char* argv[])
{
  char line[OLED_LINE_SIZE];
  char nodename[BUFSIZ];
  char arch[BUFSIZ];
  char buf[BUFSIZ];

  /* catch interrupts and stop */
  signal(SIGINT, intHandler);

  if (oled_init() < 0) {
    fprintf(stderr, "Unable to initialize I2C bus 0-2, please check your connections: 'i2cdetect -l' and 'i2cdetect -y <channel>'\n");
    exit(1);
  }

  shell_run("uname -n",nodename,BUFSIZ);
  shell_run("uname -m",arch,BUFSIZ);

  while(loop) {
    int k,l = 0;

    /* name */
    (void) snprintf(line, OLED_LINE_SIZE - 1, nodename);
    k = oled_center_normal(l, line); l += k;

    /* host ipaddr */
    (void) snprintf(line, OLED_LINE_SIZE - 1, getenv("LOCAL_IP_ADDRESS"));
    k = oled_center_normal(l, line); l += k;

    /* current time (ZULU) */
    shell_run("date -u '+%T UTC'",buf,BUFSIZ);
    (void) snprintf(line, OLED_LINE_SIZE - 1, buf);
    k = oled_center_normal(l, line); l += k;

    /* uptime */
    int since=get_uptime();
    (void) snprintf(line, OLED_LINE_SIZE - 1, "UP: %d", since);
    k = oled_center_normal(l, line); l += k;

    /* load average */
    shell_run("awk '{ print $1,$2,$3 }' /proc/loadavg",buf,BUFSIZ);
    (void) snprintf(line, OLED_LINE_SIZE - 1, buf);
    k = oled_center_small(l, line); l += k;

    (void) snprintf(line, OLED_LINE_SIZE - 1, arch);
    k = oled_center_small(l, line); l += k;

    for (;l < 8; l++) {
      (void) snprintf(line, OLED_LINE_SIZE - 1, OLED_SMALL_SPACES);
      l += oled_center_small(l, line);
    }

    sleep(SLEEP_SEC);
  }
  exit(0);
}
